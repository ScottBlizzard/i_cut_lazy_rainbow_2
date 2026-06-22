"""Analyze Phase 1 reconstruction bridge results."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def main() -> None:
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

    lines = []
    lines.append("# Phase 1 Reconstruction Bridge")
    lines.append("")
    lines.append("> Bridge success means trace-core proof-core recovery plus successful replay of the original traced tactic script in a real Lean process.")
    lines.append("")
    lines.append(f"- Replay goals: {len(bridge_goal_ids)}")
    lines.append(f"- Replay success: {replay['n_success']}/{replay['n_goals']} ({pct(replay['n_success'] / replay['n_goals'])})")
    lines.append("")
    lines.append("| Policy | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |")
    lines.append("|---|---:|---:|---:|---:|---:|")

    for policy, runs in sorted(by_policy.items()):
        n = len(runs)
        trace_solved = sum(1 for r in runs if r["solved"])
        bridge_solved = sum(
            1 for r in runs if r["solved"] and replay_by_goal[r["goal_id"]]["success"]
        )
        first_failed = sum(
            1 for r in runs if r["attempts"] and not r["attempts"][0]["result"]["verified"]
        )
        bridge_recovered = sum(
            1
            for r in runs
            if r["first_failure_recovered"] and replay_by_goal[r["goal_id"]]["success"]
        )
        avg_premises = sum(r["total_premises_tried"] for r in runs) / n if n else 0.0
        ffr = bridge_recovered / first_failed if first_failed else 0.0
        lines.append(
            f"| `{policy}` | {n} | {pct(trace_solved / n)} | {pct(bridge_solved / n)} | "
            f"{pct(ffr)} | {avg_premises:.1f} |"
        )

    lines.append("")
    lines.append("## Replay Status Counts")
    lines.append("")
    lines.append(f"- Overall: {dict(Counter(r['status'] for r in replay['results']))}")
    lines.append(f"- By category: {dict(Counter(r.get('category', 'unknown') for r in replay['results']))}")
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
