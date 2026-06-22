"""Generate Phase 3 Mathlib goals with real same-file and imported proof cores."""

from __future__ import annotations

import argparse
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

from data_io import write_goals_jsonl
from feature_extraction import goal_query_tokens, lean_name_tokens
from make_phase1_mathlib_goals_v2 import (
    collect_proof_core,
    is_private_theorem,
    pos_tuple,
    premise_tags,
    tactic_script,
)
from make_phase3_global_candidates import (
    PoolEntry,
    cap_with_core,
    clone_candidate,
    hard_negative_score,
    imported_hard_negatives,
    imported_tags,
    useful_tokens,
)
from schema import Goal, Premise


def traced_files(traced: object) -> list[object]:
    files = getattr(traced, "traced_files", None)
    if files is not None:
        return list(files)
    getter = getattr(traced, "get_traced_files", None)
    if getter is not None:
        return list(getter())
    raise AttributeError("TracedRepo exposes neither traced_files nor get_traced_files()")


def theorem_file_path(thm: object) -> str:
    return str(getattr(thm, "file_path", getattr(thm.traced_file, "path", "")))


def core_tags(name: str, *, same_file: bool) -> list[str]:
    bucket = sum(ord(ch) for ch in name) % 4
    tags = ["same_file" if same_file else "imported", "lean_friendly"]
    tags.append(["bridge", "type_compatible", "rewrite", "typeclass"][bucket])
    if not same_file:
        tags.append("imported_core")
    return tags


def build_global_pool(traced: object) -> tuple[list[PoolEntry], dict[str, PoolEntry], dict[str, list[int]], dict[str, list[PoolEntry]]]:
    pool: list[PoolEntry] = []
    by_name: dict[str, PoolEntry] = {}
    by_file: dict[str, list[PoolEntry]] = defaultdict(list)

    for tf in traced_files(traced):
        source_file = str(getattr(tf, "path", ""))
        seen_in_file: set[str] = set()
        for raw in tf.get_premise_definitions():
            name = raw.get("full_name")
            code = raw.get("code")
            if not name or not code or name in seen_in_file:
                continue
            seen_in_file.add(name)
            if name in by_name:
                continue
            premise = Premise(name=name, text=code, base_score=0.0)
            entry = PoolEntry(
                premise=premise,
                source_file=source_file,
                name_tokens=frozenset(useful_tokens(lean_name_tokens(name))),
                all_tokens=frozenset(useful_tokens(lean_name_tokens(f"{name} {code}"))),
            )
            by_name[name] = entry
            by_file[source_file].append(entry)
            pool.append(entry)

    token_index: dict[str, list[int]] = defaultdict(list)
    for idx, entry in enumerate(pool):
        for tok in entry.all_tokens:
            token_index[tok].append(idx)
    return pool, by_name, token_index, by_file


def same_file_hard_negatives(
    goal: Goal,
    *,
    entries: list[PoolEntry],
    existing_names: set[str],
    limit: int,
    rng: random.Random,
) -> list[PoolEntry]:
    if limit <= 0:
        return []
    query = useful_tokens(goal_query_tokens(goal))
    filtered = [entry for entry in entries if entry.premise.name not in existing_names]
    filtered.sort(key=lambda entry: hard_negative_score(query, entry, rng), reverse=True)
    return filtered[:limit]


def make_goals(
    traced: object,
    *,
    n_goals: int,
    seed: int,
    max_candidates: int,
    max_same_file: int,
    max_imported: int,
    min_candidates: int,
    min_imported_core: int,
) -> list[Goal]:
    rng = random.Random(seed)
    pool, global_by_name, token_index, premises_by_file = build_global_pool(traced)
    candidate_theorems = [
        thm
        for thm in traced.get_traced_theorems()
        if not is_private_theorem(thm) and thm.has_tactic_proof()
    ]
    rng.shuffle(candidate_theorems)

    goals: list[Goal] = []
    for thm in candidate_theorems:
        file_path = theorem_file_path(thm)
        proof_core = collect_proof_core(thm)
        matched_core = [name for name in proof_core if name in global_by_name]
        if not matched_core or len(matched_core) > max_candidates:
            continue

        imported_core = [name for name in matched_core if global_by_name[name].source_file != file_path]
        if len(imported_core) < min_imported_core:
            continue

        statement = thm.get_theorem_statement().rstrip()
        metadata = {
            "repo_url": thm.repo.url,
            "commit": thm.repo.commit,
            "file_path": file_path,
            "theorem": thm.theorem.full_name,
            "start": pos_tuple(thm.start),
            "end": pos_tuple(thm.end),
            "source": "leandojo_v2_trace_phase3_global_imported_core",
            "tactic_script": tactic_script(thm),
            "evaluator": "trace_core_recovery",
            "candidate_scope": "global_same_file_and_imported_core",
        }
        goal_seed = random.Random(f"{seed}:{thm.theorem.full_name}")
        shell_goal = Goal(
            goal_id=f"mathlib4::{thm.theorem.full_name}",
            goal_state=statement,
            candidates=[],
            proof_core=matched_core,
            local_premises=[],
            metadata=metadata,
        )

        candidates: list[Premise] = []
        existing_names: set[str] = set()
        for name in matched_core:
            entry = global_by_name[name]
            same_file = entry.source_file == file_path
            candidates.append(
                clone_candidate(
                    shell_goal,
                    entry.premise,
                    same_file=same_file,
                    tags=core_tags(name, same_file=same_file),
                    rng=goal_seed,
                )
            )
            existing_names.add(name)

        same_file_budget = max(0, max_same_file - sum(1 for p in candidates if "same_file" in p.tags))
        for entry in same_file_hard_negatives(
            shell_goal,
            entries=premises_by_file.get(file_path, []),
            existing_names=existing_names,
            limit=same_file_budget,
            rng=goal_seed,
        ):
            candidates.append(
                clone_candidate(
                    shell_goal,
                    entry.premise,
                    same_file=True,
                    tags=premise_tags(entry.premise.name, is_core=False, rng=goal_seed),
                    rng=goal_seed,
                )
            )
            existing_names.add(entry.premise.name)

        for entry in imported_hard_negatives(
            shell_goal,
            pool=pool,
            token_index=token_index,
            existing_names=existing_names | set(matched_core),
            max_imported=max_imported,
            rng=goal_seed,
        ):
            candidates.append(
                clone_candidate(
                    shell_goal,
                    entry.premise,
                    same_file=False,
                    tags=imported_tags(goal_seed),
                    rng=goal_seed,
                )
            )
            existing_names.add(entry.premise.name)

        if len(candidates) < min_candidates:
            continue
        capped = cap_with_core(candidates, set(matched_core), max_candidates)
        metadata.update(
            {
                "phase3_imported_core": len(imported_core),
                "phase3_same_file_core": len(matched_core) - len(imported_core),
                "phase3_same_file_candidates": sum(1 for p in capped if "same_file" in p.tags),
                "phase3_imported_candidates": sum(1 for p in capped if "imported" in p.tags),
                "phase3_max_candidates": max_candidates,
                "phase3_seed": seed,
            }
        )
        goals.append(
            Goal(
                goal_id=f"mathlib4::{thm.theorem.full_name}",
                goal_state=statement,
                candidates=capped,
                proof_core=matched_core,
                local_premises=[],
                metadata=metadata,
            )
        )
        if len(goals) % 250 == 0:
            print(f"wrote-ready {len(goals)}/{n_goals} goals")
        if len(goals) >= n_goals:
            break

    return goals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--n-goals", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--max-candidates", type=int, default=256)
    parser.add_argument("--max-same-file", type=int, default=96)
    parser.add_argument("--max-imported", type=int, default=192)
    parser.add_argument("--min-candidates", type=int, default=32)
    parser.add_argument("--min-imported-core", type=int, default=1)
    args = parser.parse_args()

    from lean_dojo_v2.lean_dojo.data_extraction.traced_data import TracedRepo

    traced = TracedRepo.load_from_disk(args.trace_root, build_deps=False)
    goals = make_goals(
        traced,
        n_goals=args.n_goals,
        seed=args.seed,
        max_candidates=args.max_candidates,
        max_same_file=args.max_same_file,
        max_imported=args.max_imported,
        min_candidates=args.min_candidates,
        min_imported_core=args.min_imported_core,
    )
    write_goals_jsonl(goals, args.out)
    avg_imported_core = sum(int(g.metadata["phase3_imported_core"]) for g in goals) / max(len(goals), 1)
    avg_imported = sum(int(g.metadata["phase3_imported_candidates"]) for g in goals) / max(len(goals), 1)
    print(
        f"wrote {len(goals)} goals to {args.out}; "
        f"avg imported core={avg_imported_core:.2f}, avg imported candidates={avg_imported:.1f}"
    )
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
