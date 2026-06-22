"""Summarize Phase 3 split-stability result JSON files."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def first_attempt_failed(run: dict[str, Any]) -> bool:
    attempts = run.get("attempts", [])
    return bool(attempts and not attempts[0].get("result", {}).get("verified"))


def policy_stats(runs: list[dict[str, Any]]) -> dict[str, float]:
    n = len(runs)
    solved = sum(1 for run in runs if run.get("solved"))
    first_failed = sum(1 for run in runs if first_attempt_failed(run))
    recovered = sum(1 for run in runs if run.get("first_failure_recovered"))
    avg_premises = sum(float(run.get("total_premises_tried", 0.0)) for run in runs) / max(n, 1)
    return {
        "n": n,
        "success": solved / max(n, 1),
        "ffr": recovered / max(first_failed, 1),
        "avg_premises": avg_premises,
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True, help="LABEL=PATH result JSON pairs")
    parser.add_argument("--policies", nargs="+", required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()

    split_rows: list[dict[str, Any]] = []
    by_policy_metric: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for item in args.inputs:
        label, path_text = item.split("=", 1)
        data = json.loads(Path(path_text).read_text(encoding="utf-8"))
        by_policy: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for run in data["runs"]:
            by_policy[run["policy"]].append(run)
        for policy in args.policies:
            stats = policy_stats(by_policy.get(policy, []))
            row = {"split": label, "policy": policy, **stats}
            split_rows.append(row)
            for metric in ("success", "ffr", "avg_premises"):
                by_policy_metric[policy][metric].append(float(stats[metric]))

    aggregate_rows = []
    for policy in args.policies:
        row = {"policy": policy}
        for metric in ("success", "ffr", "avg_premises"):
            values = by_policy_metric[policy][metric]
            row[f"{metric}_mean"] = statistics.mean(values) if values else 0.0
            row[f"{metric}_std"] = statistics.pstdev(values) if len(values) > 1 else 0.0
            row[f"{metric}_min"] = min(values) if values else 0.0
            row[f"{metric}_max"] = max(values) if values else 0.0
        aggregate_rows.append(row)

    payload = {
        "inputs": args.inputs,
        "policies": args.policies,
        "splits": split_rows,
        "aggregate": aggregate_rows,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Phase 3 Split-Stability Summary")
    lines.append("")
    lines.append("## Per-Split Results")
    lines.append("")
    lines.append("| Split | Policy | Success | FFR | Avg premises |")
    lines.append("|---|---|---:|---:|---:|")
    for row in split_rows:
        lines.append(
            f"| `{row['split']}` | `{row['policy']}` | {pct(row['success'])} | "
            f"{pct(row['ffr'])} | {row['avg_premises']:.1f} |"
        )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| Policy | Success mean | Success std | Success min-max | FFR mean | Avg premises mean |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in aggregate_rows:
        lines.append(
            f"| `{row['policy']}` | {pct(row['success_mean'])} | "
            f"{100 * row['success_std']:.1f} | "
            f"{pct(row['success_min'])}-{pct(row['success_max'])} | "
            f"{pct(row['ffr_mean'])} | {row['avg_premises_mean']:.1f} |"
        )
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
