"""Replay original traced Mathlib tactics in Lean for bridge validation.

This script checks whether a traced theorem's original tactic script still
replays in a real Lean process after reconstructing the source-file context up
to the theorem start position. It does not enforce premise restrictions by
itself; policy-specific bridge success is computed as:

    trace-core proof-core recovered AND original tactic replay succeeds.
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
from typing import Any

from data_io import load_goals_jsonl
from schema import Goal


def ensure_lean_tools() -> None:
    elan_bin = Path.home() / ".elan" / "bin"
    if elan_bin.exists():
        os.environ["PATH"] = f"{elan_bin}:{os.environ.get('PATH', '')}"
    if shutil.which("lake") is None:
        raise RuntimeError("lake executable not found; source elan before running")
    if shutil.which("lean") is None:
        raise RuntimeError("lean executable not found; source elan before running")


def prefix_before_theorem(source: str, start: list[int]) -> str:
    line_no = int(start[0])
    col_no = int(start[1])
    lines = source.splitlines()
    before = lines[: max(0, line_no - 1)]
    if 1 <= line_no <= len(lines) and col_no > 1:
        before.append(lines[line_no - 1][: col_no - 1])
    return "\n".join(before).rstrip() + "\n\n"


def theorem_replay_block(goal: Goal) -> str:
    statement = goal.goal_state.rstrip()
    lines = [statement]
    stripped = statement.strip()
    if stripped.endswith(":="):
        lines.append("by")
    elif not stripped.endswith("by"):
        lines.append(":= by")

    for tactic in goal.metadata.get("tactic_script", []):
        for line in str(tactic).splitlines():
            lines.append(f"  {line}" if line.strip() else "")
    return "\n".join(lines).rstrip() + "\n"


def build_replay_text(goal: Goal, repo_root: Path) -> str:
    file_path = repo_root / str(goal.metadata["file_path"])
    source = file_path.read_text(encoding="utf-8")
    prefix = prefix_before_theorem(source, list(goal.metadata["start"]))
    return prefix + "\n" + theorem_replay_block(goal)


def replay_goal(
    goal: Goal,
    *,
    repo_root: Path,
    timeout_s: float,
    save_dir: Path | None,
) -> dict[str, Any]:
    start = time.perf_counter()
    theorem = str(goal.metadata.get("theorem", goal.goal_id))
    category = str(goal.metadata.get("bridge_category", "unknown"))

    try:
        lean_text = build_replay_text(goal, repo_root)
    except Exception as exc:
        return {
            "goal_id": goal.goal_id,
            "theorem": theorem,
            "category": category,
            "success": False,
            "status": "build_replay_file_failed",
            "time_s": time.perf_counter() - start,
            "error": repr(exc),
        }

    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
        safe_name = theorem.replace(".", "__").replace("/", "_")
        lean_file = save_dir / f"{safe_name}.lean"
        lean_file.write_text(lean_text, encoding="utf-8")
        cleanup = False
    else:
        tmp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".lean", delete=False)
        tmp.write(lean_text)
        tmp.close()
        lean_file = Path(tmp.name)
        cleanup = True

    try:
        proc = subprocess.run(
            ["lake", "env", "lean", str(lean_file)],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_s,
        )
        elapsed = time.perf_counter() - start
        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        return {
            "goal_id": goal.goal_id,
            "theorem": theorem,
            "file_path": goal.metadata.get("file_path"),
            "category": category,
            "success": proc.returncode == 0,
            "status": "verified" if proc.returncode == 0 else "lean_error",
            "returncode": proc.returncode,
            "time_s": elapsed,
            "lean_file": str(lean_file) if save_dir is not None else None,
            "output_tail": output[-3000:],
        }
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - start
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return {
            "goal_id": goal.goal_id,
            "theorem": theorem,
            "file_path": goal.metadata.get("file_path"),
            "category": category,
            "success": False,
            "status": "timeout",
            "time_s": elapsed,
            "lean_file": str(lean_file) if save_dir is not None else None,
            "output_tail": output[-3000:],
        }
    finally:
        if cleanup:
            try:
                lean_file.unlink()
            except OSError:
                pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--max-goals", type=int, default=None)
    parser.add_argument("--save-dir", type=Path, default=None)
    args = parser.parse_args()

    ensure_lean_tools()
    goals = load_goals_jsonl(args.goals)
    if args.max_goals is not None:
        goals = goals[: args.max_goals]
    if not goals:
        raise ValueError("no goals to replay")
    if args.save_dir is not None:
        args.save_dir = args.save_dir.resolve()

    repo_root = args.repo_root
    if repo_root is None:
        repo_root = Path(str(goals[0].metadata["repo_url"]))
    repo_root = repo_root.resolve()

    results = []
    for idx, goal in enumerate(goals, start=1):
        result = replay_goal(
            goal,
            repo_root=repo_root,
            timeout_s=args.timeout_s,
            save_dir=args.save_dir,
        )
        results.append(result)
        print(
            f"[{idx}/{len(goals)}] {result['status']} {result['theorem']} "
            f"{result['time_s']:.2f}s",
            flush=True,
        )

    payload = {
        "goals": str(args.goals),
        "repo_root": str(repo_root),
        "timeout_s": args.timeout_s,
        "n_goals": len(goals),
        "n_success": sum(1 for r in results if r["success"]),
        "results": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
