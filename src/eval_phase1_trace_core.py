"""Run Phase 1 evaluation with the in-process trace-core prover."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

from config import Phase1Config, outputs_dir
from data_io import load_goals_jsonl, write_experiment
from eval_phase1 import run_policy_on_goal
from provers.trace_core import TraceCoreProver
from schema import ExperimentResult


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=outputs_dir() / "phase1_trace_core.json")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--first-k", type=int, default=32)
    parser.add_argument("--retry-k", type=int, default=32)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--timeout-s", type=float, default=30.0)
    parser.add_argument("--timeout-first", action="store_true")
    parser.add_argument("--timeout-noise-threshold", type=int, default=64)
    parser.add_argument("--timeout-broad-threshold", type=int, default=8)
    parser.add_argument("--policies", nargs="+", required=True)
    args = parser.parse_args()

    cfg = Phase1Config(
        seed=args.seed,
        n_goals=0,
        first_k=args.first_k,
        retry_k=args.retry_k,
        max_attempts=args.max_attempts,
    )
    goals = load_goals_jsonl(args.goals)
    prover = TraceCoreProver(
        timeout_first=args.timeout_first,
        timeout_noise_threshold=args.timeout_noise_threshold,
        timeout_broad_threshold=args.timeout_broad_threshold,
    )

    runs = []
    for idx, goal in enumerate(goals):
        for policy_name in args.policies:
            runs.append(
                run_policy_on_goal(
                    goal,
                    policy_name=policy_name,
                    cfg=cfg,
                    timeout_s=args.timeout_s,
                    seed=args.seed + idx,
                    prover=prover,
                )
            )

    result = ExperimentResult(
        experiment_name="phase1_mathlib_trace_core",
        config=asdict(cfg)
        | {
            "policies": args.policies,
            "backend": "trace_core_oracle",
            "goals": str(args.goals),
            "timeout_s": args.timeout_s,
            "prover": "in_process",
            "timeout_first": args.timeout_first,
            "timeout_noise_threshold": args.timeout_noise_threshold,
            "timeout_broad_threshold": args.timeout_broad_threshold,
        },
        runs=runs,
    )
    write_experiment(result, args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
