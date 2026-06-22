"""Synthetic prover used only for local Phase 1 pipeline validation.

This is not a scientific result. The rules encode expected Lean hammer failure
modes so that evaluation, logging, and controller logic can be tested before
the server-side Lean backend is connected.
"""

from __future__ import annotations

import random

from failure_parser import parse_failure
from schema import Goal, Premise, ProverResult


class MockProver:
    name = "mock_hammer"

    def __init__(
        self,
        *,
        timeout_noise_threshold: int = 18,
        timeout_broad_threshold: int = 5,
        reconstruction_hostile_threshold: int = 3,
        seed: int = 0,
    ) -> None:
        self.timeout_noise_threshold = timeout_noise_threshold
        self.timeout_broad_threshold = timeout_broad_threshold
        self.reconstruction_hostile_threshold = reconstruction_hostile_threshold
        self.rng = random.Random(seed)

    def prove(self, goal: Goal, premises: list[Premise], *, timeout_s: float) -> ProverResult:
        names = {p.name for p in premises}
        core = set(goal.proof_core)
        recovered = sorted(core & names)
        missing = sorted(core - names)

        noise_count = sum(1 for p in premises if p.has("noise"))
        broad_count = sum(1 for p in premises if p.has("broad"))
        recon_hostile_count = sum(1 for p in premises if p.has("reconstruction_hostile"))

        base_time = 0.05 + 0.003 * len(premises) + 0.006 * noise_count + 0.02 * broad_count

        if missing:
            missing_local = any(m in goal.local_premises for m in missing)
            failure_type = "local_context_missing" if missing_local else "missing_bridge"
            msg = (
                "local premise not found in environment"
                if missing_local
                else "no proof found; missing premise bridge"
            )
            return self._fail(goal, premises, recovered, base_time, failure_type, msg)

        if noise_count >= self.timeout_noise_threshold or broad_count >= self.timeout_broad_threshold:
            return self._fail(
                goal,
                premises,
                recovered,
                timeout_s,
                "timeout",
                "timeout: search explosion from broad/noisy premises",
                backend_status="timeout",
            )

        if recon_hostile_count >= self.reconstruction_hostile_threshold:
            return self._fail(
                goal,
                premises,
                recovered,
                base_time,
                "reconstruction_failure",
                "ATP proof found but Lean reconstruction failed",
                backend_status="atp_success",
                reconstruction_status="failed",
            )

        return ProverResult(
            success=True,
            verified=True,
            failure=None,
            used_premises=sorted(core),
            proof_core_recovered=recovered,
            time_s=min(base_time, timeout_s),
            backend_status="success",
            reconstruction_status="verified",
        )

    def _fail(
        self,
        goal: Goal,
        premises: list[Premise],
        recovered: list[str],
        time_s: float,
        failure_type: str,
        message: str,
        *,
        backend_status: str = "fail",
        reconstruction_status: str = "not_attempted",
    ) -> ProverResult:
        failure = parse_failure(
            message,
            backend=self.name,
            backend_status=backend_status,
            reconstruction_status=reconstruction_status,
            unsolved_goals=[goal.goal_state],
            raw={"forced_failure_type": failure_type},
        )
        if failure.failure_type == "unknown":
            failure.failure_type = failure_type
        return ProverResult(
            success=False,
            verified=False,
            failure=failure,
            used_premises=[],
            proof_core_recovered=recovered,
            time_s=time_s,
            backend_status=backend_status,
            reconstruction_status=reconstruction_status,
        )

