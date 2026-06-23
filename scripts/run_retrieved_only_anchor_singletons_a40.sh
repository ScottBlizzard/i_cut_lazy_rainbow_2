#!/usr/bin/env bash
set -euo pipefail

export PATH="/root/miniconda3/bin:/root/.elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"
export ELAN_TOOLCHAIN="leanprover/lean4:v4.30.0"

ROOT="/workspace/thymic_project/paper/iclr_2"
cd "${ROOT}"

mkdir -p outputs/retrieved_only_anchor_logs tmp/retrieved_only_anchor

JOBS="${JOBS:-1}"
PARALLEL_SHARDS="${PARALLEL_SHARDS:-64}"
START_OFFSET="${START_OFFSET:-0}"
END_OFFSET="${END_OFFSET:-229}"

running=0

for OFFSET in $(seq "${START_OFFSET}" "${END_OFFSET}"); do
  GOAL=$(printf "g%03d" "${OFFSET}")
  (
    python3 src/run_mathlib430_pretheorem_action_matrix.py \
      --input-jsonl outputs/mathlib430_clean_trace_subset_500.jsonl \
      --replay-json outputs/mathlib430_pretheorem_original_tactic_probe_490.json \
      --mathlib-root repos/mathlib4_lean430 \
      --hammer-root repos/LeanHammer \
      --save-dir "tmp/retrieved_only_anchor/${GOAL}_lean" \
      --check-dir "tmp/retrieved_only_anchor/${GOAL}_check" \
      --out-json "outputs/mathlib430_retrieved_only_anchor_${GOAL}.json" \
      --out-md "outputs/mathlib430_retrieved_only_anchor_${GOAL}.md" \
      --max-goals 1 \
      --goal-offset "${OFFSET}" \
      --max-candidates 32 \
      --candidate-source retrieved_only \
      --jobs "${JOBS}" \
      --timeout-s 120
  ) > "outputs/retrieved_only_anchor_logs/${GOAL}.log" 2>&1 &
  running=$((running + 1))
  if [[ "${running}" -ge "${PARALLEL_SHARDS}" ]]; then
    wait -n
    running=$((running - 1))
  fi
done

wait
