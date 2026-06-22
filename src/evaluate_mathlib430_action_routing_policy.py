#!/usr/bin/env python3
"""Evaluate simple proof-action routing policies from an action-matrix JSON."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pct(num: int, den: int) -> str:
    if den == 0:
        return "0.0%"
    return f"{100.0 * num / den:.1f}%"


def goal_action_index(results: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    by_goal: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in results:
        by_goal[row["goal_id"]][row["action"]] = row
    return by_goal


def action_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str, action: str) -> bool:
    row = by_goal.get(goal, {}).get(action)
    return bool(row and row.get("verified"))


def any_verified(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> bool:
    return any(bool(row.get("verified")) for row in by_goal.get(goal, {}).values())


def empty_status(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> str:
    row = by_goal.get(goal, {}).get("hammer_empty")
    if not row:
        return "missing"
    return "proved" if row.get("verified") else str(row.get("status", "unknown"))


def text_tokens(by_goal: dict[str, dict[str, dict[str, Any]]], goal: str) -> Counter[str]:
    row = by_goal.get(goal, {}).get("hammer_empty", {})
    text = f"{goal}\n{row.get('output_tail', '')}"
    raw_tokens = re.findall(r"[\w']+", text.lower(), flags=re.UNICODE)
    stop = {
        "mathlib4",
        "workspace",
        "thymic_project",
        "paper",
        "iclr_2",
        "outputs",
        "lean",
        "hammer",
        "premises",
        "user",
        "input",
        "terms",
        "from",
        "premise",
        "selector",
        "after",
        "removing",
        "duplicates",
        "in",
        "try",
        "this",
        "apply",
        "sorry",
        "initial",
        "goal",
        "error",
        "failed",
        "made",
        "no",
        "progress",
    }
    return Counter(token for token in raw_tokens if len(token) > 1 and token not in stop)


def train_text_nb(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    train_goals: list[str],
    actions: list[str],
) -> dict[str, dict[str, Any]]:
    docs = {goal: text_tokens(by_goal, goal) for goal in train_goals}
    vocab = sorted({token for counts in docs.values() for token in counts})
    vocab_size = max(1, len(vocab))
    models: dict[str, dict[str, Any]] = {}
    for action in actions:
        pos_goals = [goal for goal in train_goals if action_verified(by_goal, goal, action)]
        neg_goals = [goal for goal in train_goals if not action_verified(by_goal, goal, action)]
        pos_counts: Counter[str] = Counter()
        neg_counts: Counter[str] = Counter()
        for goal in pos_goals:
            pos_counts.update(docs[goal])
        for goal in neg_goals:
            neg_counts.update(docs[goal])
        pos_total = sum(pos_counts.values()) + vocab_size
        neg_total = sum(neg_counts.values()) + vocab_size
        prior = (len(pos_goals) + 1.0) / (len(train_goals) + 2.0)
        models[action] = {
            "prior": prior,
            "pos_counts": pos_counts,
            "neg_counts": neg_counts,
            "pos_total": pos_total,
            "neg_total": neg_total,
            "vocab_size": vocab_size,
            "n_pos": len(pos_goals),
        }
    return models


def predict_text_nb(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goal: str,
    models: dict[str, dict[str, Any]],
    fallback_action: str,
) -> str:
    tokens = text_tokens(by_goal, goal)
    best_action = fallback_action
    best_score = -math.inf
    for action, model in models.items():
        prior = float(model["prior"])
        score = math.log(prior) - math.log(1.0 - prior)
        pos_counts: Counter[str] = model["pos_counts"]
        neg_counts: Counter[str] = model["neg_counts"]
        pos_total = float(model["pos_total"])
        neg_total = float(model["neg_total"])
        for token, count in tokens.items():
            pos_prob = (pos_counts[token] + 1.0) / pos_total
            neg_prob = (neg_counts[token] + 1.0) / neg_total
            score += count * (math.log(pos_prob) - math.log(neg_prob))
        if score > best_score:
            best_score = score
            best_action = action
    return best_action


def success_count(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    action: str,
    *,
    include_empty_first: bool,
) -> int:
    count = 0
    for goal in goals:
        if include_empty_first and action_verified(by_goal, goal, "hammer_empty"):
            count += 1
        elif action_verified(by_goal, goal, action):
            count += 1
    return count


def choose_best_action(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    actions: list[str],
    *,
    include_empty_first: bool,
) -> tuple[str, int]:
    scored = [
        (success_count(by_goal, goals, action, include_empty_first=include_empty_first), action)
        for action in actions
    ]
    scored.sort(key=lambda item: (-item[0], item[1]))
    best_count, best_action = scored[0]
    return best_action, best_count


def train_status_rule(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    train_goals: list[str],
    actions: list[str],
    fallback_action: str,
) -> dict[str, str]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for goal in train_goals:
        status = empty_status(by_goal, goal)
        if status != "proved":
            grouped[status].append(goal)

    rule: dict[str, str] = {}
    for status, goals in grouped.items():
        best_action, _ = choose_best_action(
            by_goal,
            goals,
            actions,
            include_empty_first=False,
        )
        rule[status] = best_action
    rule["__fallback__"] = fallback_action
    return rule


def eval_status_rule(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    rule: dict[str, str],
) -> int:
    count = 0
    fallback = rule["__fallback__"]
    for goal in goals:
        status = empty_status(by_goal, goal)
        if status == "proved":
            count += 1
            continue
        action = rule.get(status, fallback)
        if action_verified(by_goal, goal, action):
            count += 1
    return count


def eval_text_nb(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    models: dict[str, dict[str, Any]],
    fallback_action: str,
) -> int:
    count = 0
    for goal in goals:
        if action_verified(by_goal, goal, "hammer_empty"):
            count += 1
            continue
        action = predict_text_nb(by_goal, goal, models, fallback_action)
        if action_verified(by_goal, goal, action):
            count += 1
    return count


def eval_portfolio(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    goals: list[str],
    actions: list[str],
    *,
    include_empty_first: bool,
) -> int:
    count = 0
    for goal in goals:
        if include_empty_first and action_verified(by_goal, goal, "hammer_empty"):
            count += 1
            continue
        if any(action_verified(by_goal, goal, action) for action in actions):
            count += 1
    return count


def greedy_portfolios(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    train_goals: list[str],
    actions: list[str],
    max_k: int,
) -> list[list[str]]:
    selected: list[str] = []
    portfolios: list[list[str]] = []
    remaining = list(actions)
    for _ in range(max_k):
        scored: list[tuple[int, str]] = []
        for action in remaining:
            trial = selected + [action]
            score = eval_portfolio(by_goal, train_goals, trial, include_empty_first=True)
            scored.append((score, action))
        scored.sort(key=lambda item: (-item[0], item[1]))
        _, best_action = scored[0]
        selected.append(best_action)
        remaining.remove(best_action)
        portfolios.append(list(selected))
    return portfolios


def split_metrics(
    name: str,
    goals: list[str],
    by_goal: dict[str, dict[str, dict[str, Any]]],
    best_single_action: str,
    best_second_action: str,
    status_rule: dict[str, str],
    text_models: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    strict_goals = [
        goal
        for goal in goals
        if (not action_verified(by_goal, goal, "hammer_empty")) and any_verified(by_goal, goal)
    ]
    return {
        "split": name,
        "n": len(goals),
        "empty_only": success_count(by_goal, goals, "hammer_empty", include_empty_first=False),
        "best_single": success_count(
            by_goal, goals, best_single_action, include_empty_first=False
        ),
        "empty_then_best_second": success_count(
            by_goal, goals, best_second_action, include_empty_first=True
        ),
        "empty_then_status_rule": eval_status_rule(by_goal, goals, status_rule),
        "empty_then_text_nb": eval_text_nb(
            by_goal, goals, text_models, best_second_action
        ),
        "oracle": sum(1 for goal in goals if any_verified(by_goal, goal)),
        "strict_n": len(strict_goals),
        "strict_best_second": success_count(
            by_goal, strict_goals, best_second_action, include_empty_first=False
        ),
        "strict_status_rule": eval_status_rule(by_goal, strict_goals, status_rule),
        "strict_text_nb": eval_text_nb(
            by_goal, strict_goals, text_models, best_second_action
        ),
        "strict_oracle": len(strict_goals),
    }


def portfolio_metrics(
    name: str,
    goals: list[str],
    by_goal: dict[str, dict[str, dict[str, Any]]],
    portfolios: list[list[str]],
) -> list[dict[str, Any]]:
    strict_goals = [
        goal
        for goal in goals
        if (not action_verified(by_goal, goal, "hammer_empty")) and any_verified(by_goal, goal)
    ]
    rows: list[dict[str, Any]] = []
    for idx, portfolio in enumerate(portfolios, start=1):
        rows.append(
            {
                "split": name,
                "k": idx,
                "actions": portfolio,
                "success": eval_portfolio(
                    by_goal, goals, portfolio, include_empty_first=True
                ),
                "n": len(goals),
                "strict_success": eval_portfolio(
                    by_goal, strict_goals, portfolio, include_empty_first=False
                ),
                "strict_n": len(strict_goals),
            }
        )
    return rows


def crossval_metrics(
    by_goal: dict[str, dict[str, dict[str, Any]]],
    all_goals: list[str],
    actions: list[str],
    k: int = 5,
) -> dict[str, Any]:
    folds = [all_goals[i::k] for i in range(k)]
    second_actions = [action for action in actions if action != "hammer_empty"]
    totals = Counter()
    fold_rows: list[dict[str, Any]] = []
    for idx, heldout in enumerate(folds):
        heldout_set = set(heldout)
        train = [goal for goal in all_goals if goal not in heldout_set]
        best_single_action, _ = choose_best_action(
            by_goal, train, actions, include_empty_first=False
        )
        best_second_action, _ = choose_best_action(
            by_goal, train, second_actions, include_empty_first=True
        )
        status_rule = train_status_rule(
            by_goal, train, second_actions, fallback_action=best_second_action
        )
        text_models = train_text_nb(by_goal, train, second_actions)
        row = split_metrics(
            f"fold{idx}",
            heldout,
            by_goal,
            best_single_action,
            best_second_action,
            status_rule,
            text_models,
        )
        row["best_single_action"] = best_single_action
        row["best_second_action"] = best_second_action
        fold_rows.append(row)
        for key in [
            "n",
            "empty_only",
            "best_single",
            "empty_then_best_second",
            "empty_then_status_rule",
            "empty_then_text_nb",
            "oracle",
            "strict_n",
            "strict_best_second",
            "strict_status_rule",
            "strict_text_nb",
            "strict_oracle",
        ]:
            totals[key] += int(row[key])
    return {"folds": fold_rows, "totals": dict(totals)}


def markdown_report(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Action Routing Policy Gate")
    lines.append("")
    lines.append("Date: 2026-06-22")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Matrix: `{payload['matrix_json']}`")
    lines.append(f"- Splits: `{payload['split_json']}`")
    lines.append(f"- Best single action selected on train: `{payload['best_single_action']}`")
    lines.append(f"- Best fixed second action after `hammer_empty`: `{payload['best_second_action']}`")
    lines.append("")
    lines.append("Status-rule policy learned on train:")
    lines.append("")
    for status, action in sorted(payload["status_rule"].items()):
        lines.append(f"- `{status}` -> `{action}`")
    lines.append("")
    lines.append("## All Goals")
    lines.append("")
    lines.append(
        "| Split | N | Empty Only | Best Single | Empty -> Best Second | Empty -> Status Rule | Oracle |"
    )
    lines[-1] = (
        "| Split | N | Empty Only | Best Single | Empty -> Best Second | "
        "Empty -> Status Rule | Empty -> Text NB | Oracle |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in payload["metrics"]:
        n = row["n"]
        lines.append(
            f"| {row['split']} | {n} | "
            f"{row['empty_only']} ({pct(row['empty_only'], n)}) | "
            f"{row['best_single']} ({pct(row['best_single'], n)}) | "
            f"{row['empty_then_best_second']} ({pct(row['empty_then_best_second'], n)}) | "
            f"{row['empty_then_status_rule']} ({pct(row['empty_then_status_rule'], n)}) | "
            f"{row['empty_then_text_nb']} ({pct(row['empty_then_text_nb'], n)}) | "
            f"{row['oracle']} ({pct(row['oracle'], n)}) |"
        )
    lines.append("")
    lines.append("## Strict Action-Dependent Goals")
    lines.append("")
    lines.append(
        "| Split | Strict N | Best Second Hits | Status Rule Hits | Text NB Hits | Oracle |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in payload["metrics"]:
        n = row["strict_n"]
        lines.append(
            f"| {row['split']} | {n} | "
            f"{row['strict_best_second']} ({pct(row['strict_best_second'], n)}) | "
            f"{row['strict_status_rule']} ({pct(row['strict_status_rule'], n)}) | "
            f"{row['strict_text_nb']} ({pct(row['strict_text_nb'], n)}) | "
            f"{row['strict_oracle']} ({pct(row['strict_oracle'], n)}) |"
        )
    lines.append("")
    lines.append("## Train-Greedy Fixed Portfolios")
    lines.append("")
    lines.append(
        "These schedules always run `hammer_empty` first, then a fixed list of second-stage actions selected greedily on train. They test whether the oracle headroom is mostly a generic retry-portfolio effect."
    )
    lines.append("")
    lines.append("| Split | Extra Actions | Fixed Actions | Success | Strict Hits |")
    lines.append("|---|---:|---|---:|---:|")
    for row in payload["portfolio_metrics"]:
        actions = ", ".join(f"`{action}`" for action in row["actions"])
        lines.append(
            f"| {row['split']} | {row['k']} | {actions} | "
            f"{row['success']}/{row['n']} ({pct(row['success'], row['n'])}) | "
            f"{row['strict_success']}/{row['strict_n']} ({pct(row['strict_success'], row['strict_n'])}) |"
        )
    lines.append("")
    lines.append("## 5-Fold Out-of-Fold Policy Check")
    lines.append("")
    cv = payload["crossval"]["totals"]
    n = cv["n"]
    lines.append(
        "| N | Empty Only | Best Single | Empty -> Best Second | Empty -> Status Rule | Empty -> Text NB | Oracle |"
    )
    lines.append("|---:|---:|---:|---:|---:|---:|---:|")
    lines.append(
        f"| {n} | "
        f"{cv['empty_only']} ({pct(cv['empty_only'], n)}) | "
        f"{cv['best_single']} ({pct(cv['best_single'], n)}) | "
        f"{cv['empty_then_best_second']} ({pct(cv['empty_then_best_second'], n)}) | "
        f"{cv['empty_then_status_rule']} ({pct(cv['empty_then_status_rule'], n)}) | "
        f"{cv['empty_then_text_nb']} ({pct(cv['empty_then_text_nb'], n)}) | "
        f"{cv['oracle']} ({pct(cv['oracle'], n)}) |"
    )
    lines.append("")
    strict_n = cv["strict_n"]
    lines.append(
        "| Strict N | Best Second Hits | Status Rule Hits | Text NB Hits | Oracle |"
    )
    lines.append("|---:|---:|---:|---:|---:|")
    lines.append(
        f"| {strict_n} | "
        f"{cv['strict_best_second']} ({pct(cv['strict_best_second'], strict_n)}) | "
        f"{cv['strict_status_rule']} ({pct(cv['strict_status_rule'], strict_n)}) | "
        f"{cv['strict_text_nb']} ({pct(cv['strict_text_nb'], strict_n)}) | "
        f"{cv['strict_oracle']} ({pct(cv['strict_oracle'], strict_n)}) |"
    )
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    test = next(row for row in payload["metrics"] if row["split"] == "test")
    if test["empty_then_status_rule"] > test["empty_then_best_second"]:
        lines.append(
            "- The coarse first-failure-status rule beats the best fixed second action on test."
        )
    elif test["empty_then_status_rule"] == test["empty_then_best_second"]:
        lines.append(
            "- The coarse first-failure-status rule ties the best fixed second action on test."
        )
    else:
        lines.append(
            "- The coarse first-failure-status rule does not beat the best fixed second action on test."
        )
    lines.append(
        "- This is a low-capacity policy gate using only the first `hammer_empty` status; richer failure transcript and goal/action features are still needed before making a strong adaptive-policy claim."
    )
    if test["empty_then_text_nb"] > test["empty_then_best_second"]:
        lines.append(
            "- The text NB policy beats the best fixed second action on test, but this split is small and should be treated as exploratory."
        )
    elif test["empty_then_text_nb"] == test["empty_then_best_second"]:
        lines.append(
            "- The text NB policy ties the best fixed second action on test."
        )
    else:
        lines.append(
            "- The text NB policy does not beat the best fixed second action on test."
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-json", required=True, type=Path)
    parser.add_argument("--split-json", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    matrix = load_json(args.matrix_json)
    split = load_json(args.split_json)
    results = matrix["results"]
    by_goal = goal_action_index(results)
    actions = list(matrix.get("action_names") or sorted({row["action"] for row in results}))

    split_goals = {
        "train": list(split["train"]),
        "dev": list(split["dev"]),
        "test": list(split["test"]),
        "all": list(split["train"]) + list(split["dev"]) + list(split["test"]),
    }
    missing = sorted(goal for goal in split_goals["all"] if goal not in by_goal)
    if missing:
        raise SystemExit(f"Split goals missing from matrix JSON: {missing[:5]}")

    best_single_action, best_single_train = choose_best_action(
        by_goal,
        split_goals["train"],
        actions,
        include_empty_first=False,
    )
    second_actions = [action for action in actions if action != "hammer_empty"]
    best_second_action, best_second_train = choose_best_action(
        by_goal,
        split_goals["train"],
        second_actions,
        include_empty_first=True,
    )
    status_rule = train_status_rule(
        by_goal,
        split_goals["train"],
        second_actions,
        fallback_action=best_second_action,
    )
    text_models = train_text_nb(by_goal, split_goals["train"], second_actions)

    metrics = [
        split_metrics(
            name,
            goals,
            by_goal,
            best_single_action,
            best_second_action,
            status_rule,
            text_models,
        )
        for name, goals in split_goals.items()
    ]
    portfolios = greedy_portfolios(by_goal, split_goals["train"], second_actions, max_k=4)
    portfolio_rows: list[dict[str, Any]] = []
    for name, goals in split_goals.items():
        portfolio_rows.extend(portfolio_metrics(name, goals, by_goal, portfolios))
    cv = crossval_metrics(by_goal, split_goals["all"], actions, k=5)
    payload = {
        "matrix_json": str(args.matrix_json),
        "split_json": str(args.split_json),
        "best_single_action": best_single_action,
        "best_single_train_success": best_single_train,
        "best_second_action": best_second_action,
        "best_second_train_success": best_second_train,
        "status_rule": status_rule,
        "text_nb_action_positive_counts": {
            action: model["n_pos"] for action, model in text_models.items()
        },
        "first_status_counts": dict(Counter(empty_status(by_goal, goal) for goal in split_goals["all"])),
        "metrics": metrics,
        "greedy_portfolios": portfolios,
        "portfolio_metrics": portfolio_rows,
        "crossval": cv,
    }

    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(markdown_report(payload), encoding="utf-8")


if __name__ == "__main__":
    main()
