"""External Lean prover wrapper for Phase 1 synthetic Lean goals.

This is a real Lean invocation wrapper. It is intentionally minimal: selected
premises are written into a temporary Lean file, followed by the target theorem
and proof script stored in the goal metadata. Success means `lean file.lean`
exits with code 0.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from failure_parser import parse_failure
from schema import goal_from_dict, premise_from_dict, to_jsonable


def ensure_lean_on_path() -> str:
    elan_bin = Path.home() / ".elan" / "bin"
    if elan_bin.exists():
        os.environ["PATH"] = f"{elan_bin}:{os.environ.get('PATH', '')}"
    lean = shutil.which("lean")
    if lean is None:
        raise RuntimeError("lean executable not found; install elan/Lean or source ~/.elan/env")
    return lean


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--response", required=True)
    args = parser.parse_args()

    lean = ensure_lean_on_path()
    req = json.loads(Path(args.request).read_text(encoding="utf-8"))
    goal = goal_from_dict(req["goal"])
    premises = [premise_from_dict(p) for p in req.get("premises", [])]
    candidate_order = {p.name: i for i, p in enumerate(goal.candidates)}
    premises = sorted(premises, key=lambda p: candidate_order.get(p.name, 10**9))
    timeout_s = float(req.get("timeout_s", 10.0))

    imports = goal.metadata.get("imports", [])
    target_signature = goal.metadata["target_signature"]
    proof_script = goal.metadata["proof_script"]

    selected_names = {p.name for p in premises}
    recovered = [p for p in goal.proof_core if p in selected_names]

    lines: list[str] = []
    for imp in imports:
        lines.append(f"import {imp}")
    lines.append("")
    for p in premises:
        if p.text.strip():
            lines.append(p.text.strip())
            lines.append("")
    lines.append(target_signature.rstrip())
    lines.append(":= by")
    for line in proof_script.splitlines():
        lines.append(f"  {line}" if line.strip() else "")
    lean_text = "\n".join(lines) + "\n"

    start = time.perf_counter()
    with tempfile.TemporaryDirectory() as td:
        lean_file = Path(td) / "Attempt.lean"
        lean_file.write_text(lean_text, encoding="utf-8")
        try:
            proc = subprocess.run(
                [lean, str(lean_file)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_s,
            )
            elapsed = time.perf_counter() - start
            output = (proc.stdout or "") + "\n" + (proc.stderr or "")
            if proc.returncode == 0:
                response = {
                    "success": True,
                    "verified": True,
                    "failure": None,
                    "used_premises": list(goal.proof_core),
                    "proof_core_recovered": recovered,
                    "time_s": elapsed,
                    "backend_status": "success",
                    "reconstruction_status": "verified",
                }
            else:
                failure = parse_failure(
                    output,
                    backend="lean_external",
                    backend_status="fail",
                    reconstruction_status="failed" if "unknown identifier" not in output else "not_attempted",
                    unsolved_goals=[goal.goal_state],
                    raw={"returncode": proc.returncode},
                )
                response = {
                    "success": False,
                    "verified": False,
                    "failure": to_jsonable(failure),
                    "used_premises": [],
                    "proof_core_recovered": recovered,
                    "time_s": elapsed,
                    "backend_status": "fail",
                    "reconstruction_status": failure.reconstruction_status,
                }
        except subprocess.TimeoutExpired as exc:
            elapsed = time.perf_counter() - start
            output = (exc.stdout or "") + "\n" + (exc.stderr or "")
            failure = parse_failure(
                output or "timeout",
                backend="lean_external",
                backend_status="timeout",
                reconstruction_status="not_attempted",
                unsolved_goals=[goal.goal_state],
                raw={"timeout_s": timeout_s},
            )
            response = {
                "success": False,
                "verified": False,
                "failure": to_jsonable(failure),
                "used_premises": [],
                "proof_core_recovered": recovered,
                "time_s": elapsed,
                "backend_status": "timeout",
                "reconstruction_status": "not_attempted",
            }

    Path(args.response).write_text(json.dumps(response, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
