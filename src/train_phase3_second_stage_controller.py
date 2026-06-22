"""Train failure-conditioned second-stage rankers for Phase 3 learned retrieval."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from data_io import load_goals_jsonl, write_goals_jsonl
from feature_extraction import bm25_scores, features_for_premise, visible_feature_score
from provers.trace_core import TraceCoreProver
from schema import Goal, Premise


FAILURE_TYPES = (
    "imported_premise_missing",
    "missing_bridge",
    "type_mismatch",
    "rewrite_direction",
    "typeclass_missing",
    "reconstruction_failure",
    "local_context_missing",
    "timeout",
)

DECL_KINDS = ("theorem", "lemma", "def", "abbrev", "instance", "class", "structure", "inductive", "unknown")

FEATURE_NAMES = [
    "learned_score",
    "learned_rank_pct",
    "base_score",
    "base_rank_pct",
    "bm25_all",
    "bm25_all_rank_pct",
    "visible_all",
    "visible_all_rank_pct",
    "visible_name",
    "visible_statement",
    "visible_decl",
    "same_file",
    "imported_candidate",
    "namespace_prefix_len",
    "name_depth",
    "name_token_overlap",
    "leaf_token_overlap",
    "statement_token_overlap",
    "log_text_length",
    "is_def_like",
    "is_theorem_like",
    "has_simp_attr",
] + [f"decl_kind_{kind}" for kind in DECL_KINDS]


def rank_pct(scores: dict[str, float], candidates: list[Premise]) -> dict[str, float]:
    ranked = sorted(candidates, key=lambda p: scores.get(p.name, 0.0), reverse=True)
    denom = max(len(ranked) - 1, 1)
    return {p.name: idx / denom for idx, p in enumerate(ranked)}


def learned_scores(goal: Goal) -> dict[str, float]:
    return {p.name: float(p.features.get("learned_score", p.base_score)) for p in goal.candidates}


def goal_views(goal: Goal) -> dict[str, dict[str, float]]:
    learned = learned_scores(goal)
    base = {p.name: float(p.base_score) for p in goal.candidates}
    bm25_all = bm25_scores(goal)
    visible_all = {p.name: visible_feature_score(goal, p) for p in goal.candidates}
    visible_name = {p.name: visible_feature_score(goal, p, group="name") for p in goal.candidates}
    visible_statement = {p.name: visible_feature_score(goal, p, group="statement") for p in goal.candidates}
    visible_decl = {p.name: visible_feature_score(goal, p, group="decl") for p in goal.candidates}
    return {
        "learned": learned,
        "learned_rank_pct": rank_pct(learned, goal.candidates),
        "base": base,
        "base_rank_pct": rank_pct(base, goal.candidates),
        "bm25_all": bm25_all,
        "bm25_all_rank_pct": rank_pct(bm25_all, goal.candidates),
        "visible_all": visible_all,
        "visible_all_rank_pct": rank_pct(visible_all, goal.candidates),
        "visible_name": visible_name,
        "visible_statement": visible_statement,
        "visible_decl": visible_decl,
    }


def initial_attempt(goal: Goal) -> list[Premise]:
    return sorted(goal.candidates, key=lambda p: float(p.features.get("learned_score", p.base_score)), reverse=True)[:32]


def first_failure(goal: Goal, prover: TraceCoreProver) -> tuple[str | None, set[str], set[str]]:
    premises = initial_attempt(goal)
    result = prover.prove(goal, premises, timeout_s=30.0)
    selected = {p.name for p in premises}
    if result.verified or result.failure is None:
        return None, selected, set()
    missing = set(result.failure.raw.get("missing_core", []))
    return result.failure.failure_type, selected, missing


def feature_vector(goal: Goal, premise: Premise, views: dict[str, dict[str, float]]) -> list[float]:
    f = features_for_premise(goal, premise)
    kind = str(f.get("decl_kind", "unknown"))
    if kind not in DECL_KINDS:
        kind = "unknown"
    same_file = bool(f.get("same_file", False))
    values = [
        views["learned"].get(premise.name, 0.0),
        views["learned_rank_pct"].get(premise.name, 1.0),
        views["base"].get(premise.name, 0.0),
        views["base_rank_pct"].get(premise.name, 1.0),
        views["bm25_all"].get(premise.name, 0.0),
        views["bm25_all_rank_pct"].get(premise.name, 1.0),
        views["visible_all"].get(premise.name, 0.0),
        views["visible_all_rank_pct"].get(premise.name, 1.0),
        views["visible_name"].get(premise.name, 0.0),
        views["visible_statement"].get(premise.name, 0.0),
        views["visible_decl"].get(premise.name, 0.0),
        1.0 if same_file else 0.0,
        0.0 if same_file else 1.0,
        float(f.get("namespace_prefix_len", 0)),
        float(f.get("name_depth", 0)),
        float(f.get("name_token_overlap", 0)),
        float(f.get("leaf_token_overlap", 0)),
        float(f.get("statement_token_overlap", 0)),
        math.log1p(float(f.get("text_length", 0))),
        1.0 if bool(f.get("is_def_like", False)) else 0.0,
        1.0 if bool(f.get("is_theorem_like", False)) else 0.0,
        1.0 if bool(f.get("has_simp_attr", False)) else 0.0,
    ]
    values.extend(1.0 if kind == decl_kind else 0.0 for decl_kind in DECL_KINDS)
    return values


def build_training_data(goals: list[Goal]) -> tuple[dict[str, list[list[float]]], dict[str, list[int]], dict[str, Any]]:
    prover = TraceCoreProver()
    x_by_type: dict[str, list[list[float]]] = defaultdict(list)
    y_by_type: dict[str, list[int]] = defaultdict(list)
    failure_counts = Counter()
    positive_counts = Counter()
    skipped_solved = 0

    for goal in goals:
        failure_type, selected, missing = first_failure(goal, prover)
        if failure_type is None:
            skipped_solved += 1
            continue
        failure_counts[failure_type] += 1
        views = goal_views(goal)
        for premise in goal.candidates:
            if premise.name in selected:
                continue
            label = 1 if premise.name in missing else 0
            x_by_type[failure_type].append(feature_vector(goal, premise, views))
            y_by_type[failure_type].append(label)
            positive_counts[failure_type] += label

    stats = {
        "failure_counts": dict(failure_counts),
        "positive_counts": dict(positive_counts),
        "skipped_initially_solved": skipped_solved,
    }
    return x_by_type, y_by_type, stats


def fit_models(x_by_type: dict[str, list[list[float]]], y_by_type: dict[str, list[int]]) -> tuple[dict[str, Any], dict[str, Any]]:
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    models: dict[str, Any] = {}
    model_json: dict[str, Any] = {
        "backend": "sklearn_logistic_regression_per_failure_type",
        "feature_names": FEATURE_NAMES,
        "failure_types": list(FAILURE_TYPES),
        "models": {},
    }
    for failure_type in FAILURE_TYPES:
        x = x_by_type.get(failure_type, [])
        y = y_by_type.get(failure_type, [])
        if not x or len(set(y)) < 2:
            continue
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(class_weight="balanced", max_iter=1000, solver="lbfgs"),
        )
        model.fit(x, y)
        models[failure_type] = model
        scaler = model.named_steps["standardscaler"]
        lr = model.named_steps["logisticregression"]
        model_json["models"][failure_type] = {
            "n_examples": len(x),
            "n_positive": int(sum(y)),
            "positive_rate": float(sum(y) / max(len(y), 1)),
            "mean": [float(v) for v in scaler.mean_],
            "scale": [float(v) for v in scaler.scale_],
            "coef": [float(v) for v in lr.coef_[0]],
            "intercept": float(lr.intercept_[0]),
        }
    return models, model_json


def score_goals(goals: list[Goal], models: dict[str, Any]) -> list[Goal]:
    scored_goals: list[Goal] = []
    for goal in goals:
        views = goal_views(goal)
        x = [feature_vector(goal, premise, views) for premise in goal.candidates]
        scores_by_type: dict[str, list[float]] = {}
        for failure_type in FAILURE_TYPES:
            model = models.get(failure_type)
            if model is None:
                scores_by_type[failure_type] = [float(p.features.get("learned_score", p.base_score)) for p in goal.candidates]
            else:
                scores_by_type[failure_type] = [float(v) for v in model.decision_function(x)]

        new_candidates = []
        for idx, premise in enumerate(goal.candidates):
            features = dict(premise.features)
            for failure_type in FAILURE_TYPES:
                features[f"second_stage_score_{failure_type}"] = scores_by_type[failure_type][idx]
            new_candidates.append(
                Premise(
                    name=premise.name,
                    text=premise.text,
                    base_score=premise.base_score,
                    tags=premise.tags,
                    features=features,
                )
            )
        metadata = dict(goal.metadata)
        metadata["second_stage_scored"] = True
        scored_goals.append(
            Goal(
                goal_id=goal.goal_id,
                goal_state=goal.goal_state,
                candidates=new_candidates,
                proof_core=goal.proof_core,
                local_premises=goal.local_premises,
                metadata=metadata,
            )
        )
    return scored_goals


def ranking_metrics(goals: list[Goal], failure_type: str) -> dict[str, float]:
    ks = (32, 56, 96)
    solved = {k: 0 for k in ks}
    recall = {k: 0.0 for k in ks}
    key = f"second_stage_score_{failure_type}"
    for goal in goals:
        core = set(goal.proof_core)
        ranked = sorted(goal.candidates, key=lambda p: float(p.features.get(key, p.features.get("learned_score", 0.0))), reverse=True)
        for k in ks:
            selected = {p.name for p in ranked[:k]}
            if core <= selected:
                solved[k] += 1
            recall[k] += len(core & selected) / max(len(core), 1)
    n = max(len(goals), 1)
    return {f"all_core_at_{k}": solved[k] / n for k in ks} | {
        f"mean_core_recall_at_{k}": recall[k] / n for k in ks
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-goals", type=Path, required=True)
    parser.add_argument("--eval-goals", type=Path, required=True)
    parser.add_argument("--eval-out", type=Path, required=True)
    parser.add_argument("--model-out", type=Path, required=True)
    args = parser.parse_args()

    train_goals = load_goals_jsonl(args.train_goals)
    eval_goals = load_goals_jsonl(args.eval_goals)
    x_by_type, y_by_type, stats = build_training_data(train_goals)
    models, model_json = fit_models(x_by_type, y_by_type)
    scored_eval = score_goals(eval_goals, models)
    write_goals_jsonl(scored_eval, args.eval_out)

    model_json.update(
        {
            "train_goals": len(train_goals),
            "eval_goals": len(eval_goals),
            "training_stats": stats,
            "eval_metrics": {
                failure_type: ranking_metrics(scored_eval, failure_type)
                for failure_type in FAILURE_TYPES
                if failure_type in models
            },
        }
    )
    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    args.model_out.write_text(json.dumps(model_json, indent=2), encoding="utf-8")
    print(
        f"trained {len(models)} second-stage models on {len(train_goals)} goals; "
        f"wrote {args.eval_out}"
    )
    print(json.dumps(model_json["training_stats"], indent=2))


if __name__ == "__main__":
    main()
