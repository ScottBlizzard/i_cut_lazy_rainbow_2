#!/usr/bin/env python3
"""Evaluate budgeted proof-action policies on a verified action matrix.

This is an offline evaluator: it does not run Lean.  It asks whether richer
goal/failure features can route a small retry budget better than a fixed
train-greedy action portfolio.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable


STOPWORDS = {
    "after",
    "apply",
    "duplicates",
    "error",
    "failed",
    "from",
    "goal",
    "hammer",
    "iclr",
    "initial",
    "input",
    "lean",
    "made",
    "mathlib4",
    "no",
    "outputs",
    "paper",
    "premise",
    "premises",
    "progress",
    "project",
    "removing",
    "selector",
    "sorry",
    "terms",
    "the",
    "this",
    "thymic",
    "try",
    "user",
    "workspace",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pct(num: int, den: int) -> str:
    if den == 0:
        return "0.0%"
    return f"{100.0 * num / den:.1f}%"


def goal_action_index(results: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    by_goal: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in results:
        by_goal[str(row["goal_id"])][str(row["action"])] = row
    return by_goal


def action_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, action: str) -> bool:
    return bool(by_goal.get(goal, {}).get(action, {}).get("verified"))


def any_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return any(bool(row.get("verified")) for row in by_goal.get(goal, {}).values())


def empty_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return action_verified(by_goal, goal, "hammer_empty")


def empty_status(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> str:
    row = by_goal.get(goal, {}).get("hammer_empty")
    if not row:
        return "missing"
    return "proved" if row.get("verified") else str(row.get("status", "unknown"))


def first_row(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> dict[str, Any]:
    rows = by_goal.get(goal, {})
    if not rows:
        return {}
    return next(iter(rows.values()))


def token_counts(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> Counter[str]:
    rows = by_goal.get(goal, {})
    row0 = first_row(by_goal, goal)
    empty = rows.get("hammer_empty", {})
    facts: list[str] = []
    simps: list[str] = []
    for row in rows.values():
        facts.extend(str(name) for name in row.get("facts") or [])
        simps.extend(str(name) for name in row.get("simps") or [])
    pieces = [
        goal,
        str(row0.get("theorem", "")),
        str(row0.get("file_path", "")),
        str(empty.get("status", "")),
        str(empty.get("output_tail", "")),
        *facts,
        *simps,
    ]
    raw_tokens = re.findall(r"[A-Za-z0-9_']+", "\n".join(pieces).lower())
    counts = Counter(token for token in raw_tokens if len(token) > 1 and token not in STOPWORDS)
    counts[f"status::{empty_status(by_goal, goal)}"] += 5
    theorem = str(row0.get("theorem", ""))
    for namespace in theorem.split(".")[:-1]:
        if namespace:
            counts[f"namespace::{namespace.lower()}"] += 3
    file_path = str(row0.get("file_path", ""))
    for part in re.split(r"[\\/]", file_path):
        if part and part.endswith(".lean"):
            part = part[:-5]
        if part:
            counts[f"file::{part.lower()}"] += 2
    return counts


def train_nb(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    tokens: dict[str, Counter[str]],
    train_goals: list[str],
    actions: list[str],
    residual_solved: Callable[[str], bool] | None = None,
) -> dict[str, dict[str, Any]]:
    if residual_solved is None:
        residual_solved = lambda _goal: False
    vocab = sorted({token for goal in train_goals for token in tokens[goal]})
    vocab_size = max(1, len(vocab))
    models: dict[str, dict[str, Any]] = {}
    for action in actions:
        pos_counts: Counter[str] = Counter()
        neg_counts: Counter[str] = Counter()
        n_pos = 0
        for goal in train_goals:
            positive = (not residual_solved(goal)) and action_verified(by_goal, goal, action)
            if positive:
                n_pos += 1
                pos_counts.update(tokens[goal])
            else:
                neg_counts.update(tokens[goal])
        models[action] = {
            "prior": (n_pos + 1.0) / (len(train_goals) + 2.0),
            "pos_counts": pos_counts,
            "neg_counts": neg_counts,
            "pos_total": sum(pos_counts.values()) + vocab_size,
            "neg_total": sum(neg_counts.values()) + vocab_size,
            "n_pos": n_pos,
        }
    return models


def nb_rank(tokens: dict[str, Counter[str]], goal: str, models: dict[str, dict[str, Any]]) -> list[str]:
    counts = tokens[goal]
    scored: list[tuple[float, str]] = []
    for action, model in models.items():
        prior = float(model["prior"])
        score = math.log(prior) - math.log(1.0 - prior)
        pos_counts: Counter[str] = model["pos_counts"]
        neg_counts: Counter[str] = model["neg_counts"]
        pos_total = float(model["pos_total"])
        neg_total = float(model["neg_total"])
        for token, count in counts.items():
            pos_prob = (pos_counts[token] + 1.0) / pos_total
            neg_prob = (neg_counts[token] + 1.0) / neg_total
            score += count * (math.log(pos_prob) - math.log(neg_prob))
        scored.append((score, action))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [action for _, action in scored]


def cosine(a: Counter[str], b: Counter[str]) -> float:
    dot = sum(value * b.get(token, 0) for token, value in a.items())
    if dot == 0:
        return 0.0
    norm_a = math.sqrt(sum(value * value for value in a.values()))
    norm_b = math.sqrt(sum(value * value for value in b.values()))
    return dot / max(norm_a * norm_b, 1e-12)


def knn_rank(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    tokens: dict[str, Counter[str]],
    train_goals: list[str],
    goal: str,
    actions: list[str],
    residual_solved: Callable[[str], bool] | None = None,
    neighbor_k: int = 25,
    prior_weight: float = 0.5,
) -> list[str]:
    if residual_solved is None:
        residual_solved = lambda _goal: False
    neighbors = sorted(
        ((cosine(tokens[goal], tokens[train_goal]), train_goal) for train_goal in train_goals if train_goal != goal),
        key=lambda item: (-item[0], item[1]),
    )[:neighbor_k]
    scored: list[tuple[float, str]] = []
    for action in actions:
        positives = sum(
            1
            for train_goal in train_goals
            if (not residual_solved(train_goal)) and action_verified(by_goal, train_goal, action)
        )
        prior = (positives + 1.0) / (len(train_goals) + 2.0)
        numerator = 0.0
        denominator = 0.0
        for similarity, train_goal in neighbors:
            if similarity <= 0:
                continue
            denominator += similarity
            if (not residual_solved(train_goal)) and action_verified(by_goal, train_goal, action):
                numerator += similarity
        score = (numerator + prior_weight * prior) / (denominator + prior_weight)
        scored.append((score, action))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [action for _, action in scored]


def eval_fixed(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    actions: list[str],
) -> int:
    return sum(
        1
        for goal in goals
        if empty_verified(by_goal, goal) or any(action_verified(by_goal, goal, action) for action in actions)
    )


def eval_policy(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    ranker: Callable[[str], list[str]],
    budget: int,
) -> int:
    return sum(
        1
        for goal in goals
        if empty_verified(by_goal, goal)
        or any(action_verified(by_goal, goal, action) for action in ranker(goal)[:budget])
    )


def greedy_portfolios(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    train_goals: list[str],
    actions: list[str],
    max_budget: int,
) -> list[list[str]]:
    selected: list[str] = []
    remaining = list(actions)
    portfolios: list[list[str]] = []
    for _ in range(max_budget):
        scored = [
            (eval_fixed(by_goal, train_goals, selected + [action]), action)
            for action in remaining
        ]
        scored.sort(key=lambda item: (-item[0], item[1]))
        best_action = scored[0][1]
        selected.append(best_action)
        remaining.remove(best_action)
        portfolios.append(list(selected))
    return portfolios


def strict_goals(by_goal: dict[str, dict[str, dict[str, Any]]], goals: list[str]) -> list[str]:
    return [
        goal
        for goal in goals
        if (not empty_verified(by_goal, goal)) and any_verified(by_goal, goal)
    ]


def evaluate_split(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    tokens: dict[str, Counter[str]],
    train_goals: list[str],
    eval_goals: list[str],
    actions: list[str],
    max_budget: int,
) -> list[dict[str, Any]]:
    portfolios = greedy_portfolios(by_goal, train_goals, actions, max_budget)
    nb_models = train_nb(by_goal=by_goal, tokens=tokens, train_goals=train_goals, actions=actions)

    rows: list[dict[str, Any]] = []
    eval_strict = strict_goals(by_goal, eval_goals)
    for budget in range(1, max_budget + 1):
        fixed = portfolios[budget - 1]
        pure_nb = lambda goal, models=nb_models: nb_rank(tokens, goal, models)
        pure_knn = lambda goal, tg=train_goals: knn_rank(
            by_goal=by_goal,
            tokens=tokens,
            train_goals=tg,
            goal=goal,
            actions=actions,
        )

        row: dict[str, Any] = {
            "budget": budget,
            "fixed_actions": fixed,
            "fixed": eval_fixed(by_goal, eval_goals, fixed),
            "pure_nb": eval_policy(by_goal, eval_goals, pure_nb, budget),
            "pure_knn": eval_policy(by_goal, eval_goals, pure_knn, budget),
            "fixed_strict": eval_fixed(by_goal, eval_strict, fixed),
            "pure_nb_strict": eval_policy(by_goal, eval_strict, pure_nb, budget),
            "pure_knn_strict": eval_policy(by_goal, eval_strict, pure_knn, budget),
        }
        if budget == 1:
            row["hybrid_nb"] = row["pure_nb"]
            row["hybrid_knn"] = row["pure_knn"]
            row["hybrid_nb_strict"] = row["pure_nb_strict"]
            row["hybrid_knn_strict"] = row["pure_knn_strict"]
        else:
            prefix = portfolios[budget - 2]

            def residual_solved(goal: str, prefix_actions: list[str] = prefix) -> bool:
                return empty_verified(by_goal, goal) or any(
                    action_verified(by_goal, goal, action) for action in prefix_actions
                )

            remaining = [action for action in actions if action not in prefix]
            residual_nb = train_nb(
                by_goal=by_goal,
                tokens=tokens,
                train_goals=train_goals,
                actions=remaining,
                residual_solved=residual_solved,
            )

            def hybrid_nb_rank(goal: str, prefix_actions: list[str] = prefix, models: dict[str, dict[str, Any]] = residual_nb) -> list[str]:
                return prefix_actions + [
                    action for action in nb_rank(tokens, goal, models) if action not in prefix_actions
                ]

            def hybrid_knn_rank(goal: str, prefix_actions: list[str] = prefix, remaining_actions: list[str] = remaining) -> list[str]:
                return prefix_actions + [
                    action
                    for action in knn_rank(
                        by_goal=by_goal,
                        tokens=tokens,
                        train_goals=train_goals,
                        goal=goal,
                        actions=remaining_actions,
                        residual_solved=residual_solved,
                    )
                    if action not in prefix_actions
                ]

            row["hybrid_nb"] = eval_policy(by_goal, eval_goals, hybrid_nb_rank, budget)
            row["hybrid_knn"] = eval_policy(by_goal, eval_goals, hybrid_knn_rank, budget)
            row["hybrid_nb_strict"] = eval_policy(by_goal, eval_strict, hybrid_nb_rank, budget)
            row["hybrid_knn_strict"] = eval_policy(by_goal, eval_strict, hybrid_knn_rank, budget)
        rows.append(row)
    return rows


def crossval(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    tokens: dict[str, Counter[str]],
    all_goals: list[str],
    actions: list[str],
    max_budget: int,
    folds: int,
) -> dict[str, Any]:
    fold_goals = [all_goals[i::folds] for i in range(folds)]
    totals: dict[int, Counter[str]] = {budget: Counter() for budget in range(1, max_budget + 1)}
    fold_rows: list[dict[str, Any]] = []
    for fold_idx, heldout in enumerate(fold_goals):
        heldout_set = set(heldout)
        train_goals = [goal for goal in all_goals if goal not in heldout_set]
        rows = evaluate_split(
            by_goal=by_goal,
            tokens=tokens,
            train_goals=train_goals,
            eval_goals=heldout,
            actions=actions,
            max_budget=max_budget,
        )
        heldout_strict = strict_goals(by_goal, heldout)
        for row in rows:
            budget = int(row["budget"])
            totals[budget]["n"] += len(heldout)
            totals[budget]["strict_n"] += len(heldout_strict)
            totals[budget]["empty"] += sum(1 for goal in heldout if empty_verified(by_goal, goal))
            totals[budget]["oracle"] += sum(1 for goal in heldout if any_verified(by_goal, goal))
            totals[budget]["strict_oracle"] += len(heldout_strict)
            for key in [
                "fixed",
                "pure_nb",
                "pure_knn",
                "hybrid_nb",
                "hybrid_knn",
                "fixed_strict",
                "pure_nb_strict",
                "pure_knn_strict",
                "hybrid_nb_strict",
                "hybrid_knn_strict",
            ]:
                totals[budget][key] += int(row[key])
            fold_rows.append({"fold": fold_idx, **row})
    return {
        "folds": fold_rows,
        "totals": {str(budget): dict(counter) for budget, counter in totals.items()},
    }


def missed_oracle_goals(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    actions: list[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for goal in goals:
        if not any_verified(by_goal, goal):
            continue
        if empty_verified(by_goal, goal) or any(action_verified(by_goal, goal, action) for action in actions):
            continue
        verified_actions = sorted(
            action for action, row in by_goal[goal].items() if bool(row.get("verified"))
        )
        row0 = first_row(by_goal, goal)
        rows.append(
            {
                "goal_id": goal,
                "theorem": row0.get("theorem", goal),
                "file_path": row0.get("file_path", ""),
                "verified_actions": verified_actions,
            }
        )
    return rows


def metric_cell(value: int, n: int) -> str:
    return f"{value}/{n} ({pct(value, n)})"


def markdown_report(payload: dict[str, Any]) -> str:
    split_rows = payload["split_metrics"]
    crossval_totals = payload["crossval"]["totals"]
    max_budget = int(payload["max_budget"])
    n_all = int(payload["n_all"])
    strict_all = int(payload["strict_all"])

    lines: list[str] = []
    lines.append("# Mathlib 4.30 Budgeted Action-Policy Experiment")
    lines.append("")
    lines.append("Date: 2026-06-22")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Matrix: `{payload['matrix_json']}`")
    lines.append(f"- Splits: `{payload['split_json']}`")
    lines.append(f"- Replayable goals: {n_all}")
    lines.append(f"- Strict action-dependent oracle goals: {strict_all}")
    lines.append("- Policies always run `hammer_empty` first, then spend K retry actions.")
    lines.append("- Learned policies are trained only on the train split, except the OOF table which retrains per fold.")
    lines.append("")
    lines.append("## Train-Fitted Split Results")
    lines.append("")
    lines.append("| Split | K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for split_name in ["train", "dev", "test", "all"]:
        block = split_rows[split_name]
        n = int(block["n"])
        oracle = int(block["oracle"])
        for row in block["rows"]:
            lines.append(
                f"| {split_name} | {row['budget']} | "
                f"{metric_cell(row['fixed'], n)} | "
                f"{metric_cell(row['pure_nb'], n)} | "
                f"{metric_cell(row['pure_knn'], n)} | "
                f"{metric_cell(row['hybrid_nb'], n)} | "
                f"{metric_cell(row['hybrid_knn'], n)} | "
                f"{metric_cell(oracle, n)} |"
            )
    lines.append("")
    lines.append("## 5-Fold Out-of-Fold Results")
    lines.append("")
    lines.append("| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Empty | Oracle |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for budget in range(1, max_budget + 1):
        row = crossval_totals[str(budget)]
        n = int(row["n"])
        lines.append(
            f"| {budget} | "
            f"{metric_cell(row['fixed'], n)} | "
            f"{metric_cell(row['pure_nb'], n)} | "
            f"{metric_cell(row['pure_knn'], n)} | "
            f"{metric_cell(row['hybrid_nb'], n)} | "
            f"{metric_cell(row['hybrid_knn'], n)} | "
            f"{metric_cell(row['empty'], n)} | "
            f"{metric_cell(row['oracle'], n)} |"
        )
    lines.append("")
    lines.append("## 5-Fold Strict-Goal Results")
    lines.append("")
    lines.append("| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|")
    for budget in range(1, max_budget + 1):
        row = crossval_totals[str(budget)]
        n = int(row["strict_n"])
        lines.append(
            f"| {budget} | "
            f"{metric_cell(row['fixed_strict'], n)} | "
            f"{metric_cell(row['pure_nb_strict'], n)} | "
            f"{metric_cell(row['pure_knn_strict'], n)} | "
            f"{metric_cell(row['hybrid_nb_strict'], n)} | "
            f"{metric_cell(row['hybrid_knn_strict'], n)} | "
            f"{metric_cell(row['strict_oracle'], n)} |"
        )
    lines.append("")
    lines.append("## Fixed Greedy Portfolios")
    lines.append("")
    lines.append("| K | Actions | Train-Fitted All Success |")
    lines.append("|---:|---|---:|")
    all_block = split_rows["all"]
    for row in all_block["rows"]:
        actions = ", ".join(f"`{action}`" for action in row["fixed_actions"])
        lines.append(f"| {row['budget']} | {actions} | {metric_cell(row['fixed'], int(all_block['n']))} |")
    lines.append("")
    lines.append("## Oracle Misses For Train-Greedy Fixed Portfolios")
    lines.append("")
    for budget in range(1, max_budget + 1):
        misses = payload["fixed_oracle_misses"][str(budget)]
        lines.append(f"### K={budget}")
        if not misses:
            lines.append("")
            lines.append("- None.")
            lines.append("")
            continue
        lines.append("")
        for item in misses:
            actions = ", ".join(f"`{action}`" for action in item["verified_actions"])
            lines.append(f"- `{item['goal_id']}`: solved by {actions}")
        lines.append("")
    lines.append("## Readout")
    lines.append("")
    oof_k2 = crossval_totals["2"]
    oof_k3 = crossval_totals["3"]
    lines.append(
        f"- OOF fixed greedy K=2 reaches {oof_k2['fixed']}/{oof_k2['n']}; residual adaptive K=2 reaches "
        f"{oof_k2['hybrid_nb']}/{oof_k2['n']} (NB) and {oof_k2['hybrid_knn']}/{oof_k2['n']} (kNN)."
    )
    lines.append(
        f"- OOF fixed greedy K=3 reaches {oof_k3['fixed']}/{oof_k3['n']}; residual adaptive K=3 reaches "
        f"{oof_k3['hybrid_nb']}/{oof_k3['n']} (NB) and {oof_k3['hybrid_knn']}/{oof_k3['n']} (kNN)."
    )
    lines.append(
        "- Current evidence favors a compute-budgeted typed portfolio as the hard baseline/main mechanism; "
        "richer adaptive routing is not yet clearly above that baseline."
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-json", required=True, type=Path)
    parser.add_argument("--split-json", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-budget", type=int, default=4)
    parser.add_argument("--folds", type=int, default=5)
    args = parser.parse_args()

    matrix = load_json(args.matrix_json)
    split = load_json(args.split_json)
    by_goal = goal_action_index(matrix["results"])
    actions = [
        action
        for action in list(matrix.get("action_names") or sorted({row["action"] for row in matrix["results"]}))
        if action != "hammer_empty"
    ]
    split_goals = {
        "train": list(split["train"]),
        "dev": list(split["dev"]),
        "test": list(split["test"]),
    }
    split_goals["all"] = split_goals["train"] + split_goals["dev"] + split_goals["test"]
    missing = sorted(goal for goal in split_goals["all"] if goal not in by_goal)
    if missing:
        raise SystemExit(f"Split goals missing from matrix JSON: {missing[:5]}")

    tokens = {goal: token_counts(by_goal, goal) for goal in split_goals["all"]}
    split_metrics: dict[str, Any] = {}
    for name, goals in split_goals.items():
        rows = evaluate_split(
            by_goal=by_goal,
            tokens=tokens,
            train_goals=split_goals["train"],
            eval_goals=goals,
            actions=actions,
            max_budget=args.max_budget,
        )
        split_metrics[name] = {
            "n": len(goals),
            "empty": sum(1 for goal in goals if empty_verified(by_goal, goal)),
            "oracle": sum(1 for goal in goals if any_verified(by_goal, goal)),
            "strict_n": len(strict_goals(by_goal, goals)),
            "rows": rows,
        }

    cv = crossval(
        by_goal=by_goal,
        tokens=tokens,
        all_goals=split_goals["all"],
        actions=actions,
        max_budget=args.max_budget,
        folds=args.folds,
    )
    all_portfolios = greedy_portfolios(
        by_goal,
        split_goals["train"],
        actions,
        args.max_budget,
    )
    fixed_misses = {
        str(idx): missed_oracle_goals(by_goal, split_goals["all"], portfolio)
        for idx, portfolio in enumerate(all_portfolios, start=1)
    }
    payload = {
        "matrix_json": str(args.matrix_json),
        "split_json": str(args.split_json),
        "max_budget": args.max_budget,
        "folds": args.folds,
        "n_all": len(split_goals["all"]),
        "strict_all": len(strict_goals(by_goal, split_goals["all"])),
        "actions": actions,
        "split_metrics": split_metrics,
        "crossval": cv,
        "fixed_oracle_misses": fixed_misses,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(markdown_report(payload), encoding="utf-8")
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
