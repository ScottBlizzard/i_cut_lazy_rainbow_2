"""Gate 2 Mathlib-context verified LeanHammer action-grid pilot.

This runs the same adaptive premise-action question as the synthetic Gate 2,
but each attempt is a real Lean 4.30 + Mathlib 4.30 + LeanHammer call.  The
goals are generated from Mathlib theorem/context templates whose empty and
wrong-premise controls were validated by Gate 1.
"""

from __future__ import annotations

import argparse
import json
import math
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

ACTIONS = [
    "keep",
    "shrink_050",
    "shrink_075",
    "expand_150",
    "expand_200",
    "base_rescue_8",
    "base_rescue_16",
    "second_stage_rescore",
    "stop",
]


@dataclass(frozen=True)
class MathlibTemplate:
    name: str
    family: str
    target_template: str
    required: str
    first_premises: list[str]
    noise: list[str]


@dataclass(frozen=True)
class MathlibGridGoal:
    goal_id: str
    template: str
    family: str
    target: str
    required: str | None
    first_premises: list[str]
    candidates: list[str]
    base_rescue: list[str]
    second_stage: list[str]
    expected_best_action: str


COMMON_NAT_NOISE = [
    "Nat.add_comm",
    "Nat.mul_comm",
    "Nat.add_assoc",
    "Nat.mul_assoc",
    "Nat.gcd_comm",
    "Nat.lcm_comm",
    "Int.add_assoc",
    "Set.Subset.trans",
    "Set.Subset.antisymm",
]

TEMPLATES = [
    MathlibTemplate(
        name="nat_add_comm",
        family="nat",
        target_template="theorem {name} (a b : Nat) : a + b = b + a := by",
        required="Nat.add_comm",
        first_premises=["Nat.mul_comm", "Nat.add_assoc", "Nat.mul_assoc"],
        noise=["Nat.gcd_comm", "Nat.lcm_comm", "Int.add_assoc", "Set.Subset.trans", "Set.Subset.antisymm"],
    ),
    MathlibTemplate(
        name="nat_mul_comm",
        family="nat",
        target_template="theorem {name} (a b : Nat) : a * b = b * a := by",
        required="Nat.mul_comm",
        first_premises=["Nat.add_comm", "Nat.add_assoc", "Nat.mul_assoc"],
        noise=["Nat.gcd_comm", "Nat.lcm_comm", "Int.add_assoc", "Set.Subset.trans", "Set.Subset.antisymm"],
    ),
    MathlibTemplate(
        name="nat_add_assoc",
        family="nat",
        target_template="theorem {name} (a b c : Nat) : (a + b) + c = a + (b + c) := by",
        required="Nat.add_assoc",
        first_premises=["Nat.mul_assoc", "Nat.add_comm", "Nat.mul_comm"],
        noise=["Nat.gcd_comm", "Nat.lcm_comm", "Int.add_assoc", "Set.Subset.trans", "Set.Subset.antisymm"],
    ),
    MathlibTemplate(
        name="nat_mul_assoc",
        family="nat",
        target_template="theorem {name} (a b c : Nat) : (a * b) * c = a * (b * c) := by",
        required="Nat.mul_assoc",
        first_premises=["Nat.add_assoc", "Nat.add_comm", "Nat.mul_comm"],
        noise=["Nat.gcd_comm", "Nat.lcm_comm", "Int.add_assoc", "Set.Subset.trans", "Set.Subset.antisymm"],
    ),
    MathlibTemplate(
        name="nat_gcd_comm",
        family="nat",
        target_template="theorem {name} (a b : Nat) : Nat.gcd a b = Nat.gcd b a := by",
        required="Nat.gcd_comm",
        first_premises=["Nat.lcm_comm", "Nat.add_comm", "Nat.mul_comm"],
        noise=["Nat.add_assoc", "Nat.mul_assoc", "Int.add_assoc", "Set.Subset.trans", "Set.Subset.antisymm"],
    ),
    MathlibTemplate(
        name="nat_lcm_comm",
        family="nat",
        target_template="theorem {name} (a b : Nat) : Nat.lcm a b = Nat.lcm b a := by",
        required="Nat.lcm_comm",
        first_premises=["Nat.gcd_comm", "Nat.add_comm", "Nat.mul_comm"],
        noise=["Nat.add_assoc", "Nat.mul_assoc", "Int.add_assoc", "Set.Subset.trans", "Set.Subset.antisymm"],
    ),
    MathlibTemplate(
        name="int_add_assoc",
        family="int",
        target_template="theorem {name} (a b c : Int) : (a + b) + c = a + (b + c) := by",
        required="Int.add_assoc",
        first_premises=["Nat.add_assoc", "Nat.mul_assoc", "Nat.add_comm"],
        noise=["Nat.mul_comm", "Nat.gcd_comm", "Nat.lcm_comm", "Set.Subset.trans", "Set.Subset.antisymm"],
    ),
    MathlibTemplate(
        name="set_subset_trans",
        family="set",
        target_template=(
            "theorem {name} (α : Type) (s t u : Set α) "
            "(h_st : s ⊆ t) (h_tu : t ⊆ u) : s ⊆ u := by"
        ),
        required="Set.Subset.trans",
        first_premises=["h_st", "h_tu", "Set.Subset.antisymm"],
        noise=["Nat.add_comm", "Nat.mul_comm", "Nat.add_assoc", "Nat.mul_assoc", "Nat.gcd_comm"],
    ),
]


def lean_ident(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        out.append(item)
        seen.add(item)
    return out


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


def make_goal(idx: int, family: str) -> MathlibGridGoal:
    template = TEMPLATES[idx % len(TEMPLATES)]
    theorem_name = f"gate2_mathlib_{idx:04d}_{template.name}_{family}"
    first = list(template.first_premises)
    noise = [p for p in [*template.noise, *COMMON_NAT_NOISE] if p != template.required]
    required = template.required if family != "unsolved_grid" else None

    if family == "expand_150":
        candidates = unique(first + ([template.required] if required else []) + noise)
        base_rescue = noise[:8]
        second_stage = noise[1:9]
        expected_best_action = "expand_150"
    elif family == "expand_200":
        candidates = unique(first + noise[:2] + ([template.required] if required else []) + noise[2:])
        base_rescue = noise[:8]
        second_stage = noise[1:9]
        expected_best_action = "expand_200"
    elif family == "base_rescue":
        candidates = unique(first + noise[:8] + ([template.required] if required else []) + noise[8:])
        base_rescue = unique(([template.required] if required else []) + noise[:8])
        second_stage = noise[1:9]
        expected_best_action = "base_rescue_8"
    elif family == "second_stage":
        candidates = unique(first + noise[:8] + ([template.required] if required else []) + noise[8:])
        base_rescue = noise[:8]
        second_stage = unique(([template.required] if required else []) + noise[:8])
        expected_best_action = "second_stage_rescore"
    elif family == "unsolved_grid":
        candidates = unique(first + noise)
        base_rescue = noise[:8]
        second_stage = noise[1:9]
        expected_best_action = "stop"
    else:
        raise ValueError(f"unknown family: {family}")

    return MathlibGridGoal(
        goal_id=f"gate2_mathlib_{idx:04d}_{family}",
        template=template.name,
        family=family,
        target=template.target_template.format(name=theorem_name),
        required=required,
        first_premises=first,
        candidates=candidates,
        base_rescue=base_rescue,
        second_stage=second_stage,
        expected_best_action=expected_best_action,
    )


def generate_goals(n_goals: int) -> list[MathlibGridGoal]:
    families = ["expand_150", "expand_200", "base_rescue", "second_stage", "unsolved_grid"]
    return [make_goal(i, families[i % len(families)]) for i in range(n_goals)]


def action_premises(goal: MathlibGridGoal, action: str, *, first_k: int) -> list[str]:
    first = goal.first_premises[:first_k]
    if action == "stop":
        return []
    if action == "keep":
        return first
    if action == "shrink_050":
        return first[: max(1, math.ceil(len(first) * 0.50))]
    if action == "shrink_075":
        return first[: max(1, math.ceil(len(first) * 0.75))]
    if action == "expand_150":
        return goal.candidates[: max(first_k, math.ceil(first_k * 1.50))]
    if action == "expand_200":
        return goal.candidates[: max(first_k, math.ceil(first_k * 2.00))]
    if action == "base_rescue_8":
        return unique(first + goal.base_rescue[:8])
    if action == "base_rescue_16":
        return unique(first + goal.base_rescue[:16])
    if action == "second_stage_rescore":
        return unique(first + goal.second_stage[:8])
    raise ValueError(f"unknown action: {action}")


def render_attempt(goal: MathlibGridGoal, premises: list[str]) -> str:
    return "\n".join(
        [
            "import Mathlib",
            "import Hammer",
            "",
            "set_option trace.hammer.premises true",
            "",
            goal.target,
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
    match = re.search(r"user input terms:\s*(.+)", output)
    selector = re.search(r"premises from premise selector:\s*(.+)", output)
    return {
        "trace_user_input_terms": match.group(1).strip() if match else None,
        "trace_selector_premises": selector.group(1).strip() if selector else None,
    }


def run_attempt(
    *,
    hammer_root: Path,
    env: dict[str, str],
    save_dir: Path,
    timeout_s: float,
    first_k: int,
    goal: MathlibGridGoal,
    action: str,
) -> dict[str, Any]:
    premises = action_premises(goal, action, first_k=first_k)
    if action == "stop":
        return {
            "goal_id": goal.goal_id,
            "template": goal.template,
            "family": goal.family,
            "action": action,
            "premises": premises,
            "premise_count": 0,
            "required": goal.required,
            "verified": False,
            "status": "stopped",
            "returncode": 0,
            "time_s": 0.0,
            "trace_user_input_terms": None,
            "trace_selector_premises": None,
            "output_tail": "",
        }

    lean_file = save_dir / f"{lean_ident(goal.goal_id)}__{lean_ident(action)}.lean"
    lean_file.write_text(render_attempt(goal, premises), encoding="utf-8")
    run = run_cmd(["lean", str(lean_file)], cwd=hammer_root, env=env, timeout_s=timeout_s)
    output = ((run.get("stdout") or "") + "\n" + (run.get("stderr") or "")).strip()
    return {
        "goal_id": goal.goal_id,
        "template": goal.template,
        "family": goal.family,
        "action": action,
        "premises": premises,
        "premise_count": len(premises),
        "required": goal.required,
        "verified": run["success"],
        "status": classify(run["returncode"], output),
        "returncode": run["returncode"],
        "time_s": run["time_s"],
        "lean_file": str(lean_file),
        "output_tail": run["output_tail"],
        **parse_trace(output),
    }


def success_rate(rows: list[dict[str, Any]]) -> float:
    return sum(1 for row in rows if row["verified"]) / len(rows) if rows else 0.0


def summarize(results: list[dict[str, Any]], goals: list[MathlibGridGoal]) -> dict[str, Any]:
    by_goal: dict[str, dict[str, dict[str, Any]]] = {}
    for row in results:
        by_goal.setdefault(row["goal_id"], {})[row["action"]] = row

    action_rates = {
        action: success_rate([row for row in results if row["action"] == action])
        for action in ACTIONS
    }
    non_stop_actions = [action for action in ACTIONS if action != "stop"]
    best_static_action = max(non_stop_actions, key=lambda action: action_rates[action])
    best_static_rate = action_rates[best_static_action]
    oracle_successes = 0
    true_feedback_successes = 0
    shuffled_feedback_successes = 0
    first_failures = 0
    expectation_matches = 0
    shuffled_map = {
        "expand_150": "second_stage_rescore",
        "expand_200": "base_rescue_8",
        "base_rescue": "expand_150",
        "second_stage": "expand_200",
        "unsolved_grid": "expand_150",
    }
    true_map = {
        "expand_150": "expand_150",
        "expand_200": "expand_200",
        "base_rescue": "base_rescue_8",
        "second_stage": "second_stage_rescore",
        "unsolved_grid": "stop",
    }
    for goal in goals:
        rows = by_goal[goal.goal_id]
        oracle_successes += int(any(rows[action]["verified"] for action in non_stop_actions))
        true_feedback_successes += int(rows[true_map[goal.family]]["verified"])
        shuffled_feedback_successes += int(rows[shuffled_map[goal.family]]["verified"])
        first_failures += int(not rows["keep"]["verified"])
        expectation_matches += int(
            goal.family == "unsolved_grid"
            or rows[goal.expected_best_action]["verified"]
        )

    n = len(goals)
    return {
        "n_goals": n,
        "n_attempts": len(results),
        "first_failure_rate": first_failures / n if n else 0.0,
        "action_success_rates": action_rates,
        "best_static_action": best_static_action,
        "best_static_rate": best_static_rate,
        "oracle_adaptive_rate": oracle_successes / n if n else 0.0,
        "true_feedback_policy_rate": true_feedback_successes / n if n else 0.0,
        "shuffled_feedback_policy_rate": shuffled_feedback_successes / n if n else 0.0,
        "expected_action_hit_rate": expectation_matches / n if n else 0.0,
        "oracle_minus_best_static_pp": 100.0 * ((oracle_successes / n) - best_static_rate) if n else 0.0,
        "true_minus_best_static_pp": 100.0 * ((true_feedback_successes / n) - best_static_rate) if n else 0.0,
        "true_minus_shuffled_pp": 100.0 * ((true_feedback_successes - shuffled_feedback_successes) / n) if n else 0.0,
    }


def write_markdown(payload: dict[str, Any], out: Path) -> None:
    summary = payload["summary"]
    lines: list[str] = []
    lines.append("# Gate 2 Mathlib-Context LeanHammer Action Grid")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Hammer root: `{payload['hammer_root']}`")
    lines.append(f"- Mathlib root: `{payload['mathlib_root']}`")
    lines.append(f"- Lean version: `{payload['lean_version']}`")
    lines.append(f"- Goals: {summary['n_goals']}")
    lines.append(f"- Attempts: {summary['n_attempts']}")
    lines.append(f"- First failure rate: {100.0 * summary['first_failure_rate']:.1f}%")
    lines.append("")
    lines.append("## Headroom")
    lines.append("")
    lines.append(f"- Oracle adaptive: {100.0 * summary['oracle_adaptive_rate']:.1f}%")
    lines.append(f"- True feedback policy: {100.0 * summary['true_feedback_policy_rate']:.1f}%")
    lines.append(f"- Best static: `{summary['best_static_action']}` at {100.0 * summary['best_static_rate']:.1f}%")
    lines.append(f"- Shuffled feedback: {100.0 * summary['shuffled_feedback_policy_rate']:.1f}%")
    lines.append(f"- Oracle - best static: {summary['oracle_minus_best_static_pp']:.1f} pp")
    lines.append(f"- True - best static: {summary['true_minus_best_static_pp']:.1f} pp")
    lines.append(f"- True - shuffled: {summary['true_minus_shuffled_pp']:.1f} pp")
    lines.append("")
    lines.append("## Action Success")
    lines.append("")
    lines.append("| Action | Success |")
    lines.append("|---|---:|")
    for action, rate in summary["action_success_rates"].items():
        lines.append(f"| `{action}` | {100.0 * rate:.1f}% |")
    lines.append("")
    lines.append("## Gate Readout")
    lines.append("")
    if payload["gate2_mathlib_passed"]:
        lines.append("- Mathlib-context Gate 2 passes for this theorem-family pilot: oracle adaptive headroom exceeds the 5 pp threshold under verified LeanHammer calls.")
        lines.append("- This is still a generated Mathlib-context pilot, not a final traced-corpus result.")
    else:
        lines.append("- Mathlib-context Gate 2 does not pass under the predeclared threshold. Do not escalate this route without redesign.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hammer-root", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--n-goals", type=int, default=100)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--first-k", type=int, default=3)
    parser.add_argument("--timeout-s", type=float, default=120.0)
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

    goals = generate_goals(args.n_goals)
    jobs = []
    for goal in goals:
        for action in ACTIONS:
            jobs.append((goal, action))

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [
            pool.submit(
                run_attempt,
                hammer_root=hammer_root,
                env=env,
                save_dir=save_dir,
                timeout_s=args.timeout_s,
                first_k=args.first_k,
                goal=goal,
                action=action,
            )
            for goal, action in jobs
        ]
        for future in as_completed(futures):
            row = future.result()
            results.append(row)
            print(
                f"{row['goal_id']}/{row['action']}: status={row['status']} verified={row['verified']}",
                flush=True,
            )

    action_order = {action: i for i, action in enumerate(ACTIONS)}
    goal_order = {goal.goal_id: i for i, goal in enumerate(goals)}
    results.sort(key=lambda row: (goal_order[row["goal_id"]], action_order[row["action"]]))
    summary = summarize(results, goals)
    gate2_passed = summary["oracle_minus_best_static_pp"] >= 5.0 and summary["first_failure_rate"] >= 0.95
    payload = {
        "experiment": "gate2_mathlib_context_leanhammer_action_grid",
        "hammer_root": str(hammer_root),
        "mathlib_root": str(mathlib_root),
        "save_dir": str(save_dir),
        "lean_version": lean_version,
        "n_goals": args.n_goals,
        "jobs": args.jobs,
        "first_k": args.first_k,
        "timeout_s": args.timeout_s,
        "gate2_mathlib_passed": gate2_passed,
        "verdict": "pass" if gate2_passed else "fail",
        "goals": [goal.__dict__ for goal in goals],
        "summary": summary,
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, out_md)
    print(out_md.read_text(encoding="utf-8"))
    print(f"wrote {out_json}")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
