"""Input/output helpers for Phase 1 experiments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from schema import ExperimentResult, Goal, goal_from_dict, to_jsonable


def load_goals_jsonl(path: Path) -> list[Goal]:
    goals: list[Goal] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                goals.append(goal_from_dict(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"failed to parse {path}:{line_no}: {exc}") from exc
    return goals


def write_goals_jsonl(goals: Iterable[Goal], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for goal in goals:
            f.write(json.dumps(to_jsonable(goal), ensure_ascii=False) + "\n")


def write_experiment(result: ExperimentResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(result), indent=2), encoding="utf-8")

