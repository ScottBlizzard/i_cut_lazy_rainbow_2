# Mathlib 4.30 Fresh Holdout Summary

Date: 2026-06-23

## Protocol

- Source folds: `phase3_second_stage_eval_fold0_goals_500.jsonl` and `phase3_second_stage_eval_fold1_goals_500.jsonl`
- Overlap with the original 230-goal design/evaluation set: 0 goals for each fold
- Candidate source: `retrieved_only`
- Action subset: frozen before running the holdouts
- Empty baseline: `hammer_empty`
- Frozen typed portfolio:
  1. `aesop_core_plus_learned16`
  2. `hammerCore_core_plus_learned`
  3. `aesop_core_plus_learned_swapped`
  4. `aesop_core`
- Singleton controls:
  - `aesop_core_plus_learned16`
  - `hammerCore_core_plus_learned`
  - `aesop_core_plus_learned_swapped`
  - `aesop_core`
  - `aesop_core_plus_learned32`
  - `aesop_learned16`
  - `aesop_learned32`
  - `aesop_core_plus_learned`
  - `aesop_learned8`

## Replayability

| Fold | Input goals | Clean goals | Original-tactic replayable goals |
|---|---:|---:|---:|
| fold0 | 500 | 483 | 208 |
| fold1 | 500 | 483 | 224 |
| combined | 1000 | 966 | 432 |

## Frozen Holdout Results

| Fold | Goals | Empty Hammer | Best singleton | Frozen K=1 | Frozen K=2 | Frozen K=3 | Frozen K=4 | Tested-action oracle | Strict K=4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fold0 | 208 | 16 | 23 | 24 | 24 | 28 | 28 | 28 | 12/12 |
| fold1 | 224 | 14 | 31 | 32 | 34 | 39 | 39 | 40 | 25/26 |
| combined | 432 | 30 | 54 | 56 | 58 | 67 | 67 | 68 | 37/38 |

## Readout

- The prospective fresh-holdout gate passes on two disjoint folds.
- The frozen K=3/K=4 typed portfolio beats the best predeclared singleton control on both folds.
- The final K=4 portfolio has paired deltas of +5/-0 versus the fold0 best singleton and +9/-1 versus the fold1 best singleton.
- The portfolio covers nearly all strict after-`hammer_empty` opportunities in the tested action subset: 12/12 on fold0 and 25/26 on fold1.
- Further fresh folds are not necessary before paper revision unless the paper claims a precise population estimate. The current use should be framed as prospective validation of the frozen typed-compiler effect, not as a new benchmark-scale leaderboard.

## Canonical Files

- `analysis/mathlib430_fresh_holdout_fold0_summary.md`
- `analysis/mathlib430_fresh_holdout_fold1_summary.md`
- `outputs/mathlib430_fresh_holdout_fold0_frozen_actions_merged.md`
- `outputs/mathlib430_fresh_holdout_fold1_frozen_actions_merged.md`
- `outputs/fresh_holdout_fold0_jsons.tgz`
- `outputs/fresh_holdout_fold1_jsons.tgz`
- `scripts/run_fresh_holdout_fold0_a40.sh`
- `src/evaluate_mathlib430_fresh_holdout.py`
