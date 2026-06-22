# Mathlib 4.30 Budgeted Action-Policy Experiment

Date: 2026-06-22

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- Splits: `outputs\mathlib430_replayable490_splits.json`
- Replayable goals: 230
- Strict action-dependent oracle goals: 29
- Policies always run `hammer_empty` first, then spend K retry actions.
- Learned policies are trained only on the train split, except the OOF table which retrains per fold.

## Train-Fitted Split Results

| Split | K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1 | 30/138 (21.7%) | 37/138 (26.8%) | 26/138 (18.8%) | 37/138 (26.8%) | 26/138 (18.8%) | 37/138 (26.8%) |
| train | 2 | 35/138 (25.4%) | 37/138 (26.8%) | 27/138 (19.6%) | 37/138 (26.8%) | 34/138 (24.6%) | 37/138 (26.8%) |
| train | 3 | 36/138 (26.1%) | 37/138 (26.8%) | 29/138 (21.0%) | 37/138 (26.8%) | 36/138 (26.1%) | 37/138 (26.8%) |
| train | 4 | 37/138 (26.8%) | 37/138 (26.8%) | 29/138 (21.0%) | 37/138 (26.8%) | 37/138 (26.8%) | 37/138 (26.8%) |
| train | 5 | 37/138 (26.8%) | 37/138 (26.8%) | 29/138 (21.0%) | 37/138 (26.8%) | 37/138 (26.8%) | 37/138 (26.8%) |
| train | 6 | 37/138 (26.8%) | 37/138 (26.8%) | 32/138 (23.2%) | 37/138 (26.8%) | 37/138 (26.8%) | 37/138 (26.8%) |
| dev | 1 | 12/46 (26.1%) | 8/46 (17.4%) | 12/46 (26.1%) | 8/46 (17.4%) | 12/46 (26.1%) | 13/46 (28.3%) |
| dev | 2 | 12/46 (26.1%) | 8/46 (17.4%) | 12/46 (26.1%) | 12/46 (26.1%) | 12/46 (26.1%) | 13/46 (28.3%) |
| dev | 3 | 12/46 (26.1%) | 8/46 (17.4%) | 12/46 (26.1%) | 12/46 (26.1%) | 12/46 (26.1%) | 13/46 (28.3%) |
| dev | 4 | 13/46 (28.3%) | 8/46 (17.4%) | 12/46 (26.1%) | 12/46 (26.1%) | 13/46 (28.3%) | 13/46 (28.3%) |
| dev | 5 | 13/46 (28.3%) | 9/46 (19.6%) | 12/46 (26.1%) | 13/46 (28.3%) | 13/46 (28.3%) | 13/46 (28.3%) |
| dev | 6 | 13/46 (28.3%) | 10/46 (21.7%) | 12/46 (26.1%) | 13/46 (28.3%) | 13/46 (28.3%) | 13/46 (28.3%) |
| test | 1 | 7/46 (15.2%) | 5/46 (10.9%) | 7/46 (15.2%) | 5/46 (10.9%) | 7/46 (15.2%) | 8/46 (17.4%) |
| test | 2 | 8/46 (17.4%) | 5/46 (10.9%) | 7/46 (15.2%) | 7/46 (15.2%) | 8/46 (17.4%) | 8/46 (17.4%) |
| test | 3 | 8/46 (17.4%) | 5/46 (10.9%) | 7/46 (15.2%) | 8/46 (17.4%) | 8/46 (17.4%) | 8/46 (17.4%) |
| test | 4 | 8/46 (17.4%) | 5/46 (10.9%) | 7/46 (15.2%) | 8/46 (17.4%) | 8/46 (17.4%) | 8/46 (17.4%) |
| test | 5 | 8/46 (17.4%) | 5/46 (10.9%) | 7/46 (15.2%) | 8/46 (17.4%) | 8/46 (17.4%) | 8/46 (17.4%) |
| test | 6 | 8/46 (17.4%) | 5/46 (10.9%) | 7/46 (15.2%) | 8/46 (17.4%) | 8/46 (17.4%) | 8/46 (17.4%) |
| all | 1 | 49/230 (21.3%) | 50/230 (21.7%) | 45/230 (19.6%) | 50/230 (21.7%) | 45/230 (19.6%) | 58/230 (25.2%) |
| all | 2 | 55/230 (23.9%) | 50/230 (21.7%) | 46/230 (20.0%) | 56/230 (24.3%) | 54/230 (23.5%) | 58/230 (25.2%) |
| all | 3 | 56/230 (24.3%) | 50/230 (21.7%) | 48/230 (20.9%) | 57/230 (24.8%) | 56/230 (24.3%) | 58/230 (25.2%) |
| all | 4 | 58/230 (25.2%) | 50/230 (21.7%) | 48/230 (20.9%) | 57/230 (24.8%) | 58/230 (25.2%) | 58/230 (25.2%) |
| all | 5 | 58/230 (25.2%) | 51/230 (22.2%) | 48/230 (20.9%) | 58/230 (25.2%) | 58/230 (25.2%) | 58/230 (25.2%) |
| all | 6 | 58/230 (25.2%) | 52/230 (22.6%) | 51/230 (22.2%) | 58/230 (25.2%) | 58/230 (25.2%) | 58/230 (25.2%) |

## 5-Fold Out-of-Fold Results

| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Empty | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 49/230 (21.3%) | 29/230 (12.6%) | 44/230 (19.1%) | 29/230 (12.6%) | 44/230 (19.1%) | 29/230 (12.6%) | 58/230 (25.2%) |
| 2 | 55/230 (23.9%) | 29/230 (12.6%) | 44/230 (19.1%) | 50/230 (21.7%) | 54/230 (23.5%) | 29/230 (12.6%) | 58/230 (25.2%) |
| 3 | 55/230 (23.9%) | 29/230 (12.6%) | 44/230 (19.1%) | 55/230 (23.9%) | 55/230 (23.9%) | 29/230 (12.6%) | 58/230 (25.2%) |
| 4 | 57/230 (24.8%) | 30/230 (13.0%) | 45/230 (19.6%) | 55/230 (23.9%) | 57/230 (24.8%) | 29/230 (12.6%) | 58/230 (25.2%) |
| 5 | 57/230 (24.8%) | 35/230 (15.2%) | 46/230 (20.0%) | 57/230 (24.8%) | 57/230 (24.8%) | 29/230 (12.6%) | 58/230 (25.2%) |
| 6 | 57/230 (24.8%) | 36/230 (15.7%) | 49/230 (21.3%) | 57/230 (24.8%) | 57/230 (24.8%) | 29/230 (12.6%) | 58/230 (25.2%) |

## 5-Fold Strict-Goal Results

| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 20/29 (69.0%) | 0/29 (0.0%) | 15/29 (51.7%) | 0/29 (0.0%) | 15/29 (51.7%) | 29/29 (100.0%) |
| 2 | 26/29 (89.7%) | 0/29 (0.0%) | 15/29 (51.7%) | 21/29 (72.4%) | 25/29 (86.2%) | 29/29 (100.0%) |
| 3 | 26/29 (89.7%) | 0/29 (0.0%) | 15/29 (51.7%) | 26/29 (89.7%) | 26/29 (89.7%) | 29/29 (100.0%) |
| 4 | 28/29 (96.6%) | 1/29 (3.4%) | 16/29 (55.2%) | 26/29 (89.7%) | 28/29 (96.6%) | 29/29 (100.0%) |
| 5 | 28/29 (96.6%) | 6/29 (20.7%) | 17/29 (58.6%) | 28/29 (96.6%) | 28/29 (96.6%) | 29/29 (100.0%) |
| 6 | 28/29 (96.6%) | 7/29 (24.1%) | 20/29 (69.0%) | 28/29 (96.6%) | 28/29 (96.6%) | 29/29 (100.0%) |

## Fixed Greedy Portfolios

| K | Actions | Train-Fitted All Success |
|---:|---|---:|
| 1 | `aesop_core_plus_learned` | 49/230 (21.3%) |
| 2 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` | 55/230 (23.9%) |
| 3 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16` | 56/230 (24.3%) |
| 4 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core` | 58/230 (25.2%) |
| 5 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core` | 58/230 (25.2%) |
| 6 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core`, `aesop_core_facts` | 58/230 (25.2%) |

## Oracle Misses For Train-Greedy Fixed Portfolios

### K=1

- `mathlib4::dist_eq_norm_inv_mul'`: solved by `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`
- `mathlib4::rTensor.inverse_comp_rTensor`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`
- `mathlib4::Projectivization.logHeight_nonneg`: solved by `hammerCore_core_plus_learned`
- `mathlib4::Equiv.Perm.swap_isSwap_iff`: solved by `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`
- `mathlib4::ENNReal.mul_div_right_comm`: solved by `hammerCore_core`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`
- `mathlib4::isMinOn_Ioi_of_deriv`: solved by `hammer_core_plus_learned16`, `hammer_core_plus_learned32`
- `mathlib4::Units.inv_mul_cancel_left`: solved by `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`
- `mathlib4::SkewMonoidAlgebra.sum_mul`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`
- `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst`: solved by `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`

### K=2

- `mathlib4::rTensor.inverse_comp_rTensor`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`
- `mathlib4::isMinOn_Ioi_of_deriv`: solved by `hammer_core_plus_learned16`, `hammer_core_plus_learned32`
- `mathlib4::SkewMonoidAlgebra.sum_mul`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`

### K=3

- `mathlib4::rTensor.inverse_comp_rTensor`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`
- `mathlib4::SkewMonoidAlgebra.sum_mul`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`

### K=4

- None.

### K=5

- None.

### K=6

- None.

## Readout

- OOF fixed greedy K=2 reaches 55/230; residual adaptive K=2 reaches 50/230 (NB) and 54/230 (kNN).
- OOF fixed greedy K=3 reaches 55/230; residual adaptive K=3 reaches 55/230 (NB) and 55/230 (kNN).
- Current evidence favors a compute-budgeted typed portfolio as the hard baseline/main mechanism; richer adaptive routing is not yet clearly above that baseline.
