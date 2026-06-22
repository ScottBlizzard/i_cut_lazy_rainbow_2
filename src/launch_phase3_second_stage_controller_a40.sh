#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
TRAIN_GOALS="${1:-$ROOT/outputs/phase3_learned_train_goals_1500.jsonl}"
EVAL_GOALS="${2:-$ROOT/outputs/phase3_learned_eval_goals_500.jsonl}"
SECOND_STAGE_EVAL="${3:-$ROOT/outputs/phase3_second_stage_eval_goals_500.jsonl}"
MODEL="${4:-$ROOT/outputs/phase3_second_stage_controller_model_1500_500.json}"
OUT="${5:-$ROOT/outputs/phase3_second_stage_controller_eval_500_a40.json}"
REPORT="${6:-$ROOT/outputs/phase3_second_stage_controller_eval_500_a40.md}"

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

python train_phase3_second_stage_controller.py \
  --train-goals "$TRAIN_GOALS" \
  --eval-goals "$EVAL_GOALS" \
  --eval-out "$SECOND_STAGE_EVAL" \
  --model-out "$MODEL" \
  > "$ROOT/outputs/log_train_phase3_second_stage_controller_1500_500_a40.txt" 2>&1

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
    rule_far_full \
  > "$ROOT/outputs/log_phase3_second_stage_controller_eval_500_a40.txt" 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase3_second_stage_controller_eval_500_a40.txt" 2>&1
