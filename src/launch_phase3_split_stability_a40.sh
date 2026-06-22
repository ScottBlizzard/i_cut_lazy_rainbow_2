#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
FOLD_INDEX="${1:-0}"
SOURCE_GOALS="${2:-$ROOT/outputs/phase3_mathlib_global_imported_core_goals_2000.jsonl}"
FOLD_SIZE="${3:-500}"
TAG="fold${FOLD_INDEX}"

REORDERED="$ROOT/outputs/phase3_split_stability_${TAG}_source_2000.jsonl"
TRAIN_GOALS="$ROOT/outputs/phase3_learned_train_${TAG}_goals_1500.jsonl"
EVAL_GOALS="$ROOT/outputs/phase3_learned_eval_${TAG}_goals_500.jsonl"
RETRIEVER_MODEL="$ROOT/outputs/phase3_learned_retriever_model_${TAG}_1500_500.json"
SECOND_STAGE_EVAL="$ROOT/outputs/phase3_second_stage_eval_${TAG}_goals_500.jsonl"
SECOND_STAGE_MODEL="$ROOT/outputs/phase3_second_stage_controller_model_${TAG}_1500_500.json"
OUT="$ROOT/outputs/phase3_second_stage_controller_eval_${TAG}_500_a40.json"
REPORT="$ROOT/outputs/phase3_second_stage_controller_eval_${TAG}_500_a40.md"

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

python make_phase3_fold_split.py \
  --input "$SOURCE_GOALS" \
  --out "$REORDERED" \
  --fold-index "$FOLD_INDEX" \
  --fold-size "$FOLD_SIZE" \
  > "$ROOT/outputs/log_phase3_split_stability_${TAG}_make.txt" 2>&1

python train_phase3_learned_retriever.py \
  --input "$REORDERED" \
  --train-out "$TRAIN_GOALS" \
  --eval-out "$EVAL_GOALS" \
  --model-out "$RETRIEVER_MODEL" \
  --split-index 1500 \
  > "$ROOT/outputs/log_phase3_split_stability_${TAG}_train_retriever.txt" 2>&1

python train_phase3_second_stage_controller.py \
  --train-goals "$TRAIN_GOALS" \
  --eval-goals "$EVAL_GOALS" \
  --eval-out "$SECOND_STAGE_EVAL" \
  --model-out "$SECOND_STAGE_MODEL" \
  > "$ROOT/outputs/log_phase3_split_stability_${TAG}_train_second_stage.txt" 2>&1

python eval_phase1_trace_core.py \
  --goals "$SECOND_STAGE_EVAL" \
  --out "$OUT" \
  --timeout-s 30 \
  --policies \
    learned_rerank \
    learned_expansion \
    learned_base_fallback \
    rule_far_learned \
    rule_far_learned_failure_specific \
    rule_far_learned_second_stage \
    rule_far_learned_second_stage_final_base_guardrail_8 \
    rule_far_full \
  > "$ROOT/outputs/log_phase3_split_stability_${TAG}_eval.txt" 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_phase3_split_stability_${TAG}_analyze.txt" 2>&1

echo "$REPORT"
