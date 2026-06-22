"""Mock retriever for local Phase 1 pipeline tests."""

from __future__ import annotations

from schema import Goal
from retrievers.base import RetrievalResult


class MockRetriever:
    name = "mock_base_score"

    def retrieve(self, goal: Goal, k: int, *, exclude: set[str] | None = None) -> RetrievalResult:
        exclude = exclude or set()
        ranked = sorted(goal.candidates, key=lambda p: p.base_score, reverse=True)
        chosen = [p for p in ranked if p.name not in exclude][:k]
        return RetrievalResult(
            premises=chosen,
            scores={p.name: p.base_score for p in chosen},
        )

