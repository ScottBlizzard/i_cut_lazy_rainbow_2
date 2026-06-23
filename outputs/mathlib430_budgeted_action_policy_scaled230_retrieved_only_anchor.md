# Mathlib 4.30 Budgeted Action-Policy Experiment

Date: 2026-06-22

## Setup

- Matrix: `outputs/mathlib430_pretheorem_action_matrix_scaled230_retrieved_only_anchor_merged.json`
- Splits: `outputs/mathlib430_replayable490_splits.json`
- Replayable goals: 230
- Strict action-dependent oracle goals: 23
- Policies always run `hammer_empty` first, then spend K retry actions.
- Learned policies are trained only on the train split, except the OOF table which retrains per fold.

## Train-Fitted Split Results

| Split | K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1 | 29/138 (21.0%) | 32/138 (23.2%) | 25/138 (18.1%) | 32/138 (23.2%) | 25/138 (18.1%) | 32/138 (23.2%) |
| train | 2 | 31/138 (22.5%) | 32/138 (23.2%) | 25/138 (18.1%) | 32/138 (23.2%) | 31/138 (22.5%) | 32/138 (23.2%) |
| train | 3 | 32/138 (23.2%) | 32/138 (23.2%) | 26/138 (18.8%) | 32/138 (23.2%) | 32/138 (23.2%) | 32/138 (23.2%) |
| train | 4 | 32/138 (23.2%) | 32/138 (23.2%) | 26/138 (18.8%) | 32/138 (23.2%) | 32/138 (23.2%) | 32/138 (23.2%) |
| train | 5 | 32/138 (23.2%) | 32/138 (23.2%) | 27/138 (19.6%) | 32/138 (23.2%) | 32/138 (23.2%) | 32/138 (23.2%) |
| train | 6 | 32/138 (23.2%) | 32/138 (23.2%) | 27/138 (19.6%) | 32/138 (23.2%) | 32/138 (23.2%) | 32/138 (23.2%) |
| dev | 1 | 11/46 (23.9%) | 8/46 (17.4%) | 11/46 (23.9%) | 8/46 (17.4%) | 11/46 (23.9%) | 11/46 (23.9%) |
| dev | 2 | 11/46 (23.9%) | 8/46 (17.4%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) |
| dev | 3 | 11/46 (23.9%) | 8/46 (17.4%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) |
| dev | 4 | 11/46 (23.9%) | 8/46 (17.4%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) |
| dev | 5 | 11/46 (23.9%) | 8/46 (17.4%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) |
| dev | 6 | 11/46 (23.9%) | 8/46 (17.4%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) | 11/46 (23.9%) |
| test | 1 | 7/46 (15.2%) | 5/46 (10.9%) | 7/46 (15.2%) | 5/46 (10.9%) | 7/46 (15.2%) | 9/46 (19.6%) |
| test | 2 | 7/46 (15.2%) | 5/46 (10.9%) | 7/46 (15.2%) | 8/46 (17.4%) | 8/46 (17.4%) | 9/46 (19.6%) |
| test | 3 | 9/46 (19.6%) | 5/46 (10.9%) | 7/46 (15.2%) | 8/46 (17.4%) | 9/46 (19.6%) | 9/46 (19.6%) |
| test | 4 | 9/46 (19.6%) | 5/46 (10.9%) | 7/46 (15.2%) | 9/46 (19.6%) | 9/46 (19.6%) | 9/46 (19.6%) |
| test | 5 | 9/46 (19.6%) | 5/46 (10.9%) | 7/46 (15.2%) | 9/46 (19.6%) | 9/46 (19.6%) | 9/46 (19.6%) |
| test | 6 | 9/46 (19.6%) | 5/46 (10.9%) | 7/46 (15.2%) | 9/46 (19.6%) | 9/46 (19.6%) | 9/46 (19.6%) |
| all | 1 | 47/230 (20.4%) | 45/230 (19.6%) | 43/230 (18.7%) | 45/230 (19.6%) | 43/230 (18.7%) | 52/230 (22.6%) |
| all | 2 | 49/230 (21.3%) | 45/230 (19.6%) | 43/230 (18.7%) | 51/230 (22.2%) | 50/230 (21.7%) | 52/230 (22.6%) |
| all | 3 | 52/230 (22.6%) | 45/230 (19.6%) | 44/230 (19.1%) | 51/230 (22.2%) | 52/230 (22.6%) | 52/230 (22.6%) |
| all | 4 | 52/230 (22.6%) | 45/230 (19.6%) | 44/230 (19.1%) | 52/230 (22.6%) | 52/230 (22.6%) | 52/230 (22.6%) |
| all | 5 | 52/230 (22.6%) | 45/230 (19.6%) | 45/230 (19.6%) | 52/230 (22.6%) | 52/230 (22.6%) | 52/230 (22.6%) |
| all | 6 | 52/230 (22.6%) | 45/230 (19.6%) | 45/230 (19.6%) | 52/230 (22.6%) | 52/230 (22.6%) | 52/230 (22.6%) |

## 5-Fold Out-of-Fold Results

| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Empty | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 47/230 (20.4%) | 32/230 (13.9%) | 39/230 (17.0%) | 32/230 (13.9%) | 39/230 (17.0%) | 29/230 (12.6%) | 52/230 (22.6%) |
| 2 | 50/230 (21.7%) | 32/230 (13.9%) | 40/230 (17.4%) | 47/230 (20.4%) | 50/230 (21.7%) | 29/230 (12.6%) | 52/230 (22.6%) |
| 3 | 52/230 (22.6%) | 32/230 (13.9%) | 41/230 (17.8%) | 50/230 (21.7%) | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) |
| 4 | 52/230 (22.6%) | 32/230 (13.9%) | 41/230 (17.8%) | 52/230 (22.6%) | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) |
| 5 | 52/230 (22.6%) | 33/230 (14.3%) | 41/230 (17.8%) | 52/230 (22.6%) | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) |
| 6 | 52/230 (22.6%) | 34/230 (14.8%) | 41/230 (17.8%) | 52/230 (22.6%) | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) |

## 5-Fold Strict-Goal Results

| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 18/23 (78.3%) | 3/23 (13.0%) | 10/23 (43.5%) | 3/23 (13.0%) | 10/23 (43.5%) | 23/23 (100.0%) |
| 2 | 21/23 (91.3%) | 3/23 (13.0%) | 11/23 (47.8%) | 18/23 (78.3%) | 21/23 (91.3%) | 23/23 (100.0%) |
| 3 | 23/23 (100.0%) | 3/23 (13.0%) | 12/23 (52.2%) | 21/23 (91.3%) | 23/23 (100.0%) | 23/23 (100.0%) |
| 4 | 23/23 (100.0%) | 3/23 (13.0%) | 12/23 (52.2%) | 23/23 (100.0%) | 23/23 (100.0%) | 23/23 (100.0%) |
| 5 | 23/23 (100.0%) | 4/23 (17.4%) | 12/23 (52.2%) | 23/23 (100.0%) | 23/23 (100.0%) | 23/23 (100.0%) |
| 6 | 23/23 (100.0%) | 5/23 (21.7%) | 12/23 (52.2%) | 23/23 (100.0%) | 23/23 (100.0%) | 23/23 (100.0%) |

## Fixed Greedy Portfolios

| K | Actions | Train-Fitted All Success |
|---:|---|---:|
| 1 | `aesop_core_plus_learned16` | 47/230 (20.4%) |
| 2 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned` | 49/230 (21.3%) |
| 3 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped` | 52/230 (22.6%) |
| 4 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core` | 52/230 (22.6%) |
| 5 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core`, `aesop_core_facts` | 52/230 (22.6%) |
| 6 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned` | 52/230 (22.6%) |

## Oracle Misses For Train-Greedy Fixed Portfolios

### K=1

- `mathlib4::dist_eq_norm_inv_mul'`: solved by `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`, `rw_core_plus_learned`, `rw_core_plus_learned_then_simp`
- `mathlib4::ENNReal.mul_div_right_comm`: solved by `hammerCore_core_plus_learned`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32`
- `mathlib4::Submodule.mem_ideal_smul_span_iff_exists_sum'`: solved by `aesop_core_plus_learned_swapped`, `aesop_learned8_swapped`
- `mathlib4::MvPowerSeries.coeff_mul_prod_one_sub_of_lt_order`: solved by `aesop_core_plus_learned_swapped`, `aesop_learned8_swapped`
- `mathlib4::Polynomial.cyclotomic_prime_mul_X_sub_one`: solved by `aesop_core_plus_learned_swapped`, `aesop_learned8_swapped`

### K=2

- `mathlib4::Submodule.mem_ideal_smul_span_iff_exists_sum'`: solved by `aesop_core_plus_learned_swapped`, `aesop_learned8_swapped`
- `mathlib4::MvPowerSeries.coeff_mul_prod_one_sub_of_lt_order`: solved by `aesop_core_plus_learned_swapped`, `aesop_learned8_swapped`
- `mathlib4::Polynomial.cyclotomic_prime_mul_X_sub_one`: solved by `aesop_core_plus_learned_swapped`, `aesop_learned8_swapped`

### K=3

- None.

### K=4

- None.

### K=5

- None.

### K=6

- None.

## Readout

- OOF fixed greedy K=2 reaches 50/230; residual adaptive K=2 reaches 47/230 (NB) and 50/230 (kNN).
- OOF fixed greedy K=3 reaches 52/230; residual adaptive K=3 reaches 50/230 (NB) and 52/230 (kNN).
- Current evidence favors a compute-budgeted typed portfolio as the hard baseline/main mechanism; richer adaptive routing is not yet clearly above that baseline.
