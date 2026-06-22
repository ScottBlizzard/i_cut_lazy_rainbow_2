#!/usr/bin/env python3
"""Evaluate learned typed action allocators against fixed portfolios.

This is an offline gate over an existing verified action matrix.  It tests
whether a stronger text/numeric allocator can beat or compress the fixed typed
portfolio under matched proof-action budgets.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB


STOPWORDS = {
    "after",
    "apply",
    "error",
    "failed",
    "from",
    "goal",
    "hammer",
    "input",
    "lean",
    "mathlib4",
    "no",
    "premise",
    "premises",
    "sorry",
    "tactic",
    "the",
    "this",
    "try",
}


@dataclass
class LinearActionModels:
    name: str
    vectorizer: Any
    models: dict[str, Any]
    priors: dict[str, float]
    actions: list[str]

    def rank(self, text: str) -> list[str]:
        x = self.vectorizer.transform([text])
        scored: list[tuple[float, str]] = []
        for action in self.actions:
            model = self.models.get(action)
            prior = self.priors.get(action, 0.0)
            if model is None:
                score = -1e9 + prior
            elif hasattr(model, "decision_function"):
                score = float(model.decision_function(x)[0])
            else:
                score = float(model.predict_log_proba(x)[0][1])
            scored.append((score + 1e-3 * prior, action))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [action for _, action in scored]


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


def empty_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return action_verified(by_goal, goal, "hammer_empty")


def any_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return any(bool(row.get("verified")) for row in by_goal.get(goal, {}).values())


def first_row(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> dict[str, Any]:
    rows = by_goal.get(goal, {})
    if not rows:
        return {}
    return next(iter(rows.values()))


def status_of(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, action: str) -> str:
    row = by_goal.get(goal, {}).get(action)
    if not row:
        return "missing"
    return "verified" if row.get("verified") else str(row.get("status", "unknown"))


def split_identifier(text: str) -> list[str]:
    return [part.lower() for part in re.findall(r"[A-Za-z0-9_']+", text) if len(part) > 1]


def goal_text(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, actions: list[str]) -> str:
    row0 = first_row(by_goal, goal)
    pieces: list[str] = [
        goal,
        str(row0.get("theorem", "")),
        str(row0.get("file_path", "")),
        f"empty_status::{status_of(by_goal, goal, 'hammer_empty')}",
    ]
    empty = by_goal.get(goal, {}).get("hammer_empty", {})
    pieces.append(str(empty.get("output_tail", ""))[:2000])
    theorem = str(row0.get("theorem", ""))
    namespace_parts = theorem.split(".")[:-1]
    pieces.extend(f"namespace::{part}" for part in namespace_parts if part)
    file_path = str(row0.get("file_path", ""))
    pieces.extend(f"file::{part}" for part in re.split(r"[\\/]", file_path) if part)

    for action in actions:
        row = by_goal.get(goal, {}).get(action, {})
        facts = [str(name) for name in row.get("facts") or []]
        simps = [str(name) for name in row.get("simps") or []]
        pieces.append(f"action::{action}")
        pieces.append(f"kind::{row.get('kind', '')}")
        pieces.append(f"fact_count::{min(len(facts), 32)}")
        pieces.append(f"simp_count::{min(len(simps), 32)}")
        if facts:
            pieces.append(f"has_facts::{action}")
        if simps:
            pieces.append(f"has_simps::{action}")
        pieces.extend(f"fact::{name}" for name in facts)
        pieces.extend(f"simp::{name}" for name in simps)

    tokens = []
    for piece in pieces:
        for token in split_identifier(piece):
            if token not in STOPWORDS:
                tokens.append(token)
    return " ".join(tokens)


def strict_goal(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return (not empty_verified(by_goal, goal)) and any_verified(by_goal, goal)


def eval_sequence(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    sequences: dict[str, list[str]],
    budget: int,
) -> dict[str, Any]:
    success = 0
    total_calls = 0
    strict_goals = [goal for goal in goals if strict_goal(by_goal, goal)]
    strict_success = 0
    for goal in goals:
        calls = 1
        solved = empty_verified(by_goal, goal)
        if not solved:
            for action in sequences[goal][:budget]:
                calls += 1
                if action_verified(by_goal, goal, action):
                    solved = True
                    break
        total_calls += calls
        if solved:
            success += 1
            if goal in strict_goals:
                strict_success += 1
    return {
        "n": len(goals),
        "success": success,
        "avg_calls": total_calls / max(1, len(goals)),
        "strict_n": len(strict_goals),
        "strict_success": strict_success,
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
    for _ in range(max_budget):
        scored = []
        for action in remaining:
            seq = {goal: selected + [action] for goal in train_goals}
            scored.append((eval_sequence(by_goal, train_goals, seq, len(selected) + 1)["success"], action))
        scored.sort(key=lambda item: (-item[0], item[1]))
        best = scored[0][1]
        selected.append(best)
        remaining.remove(best)
        portfolios.append(list(selected))
    return portfolios


def train_logreg(
    *,
    name: str,
    texts: dict[str, str],
    train_goals: list[str],
    actions: list[str],
    by_goal: dict[str, dict[str, dict[str, Any]]],
    residual_solved: Callable[[str], bool] | None = None,
    c_value: float = 1.0,
    class_weight: str | None = "balanced",
) -> LinearActionModels:
    if residual_solved is None:
        residual_solved = lambda _goal: False
    vectorizer = TfidfVectorizer(min_df=1, max_features=12000, ngram_range=(1, 2), sublinear_tf=True)
    x = vectorizer.fit_transform([texts[goal] for goal in train_goals])
    models: dict[str, Any] = {}
    priors: dict[str, float] = {}
    for action in actions:
        y = np.array(
            [
                int((not residual_solved(goal)) and action_verified(by_goal, goal, action))
                for goal in train_goals
            ]
        )
        priors[action] = float(y.mean())
        if y.sum() == 0 or y.sum() == len(y):
            continue
        model = LogisticRegression(
            C=c_value,
            class_weight=class_weight,
            solver="liblinear",
            max_iter=2000,
            random_state=0,
        )
        model.fit(x, y)
        models[action] = model
    return LinearActionModels(name=name, vectorizer=vectorizer, models=models, priors=priors, actions=actions)


def train_cnb(
    *,
    name: str,
    texts: dict[str, str],
    train_goals: list[str],
    actions: list[str],
    by_goal: dict[str, dict[str, dict[str, Any]]],
    residual_solved: Callable[[str], bool] | None = None,
) -> LinearActionModels:
    if residual_solved is None:
        residual_solved = lambda _goal: False
    vectorizer = CountVectorizer(min_df=1, max_features=12000, ngram_range=(1, 2))
    x = vectorizer.fit_transform([texts[goal] for goal in train_goals])
    models: dict[str, Any] = {}
    priors: dict[str, float] = {}
    for action in actions:
        y = np.array(
            [
                int((not residual_solved(goal)) and action_verified(by_goal, goal, action))
                for goal in train_goals
            ]
        )
        priors[action] = float(y.mean())
        if y.sum() == 0 or y.sum() == len(y):
            continue
        model = ComplementNB(alpha=0.5)
        model.fit(x, y)
        models[action] = model
    return LinearActionModels(name=name, vectorizer=vectorizer, models=models, priors=priors, actions=actions)


def metric_cell(value: int, n: int) -> str:
    return f"{value}/{n} ({pct(value, n)})"


def evaluate_oof(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    texts: dict[str, str],
    all_goals: list[str],
    actions: list[str],
    max_budget: int,
    folds: int,
) -> dict[str, Any]:
    fold_goals = [all_goals[i::folds] for i in range(folds)]
    totals: dict[str, dict[int, Counter[str]]] = {
        policy: {budget: Counter() for budget in range(1, max_budget + 1)}
        for policy in ["fixed", "logreg", "logreg_unbalanced", "cnb", "hybrid_logreg", "hybrid_cnb"]
    }
    fold_rows: list[dict[str, Any]] = []
    for fold_idx, heldout in enumerate(fold_goals):
        heldout_set = set(heldout)
        train_goals = [goal for goal in all_goals if goal not in heldout_set]
        portfolios = greedy_portfolios(by_goal, train_goals, actions, max_budget)
        logreg = train_logreg(
            name="logreg_balanced",
            texts=texts,
            train_goals=train_goals,
            actions=actions,
            by_goal=by_goal,
            c_value=1.0,
            class_weight="balanced",
        )
        logreg_unbalanced = train_logreg(
            name="logreg_unbalanced",
            texts=texts,
            train_goals=train_goals,
            actions=actions,
            by_goal=by_goal,
            c_value=1.0,
            class_weight=None,
        )
        cnb = train_cnb(
            name="cnb",
            texts=texts,
            train_goals=train_goals,
            actions=actions,
            by_goal=by_goal,
        )
        pure_sequences = {
            "fixed": {goal: portfolios[max_budget - 1] for goal in heldout},
            "logreg": {goal: logreg.rank(texts[goal]) for goal in heldout},
            "logreg_unbalanced": {goal: logreg_unbalanced.rank(texts[goal]) for goal in heldout},
            "cnb": {goal: cnb.rank(texts[goal]) for goal in heldout},
        }
        for budget in range(1, max_budget + 1):
            prefix = portfolios[max(0, budget - 2)] if budget > 1 else []

            def residual_solved(goal: str, prefix_actions: list[str] = prefix) -> bool:
                return empty_verified(by_goal, goal) or any(
                    action_verified(by_goal, goal, action) for action in prefix_actions
                )

            remaining = [action for action in actions if action not in prefix]
            if budget > 1:
                residual_logreg = train_logreg(
                    name="residual_logreg",
                    texts=texts,
                    train_goals=train_goals,
                    actions=remaining,
                    by_goal=by_goal,
                    residual_solved=residual_solved,
                    c_value=1.0,
                    class_weight="balanced",
                )
                residual_cnb = train_cnb(
                    name="residual_cnb",
                    texts=texts,
                    train_goals=train_goals,
                    actions=remaining,
                    by_goal=by_goal,
                    residual_solved=residual_solved,
                )
                pure_sequences["hybrid_logreg"] = {
                    goal: prefix + [action for action in residual_logreg.rank(texts[goal]) if action not in prefix]
                    for goal in heldout
                }
                pure_sequences["hybrid_cnb"] = {
                    goal: prefix + [action for action in residual_cnb.rank(texts[goal]) if action not in prefix]
                    for goal in heldout
                }
            else:
                pure_sequences["hybrid_logreg"] = pure_sequences["logreg"]
                pure_sequences["hybrid_cnb"] = pure_sequences["cnb"]

            for policy, sequences in pure_sequences.items():
                metrics = eval_sequence(by_goal, heldout, sequences, budget)
                total = totals[policy][budget]
                total["n"] += metrics["n"]
                total["success"] += metrics["success"]
                total["calls_x1000"] += int(round(metrics["avg_calls"] * metrics["n"] * 1000))
                total["strict_n"] += metrics["strict_n"]
                total["strict_success"] += metrics["strict_success"]
                fold_rows.append({"fold": fold_idx, "budget": budget, "policy": policy, **metrics})
    return {
        "folds": fold_rows,
        "totals": {
            policy: {
                str(budget): {
                    **dict(counter),
                    "avg_calls": counter["calls_x1000"] / 1000.0 / max(1, counter["n"]),
                }
                for budget, counter in budget_rows.items()
            }
            for policy, budget_rows in totals.items()
        },
    }


def train_fitted(
    *,
    by_goal: dict[str, dict[str, dict[str, Any]]],
    texts: dict[str, str],
    train_goals: list[str],
    eval_goals: list[str],
    actions: list[str],
    max_budget: int,
) -> dict[str, Any]:
    portfolios = greedy_portfolios(by_goal, train_goals, actions, max_budget)
    logreg = train_logreg(
        name="logreg_balanced",
        texts=texts,
        train_goals=train_goals,
        actions=actions,
        by_goal=by_goal,
    )
    cnb = train_cnb(name="cnb", texts=texts, train_goals=train_goals, actions=actions, by_goal=by_goal)
    rows: list[dict[str, Any]] = []
    for budget in range(1, max_budget + 1):
        policies = {
            "fixed": {goal: portfolios[budget - 1] for goal in eval_goals},
            "logreg": {goal: logreg.rank(texts[goal]) for goal in eval_goals},
            "cnb": {goal: cnb.rank(texts[goal]) for goal in eval_goals},
        }
        for policy, seqs in policies.items():
            rows.append({"budget": budget, "policy": policy, **eval_sequence(by_goal, eval_goals, seqs, budget)})
    return {"rows": rows, "fixed_portfolios": portfolios}


def markdown_report(payload: dict[str, Any]) -> str:
    max_budget = int(payload["max_budget"])
    n = int(payload["n_goals"])
    strict_n = int(payload["n_strict"])
    totals = payload["oof"]["totals"]
    policy_names = ["fixed", "logreg", "logreg_unbalanced", "cnb", "hybrid_logreg", "hybrid_cnb"]
    policy_labels = {
        "fixed": "Fixed greedy",
        "logreg": "Pure logreg",
        "logreg_unbalanced": "Pure logreg no weight",
        "cnb": "Pure ComplementNB",
        "hybrid_logreg": "Fixed prefix + residual logreg",
        "hybrid_cnb": "Fixed prefix + residual CNB",
    }

    lines: list[str] = []
    lines.append("# Mathlib 4.30 Typed Allocator Gate")
    lines.append("")
    lines.append("Date: 2026-06-23")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Matrix: `{payload['matrix_json']}`")
    lines.append(f"- Splits: `{payload['split_json']}`")
    lines.append(f"- Goals: {n}")
    lines.append(f"- Strict action-dependent goals: {strict_n}")
    lines.append("- All policies run `hammer_empty` first, then spend a retry budget over typed proof actions.")
    lines.append("- Learned policies are trained out of fold using goal text, first-failure status/output, and typed fact/simp pool features.")
    lines.append("")
    lines.append("## 5-Fold Out-of-Fold Success")
    lines.append("")
    lines.append(
        "| K | Fixed greedy | Pure logreg | Logreg no weight | Pure CNB | "
        "Fixed+residual logreg | Fixed+residual CNB | Oracle |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for budget in range(1, max_budget + 1):
        row = [totals[policy][str(budget)] for policy in policy_names]
        oracle = payload["oracle"]
        lines.append(
            f"| {budget} | "
            f"{metric_cell(row[0]['success'], n)} | {metric_cell(row[1]['success'], n)} | "
            f"{metric_cell(row[2]['success'], n)} | {metric_cell(row[3]['success'], n)} | "
            f"{metric_cell(row[4]['success'], n)} | {metric_cell(row[5]['success'], n)} | "
            f"{metric_cell(oracle, n)} |"
        )
    lines.append("")
    lines.append("## 5-Fold Strict-Goal Success")
    lines.append("")
    lines.append(
        "| K | Fixed greedy | Pure logreg | Logreg no weight | Pure CNB | "
        "Fixed+residual logreg | Fixed+residual CNB | Oracle |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for budget in range(1, max_budget + 1):
        row = [totals[policy][str(budget)] for policy in policy_names]
        lines.append(
            f"| {budget} | "
            f"{metric_cell(row[0]['strict_success'], strict_n)} | "
            f"{metric_cell(row[1]['strict_success'], strict_n)} | "
            f"{metric_cell(row[2]['strict_success'], strict_n)} | "
            f"{metric_cell(row[3]['strict_success'], strict_n)} | "
            f"{metric_cell(row[4]['strict_success'], strict_n)} | "
            f"{metric_cell(row[5]['strict_success'], strict_n)} | "
            f"{metric_cell(strict_n, strict_n)} |"
        )
    lines.append("")
    lines.append("## Average Lean Calls")
    lines.append("")
    lines.append("| K | " + " | ".join(policy_labels[policy] for policy in policy_names) + " |")
    lines.append("|---:|" + "|".join(["---:"] * len(policy_names)) + "|")
    for budget in range(1, max_budget + 1):
        lines.append(
            f"| {budget} | "
            + " | ".join(f"{totals[policy][str(budget)]['avg_calls']:.2f}" for policy in policy_names)
            + " |"
        )
    lines.append("")
    lines.append("## Train-Fitted Fixed Portfolios")
    lines.append("")
    lines.append("| K | Actions |")
    lines.append("|---:|---|")
    for idx, portfolio in enumerate(payload["train_fitted"]["fixed_portfolios"], start=1):
        lines.append(f"| {idx} | " + ", ".join(f"`{action}`" for action in portfolio) + " |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    fixed_k4 = totals["fixed"][str(min(4, max_budget))]["success"]
    best_learned = max(
        (totals[policy][str(budget)]["success"], policy, budget)
        for policy in policy_names
        if policy != "fixed"
        for budget in range(1, max_budget + 1)
    )
    lines.append(
        f"- Fixed K=4 reaches {fixed_k4}/{n} OOF. The best learned allocator setting reaches "
        f"{best_learned[0]}/{n} with `{best_learned[1]}` at K={best_learned[2]}."
    )
    if best_learned[0] > fixed_k4:
        lines.append("- Gate result: learned typed allocation beats the fixed K=4 control.")
    elif best_learned[0] == fixed_k4 and best_learned[2] < 4:
        lines.append("- Gate result: learned typed allocation matches fixed K=4 with fewer retry slots.")
    else:
        lines.append(
            "- Gate result: learned typed allocation does not beat or compress fixed K=4; adaptive routing "
            "should remain outside the main claim."
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
        str(action)
        for action in list(matrix.get("action_names") or sorted({row["action"] for row in matrix["results"]}))
        if str(action) != "hammer_empty"
    ]
    split_goals = {
        "train": list(split["train"]),
        "dev": list(split["dev"]),
        "test": list(split["test"]),
    }
    all_goals = split_goals["train"] + split_goals["dev"] + split_goals["test"]
    texts = {goal: goal_text(by_goal, goal, actions) for goal in all_goals}
    missing = sorted(goal for goal in all_goals if goal not in by_goal)
    if missing:
        raise SystemExit(f"Split goals missing from matrix JSON: {missing[:5]}")

    oof = evaluate_oof(
        by_goal=by_goal,
        texts=texts,
        all_goals=all_goals,
        actions=actions,
        max_budget=args.max_budget,
        folds=args.folds,
    )
    train_eval = train_fitted(
        by_goal=by_goal,
        texts=texts,
        train_goals=split_goals["train"],
        eval_goals=all_goals,
        actions=actions,
        max_budget=args.max_budget,
    )
    payload = {
        "matrix_json": str(args.matrix_json),
        "split_json": str(args.split_json),
        "max_budget": args.max_budget,
        "folds": args.folds,
        "n_goals": len(all_goals),
        "n_strict": sum(1 for goal in all_goals if strict_goal(by_goal, goal)),
        "oracle": sum(1 for goal in all_goals if any_verified(by_goal, goal)),
        "oof": oof,
        "train_fitted": train_eval,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(markdown_report(payload), encoding="utf-8")
    sys.stdout.buffer.write(args.out_md.read_text(encoding="utf-8").encode("utf-8"))


if __name__ == "__main__":
    main()
