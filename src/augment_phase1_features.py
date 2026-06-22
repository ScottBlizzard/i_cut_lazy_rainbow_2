"""Add retriever-visible candidate features to an existing Phase 1 goals JSONL."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_io import load_goals_jsonl, write_goals_jsonl
from feature_extraction import build_candidate_features


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    goals = load_goals_jsonl(args.goals)
    for goal in goals:
        theorem_name = str(goal.metadata.get("theorem", goal.goal_id))
        for premise in goal.candidates:
            premise.features = build_candidate_features(
                theorem_name=theorem_name,
                goal_state=goal.goal_state,
                premise_name=premise.name,
                premise_text=premise.text,
                same_file=True,
            )

    write_goals_jsonl(goals, args.out)
    print(f"wrote {len(goals)} feature-augmented goals to {args.out}")


if __name__ == "__main__":
    main()
