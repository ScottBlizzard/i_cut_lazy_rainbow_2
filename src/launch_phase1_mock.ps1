$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python check_env.py
python eval_phase1.py --n-goals 500 --seed 0 --out ..\outputs\phase1_synthetic_smoke.json
python analyze_phase1.py --input ..\outputs\phase1_synthetic_smoke.json --out ..\outputs\phase1_synthetic_smoke.md

