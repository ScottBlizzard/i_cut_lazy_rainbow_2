#!/usr/bin/env bash
set -euo pipefail

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2_py311
source /root/.elan/env
unset GITHUB_ACCESS_TOKEN

cd /workspace/thymic_project/paper/iclr_2/src

COMMIT="${1:-014c1563dc2c952488b6acfd3fac97ee588f0c6d}"

python trace_mathlib_v2.py \
  --commit "$COMMIT" \
  --summary "../outputs/mathlib4_trace_v2_current_summary.json" \
  > "../outputs/log_mathlib4_trace_v2_current.txt" 2>&1
