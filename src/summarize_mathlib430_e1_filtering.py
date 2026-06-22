#!/usr/bin/env python3
"""Summarize E1 strict interface-filtering runs against the baseline matrix."""

from __future__ import annotations

import argparse
import json
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


def verified_goals(payload: dict[str, Any]) -> set[str]:
    return {str(row["goal_id"]) for row in payload["results"] if row.get("verified")}


def by_action_verified(results: list[dict[str, Any]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    for row in results:
        if row.get("verified"):
            out[str(row["action"])].add(str(row["goal_id"]))
    return out


def audit_totals(filtered_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    totals: Counter[str] = Counter()
    by_category: Counter[str] = Counter()
    by_kind: Counter[str] = Counter()
    goal_rows = []
    for payload in filtered_payloads:
        availability = ((payload.get("summary") or {}).get("availability") or [])
        for row in availability:
            audit = row.get("candidate_audit") or {}
            goal_rows.append(
                {
                    "goal_id": row.get("goal_id", ""),
                    "checked": row.get("checked", 0),
                    "available": row.get("available", 0),
                    "failed": row.get("failed", 0),
                    "target_or_alias": audit.get("target_or_alias", 0),
                    "aesop_safe_fact_available": audit.get("aesop_safe_fact_available", 0),
                    "aesop_unsafe_fact_available": audit.get("aesop_unsafe_fact_available", 0),
                    "simp_safe_available": audit.get("simp_safe_available", 0),
                    "simp_unsafe_available": audit.get("simp_unsafe_available", 0),
                }
            )
            for key in [
                "selected",
                "available",
                "unavailable",
                "target_or_alias",
                "proof_core",
                "learned_candidate",
                "aesop_safe_fact_available",
                "aesop_unsafe_fact_available",
                "simp_safe_available",
                "simp_unsafe_available",
            ]:
                totals[key] += int(audit.get(key, 0))
            for key, value in (audit.get("by_category") or {}).items():
                by_category[key] += int(value)
            for key, value in (audit.get("by_decl_kind") or {}).items():
                by_kind[key] += int(value)
    return {
        "totals": dict(totals),
        "by_category": dict(by_category),
        "by_decl_kind": dict(by_kind),
        "goal_rows": goal_rows,
    }


def summarize(baseline: dict[str, Any], filtered_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    filtered_results = [row for payload in filtered_payloads for row in payload["results"]]
    baseline_solved = verified_goals(baseline)
    filtered_solved = {str(row["goal_id"]) for row in filtered_results if row.get("verified")}
    combined_solved = baseline_solved | filtered_solved
    filtered_by_action = by_action_verified(filtered_results)
    baseline_by_action = by_action_verified(baseline["results"])
    paired_actions = {}
    for action in sorted(filtered_by_action):
        source = action.removesuffix("_filtered")
        filtered_goals = filtered_by_action[action]
        baseline_goals = baseline_by_action.get(source, set())
        paired_actions[action] = {
            "source_action": source,
            "filtered_goals": len(filtered_goals),
            "baseline_goals": len(baseline_goals),
            "kept_from_source": len(filtered_goals & baseline_goals),
            "new_vs_source": sorted(filtered_goals - baseline_goals),
            "lost_vs_source": sorted(baseline_goals - filtered_goals),
        }
    return {
        "n_baseline_goals": int((baseline.get("summary") or {}).get("n_goals", len({row["goal_id"] for row in baseline["results"]}))),
        "baseline_oracle": len(baseline_solved),
        "filtered_oracle": len(filtered_solved),
        "combined_oracle": len(combined_solved),
        "new_oracle_goals": sorted(filtered_solved - baseline_solved),
        "filtered_only_lost_from_baseline": sorted(baseline_solved - filtered_solved),
        "filtered_by_action": {
            action: sorted(goals)
            for action, goals in sorted(filtered_by_action.items())
        },
        "paired_actions": paired_actions,
        "audit": audit_totals(filtered_payloads),
    }


def markdown(payload: dict[str, Any]) -> str:
    s = payload["summary"]
    n = s["n_baseline_goals"]
    lines: list[str] = []
    lines.append("# Mathlib 4.30 E1 Strict Interface Filtering")
    lines.append("")
    lines.append("Date: 2026-06-22")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Baseline matrix: `{payload['baseline_json']}`")
    for path in payload["filtered_jsons"]:
        lines.append(f"- Filtered part: `{path}`")
    lines.append("- Filter mode: `strict_aesop`")
    lines.append("- Filtered actions use suffix: `_filtered`")
    lines.append("")
    lines.append("## Oracle Readout")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Baseline oracle | {s['baseline_oracle']} / {n} ({pct(s['baseline_oracle'], n)}) |")
    lines.append(f"| Filtered-only oracle | {s['filtered_oracle']} / {n} ({pct(s['filtered_oracle'], n)}) |")
    lines.append(f"| Combined oracle | {s['combined_oracle']} / {n} ({pct(s['combined_oracle'], n)}) |")
    lines.append(f"| New oracle goals from filtering | {len(s['new_oracle_goals'])} |")
    lines.append("")
    lines.append("## Filtered Actions")
    lines.append("")
    lines.append("| Filtered action | Source action | Filtered goals | Source goals | Kept | New vs source | Lost vs source |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for action, row in sorted(
        s["paired_actions"].items(),
        key=lambda item: (-item[1]["filtered_goals"], item[0]),
    ):
        lines.append(
            f"| `{action}` | `{row['source_action']}` | {row['filtered_goals']} | "
            f"{row['baseline_goals']} | {row['kept_from_source']} | "
            f"{len(row['new_vs_source'])} | {len(row['lost_vs_source'])} |"
        )
    lines.append("")
    lines.append("## New Oracle Goals")
    lines.append("")
    if s["new_oracle_goals"]:
        for goal in s["new_oracle_goals"]:
            lines.append(f"- `{goal}`")
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Candidate Audit")
    lines.append("")
    totals = s["audit"]["totals"]
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    for key in sorted(totals):
        lines.append(f"| `{key}` | {totals[key]} |")
    lines.append("")
    lines.append("### By Category")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    for key, value in sorted(s["audit"]["by_category"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("### By Decl Kind")
    lines.append("")
    lines.append("| Decl kind | Count |")
    lines.append("|---|---:|")
    for key, value in sorted(s["audit"]["by_decl_kind"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    if s["combined_oracle"] > s["baseline_oracle"]:
        lines.append("- Filtering adds new oracle headroom and should be promoted to the main verified matrix.")
    elif s["filtered_oracle"] > 0:
        lines.append("- Filtering does not raise oracle headroom, but it provides a cleaner robustness/mechanism audit.")
    else:
        lines.append("- Filtering removes all successes and should not be used as the main action policy.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-json", required=True, type=Path)
    parser.add_argument("--filtered-jsons", nargs="+", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    baseline = load_json(args.baseline_json)
    filtered = [load_json(path) for path in args.filtered_jsons]
    summary = summarize(baseline, filtered)
    payload = {
        "baseline_json": str(args.baseline_json),
        "filtered_jsons": [str(path) for path in args.filtered_jsons],
        "summary": summary,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(markdown(payload), encoding="utf-8")
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
