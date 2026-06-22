#!/usr/bin/env bash
set -euo pipefail

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2_py311
source /root/.elan/env
unset GITHUB_ACCESS_TOKEN

PROBE_DIR="/workspace/thymic_project/paper/iclr_2/lean_dojo_probe"
cd "$PROBE_DIR"

if ! grep -q "theorem probe_use" Probe/Basic.lean; then
  cat >> Probe/Basic.lean <<'EOF'

theorem probe_use (n : Nat) : n = n := by
  exact probe_rfl n
EOF
  git add Probe/Basic.lean
  git commit -q -m theorem_probe_use
fi

cd /workspace/thymic_project/paper/iclr_2/src

python trace_mathlib_v2.py \
  --repo-url "$PROBE_DIR" \
  --commit HEAD \
  --summary ../outputs/lean_dojo_v2_probe_summary.json \
  > ../outputs/log_lean_dojo_v2_probe_trace.txt 2>&1

TRACE_ROOT="$(python -c 'import json; from pathlib import Path; print(json.loads(Path("../outputs/lean_dojo_v2_probe_summary.json").read_text())["traced_root"])')"

python make_phase1_mathlib_goals_v2.py \
  --trace-root "$TRACE_ROOT" \
  --out ../outputs/lean_dojo_v2_probe_goals.jsonl \
  --n-goals 5 \
  --max-candidates 32 \
  --min-candidates 1
