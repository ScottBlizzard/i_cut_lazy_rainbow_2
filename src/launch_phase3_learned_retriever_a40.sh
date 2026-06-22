#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
SOURCE_GOALS="${1:-$ROOT/outputs/phase3_mathlib_global_imported_core_goals_2000.jsonl}"
TRAIN_GOALS="${2:-$ROOT/outputs/phase3_learned_train_goals_1500.jsonl}"
EVAL_GOALS="${3:-$ROOT/outputs/phase3_learned_eval_goals_500.jsonl}"
MODEL="${4:-$ROOT/outputs/phase3_learned_retriever_model_1500_500.json}"
OUT="${5:-$ROOT/outputs/phase3_learned_retriever_eval_500_a40.json}"
REPORT="${6:-$ROOT/outputs/phase3_learned_retriever_eval_500_a40.md}"

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

python train_phase3_learned_retriever.py \
  --input "$SOURCE_GOALS" \
  --train-out "$TRAIN_GOALS" \
  --eval-out "$EVAL_GOALS" \
  --model-out "$MODEL" \
  --split-index 1500 \
  > "$ROOT/outputs/log_train_phase3_learned_retriever_1500_500_a40.txt" 2>&1

python eval_phase1_trace_core.py \
  --goals "$EVAL_GOALS" \
  --out "$OUT" \
  --timeout-s 30 \
  --policies \
    one_shot \
    topk_equal_budget \
    visible_feature_rerank \
    same_file_prior_rerank \
    bm25_rerank \
    bm25_expansion \
    bm25_same_file_prior_expansion \
    leansearch_iterative \
    learned_rerank \
    learned_expansion \
    rule_far_bm25 \
    rule_far_learned \
    rule_far_no_core_tags \
    rule_far_full \
  > "$ROOT/outputs/log_phase3_learned_retriever_eval_500_a40.txt" 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase3_learned_retriever_eval_500_a40.txt" 2>&1
