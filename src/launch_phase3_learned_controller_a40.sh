#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
GOALS="${1:-$ROOT/outputs/phase3_learned_eval_goals_500.jsonl}"
OUT="${2:-$ROOT/outputs/phase3_learned_controller_ablation_500_a40.json}"
REPORT="${3:-$ROOT/outputs/phase3_learned_controller_ablation_500_a40.md}"

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

python eval_phase1_trace_core.py \
  --goals "$GOALS" \
  --out "$OUT" \
  --timeout-s 30 \
  --policies \
    learned_rerank \
    learned_expansion \
    learned_base_fallback \
    rule_far_learned \
    rule_far_learned_failure_specific \
    rule_far_full \
  > "$ROOT/outputs/log_phase3_learned_controller_ablation_500_a40.txt" 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase3_learned_controller_ablation_500_a40.txt" 2>&1
