"""Rule-based Phase 1 FAR controller and baselines."""

from __future__ import annotations

import random
from dataclasses import dataclass

from feature_extraction import bm25_rank, features_for_premise, visible_feature_score
from schema import FailureTrace, Goal, Premise

SECOND_STAGE_FAILURE_TYPES = (
    "imported_premise_missing",
    "missing_bridge",
    "type_mismatch",
    "rewrite_direction",
    "typeclass_missing",
    "local_context_missing",
    "reconstruction_failure",
)


def rank_by_base(goal: Goal, *, exclude: set[str] | None = None) -> list[Premise]:
    exclude = exclude or set()
    return [
        p
        for p in sorted(goal.candidates, key=lambda x: x.base_score, reverse=True)
        if p.name not in exclude
    ]


def visible_premise_score(
    goal: Goal,
    premise: Premise,
    *,
    prefer_short: bool = False,
    group: str = "all",
) -> float:
    return visible_feature_score(goal, premise, prefer_short=prefer_short, group=group)


@dataclass
class PolicyState:
    tried: set[str]
    last_failure: FailureTrace | None = None
    attempt_id: int = 0


class Phase1Policy:
    def __init__(self, name: str, *, seed: int = 0) -> None:
        self.name = name
        self.rng = random.Random(seed)

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        raise NotImplementedError


class OneShotPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("one_shot")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        if state.tried:
            return []
        return rank_by_base(goal)[:k]


class TopKExpansionPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("topk_expansion")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        return rank_by_base(goal)[: k * (state.attempt_id + 1)]


class TopKEqualBudgetPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("topk_equal_budget")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        if state.tried:
            return []
        return rank_by_base(goal)[: max(k, int(round(1.75 * k)))]


class VisibleFeatureRerankPolicy(Phase1Policy):
    def __init__(self, *, group: str = "all", name: str = "visible_feature_rerank") -> None:
        super().__init__(name)
        self.group = group

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        if state.tried:
            return []
        effective_k = max(k, int(round(1.75 * k)))
        return sorted(
            goal.candidates,
            key=lambda p: visible_premise_score(goal, p, group=self.group),
            reverse=True,
        )[:effective_k]


def rank_by_same_file_prior(goal: Goal) -> list[Premise]:
    def score(p: Premise) -> float:
        f = features_for_premise(goal, p)
        s = visible_premise_score(goal, p)
        if bool(f.get("same_file", False)):
            s += 0.35
        return s

    return sorted(goal.candidates, key=score, reverse=True)


def learned_premise_score(
    goal: Goal,
    premise: Premise,
    *,
    imported_prior: float = 0.0,
    visible_mix: float = 0.0,
) -> float:
    f = features_for_premise(goal, premise)
    score = float(f.get("learned_score", premise.base_score))
    if imported_prior:
        score += imported_prior if not bool(f.get("same_file", False)) else -imported_prior
    if visible_mix:
        score += visible_mix * visible_premise_score(goal, premise)
    return score


def rank_by_learned(
    goal: Goal,
    *,
    imported_prior: float = 0.0,
    visible_mix: float = 0.0,
) -> list[Premise]:
    return sorted(
        goal.candidates,
        key=lambda p: learned_premise_score(goal, p, imported_prior=imported_prior, visible_mix=visible_mix),
        reverse=True,
    )


def rank_by_learned_then_base(goal: Goal, *, learned_k: int, base_k: int, budget: int = 96) -> list[Premise]:
    selected: list[Premise] = []
    seen: set[str] = set()
    for pool in (rank_by_learned(goal)[:learned_k], rank_by_base(goal)[:base_k]):
        for premise in pool:
            if premise.name in seen:
                continue
            selected.append(premise)
            seen.add(premise.name)
            if len(selected) >= budget:
                return selected
    return selected


def rank_by_second_stage(goal: Goal, failure_type: str) -> list[Premise]:
    key = f"second_stage_score_{failure_type}"
    return sorted(
        goal.candidates,
        key=lambda p: float(features_for_premise(goal, p).get(key, features_for_premise(goal, p).get("learned_score", p.base_score))),
        reverse=True,
    )


def rank_by_second_stage_base_mix(goal: Goal, failure_type: str, *, base_alpha: float) -> list[Premise]:
    key = f"second_stage_score_{failure_type}"

    def score(p: Premise) -> float:
        f = features_for_premise(goal, p)
        second_stage_score = float(f.get(key, f.get("learned_score", p.base_score)))
        return second_stage_score + base_alpha * float(p.base_score)

    return sorted(goal.candidates, key=score, reverse=True)


def rank_by_second_stage_expert_max(
    goal: Goal,
    *,
    failure_types: list[str],
    penalties: dict[str, float] | None = None,
) -> list[Premise]:
    penalties = penalties or {}

    def score(p: Premise) -> float:
        f = features_for_premise(goal, p)
        fallback = float(f.get("learned_score", p.base_score))
        values = []
        for failure_type in failure_types:
            key = f"second_stage_score_{failure_type}"
            values.append(float(f.get(key, fallback)) - float(penalties.get(failure_type, 0.0)))
        return max(values) if values else fallback

    return sorted(goal.candidates, key=score, reverse=True)


def keep_tried_then_rank(goal: Goal, *, tried: set[str], ranked: list[Premise], target: int) -> list[Premise]:
    selected: list[Premise] = []
    seen: set[str] = set()
    for premise in goal.candidates:
        if premise.name in tried:
            selected.append(premise)
            seen.add(premise.name)
    for premise in ranked:
        if premise.name in seen:
            continue
        selected.append(premise)
        seen.add(premise.name)
        if len(seen) >= target:
            break
    return selected


def keep_tried_then_pools(
    goal: Goal,
    *,
    tried: set[str],
    pools: list[list[Premise]],
    target: int,
) -> list[Premise]:
    selected: list[Premise] = []
    seen: set[str] = set()
    for premise in goal.candidates:
        if premise.name in tried:
            selected.append(premise)
            seen.add(premise.name)
    for pool in pools:
        for premise in pool:
            if premise.name in seen:
                continue
            selected.append(premise)
            seen.add(premise.name)
            if len(seen) >= target:
                return selected
    return selected


class BM25RerankPolicy(Phase1Policy):
    def __init__(self, *, name: str = "bm25_rerank", same_file_prior: float = 0.0) -> None:
        super().__init__(name)
        self.same_file_prior = same_file_prior

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        if state.tried:
            return []
        effective_k = max(k, int(round(1.75 * k)))
        return bm25_rank(goal, same_file_prior=self.same_file_prior)[:effective_k]


class BM25ExpansionPolicy(Phase1Policy):
    def __init__(self, *, name: str = "bm25_expansion", same_file_prior: float = 0.0) -> None:
        super().__init__(name)
        self.same_file_prior = same_file_prior

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        effective_k = min(k * (state.attempt_id + 1), 96)
        return bm25_rank(goal, same_file_prior=self.same_file_prior)[:effective_k]


class SameFilePriorRerankPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("same_file_prior_rerank")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        if state.tried:
            return []
        effective_k = max(k, int(round(1.75 * k)))
        return rank_by_same_file_prior(goal)[:effective_k]


class SameFilePriorExpansionPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("same_file_prior_expansion")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        effective_k = min(k * (state.attempt_id + 1), 96)
        return rank_by_same_file_prior(goal)[:effective_k]


class LearnedRerankPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("learned_rerank")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        if state.tried:
            return []
        effective_k = max(k, int(round(1.75 * k)))
        return rank_by_learned(goal)[:effective_k]


class LearnedExpansionPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("learned_expansion")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        effective_k = min(k * (state.attempt_id + 1), 96)
        return rank_by_learned(goal)[:effective_k]


class LearnedBaseFallbackPolicy(Phase1Policy):
    """Strong failure-agnostic learned retriever with base-score fallback."""

    def __init__(self) -> None:
        super().__init__("learned_base_fallback")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        if state.attempt_id == 0:
            return rank_by_learned(goal)[:k]
        if state.attempt_id == 1:
            return rank_by_learned_then_base(goal, learned_k=56, base_k=24)
        return rank_by_learned_then_base(goal, learned_k=80, base_k=32)


class LeanSearchIterativePolicy(Phase1Policy):
    """Failure-agnostic iterative lexical retrieval baseline.

    This is intentionally stronger than a single static rerank: retries change
    query views and keep previous candidates in the current prover call, but the
    policy still cannot condition on parsed failure type.
    """

    def __init__(self) -> None:
        super().__init__("leansearch_iterative")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        target = min(k * (state.attempt_id + 1), 96)
        if state.attempt_id == 0:
            rank = bm25_rank(goal)
        elif state.attempt_id == 1:
            rank = bm25_rank(goal, query_variant="statement", same_file_prior=0.15)
        else:
            rank = rank_by_same_file_prior(goal)

        selected: list[Premise] = []
        seen: set[str] = set()
        for p in goal.candidates:
            if p.name in state.tried:
                selected.append(p)
                seen.add(p.name)
        for p in rank:
            if p.name in seen:
                continue
            selected.append(p)
            seen.add(p.name)
            if len(seen) >= target:
                break
        return selected


class RandomRetryPolicy(Phase1Policy):
    def __init__(self, *, seed: int = 0) -> None:
        super().__init__("random_retry", seed=seed)

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        pool = [p for p in goal.candidates if p.name not in state.tried]
        self.rng.shuffle(pool)
        return pool[:k]


class HistoryOnlyPolicy(Phase1Policy):
    def __init__(self) -> None:
        super().__init__("history_only")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        # A history-only baseline may know what it already tried, but it must
        # not use failure type or oracle-style candidate tags.
        return rank_by_base(goal, exclude=state.tried)[:k]


class RuleFarPolicy(Phase1Policy):
    """Failure-type-only controller for Phase 1.

    It implements the paper hypothesis in a transparent way:
    - timeout: shrink and avoid broad/noisy premises;
    - local missing: boost local premises;
    - reconstruction failure: avoid reconstruction-hostile premises;
    - missing bridge/type mismatch: boost bridge/type-compatible tags.
    """

    def __init__(self) -> None:
        super().__init__("rule_far")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_base(goal)[:k]

        pool = list(goal.candidates)

        def score(p: Premise) -> float:
            s = p.base_score
            if failure_type == "timeout":
                if p.has("noise"):
                    s -= 2.0
                if p.has("broad"):
                    s -= 2.5
                if p.has("precise"):
                    s += 0.5
            elif failure_type == "local_context_missing":
                if p.has("local"):
                    s += 3.0
                if p.has("bridge"):
                    s += 1.0
            elif failure_type == "reconstruction_failure":
                if p.has("reconstruction_hostile"):
                    s -= 3.0
                if p.has("lean_friendly"):
                    s += 1.5
            elif failure_type in {"missing_bridge", "type_mismatch"}:
                if p.has("bridge"):
                    s += 1.7
                if p.has("type_compatible"):
                    s += 1.0
            elif failure_type in {"rewrite_direction", "typeclass_missing"}:
                if p.has("rewrite") or p.has("typeclass"):
                    s += 1.5
            elif failure_type == "imported_premise_missing":
                if p.has("imported_core"):
                    s += 2.0
                if p.has("same_file"):
                    s -= 0.3
            else:
                if p.has("noise") or p.has("broad"):
                    s -= 0.2
            return s

        # Shrink after timeout by selecting a smaller, higher-precision batch.
        # Other failure modes keep a full set so previously useful premises can
        # remain available while the controller swaps in the missing bridge.
        effective_k = (
            max(8, k // 2)
            if failure_type == "timeout"
            else min(k * (state.attempt_id + 1), 96)
        )
        ranked = sorted(pool, key=score, reverse=True)
        return ranked[:effective_k]


class RuleFarNoCoreTagsPolicy(Phase1Policy):
    """Less-oracle FAR using failure type plus retriever-visible features."""

    def __init__(
        self,
        *,
        group: str = "all",
        name: str = "rule_far_no_core_tags",
        timeout_action: str = "expand",
    ) -> None:
        super().__init__(name)
        self.group = group
        self.timeout_action = timeout_action

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_base(goal)[:k]

        if failure_type == "timeout":
            effective_k = max(8, k // 2) if self.timeout_action == "shrink" else min(max(2 * k, k), 96)
            return sorted(
                goal.candidates,
                key=lambda p: visible_premise_score(goal, p, prefer_short=True, group=self.group),
                reverse=True,
            )[:effective_k]

        if failure_type == "imported_premise_missing":
            effective_k = min(k * (state.attempt_id + 1), 96)

            def imported_score(p: Premise) -> float:
                f = features_for_premise(goal, p)
                s = visible_premise_score(goal, p, group=self.group)
                s += 0.30 if not bool(f.get("same_file", False)) else -0.20
                return s

            return sorted(goal.candidates, key=imported_score, reverse=True)[:effective_k]

        if failure_type in {
            "missing_bridge",
            "type_mismatch",
            "rewrite_direction",
            "typeclass_missing",
            "local_context_missing",
            "reconstruction_failure",
            "imported_premise_missing",
        }:
            effective_k = min(k * (state.attempt_id + 1), 96)
        else:
            effective_k = k

        return sorted(
            goal.candidates,
            key=lambda p: visible_premise_score(goal, p, group=self.group),
            reverse=True,
        )[:effective_k]


class RuleFarFailureTypeOnlyPolicy(Phase1Policy):
    """FAR ablation using failure type only, with no candidate-side features."""

    def __init__(self) -> None:
        super().__init__("rule_far_failure_type_only")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_base(goal)[:k]
        if failure_type == "timeout":
            return rank_by_base(goal)[: max(8, k // 2)]
        if failure_type in {
            "missing_bridge",
            "type_mismatch",
            "rewrite_direction",
            "typeclass_missing",
            "local_context_missing",
            "reconstruction_failure",
            "imported_premise_missing",
        }:
            return rank_by_base(goal)[: min(k * (state.attempt_id + 1), 96)]
        return rank_by_base(goal)[:k]


class RuleFarBM25Policy(Phase1Policy):
    """Failure-aware wrapper around a strong lexical/global retriever."""

    def __init__(self) -> None:
        super().__init__("rule_far_bm25")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return bm25_rank(goal, same_file_prior=0.15)[:k]
        if failure_type == "timeout":
            return bm25_rank(goal, same_file_prior=0.0)[: max(8, k // 2)]
        effective_k = min(k * (state.attempt_id + 1), 96)
        if failure_type == "imported_premise_missing":
            return bm25_rank(goal, same_file_prior=-0.35)[:effective_k]
        if failure_type in {
            "missing_bridge",
            "type_mismatch",
            "rewrite_direction",
            "typeclass_missing",
            "local_context_missing",
            "reconstruction_failure",
        }:
            return bm25_rank(goal, same_file_prior=0.15)[:effective_k]
        return bm25_rank(goal, same_file_prior=0.0)[:effective_k]


class RuleFarLearnedPolicy(Phase1Policy):
    """Failure-aware wrapper around a supervised global premise scorer."""

    def __init__(self) -> None:
        super().__init__("rule_far_learned")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        effective_k = min(k * (state.attempt_id + 1), 96)
        if failure_type == "imported_premise_missing":
            return rank_by_learned(goal, imported_prior=0.10)[:effective_k]
        if failure_type in {
            "missing_bridge",
            "type_mismatch",
            "rewrite_direction",
            "typeclass_missing",
            "local_context_missing",
            "reconstruction_failure",
        }:
            return rank_by_learned(goal, visible_mix=0.05)[:effective_k]
        return rank_by_learned(goal)[:effective_k]


class RuleFarLearnedFailureSpecificPolicy(Phase1Policy):
    """Failure-aware learned controller with non-oracle fallback features."""

    def __init__(self) -> None:
        super().__init__("rule_far_learned_failure_specific")

    def _bridge_rank(self, goal: Goal, *, learned_k: int, base_k: int, budget: int = 96) -> list[Premise]:
        # Base score is the strongest non-oracle fallback for missed learned
        # cores in the imported-core heldout set; visible mix breaks ties toward
        # theorem/statement-compatible candidates.
        learned_pool = sorted(
            goal.candidates,
            key=lambda p: learned_premise_score(goal, p, visible_mix=0.04),
            reverse=True,
        )[:learned_k]
        selected: list[Premise] = []
        seen: set[str] = set()
        for pool in (learned_pool, rank_by_base(goal)[:base_k]):
            for premise in pool:
                if premise.name in seen:
                    continue
                selected.append(premise)
                seen.add(premise.name)
                if len(selected) >= budget:
                    return selected
        return selected

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        if state.attempt_id == 1:
            if failure_type == "imported_premise_missing":
                return rank_by_learned_then_base(goal, learned_k=56, base_k=24)
            return self._bridge_rank(goal, learned_k=56, base_k=16)

        if failure_type == "imported_premise_missing":
            return rank_by_learned_then_base(goal, learned_k=80, base_k=32)
        if failure_type in {
            "missing_bridge",
            "type_mismatch",
            "rewrite_direction",
            "typeclass_missing",
            "local_context_missing",
            "reconstruction_failure",
        }:
            return self._bridge_rank(goal, learned_k=80, base_k=32)
        return rank_by_learned_then_base(goal, learned_k=80, base_k=32)


class RuleFarLearnedSecondStagePolicy(Phase1Policy):
    """Failure-conditioned controller using trained second-stage scores."""

    def __init__(self) -> None:
        super().__init__("rule_far_learned_second_stage")

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        second_stage_rank = rank_by_second_stage(goal, failure_type)
        return keep_tried_then_rank(goal, tried=state.tried, ranked=second_stage_rank, target=target)


class RuleFarLearnedSecondStageFixedFailurePolicy(Phase1Policy):
    """Negative control that ignores the observed failure type after attempt 0."""

    def __init__(self, *, name: str, fixed_failure_type: str) -> None:
        super().__init__(name)
        self.fixed_failure_type = fixed_failure_type

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        observed_failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if observed_failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if observed_failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        ranked = rank_by_second_stage(goal, self.fixed_failure_type)
        return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)


class RuleFarLearnedSecondStageCyclicFailurePolicy(Phase1Policy):
    """Negative control that uses deterministic non-observed failure-type scores."""

    def __init__(self, *, name: str = "rule_far_learned_second_stage_cyclic") -> None:
        super().__init__(name)

    def _surrogate_failure_type(self, observed_failure_type: str, attempt_id: int) -> str:
        if observed_failure_type not in SECOND_STAGE_FAILURE_TYPES:
            return SECOND_STAGE_FAILURE_TYPES[0]
        idx = SECOND_STAGE_FAILURE_TYPES.index(observed_failure_type)
        return SECOND_STAGE_FAILURE_TYPES[(idx + attempt_id) % len(SECOND_STAGE_FAILURE_TYPES)]

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        observed_failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if observed_failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if observed_failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        surrogate_failure_type = self._surrogate_failure_type(observed_failure_type, state.attempt_id)
        ranked = rank_by_second_stage(goal, surrogate_failure_type)
        return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)


class RuleFarLearnedSecondStageShuffledFailurePolicy(Phase1Policy):
    """Seeded negative control that samples a failure-type score independent of the trace."""

    def __init__(self, *, seed: int, name: str = "rule_far_learned_second_stage_shuffled") -> None:
        super().__init__(name, seed=seed)

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        observed_failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if observed_failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if observed_failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        surrogate_failure_type = self.rng.choice(SECOND_STAGE_FAILURE_TYPES)
        ranked = rank_by_second_stage(goal, surrogate_failure_type)
        return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)


class RuleFarLearnedSecondStageBaseGuardrailPolicy(Phase1Policy):
    """Second-stage controller with a small high-base fallback guardrail."""

    def __init__(
        self,
        *,
        name: str = "rule_far_learned_second_stage_base_guardrail",
        imported_base_k: tuple[int, int] = (16, 32),
        other_base_k: tuple[int, int] = (8, 16),
        final_only: bool = False,
    ) -> None:
        super().__init__(name)
        self.imported_base_k = imported_base_k
        self.other_base_k = other_base_k
        self.final_only = final_only

    def _base_guardrail_k(self, failure_type: str, attempt_id: int) -> int:
        idx = 0 if attempt_id == 1 else 1
        if failure_type == "imported_premise_missing":
            return self.imported_base_k[idx]
        return self.other_base_k[idx]

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        if self.final_only and state.attempt_id == 1:
            second_stage_rank = rank_by_second_stage(goal, failure_type)
            return keep_tried_then_rank(goal, tried=state.tried, ranked=second_stage_rank, target=target)

        guardrail_k = self._base_guardrail_k(failure_type, state.attempt_id)
        base_guardrail = rank_by_base(goal)[:guardrail_k]
        second_stage_rank = rank_by_second_stage(goal, failure_type)
        return keep_tried_then_pools(
            goal,
            tried=state.tried,
            pools=[base_guardrail, second_stage_rank],
            target=target,
        )


class RuleFarLearnedSecondStageBaseMixPolicy(Phase1Policy):
    """Second-stage controller with a soft base-score prior."""

    def __init__(
        self,
        *,
        name: str,
        imported_base_alpha: float,
        other_base_alpha: float = 0.0,
    ) -> None:
        super().__init__(name)
        self.imported_base_alpha = imported_base_alpha
        self.other_base_alpha = other_base_alpha

    def _alpha(self, failure_type: str) -> float:
        if failure_type == "imported_premise_missing":
            return self.imported_base_alpha
        return self.other_base_alpha

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        alpha = self._alpha(failure_type)
        if alpha <= 0.0:
            ranked = rank_by_second_stage(goal, failure_type)
        else:
            ranked = rank_by_second_stage_base_mix(goal, failure_type, base_alpha=alpha)
        return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)


class RuleFarLearnedSecondStageMultiExpertPolicy(Phase1Policy):
    """Second-stage controller that treats imported failures as coarse signals."""

    def __init__(
        self,
        *,
        name: str,
        imported_experts: list[str],
        penalties: dict[str, float] | None = None,
        final_only: bool = False,
    ) -> None:
        super().__init__(name)
        self.imported_experts = imported_experts
        self.penalties = penalties or {}
        self.final_only = final_only

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        if self.final_only and state.attempt_id == 1:
            ranked = rank_by_second_stage(goal, failure_type)
            return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)

        if failure_type == "imported_premise_missing":
            ranked = rank_by_second_stage_expert_max(
                goal,
                failure_types=self.imported_experts,
                penalties=self.penalties,
            )
        else:
            ranked = rank_by_second_stage(goal, failure_type)
        return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)


class RuleFarLearnedSecondStageFinalExpertGuardrailPolicy(Phase1Policy):
    """Final retry guardrail from neighboring failure experts."""

    def __init__(self, *, name: str, expert_k: int) -> None:
        super().__init__(name)
        self.expert_k = expert_k

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        if state.attempt_id == 1 or failure_type != "imported_premise_missing":
            ranked = rank_by_second_stage(goal, failure_type)
            return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)

        bridge_pool = rank_by_second_stage(goal, "missing_bridge")[: self.expert_k]
        type_pool = rank_by_second_stage(goal, "type_mismatch")[: self.expert_k]
        imported_rank = rank_by_second_stage(goal, failure_type)
        return keep_tried_then_pools(
            goal,
            tried=state.tried,
            pools=[bridge_pool, type_pool, imported_rank],
            target=target,
        )


class RuleFarLearnedSecondStageFinalHybridGuardrailPolicy(Phase1Policy):
    """Final retry guardrail combining high-base and neighboring experts."""

    def __init__(self, *, name: str, base_k: int, expert_k: int) -> None:
        super().__init__(name)
        self.base_k = base_k
        self.expert_k = expert_k

    def select(self, goal: Goal, k: int, state: PolicyState) -> list[Premise]:
        failure_type = state.last_failure.failure_type if state.last_failure else "initial"
        if failure_type == "initial":
            return rank_by_learned(goal)[:k]
        if failure_type == "timeout":
            return rank_by_learned(goal, visible_mix=0.05)[: max(8, k // 2)]

        target = 64 if state.attempt_id == 1 else 96
        if state.attempt_id == 1 or failure_type != "imported_premise_missing":
            ranked = rank_by_second_stage(goal, failure_type)
            return keep_tried_then_rank(goal, tried=state.tried, ranked=ranked, target=target)

        base_pool = rank_by_base(goal)[: self.base_k]
        bridge_pool = rank_by_second_stage(goal, "missing_bridge")[: self.expert_k]
        type_pool = rank_by_second_stage(goal, "type_mismatch")[: self.expert_k]
        imported_rank = rank_by_second_stage(goal, failure_type)
        return keep_tried_then_pools(
            goal,
            tried=state.tried,
            pools=[base_pool, bridge_pool, type_pool, imported_rank],
            target=target,
        )


def make_policy(name: str, *, seed: int = 0) -> Phase1Policy:
    if name == "one_shot":
        return OneShotPolicy()
    if name == "topk_expansion":
        return TopKExpansionPolicy()
    if name == "topk_equal_budget":
        return TopKEqualBudgetPolicy()
    if name == "visible_feature_rerank":
        return VisibleFeatureRerankPolicy()
    if name == "visible_feature_name_rerank":
        return VisibleFeatureRerankPolicy(group="name", name=name)
    if name == "visible_feature_statement_rerank":
        return VisibleFeatureRerankPolicy(group="statement", name=name)
    if name == "visible_feature_decl_rerank":
        return VisibleFeatureRerankPolicy(group="decl", name=name)
    if name == "visible_feature_name_statement_rerank":
        return VisibleFeatureRerankPolicy(group="name_statement", name=name)
    if name == "bm25_rerank":
        return BM25RerankPolicy()
    if name == "bm25_same_file_prior_rerank":
        return BM25RerankPolicy(name=name, same_file_prior=0.35)
    if name == "bm25_expansion":
        return BM25ExpansionPolicy()
    if name == "bm25_same_file_prior_expansion":
        return BM25ExpansionPolicy(name=name, same_file_prior=0.35)
    if name == "same_file_prior_rerank":
        return SameFilePriorRerankPolicy()
    if name == "same_file_prior_expansion":
        return SameFilePriorExpansionPolicy()
    if name == "learned_rerank":
        return LearnedRerankPolicy()
    if name == "learned_expansion":
        return LearnedExpansionPolicy()
    if name == "learned_base_fallback":
        return LearnedBaseFallbackPolicy()
    if name == "leansearch_iterative":
        return LeanSearchIterativePolicy()
    if name == "random_retry":
        return RandomRetryPolicy(seed=seed)
    if name == "history_only":
        return HistoryOnlyPolicy()
    if name in {"rule_far", "rule_far_full"}:
        return RuleFarPolicy()
    if name == "rule_far_no_core_tags":
        return RuleFarNoCoreTagsPolicy()
    if name == "rule_far_no_core_timeout_shrink":
        return RuleFarNoCoreTagsPolicy(name=name, timeout_action="shrink")
    if name == "rule_far_no_core_name_features":
        return RuleFarNoCoreTagsPolicy(group="name", name=name)
    if name == "rule_far_no_core_statement_features":
        return RuleFarNoCoreTagsPolicy(group="statement", name=name)
    if name == "rule_far_no_core_decl_features":
        return RuleFarNoCoreTagsPolicy(group="decl", name=name)
    if name == "rule_far_no_core_name_statement_features":
        return RuleFarNoCoreTagsPolicy(group="name_statement", name=name)
    if name == "rule_far_failure_type_only":
        return RuleFarFailureTypeOnlyPolicy()
    if name == "rule_far_bm25":
        return RuleFarBM25Policy()
    if name == "rule_far_learned":
        return RuleFarLearnedPolicy()
    if name == "rule_far_learned_failure_specific":
        return RuleFarLearnedFailureSpecificPolicy()
    if name == "rule_far_learned_second_stage":
        return RuleFarLearnedSecondStagePolicy()
    fixed_prefix = "rule_far_learned_second_stage_fixed_"
    if name.startswith(fixed_prefix):
        suffix = name[len(fixed_prefix) :]
        aliases = {
            "imported": "imported_premise_missing",
            "bridge": "missing_bridge",
            "type": "type_mismatch",
            "rewrite": "rewrite_direction",
            "typeclass": "typeclass_missing",
            "local": "local_context_missing",
            "reconstruction": "reconstruction_failure",
        }
        failure_type = aliases.get(suffix, suffix)
        if failure_type not in SECOND_STAGE_FAILURE_TYPES:
            raise ValueError(f"unknown fixed second-stage failure type: {suffix}")
        return RuleFarLearnedSecondStageFixedFailurePolicy(
            name=name,
            fixed_failure_type=failure_type,
        )
    if name == "rule_far_learned_second_stage_cyclic":
        return RuleFarLearnedSecondStageCyclicFailurePolicy()
    if name == "rule_far_learned_second_stage_shuffled":
        return RuleFarLearnedSecondStageShuffledFailurePolicy(seed=seed)
    if name == "rule_far_learned_second_stage_base_guardrail":
        return RuleFarLearnedSecondStageBaseGuardrailPolicy()
    if name == "rule_far_learned_second_stage_base_guardrail_small":
        return RuleFarLearnedSecondStageBaseGuardrailPolicy(
            name=name,
            imported_base_k=(8, 16),
            other_base_k=(4, 8),
        )
    if name == "rule_far_learned_second_stage_base_guardrail_wide":
        return RuleFarLearnedSecondStageBaseGuardrailPolicy(
            name=name,
            imported_base_k=(24, 48),
            other_base_k=(12, 24),
        )
    if name == "rule_far_learned_second_stage_final_base_guardrail_8":
        return RuleFarLearnedSecondStageBaseGuardrailPolicy(
            name=name,
            imported_base_k=(0, 8),
            other_base_k=(0, 4),
            final_only=True,
        )
    if name == "rule_far_learned_second_stage_final_base_guardrail_16":
        return RuleFarLearnedSecondStageBaseGuardrailPolicy(
            name=name,
            imported_base_k=(0, 16),
            other_base_k=(0, 8),
            final_only=True,
        )
    if name == "rule_far_learned_second_stage_final_base_guardrail_32":
        return RuleFarLearnedSecondStageBaseGuardrailPolicy(
            name=name,
            imported_base_k=(0, 32),
            other_base_k=(0, 16),
            final_only=True,
        )
    mix_prefix = "rule_far_learned_second_stage_base_mix_"
    if name.startswith(mix_prefix):
        alpha_code = name[len(mix_prefix) :]
        try:
            alpha = int(alpha_code) / 100.0
        except ValueError as exc:
            raise ValueError(f"invalid base-mix alpha policy: {name}") from exc
        return RuleFarLearnedSecondStageBaseMixPolicy(
            name=name,
            imported_base_alpha=alpha,
        )
    if name == "rule_far_learned_second_stage_imported_bt_max":
        return RuleFarLearnedSecondStageMultiExpertPolicy(
            name=name,
            imported_experts=[
                "imported_premise_missing",
                "missing_bridge",
                "type_mismatch",
            ],
        )
    if name == "rule_far_learned_second_stage_imported_bt_penalty050":
        return RuleFarLearnedSecondStageMultiExpertPolicy(
            name=name,
            imported_experts=[
                "imported_premise_missing",
                "missing_bridge",
                "type_mismatch",
            ],
            penalties={
                "missing_bridge": 0.50,
                "type_mismatch": 0.50,
            },
        )
    if name == "rule_far_learned_second_stage_imported_all_penalty050":
        return RuleFarLearnedSecondStageMultiExpertPolicy(
            name=name,
            imported_experts=[
                "imported_premise_missing",
                "missing_bridge",
                "type_mismatch",
                "rewrite_direction",
                "typeclass_missing",
            ],
            penalties={
                "missing_bridge": 0.50,
                "type_mismatch": 0.50,
                "rewrite_direction": 0.50,
                "typeclass_missing": 0.50,
            },
        )
    if name == "rule_far_learned_second_stage_final_imported_bt_max":
        return RuleFarLearnedSecondStageMultiExpertPolicy(
            name=name,
            imported_experts=[
                "imported_premise_missing",
                "missing_bridge",
                "type_mismatch",
            ],
            final_only=True,
        )
    if name == "rule_far_learned_second_stage_final_bt_expert_guardrail_4":
        return RuleFarLearnedSecondStageFinalExpertGuardrailPolicy(name=name, expert_k=4)
    if name == "rule_far_learned_second_stage_final_bt_expert_guardrail_8":
        return RuleFarLearnedSecondStageFinalExpertGuardrailPolicy(name=name, expert_k=8)
    if name == "rule_far_learned_second_stage_final_bt_expert_guardrail_16":
        return RuleFarLearnedSecondStageFinalExpertGuardrailPolicy(name=name, expert_k=16)
    if name == "rule_far_learned_second_stage_final_hybrid_guardrail_b8_e4":
        return RuleFarLearnedSecondStageFinalHybridGuardrailPolicy(name=name, base_k=8, expert_k=4)
    if name == "rule_far_learned_second_stage_final_hybrid_guardrail_b8_e8":
        return RuleFarLearnedSecondStageFinalHybridGuardrailPolicy(name=name, base_k=8, expert_k=8)
    raise ValueError(f"unknown policy: {name}")
