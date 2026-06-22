"""Analyze Phase 3 imported-core bridge replay results."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


POLICY_ORDER = [
    "learned_rerank",
    "learned_expansion",
    "rule_far_learned",
    "learned_base_fallback",
    "rule_far_learned_failure_specific",
    "rule_far_learned_second_stage",
    "rule_far_full",
]


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def first_attempt_failed(run: dict[str, Any]) -> bool:
    attempts = run.get("attempts") or []
    return bool(attempts and not attempts[0]["result"]["verified"])


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--trace-result", type=Path, required=True)
    parser.add_argument("--replay-result", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    trace = json.loads(args.trace_result.read_text(encoding="utf-8"))
    replay = json.loads(args.replay_result.read_text(encoding="utf-8"))
    replay_by_goal = {r["goal_id"]: r for r in replay["results"]}
    bridge_goal_ids = set(replay_by_goal)

    by_policy: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in trace["runs"]:
        if run["goal_id"] in bridge_goal_ids:
            by_policy[run["policy"]].append(run)

    policies = [p for p in POLICY_ORDER if p in by_policy] + sorted(set(by_policy) - set(POLICY_ORDER))

    lines = []
    lines.append("# Phase 3 Imported-Core Bridge Replay")
    lines.append("")
    lines.append("> Bridge success means trace-core proof-core recovery plus successful replay of the original traced tactic script in a real Lean process.")
    lines.append("")
    lines.append(f"- Replay goals: {len(bridge_goal_ids)}")
    lines.append(f"- Replay success: {replay['n_success']}/{replay['n_goals']} ({pct(replay['n_success'] / max(replay['n_goals'], 1))})")
    lines.append(f"- Trace result: `{args.trace_result}`")
    lines.append(f"- Replay result: `{args.replay_result}`")
    lines.append("")
    lines.append("| Policy | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |")
    lines.append("|---|---:|---:|---:|---:|---:|")

    policy_stats: dict[str, dict[str, float]] = {}
    for policy in policies:
        runs = by_policy[policy]
        n = len(runs)
        trace_solved = sum(1 for r in runs if r["solved"])
        bridge_solved = sum(
            1 for r in runs if r["solved"] and replay_by_goal[r["goal_id"]]["success"]
        )
        first_failed = sum(1 for r in runs if first_attempt_failed(r))
        bridge_recovered = sum(
            1
            for r in runs
            if r["first_failure_recovered"] and replay_by_goal[r["goal_id"]]["success"]
        )
        avg_premises = sum(r["total_premises_tried"] for r in runs) / n if n else 0.0
        bridge_rate = bridge_solved / n if n else 0.0
        ffr = bridge_recovered / first_failed if first_failed else 0.0
        policy_stats[policy] = {
            "bridge_rate": bridge_rate,
            "ffr": ffr,
            "avg_premises": avg_premises,
        }
        lines.append(
            f"| `{policy}` | {n} | {pct(trace_solved / max(n, 1))} | {pct(bridge_rate)} | "
            f"{pct(ffr)} | {avg_premises:.1f} |"
        )

    if "rule_far_learned_second_stage" in policy_stats and "learned_base_fallback" in policy_stats:
        second = policy_stats["rule_far_learned_second_stage"]
        fallback = policy_stats["learned_base_fallback"]
        lines.append("")
        lines.append("## Key Delta")
        lines.append("")
        lines.append(
            "- Bridge verified delta, second-stage minus fallback: "
            f"{100 * (second['bridge_rate'] - fallback['bridge_rate']):+.1f} points"
        )
        lines.append(
            "- Bridge FFR delta, second-stage minus fallback: "
            f"{100 * (second['ffr'] - fallback['ffr']):+.1f} points"
        )
        lines.append(
            "- Avg premise delta, second-stage minus fallback: "
            f"{second['avg_premises'] - fallback['avg_premises']:+.1f}"
        )
        final_policy = "rule_far_learned_second_stage_final_base_guardrail_8"
        if final_policy in policy_stats:
            final = policy_stats[final_policy]
            lines.append(
                "- Bridge verified delta, final-base8 minus fallback: "
                f"{100 * (final['bridge_rate'] - fallback['bridge_rate']):+.1f} points"
            )
            lines.append(
                "- Bridge FFR delta, final-base8 minus fallback: "
                f"{100 * (final['ffr'] - fallback['ffr']):+.1f} points"
            )
            lines.append(
                "- Avg premise delta, final-base8 minus fallback: "
                f"{final['avg_premises'] - fallback['avg_premises']:+.1f}"
            )

    lines.append("")
    lines.append("## Replay Status Counts")
    lines.append("")
    lines.append(f"- Overall: {dict(Counter(r['status'] for r in replay['results']))}")
    lines.append(f"- By category: {dict(Counter(r.get('category', 'unknown') for r in replay['results']))}")
    lines.append("")

    lines.append("## Category-Level Replay")
    lines.append("")
    lines.append("| Category | Goals | Replay verified |")
    lines.append("|---|---:|---:|")
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in replay["results"]:
        by_category[result.get("category", "unknown")].append(result)
    for category, results in sorted(by_category.items()):
        n = len(results)
        ok = sum(1 for r in results if r["success"])
        lines.append(f"| `{category}` | {n} | {pct(ok / max(n, 1))} |")

    lines.append("")
    lines.append("## Failed Replay Examples")
    lines.append("")
    failures = [r for r in replay["results"] if not r["success"]]
    for r in failures[:10]:
        tail = str(r.get("output_tail") or r.get("error") or "").replace("\n", " ")
        lines.append(f"- `{r['theorem']}` ({r.get('category', 'unknown')}): `{r['status']}`; {tail[:500]}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
