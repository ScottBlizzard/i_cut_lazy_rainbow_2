#!/usr/bin/env bash
set -euo pipefail

export PATH="/root/miniconda3/bin:/root/.elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"
export ELAN_TOOLCHAIN="leanprover/lean4:v4.30.0"

cd /workspace/thymic_project/paper/iclr_2

ACTIONS=(
  aesop_empty
  aesop_core
  aesop_core_facts
  aesop_core_simps
  aesop_core_plus_learned
  aesop_core_plus_learned_facts
  aesop_core_plus_learned_simps
  aesop_learned8
  aesop_learned8_facts
  aesop_learned8_simps
  aesop_core_plus_learned_identity
  aesop_core_plus_learned_swapped
  aesop_core_plus_learned_countmatched_facts
  aesop_core_plus_learned_countmatched_simps
  aesop_core_plus_learned_random_split
  aesop_learned8_identity
  aesop_learned8_swapped
  aesop_learned8_countmatched_facts
  aesop_learned8_countmatched_simps
  aesop_learned8_random_split
)

mkdir -p outputs/evidence_contract_exact_logs tmp/evidence_contract_exact

SHARD_SIZE="${SHARD_SIZE:-10}"
JOBS="${JOBS:-1}"
PARALLEL_SHARDS="${PARALLEL_SHARDS:-36}"
running=0

for MODE in oracle_plus_retrieved retrieved_only oracle_core_only; do
  for OFFSET in $(seq 0 "${SHARD_SIZE}" 229); do
    REMAINING=$((230 - OFFSET))
    if [[ "${REMAINING}" -lt "${SHARD_SIZE}" ]]; then
      COUNT="${REMAINING}"
    else
      COUNT="${SHARD_SIZE}"
    fi
    SHARD=$(printf "shard%03d" "${OFFSET}")
    (
      python3 src/run_mathlib430_pretheorem_action_matrix.py \
        --input-jsonl outputs/mathlib430_clean_trace_subset_500.jsonl \
        --replay-json outputs/mathlib430_pretheorem_original_tactic_probe_490.json \
        --mathlib-root repos/mathlib4_lean430 \
        --hammer-root repos/LeanHammer \
        --save-dir "tmp/evidence_contract_exact/${MODE}_${SHARD}_lean" \
        --check-dir "tmp/evidence_contract_exact/${MODE}_${SHARD}_check" \
        --out-json "outputs/mathlib430_aesop_exact_controls_${MODE}_${SHARD}.json" \
        --out-md "outputs/mathlib430_aesop_exact_controls_${MODE}_${SHARD}.md" \
        --max-goals "${COUNT}" \
        --goal-offset "${OFFSET}" \
        --max-candidates 32 \
        --candidate-source "${MODE}" \
        --result-action-suffix "_${MODE}_exact" \
        --jobs "${JOBS}" \
        --timeout-s 120 \
        --action-names "${ACTIONS[@]}"
    ) > "outputs/evidence_contract_exact_logs/${MODE}_${SHARD}.log" 2>&1 &
    running=$((running + 1))
    if [[ "${running}" -ge "${PARALLEL_SHARDS}" ]]; then
      wait -n
      running=$((running - 1))
    fi
  done
done

wait
