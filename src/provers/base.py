"""Prover interfaces."""

from __future__ import annotations

from typing import Protocol

from schema import Goal, Premise, ProverResult


class BaseProver(Protocol):
    name: str

    def prove(self, goal: Goal, premises: list[Premise], *, timeout_s: float) -> ProverResult:
        ...

