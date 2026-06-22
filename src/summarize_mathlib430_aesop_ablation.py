#!/usr/bin/env python3
"""Summarize focused Aesop ablation outcomes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pct(num: int, den: int) -> str:
    if den == 0:
        return "0.0%"
    return f"{100.0 * num / den:.1f}%"


def action_bucket(action: str) -> tuple[str, str]:
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
    return "other", "other"


def verified_by_goal(payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_goal: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in payload["results"]:
        if row.get("verified"):
            by_goal[str(row["goal_id"])].append(row)
    return by_goal


def summarize(ablation: dict[str, Any], baseline: dict[str, Any] | None) -> dict[str, Any]:
    rows = [row for row in ablation["results"] if str(row.get("action", "")).startswith("aesop_")]
    n_goals = len({row["goal_id"] for row in rows})
    action_counts: dict[str, dict[str, Any]] = {}
    source_counts: Counter[str] = Counter()
    exposure_counts: Counter[str] = Counter()
    source_exposure_counts: Counter[tuple[str, str]] = Counter()
    proved_by_goal: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        action = str(row["action"])
        source, exposure = action_bucket(action)
        bucket = action_counts.setdefault(
            action,
            {
                "attempts": 0,
                "verified": 0,
                "verified_goals": 0,
                "source": source,
                "exposure": exposure,
            },
        )
        bucket["attempts"] += 1
        if row.get("verified"):
            bucket["verified"] += 1
            proved_by_goal[str(row["goal_id"])].append(row)

    for action, bucket in action_counts.items():
        bucket["verified_goals"] = len(
            {row["goal_id"] for row in rows if row.get("verified") and row["action"] == action}
        )

    for goal, goal_rows in proved_by_goal.items():
        source_seen = set()
        exposure_seen = set()
        source_exposure_seen = set()
        for row in goal_rows:
            source, exposure = action_bucket(str(row["action"]))
            source_seen.add(source)
            exposure_seen.add(exposure)
            source_exposure_seen.add((source, exposure))
        for source in source_seen:
            source_counts[source] += 1
        for exposure in exposure_seen:
            exposure_counts[exposure] += 1
        for key in source_exposure_seen:
            source_exposure_counts[key] += 1

    baseline_solved = set(verified_by_goal(baseline).keys()) if baseline else set()
    ablation_solved = set(proved_by_goal.keys())
    new_goals = sorted(ablation_solved - baseline_solved)
    recovered_details = []
    for goal in new_goals:
        recovered_details.append(
            {
                "goal_id": goal,
                "actions": sorted(
                    {
                        str(row["action"])
                        for row in proved_by_goal[goal]
                    }
                ),
            }
        )

    return {
        "n_goals": n_goals,
        "n_actions": len(action_counts),
        "n_ablation_solved_goals": len(ablation_solved),
        "n_new_goals_over_baseline": len(new_goals),
        "action_counts": action_counts,
        "source_counts": dict(source_counts),
        "exposure_counts": dict(exposure_counts),
        "source_exposure_counts": {
            f"{source}|{exposure}": count
            for (source, exposure), count in source_exposure_counts.items()
        },
        "new_goals_over_baseline": recovered_details,
    }


def markdown_report(payload: dict[str, Any]) -> str:
    n = int(payload["summary"]["n_goals"])
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Focused Aesop Ablation")
    lines.append("")
    lines.append("Date: 2026-06-22")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Ablation matrix: `{payload['ablation_json']}`")
    if payload.get("baseline_json"):
        lines.append(f"- Baseline matrix: `{payload['baseline_json']}`")
    lines.append(f"- Goals: {n}")
    lines.append(f"- Aesop ablation actions: {payload['summary']['n_actions']}")
    lines.append("")
    lines.append("## By Action")
    lines.append("")
    lines.append("| Action | Source | Exposure | Verified goals | Attempts |")
    lines.append("|---|---|---|---:|---:|")
    for action, row in sorted(
        payload["summary"]["action_counts"].items(),
        key=lambda item: (-item[1]["verified_goals"], item[0]),
    ):
        lines.append(
            f"| `{action}` | `{row['source']}` | `{row['exposure']}` | "
            f"{row['verified_goals']} / {n} ({pct(row['verified_goals'], n)}) | {row['attempts']} |"
        )
    lines.append("")
    lines.append("## By Source")
    lines.append("")
    lines.append("| Source pool | Goals solved by at least one action |")
    lines.append("|---|---:|")
    for source, count in sorted(payload["summary"]["source_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{source}` | {count} / {n} ({pct(int(count), n)}) |")
    lines.append("")
    lines.append("## By Exposure")
    lines.append("")
    lines.append("| Exposure | Goals solved by at least one action |")
    lines.append("|---|---:|")
    for exposure, count in sorted(payload["summary"]["exposure_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{exposure}` | {count} / {n} ({pct(int(count), n)}) |")
    lines.append("")
    lines.append("## New Goals Over Baseline")
    lines.append("")
    new_goals = payload["summary"]["new_goals_over_baseline"]
    if not new_goals:
        lines.append("- None.")
    else:
        for row in new_goals:
            actions = ", ".join(f"`{action}`" for action in row["actions"])
            lines.append(f"- `{row['goal_id']}`: {actions}")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    lines.append(
        "- This report isolates whether Aesop gains come from fact rules, simp rules, or their combination."
    )
    lines.append(
        "- Use it to decide whether the final method should expose selected names to Aesop as facts, simp lemmas, or both."
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ablation-json", required=True, type=Path)
    parser.add_argument("--baseline-json", type=Path, default=None)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    ablation = load_json(args.ablation_json)
    baseline = load_json(args.baseline_json) if args.baseline_json else None
    summary = summarize(ablation, baseline)
    payload = {
        "ablation_json": str(args.ablation_json),
        "baseline_json": str(args.baseline_json) if args.baseline_json else None,
        "summary": summary,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(markdown_report(payload), encoding="utf-8")
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
