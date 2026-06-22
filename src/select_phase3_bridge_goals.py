"""Select Phase 3 imported-core bridge replay goals."""

from __future__ import annotations

import argparse
import copy
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from data_io import load_goals_jsonl, write_goals_jsonl


REQUIRED_REPLAY_METADATA = ("repo_url", "file_path", "start", "theorem", "tactic_script")


def runs_by_goal_policy(trace_result: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(run["goal_id"], run["policy"]): run for run in trace_result["runs"]}


def is_solved(index: dict[tuple[str, str], dict[str, Any]], goal_id: str, policy: str) -> bool:
    run = index.get((goal_id, policy))
    return bool(run and run.get("solved", False))


def has_replay_metadata(goal: Any) -> bool:
    metadata = getattr(goal, "metadata", {})
    return all(metadata.get(key) not in (None, "", []) for key in REQUIRED_REPLAY_METADATA)


def split_label(goal: Any) -> str:
    metadata = getattr(goal, "metadata", {})
    if "phase3_split_fold" in metadata:
        return f"fold{metadata['phase3_split_fold']}"
    return "main"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", type=Path, required=True)
    parser.add_argument("--trace-result", type=Path, required=True)
    parser.add_argument("--out-goals", type=Path, required=True)
    parser.add_argument("--out-manifest", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--second-policy", default="rule_far_learned_second_stage")
    parser.add_argument("--fallback-policy", default="learned_base_fallback")
    parser.add_argument("--expansion-policy", default="learned_expansion")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    goals = load_goals_jsonl(args.goals)
    trace_result = json.loads(args.trace_result.read_text(encoding="utf-8"))
    index = runs_by_goal_policy(trace_result)

    buckets: dict[str, list[Any]] = defaultdict(list)
    skipped_missing_metadata = []
    for goal in goals:
        if not has_replay_metadata(goal):
            skipped_missing_metadata.append(goal.goal_id)
            continue

        gid = goal.goal_id
        second_stage = is_solved(index, gid, args.second_policy)
        fallback = is_solved(index, gid, args.fallback_policy)
        expansion = is_solved(index, gid, args.expansion_policy)

        if second_stage and not fallback:
            buckets["second_stage_over_fallback"].append(goal)
        if second_stage and not expansion:
            buckets["second_stage_over_expansion"].append(goal)
        if fallback and not second_stage:
            buckets["fallback_over_second_stage"].append(goal)
        if (not second_stage) and (not fallback):
            buckets["both_fail"].append(goal)
        if second_stage and fallback:
            buckets["both_success"].append(goal)

    base_quotas = [
        ("second_stage_over_fallback", 40),
        ("second_stage_over_expansion", 20),
        ("fallback_over_second_stage", 10),
        ("both_fail", 20),
        ("both_success", 10),
    ]
    scale = max(args.max_goals, 1) / 100.0
    quotas = [(category, max(1, int(round(quota * scale)))) for category, quota in base_quotas]
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
            copied.metadata["bridge_source_split"] = split_label(goal)
            selected.append(copied)
            selected_ids.add(copied.goal_id)
            category_counts[category] += 1

    if len(selected) < args.max_goals:
        fallback_pool = [goal for goal in goals if has_replay_metadata(goal)]
        rng.shuffle(fallback_pool)
        for goal in fallback_pool:
            if len(selected) >= args.max_goals:
                break
            if goal.goal_id in selected_ids:
                continue
            copied = copy.deepcopy(goal)
            copied.metadata["bridge_category"] = "fallback_fill"
            copied.metadata["bridge_source_split"] = split_label(goal)
            selected.append(copied)
            selected_ids.add(copied.goal_id)
            category_counts["fallback_fill"] = category_counts.get("fallback_fill", 0) + 1

    write_goals_jsonl(selected, args.out_goals)
    manifest = {
        "goals": str(args.goals),
        "trace_result": str(args.trace_result),
        "out_goals": str(args.out_goals),
        "max_goals": args.max_goals,
        "seed": args.seed,
        "second_policy": args.second_policy,
        "fallback_policy": args.fallback_policy,
        "expansion_policy": args.expansion_policy,
        "required_replay_metadata": list(REQUIRED_REPLAY_METADATA),
        "skipped_missing_metadata": len(skipped_missing_metadata),
        "skipped_missing_metadata_goal_ids": skipped_missing_metadata[:50],
        "available": {k: len(v) for k, v in sorted(buckets.items())},
        "selected": category_counts,
        "goal_ids": [goal.goal_id for goal in selected],
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {len(selected)} Phase 3 bridge goals to {args.out_goals}")
    print(
        json.dumps(
            {
                "available": manifest["available"],
                "selected": category_counts,
                "skipped_missing_metadata": len(skipped_missing_metadata),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
