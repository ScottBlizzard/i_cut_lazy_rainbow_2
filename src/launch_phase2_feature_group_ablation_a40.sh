#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
GOALS="${1:-$ROOT/outputs/phase1_mathlib_v2_goals_2000_features.jsonl}"
OUT="${2:-$ROOT/outputs/phase2_feature_group_ablation_2000_a40.json}"
REPORT="${3:-$ROOT/outputs/phase2_feature_group_ablation_2000_a40.md}"

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

python eval_phase1_trace_core.py \
  --goals "$GOALS" \
  --out "$OUT" \
  --timeout-s 30 \
  --policies \
    one_shot \
    topk_equal_budget \
    visible_feature_name_rerank \
    visible_feature_statement_rerank \
    visible_feature_decl_rerank \
    visible_feature_name_statement_rerank \
    visible_feature_rerank \
    topk_expansion \
    rule_far_failure_type_only \
    rule_far_no_core_name_features \
    rule_far_no_core_statement_features \
    rule_far_no_core_decl_features \
    rule_far_no_core_name_statement_features \
    rule_far_no_core_tags \
    rule_far_full \
  > "$ROOT/outputs/log_phase2_feature_group_ablation_2000_a40.txt" 2>&1

python analyze_phase1.py \
  --input "$OUT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase2_feature_group_ablation_2000_a40.txt" 2>&1
