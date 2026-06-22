"""Retriever interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from schema import Goal, Premise


@dataclass
class RetrievalResult:
    premises: list[Premise]
    scores: dict[str, float]


class BaseRetriever(Protocol):
    name: str

    def retrieve(self, goal: Goal, k: int, *, exclude: set[str] | None = None) -> RetrievalResult:
        ...

