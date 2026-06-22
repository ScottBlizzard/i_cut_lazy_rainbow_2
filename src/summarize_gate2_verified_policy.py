"""Summarize verified action-policy readouts from Gate 2 action-grid results."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TRUE_POLICY = {
    "expand_150": "expand_150",
    "expand_200": "expand_200",
    "base_rescue": "base_rescue_8",
    "second_stage": "second_stage_rescore",
    "unsolved_grid": "expand_200",
}

FIXED_CONTROLS = [
    "keep",
    "expand_150",
    "expand_200",
    "base_rescue_8",
    "second_stage_rescore",
]


def pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def load_results(path: Path) -> dict[str, dict[str, dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    by_goal: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in data["results"]:
        by_goal[row["goal_id"]][row["action"]] = row
    return dict(by_goal)


def evaluate_policy(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    *,
    name: str,
    selector,
) -> dict[str, Any]:
    rows = []
    for goal_id, actions in by_goal.items():
        family = next(iter(actions.values()))["family"]
        action = selector(goal_id, family, actions)
        row = actions[action]
        rows.append(row)
    n = len(rows)
    return {
        "policy": name,
        "goals": n,
        "verified": sum(1 for row in rows if row["verified"]),
        "success_rate": sum(1 for row in rows if row["verified"]) / n if n else 0.0,
        "avg_premises": sum(float(row["premise_count"]) for row in rows) / n if n else 0.0,
        "avg_time_s": sum(float(row["time_s"]) for row in rows) / n if n else 0.0,
        "action_counts": dict(Counter(row["action"] for row in rows)),
    }


def render(path: Path, seed: int) -> str:
    by_goal = load_results(path)
    rng = random.Random(seed)

    policies = []
    policies.append(
        evaluate_policy(
            by_goal,
            name="verified_true_feedback_policy",
            selector=lambda _gid, family, _actions: TRUE_POLICY[family],
        )
    )
    for fixed in FIXED_CONTROLS:
        policies.append(
            evaluate_policy(
                by_goal,
                name=f"fixed_{fixed}",
                selector=lambda _gid, _family, _actions, fixed=fixed: fixed,
            )
        )
    policies.append(
        evaluate_policy(
            by_goal,
            name="masked_best_static",
            selector=lambda _gid, _family, _actions: "expand_200",
        )
    )
    policies.append(
        evaluate_policy(
            by_goal,
            name="shuffled_feedback_policy",
            selector=lambda _gid, _family, _actions: TRUE_POLICY[
                rng.choice(list(TRUE_POLICY.keys()))
            ],
        )
    )

    oracle = evaluate_policy(
        by_goal,
        name="oracle_adaptive_action",
        selector=lambda _gid, _family, actions: max(
            actions.values(),
            key=lambda row: (bool(row["verified"]), -float(row["premise_count"])),
        )["action"],
    )

    best_static = max(
        [row for row in policies if row["policy"].startswith("fixed_")],
        key=lambda row: row["success_rate"],
    )
    true_policy = next(row for row in policies if row["policy"] == "verified_true_feedback_policy")
    masked = next(row for row in policies if row["policy"] == "masked_best_static")
    shuffled = next(row for row in policies if row["policy"] == "shuffled_feedback_policy")

    lines = []
    lines.append("# Gate 2 Verified Policy Readout")
    lines.append("")
    lines.append("This report converts the verified action-grid outcomes into policy-level comparisons.")
    lines.append("")
    lines.append("| Policy | Goals | Verified | Success | Avg premises | Avg time | Action counts |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for row in [true_policy, oracle, masked, shuffled, *[p for p in policies if p["policy"].startswith("fixed_")]]:
        lines.append(
            f"| `{row['policy']}` | {row['goals']} | {row['verified']} | {pct(row['success_rate'])} | "
            f"{row['avg_premises']:.1f} | {row['avg_time_s']:.2f}s | `{row['action_counts']}` |"
        )

    lines.append("")
    lines.append("## Gate Readout")
    lines.append("")
    lines.append(f"- Best static: `{best_static['policy']}` at {pct(best_static['success_rate'])}.")
    lines.append(f"- True feedback policy: {pct(true_policy['success_rate'])}.")
    lines.append(f"- Oracle adaptive action: {pct(oracle['success_rate'])}.")
    lines.append(f"- True minus best static: {100.0 * (true_policy['success_rate'] - best_static['success_rate']):+.1f} pp.")
    lines.append(f"- True minus masked best-static: {100.0 * (true_policy['success_rate'] - masked['success_rate']):+.1f} pp.")
    lines.append(f"- True minus shuffled feedback: {100.0 * (true_policy['success_rate'] - shuffled['success_rate']):+.1f} pp.")
    lines.append("")
    lines.append("Caveat: the policy signal here is synthetic family metadata, not a learned Mathlib failure-transcript model. Use this as pipeline validation, not paper evidence.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    report = render(args.input, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
