"""Retriever-visible premise features for Phase 1 Mathlib experiments."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from schema import Goal, Premise


_SEGMENT_RE = re.compile(r"[._\s\[\]\(\){}:,+\-*/=<>]+")
_CAMEL_RE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")
_DECL_KINDS = (
    "theorem",
    "lemma",
    "def",
    "abbrev",
    "instance",
    "class",
    "structure",
    "inductive",
)
_DECL_KIND_RE = {kind: re.compile(rf"\b{kind}\b") for kind in _DECL_KINDS}


def lean_name_tokens(text: str) -> set[str]:
    """Split Lean names and statements into stable, retriever-visible tokens."""
    tokens: list[str] = []
    for segment in _SEGMENT_RE.split(text or ""):
        if not segment:
            continue
        parts = [m.group(0).lower() for m in _CAMEL_RE.finditer(segment)]
        tokens.extend(parts or [segment.lower()])
    return {tok for tok in tokens if len(tok) > 1 or tok.isdigit()}


def namespace_prefix_len(a: str, b: str) -> int:
    a_parts = (a or "").split(".")
    b_parts = (b or "").split(".")
    n = 0
    for x, y in zip(a_parts, b_parts):
        if x != y:
            break
        n += 1
    return n


def declaration_kind(code: str) -> str:
    head = (code or "")[:220].lower()
    for kind, pattern in _DECL_KIND_RE.items():
        if pattern.search(head):
            return kind
    return "unknown"


def build_candidate_features(
    *,
    theorem_name: str,
    goal_state: str,
    premise_name: str,
    premise_text: str,
    same_file: bool = True,
) -> dict[str, Any]:
    theorem_tokens = lean_name_tokens(theorem_name)
    theorem_leaf_tokens = lean_name_tokens((theorem_name or "").split(".")[-1])
    statement_tokens = lean_name_tokens(goal_state)
    premise_name_tokens = lean_name_tokens(premise_name)
    premise_text_tokens = lean_name_tokens((premise_text or "")[:1200])
    premise_all_tokens = premise_name_tokens | premise_text_tokens
    kind = declaration_kind(premise_text)

    return {
        "same_file": bool(same_file),
        "decl_kind": kind,
        "is_def_like": kind in {"def", "abbrev"},
        "is_theorem_like": kind in {"theorem", "lemma"},
        "has_simp_attr": "@[simp" in (premise_text or "")[:260]
        or "(attr := simp)" in (premise_text or "")[:260],
        "namespace_prefix_len": namespace_prefix_len(theorem_name, premise_name),
        "name_depth": premise_name.count("."),
        "name_token_overlap": len(theorem_tokens & premise_name_tokens),
        "leaf_token_overlap": len(theorem_leaf_tokens & premise_name_tokens),
        "statement_token_overlap": len(statement_tokens & premise_all_tokens),
        "text_length": len(premise_text or ""),
    }


def features_for_premise(goal: Goal, premise: Premise) -> dict[str, Any]:
    if premise.features:
        return premise.features
    theorem_name = str(goal.metadata.get("theorem", goal.goal_id))
    return build_candidate_features(
        theorem_name=theorem_name,
        goal_state=goal.goal_state,
        premise_name=premise.name,
        premise_text=premise.text,
        same_file=True,
    )


def goal_query_tokens(goal: Goal, *, variant: str = "all") -> list[str]:
    theorem_name = str(goal.metadata.get("theorem", goal.goal_id))
    if variant == "name":
        text = theorem_name
    elif variant == "statement":
        text = goal.goal_state
    else:
        text = f"{theorem_name} {goal.goal_state}"
    return sorted(lean_name_tokens(text))


def premise_bm25_terms(premise: Premise, *, variant: str = "all") -> list[str]:
    if variant == "name":
        text = premise.name
    elif variant == "statement":
        text = premise.text
    else:
        text = f"{premise.name} {premise.text}"
    tokens = lean_name_tokens(text)
    name_tokens = lean_name_tokens(premise.name)
    # Premise names are high-signal in Lean retrieval, so count them twice.
    return sorted(tokens | name_tokens) + sorted(name_tokens)


def bm25_scores(goal: Goal, *, query_variant: str = "all", doc_variant: str = "all") -> dict[str, float]:
    query_terms = goal_query_tokens(goal, variant=query_variant)
    if not query_terms:
        return {p.name: float(p.base_score) for p in goal.candidates}

    doc_terms = {p.name: premise_bm25_terms(p, variant=doc_variant) for p in goal.candidates}
    n_docs = max(1, len(doc_terms))
    avg_len = sum(len(terms) for terms in doc_terms.values()) / n_docs
    avg_len = max(avg_len, 1.0)

    df = Counter()
    for terms in doc_terms.values():
        for term in set(terms):
            df[term] += 1

    k1 = 1.2
    b = 0.75
    scores: dict[str, float] = {}
    for p in goal.candidates:
        terms = doc_terms[p.name]
        counts = Counter(terms)
        dl = max(len(terms), 1)
        score = 0.0
        for term in query_terms:
            tf = counts.get(term, 0)
            if not tf:
                continue
            idf = math.log(1.0 + (n_docs - df[term] + 0.5) / (df[term] + 0.5))
            denom = tf + k1 * (1.0 - b + b * dl / avg_len)
            score += idf * (tf * (k1 + 1.0)) / denom
        scores[p.name] = score
    return scores


def bm25_rank(
    goal: Goal,
    *,
    query_variant: str = "all",
    doc_variant: str = "all",
    same_file_prior: float = 0.0,
    exclude: set[str] | None = None,
) -> list[Premise]:
    exclude = exclude or set()
    bm25 = bm25_scores(goal, query_variant=query_variant, doc_variant=doc_variant)

    def score(p: Premise) -> float:
        f = features_for_premise(goal, p)
        s = bm25.get(p.name, 0.0)
        s += 0.10 * float(p.base_score)
        if same_file_prior and bool(f.get("same_file", False)):
            s += same_file_prior
        return s

    return sorted(
        [p for p in goal.candidates if p.name not in exclude],
        key=score,
        reverse=True,
    )


def visible_feature_score(
    goal: Goal,
    premise: Premise,
    *,
    prefer_short: bool = False,
    group: str = "all",
) -> float:
    """Rank by base retrieval score plus non-oracle name/statement features."""
    f = features_for_premise(goal, premise)
    score = float(premise.base_score)

    use_name = group in {"all", "name", "name_statement"}
    use_statement = group in {"all", "statement", "name_statement"}
    use_decl = group in {"all", "decl"}

    if use_name:
        score += 0.12 * min(int(f.get("name_token_overlap", 0)), 8)
        score += 0.15 * min(int(f.get("leaf_token_overlap", 0)), 6)
        score -= 0.02 * min(int(f.get("name_depth", 0)), 5)

    if use_statement:
        score += 0.015 * min(int(f.get("statement_token_overlap", 0)), 20)

    if use_decl:
        kind = str(f.get("decl_kind", "unknown"))
        score -= 0.00005 * min(int(f.get("text_length", 0)), 2000)
        if kind in {"def", "abbrev"} or bool(f.get("is_def_like", False)):
            score += 0.04
        if kind in {"lemma", "theorem"} or bool(f.get("is_theorem_like", False)):
            score -= 0.03
        if bool(f.get("has_simp_attr", False)):
            score += 0.015

    if prefer_short:
        score -= 0.00008 * min(int(f.get("text_length", 0)), 2000)
        score -= 0.006 * min(int(f.get("name_depth", 0)), 5)
    return score
