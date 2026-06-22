"""Trace-grounded proof-core oracle for Phase 1 Mathlib experiments.

This is not a Lean proof reconstruction backend. It evaluates whether a policy
recovers the premise core observed in a LeanDojo trace and emits failure types
that the FAR controller can react to.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from provers.trace_core import TraceCoreProver
from schema import goal_from_dict, premise_from_dict, to_jsonable


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--response", required=True)
    args = parser.parse_args()

    req = json.loads(Path(args.request).read_text(encoding="utf-8-sig"))
    goal = goal_from_dict(req["goal"])
    premises = [premise_from_dict(p) for p in req.get("premises", [])]
    result = TraceCoreProver().prove(goal, premises, timeout_s=float(req.get("timeout_s", 10.0)))

    Path(args.response).write_text(json.dumps(to_jsonable(result), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
