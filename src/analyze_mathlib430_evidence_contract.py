#!/usr/bin/env python3
"""Audit the evidence contract behind the Mathlib 4.30 action matrix.

This script is deliberately offline: it reads an existing verified action
matrix and the frozen trace corpus, then computes reviewer-facing controls for
source provenance, Aesop channel interactions, homogeneous portfolios, and
first-success compute accounting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pct(num: int | float, den: int | float) -> str:
    if den == 0:
        return "0.0%"
    return f"{100.0 * float(num) / float(den):.1f}%"


def mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    idx = min(len(xs) - 1, max(0, round((len(xs) - 1) * q)))
    return xs[idx]


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def goal_action_index(results: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    by_goal: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in results:
        by_goal[str(row["goal_id"])][str(row["action"])] = row
    return by_goal


def action_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, action: str) -> bool:
    return bool(by_goal.get(goal, {}).get(action, {}).get("verified"))


def action_time(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, action: str) -> float:
    row = by_goal.get(goal, {}).get(action)
    if not row:
        return 0.0
    try:
        return float(row.get("time_s") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def empty_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return action_verified(by_goal, goal, "hammer_empty")


def any_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return any(bool(row.get("verified")) for row in by_goal.get(goal, {}).values())


def strict_goal(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return (not empty_verified(by_goal, goal)) and any_verified(by_goal, goal)


def candidate_records(row: dict[str, Any], n: int) -> list[dict[str, Any]]:
    candidates = list(row.get("candidates") or [])

    def key(item: dict[str, Any]) -> tuple[float, float, str]:
        features = item.get("features") or {}
        rank = features.get("learned_rank")
        score = features.get("learned_score")
        return (
            float(rank) if rank is not None else 1e9,
            -float(score) if score is not None else 0.0,
            str(item.get("name", "")),
        )

    return sorted(candidates, key=key)[:n]


def load_trace_rows(path: Path, goal_ids: set[str]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            goal_id = str(row.get("goal_id", ""))
            if goal_id in goal_ids:
                rows[goal_id] = row
    missing = goal_ids - set(rows)
    if missing:
        raise SystemExit(f"missing {len(missing)} matrix goals from trace jsonl; first={sorted(missing)[:3]}")
    return rows


def exact_binom_two_sided(k: int, n: int) -> float:
    if n <= 0:
        return 1.0
    observed = math.comb(n, k) * (0.5**n)
    prob = 0.0
    for i in range(n + 1):
        pi = math.comb(n, i) * (0.5**n)
        if pi <= observed + 1e-15:
            prob += pi
    return min(1.0, prob)


def bootstrap_delta_ci(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    action: str,
    baseline: str,
    *,
    rounds: int = 2000,
    seed: int = 17,
) -> tuple[float, float]:
    rng = random.Random(seed)
    deltas: list[float] = []
    n = len(goals)
    for _ in range(rounds):
        sample = [goals[rng.randrange(n)] for _ in range(n)]
        delta = sum(
            int(action_verified(by_goal, goal, action)) - int(action_verified(by_goal, goal, baseline))
            for goal in sample
        ) / max(1, n)
        deltas.append(delta)
    return quantile(deltas, 0.025), quantile(deltas, 0.975)


def paired_action_delta(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    action: str,
    baseline: str,
) -> dict[str, Any]:
    gains: list[str] = []
    losses: list[str] = []
    both_success = 0
    both_fail = 0
    for goal in goals:
        a = action_verified(by_goal, goal, action)
        b = action_verified(by_goal, goal, baseline)
        if a and not b:
            gains.append(goal)
        elif b and not a:
            losses.append(goal)
        elif a and b:
            both_success += 1
        else:
            both_fail += 1
    ci_low, ci_high = bootstrap_delta_ci(by_goal, goals, action, baseline)
    return {
        "action": action,
        "baseline": baseline,
        "action_success": sum(1 for goal in goals if action_verified(by_goal, goal, action)),
        "baseline_success": sum(1 for goal in goals if action_verified(by_goal, goal, baseline)),
        "gains": gains,
        "losses": losses,
        "both_success": both_success,
        "both_fail": both_fail,
        "net_gain": len(gains) - len(losses),
        "mcnemar_exact_p": exact_binom_two_sided(min(len(gains), len(losses)), len(gains) + len(losses)),
        "bootstrap_delta_ci": [ci_low, ci_high],
    }


def aesop_bucket(action: str) -> tuple[str, str]:
    if action == "aesop_empty":
        return "empty", "empty"
    if action.startswith("aesop_core_plus_learned32"):
        source = "oracle_core+retrieved32"
    elif action.startswith("aesop_core_plus_learned16"):
        source = "oracle_core+retrieved16"
    elif action.startswith("aesop_core_plus_learned"):
        source = "oracle_core+retrieved8"
    elif action.startswith("aesop_learned32"):
        source = "retrieved32"
    elif action.startswith("aesop_learned16"):
        source = "retrieved16"
    elif action.startswith("aesop_learned8"):
        source = "retrieved8"
    elif action.startswith("aesop_core"):
        source = "oracle_core"
    else:
        source = "other"
    if action.endswith("_facts"):
        exposure = "facts-only"
    elif action.endswith("_simps"):
        exposure = "simps-only"
    else:
        exposure = "facts+simps"
    return source, exposure


def summarize_provenance(
    *,
    matrix: dict[str, Any],
    trace_rows: dict[str, dict[str, Any]],
    goals: list[str],
) -> dict[str, Any]:
    by_action: dict[str, dict[str, Any]] = {}
    source_counter: dict[str, Counter[str]] = defaultdict(Counter)
    for result in matrix["results"]:
        action = str(result["action"])
        goal = str(result["goal_id"])
        trace = trace_rows[goal]
        proof_core = {str(name) for name in trace.get("proof_core") or [] if name}
        retrieved_any = {str(c.get("name", "")) for c in trace.get("candidates") or [] if c.get("name")}
        retrieved_top8 = {str(c.get("name", "")) for c in candidate_records(trace, 8) if c.get("name")}
        retrieved_top32 = {str(c.get("name", "")) for c in candidate_records(trace, 32) if c.get("name")}
        selected = [str(name) for name in (result.get("facts") or []) + (result.get("simps") or [])]
        bucket = by_action.setdefault(
            action,
            {
                "attempts": 0,
                "verified": 0,
                "fact_counts": [],
                "simp_counts": [],
                "time_s": [],
                "selected_names": 0,
                "oracle_core_names": 0,
                "retrieved_top8_names": 0,
                "retrieved_top32_names": 0,
                "retrieved_any_names": 0,
                "unknown_names": 0,
            },
        )
        bucket["attempts"] += 1
        bucket["verified"] += int(bool(result.get("verified")))
        bucket["fact_counts"].append(int(result.get("fact_count") or 0))
        bucket["simp_counts"].append(int(result.get("simp_count") or 0))
        bucket["time_s"].append(float(result.get("time_s") or 0.0))
        for name in selected:
            bucket["selected_names"] += 1
            if name in proof_core:
                bucket["oracle_core_names"] += 1
                source_counter[action]["oracle_core"] += 1
            if name in retrieved_top8:
                bucket["retrieved_top8_names"] += 1
            if name in retrieved_top32:
                bucket["retrieved_top32_names"] += 1
            if name in retrieved_any:
                bucket["retrieved_any_names"] += 1
                source_counter[action]["retrieved_any"] += 1
            if name not in proof_core and name not in retrieved_any:
                bucket["unknown_names"] += 1
                source_counter[action]["unknown"] += 1

    action_summary: dict[str, Any] = {}
    for action, row in by_action.items():
        action_summary[action] = {
            "attempts": row["attempts"],
            "verified": row["verified"],
            "avg_facts": mean(row["fact_counts"]),
            "avg_simps": mean(row["simp_counts"]),
            "avg_time_s": mean(row["time_s"]),
            "selected_names": row["selected_names"],
            "oracle_core_names": row["oracle_core_names"],
            "retrieved_top8_names": row["retrieved_top8_names"],
            "retrieved_top32_names": row["retrieved_top32_names"],
            "retrieved_any_names": row["retrieved_any_names"],
            "unknown_names": row["unknown_names"],
        }

    trace_summary_rows: list[dict[str, Any]] = []
    for goal in goals:
        trace = trace_rows[goal]
        proof_core = unique([str(name) for name in trace.get("proof_core") or [] if name])
        retrieved8 = unique([str(c.get("name", "")) for c in candidate_records(trace, 8) if c.get("name")])
        retrieved32 = unique([str(c.get("name", "")) for c in candidate_records(trace, 32) if c.get("name")])
        trace_summary_rows.append(
            {
                "goal_id": goal,
                "proof_core": len(proof_core),
                "retrieved_top8": len(retrieved8),
                "retrieved_top32": len(retrieved32),
                "proof_core_in_top8": len(set(proof_core) & set(retrieved8)),
                "proof_core_in_top32": len(set(proof_core) & set(retrieved32)),
                "proof_core_only_top32": len(set(proof_core) - set(retrieved32)),
            }
        )
    agg_keys = [
        "proof_core",
        "retrieved_top8",
        "retrieved_top32",
        "proof_core_in_top8",
        "proof_core_in_top32",
        "proof_core_only_top32",
    ]
    trace_agg = {
        key: {
            "mean": mean([float(row[key]) for row in trace_summary_rows]),
            "median": statistics.median([float(row[key]) for row in trace_summary_rows]),
            "sum": sum(int(row[key]) for row in trace_summary_rows),
        }
        for key in agg_keys
    }
    return {
        "action_summary": action_summary,
        "trace_goal_summary": trace_summary_rows,
        "trace_aggregate": trace_agg,
        "source_counter": {action: dict(counter) for action, counter in source_counter.items()},
    }


def summarize_aesop_controls(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
) -> dict[str, Any]:
    aesop_actions = sorted(
        {
            action
            for rows in by_goal.values()
            for action in rows
            if action.startswith("aesop_")
        }
    )
    by_action: dict[str, Any] = {}
    for action in aesop_actions:
        source, exposure = aesop_bucket(action)
        by_action[action] = {
            "source": source,
            "exposure": exposure,
            "success": sum(1 for goal in goals if action_verified(by_goal, goal, action)),
            "paired_vs_aesop_empty": paired_action_delta(by_goal, goals, action, "aesop_empty")
            if action != "aesop_empty"
            else None,
        }

    triples: dict[str, Any] = {}
    for base in [
        "aesop_core",
        "aesop_core_plus_learned",
        "aesop_core_plus_learned16",
        "aesop_core_plus_learned32",
        "aesop_learned8",
        "aesop_learned16",
        "aesop_learned32",
    ]:
        facts = f"{base}_facts"
        simps = f"{base}_simps"
        if base not in aesop_actions or facts not in aesop_actions or simps not in aesop_actions:
            continue
        joint_only_single = []
        joint_new_empty = []
        joint_poison_empty = []
        single_any = []
        for goal in goals:
            j = action_verified(by_goal, goal, base)
            f = action_verified(by_goal, goal, facts)
            s = action_verified(by_goal, goal, simps)
            e = action_verified(by_goal, goal, "aesop_empty")
            if j and not f and not s:
                joint_only_single.append(goal)
            if j and not e:
                joint_new_empty.append(goal)
            if e and not j:
                joint_poison_empty.append(goal)
            if f or s:
                single_any.append(goal)
        triples[base] = {
            "joint_success": sum(1 for goal in goals if action_verified(by_goal, goal, base)),
            "facts_success": sum(1 for goal in goals if action_verified(by_goal, goal, facts)),
            "simps_success": sum(1 for goal in goals if action_verified(by_goal, goal, simps)),
            "single_union_success": len(set(single_any)),
            "joint_only_over_single_channels": joint_only_single,
            "joint_new_over_empty": joint_new_empty,
            "joint_poisoned_vs_empty": joint_poison_empty,
            "paired_vs_empty": paired_action_delta(by_goal, goals, base, "aesop_empty"),
            "paired_vs_facts": paired_action_delta(by_goal, goals, base, facts),
            "paired_vs_simps": paired_action_delta(by_goal, goals, base, simps),
        }
    return {"by_action": by_action, "triples": triples}


def eval_sequence(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    sequences: dict[str, list[str]],
    budget: int,
    *,
    include_hammer_empty: bool = True,
) -> dict[str, Any]:
    successes: list[str] = []
    calls: list[int] = []
    times: list[float] = []
    first_success: Counter[str] = Counter()
    strict_successes = 0
    strict_goals = [goal for goal in goals if strict_goal(by_goal, goal)]
    for goal in goals:
        goal_calls = 0
        goal_time = 0.0
        solved = False
        if include_hammer_empty:
            goal_calls += 1
            goal_time += action_time(by_goal, goal, "hammer_empty")
            if empty_verified(by_goal, goal):
                solved = True
                first_success["hammer_empty"] += 1
        if not solved:
            for action in sequences.get(goal, [])[:budget]:
                goal_calls += 1
                goal_time += action_time(by_goal, goal, action)
                if action_verified(by_goal, goal, action):
                    solved = True
                    first_success[action] += 1
                    break
        calls.append(goal_calls)
        times.append(goal_time)
        if solved:
            successes.append(goal)
            if goal in strict_goals:
                strict_successes += 1
    return {
        "n": len(goals),
        "success": len(successes),
        "strict_n": len(strict_goals),
        "strict_success": strict_successes,
        "avg_calls": mean([float(c) for c in calls]),
        "avg_time_s": mean(times),
        "median_time_s": quantile(times, 0.5),
        "p90_time_s": quantile(times, 0.9),
        "total_time_s": sum(times),
        "first_success": dict(first_success),
        "success_goals": successes,
    }


def greedy_portfolios(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    train_goals: list[str],
    actions: list[str],
    max_budget: int,
) -> list[list[str]]:
    selected: list[str] = []
    remaining = list(actions)
    portfolios: list[list[str]] = []
    for _ in range(min(max_budget, len(remaining))):
        scored: list[tuple[int, str]] = []
        for action in remaining:
            seq = {goal: selected + [action] for goal in train_goals}
            scored.append((eval_sequence(by_goal, train_goals, seq, len(selected) + 1)["success"], action))
        scored.sort(key=lambda item: (-item[0], item[1]))
        best = scored[0][1]
        selected.append(best)
        remaining.remove(best)
        portfolios.append(list(selected))
    while len(portfolios) < max_budget:
        portfolios.append(list(selected))
    return portfolios


def action_groups(actions: list[str]) -> dict[str, list[str]]:
    nonempty = [action for action in actions if action != "hammer_empty"]
    simplification = [
        action
        for action in nonempty
        if action.startswith("simp")
        or action.startswith("simpa")
        or action in {"norm_num_empty", "ring_nf_empty"}
    ]
    return {
        "full_action_grid": nonempty,
        "typed_nonempty_grid": [
            action
            for action in nonempty
            if not action.endswith("_empty") and action not in {"linarith_empty", "nlinarith_empty", "omega_empty", "ring_nf_empty", "norm_num_empty"}
        ],
        "aesop_all": [action for action in nonempty if action.startswith("aesop_")],
        "aesop_nonempty": [action for action in nonempty if action.startswith("aesop_") and action != "aesop_empty"],
        "hammer_only": [action for action in nonempty if action.startswith("hammer_")],
        "hammerCore_only": [action for action in nonempty if action.startswith("hammerCore_")],
        "simplification_only": simplification,
        "solve_by_elim_only": [action for action in nonempty if action.startswith("solve_by_elim_")],
        "raw_arith_norm_only": [
            action
            for action in nonempty
            if action in {"linarith_empty", "nlinarith_empty", "omega_empty", "ring_nf_empty", "norm_num_empty"}
        ],
    }


def fold_goals_from_split(split: dict[str, Any], folds: int) -> list[list[str]]:
    all_goals = [str(goal) for goal in split["train"]] + [str(goal) for goal in split["dev"]] + [str(goal) for goal in split["test"]]
    return [all_goals[i::folds] for i in range(folds)]


def summarize_homogeneous_portfolios(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    split: dict[str, Any],
    actions: list[str],
    max_budget: int,
    folds: int,
) -> dict[str, Any]:
    groups = {name: values for name, values in action_groups(actions).items() if values}
    fold_goals = fold_goals_from_split(split, folds)
    group_totals: dict[str, dict[str, Any]] = {}
    group_folds: list[dict[str, Any]] = []
    for group_name, group_actions in groups.items():
        totals = {
            str(k): {
                "n": 0,
                "success": 0,
                "strict_n": 0,
                "strict_success": 0,
                "calls_sum": 0.0,
                "time_sum": 0.0,
            }
            for k in range(1, max_budget + 1)
        }
        for fold_idx, heldout in enumerate(fold_goals):
            heldout_set = set(heldout)
            train = [goal for goal in goals if goal not in heldout_set]
            portfolios = greedy_portfolios(by_goal, train, group_actions, max_budget)
            for budget, portfolio in enumerate(portfolios, start=1):
                sequences = {goal: portfolio for goal in heldout}
                eval_row = eval_sequence(by_goal, heldout, sequences, budget)
                group_folds.append(
                    {
                        "group": group_name,
                        "fold": fold_idx,
                        "budget": budget,
                        "portfolio": portfolio,
                        "success": eval_row["success"],
                        "n": eval_row["n"],
                        "strict_success": eval_row["strict_success"],
                        "strict_n": eval_row["strict_n"],
                        "avg_calls": eval_row["avg_calls"],
                        "avg_time_s": eval_row["avg_time_s"],
                    }
                )
                total = totals[str(budget)]
                total["n"] += eval_row["n"]
                total["success"] += eval_row["success"]
                total["strict_n"] += eval_row["strict_n"]
                total["strict_success"] += eval_row["strict_success"]
                total["calls_sum"] += eval_row["avg_calls"] * eval_row["n"]
                total["time_sum"] += eval_row["avg_time_s"] * eval_row["n"]
        for row in totals.values():
            row["avg_calls"] = row["calls_sum"] / max(1, row["n"])
            row["avg_time_s"] = row["time_sum"] / max(1, row["n"])
        train_portfolios = greedy_portfolios(by_goal, list(split["train"]), group_actions, max_budget)
        group_totals[group_name] = {
            "n_actions": len(group_actions),
            "actions": group_actions,
            "oof_totals": totals,
            "train_fitted": [
                {
                    "budget": budget,
                    "portfolio": portfolio,
                    **eval_sequence(by_goal, goals, {goal: portfolio for goal in goals}, budget),
                }
                for budget, portfolio in enumerate(train_portfolios, start=1)
            ],
        }

    random_summary = random_portfolio_summary(
        by_goal=by_goal,
        goals=goals,
        actions=groups["full_action_grid"],
        max_budget=max_budget,
        seeds=100,
    )
    return {
        "groups": group_totals,
        "folds": group_folds,
        "random_full_grid": random_summary,
    }


def random_portfolio_summary(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    actions: list[str],
    max_budget: int,
    seeds: int,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for seed in range(seeds):
        rng = random.Random(seed)
        shuffled = list(actions)
        rng.shuffle(shuffled)
        portfolio = shuffled[:max_budget]
        eval_row = eval_sequence(by_goal, goals, {goal: portfolio for goal in goals}, max_budget)
        rows.append(
            {
                "seed": seed,
                "portfolio": portfolio,
                "success": eval_row["success"],
                "strict_success": eval_row["strict_success"],
                "avg_calls": eval_row["avg_calls"],
                "avg_time_s": eval_row["avg_time_s"],
            }
        )
    successes = [float(row["success"]) for row in rows]
    return {
        "seeds": seeds,
        "budget": max_budget,
        "mean_success": mean(successes),
        "median_success": quantile(successes, 0.5),
        "min_success": min(successes) if successes else 0,
        "max_success": max(successes) if successes else 0,
        "rows": rows,
    }


def summarize_compute_frontier(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    homogeneous: dict[str, Any],
    max_budget: int,
) -> dict[str, Any]:
    frontier: list[dict[str, Any]] = []
    empty_eval = eval_sequence(by_goal, goals, {goal: [] for goal in goals}, 0)
    frontier.append({"policy": "hammer_empty", "budget": 0, **empty_eval})
    best_single = "aesop_core_plus_learned"
    if all(best_single in by_goal[goal] for goal in goals):
        row = eval_sequence(by_goal, goals, {goal: [best_single] for goal in goals}, 1)
        frontier.append({"policy": best_single, "budget": 1, **row})
    for group_name, group in homogeneous["groups"].items():
        for budget in range(1, max_budget + 1):
            train_fitted = group["train_fitted"][budget - 1]
            portfolio = train_fitted["portfolio"]
            row = eval_sequence(by_goal, goals, {goal: portfolio for goal in goals}, budget)
            frontier.append(
                {
                    "policy": f"{group_name}_train_fitted",
                    "budget": budget,
                    "portfolio": portfolio,
                    **row,
                }
            )
    frontier.sort(key=lambda row: (float(row["avg_time_s"]), -int(row["success"]), str(row["policy"])))
    return {"frontier": frontier}


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    n = payload["n_goals"]
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Evidence Contract Audit")
    lines.append("")
    lines.append("Date: 2026-06-23")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    for key in ["matrix_json", "split_json", "input_jsonl"]:
        meta = payload["inputs"][key]
        lines.append(f"- `{meta['path']}` (`sha256={meta['sha256'][:12]}...`)")
    lines.append(f"- Goals: {n}")
    lines.append(f"- Matrix attempts: {payload['matrix_summary']['n_attempts']}")
    lines.append("")
    lines.append("## Protocol Readout")
    lines.append("")
    lines.append(
        "- `core` in the current action names is traced `proof_core`; this audit therefore relabels it as `oracle_core` in interpretation."
    )
    lines.append(
        "- Current headline results should be described as a mechanism-isolation setting over oracle-core plus retrieved evidence, not as a deployable retriever-only premise selector."
    )
    lines.append(
        "- Existing timing is runner wallclock per Lean attempt. It supports matched Lean-call and empirical wallclock frontier wording, but not a formal heartbeat-normalized compute claim."
    )
    lines.append("")
    lines.append("## Trace Provenance")
    lines.append("")
    agg = payload["provenance"]["trace_aggregate"]
    lines.append("| Quantity per goal | Mean | Median | Sum |")
    lines.append("|---|---:|---:|---:|")
    for key in [
        "proof_core",
        "retrieved_top8",
        "retrieved_top32",
        "proof_core_in_top8",
        "proof_core_in_top32",
        "proof_core_only_top32",
    ]:
        row = agg[key]
        lines.append(f"| `{key}` | {row['mean']:.2f} | {row['median']:.1f} | {row['sum']} |")
    lines.append("")
    lines.append("## Action Provenance")
    lines.append("")
    lines.append("| Action | Verified | Avg facts | Avg simps | Oracle-core names | Retrieved top-8 names | Retrieved top-32 names | Unknown | Avg time(s) |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for action, row in sorted(
        payload["provenance"]["action_summary"].items(),
        key=lambda item: (-item[1]["verified"], item[0]),
    )[:30]:
        lines.append(
            f"| `{action}` | {row['verified']} | {row['avg_facts']:.2f} | {row['avg_simps']:.2f} | "
            f"{row['oracle_core_names']} | {row['retrieved_top8_names']} | {row['retrieved_top32_names']} | "
            f"{row['unknown_names']} | {row['avg_time_s']:.2f} |"
        )
    lines.append("")
    lines.append("## Aesop Exact-Available Controls")
    lines.append("")
    lines.append("| Action | Source | Exposure | Success | Gain vs empty | Loss vs empty | Net | McNemar p | Bootstrap delta CI |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---|")
    for action, row in sorted(
        payload["aesop"]["by_action"].items(),
        key=lambda item: (-item[1]["success"], item[0]),
    ):
        paired = row.get("paired_vs_aesop_empty")
        if paired is None:
            lines.append(f"| `{action}` | `{row['source']}` | `{row['exposure']}` | {row['success']} | - | - | - | - | - |")
        else:
            ci = paired["bootstrap_delta_ci"]
            lines.append(
                f"| `{action}` | `{row['source']}` | `{row['exposure']}` | {row['success']} | "
                f"{len(paired['gains'])} | {len(paired['losses'])} | {paired['net_gain']} | "
                f"{paired['mcnemar_exact_p']:.4f} | [{ci[0]:.3f}, {ci[1]:.3f}] |"
            )
    lines.append("")
    lines.append("### Joint Channel Triples")
    lines.append("")
    lines.append("| Joint action | Joint | Facts | Simps | Single union | Joint-only vs singles | New vs empty | Poisoned vs empty |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for action, row in sorted(
        payload["aesop"]["triples"].items(),
        key=lambda item: (-item[1]["joint_success"], item[0]),
    ):
        lines.append(
            f"| `{action}` | {row['joint_success']} | {row['facts_success']} | {row['simps_success']} | "
            f"{row['single_union_success']} | {len(row['joint_only_over_single_channels'])} | "
            f"{len(row['joint_new_over_empty'])} | {len(row['joint_poisoned_vs_empty'])} |"
        )
    lines.append("")
    lines.append("## Homogeneous K=4 Portfolio Controls")
    lines.append("")
    lines.append("| Group | # actions | OOF K=1 | OOF K=2 | OOF K=3 | OOF K=4 | Avg calls K=4 | Avg wallclock K=4(s) |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for group_name, group in sorted(payload["homogeneous"]["groups"].items()):
        totals = group["oof_totals"]
        k4 = totals["4"]
        lines.append(
            f"| `{group_name}` | {group['n_actions']} | "
            f"{totals['1']['success']}/{totals['1']['n']} | {totals['2']['success']}/{totals['2']['n']} | "
            f"{totals['3']['success']}/{totals['3']['n']} | {k4['success']}/{k4['n']} | "
            f"{k4['avg_calls']:.2f} | {k4['avg_time_s']:.2f} |"
        )
    rnd = payload["homogeneous"]["random_full_grid"]
    lines.append("")
    lines.append(
        f"- Random full-grid K=4 over {rnd['seeds']} seeds: mean {rnd['mean_success']:.1f}/{n}, "
        f"median {rnd['median_success']:.0f}/{n}, range {rnd['min_success']:.0f}-{rnd['max_success']:.0f}."
    )
    lines.append("")
    lines.append("## First-Success Wallclock Frontier")
    lines.append("")
    lines.append("| Policy | K | Success | Strict success | Avg calls | Avg time(s) | Median time(s) | P90 time(s) | First-success leaders |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---|")
    top_frontier = sorted(
        payload["compute_frontier"]["frontier"],
        key=lambda row: (-int(row["success"]), float(row["avg_time_s"]), str(row["policy"])),
    )[:20]
    for row in top_frontier:
        first = Counter(row.get("first_success") or {})
        leaders = ", ".join(f"`{name}`:{count}" for name, count in first.most_common(3))
        lines.append(
            f"| `{row['policy']}` | {row['budget']} | {row['success']}/{row['n']} | "
            f"{row['strict_success']}/{row['strict_n']} | {row['avg_calls']:.2f} | "
            f"{row['avg_time_s']:.2f} | {row['median_time_s']:.2f} | {row['p90_time_s']:.2f} | {leaders} |"
        )
    lines.append("")
    lines.append("## Paper Implications")
    lines.append("")
    lines.append("- Submission text must replace `core` with `oracle_core` or explicitly define it as traced proof-core evidence.")
    lines.append("- The cleanest current main claim is about action-conditional evidence allocation under a frozen oracle-core-plus-retrieved evidence pool.")
    lines.append("- Aesop's strong result should be written as a source-composition by channel-assignment interaction, not merely facts versus simps complementarity.")
    lines.append("- The strongest compute-safe wording is `matched Lean-call budget`; empirical wallclock numbers can be reported as a secondary frontier.")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-json", required=True, type=Path)
    parser.add_argument("--split-json", required=True, type=Path)
    parser.add_argument("--input-jsonl", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-budget", type=int, default=4)
    parser.add_argument("--folds", type=int, default=5)
    args = parser.parse_args()

    matrix = load_json(args.matrix_json)
    split = load_json(args.split_json)
    by_goal = goal_action_index(matrix["results"])
    goals = sorted(by_goal)
    actions = sorted({str(row["action"]) for row in matrix["results"]})
    trace_rows = load_trace_rows(args.input_jsonl, set(goals))

    provenance = summarize_provenance(matrix=matrix, trace_rows=trace_rows, goals=goals)
    aesop = summarize_aesop_controls(by_goal, goals)
    homogeneous = summarize_homogeneous_portfolios(
        by_goal=by_goal,
        goals=goals,
        split=split,
        actions=actions,
        max_budget=args.max_budget,
        folds=args.folds,
    )
    compute_frontier = summarize_compute_frontier(
        by_goal=by_goal,
        goals=goals,
        homogeneous=homogeneous,
        max_budget=args.max_budget,
    )

    payload = {
        "experiment": "mathlib430_evidence_contract_audit",
        "inputs": {
            "matrix_json": {"path": str(args.matrix_json), "sha256": file_sha256(args.matrix_json)},
            "split_json": {"path": str(args.split_json), "sha256": file_sha256(args.split_json)},
            "input_jsonl": {"path": str(args.input_jsonl), "sha256": file_sha256(args.input_jsonl)},
        },
        "n_goals": len(goals),
        "matrix_summary": matrix["summary"],
        "provenance": provenance,
        "aesop": aesop,
        "homogeneous": homogeneous,
        "compute_frontier": compute_frontier,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(payload, args.out_md)
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
