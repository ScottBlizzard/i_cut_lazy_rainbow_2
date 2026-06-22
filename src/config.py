"""Configuration helpers for FAR-Hammer Phase 1 experiments.

The Phase 1 code is intentionally standard-library first. The local mock
experiment validates schema, controllers, and analysis before the server-side
Lean backend is wired in.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def outputs_dir() -> Path:
    out = project_root() / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    return out


@dataclass(frozen=True)
class Phase1Config:
    seed: int = 0
    n_goals: int = 500
    n_candidates: int = 160
    proof_core_size: int = 4
    first_k: int = 32
    retry_k: int = 32
    max_attempts: int = 3
    total_premise_budget: int = 96
    timeout_noise_threshold: int = 18
    timeout_broad_threshold: int = 5
    reconstruction_hostile_threshold: int = 3
    local_missing_rate: float = 0.25


DEFAULT_POLICIES = [
    "one_shot",
    "topk_expansion",
    "random_retry",
    "history_only",
    "rule_far",
]

