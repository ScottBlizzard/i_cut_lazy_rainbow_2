"""Probe a Mathlib 4.30 + LeanHammer 4.30 combined environment.

The paper-level LeanHammer experiments need a single Lean process that can
import both Mathlib and Hammer.  The current traced mathlib repo is Lean 4.31,
while LeanHammer is Lean 4.30, so this probe validates the route-A stack:
pin an evaluation mathlib checkout to v4.30.0 and combine it with the built
LeanHammer v4.30.0 checkout.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
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
            "cmd": cmd,
            "cwd": str(cwd),
            "returncode": proc.returncode,
            "success": proc.returncode == 0,
            "time_s": time.perf_counter() - start,
            "stdout": proc.stdout.strip() if proc.stdout else "",
            "stderr_tail": (proc.stderr or "")[-3000:],
            "output_tail": output[-5000:],
        }
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return {
            "cmd": cmd,
            "cwd": str(cwd),
            "returncode": None,
            "success": False,
            "time_s": time.perf_counter() - start,
            "stdout": (exc.stdout or "").strip(),
            "stderr_tail": (exc.stderr or "")[-3000:],
            "output_tail": output[-5000:],
            "timeout": True,
        }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def git_commit(root: Path, timeout_s: float) -> str:
    result = run_cmd(["git", "rev-parse", "HEAD"], cwd=root, timeout_s=timeout_s)
    return result.get("stdout", "").splitlines()[-1] if result.get("success") else ""


def lake_lean_path(root: Path, timeout_s: float) -> tuple[str, dict[str, Any]]:
    result = run_cmd(["lake", "env", "printenv", "LEAN_PATH"], cwd=root, timeout_s=timeout_s)
    lean_path = result.get("stdout", "").splitlines()[0].strip() if result.get("stdout") else ""
    return lean_path, result


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def render_md(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Mathlib 4.30 / LeanHammer 4.30 Compatibility Probe")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Hammer root: `{payload['hammer_root']}`")
    lines.append(f"- Hammer commit: `{payload['hammer_commit']}`")
    lines.append(f"- Hammer toolchain: `{payload['hammer_toolchain']}`")
    lines.append(f"- Mathlib root: `{payload['mathlib_root']}`")
    lines.append(f"- Mathlib commit: `{payload['mathlib_commit']}`")
    lines.append(f"- Mathlib toolchain: `{payload['mathlib_toolchain']}`")
    lines.append(f"- Combined Lean version: `{payload['combined_lean_version']}`")
    lines.append("")
    lines.append("| Probe | Success | Return code | Time |")
    lines.append("|---|---:|---:|---:|")
    for row in payload["results"]:
        lines.append(
            f"| `{row['name']}` | {str(row['success']).lower()} | "
            f"{row['returncode']} | {row['time_s']:.2f}s |"
        )
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    if payload["compat_passed"]:
        lines.append("- The route-A stack is usable: one Lean 4.30 process can import both `Mathlib` and `Hammer`.")
        lines.append("- This removes the immediate Mathlib/LeanHammer compatibility blocker for Mathlib-context smoke tests.")
    else:
        lines.append("- The route-A stack is not usable yet. Do not run Mathlib-scale LeanHammer gates until this passes.")
    lines.append("")
    lines.append("## Output Tails")
    for row in payload["results"]:
        lines.append("")
        lines.append(f"### {row['name']}")
        lines.append("")
        lines.append("```text")
        lines.append(row.get("output_tail", ""))
        lines.append("```")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hammer-root", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    args = parser.parse_args()

    hammer_root = args.hammer_root.resolve()
    mathlib_root = args.mathlib_root.resolve()
    work_dir = args.work_dir.resolve()
    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    hammer_only = write(work_dir / "HammerOnly.lean", "import Hammer\n\n#check Hammer.evalHammer\n")
    mathlib_only = write(work_dir / "MathlibOnly.lean", "import Mathlib\n\n#check Nat.add_comm\n")
    combined = write(
        work_dir / "CombinedMathlibHammer.lean",
        "\n".join(
            [
                "import Mathlib",
                "import Hammer",
                "",
                "#check Nat.add_comm",
                "#check Hammer.evalHammer",
                "",
                "example (a b : Nat) : a + b = b + a := by",
                "  exact Nat.add_comm a b",
                "",
            ]
        ),
    )

    results: list[dict[str, Any]] = []
    hammer_path, hammer_path_result = lake_lean_path(hammer_root, args.timeout_s)
    mathlib_path, mathlib_path_result = lake_lean_path(mathlib_root, args.timeout_s)
    results.append({"name": "hammer_lake_lean_path", **hammer_path_result})
    results.append({"name": "mathlib_lake_lean_path", **mathlib_path_result})
    results.append(
        {
            "name": "hammer_only_lake_env",
            **run_cmd(["lake", "env", "lean", str(hammer_only)], cwd=hammer_root, timeout_s=args.timeout_s),
        }
    )
    results.append(
        {
            "name": "mathlib_only_lake_env",
            **run_cmd(["lake", "env", "lean", str(mathlib_only)], cwd=mathlib_root, timeout_s=args.timeout_s),
        }
    )

    combined_env = os.environ.copy()
    combined_env["LEAN_PATH"] = ":".join(p for p in [hammer_path, mathlib_path] if p)
    lean_version = run_cmd(["lean", "--version"], cwd=hammer_root, env=combined_env, timeout_s=args.timeout_s)
    combined_run = run_cmd(["lean", str(combined)], cwd=hammer_root, env=combined_env, timeout_s=args.timeout_s)
    results.append({"name": "combined_lean_version", **lean_version})
    results.append({"name": "combined_import_mathlib_hammer", **combined_run})

    compat_passed = (
        hammer_path_result["success"]
        and mathlib_path_result["success"]
        and all(row["success"] for row in results if row["name"].endswith("_lake_env"))
        and combined_run["success"]
        and "4.30.0" in lean_version.get("stdout", "")
    )
    payload = {
        "experiment": "mathlib_leanhammer_compat_probe_v2",
        "hammer_root": str(hammer_root),
        "hammer_commit": git_commit(hammer_root, args.timeout_s),
        "hammer_toolchain": read_text(hammer_root / "lean-toolchain"),
        "mathlib_root": str(mathlib_root),
        "mathlib_commit": git_commit(mathlib_root, args.timeout_s),
        "mathlib_toolchain": read_text(mathlib_root / "lean-toolchain"),
        "work_dir": str(work_dir),
        "combined_lean_version": lean_version.get("stdout", "").splitlines()[0] if lean_version.get("stdout") else "",
        "compat_passed": compat_passed,
        "verdict": "pass" if compat_passed else "fail",
        "combined_lean_path_entry_count": len(combined_env["LEAN_PATH"].split(":")) if combined_env["LEAN_PATH"] else 0,
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    out_md.write_text(render_md(payload), encoding="utf-8")
    print(out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
