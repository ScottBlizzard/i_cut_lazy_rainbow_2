"""Run Phase 1 fixed-budget evaluation.

Default mode is a local synthetic smoke test. It validates the experiment
plumbing before server-side Lean backends are connected.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from config import DEFAULT_POLICIES, Phase1Config, outputs_dir
from far_controller import PolicyState, make_policy
from provers.mock import MockProver
from provers.base import BaseProver
from schema import AttemptRecord, ExperimentResult, Goal, GoalRun, to_jsonable
from synthetic_data import make_synthetic_goals


def run_policy_on_goal(
    goal: Goal,
    *,
    policy_name: str,
    cfg: Phase1Config,
    timeout_s: float,
    seed: int,
    prover: BaseProver | None = None,
) -> GoalRun:
    policy = make_policy(policy_name, seed=seed)
    if prover is None:
        prover = MockProver(
            timeout_noise_threshold=cfg.timeout_noise_threshold,
            timeout_broad_threshold=cfg.timeout_broad_threshold,
            reconstruction_hostile_threshold=cfg.reconstruction_hostile_threshold,
            seed=seed,
        )

    state = PolicyState(tried=set())
    attempts: list[AttemptRecord] = []
    total_time = 0.0
    solved = False
    first_failed = False

    for attempt_id in range(cfg.max_attempts):
        state.attempt_id = attempt_id
        k = cfg.first_k if attempt_id == 0 else cfg.retry_k
        if len(state.tried) >= cfg.total_premise_budget:
            break
        premises = policy.select(goal, k, state)
        if not premises:
            break
        # Enforce a cumulative unique-premise budget across retries. Policies
        # may keep previous premises in the current call, but they cannot keep
        # introducing fresh premises after the total budget is exhausted.
        remaining_new = cfg.total_premise_budget - len(state.tried)
        budgeted: list = []
        seen_in_call: set[str] = set()
        for premise in premises:
            if premise.name in seen_in_call:
                continue
            seen_in_call.add(premise.name)
            if premise.name in state.tried:
                budgeted.append(premise)
                continue
            if remaining_new <= 0:
                continue
            budgeted.append(premise)
            remaining_new -= 1
        premises = budgeted[: cfg.total_premise_budget]
        if not premises:
            break

        result = prover.prove(goal, premises, timeout_s=timeout_s)
        attempts.append(
            AttemptRecord(
                attempt_id=attempt_id,
                policy=policy_name,
                premise_names=[p.name for p in premises],
                result=result,
            )
        )
        total_time += result.time_s
        state.tried.update(p.name for p in premises)
        state.last_failure = result.failure

        if result.verified:
            solved = True
            break
        if attempt_id == 0:
            first_failed = True

    return GoalRun(
        goal_id=goal.goal_id,
        policy=policy_name,
        attempts=attempts,
        solved=solved,
        first_failure_recovered=first_failed and solved,
        total_time_s=total_time,
        total_premises_tried=len(state.tried),
    )


def run_experiment(goals: Iterable[Goal], cfg: Phase1Config, policies: list[str]) -> ExperimentResult:
    runs: list[GoalRun] = []
    for idx, goal in enumerate(goals):
        for policy_name in policies:
            runs.append(
                run_policy_on_goal(
                    goal,
                    policy_name=policy_name,
                    cfg=cfg,
                    timeout_s=10.0,
                    seed=cfg.seed + idx,
                )
            )
    return ExperimentResult(
        experiment_name="phase1_synthetic_smoke",
        config=asdict(cfg) | {"policies": policies, "backend": "mock"},
        runs=runs,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-goals", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--first-k", type=int, default=32)
    parser.add_argument("--retry-k", type=int, default=32)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--policies", nargs="*", default=DEFAULT_POLICIES)
    args = parser.parse_args()

    cfg = Phase1Config(
        seed=args.seed,
        n_goals=args.n_goals,
        first_k=args.first_k,
        retry_k=args.retry_k,
        max_attempts=args.max_attempts,
    )
    goals = make_synthetic_goals(
        n_goals=cfg.n_goals,
        n_candidates=cfg.n_candidates,
        proof_core_size=cfg.proof_core_size,
        local_missing_rate=cfg.local_missing_rate,
        seed=cfg.seed,
    )
    result = run_experiment(goals, cfg, list(args.policies))

    out = args.out or outputs_dir() / "phase1_synthetic_smoke.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(to_jsonable(result), indent=2), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
