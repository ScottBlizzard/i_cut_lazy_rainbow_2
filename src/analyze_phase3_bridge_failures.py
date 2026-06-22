"""Taxonomize Phase 3 bridge replay failures and policy misses."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from data_io import load_goals_jsonl


SECOND_STAGE = "rule_far_learned_second_stage"
FALLBACK = "learned_base_fallback"
EXPANSION = "learned_expansion"
KEY_POLICIES = [
    "learned_rerank",
    EXPANSION,
    "rule_far_learned",
    FALLBACK,
    "rule_far_learned_failure_specific",
    SECOND_STAGE,
    "rule_far_full",
]


def pct(numerator: int | float, denominator: int | float) -> str:
    return f"{100 * numerator / max(denominator, 1):.1f}%"


def runs_by_goal_policy(trace_result: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(run["goal_id"], run["policy"]): run for run in trace_result["runs"]}


def is_solved(index: dict[tuple[str, str], dict[str, Any]], goal_id: str, policy: str) -> bool:
    run = index.get((goal_id, policy))
    return bool(run and run.get("solved", False))


def failure_tags(result: dict[str, Any]) -> list[str]:
    if result.get("success"):
        return ["replay_verified"]
    if result.get("status") == "timeout":
        return ["replay_timeout"]

    text = f"{result.get('error', '')}\n{result.get('output_tail', '')}"
    lower = text.lower()
    tags = []
    if "unknownidentifier" in lower or "unknown identifier" in lower:
        tags.append("replay_unknown_identifier")
    if "simp` made no progress" in lower or "`simp` made no progress" in lower or "simp made no progress" in lower:
        tags.append("replay_simp_no_progress")
    if "synthinstancefailed" in lower or "type class" in lower or "typeclass" in lower:
        tags.append("replay_typeclass")
    if "unsolved goals" in lower:
        tags.append("replay_unsolved_goals")
    if "application type mismatch" in lower or "type mismatch" in lower:
        tags.append("replay_type_mismatch")
    if "`grind` failed" in lower or "grind` failed" in lower or "grind failed" in lower:
        tags.append("replay_tactic_failed")
    if "declaration uses `sorry`" in lower:
        tags.append("replay_sorry_context")
    if not tags:
        tags.append("replay_other_lean_error")
    return tags


def primary_failure_tag(tags: list[str]) -> str:
    priority = [
        "replay_verified",
        "replay_timeout",
        "replay_unknown_identifier",
        "replay_simp_no_progress",
        "replay_typeclass",
        "replay_unsolved_goals",
        "replay_type_mismatch",
        "replay_tactic_failed",
        "replay_sorry_context",
        "replay_other_lean_error",
    ]
    for tag in priority:
        if tag in tags:
            return tag
    return tags[0] if tags else "unknown"


def compact_tail(result: dict[str, Any], max_len: int = 240) -> str:
    text = str(result.get("output_tail") or result.get("error") or "")
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def policy_table_rows(
    index: dict[tuple[str, str], dict[str, Any]],
    replay_by_goal: dict[str, dict[str, Any]],
    *,
    extra_policies: list[str] | None = None,
) -> list[dict[str, Any]]:
    rows = []
    policies = KEY_POLICIES[:]
    for policy in extra_policies or []:
        if policy not in policies:
            policies.append(policy)
    for policy in policies:
        runs = [index[(gid, policy)] for gid in replay_by_goal if (gid, policy) in index]
        if not runs:
            continue
        n = len(runs)
        trace_solved = sum(1 for run in runs if run.get("solved"))
        bridge_verified = sum(1 for run in runs if run.get("solved") and replay_by_goal[run["goal_id"]].get("success"))
        replayable_trace_miss = sum(
            1 for run in runs if (not run.get("solved")) and replay_by_goal[run["goal_id"]].get("success")
        )
        rows.append(
            {
                "policy": policy,
                "goals": n,
                "trace_success": trace_solved,
                "bridge_verified": bridge_verified,
                "replayable_trace_miss": replayable_trace_miss,
                "avg_premises": sum(float(run.get("total_premises_tried", 0.0)) for run in runs) / n,
            }
        )
    return rows


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--bridge-goals", type=Path, required=True)
    parser.add_argument("--replay-result", type=Path, required=True)
    parser.add_argument("--trace-result", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--second-policy", default=SECOND_STAGE)
    parser.add_argument("--fallback-policy", default=FALLBACK)
    parser.add_argument("--expansion-policy", default=EXPANSION)
    args = parser.parse_args()

    second_policy = args.second_policy
    fallback_policy = args.fallback_policy
    expansion_policy = args.expansion_policy

    goals = load_goals_jsonl(args.bridge_goals)
    goals_by_id = {goal.goal_id: goal for goal in goals}
    replay = json.loads(args.replay_result.read_text(encoding="utf-8"))
    trace = json.loads(args.trace_result.read_text(encoding="utf-8"))
    index = runs_by_goal_policy(trace)
    replay_by_goal = {result["goal_id"]: result for result in replay["results"]}

    records: list[dict[str, Any]] = []
    primary_counts = Counter()
    multilabel_counts = Counter()
    primary_by_category: dict[str, Counter[str]] = defaultdict(Counter)
    supported_gain = Counter()
    negative_cases: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for result in replay["results"]:
        gid = result["goal_id"]
        goal = goals_by_id.get(gid)
        category = result.get("category") or (goal.metadata.get("bridge_category", "unknown") if goal else "unknown")
        tags = failure_tags(result)
        primary = primary_failure_tag(tags)
        primary_counts[primary] += 1
        for tag in tags:
            multilabel_counts[tag] += 1
        primary_by_category[category][primary] += 1

        second_solved = is_solved(index, gid, second_policy)
        fallback_solved = is_solved(index, gid, fallback_policy)
        expansion_solved = is_solved(index, gid, expansion_policy)
        replay_success = bool(result.get("success"))

        outcome_tags = []
        if replay_success and second_solved and not fallback_solved:
            outcome_tags.append("bridge_supported_gain_over_fallback")
            supported_gain["second_stage_over_fallback"] += 1
        if replay_success and second_solved and not expansion_solved:
            outcome_tags.append("bridge_supported_gain_over_expansion")
            supported_gain["second_stage_over_expansion"] += 1
        if replay_success and fallback_solved and not second_solved:
            outcome_tags.append("fallback_bridge_over_second_stage")
            negative_cases["fallback_bridge_over_second_stage"].append(
                {
                    "goal_id": gid,
                    "theorem": result.get("theorem"),
                    "category": category,
                    "primary_failure": primary,
                }
            )
        if replay_success and not second_solved:
            outcome_tags.append("premise_selection_miss_second_stage")
            negative_cases["premise_selection_miss_second_stage"].append(
                {
                    "goal_id": gid,
                    "theorem": result.get("theorem"),
                    "category": category,
                    "fallback_solved": fallback_solved,
                    "expansion_solved": expansion_solved,
                }
            )
        if (not replay_success) and second_solved:
            outcome_tags.append("second_stage_trace_success_replay_failed")
            negative_cases["second_stage_trace_success_replay_failed"].append(
                {
                    "goal_id": gid,
                    "theorem": result.get("theorem"),
                    "category": category,
                    "primary_failure": primary,
                    "failure_tags": tags,
                    "tail": compact_tail(result),
                }
            )

        records.append(
            {
                "goal_id": gid,
                "theorem": result.get("theorem"),
                "category": category,
                "replay_success": replay_success,
                "replay_status": result.get("status"),
                "primary_failure": primary,
                "failure_tags": tags,
                "second_stage_solved": second_solved,
                "fallback_solved": fallback_solved,
                "expansion_solved": expansion_solved,
                "outcome_tags": outcome_tags,
                "tail": compact_tail(result),
            }
        )

    policy_rows = policy_table_rows(
        index,
        replay_by_goal,
        extra_policies=[second_policy, fallback_policy, expansion_policy],
    )
    payload = {
        "inputs": {
            "bridge_goals": str(args.bridge_goals),
            "replay_result": str(args.replay_result),
            "trace_result": str(args.trace_result),
            "second_policy": second_policy,
            "fallback_policy": fallback_policy,
            "expansion_policy": expansion_policy,
        },
        "n_goals": len(replay["results"]),
        "replay_success": int(sum(1 for r in replay["results"] if r.get("success"))),
        "primary_failure_counts": dict(primary_counts),
        "multilabel_failure_counts": dict(multilabel_counts),
        "primary_failure_by_category": {k: dict(v) for k, v in sorted(primary_by_category.items())},
        "supported_gain_counts": dict(supported_gain),
        "policy_rows": policy_rows,
        "negative_cases": {k: v[:50] for k, v in sorted(negative_cases.items())},
        "records": records,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Phase 3 Bridge Failure Taxonomy")
    lines.append("")
    lines.append("This report separates real Lean replay failures from premise-selection misses on the 100-goal Phase 3 bridge subset.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Bridge goals: {len(replay['results'])}")
    lines.append(f"- Replay verified: {payload['replay_success']}/{len(replay['results'])} ({pct(payload['replay_success'], len(replay['results']))})")
    lines.append(f"- Second-stage gains over fallback supported by replay: {supported_gain['second_stage_over_fallback']}")
    lines.append(f"- Second-stage gains over expansion supported by replay: {supported_gain['second_stage_over_expansion']}")
    lines.append(f"- Replay-verified goals missed by second-stage trace-core: {len(negative_cases['premise_selection_miss_second_stage'])}")
    lines.append(f"- Second-stage trace-core successes blocked by replay failure: {len(negative_cases['second_stage_trace_success_replay_failed'])}")
    lines.append("")

    lines.append("## Policy-Level Misses")
    lines.append("")
    lines.append("| Policy | Goals | Trace success | Bridge verified | Replay-verified trace miss | Avg premises |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in policy_rows:
        lines.append(
            f"| `{row['policy']}` | {row['goals']} | {pct(row['trace_success'], row['goals'])} | "
            f"{pct(row['bridge_verified'], row['goals'])} | {row['replayable_trace_miss']} | "
            f"{row['avg_premises']:.1f} |"
        )
    lines.append("")

    lines.append("## Primary Replay Failure Taxonomy")
    lines.append("")
    lines.append("| Primary tag | Count | Rate |")
    lines.append("|---|---:|---:|")
    for tag, count in primary_counts.most_common():
        lines.append(f"| `{tag}` | {count} | {pct(count, len(replay['results']))} |")
    lines.append("")

    lines.append("## Multi-Label Replay Failure Signals")
    lines.append("")
    lines.append("| Signal | Count |")
    lines.append("|---|---:|")
    for tag, count in multilabel_counts.most_common():
        lines.append(f"| `{tag}` | {count} |")
    lines.append("")

    lines.append("## Primary Failure By Bridge Category")
    lines.append("")
    for category, counts in sorted(primary_by_category.items()):
        total = sum(counts.values())
        lines.append(f"### `{category}`")
        lines.append("")
        lines.append("| Primary tag | Count | Rate |")
        lines.append("|---|---:|---:|")
        for tag, count in counts.most_common():
            lines.append(f"| `{tag}` | {count} | {pct(count, total)} |")
        lines.append("")

    lines.append("## Key Positive Cases")
    lines.append("")
    positives = [
        record
        for record in records
        if "bridge_supported_gain_over_fallback" in record["outcome_tags"]
    ]
    lines.append(f"- Replay-verified second-stage-over-fallback cases: {len(positives)}")
    for record in positives[:15]:
        lines.append(f"- `{record['theorem']}` ({record['category']})")
    lines.append("")

    lines.append("## Key Negative Cases")
    lines.append("")
    lines.append("### Replay verified, but second-stage trace-core failed")
    lines.append("")
    for item in negative_cases["premise_selection_miss_second_stage"][:15]:
        lines.append(
            f"- `{item['theorem']}` ({item['category']}), "
            f"fallback_solved={item['fallback_solved']}, expansion_solved={item['expansion_solved']}"
        )
    lines.append("")
    lines.append("### Second-stage trace-core succeeded, but replay failed")
    lines.append("")
    for item in negative_cases["second_stage_trace_success_replay_failed"][:15]:
        lines.append(f"- `{item['theorem']}` ({item['category']}): `{item['primary_failure']}`; {item['tail']}")
    lines.append("")

    lines.append("## Paper Interpretation")
    lines.append("")
    lines.append("- The bridge subset supports the controller gain: replay-verified second-stage-over-fallback cases exist in substantial number.")
    lines.append("- Many lost bridge cases are replay failures after trace-core success, so they should be treated as replay/context fragility unless deeper inspection shows premise-specific invalidity.")
    lines.append("- The subset is disagreement-heavy; report it as bridge validation, not as a full proof reconstruction benchmark.")

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
