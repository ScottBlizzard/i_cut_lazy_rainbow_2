#!/usr/bin/env bash
set -euo pipefail

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2/.conda
source /root/.elan/env

cd /workspace/thymic_project/paper/iclr_2/src
mkdir -p ../outputs

python check_env.py > ../outputs/log_phase1_env_a40_with_lean.txt 2>&1
python make_phase1_lean_synthetic_goals.py --n-goals 10 --seed 0 --out ../outputs/phase1_lean_synth_10.jsonl > ../outputs/log_make_phase1_lean_synth_10.txt 2>&1
python eval_phase1_real.py --goals ../outputs/phase1_lean_synth_10.jsonl --prover-command "python lean_attempt.py" --out ../outputs/phase1_lean_synth_10_a40.json --timeout-s 30 --policies one_shot topk_expansion rule_far > ../outputs/log_phase1_lean_synth_10_a40.txt 2>&1
python analyze_phase1.py --input ../outputs/phase1_lean_synth_10_a40.json --out ../outputs/phase1_lean_synth_10_a40.md > ../outputs/log_analyze_phase1_lean_synth_10_a40.txt 2>&1
