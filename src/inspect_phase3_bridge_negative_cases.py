"""Inspect Phase 3 bridge negative cases at premise/rank level."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from data_io import load_goals_jsonl
from feature_extraction import features_for_premise
from schema import Goal, Premise


SECOND_STAGE = "rule_far_learned_second_stage"
FALLBACK = "learned_base_fallback"
EXPANSION = "learned_expansion"


def pct(numerator: int | float, denominator: int | float) -> str:
    return f"{100 * numerator / max(denominator, 1):.1f}%"


def runs_by_goal_policy(trace_result: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(run["goal_id"], run["policy"]): run for run in trace_result["runs"]}


def run_for(index: dict[tuple[str, str], dict[str, Any]], goal_id: str, policy: str) -> dict[str, Any] | None:
    return index.get((goal_id, policy))


def selected_union(run: dict[str, Any] | None) -> set[str]:
    if not run:
        return set()
    selected: set[str] = set()
    for attempt in run.get("attempts", []):
        selected.update(attempt.get("premise_names", []))
    return selected


def selected_attempt_ids(run: dict[str, Any] | None, premise_name: str) -> list[int]:
    if not run:
        return []
    ids = []
    for attempt in run.get("attempts", []):
        if premise_name in set(attempt.get("premise_names", [])):
            ids.append(int(attempt.get("attempt_id", -1)))
    return ids


def noninitial_failure_types(run: dict[str, Any] | None) -> list[str]:
    if not run:
        return []
    failure_types = []
    for attempt in run.get("attempts", []):
        result = attempt.get("result", {})
        if result.get("verified"):
            continue
        failure = result.get("failure") or {}
        failure_type = failure.get("failure_type")
        if failure_type and failure_type not in failure_types:
            failure_types.append(str(failure_type))
    return failure_types


def first_failure_type(run: dict[str, Any] | None) -> str | None:
    types = noninitial_failure_types(run)
    return types[0] if types else None


def compact_message(run: dict[str, Any] | None, max_len: int = 180) -> str:
    if not run:
        return ""
    for attempt in reversed(run.get("attempts", [])):
        result = attempt.get("result", {})
        if result.get("verified"):
            continue
        failure = result.get("failure") or {}
        text = str(failure.get("message") or "")
        if not text:
            text = json.dumps(failure.get("raw", {}), ensure_ascii=False)
        text = " ".join(text.split())
        if len(text) <= max_len:
            return text
        return text[: max_len - 3] + "..."
    return ""


def rank_map(candidates: list[Premise], score_fn: Any) -> dict[str, int]:
    ranked = sorted(candidates, key=score_fn, reverse=True)
    return {premise.name: idx + 1 for idx, premise in enumerate(ranked)}


def score_feature(goal: Goal, premise: Premise, key: str, default: float = 0.0) -> float:
    features = features_for_premise(goal, premise)
    return float(features.get(key, default))


def rank_context(goal: Goal, failure_types: list[str]) -> dict[str, dict[str, int]]:
    ranks = {
        "base": rank_map(goal.candidates, lambda p: float(p.base_score)),
        "learned": rank_map(goal.candidates, lambda p: score_feature(goal, p, "learned_score", p.base_score)),
    }
    for failure_type in failure_types:
        key = f"second_stage_score_{failure_type}"
        ranks[f"second_stage:{failure_type}"] = rank_map(
            goal.candidates,
            lambda p, feature_key=key: score_feature(
                goal,
                p,
                feature_key,
                score_feature(goal, p, "learned_score", p.base_score),
            ),
        )
    return ranks


def premise_lookup(goal: Goal) -> dict[str, Premise]:
    return {premise.name: premise for premise in goal.candidates}


def case_groups_from_taxonomy(taxonomy: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    negatives = taxonomy.get("negative_cases", {})
    fallback_ids = {
        str(item["goal_id"])
        for item in negatives.get("fallback_bridge_over_second_stage", [])
    }
    both_fail_ids = {
        str(record["goal_id"])
        for record in taxonomy.get("records", [])
        if record.get("category") == "both_fail"
        and record.get("replay_success")
        and not record.get("second_stage_solved")
        and not record.get("fallback_solved")
    }

    for item in negatives.get("premise_selection_miss_second_stage", []):
        goal_id = str(item["goal_id"])
        if goal_id in fallback_ids:
            groups["fallback_bridge_over_second_stage"].append(item)
        elif goal_id in both_fail_ids:
            groups["replay_verified_both_fail"].append(item)
        else:
            groups["premise_selection_miss_second_stage_other"].append(item)
    return dict(groups)


def classify_case(
    *,
    core_missing_from_candidates: set[str],
    missing_after_second: set[str],
    selected_fallback: set[str],
    selected_expansion: set[str],
    rank_infos: list[dict[str, Any]],
    second_failure_types: list[str],
) -> list[str]:
    reasons = []
    if core_missing_from_candidates:
        reasons.append("candidate_pool_miss")
    if not missing_after_second:
        reasons.append("trace_failed_despite_core_selected")
    if missing_after_second & selected_fallback:
        reasons.append("second_stage_dropped_fallback_core")
    if missing_after_second & selected_expansion:
        reasons.append("second_stage_dropped_expansion_core")
    if not second_failure_types:
        reasons.append("missing_failure_type_signal")

    candidate_missing_infos = [info for info in rank_infos if info.get("in_candidates")]
    if candidate_missing_infos:
        min_second_ranks = [
            int(rank)
            for info in candidate_missing_infos
            for rank in info.get("second_stage_ranks", {}).values()
            if rank is not None
        ]
        max_best_rank = max(
            int(info.get("best_second_stage_rank") or 10**9)
            for info in candidate_missing_infos
        )
        if not min_second_ranks:
            reasons.append("missing_second_stage_scores")
        elif max_best_rank <= 96:
            reasons.append("budget_or_path_miss_with_core_ranked_in_top96")
        else:
            reasons.append("failure_conditioned_rank_miss")

    if not reasons:
        reasons.append("unclassified")
    return reasons


def inspect_case(
    *,
    group: str,
    item: dict[str, Any],
    goal: Goal,
    index: dict[tuple[str, str], dict[str, Any]],
    second_policy: str = SECOND_STAGE,
    fallback_policy: str = FALLBACK,
    expansion_policy: str = EXPANSION,
) -> dict[str, Any]:
    goal_id = str(item["goal_id"])
    second_run = run_for(index, goal_id, second_policy)
    fallback_run = run_for(index, goal_id, fallback_policy)
    expansion_run = run_for(index, goal_id, expansion_policy)

    selected_second = selected_union(second_run)
    selected_fallback = selected_union(fallback_run)
    selected_expansion = selected_union(expansion_run)
    candidates = premise_lookup(goal)
    candidate_names = set(candidates)
    proof_core = set(goal.proof_core)
    core_in_candidates = proof_core & candidate_names
    core_missing_from_candidates = proof_core - candidate_names
    missing_after_second = proof_core - selected_second

    second_failure_types = noninitial_failure_types(second_run)
    ranks = rank_context(goal, second_failure_types)
    rank_infos = []
    for premise_name in sorted(missing_after_second):
        premise = candidates.get(premise_name)
        if premise is None:
            rank_infos.append(
                {
                    "premise": premise_name,
                    "in_candidates": False,
                    "selected_by_fallback": premise_name in selected_fallback,
                    "selected_by_expansion": premise_name in selected_expansion,
                }
            )
            continue

        features = features_for_premise(goal, premise)
        second_stage_ranks = {
            failure_type: ranks.get(f"second_stage:{failure_type}", {}).get(premise_name)
            for failure_type in second_failure_types
        }
        present_ranks = [rank for rank in second_stage_ranks.values() if rank is not None]
        rank_infos.append(
            {
                "premise": premise_name,
                "in_candidates": True,
                "selected_by_fallback": premise_name in selected_fallback,
                "selected_by_expansion": premise_name in selected_expansion,
                "fallback_attempts": selected_attempt_ids(fallback_run, premise_name),
                "expansion_attempts": selected_attempt_ids(expansion_run, premise_name),
                "base_rank": ranks["base"].get(premise_name),
                "learned_rank": ranks["learned"].get(premise_name),
                "second_stage_ranks": second_stage_ranks,
                "best_second_stage_rank": min(present_ranks) if present_ranks else None,
                "base_score": float(premise.base_score),
                "learned_score": float(features.get("learned_score", premise.base_score)),
                "learned_rank_pct": features.get("learned_rank_pct"),
                "base_rank_pct": features.get("base_rank_pct"),
                "same_file": bool(features.get("same_file", False)),
                "imported_candidate": bool(features.get("imported_candidate", not bool(features.get("same_file", False)))),
                "decl_kind": features.get("decl_kind", "unknown"),
                "tags": list(premise.tags),
            }
        )

    reasons = classify_case(
        core_missing_from_candidates=core_missing_from_candidates,
        missing_after_second=missing_after_second,
        selected_fallback=selected_fallback,
        selected_expansion=selected_expansion,
        rank_infos=rank_infos,
        second_failure_types=second_failure_types,
    )

    return {
        "group": group,
        "goal_id": goal_id,
        "theorem": item.get("theorem") or goal.metadata.get("theorem", goal_id),
        "category": item.get("category") or goal.metadata.get("bridge_category", "unknown"),
        "proof_core_size": len(proof_core),
        "candidate_count": len(goal.candidates),
        "core_in_candidates": len(core_in_candidates),
        "core_missing_from_candidates": sorted(core_missing_from_candidates),
        "second_stage_solved": bool(second_run and second_run.get("solved")),
        "fallback_solved": bool(fallback_run and fallback_run.get("solved")),
        "expansion_solved": bool(expansion_run and expansion_run.get("solved")),
        "second_stage_attempts": len(second_run.get("attempts", [])) if second_run else 0,
        "fallback_attempts": len(fallback_run.get("attempts", [])) if fallback_run else 0,
        "expansion_attempts": len(expansion_run.get("attempts", [])) if expansion_run else 0,
        "second_stage_failure_types": second_failure_types,
        "second_stage_first_failure_type": first_failure_type(second_run),
        "second_stage_last_failure_message": compact_message(second_run),
        "second_stage_selected_core": sorted(proof_core & selected_second),
        "fallback_selected_core": sorted(proof_core & selected_fallback),
        "expansion_selected_core": sorted(proof_core & selected_expansion),
        "missing_after_second_stage": sorted(missing_after_second),
        "missing_premises": rank_infos,
        "reasons": reasons,
    }


def summarize_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    reason_counts = Counter(reason for case in cases for reason in case["reasons"])
    group_counts = Counter(case["group"] for case in cases)
    category_counts = Counter(case["category"] for case in cases)
    failure_counts = Counter(
        failure_type
        for case in cases
        for failure_type in case.get("second_stage_failure_types", [])
    )
    candidate_pool_misses = sum(1 for case in cases if case["core_missing_from_candidates"])
    fallback_core_drops = sum(
        1
        for case in cases
        if set(case["missing_after_second_stage"]) & set(case["fallback_selected_core"])
    )
    expansion_core_drops = sum(
        1
        for case in cases
        if set(case["missing_after_second_stage"]) & set(case["expansion_selected_core"])
    )

    best_second_ranks = [
        int(info["best_second_stage_rank"])
        for case in cases
        for info in case["missing_premises"]
        if info.get("best_second_stage_rank") is not None
    ]
    learned_ranks = [
        int(info["learned_rank"])
        for case in cases
        for info in case["missing_premises"]
        if info.get("learned_rank") is not None
    ]
    base_ranks = [
        int(info["base_rank"])
        for case in cases
        for info in case["missing_premises"]
        if info.get("base_rank") is not None
    ]

    def rank_stats(values: list[int]) -> dict[str, Any]:
        if not values:
            return {}
        return {
            "count": len(values),
            "median": float(statistics.median(values)),
            "min": min(values),
            "max": max(values),
            "top64": sum(1 for value in values if value <= 64),
            "top96": sum(1 for value in values if value <= 96),
        }

    return {
        "n_cases": len(cases),
        "group_counts": dict(group_counts),
        "category_counts": dict(category_counts),
        "reason_counts": dict(reason_counts),
        "second_stage_failure_type_counts": dict(failure_counts),
        "candidate_pool_miss_cases": candidate_pool_misses,
        "fallback_core_drop_cases": fallback_core_drops,
        "expansion_core_drop_cases": expansion_core_drops,
        "best_second_stage_rank_stats_for_missed_core": rank_stats(best_second_ranks),
        "learned_rank_stats_for_missed_core": rank_stats(learned_ranks),
        "base_rank_stats_for_missed_core": rank_stats(base_ranks),
    }


def lines_for_case(case: dict[str, Any]) -> list[str]:
    lines = [
        f"- `{case['theorem']}` ({case['category']}, `{case['group']}`)",
        f"  - reasons: {', '.join(f'`{reason}`' for reason in case['reasons'])}",
        (
            "  - core: "
            f"{len(case['second_stage_selected_core'])}/{case['proof_core_size']} selected by second-stage; "
            f"{len(case['fallback_selected_core'])}/{case['proof_core_size']} by fallback; "
            f"{len(case['expansion_selected_core'])}/{case['proof_core_size']} by expansion"
        ),
        f"  - failure types: {', '.join(f'`{t}`' for t in case['second_stage_failure_types']) or '`none`'}",
    ]
    if case["core_missing_from_candidates"]:
        lines.append(f"  - missing from candidate pool: {', '.join(f'`{p}`' for p in case['core_missing_from_candidates'])}")
    for info in case["missing_premises"][:4]:
        if not info.get("in_candidates"):
            lines.append(f"  - missed `{info['premise']}`: not in candidate pool")
            continue
        second_ranks = ", ".join(
            f"{failure_type}:{rank}"
            for failure_type, rank in info.get("second_stage_ranks", {}).items()
        )
        lines.append(
            f"  - missed `{info['premise']}`: learned_rank={info.get('learned_rank')}, "
            f"base_rank={info.get('base_rank')}, second_stage_ranks={second_ranks or 'none'}, "
            f"fallback={info.get('selected_by_fallback')}, expansion={info.get('selected_by_expansion')}, "
            f"same_file={info.get('same_file')}, kind={info.get('decl_kind')}"
        )
    return lines


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    cases = payload["cases"]
    lines = []
    lines.append("# Phase 3 Bridge Negative-Case Inspection")
    lines.append("")
    lines.append("This report inspects replay-verified misses where the second-stage controller did not recover trace-core proof cores.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Inspected cases: {summary['n_cases']}")
    lines.append(f"- Candidate-pool miss cases: {summary['candidate_pool_miss_cases']}")
    lines.append(f"- Second-stage dropped a fallback-selected core premise: {summary['fallback_core_drop_cases']}")
    lines.append(f"- Second-stage dropped an expansion-selected core premise: {summary['expansion_core_drop_cases']}")
    lines.append("")
    lines.append("### Groups")
    lines.append("")
    lines.append("| Group | Count |")
    lines.append("|---|---:|")
    for group, count in sorted(summary["group_counts"].items()):
        lines.append(f"| `{group}` | {count} |")
    lines.append("")
    lines.append("### Reasons")
    lines.append("")
    lines.append("| Reason | Count |")
    lines.append("|---|---:|")
    for reason, count in Counter(summary["reason_counts"]).most_common():
        lines.append(f"| `{reason}` | {count} |")
    lines.append("")
    lines.append("### Second-Stage Failure Types")
    lines.append("")
    lines.append("| Failure type | Count |")
    lines.append("|---|---:|")
    for failure_type, count in Counter(summary["second_stage_failure_type_counts"]).most_common():
        lines.append(f"| `{failure_type}` | {count} |")
    lines.append("")
    lines.append("### Missed-Core Rank Stats")
    lines.append("")
    lines.append("| Rank source | Count | Median | Min | Max | Top64 | Top96 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for key, label in [
        ("best_second_stage_rank_stats_for_missed_core", "best second-stage"),
        ("learned_rank_stats_for_missed_core", "learned"),
        ("base_rank_stats_for_missed_core", "base"),
    ]:
        stats = summary.get(key, {})
        if not stats:
            continue
        lines.append(
            f"| `{label}` | {stats['count']} | {stats['median']:.1f} | {stats['min']} | "
            f"{stats['max']} | {stats['top64']} | {stats['top96']} |"
        )
    lines.append("")

    lines.append("## Case Details")
    lines.append("")
    for group in sorted(summary["group_counts"]):
        lines.append(f"### `{group}`")
        lines.append("")
        for case in [case for case in cases if case["group"] == group]:
            lines.extend(lines_for_case(case))
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- Candidate-pool misses are benchmark/candidate-generation ceiling cases, not controller failures.")
    lines.append("- Fallback-core drops are the actionable controller weakness: the failure-conditioned scorer can improve positives while still needing a fallback-preservation guardrail.")
    lines.append("- Rank misses indicate the second-stage model did not learn enough signal for the observed failure type; these are the best targets for bridge-replay hybrid ablations.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--bridge-goals", type=Path, required=True)
    parser.add_argument("--taxonomy", type=Path, required=True)
    parser.add_argument("--trace-result", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--second-policy", default=SECOND_STAGE)
    parser.add_argument("--fallback-policy", default=FALLBACK)
    parser.add_argument("--expansion-policy", default=EXPANSION)
    args = parser.parse_args()

    goals = load_goals_jsonl(args.bridge_goals)
    goals_by_id = {goal.goal_id: goal for goal in goals}
    taxonomy = json.loads(args.taxonomy.read_text(encoding="utf-8"))
    trace = json.loads(args.trace_result.read_text(encoding="utf-8"))
    index = runs_by_goal_policy(trace)

    cases = []
    seen: set[tuple[str, str]] = set()
    groups = case_groups_from_taxonomy(taxonomy)
    for group, items in groups.items():
        for item in items:
            goal_id = str(item["goal_id"])
            key = (group, goal_id)
            if key in seen:
                continue
            seen.add(key)
            goal = goals_by_id.get(goal_id)
            if goal is None:
                continue
            cases.append(
                inspect_case(
                    group=group,
                    item=item,
                    goal=goal,
                    index=index,
                    second_policy=args.second_policy,
                    fallback_policy=args.fallback_policy,
                    expansion_policy=args.expansion_policy,
                )
            )

    payload = {
        "inputs": {
            "bridge_goals": str(args.bridge_goals),
            "taxonomy": str(args.taxonomy),
            "trace_result": str(args.trace_result),
            "second_policy": args.second_policy,
            "fallback_policy": args.fallback_policy,
            "expansion_policy": args.expansion_policy,
        },
        "summary": summarize_cases(cases),
        "cases": cases,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(payload, args.out_md)
    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_md}")


if __name__ == "__main__":
    main()
