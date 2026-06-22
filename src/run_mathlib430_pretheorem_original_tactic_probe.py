"""Replay original traced tactic scripts inside Mathlib 4.30 source files.

This diagnostic separates corpus/context drift from LeanHammer action quality.
For each cleaned trace row, it patches the original Mathlib 4.30 theorem proof
with the traced tactic script and runs Lean on the patched file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


def run_cmd(
    cmd: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout_s: float,
) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
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


def lake_lean_path(root: Path, timeout_s: float) -> str:
    result = run_cmd(["lake", "env", "printenv", "LEAN_PATH"], cwd=root, timeout_s=timeout_s)
    if not result["success"] or not result["stdout"].strip():
        raise RuntimeError(f"failed to get LEAN_PATH for {root}:\n{result['output_tail']}")
    return result["stdout"].splitlines()[0].strip()


def load_jsonl(path: Path, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rows.append(json.loads(line))
            if limit and len(rows) >= limit:
                break
    return rows


def normalize_imports_for_probe(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if line.strip() == "module":
            continue
        if line.startswith("public import "):
            out.append(line.replace("public import ", "import ", 1))
        else:
            out.append(line)
    return out


TOP_COMMAND_RE = re.compile(
    r"^(?:@[^\n]*)?\s*(?:"
    r"lemma|theorem|def|instance|class|structure|inductive|abbrev|opaque|"
    r"section|namespace|end|variable|open|attribute|noncomputable|example"
    r")\b"
)


def find_decl_end_line(source_lines: list[str], start_line: int) -> int | None:
    saw_by = False
    for idx in range(start_line - 1, len(source_lines)):
        line = source_lines[idx]
        if ":= by" in line:
            saw_by = True
            continue
        if idx == start_line - 1:
            continue
        if saw_by and line and not line[0].isspace() and TOP_COMMAND_RE.match(line):
            return idx
    return None


def render_tactic_script(tactics: list[Any]) -> str:
    lines: list[str] = []
    for tactic in tactics:
        for line in str(tactic).splitlines():
            lines.append(f"  {line.rstrip()}" if line.strip() else "")
    return "\n".join(lines).rstrip() + "\n"


def patch_theorem_block_with_script(
    *,
    source_lines: list[str],
    start_line: int,
    end_line: int,
    tactics: list[Any],
) -> tuple[list[str] | None, str | None]:
    if not tactics:
        return None, "missing_tactic_script"
    if start_line < 1 or start_line > len(source_lines):
        return None, "invalid_source_span"
    scanned_end = find_decl_end_line(source_lines, start_line)
    if scanned_end is not None:
        end_line = scanned_end
    if end_line < start_line or end_line > len(source_lines):
        return None, "invalid_source_span"
    block = "".join(source_lines[start_line - 1 : end_line])
    match = re.search(r":=\s*by", block)
    if not match:
        return None, "no_by_proof_marker"
    prefix = block[: match.end()]
    new_block = prefix.rstrip() + "\n" + render_tactic_script(tactics)
    patched = source_lines[: start_line - 1] + [new_block] + source_lines[end_line:]
    return normalize_imports_for_probe(patched), None


def classify(output: str) -> str:
    low = output.lower()
    if "unexpected token" in low or "expected" in low and "command" in low:
        return "parse_error"
    if "unknown identifier" in low or "unknown constant" in low:
        return "unknown_identifier"
    if "failed to synthesize" in low or "failed to infer" in low or "typeclass" in low:
        return "typeclass_or_inference"
    if "application type mismatch" in low or "type mismatch" in low:
        return "type_mismatch"
    if "simp made no progress" in low or "simp" in low and "failed" in low:
        return "simp_fail"
    if "rewrite" in low or "rw" in low:
        return "rewrite_fail"
    if "unsolved goals" in low or "tactic" in low or "unable to solve" in low:
        return "tactic_fail"
    if "timeout" in low:
        return "timeout"
    return "lean_error"


def run_one(
    *,
    row: dict[str, Any],
    idx: int,
    mathlib_root: Path,
    env: dict[str, str],
    save_dir: Path,
    timeout_s: float,
) -> dict[str, Any]:
    metadata = row.get("metadata") or {}
    file_path = metadata.get("file_path", "")
    theorem = metadata.get("theorem", "")
    start = metadata.get("start") or []
    end = metadata.get("end") or []
    tactics = list(metadata.get("tactic_script") or [])
    base = {
        "goal_id": row.get("goal_id", ""),
        "theorem": theorem,
        "file_path": file_path,
        "tactic_script": tactics,
        "proof_core": [p for p in row.get("proof_core", []) if p],
    }
    if len(start) < 1 or len(end) < 1:
        return {**base, "verified": False, "status": "missing_span", "time_s": 0.0}
    source_file = mathlib_root / file_path
    if not source_file.exists():
        return {**base, "verified": False, "status": "missing_source_file", "time_s": 0.0}
    source_lines = source_file.read_text(encoding="utf-8").splitlines(keepends=True)
    patched, patch_error = patch_theorem_block_with_script(
        source_lines=source_lines,
        start_line=int(start[0]),
        end_line=int(end[0]),
        tactics=tactics,
    )
    if patch_error or patched is None:
        return {**base, "verified": False, "status": patch_error, "time_s": 0.0}
    out_file = save_dir / f"pretheorem_original_tactic_{idx:04d}.lean"
    out_file.write_text("".join(patched), encoding="utf-8")
    result = run_cmd(["lean", str(out_file)], cwd=mathlib_root, env=env, timeout_s=timeout_s)
    return {
        **base,
        "verified": result["success"],
        "status": "verified" if result["success"] else classify(result["output_tail"]),
        "time_s": result["time_s"],
        "returncode": result["returncode"],
        "patched_file": str(out_file),
        "output_tail": result["output_tail"],
    }


def write_md(payload: dict[str, Any], out: Path) -> None:
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Pre-Theorem Original-Tactic Probe")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Input: `{payload['input_jsonl']}`")
    lines.append(f"- Goals checked: {payload['summary']['n_goals']}")
    lines.append(f"- Original tactic replay verified: {payload['summary']['n_verified']}")
    lines.append("")
    lines.append("## Status Counts")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---:|")
    for status, count in payload["summary"]["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Goal | Status | Time |")
    lines.append("|---|---|---:|")
    for row in payload["results"]:
        lines.append(f"| `{row['goal_id']}` | `{row['status']}` | {row['time_s']:.2f}s |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    if payload["summary"]["n_verified"]:
        lines.append(
            "- At least one cleaned traced theorem can be replayed in the original Mathlib 4.30 file context, so corpus migration is not globally broken."
        )
        lines.append(
            "- Remaining negative Hammer results should be debugged as action/premise/backend limitations on the replayable subset."
        )
    else:
        lines.append(
            "- No original traced tactic replay succeeded in this sample; prioritize migration/span/context repair before running larger Hammer grids."
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--timeout-s", type=float, default=180.0)
    args = parser.parse_args()

    input_jsonl = args.input_jsonl.resolve()
    mathlib_root = args.mathlib_root.resolve()
    save_dir = args.save_dir.resolve()
    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    save_dir.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["LEAN_PATH"] = lake_lean_path(mathlib_root, args.timeout_s)
    rows = load_jsonl(input_jsonl, args.limit)
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [
            pool.submit(
                run_one,
                row=row,
                idx=idx,
                mathlib_root=mathlib_root,
                env=env,
                save_dir=save_dir,
                timeout_s=args.timeout_s,
            )
            for idx, row in enumerate(rows)
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"{result['goal_id']}: {result['status']}", flush=True)

    order = {row.get("goal_id", ""): i for i, row in enumerate(rows)}
    results.sort(key=lambda row: order.get(row["goal_id"], 0))
    status_counts: dict[str, int] = {}
    for row in results:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    n_verified = sum(1 for row in results if row["verified"])
    payload = {
        "experiment": "mathlib430_pretheorem_original_tactic_probe",
        "input_jsonl": str(input_jsonl),
        "mathlib_root": str(mathlib_root),
        "save_dir": str(save_dir),
        "limit": args.limit,
        "verdict": "pass" if n_verified else "probe_completed_no_original_replay",
        "summary": {
            "n_goals": len(results),
            "n_verified": n_verified,
            "status_counts": status_counts,
        },
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_md(payload, out_md)
    print(out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
