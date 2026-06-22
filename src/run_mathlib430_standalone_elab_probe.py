"""Probe standalone elaboration of cleaned trace goal statements on Mathlib 4.30."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


ATTR_RE = re.compile(r"^\s*@\[[\s\S]*?\]\s*")
DECL_RE = re.compile(r"^\s*(?:private\s+)?(?:(protected)\s+)?(lemma|theorem)\s+(?:_root_\.)?[^\s(:]+")


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
            "output_tail": output[-5000:],
        }
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return {
            "returncode": None,
            "success": False,
            "time_s": time.perf_counter() - start,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "output_tail": output[-5000:],
            "timeout": True,
        }


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


def render_statement(goal_state: str, idx: int) -> tuple[str | None, str | None]:
    text = ATTR_RE.sub("", goal_state.strip())
    match = DECL_RE.search(text)
    if not match:
        return None, "unsupported_declaration_shape"
    name = f"standalone_elab_{idx:04d}"
    text = DECL_RE.sub(f"theorem {name}", text, count=1)
    stripped = text.rstrip()
    if stripped.endswith(":="):
        body = stripped + " by\n  sorry\n"
    elif ":=" not in stripped:
        body = stripped + " := by\n  sorry\n"
    else:
        return None, "statement_already_has_body"
    return "import Mathlib\n\nset_option autoImplicit true\n\n" + body, None


def classify(output: str) -> str:
    low = output.lower()
    if "unknown identifier" in low or "unknown constant" in low:
        return "unknown_identifier"
    if "failed to synthesize" in low or "failed to infer" in low or "typeclass" in low:
        return "typeclass_or_inference"
    if "application type mismatch" in low or "type mismatch" in low:
        return "type_mismatch"
    if "unexpected token" in low or "expected" in low:
        return "syntax_or_parse"
    return "lean_error"


def run_one(
    *,
    row: dict[str, Any],
    idx: int,
    mathlib_root: Path,
    save_dir: Path,
    timeout_s: float,
) -> dict[str, Any]:
    goal_state = row.get("goal_state", "")
    rendered, render_error = render_statement(goal_state, idx)
    metadata = row.get("metadata") or {}
    base = {
        "goal_id": row.get("goal_id", ""),
        "theorem": metadata.get("theorem", ""),
        "file_path": metadata.get("file_path", ""),
    }
    if render_error or rendered is None:
        return {**base, "success": False, "status": render_error, "time_s": 0.0, "output_tail": ""}
    lean_file = save_dir / f"standalone_elab_{idx:04d}.lean"
    lean_file.write_text(rendered, encoding="utf-8")
    result = run_cmd(["lake", "env", "lean", str(lean_file)], cwd=mathlib_root, timeout_s=timeout_s)
    return {
        **base,
        "success": result["success"],
        "status": "elaborated" if result["success"] else classify(result["output_tail"]),
        "time_s": result["time_s"],
        "returncode": result["returncode"],
        "lean_file": str(lean_file),
        "output_tail": result["output_tail"],
    }


def write_md(payload: dict[str, Any], out: Path) -> None:
    summary = payload["summary"]
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Standalone Elaboration Probe")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Input: `{payload['input_jsonl']}`")
    lines.append(f"- Goals checked: {summary['n_goals']}")
    lines.append(f"- Elaborated: {summary['n_success']} ({100.0 * summary['success_rate']:.1f}%)")
    lines.append("")
    lines.append("## Status Counts")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---:|")
    for status, count in summary["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    lines.append("- This only checks standalone statement elaboration with `sorry`.")
    lines.append("- Failures usually mean the theorem depends on original file section variables, namespaces, local notation, or attributes; a pre-theorem file-patching replay harness may still handle them.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    args = parser.parse_args()

    input_jsonl = args.input_jsonl.resolve()
    mathlib_root = args.mathlib_root.resolve()
    save_dir = args.save_dir.resolve()
    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    save_dir.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl(input_jsonl, args.limit)
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [
            pool.submit(
                run_one,
                row=row,
                idx=idx,
                mathlib_root=mathlib_root,
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
    for result in results:
        status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1
    n_success = sum(1 for result in results if result["success"])
    payload = {
        "experiment": "mathlib430_standalone_elab_probe",
        "input_jsonl": str(input_jsonl),
        "mathlib_root": str(mathlib_root),
        "save_dir": str(save_dir),
        "limit": args.limit,
        "verdict": "pass" if n_success else "needs_pretheorem_context",
        "summary": {
            "n_goals": len(results),
            "n_success": n_success,
            "success_rate": n_success / len(results) if results else 0.0,
            "status_counts": status_counts,
        },
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_md(payload, out_md)
    print(out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
