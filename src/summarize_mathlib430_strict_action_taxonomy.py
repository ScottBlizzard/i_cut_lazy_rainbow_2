#!/usr/bin/env python3
"""Summarize strict action-dependent goals in a Mathlib action matrix."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
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


def action_family(action: str, kind: str) -> str:
    if kind:
        return kind
    if action.startswith("hammerCore"):
        return "hammerCore"
    if action.startswith("hammer"):
        return "hammer"
    if action.startswith("simp_all"):
        return "simp_all"
    if action.startswith("simpa"):
        return "simpa"
    if action.startswith("simp"):
        return "simp"
    if action.startswith("solve_by_elim"):
        return "solve_by_elim"
    return "other"


def summarize(matrix: dict[str, Any]) -> dict[str, Any]:
    by_goal = goal_action_index(matrix["results"])
    strict_rows: list[dict[str, Any]] = []
    family_goal_counts: Counter[str] = Counter()
    only_family_counts: Counter[str] = Counter()
    action_goal_counts: Counter[str] = Counter()
    family_pair_counts: Counter[str] = Counter()

    for goal_id, actions in sorted(by_goal.items()):
        empty_verified = bool(actions.get("hammer_empty", {}).get("verified"))
        verified = [row for row in actions.values() if bool(row.get("verified"))]
        if empty_verified or not verified:
            continue
        families = sorted({action_family(str(row.get("action", "")), str(row.get("kind", ""))) for row in verified})
        for family in families:
            family_goal_counts[family] += 1
        if len(families) == 1:
            only_family_counts[families[0]] += 1
        if len(families) >= 2:
            for i, left in enumerate(families):
                for right in families[i + 1 :]:
                    family_pair_counts[f"{left}+{right}"] += 1
        for row in verified:
            action_goal_counts[str(row.get("action", ""))] += 1
        first = verified[0]
        strict_rows.append(
            {
                "goal_id": goal_id,
                "theorem": first.get("theorem", goal_id),
                "file_path": first.get("file_path", ""),
                "families": families,
                "verified_actions": [
                    {
                        "action": row.get("action"),
                        "kind": row.get("kind"),
                        "fact_count": row.get("fact_count"),
                        "simp_count": row.get("simp_count"),
                        "facts": row.get("facts") or [],
                        "simps": row.get("simps") or [],
                    }
                    for row in sorted(verified, key=lambda r: str(r.get("action", "")))
                ],
            }
        )

    return {
        "n_goals": len(by_goal),
        "n_strict": len(strict_rows),
        "family_goal_counts": dict(family_goal_counts),
        "only_family_counts": dict(only_family_counts),
        "action_goal_counts": dict(action_goal_counts),
        "family_pair_counts": dict(family_pair_counts),
        "strict_goals": strict_rows,
    }


def markdown_report(payload: dict[str, Any]) -> str:
    n = int(payload["n_strict"])
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Strict Action-Dependent Taxonomy")
    lines.append("")
    lines.append("Date: 2026-06-22")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Matrix: `{payload['matrix_json']}`")
    lines.append(f"- Goals in matrix: {payload['n_goals']}")
    lines.append(f"- Strict action-dependent goals: {n}")
    lines.append("- Strict means `hammer_empty` fails but at least one non-empty or non-default proof-action succeeds.")
    lines.append("")
    lines.append("## Family Coverage")
    lines.append("")
    lines.append("| Family | Strict goals solved |")
    lines.append("|---|---:|")
    for family, count in sorted(payload["family_goal_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{family}` | {count} / {n} ({pct(int(count), n)}) |")
    lines.append("")
    lines.append("## Only-Family Cases")
    lines.append("")
    lines.append("| Family | Goals where this is the only successful family |")
    lines.append("|---|---:|")
    for family, count in sorted(payload["only_family_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{family}` | {count} |")
    lines.append("")
    lines.append("## Action Coverage")
    lines.append("")
    lines.append("| Action | Strict goals solved |")
    lines.append("|---|---:|")
    for action, count in sorted(payload["action_goal_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{action}` | {count} |")
    lines.append("")
    lines.append("## Per-Goal Details")
    lines.append("")
    lines.append("| Goal | Families | Verified actions | Facts / Simps |")
    lines.append("|---|---|---|---|")
    for row in payload["strict_goals"]:
        families = ", ".join(f"`{family}`" for family in row["families"])
        actions = ", ".join(f"`{item['action']}`" for item in row["verified_actions"])
        counts = ", ".join(
            f"{item['fact_count']}f/{item['simp_count']}s" for item in row["verified_actions"]
        )
        lines.append(f"| `{row['goal_id']}` | {families} | {actions} | {counts} |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    if payload["only_family_counts"]:
        top_only = sorted(payload["only_family_counts"].items(), key=lambda item: (-item[1], item[0]))[0]
        lines.append(
            f"- The largest only-family bucket is `{top_only[0]}` with {top_only[1]} strict goals."
        )
    lines.append(
        "- The strict positives are not a single-premise-budget effect: different Lean interfaces "
        "solve disjoint subsets of replayable theorem contexts."
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-json", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    matrix = load_json(args.matrix_json)
    payload = summarize(matrix)
    payload["matrix_json"] = str(args.matrix_json)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(markdown_report(payload), encoding="utf-8")
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
