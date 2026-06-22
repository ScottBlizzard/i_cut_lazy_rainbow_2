"""Analyze Phase 1 result JSON and emit a reviewer-facing markdown table."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from config import outputs_dir


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def analyze(data: dict) -> str:
    runs = data["runs"]
    by_policy: dict[str, list[dict]] = defaultdict(list)
    for run in runs:
        by_policy[run["policy"]].append(run)

    lines = []
    lines.append(f"# Phase 1 Analysis: {data['experiment_name']}")
    lines.append("")
    backend = data.get("config", {}).get("backend", "")
    if backend == "trace_core_oracle":
        lines.append("> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.")
    else:
        lines.append("> Synthetic mock results validate the pipeline only; they are not paper evidence.")
    lines.append("")
    lines.append("| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    for policy, rs in sorted(by_policy.items()):
        n = len(rs)
        solved = sum(1 for r in rs if r["solved"])
        first_failed = sum(1 for r in rs if r["attempts"] and not r["attempts"][0]["result"]["verified"])
        recovered = sum(1 for r in rs if r["first_failure_recovered"])
        attempts = sum(len(r["attempts"]) for r in rs) / n
        premises = sum(r["total_premises_tried"] for r in rs) / n
        time_s = sum(r["total_time_s"] for r in rs) / n

        fail_counts = Counter()
        for r in rs:
            for a in r["attempts"]:
                failure = a["result"]["failure"]
                if failure:
                    fail_counts[failure["failure_type"]] += 1
        total_attempts = sum(len(r["attempts"]) for r in rs)
        timeout_rate = fail_counts["timeout"] / total_attempts if total_attempts else 0.0
        recon_rate = fail_counts["reconstruction_failure"] / total_attempts if total_attempts else 0.0
        ffr = recovered / first_failed if first_failed else 0.0

        lines.append(
            f"| `{policy}` | {n} | {pct(solved / n)} | {pct(ffr)} | "
            f"{attempts:.2f} | {premises:.1f} | {time_s:.2f}s | {pct(timeout_rate)} | {pct(recon_rate)} |"
        )

    lines.append("")
    lines.append("## Failure Type Counts")
    lines.append("")
    for policy, rs in sorted(by_policy.items()):
        fail_counts = Counter()
        for r in rs:
            for a in r["attempts"]:
                failure = a["result"]["failure"]
                if failure:
                    fail_counts[failure["failure_type"]] += 1
        lines.append(f"- `{policy}`: {dict(fail_counts)}")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=outputs_dir() / "phase1_synthetic_smoke.json")
    parser.add_argument("--out", type=Path, default=outputs_dir() / "phase1_synthetic_smoke.md")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    report = analyze(data)
    args.out.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
