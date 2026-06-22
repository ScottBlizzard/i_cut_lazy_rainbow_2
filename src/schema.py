"""Shared JSON schema for Phase 1 FAR-Hammer experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Premise:
    name: str
    text: str
    base_score: float
    tags: list[str] = field(default_factory=list)
    features: dict[str, Any] = field(default_factory=dict)

    def has(self, tag: str) -> bool:
        return tag in self.tags


@dataclass
class Goal:
    goal_id: str
    goal_state: str
    candidates: list[Premise]
    proof_core: list[str]
    local_premises: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FailureTrace:
    failure_type: str
    backend: str
    message: str
    reconstruction_status: str = "not_attempted"
    unsolved_goals: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProverResult:
    success: bool
    verified: bool
    failure: FailureTrace | None
    used_premises: list[str]
    proof_core_recovered: list[str]
    time_s: float
    backend_status: str
    reconstruction_status: str


@dataclass
class AttemptRecord:
    attempt_id: int
    policy: str
    premise_names: list[str]
    result: ProverResult


@dataclass
class GoalRun:
    goal_id: str
    policy: str
    attempts: list[AttemptRecord]
    solved: bool
    first_failure_recovered: bool
    total_time_s: float
    total_premises_tried: int


@dataclass
class ExperimentResult:
    experiment_name: str
    config: dict[str, Any]
    runs: list[GoalRun]


def to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, list):
        return [to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    return obj


def premise_from_dict(d: dict[str, Any]) -> Premise:
    return Premise(
        name=d["name"],
        text=d.get("text", d["name"]),
        base_score=float(d.get("base_score", 0.0)),
        tags=list(d.get("tags", [])),
        features=dict(d.get("features", {})),
    )


def goal_from_dict(d: dict[str, Any]) -> Goal:
    return Goal(
        goal_id=d["goal_id"],
        goal_state=d["goal_state"],
        candidates=[premise_from_dict(p) for p in d.get("candidates", [])],
        proof_core=list(d.get("proof_core", [])),
        local_premises=list(d.get("local_premises", [])),
        metadata=dict(d.get("metadata", {})),
    )


def failure_from_dict(d: dict[str, Any] | None) -> FailureTrace | None:
    if d is None:
        return None
    return FailureTrace(
        failure_type=d.get("failure_type", "unknown"),
        backend=d.get("backend", "unknown"),
        message=d.get("message", ""),
        reconstruction_status=d.get("reconstruction_status", "not_attempted"),
        unsolved_goals=list(d.get("unsolved_goals", [])),
        raw=dict(d.get("raw", {})),
    )


def prover_result_from_dict(d: dict[str, Any]) -> ProverResult:
    return ProverResult(
        success=bool(d.get("success", False)),
        verified=bool(d.get("verified", False)),
        failure=failure_from_dict(d.get("failure")),
        used_premises=list(d.get("used_premises", [])),
        proof_core_recovered=list(d.get("proof_core_recovered", [])),
        time_s=float(d.get("time_s", 0.0)),
        backend_status=d.get("backend_status", "unknown"),
        reconstruction_status=d.get("reconstruction_status", "unknown"),
    )
