"""Synthetic Phase 1 data for local pipeline validation."""

from __future__ import annotations

import random

from schema import Goal, Premise


def make_synthetic_goals(
    *,
    n_goals: int,
    n_candidates: int,
    proof_core_size: int,
    local_missing_rate: float,
    seed: int,
) -> list[Goal]:
    rng = random.Random(seed)
    goals: list[Goal] = []

    for i in range(n_goals):
        hard_case = rng.choice(["missing_bridge", "timeout", "reconstruction", "local"])
        local_required = hard_case == "local" or rng.random() < local_missing_rate
        candidates: list[Premise] = []

        core_names = [f"g{i}.core{j}" for j in range(proof_core_size)]
        if local_required:
            core_names[-1] = f"g{i}.local_bridge"

        local_premises = [p for p in core_names if "local" in p]

        for j, name in enumerate(core_names):
            tags = ["core", "precise", "type_compatible", "lean_friendly"]
            if j == proof_core_size - 1:
                tags.append("bridge")
            if name in local_premises:
                tags.extend(["local", "bridge"])

            # Make one core premise easy to miss in each hard case.
            if hard_case in {"missing_bridge", "local"} and j == proof_core_size - 1:
                base_score = rng.uniform(0.15, 0.35)
            else:
                base_score = rng.uniform(0.55, 0.95)
            candidates.append(Premise(name=name, text=name, base_score=base_score, tags=tags))

        for j in range(n_candidates - proof_core_size):
            name = f"g{i}.cand{j}"
            tags: list[str] = []
            score = rng.random() * 0.65

            if rng.random() < 0.20:
                tags.append("noise")
                score += 0.20 if hard_case == "timeout" else 0.05
            if rng.random() < 0.08:
                tags.append("broad")
                score += 0.20 if hard_case == "timeout" else 0.05
            if rng.random() < 0.08:
                tags.append("reconstruction_hostile")
                score += 0.20 if hard_case == "reconstruction" else 0.02
            if rng.random() < 0.10:
                tags.append("bridge")
            if rng.random() < 0.10:
                tags.append("type_compatible")
            if rng.random() < 0.08:
                tags.append("rewrite")
            if rng.random() < 0.05:
                tags.append("typeclass")
            if rng.random() < 0.08:
                tags.append("lean_friendly")

            candidates.append(
                Premise(
                    name=name,
                    text=f"candidate theorem {j} for goal {i}",
                    base_score=min(score, 0.99),
                    tags=tags,
                )
            )

        goals.append(
            Goal(
                goal_id=f"synthetic_{i:05d}",
                goal_state=f"synthetic goal {i} [{hard_case}]",
                candidates=candidates,
                proof_core=core_names,
                local_premises=local_premises,
                metadata={"hard_case": hard_case},
            )
        )

    return goals

