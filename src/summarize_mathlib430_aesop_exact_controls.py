#!/usr/bin/env python3
"""Merge and summarize Aesop exact channel/source controls."""

from __future__ import annotations

import argparse
import glob
import json
import re
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


def strip_mode_suffix(action: str) -> str:
    return re.sub(r"_(oracle_plus_retrieved|retrieved_only|oracle_core_only)_exact$", "", action)


def mode_from_payload(payload: dict[str, Any], path: Path) -> str:
    mode = payload.get("candidate_source")
    if mode:
        return str(mode)
    match = re.search(r"(oracle_plus_retrieved|retrieved_only|oracle_core_only)", path.name)
    return match.group(1) if match else "unknown"


def goal_action_index(results: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    by_goal: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in results:
        by_goal[str(row["goal_id"])][strip_mode_suffix(str(row["action"]))] = row
    return by_goal


def action_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, action: str) -> bool:
    return bool(by_goal.get(goal, {}).get(action, {}).get("verified"))


def paired_delta(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    action: str,
    baseline: str,
) -> dict[str, Any]:
    gains: list[str] = []
    losses: list[str] = []
    both_success = 0
    both_fail = 0
    for goal in goals:
        a = action_verified(by_goal, goal, action)
        b = action_verified(by_goal, goal, baseline)
        if a and not b:
            gains.append(goal)
        elif b and not a:
            losses.append(goal)
        elif a and b:
            both_success += 1
        else:
            both_fail += 1
    return {
        "gains": gains,
        "losses": losses,
        "both_success": both_success,
        "both_fail": both_fail,
        "net": len(gains) - len(losses),
    }


def exposure_bucket(action: str) -> str:
    if action == "aesop_empty":
        return "empty"
    if action.endswith("_facts"):
        return "facts-only"
    if action.endswith("_simps"):
        return "simps-only"
    if action.endswith("_identity"):
        return "identity-both"
    if action.endswith("_swapped"):
        return "swapped"
    if action.endswith("_countmatched_facts"):
        return "countmatched-facts"
    if action.endswith("_countmatched_simps"):
        return "countmatched-simps"
    if action.endswith("_random_split"):
        return "random-split"
    return "typed-both"


def summarize_mode(mode: str, payloads: list[dict[str, Any]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for payload in payloads:
        results.extend(payload["results"])
    by_goal = goal_action_index(results)
    goals = sorted(by_goal)
    actions = sorted({action for rows in by_goal.values() for action in rows})
    by_action: dict[str, Any] = {}
    for action in actions:
        success = sum(1 for goal in goals if action_verified(by_goal, goal, action))
        row0 = next((by_goal[goal][action] for goal in goals if action in by_goal[goal]), {})
        paired = paired_delta(by_goal, goals, action, "aesop_empty") if action != "aesop_empty" else None
        by_action[action] = {
            "success": success,
            "attempts": sum(1 for goal in goals if action in by_goal[goal]),
            "exposure": exposure_bucket(action),
            "avg_facts": sum(len((by_goal[goal].get(action) or {}).get("facts") or []) for goal in goals) / max(1, len(goals)),
            "avg_simps": sum(len((by_goal[goal].get(action) or {}).get("simps") or []) for goal in goals) / max(1, len(goals)),
            "sample_tactic": row0.get("tactic_line", ""),
            "paired_vs_empty": paired,
        }
    triples: dict[str, Any] = {}
    for base in ["aesop_core_plus_learned", "aesop_learned8"]:
        facts = f"{base}_facts"
        simps = f"{base}_simps"
        if base not in actions or facts not in actions or simps not in actions:
            continue
        joint_only = [
            goal
            for goal in goals
            if action_verified(by_goal, goal, base)
            and not action_verified(by_goal, goal, facts)
            and not action_verified(by_goal, goal, simps)
        ]
        triples[base] = {
            "joint": sum(1 for goal in goals if action_verified(by_goal, goal, base)),
            "facts": sum(1 for goal in goals if action_verified(by_goal, goal, facts)),
            "simps": sum(1 for goal in goals if action_verified(by_goal, goal, simps)),
            "identity": sum(1 for goal in goals if action_verified(by_goal, goal, f"{base}_identity")),
            "swapped": sum(1 for goal in goals if action_verified(by_goal, goal, f"{base}_swapped")),
            "countmatched_facts": sum(
                1 for goal in goals if action_verified(by_goal, goal, f"{base}_countmatched_facts")
            ),
            "countmatched_simps": sum(
                1 for goal in goals if action_verified(by_goal, goal, f"{base}_countmatched_simps")
            ),
            "random_split": sum(1 for goal in goals if action_verified(by_goal, goal, f"{base}_random_split")),
            "joint_only_over_single_channels": joint_only,
        }
    return {
        "mode": mode,
        "n_goals": len(goals),
        "n_attempts": len(results),
        "by_action": by_action,
        "triples": triples,
    }


def write_md(payload: dict[str, Any], path: Path) -> None:
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Aesop Exact Source/Channel Controls")
    lines.append("")
    lines.append("Date: 2026-06-23")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    sources = payload["sources"]
    lines.append(f"- Files: {len(sources)}")
    if len(sources) <= 20:
        shown_sources = sources
    else:
        shown_sources = sources[:5] + ["..."] + sources[-5:]
    for source in shown_sources:
        if source == "...":
            lines.append("- ...")
        else:
            lines.append(f"- `{source}`")
    lines.append("")
    for mode, summary in payload["modes"].items():
        n = summary["n_goals"]
        lines.append(f"## Mode: `{mode}`")
        lines.append("")
        lines.append(f"- Goals: {n}")
        lines.append(f"- Attempts: {summary['n_attempts']}")
        lines.append("")
        lines.append("| Action | Exposure | Success | Gain vs empty | Loss vs empty | Net | Avg facts | Avg simps |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
        for action, row in sorted(summary["by_action"].items(), key=lambda item: (-item[1]["success"], item[0])):
            paired = row["paired_vs_empty"]
            if paired is None:
                gains = losses = net = "-"
            else:
                gains = str(len(paired["gains"]))
                losses = str(len(paired["losses"]))
                net = str(paired["net"])
            lines.append(
                f"| `{action}` | `{row['exposure']}` | {row['success']}/{n} ({pct(row['success'], n)}) | "
                f"{gains} | {losses} | {net} | {row['avg_facts']:.2f} | {row['avg_simps']:.2f} |"
            )
        lines.append("")
        lines.append("### Matched Triples")
        lines.append("")
        lines.append("| Base | Joint | Facts | Simps | Identity | Swapped | Count facts | Count simps | Random split | Joint-only |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for base, row in sorted(summary["triples"].items()):
            lines.append(
                f"| `{base}` | {row['joint']} | {row['facts']} | {row['simps']} | "
                f"{row['identity']} | {row['swapped']} | {row['countmatched_facts']} | "
                f"{row['countmatched_simps']} | {row['random_split']} | "
                f"{len(row['joint_only_over_single_channels'])} |"
            )
        lines.append("")
    lines.append("## Readout")
    lines.append("")
    lines.append("- Use this report to decide whether the Aesop mechanism is typed channel assignment, source composition, rule count, or identity exposure.")
    lines.append("- Keep `oracle_core` wording unless the `retrieved_only` mode independently supports the same phenomenon.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    input_paths: list[Path] = []
    for raw_path in args.inputs:
        matches = [Path(match) for match in glob.glob(str(raw_path))]
        input_paths.extend(matches or [raw_path])
    input_paths = sorted(input_paths)
    if not input_paths:
        raise ValueError("no input JSON files found")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in input_paths:
        payload = load_json(path)
        grouped[mode_from_payload(payload, path)].append(payload)

    summaries = {mode: summarize_mode(mode, payloads) for mode, payloads in grouped.items()}
    payload = {
        "experiment": "mathlib430_aesop_exact_controls_summary",
        "sources": [str(path) for path in input_paths],
        "modes": summaries,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_md(payload, args.out_md)
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
