#!/usr/bin/env bash
set -euo pipefail

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda

cd /workspace/thymic_project/paper/iclr_2/src
mkdir -p ../outputs

GOALS=${1:-../outputs/phase1_mathlib_v2_goals_500.jsonl}
OUT=${2:-../outputs/phase1_mathlib_trace_core_500_ablation_a40.json}
REPORT=${3:-../outputs/phase1_mathlib_trace_core_500_ablation_a40.md}

python eval_phase1_real.py \
  --goals "$GOALS" \
  --prover-command "python trace_core_attempt.py" \
  --out "$OUT" \
  --timeout-s 30 \
  --policies \
    one_shot \
    topk_expansion \
    topk_equal_budget \
    random_retry \
    history_only \
    rule_far_full \
    rule_far_no_core_tags \
    rule_far_failure_type_only \
  > ../outputs/log_phase1_mathlib_trace_core_500_ablation_a40.txt 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > ../outputs/log_analyze_phase1_mathlib_trace_core_500_ablation_a40.txt 2>&1
