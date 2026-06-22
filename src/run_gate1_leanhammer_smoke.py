"""Gate 1 LeanHammer premise-intervention smoke test.

This script runs small LeanHammer attempts where the only experimental variable
is the explicit premise list supplied to `hammer [premises]`. Success requires
that a complete premise set verifies and that removing a required premise changes
the terminal outcome.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
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
class SmokeCase:
    goal_id: str
    description: str
    prelude: str
    target: str
    variants: dict[str, list[str]]
    expected_verified: dict[str, bool]


CASES = [
    SmokeCase(
        goal_id="prop_chain3",
        description="Three-hop propositional chain; every link is required.",
        prelude="""
axiom A : Prop
axiom B : Prop
axiom C : Prop
axiom p_A : A
axiom p_A_to_B : A -> B
axiom p_B_to_C : B -> C
axiom distractor_AB : B -> A
""".strip(),
        target="theorem gate1_prop_chain3 : C := by",
        variants={
            "complete": ["p_A", "p_A_to_B", "p_B_to_C"],
            "missing_bridge": ["p_A", "p_A_to_B"],
            "wrong_direction": ["p_A", "distractor_AB", "p_B_to_C"],
            "extra_noise": ["p_A", "p_A_to_B", "p_B_to_C", "distractor_AB"],
        },
        expected_verified={
            "complete": True,
            "missing_bridge": False,
            "wrong_direction": False,
            "extra_noise": True,
        },
    ),
    SmokeCase(
        goal_id="prop_conjunction",
        description="Conjunction reconstruction; both conjunct premises are required.",
        prelude="""
axiom P : Prop
axiom Q : Prop
axiom p_P : P
axiom p_Q : Q
axiom p_Q_to_P : Q -> P
""".strip(),
        target="theorem gate1_prop_conjunction : P ∧ Q := by",
        variants={
            "complete": ["p_P", "p_Q"],
            "missing_right": ["p_P"],
            "missing_left": ["p_Q"],
            "extra_noise": ["p_P", "p_Q", "p_Q_to_P"],
        },
        expected_verified={
            "complete": True,
            "missing_right": False,
            "missing_left": False,
            "extra_noise": True,
        },
    ),
]


def lean_ident(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")


def render_case(case: SmokeCase, variant: str, premises: list[str]) -> str:
    premise_terms = ", ".join(premises)
    return "\n".join(
        [
            "import Hammer",
            "",
            "set_option trace.hammer.premises true",
            "set_option trace.hammer.profiling true",
            "",
            case.prelude,
            "",
            case.target,
            f"  hammer [{premise_terms}] {{{HAMMER_OPTIONS}}}",
            "",
        ]
    )


def classify_output(returncode: int, output: str) -> tuple[str, str]:
    low = output.lower()
    if returncode == 0:
        return "proved", "verified"
    if "timeout" in low:
        return "timeout", "not_attempted"
    if "failed to preprocess facts for translation" in low:
        return "translation_fail", "failed"
    if "unable to solve" in low or "aesop failed" in low or "tactic" in low:
        return "search_fail", "not_attempted"
    return "lean_error", "failed"


def parse_trace_premises(output: str) -> dict[str, str | None]:
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


def run_lean_file(hammer_root: Path, lean_file: Path, timeout_s: float) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            ["lake", "env", "lean", str(lean_file)],
            cwd=hammer_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_s,
        )
        elapsed = time.perf_counter() - start
        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        status, reconstruction_status = classify_output(proc.returncode, output)
        return {
            "returncode": proc.returncode,
            "status": status,
            "verified": proc.returncode == 0,
            "reconstruction_status": reconstruction_status,
            "time_s": elapsed,
            "output_tail": output[-3000:],
            **parse_trace_premises(output),
        }
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - start
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return {
            "returncode": None,
            "status": "wrapper_timeout",
            "verified": False,
            "reconstruction_status": "not_attempted",
            "time_s": elapsed,
            "output_tail": output[-3000:],
            **parse_trace_premises(output),
        }


def write_markdown(payload: dict[str, Any], out: Path) -> None:
    lines: list[str] = []
    lines.append("# Gate 1 LeanHammer Premise-Intervention Smoke")
    lines.append("")
    lines.append(f"- Hammer root: `{payload['hammer_root']}`")
    lines.append(f"- Timeout per attempt: {payload['timeout_s']}s")
    lines.append(f"- Verdict: `{payload['verdict']}`")
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
    if payload["gate1_passed"]:
        lines.append("- Gate 1 passes for the minimal LeanHammer interface: changing the explicit premise list changes verified outcome.")
        lines.append("- The smoke uses `hammer [premises]` with selector premise counts set to zero, so the explicit premise intervention is the controlled variable.")
    else:
        lines.append("- Gate 1 does not pass. Do not proceed to Gate 2 until the failure is resolved.")
    lines.append("")
    lines.append("## Trace Check")
    lines.append("")
    for result in payload["results"]:
        lines.append(f"### {result['goal_id']} / {result['variant']}")
        lines.append("")
        lines.append(f"- user input terms: `{result.get('trace_user_input_terms')}`")
        lines.append(f"- selector premises: `{result.get('trace_selector_premises')}`")
        lines.append(f"- selector premises after dedupe: `{result.get('trace_selector_premises_deduped')}`")
        lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hammer-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--timeout-s", type=float, default=30.0)
    args = parser.parse_args()

    args.hammer_root = args.hammer_root.resolve()
    args.save_dir = args.save_dir.resolve()
    args.out_json = args.out_json.resolve()
    args.out_md = args.out_md.resolve()
    args.save_dir.mkdir(parents=True, exist_ok=True)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for case in CASES:
        for variant, premises in case.variants.items():
            file_name = f"{lean_ident(case.goal_id)}__{lean_ident(variant)}.lean"
            lean_file = args.save_dir / file_name
            lean_file.write_text(render_case(case, variant, premises), encoding="utf-8")
            run_result = run_lean_file(args.hammer_root, lean_file, args.timeout_s)
            expected = case.expected_verified[variant]
            results.append(
                {
                    "goal_id": case.goal_id,
                    "description": case.description,
                    "variant": variant,
                    "premises": premises,
                    "expected_verified": expected,
                    "expectation_met": bool(run_result["verified"]) == expected,
                    "lean_file": str(lean_file),
                    **run_result,
                }
            )
            print(
                f"{case.goal_id}/{variant}: status={run_result['status']} "
                f"verified={run_result['verified']} expected={expected}",
                flush=True,
            )

    gate1_passed = all(result["expectation_met"] for result in results) and any(
        result["verified"] for result in results
    ) and any(not result["verified"] for result in results)
    payload = {
        "experiment": "gate1_leanhammer_premise_intervention_smoke",
        "hammer_root": str(args.hammer_root),
        "save_dir": str(args.save_dir),
        "timeout_s": args.timeout_s,
        "gate1_passed": gate1_passed,
        "verdict": "pass" if gate1_passed else "fail",
        "results": results,
    }
    args.out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, args.out_md)
    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_md}")


if __name__ == "__main__":
    main()
