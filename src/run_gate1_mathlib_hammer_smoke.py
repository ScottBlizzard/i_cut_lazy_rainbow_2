"""Gate 1 Mathlib-context LeanHammer premise-intervention smoke test.

This is the first non-synthetic LeanHammer smoke after the route-A compatibility
fix.  It runs in a combined Mathlib 4.30 + LeanHammer 4.30 environment and
checks whether explicit `hammer [premises]` interventions still causally change
kernel-verified outcomes on Mathlib theorem/context examples.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HAMMER_OPTIONS = (
    "disableAuto := true, "
    "disableGrind := true, "
    "aesopPremises := 0, "
    "autoPremises := 0, "
    "grindPremises := 0, "
    "solverTimeout := 2, "
    "wallclockTimeout := 5"
)


@dataclass(frozen=True)
class MathlibSmokeCase:
    goal_id: str
    family: str
    description: str
    target: str
    variants: dict[str, list[str]]
    expected_verified: dict[str, bool]


CASES = [
    MathlibSmokeCase(
        goal_id="mathlib_nat_add_comm",
        family="nat",
        description="Global Mathlib theorem Nat.add_comm is necessary for the bounded Aesop-only hammer call.",
        target="example (a b : Nat) : a + b = b + a := by",
        variants={
            "complete": ["Nat.add_comm"],
            "empty": [],
            "wrong_theorem": ["Nat.mul_comm"],
            "extra_noise": ["Nat.add_comm", "Nat.mul_comm"],
        },
        expected_verified={
            "complete": True,
            "empty": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
    MathlibSmokeCase(
        goal_id="mathlib_nat_mul_comm",
        family="nat",
        description="Global Mathlib theorem Nat.mul_comm is necessary under the same bounded call.",
        target="example (a b : Nat) : a * b = b * a := by",
        variants={
            "complete": ["Nat.mul_comm"],
            "empty": [],
            "wrong_theorem": ["Nat.add_comm"],
            "extra_noise": ["Nat.mul_comm", "Nat.add_comm"],
        },
        expected_verified={
            "complete": True,
            "empty": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
    MathlibSmokeCase(
        goal_id="mathlib_nat_add_assoc",
        family="nat",
        description="Nat.add_assoc is not solved by the bounded default call without the explicit theorem.",
        target="example (a b c : Nat) : (a + b) + c = a + (b + c) := by",
        variants={
            "complete": ["Nat.add_assoc"],
            "empty": [],
            "wrong_theorem": ["Nat.mul_assoc"],
            "extra_noise": ["Nat.add_assoc", "Nat.mul_assoc"],
        },
        expected_verified={
            "complete": True,
            "empty": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
    MathlibSmokeCase(
        goal_id="mathlib_nat_mul_assoc",
        family="nat",
        description="Nat.mul_assoc is controlled by the explicit premise list under the same bounded call.",
        target="example (a b c : Nat) : (a * b) * c = a * (b * c) := by",
        variants={
            "complete": ["Nat.mul_assoc"],
            "empty": [],
            "wrong_theorem": ["Nat.add_assoc"],
            "extra_noise": ["Nat.mul_assoc", "Nat.add_assoc"],
        },
        expected_verified={
            "complete": True,
            "empty": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
    MathlibSmokeCase(
        goal_id="mathlib_nat_gcd_comm",
        family="nat",
        description="Nat.gcd_comm is a Mathlib theorem whose absence leaves the bounded call unsolved.",
        target="example (a b : Nat) : Nat.gcd a b = Nat.gcd b a := by",
        variants={
            "complete": ["Nat.gcd_comm"],
            "empty": [],
            "wrong_theorem": ["Nat.lcm_comm"],
            "extra_noise": ["Nat.gcd_comm", "Nat.lcm_comm"],
        },
        expected_verified={
            "complete": True,
            "empty": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
    MathlibSmokeCase(
        goal_id="mathlib_nat_lcm_comm",
        family="nat",
        description="Nat.lcm_comm gives a second nontrivial commutativity check beyond addition/multiplication.",
        target="example (a b : Nat) : Nat.lcm a b = Nat.lcm b a := by",
        variants={
            "complete": ["Nat.lcm_comm"],
            "empty": [],
            "wrong_theorem": ["Nat.gcd_comm"],
            "extra_noise": ["Nat.lcm_comm", "Nat.gcd_comm"],
        },
        expected_verified={
            "complete": True,
            "empty": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
    MathlibSmokeCase(
        goal_id="mathlib_int_add_assoc",
        family="int",
        description="Int.add_assoc checks the same premise-control mechanism outside Nat.",
        target="example (a b c : Int) : (a + b) + c = a + (b + c) := by",
        variants={
            "complete": ["Int.add_assoc"],
            "empty": [],
            "wrong_theorem": ["Nat.add_assoc"],
            "extra_noise": ["Int.add_assoc", "Nat.add_assoc"],
        },
        expected_verified={
            "complete": True,
            "empty": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
    MathlibSmokeCase(
        goal_id="mathlib_set_subset_trans",
        family="set",
        description="Mathlib Set.Subset.trans is needed to chain local subset assumptions.",
        target="example (α : Type) (s t u : Set α) (h_st : s ⊆ t) (h_tu : t ⊆ u) : s ⊆ u := by",
        variants={
            "complete": ["Set.Subset.trans", "h_st", "h_tu"],
            "missing_trans": ["h_st", "h_tu"],
            "wrong_theorem": ["Set.Subset.antisymm", "h_st", "h_tu"],
            "extra_noise": ["Set.Subset.trans", "h_st", "h_tu", "Set.Subset.antisymm"],
        },
        expected_verified={
            "complete": True,
            "missing_trans": False,
            "wrong_theorem": False,
            "extra_noise": True,
        },
    ),
]


def lean_ident(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")


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


def lake_lean_path(root: Path, timeout_s: float) -> str:
    result = run_cmd(["lake", "env", "printenv", "LEAN_PATH"], cwd=root, timeout_s=timeout_s)
    if not result["success"] or not result["stdout"].strip():
        raise RuntimeError(f"failed to get LEAN_PATH for {root}:\n{result['output_tail']}")
    return result["stdout"].splitlines()[0].strip()


def render_case(case: MathlibSmokeCase, premises: list[str]) -> str:
    return "\n".join(
        [
            "import Mathlib",
            "import Hammer",
            "",
            "set_option trace.hammer.premises true",
            "set_option trace.hammer.profiling true",
            "",
            case.target,
            f"  hammer [{', '.join(premises)}] {{{HAMMER_OPTIONS}}}",
            "",
        ]
    )


def classify(returncode: int | None, output: str) -> str:
    if returncode == 0:
        return "proved"
    low = output.lower()
    if returncode is None or "timeout" in low:
        return "timeout"
    if "failed to preprocess facts for translation" in low:
        return "translation_fail"
    if "unknown constant" in low or "unknown identifier" in low:
        return "elaboration_fail"
    if "aesop failed" in low or "tactic" in low or "unable to solve" in low:
        return "search_fail"
    return "lean_error"


def parse_trace(output: str) -> dict[str, str | None]:
    fields = {
        "trace_user_input_terms": None,
        "trace_selector_premises": None,
        "trace_selector_premises_deduped": None,
    }
    patterns = {
        "trace_user_input_terms": r"user input terms:\s*(.+)",
        "trace_selector_premises": r"premises from premise selector:\s*(.+)",
        "trace_selector_premises_deduped": r"premises from premise selector after removing duplicates in user input terms:\s*(.+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            fields[key] = match.group(1).strip()
    return fields


def run_attempt(
    *,
    hammer_root: Path,
    env: dict[str, str],
    save_dir: Path,
    timeout_s: float,
    case: MathlibSmokeCase,
    variant: str,
    premises: list[str],
) -> dict[str, Any]:
    lean_file = save_dir / f"{lean_ident(case.goal_id)}__{lean_ident(variant)}.lean"
    lean_file.write_text(render_case(case, premises), encoding="utf-8")
    run = run_cmd(["lean", str(lean_file)], cwd=hammer_root, env=env, timeout_s=timeout_s)
    output = ((run.get("stdout") or "") + "\n" + (run.get("stderr") or "")).strip()
    status = classify(run["returncode"], output)
    expected = case.expected_verified[variant]
    return {
        "goal_id": case.goal_id,
        "family": case.family,
        "description": case.description,
        "variant": variant,
        "premises": premises,
        "expected_verified": expected,
        "verified": run["success"],
        "expectation_met": bool(run["success"]) == expected,
        "status": status,
        "time_s": run["time_s"],
        "returncode": run["returncode"],
        "lean_file": str(lean_file),
        "output_tail": run["output_tail"],
        **parse_trace(output),
    }


def write_markdown(payload: dict[str, Any], out: Path) -> None:
    lines: list[str] = []
    lines.append("# Gate 1 Mathlib-Context LeanHammer Smoke")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Hammer root: `{payload['hammer_root']}`")
    lines.append(f"- Mathlib root: `{payload['mathlib_root']}`")
    lines.append(f"- Lean version: `{payload['lean_version']}`")
    lines.append(f"- Jobs: {payload['jobs']}")
    lines.append(f"- Timeout per attempt: {payload['timeout_s']}s")
    lines.append("")
    lines.append("| Goal | Variant | Premises | Expected | Verified | Status | Time |")
    lines.append("|---|---|---|---:|---:|---|---:|")
    for result in payload["results"]:
        lines.append(
            f"| `{result['goal_id']}` | `{result['variant']}` | "
            f"`{', '.join(result['premises'])}` | {str(result['expected_verified']).lower()} | "
            f"{str(result['verified']).lower()} | `{result['status']}` | {result['time_s']:.2f}s |"
        )
    lines.append("")
    lines.append("## Gate Readout")
    lines.append("")
    if payload["gate1_mathlib_passed"]:
        lines.append("- Gate 1 passes in a Mathlib 4.30 context: explicit premise lists change kernel-verified LeanHammer outcomes.")
        lines.append("- The controlled backend has `autoPremises`, `aesopPremises`, and `grindPremises` set to zero, so selector premises are not contributing.")
    else:
        lines.append("- Gate 1 does not pass in Mathlib context. Inspect expectation misses before proceeding to Mathlib Gate 2.")
    lines.append("")
    lines.append("## Expectation Misses")
    misses = [row for row in payload["results"] if not row["expectation_met"]]
    if not misses:
        lines.append("")
        lines.append("- None.")
    else:
        lines.append("")
        for row in misses:
            lines.append(
                f"- `{row['goal_id']}/{row['variant']}` expected {row['expected_verified']} "
                f"but got {row['verified']} (`{row['status']}`)."
            )
    lines.append("")
    lines.append("## Trace Check")
    for result in payload["results"]:
        lines.append("")
        lines.append(f"### {result['goal_id']} / {result['variant']}")
        lines.append("")
        lines.append(f"- user input terms: `{result.get('trace_user_input_terms')}`")
        lines.append(f"- selector premises: `{result.get('trace_selector_premises')}`")
        lines.append(f"- selector premises after dedupe: `{result.get('trace_selector_premises_deduped')}`")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hammer-root", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--timeout-s", type=float, default=90.0)
    args = parser.parse_args()

    hammer_root = args.hammer_root.resolve()
    mathlib_root = args.mathlib_root.resolve()
    save_dir = args.save_dir.resolve()
    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    save_dir.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    hammer_path = lake_lean_path(hammer_root, args.timeout_s)
    mathlib_path = lake_lean_path(mathlib_root, args.timeout_s)
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{hammer_path}:{mathlib_path}"
    lean_version_result = run_cmd(["lean", "--version"], cwd=hammer_root, env=env, timeout_s=args.timeout_s)
    lean_version = lean_version_result["stdout"].splitlines()[0] if lean_version_result["stdout"] else ""

    tasks = []
    for case in CASES:
        for variant, premises in case.variants.items():
            tasks.append((case, variant, premises))

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [
            pool.submit(
                run_attempt,
                hammer_root=hammer_root,
                env=env,
                save_dir=save_dir,
                timeout_s=args.timeout_s,
                case=case,
                variant=variant,
                premises=premises,
            )
            for case, variant, premises in tasks
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"{result['goal_id']}/{result['variant']}: "
                f"status={result['status']} verified={result['verified']} "
                f"expected={result['expected_verified']}",
                flush=True,
            )

    order = {(case.goal_id, variant): i for i, (case, variant, _) in enumerate(tasks)}
    results.sort(key=lambda row: order[(row["goal_id"], row["variant"])])
    has_success = any(row["verified"] for row in results)
    has_failure = any(not row["verified"] for row in results)
    gate1_passed = all(row["expectation_met"] for row in results) and has_success and has_failure
    payload = {
        "experiment": "gate1_mathlib_context_leanhammer_smoke",
        "hammer_root": str(hammer_root),
        "mathlib_root": str(mathlib_root),
        "save_dir": str(save_dir),
        "lean_version": lean_version,
        "jobs": args.jobs,
        "timeout_s": args.timeout_s,
        "gate1_mathlib_passed": gate1_passed,
        "verdict": "pass" if gate1_passed else "fail",
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, out_md)
    print(f"wrote {out_json}")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
