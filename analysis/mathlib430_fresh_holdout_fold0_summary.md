# Mathlib 4.30 Fresh Holdout: fold0

- Matrix: `outputs/mathlib430_fresh_holdout_fold0_frozen_actions_merged.json`
- Candidate source: `retrieved_only`
- Goals: 208
- Tested actions: 10
- Empty Hammer: 16/208 (7.7%)
- Best singleton control: `aesop_core_plus_learned_swapped` = 23/208 (11.1%)
- Tested-action oracle: 28/208 (13.5%)
- Strict after-`hammer_empty` goals: 12

## Frozen Portfolio

| K | Success | Strict success | Actions |
|---:|---:|---:|---|
| 1 | 24/208 (11.5%) | 8/12 (66.7%) | `aesop_core_plus_learned16` |
| 2 | 24/208 (11.5%) | 8/12 (66.7%) | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned` |
| 3 | 28/208 (13.5%) | 12/12 (100.0%) | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped` |
| 4 | 28/208 (13.5%) | 12/12 (100.0%) | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core` |

## Singleton Controls

| Action | Success |
|---|---:|
| `aesop_core_plus_learned_swapped` | 23/208 (11.1%) |
| `aesop_core_plus_learned` | 20/208 (9.6%) |
| `aesop_core_plus_learned16` | 20/208 (9.6%) |
| `aesop_core_plus_learned32` | 20/208 (9.6%) |
| `aesop_learned16` | 20/208 (9.6%) |
| `aesop_learned32` | 20/208 (9.6%) |
| `aesop_learned8` | 20/208 (9.6%) |
| `aesop_core` | 16/208 (7.7%) |
| `hammer_empty` | 16/208 (7.7%) |
| `hammerCore_core_plus_learned` | 4/208 (1.9%) |

## Paired Final Portfolio Deltas

- Final K=4 vs `aesop_core_plus_learned_swapped`: +5 wins, -0 losses.
- Final K=4 vs `hammer_empty`: +12 wins, -0 losses.
