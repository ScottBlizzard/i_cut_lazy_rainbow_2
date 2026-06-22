#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 MODE OFFSET" >&2
  exit 2
fi

MODE="$1"
OFFSET="$2"
if [[ "${OFFSET}" == "0" ]]; then
  PART=part0
elif [[ "${OFFSET}" == "115" ]]; then
  PART=part1
else
  echo "OFFSET must be 0 or 115" >&2
  exit 2
fi

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

python3 src/run_mathlib430_pretheorem_action_matrix.py \
  --input-jsonl outputs/mathlib430_clean_trace_subset_500.jsonl \
  --replay-json outputs/mathlib430_pretheorem_original_tactic_probe_490.json \
  --mathlib-root repos/mathlib4_lean430 \
  --hammer-root repos/LeanHammer \
  --save-dir "tmp/evidence_contract_exact/${MODE}_${PART}_lean" \
  --check-dir "tmp/evidence_contract_exact/${MODE}_${PART}_check" \
  --out-json "outputs/mathlib430_aesop_exact_controls_${MODE}_${PART}.json" \
  --out-md "outputs/mathlib430_aesop_exact_controls_${MODE}_${PART}.md" \
  --max-goals 115 \
  --goal-offset "${OFFSET}" \
  --max-candidates 32 \
  --candidate-source "${MODE}" \
  --result-action-suffix "_${MODE}_exact" \
  --jobs 2 \
  --timeout-s 120 \
  --action-names "${ACTIONS[@]}"
