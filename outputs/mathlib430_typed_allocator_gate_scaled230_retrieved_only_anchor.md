# Mathlib 4.30 Typed Allocator Gate

Date: 2026-06-23

## Setup

- Matrix: `outputs/mathlib430_pretheorem_action_matrix_scaled230_retrieved_only_anchor_merged.json`
- Splits: `outputs/mathlib430_replayable490_splits.json`
- Goals: 230
- Strict action-dependent goals: 23
- All policies run `hammer_empty` first, then spend a retry budget over typed proof actions.
- Learned policies are trained out of fold using goal text, first-failure status/output, and typed fact/simp pool features.

## 5-Fold Out-of-Fold Success

| K | Fixed greedy | Pure logreg | Logreg no weight | Pure CNB | Fixed+residual logreg | Fixed+residual CNB | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 47/230 (20.4%) | 39/230 (17.0%) | 42/230 (18.3%) | 35/230 (15.2%) | 39/230 (17.0%) | 35/230 (15.2%) | 52/230 (22.6%) |
| 2 | 50/230 (21.7%) | 39/230 (17.0%) | 42/230 (18.3%) | 37/230 (16.1%) | 51/230 (22.2%) | 50/230 (21.7%) | 52/230 (22.6%) |
| 3 | 52/230 (22.6%) | 41/230 (17.8%) | 44/230 (19.1%) | 38/230 (16.5%) | 52/230 (22.6%) | 52/230 (22.6%) | 52/230 (22.6%) |
| 4 | 52/230 (22.6%) | 42/230 (18.3%) | 46/230 (20.0%) | 39/230 (17.0%) | 52/230 (22.6%) | 52/230 (22.6%) | 52/230 (22.6%) |

## 5-Fold Strict-Goal Success

| K | Fixed greedy | Pure logreg | Logreg no weight | Pure CNB | Fixed+residual logreg | Fixed+residual CNB | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 18/23 (78.3%) | 10/23 (43.5%) | 13/23 (56.5%) | 6/23 (26.1%) | 10/23 (43.5%) | 6/23 (26.1%) | 23/23 (100.0%) |
| 2 | 21/23 (91.3%) | 10/23 (43.5%) | 13/23 (56.5%) | 8/23 (34.8%) | 22/23 (95.7%) | 21/23 (91.3%) | 23/23 (100.0%) |
| 3 | 23/23 (100.0%) | 12/23 (52.2%) | 15/23 (65.2%) | 9/23 (39.1%) | 23/23 (100.0%) | 23/23 (100.0%) | 23/23 (100.0%) |
| 4 | 23/23 (100.0%) | 13/23 (56.5%) | 17/23 (73.9%) | 10/23 (43.5%) | 23/23 (100.0%) | 23/23 (100.0%) | 23/23 (100.0%) |

## Average Lean Calls

| K | Fixed greedy | Pure logreg | Pure logreg no weight | Pure ComplementNB | Fixed prefix + residual logreg | Fixed prefix + residual CNB |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.87 | 1.87 | 1.87 | 1.87 | 1.87 | 1.87 |
| 2 | 2.67 | 2.70 | 2.69 | 2.72 | 2.67 | 2.67 |
| 3 | 3.45 | 3.53 | 3.51 | 3.56 | 3.45 | 3.45 |
| 4 | 4.23 | 4.36 | 4.32 | 4.40 | 4.23 | 4.23 |

## Train-Fitted Fixed Portfolios

| K | Actions |
|---:|---|
| 1 | `aesop_core_plus_learned16` |
| 2 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned` |
| 3 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped` |
| 4 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core` |

## Readout

- Fixed K=4 reaches 52/230 OOF. The best learned allocator setting reaches 52/230 with `hybrid_logreg` at K=4.
- Gate result: learned typed allocation does not beat or compress fixed K=4; adaptive routing should remain outside the main claim.
