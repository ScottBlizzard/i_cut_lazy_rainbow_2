"""Train and apply a lightweight Phase 3 imported-core premise retriever."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from data_io import load_goals_jsonl, write_goals_jsonl
from feature_extraction import bm25_scores, features_for_premise, visible_feature_score
from schema import Goal, Premise


DECL_KINDS = ("theorem", "lemma", "def", "abbrev", "instance", "class", "structure", "inductive", "unknown")
FEATURE_NAMES = [
    "base_score",
    "base_rank_pct",
    "bm25_all",
    "bm25_all_rank_pct",
    "bm25_statement",
    "bm25_statement_rank_pct",
    "bm25_name",
    "bm25_name_rank_pct",
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


def goal_score_views(goal: Goal) -> dict[str, dict[str, float]]:
    bm25_all = bm25_scores(goal)
    bm25_statement = bm25_scores(goal, query_variant="statement")
    bm25_name = bm25_scores(goal, query_variant="name")
    base = {p.name: float(p.base_score) for p in goal.candidates}
    visible_all = {p.name: visible_feature_score(goal, p) for p in goal.candidates}
    visible_name = {p.name: visible_feature_score(goal, p, group="name") for p in goal.candidates}
    visible_statement = {p.name: visible_feature_score(goal, p, group="statement") for p in goal.candidates}
    visible_decl = {p.name: visible_feature_score(goal, p, group="decl") for p in goal.candidates}
    return {
        "base": base,
        "base_rank_pct": rank_pct(base, goal.candidates),
        "bm25_all": bm25_all,
        "bm25_all_rank_pct": rank_pct(bm25_all, goal.candidates),
        "bm25_statement": bm25_statement,
        "bm25_statement_rank_pct": rank_pct(bm25_statement, goal.candidates),
        "bm25_name": bm25_name,
        "bm25_name_rank_pct": rank_pct(bm25_name, goal.candidates),
        "visible_all": visible_all,
        "visible_all_rank_pct": rank_pct(visible_all, goal.candidates),
        "visible_name": visible_name,
        "visible_statement": visible_statement,
        "visible_decl": visible_decl,
    }


def feature_vector(goal: Goal, premise: Premise, views: dict[str, dict[str, float]]) -> list[float]:
    f = features_for_premise(goal, premise)
    kind = str(f.get("decl_kind", "unknown"))
    if kind not in DECL_KINDS:
        kind = "unknown"
    same_file = bool(f.get("same_file", False))
    values = [
        views["base"].get(premise.name, 0.0),
        views["base_rank_pct"].get(premise.name, 1.0),
        views["bm25_all"].get(premise.name, 0.0),
        views["bm25_all_rank_pct"].get(premise.name, 1.0),
        views["bm25_statement"].get(premise.name, 0.0),
        views["bm25_statement_rank_pct"].get(premise.name, 1.0),
        views["bm25_name"].get(premise.name, 0.0),
        views["bm25_name_rank_pct"].get(premise.name, 1.0),
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


def make_matrix(goals: list[Goal]) -> tuple[list[list[float]], list[int], list[tuple[int, int]]]:
    x: list[list[float]] = []
    y: list[int] = []
    spans: list[tuple[int, int]] = []
    for goal in goals:
        start = len(x)
        core = set(goal.proof_core)
        views = goal_score_views(goal)
        for premise in goal.candidates:
            x.append(feature_vector(goal, premise, views))
            y.append(1 if premise.name in core else 0)
        spans.append((start, len(x)))
    return x, y, spans


class MeanStdFallbackModel:
    """Dependency-light fallback if sklearn is unavailable."""

    def fit(self, x: list[list[float]], y: list[int]) -> None:
        n_features = len(x[0])
        pos = [row for row, label in zip(x, y) if label]
        neg = [row for row, label in zip(x, y) if not label]
        self.mean = [sum(row[i] for row in x) / len(x) for i in range(n_features)]
        self.std = [
            max((sum((row[i] - self.mean[i]) ** 2 for row in x) / len(x)) ** 0.5, 1e-6)
            for i in range(n_features)
        ]
        pos_mean = [sum(row[i] for row in pos) / max(len(pos), 1) for i in range(n_features)]
        neg_mean = [sum(row[i] for row in neg) / max(len(neg), 1) for i in range(n_features)]
        self.coef = [(pos_mean[i] - neg_mean[i]) / self.std[i] for i in range(n_features)]
        self.intercept = 0.0

    def decision_function(self, x: list[list[float]]) -> list[float]:
        scores = []
        for row in x:
            z = self.intercept
            for value, mean, std, coef in zip(row, self.mean, self.std, self.coef):
                z += ((value - mean) / std) * coef
            scores.append(z)
        return scores

    def to_json(self) -> dict[str, Any]:
        return {
            "backend": "mean_std_fallback",
            "feature_names": FEATURE_NAMES,
            "mean": self.mean,
            "std": self.std,
            "coef": self.coef,
            "intercept": self.intercept,
        }


def fit_model(x: list[list[float]], y: list[int]) -> tuple[Any, dict[str, Any], list[float]]:
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(class_weight="balanced", max_iter=1000, solver="lbfgs"),
        )
        model.fit(x, y)
        scores = list(model.decision_function(x))
        lr = model.named_steps["logisticregression"]
        scaler = model.named_steps["standardscaler"]
        model_json = {
            "backend": "sklearn_logistic_regression",
            "feature_names": FEATURE_NAMES,
            "mean": [float(v) for v in scaler.mean_],
            "scale": [float(v) for v in scaler.scale_],
            "coef": [float(v) for v in lr.coef_[0]],
            "intercept": float(lr.intercept_[0]),
            "class_weight": "balanced",
        }
        return model, model_json, scores
    except Exception as exc:
        model = MeanStdFallbackModel()
        model.fit(x, y)
        return model, model.to_json() | {"fallback_reason": repr(exc)}, model.decision_function(x)


def model_scores(model: Any, x: list[list[float]]) -> list[float]:
    if hasattr(model, "decision_function"):
        return [float(v) for v in model.decision_function(x)]
    raise TypeError(f"model has no decision_function: {type(model)!r}")


def add_learned_scores(goals: list[Goal], model: Any) -> list[Goal]:
    scored_goals: list[Goal] = []
    for goal in goals:
        views = goal_score_views(goal)
        x = [feature_vector(goal, p, views) for p in goal.candidates]
        scores = model_scores(model, x)
        order = sorted(range(len(goal.candidates)), key=lambda i: scores[i], reverse=True)
        rank = {idx: r for r, idx in enumerate(order)}
        new_candidates = []
        for idx, premise in enumerate(goal.candidates):
            features = dict(premise.features)
            features["learned_score"] = float(scores[idx])
            features["learned_rank"] = int(rank[idx])
            features["learned_rank_pct"] = rank[idx] / max(len(goal.candidates) - 1, 1)
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
        metadata["learned_retriever_scored"] = True
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


def ranking_metrics(goals: list[Goal], score_name: str) -> dict[str, float]:
    ks = (32, 56, 96)
    solved = {k: 0 for k in ks}
    core_recall_sum = {k: 0.0 for k in ks}
    for goal in goals:
        core = set(goal.proof_core)
        if score_name == "base_score":
            ranked = sorted(goal.candidates, key=lambda p: p.base_score, reverse=True)
        else:
            ranked = sorted(goal.candidates, key=lambda p: float(p.features.get(score_name, 0.0)), reverse=True)
        for k in ks:
            selected = {p.name for p in ranked[:k]}
            recovered = len(core & selected)
            core_recall_sum[k] += recovered / max(len(core), 1)
            if core <= selected:
                solved[k] += 1
    n = max(len(goals), 1)
    metrics: dict[str, float] = {}
    for k in ks:
        metrics[f"all_core_at_{k}"] = solved[k] / n
        metrics[f"mean_core_recall_at_{k}"] = core_recall_sum[k] / n
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--train-out", type=Path, required=True)
    parser.add_argument("--eval-out", type=Path, required=True)
    parser.add_argument("--model-out", type=Path, required=True)
    parser.add_argument("--split-index", type=int, default=1500)
    parser.add_argument("--limit-goals", type=int, default=None)
    args = parser.parse_args()

    goals = load_goals_jsonl(args.input)
    if args.limit_goals is not None:
        goals = goals[: args.limit_goals]
    train_goals = goals[: args.split_index]
    eval_goals = goals[args.split_index :]
    if not train_goals or not eval_goals:
        raise ValueError("both train and eval splits must be non-empty")

    x_train, y_train, _ = make_matrix(train_goals)
    model, model_json, train_scores = fit_model(x_train, y_train)
    scored_train = add_learned_scores(train_goals, model)
    scored_eval = add_learned_scores(eval_goals, model)
    write_goals_jsonl(scored_train, args.train_out)
    write_goals_jsonl(scored_eval, args.eval_out)

    model_json.update(
        {
            "input": str(args.input),
            "train_goals": len(train_goals),
            "eval_goals": len(eval_goals),
            "train_candidates": len(x_train),
            "train_positive_candidates": int(sum(y_train)),
            "train_positive_rate": float(sum(y_train) / max(len(y_train), 1)),
            "train_score_min": float(min(train_scores)),
            "train_score_max": float(max(train_scores)),
            "eval_metrics": {
                "base_score": ranking_metrics(scored_eval, "base_score"),
                "learned_score": ranking_metrics(scored_eval, "learned_score"),
            },
        }
    )
    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    args.model_out.write_text(json.dumps(model_json, indent=2), encoding="utf-8")
    print(
        f"trained on {len(train_goals)} goals / {len(x_train)} candidates; "
        f"eval {len(eval_goals)} goals; wrote {args.eval_out}"
    )
    print(json.dumps(model_json["eval_metrics"], indent=2))


if __name__ == "__main__":
    main()
