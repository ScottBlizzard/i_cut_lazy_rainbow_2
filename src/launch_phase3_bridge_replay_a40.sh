#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
GOALS="${1:-$ROOT/outputs/phase3_second_stage_eval_goals_500.jsonl}"
TRACE_RESULT="${2:-$ROOT/outputs/phase3_second_stage_controller_eval_500_a40.json}"
BRIDGE_GOALS="${3:-$ROOT/outputs/phase3_bridge_goals_100.jsonl}"
MANIFEST="${4:-$ROOT/outputs/phase3_bridge_manifest_100.json}"
REPLAY_RESULT="${5:-$ROOT/outputs/phase3_bridge_replay_100.json}"
REPORT="${6:-$ROOT/outputs/phase3_bridge_report_100.md}"

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda
source /root/.elan/env

cd "$ROOT/src"
mkdir -p "$ROOT/outputs"

python select_phase3_bridge_goals.py \
  --goals "$GOALS" \
  --trace-result "$TRACE_RESULT" \
  --out-goals "$BRIDGE_GOALS" \
  --out-manifest "$MANIFEST" \
  --max-goals 100 \
  --seed 0 \
  > "$ROOT/outputs/log_select_phase3_bridge_100_a40.txt" 2>&1

python mathlib_replay_tactics.py \
  --goals "$BRIDGE_GOALS" \
  --out "$REPLAY_RESULT" \
  --timeout-s 120 \
  --save-dir "$ROOT/outputs/phase3_bridge_replay_files_100" \
  > "$ROOT/outputs/log_mathlib_replay_tactics_phase3_bridge_100_a40.txt" 2>&1

python analyze_phase3_bridge.py \
  --trace-result "$TRACE_RESULT" \
  --replay-result "$REPLAY_RESULT" \
  --out "$REPORT" \
  > "$ROOT/outputs/log_analyze_phase3_bridge_100_a40.txt" 2>&1
