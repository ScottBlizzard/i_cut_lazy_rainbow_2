"""In-process trace-core prover for fast Mathlib Phase 1 experiments."""

from __future__ import annotations

import time

from failure_parser import parse_failure
from schema import FailureTrace, Goal, Premise, ProverResult


def choose_failure_type(missing_tags: set[str], selected_tags: list[str]) -> str:
    if "imported_core" in missing_tags:
        return "imported_premise_missing"
    if "bridge" in missing_tags:
        return "missing_bridge"
    if "type_compatible" in missing_tags:
        return "type_mismatch"
    if "rewrite" in missing_tags:
        return "rewrite_direction"
    if "typeclass" in missing_tags:
        return "typeclass_missing"
    if "lean_friendly" in missing_tags:
        return "reconstruction_failure"
    if selected_tags.count("broad") >= 8 or selected_tags.count("noise") >= 64:
        return "timeout"
    return "local_context_missing"


class TraceCoreProver:
    name = "trace_core_oracle_inprocess"

    def __init__(
        self,
        *,
        timeout_first: bool = False,
        timeout_noise_threshold: int = 64,
        timeout_broad_threshold: int = 8,
    ) -> None:
        self.timeout_first = timeout_first
        self.timeout_noise_threshold = timeout_noise_threshold
        self.timeout_broad_threshold = timeout_broad_threshold

    def _failure(
        self,
        *,
        goal: Goal,
        premises: list[Premise],
        missing: list[str],
        recovered: list[str],
        failure_type: str,
        elapsed: float,
        raw_extra: dict | None = None,
    ) -> ProverResult:
        selected = {p.name for p in premises}
        by_name = {p.name: p for p in goal.candidates}
        missing_tags = {
            tag
            for name in missing
            for tag in by_name.get(name, Premise(name=name, text=name, base_score=0.0)).tags
        }
        raw = {
            "missing_core": missing,
            "recovered_core": recovered,
            "missing_tags": sorted(missing_tags),
        }
        if raw_extra:
            raw.update(raw_extra)
        failure = parse_failure(
            f"missing {len(missing)} traced proof-core premise(s)",
            backend="trace_core_oracle",
            backend_status="fail",
            reconstruction_status="not_attempted",
            unsolved_goals=[goal.goal_state],
            raw=raw,
        )
        failure.failure_type = failure_type
        return ProverResult(
            success=False,
            verified=False,
            failure=failure,
            used_premises=sorted(selected),
            proof_core_recovered=recovered,
            time_s=elapsed,
            backend_status="trace_core_oracle",
            reconstruction_status="not_attempted",
        )

    def prove(self, goal: Goal, premises: list[Premise], *, timeout_s: float) -> ProverResult:
        start = time.perf_counter()
        selected = {p.name for p in premises}
        core = set(goal.proof_core)
        recovered = sorted(core & selected)
        missing = sorted(core - selected)
        elapsed = time.perf_counter() - start + 0.001 * len(premises)
        selected_tags = [tag for p in premises for tag in p.tags]

        if self.timeout_first and (
            selected_tags.count("broad") >= self.timeout_broad_threshold
            or selected_tags.count("noise") >= self.timeout_noise_threshold
        ):
            return self._failure(
                goal=goal,
                premises=premises,
                missing=missing,
                recovered=recovered,
                failure_type="timeout",
                elapsed=elapsed,
                raw_extra={
                    "timeout_first": True,
                    "selected_broad": selected_tags.count("broad"),
                    "selected_noise": selected_tags.count("noise"),
                    "timeout_broad_threshold": self.timeout_broad_threshold,
                    "timeout_noise_threshold": self.timeout_noise_threshold,
                },
            )

        if not missing:
            return ProverResult(
                success=True,
                verified=True,
                failure=None,
                used_premises=sorted(selected),
                proof_core_recovered=recovered,
                time_s=elapsed,
                backend_status="trace_core_oracle",
                reconstruction_status="core_recovered",
            )

        by_name = {p.name: p for p in goal.candidates}
        missing_tags = {tag for name in missing for tag in by_name.get(name, Premise(name=name, text=name, base_score=0.0)).tags}
        failure_type = choose_failure_type(missing_tags, selected_tags)
        return self._failure(
            goal=goal,
            premises=premises,
            missing=missing,
            recovered=recovered,
            failure_type=failure_type,
            elapsed=elapsed,
        )
