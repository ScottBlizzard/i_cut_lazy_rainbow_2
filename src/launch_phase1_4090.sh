#!/usr/bin/env bash
set -euo pipefail

source ~/miniconda3/etc/profile.d/conda.sh
conda activate iclr2

cd /home/ccj/workspace_1/iclr_2/src
mkdir -p ../outputs

python check_env.py > ../outputs/log_phase1_env.txt 2>&1
python eval_phase1.py --n-goals 5000 --seed 0 --out ../outputs/phase1_synthetic_smoke_5k.json > ../outputs/log_phase1_mock.txt 2>&1
python analyze_phase1.py --input ../outputs/phase1_synthetic_smoke_5k.json --out ../outputs/phase1_synthetic_smoke_5k.md > ../outputs/log_phase1_analyze.txt 2>&1

