"""Select disagreement goals for the Phase 1 reconstruction bridge."""

from __future__ import annotations

import argparse
import copy
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from data_io import load_goals_jsonl, write_goals_jsonl


def trace_runs_by_goal_policy(trace_result: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(run["goal_id"], run["policy"]): run for run in trace_result["runs"]}


def is_solved(index: dict[tuple[str, str], dict[str, Any]], goal_id: str, policy: str) -> bool:
    run = index.get((goal_id, policy))
    return bool(run and run.get("solved", False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", type=Path, required=True)
    parser.add_argument("--trace-result", type=Path, required=True)
    parser.add_argument("--out-goals", type=Path, required=True)
    parser.add_argument("--out-manifest", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    goals = load_goals_jsonl(args.goals)
    trace_result = json.loads(args.trace_result.read_text(encoding="utf-8"))
    index = trace_runs_by_goal_policy(trace_result)

    buckets: dict[str, list[Any]] = defaultdict(list)
    for goal in goals:
        gid = goal.goal_id
        no_core = is_solved(index, gid, "rule_far_no_core_tags")
        topk = is_solved(index, gid, "topk_expansion")
        static = is_solved(index, gid, "visible_feature_rerank")
        full = is_solved(index, gid, "rule_far_full")

        if no_core and not topk:
            buckets["far_over_topk"].append(goal)
        if no_core and not static:
            buckets["far_over_static"].append(goal)
        if full and not no_core:
            buckets["oracle_gap"].append(goal)
        if no_core and topk and static:
            buckets["all_success_control"].append(goal)

    quotas = [
        ("far_over_topk", 35),
        ("far_over_static", 35),
        ("oracle_gap", 15),
        ("all_success_control", 15),
    ]
    selected = []
    selected_ids: set[str] = set()
    category_counts: dict[str, int] = {}

    for category, quota in quotas:
        pool = list(buckets.get(category, []))
        rng.shuffle(pool)
        category_counts[category] = 0
        for goal in pool:
            if len(selected) >= args.max_goals:
                break
            if category_counts[category] >= quota:
                break
            if goal.goal_id in selected_ids:
                continue
            copied = copy.deepcopy(goal)
            copied.metadata["bridge_category"] = category
            selected.append(copied)
            selected_ids.add(copied.goal_id)
            category_counts[category] += 1

    if len(selected) < args.max_goals:
        fallback = list(goals)
        rng.shuffle(fallback)
        for goal in fallback:
            if len(selected) >= args.max_goals:
                break
            if goal.goal_id in selected_ids:
                continue
            copied = copy.deepcopy(goal)
            copied.metadata["bridge_category"] = "fallback"
            selected.append(copied)
            selected_ids.add(copied.goal_id)
            category_counts["fallback"] = category_counts.get("fallback", 0) + 1

    write_goals_jsonl(selected, args.out_goals)
    manifest = {
        "goals": str(args.goals),
        "trace_result": str(args.trace_result),
        "out_goals": str(args.out_goals),
        "max_goals": args.max_goals,
        "seed": args.seed,
        "available": {k: len(v) for k, v in sorted(buckets.items())},
        "selected": category_counts,
        "goal_ids": [goal.goal_id for goal in selected],
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {len(selected)} bridge goals to {args.out_goals}")
    print(json.dumps({"available": manifest["available"], "selected": category_counts}, indent=2))


if __name__ == "__main__":
    main()
