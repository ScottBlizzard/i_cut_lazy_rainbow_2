# Mathlib 4.30 Fresh Holdout: fold1

- Matrix: `outputs/mathlib430_fresh_holdout_fold1_frozen_actions_merged.json`
- Candidate source: `retrieved_only`
- Goals: 224
- Tested actions: 10
- Empty Hammer: 14/224 (6.2%)
- Best singleton control: `aesop_learned32` = 31/224 (13.8%)
- Tested-action oracle: 40/224 (17.9%)
- Strict after-`hammer_empty` goals: 26

## Frozen Portfolio

| K | Success | Strict success | Actions |
|---:|---:|---:|---|
| 1 | 32/224 (14.3%) | 18/26 (69.2%) | `aesop_core_plus_learned16` |
| 2 | 34/224 (15.2%) | 20/26 (76.9%) | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned` |
| 3 | 39/224 (17.4%) | 25/26 (96.2%) | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped` |
| 4 | 39/224 (17.4%) | 25/26 (96.2%) | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core` |

## Singleton Controls

| Action | Success |
|---|---:|
| `aesop_core_plus_learned32` | 31/224 (13.8%) |
| `aesop_learned32` | 31/224 (13.8%) |
| `aesop_core_plus_learned` | 30/224 (13.4%) |
| `aesop_core_plus_learned16` | 30/224 (13.4%) |
| `aesop_learned16` | 30/224 (13.4%) |
| `aesop_learned8` | 30/224 (13.4%) |
| `aesop_core_plus_learned_swapped` | 22/224 (9.8%) |
| `aesop_core` | 14/224 (6.2%) |
| `hammer_empty` | 14/224 (6.2%) |
| `hammerCore_core_plus_learned` | 4/224 (1.8%) |

## Paired Final Portfolio Deltas

- Final K=4 vs `aesop_learned32`: +9 wins, -1 losses.
- Final K=4 vs `hammer_empty`: +25 wins, -0 losses.
