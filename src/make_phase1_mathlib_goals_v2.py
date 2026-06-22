"""Create Phase 1 real-goal JSONL from a LeanDojo-v2 traced mathlib repo."""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any

from data_io import write_goals_jsonl
from feature_extraction import build_candidate_features
from schema import Goal, Premise


def pos_tuple(pos: Any) -> tuple[int, int]:
    return (int(pos.line_nb), int(pos.column_nb))


def collect_proof_core(thm: Any) -> list[str]:
    names: set[str] = set(thm.get_premise_full_names())
    for tac in thm.get_traced_tactics(atomic_only=True):
        try:
            _, provenances = tac.get_annotated_tactic()
            names.update(p["full_name"] for p in provenances if p.get("full_name"))
        except Exception:
            continue
    return sorted(names)


def file_premises(tf: Any) -> list[dict[str, Any]]:
    premises = []
    seen: set[str] = set()
    for p in tf.get_premise_definitions():
        name = p.get("full_name")
        code = p.get("code")
        if not name or not code or name in seen:
            continue
        seen.add(name)
        premises.append(p)
    return premises


def premise_tags(name: str, *, is_core: bool, rng: random.Random) -> list[str]:
    tags = ["same_file"]
    if is_core:
        tags.append("lean_friendly")
        bucket = sum(ord(ch) for ch in name) % 4
        tags.append(["bridge", "type_compatible", "rewrite", "typeclass"][bucket])
    else:
        tags.append("noise")
        if rng.random() < 0.18:
            tags.append("broad")
        if rng.random() < 0.12:
            tags.append("reconstruction_hostile")
        # Decoy compatibility tags keep the failure-aware signal imperfect.
        if rng.random() < 0.10:
            tags.append("type_compatible")
        if rng.random() < 0.06:
            tags.append("bridge")
    return tags


def retrieval_score(*, is_core: bool, tags: list[str], rng: random.Random) -> float:
    score = 0.20 + 0.65 * rng.betavariate(2.0, 2.6)
    if is_core:
        score += rng.uniform(0.00, 0.12)
    if "broad" in tags:
        score += rng.uniform(0.02, 0.10)
    if "reconstruction_hostile" in tags:
        score += rng.uniform(0.00, 0.08)
    return max(0.0, min(1.0, score))


def tactic_script(thm: Any) -> list[str]:
    tactics = []
    for tac in thm.get_traced_tactics(atomic_only=True):
        tactic = getattr(tac, "tactic", "")
        tactic = tactic() if callable(tactic) else tactic
        tactic = str(tactic).strip()
        if tactic:
            tactics.append(tactic)
    return tactics


def is_private_theorem(thm: Any) -> bool:
    value = thm.is_private
    value = value() if callable(value) else value
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def make_goals(
    traced: Any,
    *,
    n_goals: int,
    seed: int,
    max_candidates: int,
    min_candidates: int,
) -> list[Goal]:
    rng = random.Random(seed)
    candidate_theorems = [
        thm
        for thm in traced.get_traced_theorems()
        if not is_private_theorem(thm) and thm.has_tactic_proof()
    ]
    rng.shuffle(candidate_theorems)
    goals: list[Goal] = []
    premise_cache: dict[str, list[dict[str, Any]]] = {}

    for thm in candidate_theorems:
        proof_core = collect_proof_core(thm)
        if not proof_core:
            continue
        tf = thm.traced_file
        file_key = str(tf.path)
        if file_key not in premise_cache:
            premise_cache[file_key] = file_premises(tf)
        raw_candidates = premise_cache[file_key]
        if not raw_candidates:
            continue

        by_name = {p["full_name"]: p for p in raw_candidates}
        matched_core = [name for name in proof_core if name in by_name]
        if not matched_core or len(matched_core) > max_candidates:
            continue

        selected = [by_name[name] for name in matched_core]
        noise_pool = [p for p in raw_candidates if p["full_name"] not in set(matched_core)]
        rng.shuffle(noise_pool)
        selected.extend(noise_pool[: max(0, max_candidates - len(selected))])
        if len(selected) < min_candidates:
            continue

        candidates: list[Premise] = []
        core_names = set(matched_core)
        for p in selected[:max_candidates]:
            name = p["full_name"]
            tags = premise_tags(name, is_core=name in core_names, rng=rng)
            score = retrieval_score(is_core=name in core_names, tags=tags, rng=rng)
            features = build_candidate_features(
                theorem_name=thm.theorem.full_name,
                goal_state=thm.get_theorem_statement().rstrip(),
                premise_name=name,
                premise_text=p["code"],
                same_file=True,
            )
            candidates.append(
                Premise(name=name, text=p["code"], base_score=score, tags=tags, features=features)
            )
        candidates.sort(key=lambda p: p.base_score, reverse=True)

        statement = thm.get_theorem_statement().rstrip()
        goals.append(
            Goal(
                goal_id=f"mathlib4::{thm.theorem.full_name}",
                goal_state=statement,
                candidates=candidates,
                proof_core=matched_core,
                local_premises=[],
                metadata={
                    "repo_url": thm.repo.url,
                    "commit": thm.repo.commit,
                    "file_path": str(thm.file_path),
                    "theorem": thm.theorem.full_name,
                    "start": pos_tuple(thm.start),
                    "end": pos_tuple(thm.end),
                    "source": "leandojo_v2_trace",
                    "tactic_script": tactic_script(thm),
                    "evaluator": "trace_core_recovery",
                },
            )
        )
        if len(goals) >= n_goals:
            break

    return goals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--n-goals", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-candidates", type=int, default=256)
    parser.add_argument("--min-candidates", type=int, default=8)
    args = parser.parse_args()

    from lean_dojo_v2.lean_dojo.data_extraction.traced_data import TracedRepo

    traced = TracedRepo.load_from_disk(args.trace_root, build_deps=False)
    goals = make_goals(
        traced,
        n_goals=args.n_goals,
        seed=args.seed,
        max_candidates=args.max_candidates,
        min_candidates=args.min_candidates,
    )
    write_goals_jsonl(goals, args.out)
    print(f"wrote {len(goals)} goals to {args.out}")


if __name__ == "__main__":
    main()
