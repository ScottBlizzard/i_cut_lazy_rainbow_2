#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
SUMMARY="$ROOT/outputs/mathlib4_local_trace_v2_current_summary.json"
GLOBAL_GOALS="${1:-$ROOT/outputs/phase3_mathlib_global_imported_core_goals_2000.jsonl}"
OUT="${2:-$ROOT/outputs/phase3_global_retrieval_2000_a40.json}"
REPORT="${3:-$ROOT/outputs/phase3_global_retrieval_2000_a40.md}"

source /root/miniconda3/etc/profile.d/conda.sh

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

if [ ! -s "$SUMMARY" ]; then
  echo "missing trace summary: $SUMMARY" >&2
  exit 1
fi

TRACE_ROOT="$(
  conda run -p /workspace/thymic_project/paper/iclr2_py311 python -c \
    'import json, sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["traced_root"])' \
    "$SUMMARY" | tail -n 1
)"

conda run -p /workspace/thymic_project/paper/iclr2_py311 python make_phase3_mathlib_global_goals.py \
  --trace-root "$TRACE_ROOT" \
  --out "$GLOBAL_GOALS" \
  --n-goals 2000 \
  --max-candidates 256 \
  --max-same-file 96 \
  --max-imported 192 \
  --min-imported-core 1 \
  --seed 11 \
  > "$ROOT/outputs/log_make_phase3_mathlib_global_imported_core_goals_2000_a40.txt" 2>&1

conda activate /workspace/thymic_project/paper/iclr2/.conda

python eval_phase1_trace_core.py \
  --goals "$GLOBAL_GOALS" \
  --out "$OUT" \
  --timeout-s 30 \
  --policies \
    one_shot \
    topk_equal_budget \
    bm25_rerank \
    bm25_same_file_prior_rerank \
    visible_feature_rerank \
    same_file_prior_rerank \
    topk_expansion \
    bm25_expansion \
    bm25_same_file_prior_expansion \
    same_file_prior_expansion \
    leansearch_iterative \
    rule_far_failure_type_only \
    rule_far_bm25 \
    rule_far_no_core_tags \
    rule_far_full \
  > "$ROOT/outputs/log_phase3_global_retrieval_2000_a40.txt" 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase3_global_retrieval_2000_a40.txt" 2>&1
