"""Run proof-action routing probes on replayable Mathlib 4.30 trace goals."""

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
    "disableAuto := true, disableAesop := false, disableGrind := true, "
    "aesopPremises := 0, autoPremises := 0, grindPremises := 0, "
    "solverTimeout := 2, wallclockTimeout := 5"
)


@dataclass(frozen=True)
class Action:
    name: str
    kind: str
    fact_pool: str = ""
    simp_pool: str = ""
    raw_tactic: str = ""


ACTIONS = [
    Action("hammer_empty", "hammer", fact_pool="empty"),
    Action("hammer_core_facts", "hammer", fact_pool="fact_core"),
    Action("hammer_core_plus_learned", "hammer", fact_pool="fact_core_plus_learned8"),
    Action("hammer_core_plus_learned16", "hammer", fact_pool="fact_core_plus_learned16"),
    Action("hammer_core_plus_learned32", "hammer", fact_pool="fact_core_plus_learned32"),
    Action("simp_empty", "simp", simp_pool="empty"),
    Action("simp_core", "simp", simp_pool="simp_core"),
    Action("simp_core_plus_learned", "simp", simp_pool="simp_core_plus_learned8"),
    Action("simp_core_plus_learned16", "simp", simp_pool="simp_core_plus_learned16"),
    Action("simp_core_plus_learned32", "simp", simp_pool="simp_core_plus_learned32"),
    Action("simpa_empty", "simpa", simp_pool="empty"),
    Action("simpa_core", "simpa", simp_pool="simp_core"),
    Action("simpa_core_plus_learned", "simpa", simp_pool="simp_core_plus_learned8"),
    Action("simpa_core_plus_learned16", "simpa", simp_pool="simp_core_plus_learned16"),
    Action("simpa_core_plus_learned32", "simpa", simp_pool="simp_core_plus_learned32"),
    Action("simp_only_core", "simp_only", simp_pool="simp_core"),
    Action("simp_only_core_plus_learned", "simp_only", simp_pool="simp_core_plus_learned8"),
    Action("rw_core", "rw", simp_pool="simp_core"),
    Action("rw_core_plus_learned", "rw", simp_pool="simp_core_plus_learned8"),
    Action("rw_core_then_simp", "rw_simp", simp_pool="simp_core"),
    Action("rw_core_plus_learned_then_simp", "rw_simp", simp_pool="simp_core_plus_learned8"),
    Action("simp_all_core", "simp_all", simp_pool="simp_core"),
    Action("simp_all_core_plus_learned", "simp_all", simp_pool="simp_core_plus_learned8"),
    Action("simp_all_core_plus_learned16", "simp_all", simp_pool="simp_core_plus_learned16"),
    Action("simp_all_core_plus_learned32", "simp_all", simp_pool="simp_core_plus_learned32"),
    Action("simp_rw_core", "simp_rw", simp_pool="simp_core"),
    Action("simp_rw_core_plus_learned", "simp_rw", simp_pool="simp_core_plus_learned8"),
    Action("simp_rw_core_then_simp", "simp_rw_simp", simp_pool="simp_core"),
    Action("simp_rw_core_plus_learned_then_simp", "simp_rw_simp", simp_pool="simp_core_plus_learned8"),
    Action("solve_by_elim_core", "solve_by_elim", fact_pool="fact_core"),
    Action("solve_by_elim_core_plus_learned", "solve_by_elim", fact_pool="fact_core_plus_learned8"),
    Action("solve_by_elim_core_plus_learned16", "solve_by_elim", fact_pool="fact_core_plus_learned16"),
    Action("solve_by_elim_core_plus_learned32", "solve_by_elim", fact_pool="fact_core_plus_learned32"),
    Action("hammerCore_core", "hammerCore", fact_pool="fact_core", simp_pool="simp_core"),
    Action(
        "hammerCore_core_plus_learned",
        "hammerCore",
        fact_pool="fact_core_plus_learned8",
        simp_pool="simp_core_plus_learned8",
    ),
    Action(
        "hammerCore_core_plus_learned16",
        "hammerCore",
        fact_pool="fact_core_plus_learned16",
        simp_pool="simp_core_plus_learned16",
    ),
    Action(
        "hammerCore_core_plus_learned32",
        "hammerCore",
        fact_pool="fact_core_plus_learned32",
        simp_pool="simp_core_plus_learned32",
    ),
    Action("aesop_empty", "aesop", fact_pool="empty", simp_pool="empty"),
    Action("aesop_core", "aesop", fact_pool="fact_core", simp_pool="simp_core"),
    Action("aesop_core_facts", "aesop", fact_pool="fact_core", simp_pool="empty"),
    Action("aesop_core_simps", "aesop", fact_pool="empty", simp_pool="simp_core"),
    Action("aesop_core_plus_learned", "aesop", fact_pool="fact_core_plus_learned8", simp_pool="simp_core_plus_learned8"),
    Action("aesop_core_plus_learned_facts", "aesop", fact_pool="fact_core_plus_learned8", simp_pool="empty"),
    Action("aesop_core_plus_learned_simps", "aesop", fact_pool="empty", simp_pool="simp_core_plus_learned8"),
    Action("aesop_core_plus_learned16", "aesop", fact_pool="fact_core_plus_learned16", simp_pool="simp_core_plus_learned16"),
    Action("aesop_core_plus_learned16_facts", "aesop", fact_pool="fact_core_plus_learned16", simp_pool="empty"),
    Action("aesop_core_plus_learned16_simps", "aesop", fact_pool="empty", simp_pool="simp_core_plus_learned16"),
    Action("aesop_core_plus_learned32", "aesop", fact_pool="fact_core_plus_learned32", simp_pool="simp_core_plus_learned32"),
    Action("aesop_core_plus_learned32_facts", "aesop", fact_pool="fact_core_plus_learned32", simp_pool="empty"),
    Action("aesop_core_plus_learned32_simps", "aesop", fact_pool="empty", simp_pool="simp_core_plus_learned32"),
    Action("aesop_learned8", "aesop", fact_pool="fact_learned8", simp_pool="simp_learned8"),
    Action("aesop_learned8_facts", "aesop", fact_pool="fact_learned8", simp_pool="empty"),
    Action("aesop_learned8_simps", "aesop", fact_pool="empty", simp_pool="simp_learned8"),
    Action("aesop_learned16", "aesop", fact_pool="fact_learned16", simp_pool="simp_learned16"),
    Action("aesop_learned16_facts", "aesop", fact_pool="fact_learned16", simp_pool="empty"),
    Action("aesop_learned16_simps", "aesop", fact_pool="empty", simp_pool="simp_learned16"),
    Action("aesop_learned32", "aesop", fact_pool="fact_learned32", simp_pool="simp_learned32"),
    Action("aesop_learned32_facts", "aesop", fact_pool="fact_learned32", simp_pool="empty"),
    Action("aesop_learned32_simps", "aesop", fact_pool="empty", simp_pool="simp_learned32"),
    Action("omega_empty", "raw", raw_tactic="omega"),
    Action("linarith_empty", "raw", raw_tactic="linarith"),
    Action("nlinarith_empty", "raw", raw_tactic="nlinarith"),
    Action("ring_nf_empty", "raw", raw_tactic="ring_nf"),
    Action("norm_num_empty", "raw", raw_tactic="norm_num"),
]


def run_cmd(
    cmd: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout_s: float,
) -> dict[str, Any]:
    def as_text(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return str(value)

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
        stdout = as_text(exc.stdout)
        stderr = as_text(exc.stderr)
        output = (stdout + "\n" + stderr).strip()
        return {
            "returncode": None,
            "success": False,
            "time_s": time.perf_counter() - start,
            "stdout": stdout,
            "stderr": stderr,
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


def strip_dangling_attributes(lines: list[str]) -> list[str]:
    out = list(lines)
    while out and out[-1].lstrip().startswith("@["):
        out.pop()
    return out


def candidate_records(row: dict[str, Any], n: int) -> list[dict[str, Any]]:
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

    top = sorted(candidates, key=key)[:n]
    by_name: dict[str, dict[str, Any]] = {str(c.get("name", "")): c for c in candidates}
    for name in row.get("proof_core", []) or []:
        if name and name not in by_name:
            top.append({"name": str(name), "features": {}, "tags": ["proof_core_only"]})
    return top


def selected_names_for_check(row: dict[str, Any], max_candidates: int) -> list[str]:
    proof_core = [str(p) for p in row.get("proof_core", []) if p]
    learned = [str(c.get("name", "")) for c in candidate_records(row, max_candidates)]
    return unique(proof_core + learned)


def check_available_names(
    *,
    row: dict[str, Any],
    names: list[str],
    source_lines: list[str],
    mathlib_root: Path,
    env: dict[str, str],
    check_dir: Path,
    idx: int,
    timeout_s: float,
) -> tuple[set[str], dict[str, Any]]:
    metadata = row.get("metadata") or {}
    start = metadata.get("start") or []
    if not names or len(start) < 1:
        return set(), {"status": "no_names_or_missing_span", "checked": 0, "available": 0}
    prefix = strip_dangling_attributes(source_lines[: int(start[0]) - 1])
    prefix = normalize_imports_for_probe(prefix)
    check_lines = list(prefix)
    if check_lines and check_lines[-1].strip():
        check_lines.append("\n")
    line_to_name: dict[int, str] = {}
    for name in names:
        check_lines.append(f"-- FA_CHECK {name}\n")
        check_lines.append(f"#check {name}\n")
        line_to_name[len(check_lines)] = name
    check_file = check_dir / f"context_check_{idx:04d}.lean"
    check_file.write_text("".join(check_lines), encoding="utf-8")
    result = run_cmd(["lean", str(check_file)], cwd=mathlib_root, env=env, timeout_s=timeout_s)
    full_output = ((result.get("stdout") or "") + "\n" + (result.get("stderr") or "")).strip()
    failed_lines: set[int] = set()
    for match in re.finditer(r":(\d+):\d+:\s+error", full_output):
        failed_lines.add(int(match.group(1)))
    available = {name for line_no, name in line_to_name.items() if line_no not in failed_lines}
    return available, {
        "status": "ok" if result["success"] else "some_names_unavailable",
        "returncode": result["returncode"],
        "time_s": result["time_s"],
        "checked": len(names),
        "available": len(available),
        "failed": len(names) - len(available),
        "output_tail": result["output_tail"][-3000:],
        "check_file": str(check_file),
    }


def build_pools(row: dict[str, Any], available: set[str], max_candidates: int) -> dict[str, list[str]]:
    candidates = candidate_records(row, max_candidates)
    by_name = {str(c.get("name", "")): c for c in candidates}
    proof_core = unique([str(p) for p in row.get("proof_core", []) if p and str(p) in available])

    learned_records = [c for c in candidates if str(c.get("name", "")) in available]
    fact_learned: list[str] = []
    simp_learned: list[str] = []
    for candidate in learned_records:
        name = str(candidate.get("name", ""))
        features = candidate.get("features") or {}
        tags = candidate.get("tags") or []
        if features.get("is_theorem_like") and not features.get("is_def_like"):
            fact_learned.append(name)
        if features.get("has_simp_attr") or "rewrite" in tags or "lean_friendly" in tags or features.get("is_def_like"):
            simp_learned.append(name)

    fact_core: list[str] = []
    for name in proof_core:
        features = (by_name.get(name) or {}).get("features") or {}
        if not features or features.get("is_theorem_like") or name in row.get("proof_core", []):
            fact_core.append(name)

    return {
        "empty": [],
        "fact_core": unique(fact_core),
        "fact_learned8": unique(fact_learned[:8]),
        "fact_learned16": unique(fact_learned[:16]),
        "fact_learned32": unique(fact_learned[:32]),
        "fact_core_plus_learned8": unique(fact_core + fact_learned[:8]),
        "fact_core_plus_learned16": unique(fact_core + fact_learned[:16]),
        "fact_core_plus_learned32": unique(fact_core + fact_learned[:32]),
        "simp_core": proof_core,
        "simp_learned8": unique(simp_learned[:8]),
        "simp_learned16": unique(simp_learned[:16]),
        "simp_learned32": unique(simp_learned[:32]),
        "simp_core_plus_learned8": unique(proof_core + simp_learned[:8]),
        "simp_core_plus_learned16": unique(proof_core + simp_learned[:16]),
        "simp_core_plus_learned32": unique(proof_core + simp_learned[:32]),
    }


def render_action(action: Action, pools: dict[str, list[str]]) -> tuple[str, list[str], list[str]]:
    facts = pools.get(action.fact_pool, [])
    simps = pools.get(action.simp_pool, [])
    fact_text = ", ".join(facts)
    simp_text = ", ".join(simps)
    if action.kind == "hammer":
        return f"hammer [{fact_text}] {{{HAMMER_OPTIONS}}}", facts, []
    if action.kind == "simp":
        if simps:
            return f"simp [{simp_text}]", [], simps
        return "simp", [], []
    if action.kind == "simpa":
        if simps:
            return f"simpa [{simp_text}]", [], simps
        return "simpa", [], []
    if action.kind == "simp_only":
        if simps:
            return f"simp only [{simp_text}]", [], simps
        return "skip", [], []
    if action.kind == "rw":
        if simps:
            return f"rw [{simp_text}]", [], simps
        return "skip", [], []
    if action.kind == "rw_simp":
        if simps:
            return f"rw [{simp_text}] <;> simp", [], simps
        return "skip", [], []
    if action.kind == "simp_all":
        if simps:
            return f"simp_all [{simp_text}]", [], simps
        return "simp_all", [], []
    if action.kind == "simp_rw":
        if simps:
            return f"simp_rw [{simp_text}]", [], simps
        return "skip", [], []
    if action.kind == "simp_rw_simp":
        if simps:
            return f"simp_rw [{simp_text}] <;> simp", [], simps
        return "skip", [], []
    if action.kind == "solve_by_elim":
        if facts:
            return f"solve_by_elim [{fact_text}]", facts, []
        return "solve_by_elim", [], []
    if action.kind == "hammerCore":
        return f"hammerCore [{simp_text}] [{fact_text}] {{{HAMMER_OPTIONS}}}", facts, simps
    if action.kind == "aesop":
        clauses: list[str] = []
        if simps:
            clauses.append(f"(add simp [{simp_text}])")
        if facts:
            clauses.append(f"(add safe [{fact_text}])")
        if clauses:
            return "aesop " + " ".join(clauses), facts, simps
        return "aesop", [], []
    if action.kind == "raw":
        return action.raw_tactic, [], []
    raise ValueError(f"unknown action kind: {action.kind}")


def patch_theorem_block(
    *,
    source_lines: list[str],
    start_line: int,
    end_line: int,
    tactic_line: str,
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
    new_block = prefix.rstrip() + "\n" + f"  {tactic_line}\n"
    patched = source_lines[: start_line - 1] + [new_block] + source_lines[end_line:]
    return insert_hammer_prelude(patched), None


def classify(returncode: int | None, output: str) -> str:
    low = output.lower()
    if "declaration uses `sorry`" in low or "declaration uses 'sorry'" in low:
        return "sorry_warning"
    if returncode == 0:
        return "proved"
    if returncode is None or "timeout" in low:
        return "timeout"
    if "unexpected token" in low:
        return "parse_error"
    if "erroneous invocation of hammer" in low:
        return "bad_hammer_config"
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
    if "aesop failed" in low or "tactic" in low or "unable to solve" in low or "error: failed" in low:
        return "search_fail"
    return "lean_error"


def lean_ident(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_") or "goal"


def run_attempt(
    *,
    row: dict[str, Any],
    goal_index: int,
    action: Action,
    pools: dict[str, list[str]],
    source_lines: list[str],
    mathlib_root: Path,
    hammer_root: Path,
    env: dict[str, str],
    save_dir: Path,
    timeout_s: float,
) -> dict[str, Any]:
    metadata = row.get("metadata") or {}
    start = metadata.get("start") or []
    end = metadata.get("end") or []
    tactic_line, facts, simps = render_action(action, pools)
    base = {
        "goal_id": row.get("goal_id", ""),
        "theorem": metadata.get("theorem", ""),
        "file_path": metadata.get("file_path", ""),
        "action": action.name,
        "kind": action.kind,
        "fact_count": len(facts),
        "simp_count": len(simps),
        "facts": facts,
        "simps": simps,
        "tactic_line": tactic_line,
    }
    if tactic_line == "skip":
        return {
            **base,
            "verified": False,
            "nonempty": False,
            "status": "skipped_empty_action",
            "time_s": 0.0,
            "returncode": 0,
            "patched_file": None,
            "output_tail": "",
        }
    if len(start) < 1 or len(end) < 1:
        return {**base, "verified": False, "status": "missing_span", "time_s": 0.0}
    patched, patch_error = patch_theorem_block(
        source_lines=source_lines,
        start_line=int(start[0]),
        end_line=int(end[0]),
        tactic_line=tactic_line,
    )
    if patch_error or patched is None:
        return {**base, "verified": False, "status": patch_error, "time_s": 0.0}
    out_file = save_dir / f"action_matrix_{goal_index:04d}_{lean_ident(action.name)}.lean"
    out_file.write_text("".join(patched), encoding="utf-8")
    result = run_cmd(["lean", str(out_file)], cwd=hammer_root, env=env, timeout_s=timeout_s)
    output = ((result.get("stdout") or "") + "\n" + (result.get("stderr") or "")).strip()
    status = classify(result["returncode"], output)
    verified = result["success"] and status == "proved"
    return {
        **base,
        "verified": verified,
        "nonempty": bool(facts or simps),
        "status": status,
        "time_s": result["time_s"],
        "returncode": result["returncode"],
        "patched_file": str(out_file),
        "output_tail": result["output_tail"],
    }


def summarize(results: list[dict[str, Any]], availability: list[dict[str, Any]]) -> dict[str, Any]:
    by_goal: dict[str, dict[str, Any]] = {}
    by_action: dict[str, dict[str, int]] = {}
    status_counts: dict[str, int] = {}
    for result in results:
        status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1
        action_summary = by_action.setdefault(result["action"], {"attempts": 0, "verified": 0, "nonempty_verified": 0})
        action_summary["attempts"] += 1
        action_summary["verified"] += int(result["verified"])
        action_summary["nonempty_verified"] += int(result["verified"] and result["nonempty"])
        goal_summary = by_goal.setdefault(
            result["goal_id"],
            {"theorem": result["theorem"], "attempts": 0, "verified": 0, "nonempty_verified": 0, "empty_verified": 0, "best": None},
        )
        goal_summary["attempts"] += 1
        goal_summary["verified"] += int(result["verified"])
        goal_summary["nonempty_verified"] += int(result["verified"] and result["nonempty"])
        goal_summary["empty_verified"] += int(result["verified"] and not result["nonempty"])
        if result["verified"] and goal_summary["best"] is None:
            goal_summary["best"] = {
                "action": result["action"],
                "kind": result["kind"],
                "fact_count": result["fact_count"],
                "simp_count": result["simp_count"],
                "time_s": result["time_s"],
            }
    action_dependent_goals = sum(
        1 for row in by_goal.values() if row["nonempty_verified"] > 0 and row["empty_verified"] == 0
    )
    return {
        "n_goals": len(by_goal),
        "n_attempts": len(results),
        "n_verified_attempts": sum(1 for row in results if row["verified"]),
        "n_nonempty_verified_attempts": sum(1 for row in results if row["verified"] and row["nonempty"]),
        "n_verified_goals": sum(1 for row in by_goal.values() if row["verified"] > 0),
        "n_nonempty_verified_goals": sum(1 for row in by_goal.values() if row["nonempty_verified"] > 0),
        "n_action_dependent_goals": action_dependent_goals,
        "status_counts": status_counts,
        "by_action": by_action,
        "by_goal": by_goal,
        "availability": availability,
    }


def write_md(payload: dict[str, Any], out: Path) -> None:
    summary = payload["summary"]
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Replayable-Subset Proof-Action Matrix")
    lines.append("")
    lines.append(f"- Verdict: `{payload['verdict']}`")
    lines.append(f"- Replay filter: `{payload['replay_json']}`")
    lines.append(f"- Replayable goals evaluated: {summary['n_goals']}")
    lines.append(f"- Attempts: {summary['n_attempts']}")
    lines.append(f"- Verified attempts: {summary['n_verified_attempts']}")
    lines.append(f"- Non-empty-premise verified attempts: {summary['n_nonempty_verified_attempts']}")
    lines.append(f"- Goals with any proof: {summary['n_verified_goals']}")
    lines.append(f"- Goals with non-empty-premise proof: {summary['n_nonempty_verified_goals']}")
    lines.append(f"- Action-dependent goals: {summary['n_action_dependent_goals']}")
    lines.append("")
    lines.append("## Status Counts")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---:|")
    for status, count in sorted(summary["status_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.append("")
    lines.append("## By Action")
    lines.append("")
    lines.append("| Action | Verified | Non-empty verified | Attempts |")
    lines.append("|---|---:|---:|---:|")
    for action, row in sorted(summary["by_action"].items()):
        lines.append(f"| `{action}` | {row['verified']} | {row['nonempty_verified']} | {row['attempts']} |")
    lines.append("")
    lines.append("## By Goal")
    lines.append("")
    lines.append("| Goal | Verified | Non-empty verified | Empty verified | Best |")
    lines.append("|---|---:|---:|---:|---|")
    for goal_id, row in summary["by_goal"].items():
        best = row.get("best")
        best_text = "none"
        if best:
            best_text = f"`{best['action']}` ({best['fact_count']} facts, {best['simp_count']} simps)"
        lines.append(
            f"| `{goal_id}` | {row['verified']} | {row['nonempty_verified']} | {row['empty_verified']} | {best_text} |"
        )
    lines.append("")
    lines.append("## Availability")
    lines.append("")
    lines.append("| Goal | Checked | Available | Failed |")
    lines.append("|---|---:|---:|---:|")
    for row in summary["availability"]:
        lines.append(f"| `{row['goal_id']}` | {row['checked']} | {row['available']} | {row['failed']} |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    if summary["n_action_dependent_goals"]:
        lines.append("- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.")
    elif summary["n_nonempty_verified_goals"]:
        lines.append("- Non-empty-premise proofs exist, but empty baselines also solve those goals; scale cautiously and separate easy goals.")
    else:
        lines.append("- No non-empty-premise proof was found; inspect action failures before scaling.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--replay-json", type=Path, required=True)
    parser.add_argument("--mathlib-root", type=Path, required=True)
    parser.add_argument("--hammer-root", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--check-dir", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=10)
    parser.add_argument("--goal-offset", type=int, default=0)
    parser.add_argument("--max-candidates", type=int, default=32)
    parser.add_argument("--action-names", nargs="*", default=None)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--timeout-s", type=float, default=180.0)
    args = parser.parse_args()

    input_jsonl = args.input_jsonl.resolve()
    replay_json = args.replay_json.resolve()
    mathlib_root = args.mathlib_root.resolve()
    hammer_root = args.hammer_root.resolve()
    save_dir = args.save_dir.resolve()
    check_dir = args.check_dir.resolve()
    out_json = args.out_json.resolve()
    out_md = args.out_md.resolve()
    save_dir.mkdir(parents=True, exist_ok=True)
    check_dir.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    replay_verified = load_replay_verified_goal_ids(replay_json)
    rows = [row for row in load_jsonl(input_jsonl) if row.get("goal_id") in replay_verified]
    if args.goal_offset:
        if args.goal_offset < 0:
            raise ValueError("--goal-offset must be non-negative")
        rows = rows[args.goal_offset :]
    rows = rows[: args.max_goals] if args.max_goals else rows
    if not rows:
        raise ValueError("no replay-verified goals selected")
    actions = ACTIONS
    if args.action_names:
        wanted = set(args.action_names)
        actions = [action for action in ACTIONS if action.name in wanted]
        missing = sorted(wanted - {action.name for action in actions})
        if missing:
            raise ValueError(f"unknown action names: {missing}")
        if not actions:
            raise ValueError("no actions selected")

    env = os.environ.copy()
    env["LEAN_PATH"] = f"{lake_lean_path(hammer_root, args.timeout_s)}:{lake_lean_path(mathlib_root, args.timeout_s)}"

    prepared: list[dict[str, Any]] = []
    availability_rows: list[dict[str, Any]] = []
    for idx, row in enumerate(rows):
        metadata = row.get("metadata") or {}
        source_file = mathlib_root / str(metadata.get("file_path", ""))
        source_lines = source_file.read_text(encoding="utf-8").splitlines(keepends=True)
        names = selected_names_for_check(row, args.max_candidates)
        available, check = check_available_names(
            row=row,
            names=names,
            source_lines=source_lines,
            mathlib_root=mathlib_root,
            env=env,
            check_dir=check_dir,
            idx=idx,
            timeout_s=args.timeout_s,
        )
        pools = build_pools(row, available, args.max_candidates)
        availability_rows.append(
            {
                "goal_id": row.get("goal_id", ""),
                "theorem": metadata.get("theorem", ""),
                **{k: v for k, v in check.items() if k != "output_tail"},
                "pool_sizes": {name: len(items) for name, items in pools.items()},
            }
        )
        prepared.append({"row": row, "source_lines": source_lines, "pools": pools})
        print(
            f"context {row.get('goal_id', '')}: {check['available']}/{check['checked']} names available",
            flush=True,
        )

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = []
        for goal_index, item in enumerate(prepared):
            for action in actions:
                futures.append(
                    pool.submit(
                        run_attempt,
                        row=item["row"],
                        goal_index=goal_index,
                        action=action,
                        pools=item["pools"],
                        source_lines=item["source_lines"],
                        mathlib_root=mathlib_root,
                        hammer_root=hammer_root,
                        env=env,
                        save_dir=save_dir,
                        timeout_s=args.timeout_s,
                    )
                )
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"{result['goal_id']} {result['action']}: {result['status']}", flush=True)

    goal_order = {row.get("goal_id", ""): i for i, row in enumerate(rows)}
    action_order = {action.name: i for i, action in enumerate(actions)}
    results.sort(key=lambda row: (goal_order.get(row["goal_id"], 0), action_order.get(row["action"], 0)))
    summary = summarize(results, availability_rows)
    verdict = (
        "pass_action_dependent"
        if summary["n_action_dependent_goals"]
        else "partial_nonempty_positive"
        if summary["n_nonempty_verified_goals"]
        else "no_nonempty_positive"
    )
    payload = {
        "experiment": "mathlib430_pretheorem_action_matrix",
        "input_jsonl": str(input_jsonl),
        "replay_json": str(replay_json),
        "mathlib_root": str(mathlib_root),
        "hammer_root": str(hammer_root),
        "save_dir": str(save_dir),
        "check_dir": str(check_dir),
        "max_goals": args.max_goals,
        "goal_offset": args.goal_offset,
        "max_candidates": args.max_candidates,
        "action_names": [action.name for action in actions],
        "verdict": verdict,
        "summary": summary,
        "results": results,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_md(payload, out_md)
    print(out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
