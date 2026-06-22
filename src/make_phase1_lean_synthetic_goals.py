"""Generate small synthetic Lean goals for external-prover smoke tests."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from data_io import write_goals_jsonl
from schema import Goal, Premise


def theorem_decl(name: str, proof: str) -> str:
    return f"theorem {name} (n : Nat) : n = n := by\n  {proof}"


def make_goals(n_goals: int, seed: int) -> list[Goal]:
    rng = random.Random(seed)
    goals: list[Goal] = []
    for i in range(n_goals):
        hard_case = rng.choice(["missing_bridge", "local", "noise"])
        core = [f"g{i}_core{j}" for j in range(4)]
        if hard_case == "local":
            core[-1] = f"g{i}_local_bridge"

        candidates: list[Premise] = []
        prev = None
        for j, name in enumerate(core):
            proof = "rfl" if prev is None else f"exact {prev} n"
            tags = ["core", "precise", "lean_friendly", "type_compatible"]
            if j == len(core) - 1:
                tags.append("bridge")
            if "local" in name:
                tags.extend(["local", "bridge"])
            if hard_case in {"missing_bridge", "local"} and j == len(core) - 1:
                score = rng.uniform(0.10, 0.30)
            else:
                score = rng.uniform(0.55, 0.95)
            candidates.append(Premise(name=name, text=theorem_decl(name, proof), base_score=score, tags=tags))
            prev = name

        for j in range(80):
            name = f"g{i}_noise{j}"
            tags: list[str] = ["noise"] if rng.random() < 0.35 else []
            if rng.random() < 0.10:
                tags.append("broad")
            score = rng.random() * 0.65
            if hard_case == "noise" and ("noise" in tags or "broad" in tags):
                score += 0.25
            candidates.append(
                Premise(
                    name=name,
                    text=theorem_decl(name, "rfl"),
                    base_score=min(score, 0.99),
                    tags=tags,
                )
            )

        goals.append(
            Goal(
                goal_id=f"lean_synth_{i:05d}",
                goal_state=f"theorem g{i}_target (n : Nat) : n = n",
                candidates=candidates,
                proof_core=core,
                local_premises=[p for p in core if "local" in p],
                metadata={
                    "hard_case": hard_case,
                    "imports": [],
                    "target_signature": f"theorem g{i}_target (n : Nat) : n = n",
                    "proof_script": f"exact {core[-1]} n",
                },
            )
        )
    return goals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-goals", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    write_goals_jsonl(make_goals(args.n_goals, args.seed), args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

