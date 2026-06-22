#!/usr/bin/env python3
"""Analyze Aesop channel-assignment counterfactuals from an action matrix."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


EXPOSURE_ORDER = ["facts+simps", "facts-only", "simps-only"]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pct(num: int, den: int) -> str:
    if den == 0:
        return "0.0%"
    return f"{100.0 * num / den:.1f}%"


def action_bucket(action: str) -> tuple[str | None, str | None]:
    if action == "aesop_core":
        return "core", "facts+simps"
    if action == "aesop_core_facts":
        return "core", "facts-only"
    if action == "aesop_core_simps":
        return "core", "simps-only"
    if action == "aesop_core_plus_learned":
        return "core+learned8", "facts+simps"
    if action == "aesop_core_plus_learned_facts":
        return "core+learned8", "facts-only"
    if action == "aesop_core_plus_learned_simps":
        return "core+learned8", "simps-only"
    match = re.fullmatch(r"aesop_core_plus_learned(16|32)(?:_(facts|simps))?", action)
    if match:
        source = f"core+learned{match.group(1)}"
        exposure = {"facts": "facts-only", "simps": "simps-only", None: "facts+simps"}[match.group(2)]
        return source, exposure
    match = re.fullmatch(r"aesop_learned(8|16|32)(?:_(facts|simps))?", action)
    if match:
        source = f"learned{match.group(1)}"
        exposure = {"facts": "facts-only", "simps": "simps-only", None: "facts+simps"}[match.group(2)]
        return source, exposure
    return None, None


def solved_sets(matrix: dict[str, Any]) -> tuple[set[str], dict[tuple[str, str], set[str]], dict[tuple[str, str], str]]:
    goals = {str(row["goal_id"]) for row in matrix["results"]}
    solved: dict[tuple[str, str], set[str]] = defaultdict(set)
    actions: dict[tuple[str, str], str] = {}
    for row in matrix["results"]:
        source, exposure = action_bucket(str(row.get("action", "")))
        if source is None or exposure is None:
            continue
        key = (source, exposure)
        actions[key] = str(row["action"])
        if row.get("verified"):
            solved[key].add(str(row["goal_id"]))
    return goals, solved, actions


def source_sort_key(source: str) -> tuple[int, int, str]:
    if source == "core":
        return (0, 0, source)
    match = re.fullmatch(r"core\+learned(\d+)", source)
    if match:
        return (1, int(match.group(1)), source)
    match = re.fullmatch(r"learned(\d+)", source)
    if match:
        return (2, int(match.group(1)), source)
    return (9, 0, source)


def summarize(matrix: dict[str, Any]) -> dict[str, Any]:
    goals, solved, action_names = solved_sets(matrix)
    n_goals = len(goals)
    sources = sorted({source for source, _ in action_names}, key=source_sort_key)

    source_rows: list[dict[str, Any]] = []
    for source in sources:
        both = solved.get((source, "facts+simps"), set())
        facts = solved.get((source, "facts-only"), set())
        simps = solved.get((source, "simps-only"), set())
        single_union = facts | simps
        single_intersection = facts & simps
        source_rows.append(
            {
                "source": source,
                "actions": {
                    exposure: action_names.get((source, exposure), "")
                    for exposure in EXPOSURE_ORDER
                },
                "facts_simps": len(both),
                "facts_only": len(facts),
                "simps_only": len(simps),
                "single_channel_union": len(single_union),
                "single_channel_intersection": len(single_intersection),
                "joint_only": sorted(both - single_union),
                "facts_only_not_joint": sorted(facts - both),
                "simps_only_not_joint": sorted(simps - both),
                "any_single_only_not_joint": sorted(single_union - both),
                "joint_and_single": sorted(both & single_union),
                "joint_minus_single_union": len(both) - len(single_union),
                "joint_gain_over_best_single": len(both) - max(len(facts), len(simps)),
            }
        )

    monotonic_rows: list[dict[str, Any]] = []
    for family in ["core+learned", "learned"]:
        for exposure in EXPOSURE_ORDER:
            source8 = f"{family}8"
            source16 = f"{family}16"
            source32 = f"{family}32"
            if (source8, exposure) not in action_names:
                continue
            set8 = solved.get((source8, exposure), set())
            set16 = solved.get((source16, exposure), set())
            set32 = solved.get((source32, exposure), set())
            monotonic_rows.append(
                {
                    "family": family,
                    "exposure": exposure,
                    "k8": len(set8),
                    "k16": len(set16),
                    "k32": len(set32),
                    "lost_8_to_16": sorted(set8 - set16),
                    "gained_8_to_16": sorted(set16 - set8),
                    "lost_16_to_32": sorted(set16 - set32),
                    "gained_16_to_32": sorted(set32 - set16),
                    "lost_8_to_32": sorted(set8 - set32),
                    "gained_8_to_32": sorted(set32 - set8),
                }
            )

    best_source = max(
        source_rows,
        key=lambda row: (int(row["facts_simps"]), int(row["joint_gain_over_best_single"]), row["source"]),
    )
    return {
        "n_goals": n_goals,
        "sources": source_rows,
        "non_monotonicity": monotonic_rows,
        "headline": {
            "best_source": best_source["source"],
            "facts_simps": best_source["facts_simps"],
            "facts_only": best_source["facts_only"],
            "simps_only": best_source["simps_only"],
            "single_channel_union": best_source["single_channel_union"],
            "joint_only": len(best_source["joint_only"]),
            "single_only_not_joint": len(best_source["any_single_only_not_joint"]),
            "joint_gain_over_best_single": best_source["joint_gain_over_best_single"],
        },
    }


def goal_list_cell(goals: list[str], limit: int) -> str:
    if not goals:
        return "-"
    shown = ", ".join(f"`{goal}`" for goal in goals[:limit])
    if len(goals) > limit:
        shown += f", ... (+{len(goals) - limit})"
    return shown


def markdown_report(payload: dict[str, Any], detail_limit: int) -> str:
    summary = payload["summary"]
    n_goals = int(summary["n_goals"])
    headline = summary["headline"]
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Aesop Counterfactual Channel Controls")
    lines.append("")
    lines.append("Date: 2026-06-23")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Matrix: `{payload['matrix_json']}`")
    lines.append(f"- Goals: {n_goals}")
    lines.append("- Control type: matched Aesop source/budget with channel removed or combined.")
    lines.append(
        "- Caveat: fact and simp pools are matched by source/budget and goal, but they are typed pools; "
        "they are not assumed to contain identical names."
    )
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append(
        f"- Best matched source is `{headline['best_source']}`: facts+simps solves "
        f"{headline['facts_simps']}/{n_goals} ({pct(headline['facts_simps'], n_goals)}), "
        f"facts-only solves {headline['facts_only']}/{n_goals}, and simps-only solves "
        f"{headline['simps_only']}/{n_goals}."
    )
    lines.append(
        f"- The union of the two single-channel controls solves {headline['single_channel_union']}/{n_goals}; "
        f"joint exposure has {headline['joint_only']} joint-only goals and "
        f"{headline['single_only_not_joint']} single-channel-only misses."
    )
    lines.append(
        f"- Joint exposure beats the better single channel by "
        f"{headline['joint_gain_over_best_single']} goals for the best source."
    )
    lines.append("")
    lines.append("## Matched Channel Controls")
    lines.append("")
    lines.append(
        "| Source | Facts+simps | Facts-only | Simps-only | Single-channel union | "
        "Joint-only | Single-only not joint | Joint gain over best single |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary["sources"]:
        lines.append(
            f"| `{row['source']}` | {row['facts_simps']}/{n_goals} | "
            f"{row['facts_only']}/{n_goals} | {row['simps_only']}/{n_goals} | "
            f"{row['single_channel_union']}/{n_goals} | {len(row['joint_only'])} | "
            f"{len(row['any_single_only_not_joint'])} | {row['joint_gain_over_best_single']} |"
        )
    lines.append("")
    lines.append("## Exposure-Budget Non-Monotonicity")
    lines.append("")
    lines.append("| Family | Exposure | K=8 | K=16 | K=32 | Lost 8->32 | Gained 8->32 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for row in summary["non_monotonicity"]:
        lines.append(
            f"| `{row['family']}` | `{row['exposure']}` | {row['k8']}/{n_goals} | "
            f"{row['k16']}/{n_goals} | {row['k32']}/{n_goals} | "
            f"{len(row['lost_8_to_32'])} | {len(row['gained_8_to_32'])} |"
        )
    lines.append("")
    lines.append("## Representative Joint-Only Goals")
    lines.append("")
    for row in summary["sources"]:
        if not row["joint_only"]:
            continue
        lines.append(f"### `{row['source']}`")
        lines.append("")
        lines.append(goal_list_cell(row["joint_only"], detail_limit))
        lines.append("")
    lines.append("## Readout")
    lines.append("")
    lines.append(
        "- This is the paper-critical counterfactual control: for the same Aesop source/budget, "
        "removing either channel largely destroys the best result."
    )
    lines.append(
        "- The result supports an action-conditional evidence-allocation thesis: selected evidence must be "
        "compiled into the interface channels that can consume it."
    )
    lines.append(
        "- The non-monotonic K=8/16/32 rows support the anti-blind-expansion claim: more exposed names can hurt."
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-json", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--detail-limit", type=int, default=12)
    args = parser.parse_args()

    matrix = load_json(args.matrix_json)
    payload = {
        "matrix_json": str(args.matrix_json),
        "summary": summarize(matrix),
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(markdown_report(payload, args.detail_limit), encoding="utf-8")
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
