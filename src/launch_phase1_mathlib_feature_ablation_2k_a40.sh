#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
SUMMARY="$ROOT/outputs/mathlib4_local_trace_v2_current_summary.json"
GOALS="${1:-$ROOT/outputs/phase1_mathlib_v2_goals_2000_features.jsonl}"
OUT="${2:-$ROOT/outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.json}"
REPORT="${3:-$ROOT/outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.md}"

mkdir -p "$ROOT/outputs"

if [ ! -s "$SUMMARY" ]; then
  echo "missing trace summary: $SUMMARY" >&2
  exit 1
fi

source /root/miniconda3/etc/profile.d/conda.sh

TRACE_ROOT="$(
  conda run -p /workspace/thymic_project/paper/iclr2_py311 python -c \
    'import json, sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["traced_root"])' \
    "$SUMMARY" | tail -n 1
)"

cd "$ROOT/src"

if [ ! -s "$GOALS" ]; then
  conda run -p /workspace/thymic_project/paper/iclr2_py311 python make_phase1_mathlib_goals_v2.py \
    --trace-root "$TRACE_ROOT" \
    --out "$GOALS" \
    --n-goals 2000 \
    --seed 0 \
    --max-candidates 256 \
    --min-candidates 8 \
    > "$ROOT/outputs/log_make_phase1_mathlib_v2_goals_2000_features_a40.txt" 2>&1
fi

conda activate /workspace/thymic_project/paper/iclr2/.conda

python eval_phase1_real.py \
  --goals "$GOALS" \
  --prover-command "python trace_core_attempt.py" \
  --out "$OUT" \
  --timeout-s 30 \
  --policies \
    one_shot \
    topk_equal_budget \
    visible_feature_rerank \
    topk_expansion \
    rule_far_failure_type_only \
    rule_far_no_core_tags \
    rule_far_full \
  > "$ROOT/outputs/log_phase1_mathlib_trace_core_2000_feature_ablation_a40.txt" 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase1_mathlib_trace_core_2000_feature_ablation_a40.txt" 2>&1
