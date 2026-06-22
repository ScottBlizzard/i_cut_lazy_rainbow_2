"""Run Phase 1 evaluation on JSONL goals using an external Lean/prover command."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

from config import DEFAULT_POLICIES, Phase1Config, outputs_dir
from data_io import load_goals_jsonl, write_experiment
from eval_phase1 import run_policy_on_goal
from provers.external import ExternalCommandProver
from schema import ExperimentResult


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", type=Path, required=True, help="JSONL goals with candidates")
    parser.add_argument("--prover-command", required=True, help="Command implementing external prover contract")
    parser.add_argument("--out", type=Path, default=outputs_dir() / "phase1_real.json")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--first-k", type=int, default=32)
    parser.add_argument("--retry-k", type=int, default=32)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--timeout-s", type=float, default=10.0)
    parser.add_argument("--policies", nargs="*", default=DEFAULT_POLICIES)
    args = parser.parse_args()

    cfg = Phase1Config(
        seed=args.seed,
        n_goals=0,
        first_k=args.first_k,
        retry_k=args.retry_k,
        max_attempts=args.max_attempts,
    )
    goals = load_goals_jsonl(args.goals)
    prover = ExternalCommandProver(args.prover_command)
    backend = "trace_core_oracle" if "trace_core_attempt" in args.prover_command else "external"

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
        experiment_name="phase1_mathlib_trace_core" if backend == "trace_core_oracle" else "phase1_real_fixed_budget",
        config=asdict(cfg)
        | {
            "policies": args.policies,
            "backend": backend,
            "goals": str(args.goals),
            "timeout_s": args.timeout_s,
        },
        runs=runs,
    )
    write_experiment(result, args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
