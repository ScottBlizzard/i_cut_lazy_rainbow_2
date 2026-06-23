#!/usr/bin/env python3
"""Summarize a frozen fresh-holdout action subset.

This evaluator is intentionally offline: it does not choose actions from the
holdout.  It reports a predeclared fixed portfolio against empty and singleton
controls on a matrix that has already been checked by Lean.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pct(num: int, den: int) -> str:
    if den == 0:
        return "0.0%"
    return f"{100.0 * num / den:.1f}%"


def display_path(path: Path) -> str:
    return str(path).replace("\\", "/")


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


def portfolio_verified(
    by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, actions: list[str]
) -> bool:
    return empty_verified(by_goal, goal) or any(action_verified(by_goal, goal, action) for action in actions)


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
        portfolio_success = portfolio_verified(by_goal, goal, portfolio)
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
    parser.add_argument("--matrix-json", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--portfolio-actions", nargs="+", required=True)
    parser.add_argument("--singleton-controls", nargs="*", default=[])
    parser.add_argument("--tag", default="fresh_holdout")
    parser.add_argument("--candidate-source-label", default="retrieved_only")
    args = parser.parse_args()

    matrix = load_json(args.matrix_json)
    by_goal = goal_action_index(matrix["results"])
    goals = sorted(by_goal)
    all_actions = sorted({row["action"] for row in matrix["results"]})
    portfolio = list(args.portfolio_actions)
    singleton_controls = list(dict.fromkeys(args.singleton_controls or []))
    singleton_controls = [action for action in singleton_controls if action in all_actions]
    if not singleton_controls:
        singleton_controls = [action for action in all_actions if action != "hammer_empty"]

    action_success = {
        action: sum(1 for goal in goals if action_verified(by_goal, goal, action))
        for action in all_actions
    }
    best_single_action, best_single_success = max(
        ((action, action_success[action]) for action in singleton_controls),
        key=lambda item: (item[1], item[0]),
    )
    portfolio_rows = []
    for budget in range(1, len(portfolio) + 1):
        actions = portfolio[:budget]
        success = sum(1 for goal in goals if portfolio_verified(by_goal, goal, actions))
        strict_goals = [goal for goal in goals if (not empty_verified(by_goal, goal)) and any_verified(by_goal, goal)]
        strict_success = sum(1 for goal in strict_goals if portfolio_verified(by_goal, goal, actions))
        portfolio_rows.append(
            {
                "budget": budget,
                "actions": actions,
                "success": success,
                "strict_success": strict_success,
                "strict_n": len(strict_goals),
            }
        )

    final_portfolio = portfolio
    strict_goals = [goal for goal in goals if (not empty_verified(by_goal, goal)) and any_verified(by_goal, goal)]
    payload = {
        "tag": args.tag,
        "matrix_json": display_path(args.matrix_json),
        "n_goals": len(goals),
        "candidate_source": matrix.get("candidate_source") or args.candidate_source_label,
        "tested_actions": all_actions,
        "portfolio_actions": portfolio,
        "singleton_controls": singleton_controls,
        "empty_success": action_success.get("hammer_empty", 0),
        "action_success": action_success,
        "best_single_action": best_single_action,
        "best_single_success": best_single_success,
        "tested_oracle": sum(1 for goal in goals if any_verified(by_goal, goal)),
        "strict_after_empty_n": len(strict_goals),
        "portfolio": portfolio_rows,
        "paired_vs_best_single": paired_delta(by_goal, goals, final_portfolio, best_single_action),
        "paired_vs_empty": paired_delta(by_goal, goals, final_portfolio, "hammer_empty"),
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    n = payload["n_goals"]
    lines: list[str] = []
    lines.append(f"# Mathlib 4.30 Fresh Holdout: {args.tag}")
    lines.append("")
    lines.append(f"- Matrix: `{display_path(args.matrix_json)}`")
    lines.append(f"- Candidate source: `{payload['candidate_source']}`")
    lines.append(f"- Goals: {n}")
    lines.append(f"- Tested actions: {len(all_actions)}")
    lines.append(f"- Empty Hammer: {payload['empty_success']}/{n} ({pct(payload['empty_success'], n)})")
    lines.append(
        f"- Best singleton control: `{best_single_action}` = {best_single_success}/{n} ({pct(best_single_success, n)})"
    )
    lines.append(f"- Tested-action oracle: {payload['tested_oracle']}/{n} ({pct(payload['tested_oracle'], n)})")
    lines.append(f"- Strict after-`hammer_empty` goals: {payload['strict_after_empty_n']}")
    lines.append("")
    lines.append("## Frozen Portfolio")
    lines.append("")
    lines.append("| K | Success | Strict success | Actions |")
    lines.append("|---:|---:|---:|---|")
    for row in portfolio_rows:
        actions_text = ", ".join(f"`{action}`" for action in row["actions"])
        lines.append(
            f"| {row['budget']} | {row['success']}/{n} ({pct(row['success'], n)}) | "
            f"{row['strict_success']}/{row['strict_n']} ({pct(row['strict_success'], row['strict_n'])}) | {actions_text} |"
        )
    lines.append("")
    lines.append("## Singleton Controls")
    lines.append("")
    lines.append("| Action | Success |")
    lines.append("|---|---:|")
    for action in sorted(singleton_controls, key=lambda a: (-action_success[a], a)):
        lines.append(f"| `{action}` | {action_success[action]}/{n} ({pct(action_success[action], n)}) |")
    lines.append("")
    lines.append("## Paired Final Portfolio Deltas")
    lines.append("")
    paired_best = payload["paired_vs_best_single"]
    paired_empty = payload["paired_vs_empty"]
    lines.append(
        f"- Final K={len(final_portfolio)} vs `{best_single_action}`: "
        f"+{len(paired_best['wins'])} wins, -{len(paired_best['losses'])} losses."
    )
    lines.append(
        f"- Final K={len(final_portfolio)} vs `hammer_empty`: "
        f"+{len(paired_empty['wins'])} wins, -{len(paired_empty['losses'])} losses."
    )
    lines.append("")
    args.out_md.write_text("\n".join(lines), encoding="utf-8")
    print(args.out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
