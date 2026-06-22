"""Create a heldout fold ordering for Phase 3 split-stability runs."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_io import load_goals_jsonl, write_goals_jsonl
from schema import Goal


def with_split_metadata(goal: Goal, *, fold_index: int, role: str, order: int) -> Goal:
    metadata = dict(goal.metadata)
    metadata["phase3_split_fold"] = fold_index
    metadata["phase3_split_role"] = role
    metadata["phase3_split_order"] = order
    return Goal(
        goal_id=goal.goal_id,
        goal_state=goal.goal_state,
        candidates=goal.candidates,
        proof_core=goal.proof_core,
        local_premises=goal.local_premises,
        metadata=metadata,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--fold-index", type=int, required=True)
    parser.add_argument("--fold-size", type=int, default=500)
    args = parser.parse_args()

    goals = load_goals_jsonl(args.input)
    if args.fold_size <= 0:
        raise ValueError("--fold-size must be positive")
    n_folds, remainder = divmod(len(goals), args.fold_size)
    if remainder:
        raise ValueError(f"{len(goals)} goals is not divisible by fold size {args.fold_size}")
    if not 0 <= args.fold_index < n_folds:
        raise ValueError(f"--fold-index must be in [0, {n_folds - 1}]")

    start = args.fold_index * args.fold_size
    end = start + args.fold_size
    eval_goals = goals[start:end]
    train_goals = goals[:start] + goals[end:]
    ordered = [
        with_split_metadata(goal, fold_index=args.fold_index, role="train", order=idx)
        for idx, goal in enumerate(train_goals)
    ] + [
        with_split_metadata(goal, fold_index=args.fold_index, role="eval", order=idx)
        for idx, goal in enumerate(eval_goals)
    ]
    write_goals_jsonl(ordered, args.out)
    print(
        f"wrote {len(ordered)} goals to {args.out}; "
        f"train={len(train_goals)} eval={len(eval_goals)} fold={args.fold_index}"
    )


if __name__ == "__main__":
    main()
