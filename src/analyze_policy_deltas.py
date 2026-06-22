"""Compare two policies goal-by-goal in a trace-core result."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def pct(numerator: int | float, denominator: int | float) -> str:
    return f"{100 * numerator / max(denominator, 1):.1f}%"


def compact_failure(run: dict[str, Any]) -> str:
    attempts = run.get("attempts", [])
    if not attempts:
        return "no_attempt"
    failure = (attempts[-1].get("result") or {}).get("failure")
    if not failure:
        return "verified"
    return str(failure.get("failure_type", "unknown"))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--trace-result", type=Path, required=True)
    parser.add_argument("--base-policy", required=True)
    parser.add_argument("--new-policy", required=True)
    parser.add_argument("--replay-result", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    trace = json.loads(args.trace_result.read_text(encoding="utf-8"))
    by_key = {(run["goal_id"], run["policy"]): run for run in trace["runs"]}
    goal_ids = sorted({goal_id for goal_id, policy in by_key if policy == args.base_policy})

    replay_by_goal: dict[str, dict[str, Any]] = {}
    if args.replay_result:
        replay = json.loads(args.replay_result.read_text(encoding="utf-8"))
        replay_by_goal = {result["goal_id"]: result for result in replay["results"]}
        goal_ids = [goal_id for goal_id in goal_ids if goal_id in replay_by_goal]

    gained = []
    lost = []
    same_solved = 0
    same_failed = 0
    for goal_id in goal_ids:
        base = by_key.get((goal_id, args.base_policy))
        new = by_key.get((goal_id, args.new_policy))
        if not base or not new:
            continue
        base_solved = bool(base.get("solved"))
        new_solved = bool(new.get("solved"))
        replay = replay_by_goal.get(goal_id, {})
        item = {
            "goal_id": goal_id,
            "theorem": replay.get("theorem") or goal_id,
            "category": replay.get("category", "unknown"),
            "replay_success": replay.get("success"),
            "base_failure": compact_failure(base),
            "new_failure": compact_failure(new),
            "base_premises": base.get("total_premises_tried"),
            "new_premises": new.get("total_premises_tried"),
        }
        if (not base_solved) and new_solved:
            gained.append(item)
        elif base_solved and (not new_solved):
            lost.append(item)
        elif base_solved and new_solved:
            same_solved += 1
        else:
            same_failed += 1

    replay_gained = sum(1 for item in gained if item.get("replay_success"))
    replay_lost = sum(1 for item in lost if item.get("replay_success"))
    payload = {
        "trace_result": str(args.trace_result),
        "replay_result": str(args.replay_result) if args.replay_result else None,
        "base_policy": args.base_policy,
        "new_policy": args.new_policy,
        "n_goals": len(goal_ids),
        "same_solved": same_solved,
        "same_failed": same_failed,
        "gained": gained,
        "lost": lost,
        "replay_gained": replay_gained,
        "replay_lost": replay_lost,
    }

    lines = []
    lines.append("# Policy Delta Analysis")
    lines.append("")
    lines.append(f"- Base policy: `{args.base_policy}`")
    lines.append(f"- New policy: `{args.new_policy}`")
    lines.append(f"- Goals: {len(goal_ids)}")
    lines.append(f"- Same solved: {same_solved} ({pct(same_solved, len(goal_ids))})")
    lines.append(f"- Same failed: {same_failed} ({pct(same_failed, len(goal_ids))})")
    lines.append(f"- New-only solved: {len(gained)}")
    lines.append(f"- Base-only solved: {len(lost)}")
    if replay_by_goal:
        lines.append(f"- Replay-verified new-only solved: {replay_gained}")
        lines.append(f"- Replay-verified base-only solved: {replay_lost}")
    lines.append("")

    lines.append("## New-Only Solved")
    lines.append("")
    for item in gained[:50]:
        replay_text = ""
        if replay_by_goal:
            replay_text = f", replay_success={item['replay_success']}, category={item['category']}"
        lines.append(
            f"- `{item['theorem']}`{replay_text}; "
            f"base_failure={item['base_failure']}, premises {item['base_premises']} -> {item['new_premises']}"
        )
    lines.append("")

    lines.append("## Base-Only Solved")
    lines.append("")
    for item in lost[:50]:
        replay_text = ""
        if replay_by_goal:
            replay_text = f", replay_success={item['replay_success']}, category={item['category']}"
        lines.append(
            f"- `{item['theorem']}`{replay_text}; "
            f"new_failure={item['new_failure']}, premises {item['base_premises']} -> {item['new_premises']}"
        )
    lines.append("")

    json_out = args.out.with_suffix(".json")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
