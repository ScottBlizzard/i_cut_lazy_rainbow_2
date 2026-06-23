#!/usr/bin/env bash
set -euo pipefail

export PATH="/root/miniconda3/bin:/root/.elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"
export ELAN_TOOLCHAIN="leanprover/lean4:v4.30.0"

ROOT="/workspace/thymic_project/paper/iclr_2"
cd "${ROOT}"

TAG="${TAG:-fold0}"
SOURCE_JSONL="${SOURCE_JSONL:-outputs/phase3_second_stage_eval_${TAG}_goals_500.jsonl}"
PREFLIGHT_JSON="outputs/mathlib430_trace_corpus_preflight_${TAG}_500.json"
PREFLIGHT_MD="outputs/mathlib430_trace_corpus_preflight_${TAG}_500.md"
CLEAN_JSONL="outputs/mathlib430_clean_trace_subset_${TAG}_500.jsonl"
CLEAN_MD="outputs/mathlib430_clean_trace_subset_${TAG}_500.md"
REPLAY_JSON="outputs/mathlib430_pretheorem_original_tactic_probe_${TAG}_500.json"
REPLAY_MD="outputs/mathlib430_pretheorem_original_tactic_probe_${TAG}_500.md"
MERGED_JSON="outputs/mathlib430_fresh_holdout_${TAG}_frozen_actions_merged.json"
MERGED_MD="outputs/mathlib430_fresh_holdout_${TAG}_frozen_actions_merged.md"
SUMMARY_JSON="analysis/mathlib430_fresh_holdout_${TAG}_summary.json"
SUMMARY_MD="analysis/mathlib430_fresh_holdout_${TAG}_summary.md"

mkdir -p outputs/fresh_holdout_${TAG}_logs tmp/fresh_holdout_${TAG} analysis

JOBS="${JOBS:-1}"
PARALLEL_SHARDS="${PARALLEL_SHARDS:-48}"
REPLAY_JOBS="${REPLAY_JOBS:-48}"
TIMEOUT_S="${TIMEOUT_S:-120}"

ACTION_NAMES=(
  hammer_empty
  aesop_core_plus_learned16
  hammerCore_core_plus_learned
  aesop_core_plus_learned_swapped
  aesop_core
  aesop_core_plus_learned32
  aesop_learned16
  aesop_learned32
  aesop_core_plus_learned
  aesop_learned8
)

PORTFOLIO_ACTIONS=(
  aesop_core_plus_learned16
  hammerCore_core_plus_learned
  aesop_core_plus_learned_swapped
  aesop_core
)

if [[ ! -s "${SOURCE_JSONL}" ]]; then
  echo "missing source holdout JSONL: ${SOURCE_JSONL}" >&2
  exit 1
fi

if [[ ! -s "${PREFLIGHT_JSON}" ]]; then
  python3 src/run_mathlib430_trace_corpus_preflight.py \
    --input-jsonl "${SOURCE_JSONL}" \
    --mathlib-root repos/mathlib4_lean430 \
    --work-dir "tmp/fresh_holdout_${TAG}/preflight" \
    --out-json "${PREFLIGHT_JSON}" \
    --out-md "${PREFLIGHT_MD}" \
    --limit 500 \
    --timeout-s 180 \
    > "outputs/fresh_holdout_${TAG}_logs/preflight.log" 2>&1
fi

if [[ ! -s "${CLEAN_JSONL}" ]]; then
  python3 src/build_mathlib430_clean_trace_subset.py \
    --input-jsonl "${SOURCE_JSONL}" \
    --preflight-json "${PREFLIGHT_JSON}" \
    --out-jsonl "${CLEAN_JSONL}" \
    --out-md "${CLEAN_MD}" \
    > "outputs/fresh_holdout_${TAG}_logs/clean.log" 2>&1
fi

if [[ ! -s "${REPLAY_JSON}" ]]; then
  python3 src/run_mathlib430_pretheorem_original_tactic_probe.py \
    --input-jsonl "${CLEAN_JSONL}" \
    --mathlib-root repos/mathlib4_lean430 \
    --save-dir "tmp/fresh_holdout_${TAG}/original_replay" \
    --out-json "${REPLAY_JSON}" \
    --out-md "${REPLAY_MD}" \
    --limit 0 \
    --jobs "${REPLAY_JOBS}" \
    --timeout-s "${TIMEOUT_S}" \
    > "outputs/fresh_holdout_${TAG}_logs/original_replay.log" 2>&1
fi

N_REPLAY=$(python3 - "${REPLAY_JSON}" <<'PY'
import json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
print(sum(1 for row in payload.get("results", []) if row.get("verified")))
PY
)

if [[ "${N_REPLAY}" -le 0 ]]; then
  echo "no replay-verified holdout goals; stopping before action matrix" >&2
  exit 2
fi

running=0
for OFFSET in $(seq 0 $((N_REPLAY - 1))); do
  GOAL=$(printf "g%03d" "${OFFSET}")
  OUT_JSON="outputs/mathlib430_fresh_holdout_${TAG}_${GOAL}.json"
  OUT_MD="outputs/mathlib430_fresh_holdout_${TAG}_${GOAL}.md"
  if [[ -s "${OUT_JSON}" ]]; then
    continue
  fi
  (
    python3 src/run_mathlib430_pretheorem_action_matrix.py \
      --input-jsonl "${CLEAN_JSONL}" \
      --replay-json "${REPLAY_JSON}" \
      --mathlib-root repos/mathlib4_lean430 \
      --hammer-root repos/LeanHammer \
      --save-dir "tmp/fresh_holdout_${TAG}/${GOAL}_lean" \
      --check-dir "tmp/fresh_holdout_${TAG}/${GOAL}_check" \
      --out-json "${OUT_JSON}" \
      --out-md "${OUT_MD}" \
      --max-goals 1 \
      --goal-offset "${OFFSET}" \
      --max-candidates 32 \
      --candidate-source retrieved_only \
      --action-names "${ACTION_NAMES[@]}" \
      --jobs "${JOBS}" \
      --timeout-s "${TIMEOUT_S}"
  ) > "outputs/fresh_holdout_${TAG}_logs/${GOAL}.log" 2>&1 &
  running=$((running + 1))
  if [[ "${running}" -ge "${PARALLEL_SHARDS}" ]]; then
    wait -n
    running=$((running - 1))
  fi
done
wait

python3 src/merge_mathlib430_action_matrices.py \
  --inputs outputs/mathlib430_fresh_holdout_${TAG}_g*.json \
  --out-json "${MERGED_JSON}" \
  --out-md "${MERGED_MD}" \
  > "outputs/fresh_holdout_${TAG}_logs/merge.log" 2>&1

python3 src/evaluate_mathlib430_fresh_holdout.py \
  --matrix-json "${MERGED_JSON}" \
  --out-json "${SUMMARY_JSON}" \
  --out-md "${SUMMARY_MD}" \
  --tag "${TAG}" \
  --portfolio-actions "${PORTFOLIO_ACTIONS[@]}" \
  --singleton-controls "${ACTION_NAMES[@]}" \
  > "outputs/fresh_holdout_${TAG}_logs/summary.log" 2>&1

tar -czf "outputs/fresh_holdout_${TAG}_jsons.tgz" outputs/mathlib430_fresh_holdout_${TAG}_g*.json
tar -czf "outputs/fresh_holdout_${TAG}_mds.tgz" outputs/mathlib430_fresh_holdout_${TAG}_g*.md
tar -czf "outputs/fresh_holdout_${TAG}_logs.tgz" outputs/fresh_holdout_${TAG}_logs

echo "${SUMMARY_MD}"
