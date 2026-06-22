"""Preflight existing trace-corpus data against the Mathlib 4.30 evaluation repo.

The verified LeanHammer route currently works with Mathlib v4.30.0.  Existing
trace-core datasets were generated from a current Mathlib 4.31 checkout.  This
script checks whether those datasets can plausibly be replayed on the 4.30
route-A stack before we spend time building a full traced-corpus LeanHammer
action grid.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from collections import Counter
from pathlib import Path
from typing import Any


def run_cmd(cmd: list[str], *, cwd: Path, timeout_s: float) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_s,
        )
        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        return {
            "returncode": proc.returncode,
            "success": proc.returncode == 0,
            "time_s": time.perf_counter() - start,
            "stdout": proc.stdout or "",
            "stderr": proc.stderr or "",
            "output_tail": output[-8000:],
        }
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return {
            "returncode": None,
            "success": False,
            "time_s": time.perf_counter() - start,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "output_tail": output[-8000:],
            "timeout": True,
        }


def load_goals(path: Path, limit: int | None) -> list[dict[str, Any]]:
    goals: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            goals.append(json.loads(line))
            if limit is not None and len(goals) >= limit:
                break
    return goals


def clean_decl_name(name: str | None) -> str:
    if not name:
        return ""
    return name.strip()


def module_from_file_path(file_path: str | None) -> str:
    if not file_path:
        return ""
    path = file_path.replace("\\", "/")
    if path.endswith(".lean"):
        path = path[:-5]
    return path.replace("/", ".")


def render_check_file(names: list[str], line_to_name: dict[int, str]) -> str:
    lines = ["import Mathlib", "", "set_option autoImplicit false", ""]
    for name in names:
        line_to_name[len(lines) + 1] = name
        lines.append(f"#check {name}")
    return "\n".join(lines) + "\n"


def parse_missing_names(output: str, line_to_name: dict[int, str]) -> set[str]:
    missing: set[str] = set()
    for match in re.finditer(r":(\d+):\d+: error: .*?(?:Unknown identifier|unknown constant|unexpected identifier)", output):
        line_no = int(match.group(1))
        if line_no in line_to_name:
            missing.add(line_to_name[line_no])
    for match in re.finditer(r"Unknown identifier `([^`]+)`", output):
        missing.add(match.group(1))
    return missing


def write_md(payload: dict[str, Any], out: Path) -> None:
    summary = payload["summary"]
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Trace-Corpus Preflight")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Input: `{payload['input_jsonl']}`")
    lines.append(f"- Mathlib root: `{payload['mathlib_root']}`")
    lines.append(f"- Goals checked: {summary['n_goals']}")
    lines.append(f"- Unique declaration names checked: {summary['n_unique_names']}")
    lines.append(f"- Missing declaration names: {summary['n_missing_names']}")
    lines.append("")
    lines.append("## Goal-Level Audit")
    lines.append("")
    lines.append("| Item | Count | Rate |")
    lines.append("|---|---:|---:|")
    for key in [
        "file_exists",
        "module_inferred",
        "theorem_name_present",
        "theorem_exists_in_mathlib430",
        "all_proof_core_exists_in_mathlib430",
        "target_name_in_proof_core",
        "target_name_in_candidates",
    ]:
        count = summary["goal_counts"].get(key, 0)
        rate = 100.0 * count / summary["n_goals"] if summary["n_goals"] else 0.0
        lines.append(f"| `{key}` | {count} | {rate:.1f}% |")
    lines.append("")
    lines.append("## Missing Names")
    lines.append("")
    if payload["missing_names_sample"]:
        for name in payload["missing_names_sample"]:
            lines.append(f"- `{name}`")
    else:
        lines.append("- None in checked sample.")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    if payload["preflight_passed"]:
        lines.append("- Name-level migration looks feasible for this sample.")
        lines.append("- This does not yet prove standalone elaboration or non-circular replay; it only clears the first migration gate.")
    else:
        lines.append("- Name-level migration has issues or circular-leakage risks. Inspect the samples before building a full replay grid.")
    lines.append("")
    lines.append("## Risk Samples")
    for key, rows in payload["risk_samples"].items():
        lines.append("")
        lines.append(f"### {key}")
        lines.append("")
        if not rows:
            lines.append("- None.")
            continue
        for row in rows[:10]:
            lines.append(f"- `{row['goal_id']}` theorem=`{row.get('theorem')}` file=`{row.get('file_path')}`")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--timeout-s", type=float, default=180.0)
    args = parser.parse_args()

    input_jsonl = args.input_jsonl.resolve()
    mathlib_root = args.mathlib_root.resolve()
    work_dir = args.work_dir.resolve()
    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    goals = load_goals(input_jsonl, args.limit)
    names: list[str] = []
    seen: set[str] = set()
    goal_records: list[dict[str, Any]] = []
    for goal in goals:
        metadata = goal.get("metadata") or {}
        theorem = clean_decl_name(metadata.get("theorem"))
        proof_core = [clean_decl_name(x) for x in goal.get("proof_core", []) if clean_decl_name(x)]
        candidates = [
            clean_decl_name(c.get("name"))
            for c in goal.get("candidates", [])
            if isinstance(c, dict) and clean_decl_name(c.get("name"))
        ]
        for name in [theorem, *proof_core]:
            if name and name not in seen:
                names.append(name)
                seen.add(name)
        file_path = metadata.get("file_path") or ""
        local_file = mathlib_root / file_path if file_path else None
        goal_records.append(
            {
                "goal_id": goal.get("goal_id", ""),
                "theorem": theorem,
                "file_path": file_path,
                "module": module_from_file_path(file_path),
                "file_exists": bool(local_file and local_file.exists()),
                "proof_core": proof_core,
                "candidate_names": candidates,
                "target_name_in_proof_core": theorem in set(proof_core) if theorem else False,
                "target_name_in_candidates": theorem in set(candidates) if theorem else False,
            }
        )

    line_to_name: dict[int, str] = {}
    check_file = work_dir / "CheckNames.lean"
    check_file.write_text(render_check_file(names, line_to_name), encoding="utf-8")
    check_run = run_cmd(["lake", "env", "lean", str(check_file)], cwd=mathlib_root, timeout_s=args.timeout_s)
    check_output = ((check_run.get("stdout") or "") + "\n" + (check_run.get("stderr") or "")).strip()
    missing_names = parse_missing_names(check_output, line_to_name)
    existing_names = set(names) - missing_names

    for record in goal_records:
        theorem = record["theorem"]
        proof_core = record["proof_core"]
        record["theorem_exists_in_mathlib430"] = bool(theorem and theorem in existing_names)
        record["missing_proof_core_names"] = [name for name in proof_core if name not in existing_names]
        record["all_proof_core_exists_in_mathlib430"] = not record["missing_proof_core_names"]
        record["module_inferred"] = bool(record["module"])
        record["theorem_name_present"] = bool(theorem)

    goal_counts = Counter()
    for record in goal_records:
        for key in [
            "file_exists",
            "module_inferred",
            "theorem_name_present",
            "theorem_exists_in_mathlib430",
            "all_proof_core_exists_in_mathlib430",
            "target_name_in_proof_core",
            "target_name_in_candidates",
        ]:
            goal_counts[key] += int(bool(record.get(key)))

    risk_samples = {
        "missing_file": [r for r in goal_records if not r["file_exists"]][:20],
        "missing_theorem_name": [r for r in goal_records if not r["theorem_exists_in_mathlib430"]][:20],
        "missing_proof_core": [r for r in goal_records if not r["all_proof_core_exists_in_mathlib430"]][:20],
        "target_in_proof_core": [r for r in goal_records if r["target_name_in_proof_core"]][:20],
        "target_in_candidates": [r for r in goal_records if r["target_name_in_candidates"]][:20],
    }
    n_goals = len(goal_records)
    missing_rate = len(missing_names) / len(names) if names else 0.0
    circular_candidate_rate = goal_counts["target_name_in_candidates"] / n_goals if n_goals else 0.0
    preflight_passed = (
        check_run["success"]
        and goal_counts["file_exists"] == n_goals
        and goal_counts["theorem_exists_in_mathlib430"] >= int(0.95 * n_goals)
        and goal_counts["all_proof_core_exists_in_mathlib430"] >= int(0.95 * n_goals)
        and circular_candidate_rate < 0.50
    )
    payload = {
        "experiment": "mathlib430_trace_corpus_preflight",
        "input_jsonl": str(input_jsonl),
        "mathlib_root": str(mathlib_root),
        "work_dir": str(work_dir),
        "limit": args.limit,
        "check_run": check_run,
        "preflight_passed": preflight_passed,
        "verdict": "pass" if preflight_passed else "needs_attention",
        "summary": {
            "n_goals": n_goals,
            "n_unique_names": len(names),
            "n_missing_names": len(missing_names),
            "missing_name_rate": missing_rate,
            "goal_counts": dict(goal_counts),
        },
        "missing_names_sample": sorted(missing_names)[:100],
        "risk_samples": risk_samples,
        "goals": goal_records,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_md(payload, out_md)
    print(out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
