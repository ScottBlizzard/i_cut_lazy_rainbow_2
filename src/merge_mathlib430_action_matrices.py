#!/usr/bin/env python3
"""Merge disjoint Mathlib action-matrix JSON files and summarize them."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_goal: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_action: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        by_goal[row["goal_id"]].append(row)
        by_action[row["action"]].append(row)

    goal_rows: dict[str, dict[str, Any]] = {}
    strict_goals: list[dict[str, Any]] = []
    for goal, rows in by_goal.items():
        proved = [row for row in rows if row.get("verified")]
        empty = [row for row in proved if not row.get("nonempty")]
        nonempty = [row for row in proved if row.get("nonempty")]
        best = min(proved, key=lambda row: row.get("time_s", 1e9), default=None)
        goal_rows[goal] = {
            "verified": len(proved),
            "nonempty_verified": len(nonempty),
            "empty_verified": len(empty),
            "best_action": best.get("action") if best else None,
            "best_fact_count": best.get("fact_count") if best else None,
            "best_simp_count": best.get("simp_count") if best else None,
        }
        if nonempty and not empty:
            strict_goals.append(
                {
                    "goal_id": goal,
                    "best_action": best.get("action") if best else None,
                    "fact_count": best.get("fact_count") if best else None,
                    "simp_count": best.get("simp_count") if best else None,
                }
            )

    action_rows = {
        action: {
            "attempts": len(rows),
            "verified": sum(1 for row in rows if row.get("verified")),
            "verified_goals": len({row["goal_id"] for row in rows if row.get("verified")}),
            "nonempty_verified": sum(
                1 for row in rows if row.get("verified") and row.get("nonempty")
            ),
        }
        for action, rows in by_action.items()
    }
    best_static_action, best_static = max(
        ((action, row["verified_goals"]) for action, row in action_rows.items()),
        key=lambda item: (item[1], item[0]),
    )
    return {
        "n_goals": len(by_goal),
        "n_attempts": len(results),
        "n_verified_attempts": sum(1 for row in results if row.get("verified")),
        "n_nonempty_verified_attempts": sum(
            1 for row in results if row.get("verified") and row.get("nonempty")
        ),
        "n_verified_goals": sum(1 for row in goal_rows.values() if row["verified"] > 0),
        "n_nonempty_verified_goals": sum(
            1 for row in goal_rows.values() if row["nonempty_verified"] > 0
        ),
        "n_strict_action_dependent_goals": len(strict_goals),
        "best_static_action": best_static_action,
        "best_static_goals": best_static,
        "status_counts": dict(Counter(row.get("status", "unknown") for row in results)),
        "by_action": action_rows,
        "by_goal": goal_rows,
        "strict_goals": sorted(strict_goals, key=lambda row: row["goal_id"]),
    }


def write_md(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    n = summary["n_goals"]
    gap = summary["n_verified_goals"] - summary["best_static_goals"]
    gap_pp = 100.0 * gap / n if n else 0.0
    lines = [
        "# Mathlib 4.30 Scaled-230 Merged Proof-Action Matrix",
        "",
        "Date: 2026-06-22",
        "",
        "Inputs:",
        "",
    ]
    for source in payload["sources"]:
        lines.append(f"- `{source}`")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| goals | {n} |",
            f"| attempts | {summary['n_attempts']} |",
            f"| verified attempts | {summary['n_verified_attempts']} |",
            f"| non-empty-premise verified attempts | {summary['n_nonempty_verified_attempts']} |",
            f"| oracle goals | {summary['n_verified_goals']} / {n} |",
            f"| non-empty-premise proof goals | {summary['n_nonempty_verified_goals']} / {n} |",
            f"| best static action | `{summary['best_static_action']}` |",
            f"| best static goals | {summary['best_static_goals']} / {n} |",
            f"| oracle gap over best static | +{gap} goals / +{gap_pp:.2f} pp |",
            f"| strict action-dependent goals | {summary['n_strict_action_dependent_goals']} |",
            "",
            "## By Action",
            "",
            "| Action | Verified Goals | Verified Attempts | Attempts |",
            "|---|---:|---:|---:|",
        ]
    )
    for action, row in sorted(
        summary["by_action"].items(),
        key=lambda item: (-item[1]["verified_goals"], item[0]),
    ):
        lines.append(
            f"| `{action}` | {row['verified_goals']} | {row['verified']} | {row['attempts']} |"
        )
    lines.extend(
        [
            "",
            "## Strict Action-Dependent Goals",
            "",
            "| Goal | Best Action | Facts | Simps |",
            "|---|---|---:|---:|",
        ]
    )
    for row in summary["strict_goals"]:
        lines.append(
            f"| `{row['goal_id']}` | `{row['best_action']}` | {row['fact_count']} | {row['simp_count']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()

    payloads = [load_json(path) for path in args.inputs]
    results: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for payload in payloads:
        for row in payload["results"]:
            key = (row["goal_id"], row["action"])
            if key in seen:
                raise SystemExit(f"duplicate goal/action in inputs: {key}")
            seen.add(key)
            results.append(row)
    summary = summarize(results)
    merged = {
        "experiment": "mathlib430_pretheorem_action_matrix_merged",
        "sources": [str(path) for path in args.inputs],
        "summary": summary,
        "results": results,
    }
    args.out_json.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_md(merged, args.out_md)


if __name__ == "__main__":
    main()
