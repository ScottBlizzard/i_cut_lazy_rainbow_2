# Mathlib 4.30 Typed Allocator Gate

Date: 2026-06-23

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- Splits: `outputs\mathlib430_replayable490_splits.json`
- Goals: 230
- Strict action-dependent goals: 29
- All policies run `hammer_empty` first, then spend a retry budget over typed proof actions.
- Learned policies are trained out of fold using goal text, first-failure status/output, and typed fact/simp pool features.

## 5-Fold Out-of-Fold Success

| K | Fixed greedy | Pure logreg | Logreg no weight | Pure CNB | Fixed+residual logreg | Fixed+residual CNB | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 49/230 (21.3%) | 41/230 (17.8%) | 46/230 (20.0%) | 38/230 (16.5%) | 41/230 (17.8%) | 38/230 (16.5%) | 58/230 (25.2%) |
| 2 | 55/230 (23.9%) | 41/230 (17.8%) | 46/230 (20.0%) | 38/230 (16.5%) | 55/230 (23.9%) | 52/230 (22.6%) | 58/230 (25.2%) |
| 3 | 55/230 (23.9%) | 44/230 (19.1%) | 48/230 (20.9%) | 38/230 (16.5%) | 56/230 (24.3%) | 55/230 (23.9%) | 58/230 (25.2%) |
| 4 | 57/230 (24.8%) | 47/230 (20.4%) | 49/230 (21.3%) | 39/230 (17.0%) | 57/230 (24.8%) | 57/230 (24.8%) | 58/230 (25.2%) |

## 5-Fold Strict-Goal Success

| K | Fixed greedy | Pure logreg | Logreg no weight | Pure CNB | Fixed+residual logreg | Fixed+residual CNB | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 20/29 (69.0%) | 12/29 (41.4%) | 17/29 (58.6%) | 9/29 (31.0%) | 12/29 (41.4%) | 9/29 (31.0%) | 29/29 (100.0%) |
| 2 | 26/29 (89.7%) | 12/29 (41.4%) | 17/29 (58.6%) | 9/29 (31.0%) | 26/29 (89.7%) | 23/29 (79.3%) | 29/29 (100.0%) |
| 3 | 26/29 (89.7%) | 15/29 (51.7%) | 19/29 (65.5%) | 9/29 (31.0%) | 27/29 (93.1%) | 26/29 (89.7%) | 29/29 (100.0%) |
| 4 | 28/29 (96.6%) | 18/29 (62.1%) | 20/29 (69.0%) | 10/29 (34.5%) | 28/29 (96.6%) | 28/29 (96.6%) | 29/29 (100.0%) |

## Average Lean Calls

| K | Fixed greedy | Pure logreg | Pure logreg no weight | Pure ComplementNB | Fixed prefix + residual logreg | Fixed prefix + residual CNB |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.87 | 1.87 | 1.87 | 1.87 | 1.87 | 1.87 |
| 2 | 2.66 | 2.70 | 2.67 | 2.71 | 2.66 | 2.66 |
| 3 | 3.42 | 3.52 | 3.47 | 3.54 | 3.42 | 3.42 |
| 4 | 4.18 | 4.33 | 4.27 | 4.38 | 4.18 | 4.18 |

## Train-Fitted Fixed Portfolios

| K | Actions |
|---:|---|
| 1 | `aesop_core_plus_learned` |
| 2 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` |
| 3 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16` |
| 4 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core` |

## Readout

- Fixed K=4 reaches 57/230 OOF. The best learned allocator setting reaches 57/230 with `hybrid_logreg` at K=4.
- Gate result: learned typed allocation does not beat or compress fixed K=4; adaptive routing should remain outside the main claim.
