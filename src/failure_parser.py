"""Failure taxonomy parser.

The parser is deliberately conservative. It maps backend status and message
text to a coarse failure type that the Phase 1 controller can act on. Server
experiments should keep the raw message so parser errors can be audited.
"""

from __future__ import annotations

from dataclasses import dataclass

from schema import FailureTrace


FAILURE_TYPES = [
    "success",
    "missing_bridge",
    "local_context_missing",
    "timeout",
    "reconstruction_failure",
    "type_mismatch",
    "rewrite_direction",
    "typeclass_missing",
    "history_repetition",
    "unknown",
]


@dataclass(frozen=True)
class FailurePattern:
    failure_type: str
    keywords: tuple[str, ...]


PATTERNS = [
    FailurePattern("timeout", ("timeout", "time limit", "resource exhausted", "search explosion")),
    FailurePattern("reconstruction_failure", ("reconstruction failed", "lean reconstruction", "kernel rejected")),
    FailurePattern("type_mismatch", ("type mismatch", "failed to synthesize", "application type mismatch")),
    FailurePattern("typeclass_missing", ("failed to synthesize", "instance", "typeclass", "class instance")),
    FailurePattern("rewrite_direction", ("rewrite", "rw failed", "simp made no progress", "simp failed")),
    FailurePattern("local_context_missing", ("unknown identifier", "local", "current file", "not found in environment")),
    FailurePattern("missing_bridge", ("unsolved goals", "no proof found", "saturation failed", "missing premise")),
]


def parse_failure(
    message: str,
    *,
    backend: str = "unknown",
    backend_status: str = "fail",
    reconstruction_status: str = "not_attempted",
    unsolved_goals: list[str] | None = None,
    raw: dict | None = None,
) -> FailureTrace:
    text = f"{backend_status}\n{reconstruction_status}\n{message}".lower()

    if backend_status.lower() in {"success", "verified"}:
        failure_type = "success"
    elif reconstruction_status.lower() in {"failed", "reconstruction_failed", "kernel_rejected"}:
        failure_type = "reconstruction_failure"
    else:
        failure_type = "unknown"
        for pattern in PATTERNS:
            if any(k in text for k in pattern.keywords):
                failure_type = pattern.failure_type
                break

    return FailureTrace(
        failure_type=failure_type,
        backend=backend,
        message=message,
        reconstruction_status=reconstruction_status,
        unsolved_goals=unsolved_goals or [],
        raw=raw or {},
    )

