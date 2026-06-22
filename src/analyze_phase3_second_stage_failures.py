"""Taxonomize remaining Phase 3 trace-core failures."""

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


FAILURE_TYPES = [
    "imported_premise_missing",
    "missing_bridge",
    "type_mismatch",
    "rewrite_direction",
    "typeclass_missing",
    "reconstruction_failure",
    "local_context_missing",
    "timeout",
]


def pct(numerator: int | float, denominator: int | float) -> str:
    return f"{100 * numerator / max(denominator, 1):.1f}%"


def selected_union(run: dict[str, Any]) -> set[str]:
    selected: set[str] = set()
    for attempt in run.get("attempts", []):
        selected.update(attempt.get("premise_names", []))
    return selected


def failure_types(run: dict[str, Any]) -> list[str]:
    values = []
    for attempt in run.get("attempts", []):
        result = attempt.get("result", {})
        if result.get("verified"):
            continue
        failure = result.get("failure") or {}
        failure_type = failure.get("failure_type")
        if failure_type:
            values.append(str(failure_type))
    return values


def rank_map(candidates: list[Premise], score_fn: Any) -> dict[str, int]:
    ranked = sorted(candidates, key=score_fn, reverse=True)
    return {premise.name: idx + 1 for idx, premise in enumerate(ranked)}


def rank_context(goal: Goal) -> dict[str, dict[str, int]]:
    ranks = {
        "base": rank_map(goal.candidates, lambda p: float(p.base_score)),
        "learned": rank_map(
            goal.candidates,
            lambda p: float(features_for_premise(goal, p).get("learned_score", p.base_score)),
        ),
    }
    for failure_type in FAILURE_TYPES:
        key = f"second_stage_score_{failure_type}"
        ranks[f"second_stage:{failure_type}"] = rank_map(
            goal.candidates,
            lambda p, feature_key=key: float(
                features_for_premise(goal, p).get(
                    feature_key,
                    features_for_premise(goal, p).get("learned_score", p.base_score),
                )
            ),
        )
    return ranks


def max_rank_for(names: set[str], ranks: dict[str, int]) -> int | None:
    values = [ranks[name] for name in names if name in ranks]
    if len(values) != len(names):
        return None
    return max(values) if values else 0


def classify_case(
    *,
    missing_after_policy: set[str],
    missing_from_candidates: set[str],
    last_failure_type: str | None,
    max_last_rank: int | None,
    max_best_rank: int | None,
    max_base_rank: int | None,
    baseline_solved: bool,
) -> list[str]:
    tags = []
    if missing_from_candidates:
        tags.append("candidate_pool_miss")
    if baseline_solved:
        tags.append("fallback_solved_policy_failed")
    if not missing_after_policy:
        tags.append("trace_failed_despite_core_selected")
    if max_last_rank is not None and max_last_rank <= 96:
        tags.append("last_failure_top96_but_not_selected")
    if max_best_rank is not None and (max_last_rank is None or max_best_rank + 24 < max_last_rank):
        tags.append("expert_misrouting_signal")
    if max_base_rank is not None and max_base_rank <= 16:
        tags.append("base_guardrail_candidate")
    if max_best_rank is not None:
        if max_best_rank <= 96:
            tags.append("best_expert_top96")
        elif max_best_rank <= 128:
            tags.append("best_expert_top128")
        elif max_best_rank <= 160:
            tags.append("best_expert_top160")
        else:
            tags.append("deep_rank_miss")
    if last_failure_type is None:
        tags.append("missing_failure_signal")
    if not tags:
        tags.append("unclassified")
    return tags


def inspect_policy(
    *,
    goals_by_id: dict[str, Goal],
    runs_by_key: dict[tuple[str, str], dict[str, Any]],
    policy: str,
    baseline_policy: str | None,
) -> dict[str, Any]:
    cases = []
    rank_values: dict[str, list[int]] = defaultdict(list)

    policy_runs = [run for (goal_id, run_policy), run in runs_by_key.items() if run_policy == policy]
    for run in policy_runs:
        if run.get("solved"):
            continue
        goal = goals_by_id.get(run["goal_id"])
        if goal is None:
            continue
        selected = selected_union(run)
        core = set(goal.proof_core)
        missing_after_policy = core - selected
        candidate_names = {premise.name for premise in goal.candidates}
        missing_from_candidates = missing_after_policy - candidate_names
        missing_in_candidates = missing_after_policy & candidate_names
        failures = failure_types(run)
        last_failure = failures[-1] if failures else None
        ranks = rank_context(goal)

        max_last = None
        if last_failure:
            max_last = max_rank_for(missing_in_candidates, ranks[f"second_stage:{last_failure}"])
        best_ranks = []
        for name in missing_in_candidates:
            best_ranks.append(
                min(ranks[f"second_stage:{failure_type}"].get(name, 10**9) for failure_type in FAILURE_TYPES)
            )
        max_best = max(best_ranks) if best_ranks else None
        max_base = max_rank_for(missing_in_candidates, ranks["base"])
        max_learned = max_rank_for(missing_in_candidates, ranks["learned"])

        baseline_run = runs_by_key.get((run["goal_id"], baseline_policy)) if baseline_policy else None
        baseline_solved = bool(baseline_run and baseline_run.get("solved"))
        tags = classify_case(
            missing_after_policy=missing_after_policy,
            missing_from_candidates=missing_from_candidates,
            last_failure_type=last_failure,
            max_last_rank=max_last,
            max_best_rank=max_best,
            max_base_rank=max_base,
            baseline_solved=baseline_solved,
        )

        for key, value in [
            ("last_failure", max_last),
            ("best_expert", max_best),
            ("base", max_base),
            ("learned", max_learned),
        ]:
            if value is not None:
                rank_values[key].append(int(value))

        cases.append(
            {
                "goal_id": run["goal_id"],
                "theorem": goal.metadata.get("theorem", run["goal_id"]),
                "policy": policy,
                "proof_core_size": len(core),
                "missing_after_policy": sorted(missing_after_policy),
                "missing_from_candidates": sorted(missing_from_candidates),
                "failure_types": failures,
                "last_failure_type": last_failure,
                "max_last_failure_rank": max_last,
                "max_best_expert_rank": max_best,
                "max_base_rank": max_base,
                "max_learned_rank": max_learned,
                "baseline_solved": baseline_solved,
                "tags": tags,
            }
        )

    def stats(values: list[int]) -> dict[str, Any]:
        if not values:
            return {}
        return {
            "count": len(values),
            "median": float(statistics.median(values)),
            "min": min(values),
            "max": max(values),
            "top96": sum(1 for value in values if value <= 96),
            "top128": sum(1 for value in values if value <= 128),
            "top160": sum(1 for value in values if value <= 160),
        }

    tag_counts = Counter(tag for case in cases for tag in case["tags"])
    last_failure_counts = Counter(case["last_failure_type"] or "none" for case in cases)
    return {
        "policy": policy,
        "n_runs": len(policy_runs),
        "n_unsolved": len(cases),
        "tag_counts": dict(tag_counts),
        "last_failure_counts": dict(last_failure_counts),
        "rank_stats": {key: stats(values) for key, values in rank_values.items()},
        "cases": cases,
    }


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    lines = []
    lines.append("# Phase 3 Second-Stage Failure Taxonomy")
    lines.append("")
    lines.append(f"- Goals file: `{payload['inputs']['goals']}`")
    lines.append(f"- Trace result: `{payload['inputs']['trace_result']}`")
    lines.append("")
    for summary in payload["policy_summaries"]:
        lines.append(f"## `{summary['policy']}`")
        lines.append("")
        lines.append(f"- Runs: {summary['n_runs']}")
        lines.append(f"- Unsolved: {summary['n_unsolved']} ({pct(summary['n_unsolved'], summary['n_runs'])})")
        lines.append("")
        lines.append("### Tags")
        lines.append("")
        lines.append("| Tag | Count |")
        lines.append("|---|---:|")
        for tag, count in Counter(summary["tag_counts"]).most_common():
            lines.append(f"| `{tag}` | {count} |")
        lines.append("")
        lines.append("### Last Failure Type")
        lines.append("")
        lines.append("| Failure type | Count |")
        lines.append("|---|---:|")
        for failure_type, count in Counter(summary["last_failure_counts"]).most_common():
            lines.append(f"| `{failure_type}` | {count} |")
        lines.append("")
        lines.append("### Missing-Core Rank Stats")
        lines.append("")
        lines.append("| Rank source | Count | Median | Min | Max | Top96 | Top128 | Top160 |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for key, label in [
            ("last_failure", "last-failure expert"),
            ("best_expert", "best expert"),
            ("base", "base"),
            ("learned", "learned"),
        ]:
            stats = summary["rank_stats"].get(key, {})
            if not stats:
                continue
            lines.append(
                f"| `{label}` | {stats['count']} | {stats['median']:.1f} | {stats['min']} | {stats['max']} | "
                f"{stats['top96']} | {stats['top128']} | {stats['top160']} |"
            )
        lines.append("")
        lines.append("### Representative Cases")
        lines.append("")
        for case in summary["cases"][:20]:
            lines.append(
                f"- `{case['theorem']}`: tags={','.join(case['tags'])}; "
                f"last={case['last_failure_type']}; "
                f"ranks last/best/base/learned="
                f"{case['max_last_failure_rank']}/{case['max_best_expert_rank']}/"
                f"{case['max_base_rank']}/{case['max_learned_rank']}"
            )
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", type=Path, required=True)
    parser.add_argument("--trace-result", type=Path, required=True)
    parser.add_argument("--policies", nargs="+", required=True)
    parser.add_argument("--baseline-policy")
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()

    goals = load_goals_jsonl(args.goals)
    goals_by_id = {goal.goal_id: goal for goal in goals}
    trace = json.loads(args.trace_result.read_text(encoding="utf-8"))
    runs_by_key = {(run["goal_id"], run["policy"]): run for run in trace["runs"]}

    payload = {
        "inputs": {
            "goals": str(args.goals),
            "trace_result": str(args.trace_result),
            "baseline_policy": args.baseline_policy,
        },
        "policy_summaries": [
            inspect_policy(
                goals_by_id=goals_by_id,
                runs_by_key=runs_by_key,
                policy=policy,
                baseline_policy=args.baseline_policy,
            )
            for policy in args.policies
        ],
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(payload, args.out_md)
    print(args.out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
