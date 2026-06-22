#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
GOALS="${1:-$ROOT/outputs/phase3_second_stage_eval_goals_500.jsonl}"
TRACE_RESULT="${2:-$ROOT/outputs/phase3_final_guardrail_eval_500_a40.json}"
BRIDGE_GOALS="${3:-$ROOT/outputs/phase3_bridge_goals_200.jsonl}"
MANIFEST="${4:-$ROOT/outputs/phase3_bridge_manifest_200.json}"
REPLAY_RESULT="${5:-$ROOT/outputs/phase3_bridge_replay_200.json}"
REPORT="${6:-$ROOT/outputs/phase3_bridge_report_200.md}"
MAX_GOALS="${7:-200}"
SECOND_POLICY="${8:-rule_far_learned_second_stage_final_base_guardrail_8}"
TAXONOMY_JSON="${9:-$ROOT/outputs/phase3_bridge_failure_taxonomy_200.json}"
TAXONOMY_MD="${10:-$ROOT/outputs/phase3_bridge_failure_taxonomy_200.md}"
NEG_JSON="${11:-$ROOT/outputs/phase3_bridge_negative_case_inspection_200.json}"
NEG_MD="${12:-$ROOT/outputs/phase3_bridge_negative_case_inspection_200.md}"

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda
source /root/.elan/env

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

python eval_phase1_trace_core.py \
  --goals "$GOALS" \
  --out "$TRACE_RESULT" \
  --timeout-s 30 \
  --policies \
    learned_expansion \
    learned_base_fallback \
    rule_far_learned_second_stage \
    rule_far_learned_second_stage_final_base_guardrail_8 \
  > "$ROOT/outputs/log_phase3_final_guardrail_eval_500_for_bridge_200.txt" 2>&1

python select_phase3_bridge_goals.py \
  --goals "$GOALS" \
  --trace-result "$TRACE_RESULT" \
  --out-goals "$BRIDGE_GOALS" \
  --out-manifest "$MANIFEST" \
  --max-goals "$MAX_GOALS" \
  --second-policy "$SECOND_POLICY" \
  --seed 1 \
  > "$ROOT/outputs/log_select_phase3_bridge_${MAX_GOALS}_a40.txt" 2>&1

python mathlib_replay_tactics.py \
  --goals "$BRIDGE_GOALS" \
  --out "$REPLAY_RESULT" \
  --timeout-s 120 \
  --save-dir "$ROOT/outputs/phase3_bridge_replay_files_${MAX_GOALS}" \
  > "$ROOT/outputs/log_mathlib_replay_tactics_phase3_bridge_${MAX_GOALS}_a40.txt" 2>&1

python analyze_phase3_bridge.py \
  --trace-result "$TRACE_RESULT" \
  --replay-result "$REPLAY_RESULT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase3_bridge_${MAX_GOALS}_a40.txt" 2>&1

python analyze_phase3_bridge_failures.py \
  --bridge-goals "$BRIDGE_GOALS" \
  --replay-result "$REPLAY_RESULT" \
  --trace-result "$TRACE_RESULT" \
  --out-json "$TAXONOMY_JSON" \
  --out-md "$TAXONOMY_MD" \
  --second-policy "$SECOND_POLICY" \
  > "$ROOT/outputs/log_analyze_phase3_bridge_failures_${MAX_GOALS}_a40.txt" 2>&1

python inspect_phase3_bridge_negative_cases.py \
  --bridge-goals "$BRIDGE_GOALS" \
  --taxonomy "$TAXONOMY_JSON" \
  --trace-result "$TRACE_RESULT" \
  --out-json "$NEG_JSON" \
  --out-md "$NEG_MD" \
  --second-policy "$SECOND_POLICY" \
  > "$ROOT/outputs/log_inspect_phase3_bridge_negative_cases_${MAX_GOALS}_a40.txt" 2>&1

echo "$REPORT"
