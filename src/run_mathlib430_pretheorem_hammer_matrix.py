"""Run a small LeanHammer matrix on replayable Mathlib 4.30 trace goals."""

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


@dataclass(frozen=True)
class HammerConfig:
    name: str
    options: str


HAMMER_CONFIGS = [
    HammerConfig(
        "aesop_5",
        "disableAuto := true, disableAesop := false, disableGrind := true, "
        "aesopPremises := 0, autoPremises := 0, grindPremises := 0, "
        "solverTimeout := 2, wallclockTimeout := 5",
    ),
    HammerConfig(
        "aesop_10",
        "disableAuto := true, disableAesop := false, disableGrind := true, "
        "aesopPremises := 0, autoPremises := 0, grindPremises := 0, "
        "solverTimeout := 4, wallclockTimeout := 10",
    ),
    HammerConfig(
        "aesop_grind_10",
        "disableAuto := true, disableAesop := false, disableGrind := false, "
        "aesopPremises := 0, autoPremises := 0, grindPremises := 0, "
        "solverTimeout := 4, wallclockTimeout := 10",
    ),
    HammerConfig(
        "grind_only_10",
        "disableAuto := true, disableAesop := true, disableGrind := false, "
        "aesopPremises := 0, autoPremises := 0, grindPremises := 0, "
        "solverTimeout := 4, wallclockTimeout := 10",
    ),
    HammerConfig(
        "auto_aesop_10",
        "disableAuto := false, disableAesop := false, disableGrind := true, "
        "aesopPremises := 0, autoPremises := 0, grindPremises := 0, "
        "solverTimeout := 4, wallclockTimeout := 10",
    ),
]


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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_replay_verified_goal_ids(path: Path) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {row["goal_id"] for row in payload.get("results", []) if row.get("verified")}


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


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


def insert_hammer_prelude(lines: list[str]) -> list[str]:
    lines = normalize_imports_for_probe(lines)
    last_import = -1
    for i, line in enumerate(lines):
        if line.startswith("import "):
            last_import = i
        elif last_import >= 0 and line.strip() and not line.startswith("import "):
            break
    out = list(lines)
    insert_at = last_import + 1
    if not any(line.strip() == "import Hammer" for line in out[: insert_at + 2]):
        out.insert(insert_at, "import Hammer\n")
        insert_at += 1
    if not any(line.strip() == "set_option trace.hammer.premises true" for line in out[: insert_at + 4]):
        out.insert(insert_at, "set_option trace.hammer.premises true\n")
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


def candidate_names_by_learned(row: dict[str, Any], n: int) -> list[str]:
    candidates = list(row.get("candidates") or [])

    def key(item: dict[str, Any]) -> tuple[float, float, str]:
        features = item.get("features") or {}
        rank = features.get("learned_rank")
        score = features.get("learned_score")
        return (
            float(rank) if rank is not None else 1e9,
            -float(score) if score is not None else 0.0,
            str(item.get("name", "")),
        )

    return unique([str(c.get("name", "")) for c in sorted(candidates, key=key)[:n]])


def candidate_names_by_base(row: dict[str, Any], n: int) -> list[str]:
    return unique([str(c.get("name", "")) for c in (row.get("candidates") or [])[:n]])


def candidate_names_same_file(row: dict[str, Any], n: int) -> list[str]:
    out: list[str] = []
    for candidate in row.get("candidates") or []:
        tags = candidate.get("tags") or []
        features = candidate.get("features") or {}
        if "same_file" in tags or features.get("same_file"):
            out.append(str(candidate.get("name", "")))
        if len(out) >= n:
            break
    return unique(out)


def premise_sets(row: dict[str, Any]) -> dict[str, list[str]]:
    proof_core = unique([str(p) for p in row.get("proof_core", []) if p])
    learned8 = candidate_names_by_learned(row, 8)
    learned16 = candidate_names_by_learned(row, 16)
    base8 = candidate_names_by_base(row, 8)
    same_file8 = candidate_names_same_file(row, 8)
    return {
        "empty": [],
        "proof_core": proof_core,
        "proof_core_plus_learned8": unique(proof_core + learned8),
        "learned16": learned16,
        "base8": base8,
        "same_file8_plus_core": unique(same_file8 + proof_core),
    }


def patch_theorem_block(
    *,
    source_lines: list[str],
    start_line: int,
    end_line: int,
    premises: list[str],
    config: HammerConfig,
) -> tuple[list[str] | None, str | None]:
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
    premise_text = ", ".join(premises)
    new_block = prefix.rstrip() + "\n" + f"  hammer [{premise_text}] {{{config.options}}}\n"
    patched = source_lines[: start_line - 1] + [new_block] + source_lines[end_line:]
    return insert_hammer_prelude(patched), None


def parse_trace(output: str) -> dict[str, str | None]:
    user = re.search(r"user input terms:\s*(.+)", output)
    selector = re.search(r"premises from premise selector:\s*(.+)", output)
    selector_deduped = re.search(r"premises from premise selector after removing duplicates in user input terms:\s*(.+)", output)
    return {
        "trace_user_input_terms": user.group(1).strip() if user else None,
        "trace_selector_premises": selector.group(1).strip() if selector else None,
        "trace_selector_premises_deduped": selector_deduped.group(1).strip() if selector_deduped else None,
    }


def classify(returncode: int | None, output: str) -> str:
    low = output.lower()
    if "declaration uses `sorry`" in low or "declaration uses 'sorry'" in low:
        return "sorry_warning"
    if returncode == 0:
        return "proved"
    if returncode is None or "timeout" in low:
        return "timeout"
    if "erroneous invocation of hammer" in low:
        return "bad_hammer_config"
    if "cannot find automatically downloaded zipperposition" in low:
        return "auto_backend_missing"
    if "failed to preprocess facts for translation" in low:
        return "translation_fail"
    if "unknown identifier" in low or "unknown constant" in low:
        return "unknown_identifier"
    if "failed to synthesize" in low or "failed to infer" in low or "typeclass" in low:
        return "typeclass_or_inference"
    if "application type mismatch" in low or "type mismatch" in low:
        return "type_mismatch"
    if "grind failed" in low:
        return "grind_fail"
    if "aesop failed" in low or "tactic" in low or "unable to solve" in low:
        return "search_fail"
    return "lean_error"


def lean_ident(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_") or "goal"


def run_attempt(
    *,
    row: dict[str, Any],
    goal_index: int,
    premise_name: str,
    premises: list[str],
    config: HammerConfig,
    mathlib_root: Path,
    hammer_root: Path,
    env: dict[str, str],
    save_dir: Path,
    timeout_s: float,
) -> dict[str, Any]:
    metadata = row.get("metadata") or {}
    goal_id = row.get("goal_id", "")
    theorem = metadata.get("theorem", "")
    file_path = metadata.get("file_path", "")
    start = metadata.get("start") or []
    end = metadata.get("end") or []
    base = {
        "goal_id": goal_id,
        "theorem": theorem,
        "file_path": file_path,
        "premise_set": premise_name,
        "premise_count": len(premises),
        "premises": premises,
        "config": config.name,
    }
    if len(start) < 1 or len(end) < 1:
        return {**base, "verified": False, "status": "missing_span", "time_s": 0.0}
    source_file = mathlib_root / file_path
    if not source_file.exists():
        return {**base, "verified": False, "status": "missing_source_file", "time_s": 0.0}
    source_lines = source_file.read_text(encoding="utf-8").splitlines(keepends=True)
    patched, patch_error = patch_theorem_block(
        source_lines=source_lines,
        start_line=int(start[0]),
        end_line=int(end[0]),
        premises=premises,
        config=config,
    )
    if patch_error or patched is None:
        return {**base, "verified": False, "status": patch_error, "time_s": 0.0}
    out_file = save_dir / (
        f"hammer_matrix_{goal_index:04d}_{lean_ident(premise_name)}_{lean_ident(config.name)}.lean"
    )
    out_file.write_text("".join(patched), encoding="utf-8")
    result = run_cmd(["lean", str(out_file)], cwd=hammer_root, env=env, timeout_s=timeout_s)
    output = ((result.get("stdout") or "") + "\n" + (result.get("stderr") or "")).strip()
    status = classify(result["returncode"], output)
    verified = result["success"] and status == "proved"
    return {
        **base,
        "verified": verified,
        "status": status,
        "time_s": result["time_s"],
        "returncode": result["returncode"],
        "patched_file": str(out_file),
        "output_tail": result["output_tail"],
        **parse_trace(output),
    }


def summarize(results: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    by_config: dict[str, dict[str, int]] = {}
    by_premise_set: dict[str, dict[str, int]] = {}
    by_goal: dict[str, dict[str, Any]] = {}
    for result in results:
        status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1
        config_summary = by_config.setdefault(result["config"], {"attempts": 0, "verified": 0})
        premise_summary = by_premise_set.setdefault(result["premise_set"], {"attempts": 0, "verified": 0})
        config_summary["attempts"] += 1
        premise_summary["attempts"] += 1
        config_summary["verified"] += int(result["verified"])
        premise_summary["verified"] += int(result["verified"])
        goal_summary = by_goal.setdefault(
            result["goal_id"],
            {
                "theorem": result["theorem"],
                "attempts": 0,
                "verified": 0,
                "best": None,
                "status_counts": {},
            },
        )
        goal_summary["attempts"] += 1
        goal_summary["verified"] += int(result["verified"])
        goal_summary["status_counts"][result["status"]] = goal_summary["status_counts"].get(result["status"], 0) + 1
        if result["verified"] and goal_summary["best"] is None:
            goal_summary["best"] = {
                "premise_set": result["premise_set"],
                "config": result["config"],
                "premise_count": result["premise_count"],
                "time_s": result["time_s"],
            }

    return {
        "n_goals": len(rows),
        "n_attempts": len(results),
        "n_verified_attempts": sum(1 for row in results if row["verified"]),
        "n_verified_goals": sum(1 for row in by_goal.values() if row["verified"] > 0),
        "status_counts": status_counts,
        "by_config": by_config,
        "by_premise_set": by_premise_set,
        "by_goal": by_goal,
    }


def write_md(payload: dict[str, Any], out: Path) -> None:
    summary = payload["summary"]
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Replayable-Subset Hammer Matrix")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Replay filter: `{payload['replay_json']}`")
    lines.append(f"- Replayable goals evaluated: {summary['n_goals']}")
    lines.append(f"- Hammer attempts: {summary['n_attempts']}")
    lines.append(f"- Verified Hammer attempts: {summary['n_verified_attempts']}")
    lines.append(f"- Goals with at least one Hammer proof: {summary['n_verified_goals']}")
    lines.append("")
    lines.append("## Status Counts")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---:|")
    for status, count in sorted(summary["status_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.append("")
    lines.append("## By Config")
    lines.append("")
    lines.append("| Config | Verified | Attempts |")
    lines.append("|---|---:|---:|")
    for name, row in sorted(summary["by_config"].items()):
        lines.append(f"| `{name}` | {row['verified']} | {row['attempts']} |")
    lines.append("")
    lines.append("## By Premise Set")
    lines.append("")
    lines.append("| Premise set | Verified | Attempts |")
    lines.append("|---|---:|---:|")
    for name, row in sorted(summary["by_premise_set"].items()):
        lines.append(f"| `{name}` | {row['verified']} | {row['attempts']} |")
    lines.append("")
    lines.append("## By Goal")
    lines.append("")
    lines.append("| Goal | Verified attempts | Best attempt |")
    lines.append("|---|---:|---|")
    for goal_id, row in summary["by_goal"].items():
        best = row.get("best")
        if best:
            best_text = f"`{best['premise_set']}` / `{best['config']}` / {best['premise_count']} premises"
        else:
            best_text = "none"
        lines.append(f"| `{goal_id}` | {row['verified']} | {best_text} |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    if summary["n_verified_goals"]:
        lines.append("- Hammer has at least one positive proof on a replayable traced theorem; scale this route on a larger replayable subset.")
    else:
        lines.append("- No Hammer positive was found on this replayable subset; inspect output tails and consider either stronger proof actions or a theorem-family/corpus redesign.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--replay-json", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--hammer-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=3)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--timeout-s", type=float, default=180.0)
    args = parser.parse_args()

    input_jsonl = args.input_jsonl.resolve()
    replay_json = args.replay_json.resolve()
    mathlib_root = args.mathlib_root.resolve()
    hammer_root = args.hammer_root.resolve()
    save_dir = args.save_dir.resolve()
    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    save_dir.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    replay_verified = load_replay_verified_goal_ids(replay_json)
    rows = [row for row in load_jsonl(input_jsonl) if row.get("goal_id") in replay_verified]
    rows = rows[: args.max_goals] if args.max_goals else rows
    if not rows:
        raise ValueError("no replay-verified goals selected")

    env = os.environ.copy()
    env["LEAN_PATH"] = f"{lake_lean_path(hammer_root, args.timeout_s)}:{lake_lean_path(mathlib_root, args.timeout_s)}"

    tasks: list[tuple[dict[str, Any], int, str, list[str], HammerConfig]] = []
    for goal_index, row in enumerate(rows):
        for premise_name, premises in premise_sets(row).items():
            for config in HAMMER_CONFIGS:
                tasks.append((row, goal_index, premise_name, premises, config))

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [
            pool.submit(
                run_attempt,
                row=row,
                goal_index=goal_index,
                premise_name=premise_name,
                premises=premises,
                config=config,
                mathlib_root=mathlib_root,
                hammer_root=hammer_root,
                env=env,
                save_dir=save_dir,
                timeout_s=args.timeout_s,
            )
            for row, goal_index, premise_name, premises, config in tasks
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"{result['goal_id']} {result['premise_set']} {result['config']}: {result['status']}",
                flush=True,
            )

    goal_order = {row.get("goal_id", ""): i for i, row in enumerate(rows)}
    results.sort(
        key=lambda row: (
            goal_order.get(row["goal_id"], 0),
            row["premise_set"],
            row["config"],
        )
    )
    summary = summarize(results, rows)
    payload = {
        "experiment": "mathlib430_pretheorem_hammer_matrix",
        "input_jsonl": str(input_jsonl),
        "replay_json": str(replay_json),
        "mathlib_root": str(mathlib_root),
        "hammer_root": str(hammer_root),
        "save_dir": str(save_dir),
        "max_goals": args.max_goals,
        "verdict": "pass" if summary["n_verified_goals"] else "no_hammer_positive_on_replayable_subset",
        "summary": summary,
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_md(payload, out_md)
    print(out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
