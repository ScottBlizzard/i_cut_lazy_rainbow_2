"""Build Phase 3 global/imported hard-negative goal files.

The input Phase 1 goals contain same-file candidate pools. This transform keeps
the traced proof core unchanged, caps same-file candidates, and fills the pool
with lexically similar candidates from other Mathlib files.
"""

from __future__ import annotations

import argparse
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from data_io import load_goals_jsonl, write_goals_jsonl
from feature_extraction import build_candidate_features, goal_query_tokens, lean_name_tokens
from schema import Goal, Premise


STOPWORDS = {
    "theorem",
    "lemma",
    "def",
    "abbrev",
    "instance",
    "class",
    "structure",
    "inductive",
    "type",
    "prop",
    "sort",
    "true",
    "false",
    "by",
    "let",
    "fun",
    "forall",
    "exists",
    "intro",
    "simp",
    "rw",
    "exact",
}


@dataclass(frozen=True)
class PoolEntry:
    premise: Premise
    source_file: str
    name_tokens: frozenset[str]
    all_tokens: frozenset[str]


def useful_tokens(tokens: set[str] | list[str]) -> set[str]:
    return {tok for tok in tokens if tok not in STOPWORDS and len(tok) > 1}


def build_pool(goals: list[Goal]) -> tuple[list[PoolEntry], dict[str, list[int]]]:
    pool: list[PoolEntry] = []
    seen: set[str] = set()
    for goal in goals:
        source_file = str(goal.metadata.get("file_path", ""))
        for premise in goal.candidates:
            if premise.name in seen:
                continue
            seen.add(premise.name)
            name_tokens = useful_tokens(lean_name_tokens(premise.name))
            all_tokens = useful_tokens(lean_name_tokens(f"{premise.name} {premise.text}"))
            pool.append(
                PoolEntry(
                    premise=premise,
                    source_file=source_file,
                    name_tokens=frozenset(name_tokens),
                    all_tokens=frozenset(all_tokens),
                )
            )

    token_index: dict[str, list[int]] = defaultdict(list)
    for idx, entry in enumerate(pool):
        for tok in entry.all_tokens:
            token_index[tok].append(idx)
    return pool, token_index


def global_base_score(goal: Goal, premise: Premise, *, same_file: bool, rng: random.Random) -> float:
    theorem_name = str(goal.metadata.get("theorem", goal.goal_id))
    features = build_candidate_features(
        theorem_name=theorem_name,
        goal_state=goal.goal_state,
        premise_name=premise.name,
        premise_text=premise.text,
        same_file=same_file,
    )
    score = 0.12
    score += 0.075 * min(int(features.get("name_token_overlap", 0)), 8)
    score += 0.095 * min(int(features.get("leaf_token_overlap", 0)), 6)
    score += 0.012 * min(int(features.get("statement_token_overlap", 0)), 28)
    score += 0.020 * min(int(features.get("namespace_prefix_len", 0)), 4)
    if same_file:
        score += 0.055
    if bool(features.get("is_def_like", False)):
        score += 0.025
    if bool(features.get("has_simp_attr", False)):
        score += 0.015
    score -= 0.000025 * min(int(features.get("text_length", 0)), 2400)
    score += rng.uniform(0.0, 0.10)
    return max(0.0, min(1.0, score))


def imported_tags(rng: random.Random) -> list[str]:
    tags = ["imported", "noise"]
    if rng.random() < 0.22:
        tags.append("broad")
    if rng.random() < 0.10:
        tags.append("reconstruction_hostile")
    if rng.random() < 0.10:
        tags.append("type_compatible")
    if rng.random() < 0.06:
        tags.append("bridge")
    return tags


def clone_candidate(
    goal: Goal,
    premise: Premise,
    *,
    same_file: bool,
    tags: list[str],
    rng: random.Random,
) -> Premise:
    theorem_name = str(goal.metadata.get("theorem", goal.goal_id))
    features = build_candidate_features(
        theorem_name=theorem_name,
        goal_state=goal.goal_state,
        premise_name=premise.name,
        premise_text=premise.text,
        same_file=same_file,
    )
    return Premise(
        name=premise.name,
        text=premise.text,
        base_score=global_base_score(goal, premise, same_file=same_file, rng=rng),
        tags=tags,
        features=features,
    )


def hard_negative_score(query: set[str], entry: PoolEntry, rng: random.Random) -> float:
    name_overlap = len(query & entry.name_tokens)
    text_overlap = len(query & entry.all_tokens)
    return 2.0 * name_overlap + 0.18 * text_overlap + 0.05 * entry.premise.base_score + rng.random() * 1e-4


def imported_hard_negatives(
    goal: Goal,
    *,
    pool: list[PoolEntry],
    token_index: dict[str, list[int]],
    existing_names: set[str],
    max_imported: int,
    rng: random.Random,
) -> list[PoolEntry]:
    source_file = str(goal.metadata.get("file_path", ""))
    query = useful_tokens(goal_query_tokens(goal))
    candidate_ids: set[int] = set()
    for tok in query:
        candidate_ids.update(token_index.get(tok, []))

    if len(candidate_ids) < max_imported * 4:
        sample_size = min(len(pool), max_imported * 10)
        candidate_ids.update(rng.sample(range(len(pool)), sample_size))

    filtered = [
        pool[idx]
        for idx in candidate_ids
        if pool[idx].source_file != source_file and pool[idx].premise.name not in existing_names
    ]
    filtered.sort(key=lambda entry: hard_negative_score(query, entry, rng), reverse=True)
    return filtered[:max_imported]


def cap_with_core(candidates: list[Premise], proof_core: set[str], max_candidates: int) -> list[Premise]:
    ranked = sorted(candidates, key=lambda p: p.base_score, reverse=True)
    selected = ranked[:max_candidates]
    selected_names = {p.name for p in selected}
    missing_core = [p for p in ranked if p.name in proof_core and p.name not in selected_names]
    for core_premise in missing_core:
        for idx in range(len(selected) - 1, -1, -1):
            if selected[idx].name not in proof_core:
                selected_names.remove(selected[idx].name)
                selected[idx] = core_premise
                selected_names.add(core_premise.name)
                break
    return sorted(selected, key=lambda p: p.base_score, reverse=True)


def transform_goals(
    goals: list[Goal],
    *,
    max_candidates: int,
    max_same_file: int,
    max_imported: int,
    seed: int,
) -> list[Goal]:
    pool, token_index = build_pool(goals)
    transformed: list[Goal] = []
    for idx, goal in enumerate(goals):
        rng = random.Random(f"{seed}:{goal.goal_id}")
        proof_core = set(goal.proof_core)
        same_file_ranked = sorted(goal.candidates, key=lambda p: p.base_score, reverse=True)
        same_file_kept = same_file_ranked[:max_same_file]
        kept_names = {p.name for p in same_file_kept}
        for premise in same_file_ranked:
            if premise.name in proof_core and premise.name not in kept_names:
                same_file_kept.append(premise)
                kept_names.add(premise.name)

        new_candidates = [
            clone_candidate(
                goal,
                premise,
                same_file=True,
                tags=list(dict.fromkeys([*premise.tags, "same_file"])),
                rng=rng,
            )
            for premise in same_file_kept
        ]
        existing_names = {p.name for p in new_candidates}
        imported = imported_hard_negatives(
            goal,
            pool=pool,
            token_index=token_index,
            existing_names=existing_names | proof_core,
            max_imported=max_imported,
            rng=rng,
        )
        for entry in imported:
            new_candidates.append(
                clone_candidate(
                    goal,
                    entry.premise,
                    same_file=False,
                    tags=imported_tags(rng),
                    rng=rng,
                )
            )

        capped = cap_with_core(new_candidates, proof_core, max_candidates)
        metadata = dict(goal.metadata)
        metadata.update(
            {
                "source": "phase3_global_imported_from_" + str(goal.metadata.get("source", "unknown")),
                "candidate_scope": "same_file_plus_imported_hard_negatives",
                "phase3_original_candidates": len(goal.candidates),
                "phase3_same_file_candidates": sum(1 for p in capped if "same_file" in p.tags),
                "phase3_imported_candidates": sum(1 for p in capped if "imported" in p.tags),
                "phase3_max_candidates": max_candidates,
                "phase3_seed": seed,
            }
        )
        transformed.append(
            Goal(
                goal_id=goal.goal_id,
                goal_state=goal.goal_state,
                candidates=capped,
                proof_core=goal.proof_core,
                local_premises=goal.local_premises,
                metadata=metadata,
            )
        )
        if (idx + 1) % 250 == 0:
            print(f"transformed {idx + 1}/{len(goals)} goals")
    return transformed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--limit-goals", type=int, default=None)
    parser.add_argument("--max-candidates", type=int, default=256)
    parser.add_argument("--max-same-file", type=int, default=96)
    parser.add_argument("--max-imported", type=int, default=192)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    goals = load_goals_jsonl(args.input)
    if args.limit_goals is not None:
        goals = goals[: args.limit_goals]
    transformed = transform_goals(
        goals,
        max_candidates=args.max_candidates,
        max_same_file=args.max_same_file,
        max_imported=args.max_imported,
        seed=args.seed,
    )
    write_goals_jsonl(transformed, args.out)
    avg_imported = sum(int(g.metadata["phase3_imported_candidates"]) for g in transformed) / max(len(transformed), 1)
    avg_same_file = sum(int(g.metadata["phase3_same_file_candidates"]) for g in transformed) / max(len(transformed), 1)
    print(
        f"wrote {len(transformed)} goals to {args.out}; "
        f"avg same-file={avg_same_file:.1f}, avg imported={avg_imported:.1f}"
    )


if __name__ == "__main__":
    main()
