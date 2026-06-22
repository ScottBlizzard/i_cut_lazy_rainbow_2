"""Build a cleaned Mathlib 4.30-compatible trace subset after preflight."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_md(payload: dict[str, Any], out: Path) -> None:
    lines: list[str] = []
    lines.append("# Mathlib 4.30 Clean Trace Subset")
    lines.append("")
    lines.append(f"- Input: `{payload['input_jsonl']}`")
    lines.append(f"- Preflight: `{payload['preflight_json']}`")
    lines.append(f"- Output JSONL: `{payload['out_jsonl']}`")
    lines.append(f"- Input goals: {payload['input_goals']}")
    lines.append(f"- Clean goals: {payload['clean_goals']}")
    lines.append(f"- Dropped goals: {payload['dropped_goals']}")
    lines.append(f"- Removed circular target candidates: {payload['removed_target_candidates']}")
    lines.append("")
    lines.append("## Drop Reasons")
    lines.append("")
    lines.append("| Reason | Count |")
    lines.append("|---|---:|")
    for reason, count in payload["drop_reasons"].items():
        lines.append(f"| `{reason}` | {count} |")
    lines.append("")
    lines.append("## Readout")
    lines.append("")
    lines.append("- This subset removes direct target-theorem leakage from candidate lists.")
    lines.append("- It is only a data-cleaning step. Standalone elaboration and pre-theorem replay are still required before this becomes a verified traced-corpus benchmark.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, required=True)
    parser.add_argument("--preflight-json", type=Path, required=True)
    parser.add_argument("--out-jsonl", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=0)
    args = parser.parse_args()

    input_jsonl = args.input_jsonl.resolve()
    preflight_json = args.preflight_json.resolve()
    out_jsonl = args.out_jsonl.resolve()
    out_md = args.out_md.resolve()
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl(input_jsonl)
    preflight = json.loads(preflight_json.read_text(encoding="utf-8"))
    records = {row["goal_id"]: row for row in preflight["goals"]}
    clean: list[dict[str, Any]] = []
    drop_reasons: dict[str, int] = {}
    removed_target_candidates = 0

    for row in rows:
        goal_id = row.get("goal_id", "")
        record = records.get(goal_id)
        if record is None:
            drop_reasons["not_in_preflight"] = drop_reasons.get("not_in_preflight", 0) + 1
            continue
        reason = None
        if not record.get("file_exists"):
            reason = "missing_file_in_mathlib430"
        elif not record.get("theorem_exists_in_mathlib430"):
            reason = "missing_theorem_in_mathlib430"
        elif not record.get("all_proof_core_exists_in_mathlib430"):
            reason = "missing_proof_core_in_mathlib430"
        elif record.get("target_name_in_proof_core"):
            reason = "target_name_in_proof_core"
        if reason is not None:
            drop_reasons[reason] = drop_reasons.get(reason, 0) + 1
            continue

        theorem = record.get("theorem", "")
        new_row = dict(row)
        candidates = []
        for candidate in row.get("candidates", []):
            if isinstance(candidate, dict) and candidate.get("name") == theorem:
                removed_target_candidates += 1
                continue
            candidates.append(candidate)
        new_row["candidates"] = candidates
        new_row.setdefault("metadata", {})["mathlib430_cleaned"] = True
        new_row["metadata"]["target_candidate_removed"] = True
        clean.append(new_row)
        if args.max_goals and len(clean) >= args.max_goals:
            break

    with out_jsonl.open("w", encoding="utf-8") as handle:
        for row in clean:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    payload = {
        "input_jsonl": str(input_jsonl),
        "preflight_json": str(preflight_json),
        "out_jsonl": str(out_jsonl),
        "input_goals": len(rows),
        "clean_goals": len(clean),
        "dropped_goals": sum(drop_reasons.values()),
        "drop_reasons": drop_reasons,
        "removed_target_candidates": removed_target_candidates,
    }
    write_md(payload, out_md)
    print(out_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
