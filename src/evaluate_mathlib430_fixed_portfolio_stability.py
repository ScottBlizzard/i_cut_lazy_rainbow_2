#!/usr/bin/env python3
"""Evaluate fixed greedy proof-action portfolios with per-fold stability."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pct(num: int, den: int) -> str:
    if den == 0:
        return "0.0%"
    return f"{100.0 * num / den:.1f}%"


def goal_action_index(results: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    by_goal: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in results:
        by_goal[str(row["goal_id"])][str(row["action"])] = row
    return by_goal


def action_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, action: str) -> bool:
    return bool(by_goal.get(goal, {}).get(action, {}).get("verified"))


def empty_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return action_verified(by_goal, goal, "hammer_empty")


def any_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return any(bool(row.get("verified")) for row in by_goal.get(goal, {}).values())


def strict_goal(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return (not empty_verified(by_goal, goal)) and any_verified(by_goal, goal)


def eval_fixed(by_goal: dict[str, dict[str, dict[str, Any]]], goals: list[str], actions: list[str]) -> int:
    return sum(
        1
        for goal in goals
        if empty_verified(by_goal, goal) or any(action_verified(by_goal, goal, action) for action in actions)
    )


def greedy_portfolios(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    train_goals: list[str],
    actions: list[str],
    max_budget: int,
) -> list[list[str]]:
    selected: list[str] = []
    remaining = list(actions)
    portfolios: list[list[str]] = []
    for _ in range(max_budget):
        scored = [(eval_fixed(by_goal, train_goals, selected + [action]), action) for action in remaining]
        scored.sort(key=lambda item: (-item[0], item[1]))
        best = scored[0][1]
        selected.append(best)
        remaining.remove(best)
        portfolios.append(list(selected))
    return portfolios


def paired_delta(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    portfolio: list[str],
    baseline_action: str,
) -> dict[str, Any]:
    wins: list[str] = []
    losses: list[str] = []
    ties_success = 0
    ties_fail = 0
    for goal in goals:
        portfolio_success = empty_verified(by_goal, goal) or any(
            action_verified(by_goal, goal, action) for action in portfolio
        )
        baseline_success = action_verified(by_goal, goal, baseline_action)
        if portfolio_success and not baseline_success:
            wins.append(goal)
        elif baseline_success and not portfolio_success:
            losses.append(goal)
        elif portfolio_success and baseline_success:
            ties_success += 1
        else:
            ties_fail += 1
    return {
        "wins": wins,
        "losses": losses,
        "ties_success": ties_success,
        "ties_fail": ties_fail,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-json", required=True, type=Path)
    parser.add_argument("--split-json", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-budget", type=int, default=6)
    parser.add_argument("--folds", type=int, default=5)
    args = parser.parse_args()

    matrix = load_json(args.matrix_json)
    split = load_json(args.split_json)
    by_goal = goal_action_index(matrix["results"])
    actions = [
        str(action)
        for action in list(matrix.get("action_names") or sorted({row["action"] for row in matrix["results"]}))
        if str(action) != "hammer_empty"
    ]
    all_goals = list(split["train"]) + list(split["dev"]) + list(split["test"])
    fold_goals = [all_goals[i :: args.folds] for i in range(args.folds)]

    fold_rows: list[dict[str, Any]] = []
    totals = {
        str(k): {
            "n": 0,
            "fixed": 0,
            "empty": 0,
            "oracle": 0,
            "strict_n": 0,
            "strict_fixed": 0,
            "strict_oracle": 0,
        }
        for k in range(1, args.max_budget + 1)
    }
    for fold_idx, heldout in enumerate(fold_goals):
        heldout_set = set(heldout)
        train = [goal for goal in all_goals if goal not in heldout_set]
        portfolios = greedy_portfolios(by_goal, train, actions, args.max_budget)
        strict_heldout = [goal for goal in heldout if strict_goal(by_goal, goal)]
        for budget, portfolio in enumerate(portfolios, start=1):
            fixed = eval_fixed(by_goal, heldout, portfolio)
            strict_fixed = eval_fixed(by_goal, strict_heldout, portfolio)
            row = {
                "fold": fold_idx,
                "budget": budget,
                "actions": portfolio,
                "n": len(heldout),
                "fixed": fixed,
                "empty": sum(1 for goal in heldout if empty_verified(by_goal, goal)),
                "oracle": sum(1 for goal in heldout if any_verified(by_goal, goal)),
                "strict_n": len(strict_heldout),
                "strict_fixed": strict_fixed,
                "strict_oracle": len(strict_heldout),
                "paired_vs_best_single": paired_delta(by_goal, heldout, portfolio, matrix["summary"]["best_static_action"]),
                "paired_vs_empty": paired_delta(by_goal, heldout, portfolio, "hammer_empty"),
            }
            fold_rows.append(row)
            total = totals[str(budget)]
            for key in ["n", "fixed", "empty", "oracle", "strict_n", "strict_fixed", "strict_oracle"]:
                total[key] += int(row[key])

    train_fitted_portfolios = greedy_portfolios(by_goal, list(split["train"]), actions, args.max_budget)
    train_fitted = [
        {
            "budget": budget,
            "actions": portfolio,
            "all_success": eval_fixed(by_goal, all_goals, portfolio),
            "strict_success": eval_fixed(by_goal, [goal for goal in all_goals if strict_goal(by_goal, goal)], portfolio),
        }
        for budget, portfolio in enumerate(train_fitted_portfolios, start=1)
    ]
    payload = {
        "matrix_json": str(args.matrix_json),
        "split_json": str(args.split_json),
        "max_budget": args.max_budget,
        "folds": args.folds,
        "n_goals": len(all_goals),
        "n_strict": sum(1 for goal in all_goals if strict_goal(by_goal, goal)),
        "best_static_action": matrix["summary"]["best_static_action"],
        "folds_detail": fold_rows,
        "totals": totals,
        "train_fitted": train_fitted,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines: list[str] = []
    lines.append("# Mathlib 4.30 Fixed Portfolio Stability")
    lines.append("")
    lines.append(f"- Matrix: `{args.matrix_json}`")
    lines.append(f"- Splits: `{args.split_json}`")
    lines.append(f"- Goals: {payload['n_goals']}")
    lines.append(f"- Strict action-dependent oracle goals: {payload['n_strict']}")
    lines.append(f"- Best static action: `{payload['best_static_action']}`")
    lines.append("")
    lines.append("## 5-Fold OOF Totals")
    lines.append("")
    lines.append("| K | Fixed greedy | Empty | Oracle | Strict fixed | Strict oracle |")
    lines.append("|---:|---:|---:|---:|---:|---:|")
    for budget in range(1, args.max_budget + 1):
        row = totals[str(budget)]
        lines.append(
            f"| {budget} | {row['fixed']}/{row['n']} ({pct(row['fixed'], row['n'])}) | "
            f"{row['empty']}/{row['n']} ({pct(row['empty'], row['n'])}) | "
            f"{row['oracle']}/{row['n']} ({pct(row['oracle'], row['n'])}) | "
            f"{row['strict_fixed']}/{row['strict_n']} ({pct(row['strict_fixed'], row['strict_n'])}) | "
            f"{row['strict_oracle']}/{row['strict_n']} ({pct(row['strict_oracle'], row['strict_n'])}) |"
        )
    lines.append("")
    lines.append("## Per-Fold Fixed Greedy")
    lines.append("")
    lines.append("| Fold | K | Fixed | Empty | Oracle | Actions |")
    lines.append("|---:|---:|---:|---:|---:|---|")
    for row in fold_rows:
        actions_text = ", ".join(f"`{action}`" for action in row["actions"])
        lines.append(
            f"| {row['fold']} | {row['budget']} | {row['fixed']}/{row['n']} | "
            f"{row['empty']}/{row['n']} | {row['oracle']}/{row['n']} | {actions_text} |"
        )
    lines.append("")
    lines.append("## Train-Fitted Portfolios")
    lines.append("")
    lines.append("| K | All success | Strict success | Actions |")
    lines.append("|---:|---:|---:|---|")
    for row in train_fitted:
        actions_text = ", ".join(f"`{action}`" for action in row["actions"])
        lines.append(
            f"| {row['budget']} | {row['all_success']}/{payload['n_goals']} | "
            f"{row['strict_success']}/{payload['n_strict']} | {actions_text} |"
        )
    lines.append("")
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
