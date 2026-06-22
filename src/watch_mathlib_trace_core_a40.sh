#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspace/thymic_project/paper/iclr_2"
TRACE_PID="${1:?usage: watch_mathlib_trace_core_a40.sh TRACE_PID}"
SUMMARY="$ROOT/outputs/mathlib4_local_trace_v2_current_summary.json"
GOALS="$ROOT/outputs/phase1_mathlib_v2_goals_500.jsonl"
RESULT="$ROOT/outputs/phase1_mathlib_trace_core_500_a40.json"
REPORT="$ROOT/outputs/phase1_mathlib_trace_core_500_a40.md"
WATCH_LOG="$ROOT/outputs/log_mathlib_trace_core_watcher.txt"

mkdir -p "$ROOT/outputs"

{
  echo "[watcher] started at $(date -u), waiting for trace pid $TRACE_PID"
  while kill -0 "$TRACE_PID" 2>/dev/null; do
    echo "[watcher] $(date -u) trace still running"
    sleep 300
  done

  echo "[watcher] trace pid finished at $(date -u)"
  if [ ! -s "$SUMMARY" ]; then
    echo "[watcher] summary missing or empty: $SUMMARY"
    exit 1
  fi

  source /root/miniconda3/etc/profile.d/conda.sh
  conda activate /workspace/thymic_project/paper/iclr2_py311
  cd "$ROOT/src"

  TRACE_ROOT="$(
    python - "$SUMMARY" <<'PY'
import json
import sys
from pathlib import Path

summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(summary["traced_root"])
PY
  )"
  echo "[watcher] traced root: $TRACE_ROOT"
  python make_phase1_mathlib_goals_v2.py \
    --trace-root "$TRACE_ROOT" \
    --out "$GOALS" \
    --n-goals 500

  if [ ! -s "$GOALS" ]; then
    echo "[watcher] goals missing or empty: $GOALS"
    exit 1
  fi
  echo "[watcher] generated $(wc -l < "$GOALS") goals"

  bash "$ROOT/src/launch_phase1_mathlib_trace_core_a40.sh" \
    "$GOALS" \
    "$RESULT" \
    "$REPORT"

  echo "[watcher] completed at $(date -u)"
} > "$WATCH_LOG" 2>&1
