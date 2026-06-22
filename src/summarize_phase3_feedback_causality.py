"""Summarize Phase 3 feedback-causality ablations across scored-goal splits."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TRUE_POLICY = "rule_far_learned_second_stage"


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}%"


def split_name(path: Path) -> str:
    stem = path.stem
    return stem.removeprefix("phase3_feedback_causality_").removesuffix("_500")


def policy_stats(runs: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(runs)
    solved = sum(1 for run in runs if run["solved"])
    first_failed = sum(
        1
        for run in runs
        if run["attempts"] and not run["attempts"][0]["result"]["verified"]
    )
    recovered = sum(1 for run in runs if run["first_failure_recovered"])
    attempts = sum(len(run["attempts"]) for run in runs) / n if n else 0.0
    premises = sum(run["total_premises_tried"] for run in runs) / n if n else 0.0
    time_s = sum(run["total_time_s"] for run in runs) / n if n else 0.0
    return {
        "n": n,
        "success": solved / n if n else 0.0,
        "first_failure_recovery": recovered / first_failed if first_failed else 0.0,
        "avg_attempts": attempts,
        "avg_premises": premises,
        "avg_time_s": time_s,
    }


def first_failure_counts(runs: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for run in runs:
        if not run["attempts"]:
            counts["no_attempt"] += 1
            continue
        result = run["attempts"][0]["result"]
        if result["verified"]:
            counts["initial_success"] += 1
            continue
        failure = result.get("failure") or {}
        counts[str(failure.get("failure_type", "unknown"))] += 1
    return counts


def load_grouped(path: Path) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in data["runs"]:
        grouped[run["policy"]].append(run)
    return dict(grouped), data.get("config", {})


def render(inputs: list[Path]) -> str:
    aggregate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    split_tables: list[tuple[str, dict[str, dict[str, Any]], Counter[str]]] = []

    for path in inputs:
        grouped, _ = load_grouped(path)
        for policy, runs in grouped.items():
            aggregate[policy].extend(runs)
        stats = {policy: policy_stats(runs) for policy, runs in sorted(grouped.items())}
        first_failure_policy = TRUE_POLICY if TRUE_POLICY in grouped else next(iter(grouped))
        split_tables.append((split_name(path), stats, first_failure_counts(grouped[first_failure_policy])))

    aggregate_stats = {policy: policy_stats(runs) for policy, runs in sorted(aggregate.items())}
    true_success = aggregate_stats.get(TRUE_POLICY, {}).get("success")
    control_successes = {
        policy: stats["success"]
        for policy, stats in aggregate_stats.items()
        if policy != TRUE_POLICY
    }
    best_control_policy = max(control_successes, key=control_successes.get) if control_successes else None
    best_control_success = control_successes[best_control_policy] if best_control_policy else None

    lines: list[str] = []
    lines.append("# Phase 3 Feedback-Causality Gate 0")
    lines.append("")
    lines.append(
        "This ablation tests whether the observed failure type causally affects the second-stage controller. "
        "All variants share the same first attempt and scored candidates; controls ignore or corrupt the observed failure type."
    )
    lines.append("")

    lines.append("## Aggregate")
    lines.append("")
    lines.append("| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for policy, stats in sorted(aggregate_stats.items()):
        lines.append(
            f"| `{policy}` | {stats['n']} | {pct(stats['success'])} | "
            f"{pct(stats['first_failure_recovery'])} | {stats['avg_attempts']:.2f} | "
            f"{stats['avg_premises']:.1f} | {stats['avg_time_s']:.2f}s |"
        )

    lines.append("")
    lines.append("## Gate Readout")
    lines.append("")
    if true_success is None or best_control_success is None:
        lines.append("- Verdict: inconclusive, missing true policy or controls.")
    else:
        delta_pp = 100.0 * (true_success - best_control_success)
        if delta_pp >= 1.0:
            verdict = "pass"
        elif delta_pp <= 0.2:
            verdict = "fail"
        else:
            verdict = "weak"
        lines.append(f"- Best control: `{best_control_policy}` at {pct(best_control_success)}.")
        lines.append(f"- True failure-conditioned policy delta over best control: {delta_pp:+.1f} pp.")
        lines.append(f"- Verdict: {verdict}.")
        if verdict != "pass":
            lines.append(
                "- Interpretation: the current trace-core second-stage evidence is not enough for a main-track oral claim that failure transcript content is the core causal signal."
            )

    lines.append("")
    lines.append("## Split Results")
    for name, stats_by_policy, failures in split_tables:
        lines.append("")
        lines.append(f"### {name}")
        lines.append("")
        lines.append("| Policy | Goals | Verified success | First-failure recovery |")
        lines.append("|---|---:|---:|---:|")
        for policy, stats in sorted(stats_by_policy.items()):
            lines.append(
                f"| `{policy}` | {stats['n']} | {pct(stats['success'])} | "
                f"{pct(stats['first_failure_recovery'])} |"
            )
        lines.append("")
        lines.append("First-attempt outcomes for the true-policy run:")
        for key, count in failures.most_common():
            lines.append(f"- `{key}`: {count}")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    report = render(args.inputs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
