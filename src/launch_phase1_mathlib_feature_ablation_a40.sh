#!/usr/bin/env bash
set -euo pipefail

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda

cd /workspace/thymic_project/paper/iclr_2/src
mkdir -p ../outputs

BASE_GOALS=${1:-../outputs/phase1_mathlib_v2_goals_500.jsonl}
GOALS=${2:-../outputs/phase1_mathlib_v2_goals_500_features.jsonl}
OUT=${3:-../outputs/phase1_mathlib_trace_core_500_feature_ablation_a40.json}
REPORT=${4:-../outputs/phase1_mathlib_trace_core_500_feature_ablation_a40.md}

python augment_phase1_features.py \
  --goals "$BASE_GOALS" \
  --out "$GOALS" \
  > ../outputs/log_augment_phase1_mathlib_features_500_a40.txt 2>&1

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
    random_retry \
    history_only \
    rule_far_failure_type_only \
    rule_far_no_core_tags \
    rule_far_full \
  > ../outputs/log_phase1_mathlib_trace_core_500_feature_ablation_a40.txt 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > ../outputs/log_analyze_phase1_mathlib_trace_core_500_feature_ablation_a40.txt 2>&1
