"""Gate 2 verified LeanHammer action-grid pilot.

This is a small verified-backend headroom test: every action is evaluated by an
actual LeanHammer call with an explicit premise list. The generated goals are
synthetic propositional chains, but the terminal label is kernel verification
from `lake env lean`, not trace-core coverage.
"""

from __future__ import annotations

import argparse
import json
import math
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
class SyntheticGoal:
    goal_id: str
    family: str
    prelude: str
    target: str
    candidates: list[str]
    first_premises: list[str]
    base_rescue: list[str]
    second_stage: list[str]
    missing_core: str


def lean_ident(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")


def make_goal(idx: int, family: str) -> SyntheticGoal:
    ns = f"G{idx}"
    names = {
        "p0": f"{ns}_P0",
        "p1": f"{ns}_P1",
        "p2": f"{ns}_P2",
        "p3": f"{ns}_P3",
        "seed": f"{ns}_seed",
        "s01": f"{ns}_step01",
        "s12": f"{ns}_step12",
        "s23": f"{ns}_step23",
    }
    noises = [f"{ns}_noise_{j}" for j in range(10)]
    noise_props = [f"{ns}_NoiseProp_{j}" for j in range(10)]
    prelude_lines = [
        f"axiom {names['p0']} : Prop",
        f"axiom {names['p1']} : Prop",
        f"axiom {names['p2']} : Prop",
        f"axiom {names['p3']} : Prop",
        f"axiom {names['seed']} : {names['p0']}",
        f"axiom {names['s01']} : {names['p0']} -> {names['p1']}",
        f"axiom {names['s12']} : {names['p1']} -> {names['p2']}",
        f"axiom {names['s23']} : {names['p2']} -> {names['p3']}",
    ]
    for prop, noise in zip(noise_props, noises, strict=True):
        prelude_lines.append(f"axiom {prop} : Prop")
        prelude_lines.append(f"axiom {noise} : {prop}")

    first = [names["seed"], names["s01"], names["s12"]]
    missing = names["s23"]
    if family == "expand_150":
        candidates = first + [missing] + noises
        base_rescue = noises[:8]
        second_stage = noises[2:10]
    elif family == "expand_200":
        candidates = first + noises[:2] + [missing] + noises[2:]
        base_rescue = noises[:8]
        second_stage = noises[2:10]
    elif family == "base_rescue":
        candidates = first + noises[:8] + [missing] + noises[8:]
        base_rescue = [missing] + noises[:7]
        second_stage = noises[2:10]
    elif family == "second_stage":
        candidates = first + noises[:8] + [missing] + noises[8:]
        base_rescue = noises[:8]
        second_stage = [missing] + noises[:7]
    elif family == "unsolved_grid":
        candidates = first + noises
        base_rescue = noises[:8]
        second_stage = noises[2:10]
    else:
        raise ValueError(f"unknown family: {family}")

    return SyntheticGoal(
        goal_id=f"gate2_{idx:04d}_{family}",
        family=family,
        prelude="\n".join(prelude_lines),
        target=f"theorem {ns}_target : {names['p3']} := by",
        candidates=candidates,
        first_premises=first,
        base_rescue=base_rescue,
        second_stage=second_stage,
        missing_core=missing,
    )


def generate_goals(n_goals: int) -> list[SyntheticGoal]:
    families = ["expand_150", "expand_200", "base_rescue", "second_stage", "unsolved_grid"]
    return [make_goal(i, families[i % len(families)]) for i in range(n_goals)]


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        out.append(item)
        seen.add(item)
    return out


def action_premises(goal: SyntheticGoal, action: str, *, first_k: int) -> list[str]:
    if action == "stop":
        return []
    first = goal.first_premises[:first_k]
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


def render_attempt(goal: SyntheticGoal, premises: list[str]) -> str:
    return "\n".join(
        [
            "import Hammer",
            "",
            "set_option trace.hammer.premises true",
            "",
            goal.prelude,
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
    if "timeout" in low:
        return "timeout"
    if "failed to preprocess facts for translation" in low:
        return "translation_fail"
    if "aesop failed" in low or "tactic" in low or "unable to solve" in low:
        return "search_fail"
    return "lean_error"


def parse_trace(output: str) -> dict[str, str | None]:
    match = re.search(r"user input terms:\s*(.+)", output)
    return {"trace_user_input_terms": match.group(1).strip() if match else None}


def run_attempt(
    *,
    hammer_root: Path,
    save_dir: Path,
    timeout_s: float,
    first_k: int,
    goal: SyntheticGoal,
    action: str,
) -> dict[str, Any]:
    premises = action_premises(goal, action, first_k=first_k)
    if action == "stop":
        return {
            "goal_id": goal.goal_id,
            "family": goal.family,
            "action": action,
            "premises": premises,
            "premise_count": 0,
            "verified": False,
            "status": "stopped",
            "returncode": None,
            "time_s": 0.0,
            "lean_file": None,
            "output_tail": "",
            "trace_user_input_terms": None,
            "missing_core_in_premises": False,
        }

    file_name = f"{lean_ident(goal.goal_id)}__{lean_ident(action)}.lean"
    lean_file = save_dir / file_name
    lean_file.write_text(render_attempt(goal, premises), encoding="utf-8")
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
        return {
            "goal_id": goal.goal_id,
            "family": goal.family,
            "action": action,
            "premises": premises,
            "premise_count": len(premises),
            "verified": proc.returncode == 0,
            "status": classify(proc.returncode, output),
            "returncode": proc.returncode,
            "time_s": elapsed,
            "lean_file": str(lean_file),
            "output_tail": output[-2000:],
            "missing_core_in_premises": goal.missing_core in premises,
            **parse_trace(output),
        }
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - start
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return {
            "goal_id": goal.goal_id,
            "family": goal.family,
            "action": action,
            "premises": premises,
            "premise_count": len(premises),
            "verified": False,
            "status": "wrapper_timeout",
            "returncode": None,
            "time_s": elapsed,
            "lean_file": str(lean_file),
            "output_tail": output[-2000:],
            "missing_core_in_premises": goal.missing_core in premises,
            **parse_trace(output),
        }


def summarize(results: list[dict[str, Any]], n_goals: int) -> dict[str, Any]:
    by_action: dict[str, list[dict[str, Any]]] = {action: [] for action in ACTIONS}
    by_goal: dict[str, list[dict[str, Any]]] = {}
    for result in results:
        by_action[result["action"]].append(result)
        by_goal.setdefault(result["goal_id"], []).append(result)

    action_rows = []
    for action, rows in by_action.items():
        if not rows:
            continue
        action_rows.append(
            {
                "action": action,
                "n": len(rows),
                "verified": sum(1 for row in rows if row["verified"]),
                "success_rate": sum(1 for row in rows if row["verified"]) / len(rows),
                "avg_premises": sum(float(row["premise_count"]) for row in rows) / len(rows),
                "avg_time_s": sum(float(row["time_s"]) for row in rows) / len(rows),
            }
        )

    oracle_success = sum(1 for rows in by_goal.values() if any(row["verified"] for row in rows))
    best_static = max(action_rows, key=lambda row: row["success_rate"])
    keep = next(row for row in action_rows if row["action"] == "keep")
    return {
        "n_goals": n_goals,
        "n_attempts": len(results),
        "action_rows": action_rows,
        "oracle_success": oracle_success,
        "oracle_success_rate": oracle_success / n_goals if n_goals else 0.0,
        "best_static_action": best_static["action"],
        "best_static_success_rate": best_static["success_rate"],
        "oracle_gap_points": 100.0 * ((oracle_success / n_goals) - best_static["success_rate"]) if n_goals else 0.0,
        "keep_success_rate": keep["success_rate"],
    }


def write_markdown(payload: dict[str, Any], out: Path) -> None:
    summary = payload["summary"]

    def pct(x: float) -> str:
        return f"{100.0 * x:.1f}%"

    lines = []
    lines.append("# Gate 2 LeanHammer Action-Grid Pilot")
    lines.append("")
    lines.append("Every action below is evaluated by an actual LeanHammer call with an explicit premise list.")
    lines.append("")
    lines.append(f"- Goals: {summary['n_goals']}")
    lines.append(f"- Attempts: {summary['n_attempts']}")
    lines.append(f"- Oracle adaptive success: {pct(summary['oracle_success_rate'])}")
    lines.append(f"- Best static action: `{summary['best_static_action']}` at {pct(summary['best_static_success_rate'])}")
    lines.append(f"- Oracle gap over best static: {summary['oracle_gap_points']:+.1f} pp")
    lines.append("")
    lines.append("| Action | Goals | Verified | Success | Avg premises | Avg time |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in summary["action_rows"]:
        lines.append(
            f"| `{row['action']}` | {row['n']} | {row['verified']} | {pct(row['success_rate'])} | "
            f"{row['avg_premises']:.1f} | {row['avg_time_s']:.2f}s |"
        )
    lines.append("")
    verdict = "pass" if summary["oracle_gap_points"] >= 5.0 else "weak_or_fail"
    lines.append(f"Gate 2 pilot verdict: `{verdict}`.")
    lines.append("")
    lines.append("Caveat: this is a synthetic verified-backend pilot. It validates the action-grid mechanics and oracle-headroom computation, but Mathlib-scale evaluation is still required for a paper claim.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hammer-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--n-goals", type=int, default=50)
    parser.add_argument("--first-k", type=int, default=3)
    parser.add_argument("--timeout-s", type=float, default=60.0)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()

    args.hammer_root = args.hammer_root.resolve()
    args.save_dir = args.save_dir.resolve()
    args.out_json = args.out_json.resolve()
    args.out_md = args.out_md.resolve()
    args.save_dir.mkdir(parents=True, exist_ok=True)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    goals = generate_goals(args.n_goals)
    tasks = [
        {
            "hammer_root": args.hammer_root,
            "save_dir": args.save_dir,
            "timeout_s": args.timeout_s,
            "first_k": args.first_k,
            "goal": goal,
            "action": action,
        }
        for goal in goals
        for action in ACTIONS
    ]
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        future_to_task = {pool.submit(run_attempt, **task): task for task in tasks}
        for idx, future in enumerate(as_completed(future_to_task), start=1):
            result = future.result()
            results.append(result)
            print(
                f"[{idx}/{len(tasks)}] {result['goal_id']} {result['action']} "
                f"{result['status']} verified={result['verified']}",
                flush=True,
            )

    results.sort(key=lambda r: (r["goal_id"], ACTIONS.index(r["action"])))
    payload = {
        "experiment": "gate2_leanhammer_action_grid_pilot",
        "hammer_root": str(args.hammer_root),
        "save_dir": str(args.save_dir),
        "n_goals": args.n_goals,
        "first_k": args.first_k,
        "timeout_s": args.timeout_s,
        "actions": ACTIONS,
        "summary": summarize(results, args.n_goals),
        "results": results,
    }
    args.out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, args.out_md)
    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_md}")


if __name__ == "__main__":
    main()
