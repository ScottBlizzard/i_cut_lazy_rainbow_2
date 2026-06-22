# Mathlib 4.30 Budgeted Action-Policy Experiment

Date: 2026-06-22

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_merged.json`
- Splits: `outputs\mathlib430_replayable490_splits.json`
- Replayable goals: 230
- Strict action-dependent oracle goals: 22
- Policies always run `hammer_empty` first, then spend K retry actions.
- Learned policies are trained only on the train split, except the OOF table which retrains per fold.

## Train-Fitted Split Results

| Split | K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1 | 24/138 (17.4%) | 30/138 (21.7%) | 19/138 (13.8%) | 30/138 (21.7%) | 19/138 (13.8%) | 30/138 (21.7%) |
| train | 2 | 29/138 (21.0%) | 30/138 (21.7%) | 20/138 (14.5%) | 30/138 (21.7%) | 29/138 (21.0%) | 30/138 (21.7%) |
| train | 3 | 30/138 (21.7%) | 30/138 (21.7%) | 25/138 (18.1%) | 30/138 (21.7%) | 30/138 (21.7%) | 30/138 (21.7%) |
| train | 4 | 30/138 (21.7%) | 30/138 (21.7%) | 25/138 (18.1%) | 30/138 (21.7%) | 30/138 (21.7%) | 30/138 (21.7%) |
| dev | 1 | 10/46 (21.7%) | 10/46 (21.7%) | 11/46 (23.9%) | 10/46 (21.7%) | 11/46 (23.9%) | 13/46 (28.3%) |
| dev | 2 | 11/46 (23.9%) | 10/46 (21.7%) | 12/46 (26.1%) | 11/46 (23.9%) | 11/46 (23.9%) | 13/46 (28.3%) |
| dev | 3 | 12/46 (26.1%) | 11/46 (23.9%) | 12/46 (26.1%) | 12/46 (26.1%) | 12/46 (26.1%) | 13/46 (28.3%) |
| dev | 4 | 12/46 (26.1%) | 11/46 (23.9%) | 12/46 (26.1%) | 12/46 (26.1%) | 12/46 (26.1%) | 13/46 (28.3%) |
| test | 1 | 7/46 (15.2%) | 5/46 (10.9%) | 6/46 (13.0%) | 5/46 (10.9%) | 6/46 (13.0%) | 8/46 (17.4%) |
| test | 2 | 8/46 (17.4%) | 5/46 (10.9%) | 6/46 (13.0%) | 7/46 (15.2%) | 7/46 (15.2%) | 8/46 (17.4%) |
| test | 3 | 8/46 (17.4%) | 6/46 (13.0%) | 6/46 (13.0%) | 8/46 (17.4%) | 8/46 (17.4%) | 8/46 (17.4%) |
| test | 4 | 8/46 (17.4%) | 6/46 (13.0%) | 6/46 (13.0%) | 8/46 (17.4%) | 8/46 (17.4%) | 8/46 (17.4%) |
| all | 1 | 41/230 (17.8%) | 45/230 (19.6%) | 36/230 (15.7%) | 45/230 (19.6%) | 36/230 (15.7%) | 51/230 (22.2%) |
| all | 2 | 48/230 (20.9%) | 45/230 (19.6%) | 38/230 (16.5%) | 48/230 (20.9%) | 47/230 (20.4%) | 51/230 (22.2%) |
| all | 3 | 50/230 (21.7%) | 47/230 (20.4%) | 43/230 (18.7%) | 50/230 (21.7%) | 50/230 (21.7%) | 51/230 (22.2%) |
| all | 4 | 50/230 (21.7%) | 47/230 (20.4%) | 43/230 (18.7%) | 50/230 (21.7%) | 50/230 (21.7%) | 51/230 (22.2%) |

## 5-Fold Out-of-Fold Results

| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Empty | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 38/230 (16.5%) | 37/230 (16.1%) | 34/230 (14.8%) | 37/230 (16.1%) | 34/230 (14.8%) | 29/230 (12.6%) | 51/230 (22.2%) |
| 2 | 48/230 (20.9%) | 38/230 (16.5%) | 35/230 (15.2%) | 45/230 (19.6%) | 46/230 (20.0%) | 29/230 (12.6%) | 51/230 (22.2%) |
| 3 | 48/230 (20.9%) | 43/230 (18.7%) | 41/230 (17.8%) | 50/230 (21.7%) | 48/230 (20.9%) | 29/230 (12.6%) | 51/230 (22.2%) |
| 4 | 50/230 (21.7%) | 45/230 (19.6%) | 46/230 (20.0%) | 50/230 (21.7%) | 50/230 (21.7%) | 29/230 (12.6%) | 51/230 (22.2%) |

## 5-Fold Strict-Goal Results

| K | Fixed Greedy | Pure NB | Pure kNN | Fixed Prefix + Residual NB | Fixed Prefix + Residual kNN | Oracle |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 9/22 (40.9%) | 8/22 (36.4%) | 5/22 (22.7%) | 8/22 (36.4%) | 5/22 (22.7%) | 22/22 (100.0%) |
| 2 | 19/22 (86.4%) | 9/22 (40.9%) | 6/22 (27.3%) | 16/22 (72.7%) | 17/22 (77.3%) | 22/22 (100.0%) |
| 3 | 19/22 (86.4%) | 14/22 (63.6%) | 12/22 (54.5%) | 21/22 (95.5%) | 19/22 (86.4%) | 22/22 (100.0%) |
| 4 | 21/22 (95.5%) | 16/22 (72.7%) | 17/22 (77.3%) | 21/22 (95.5%) | 21/22 (95.5%) | 22/22 (100.0%) |

## Fixed Greedy Portfolios

| K | Actions | Train-Fitted All Success |
|---:|---|---:|
| 1 | `hammerCore_core_plus_learned` | 41/230 (17.8%) |
| 2 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned` | 48/230 (20.9%) |
| 3 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 50/230 (21.7%) |
| 4 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core`, `hammerCore_core` | 50/230 (21.7%) |

## Oracle Misses For Train-Greedy Fixed Portfolios

### K=1

- `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd`: solved by `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned`
- `mathlib4::Polynomial.evalEval_intCast`: solved by `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned`
- `mathlib4::rTensor.inverse_comp_rTensor`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`
- `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom`: solved by `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned`
- `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'`: solved by `hammer_core_plus_learned`, `simp_all_core_plus_learned`
- `mathlib4::MeasureTheory.average_const`: solved by `simp_all_core_plus_learned`, `simp_core_plus_learned`, `simpa_core_plus_learned`
- `mathlib4::Nat.Primes.PNat.Prime.ne_one`: solved by `hammer_core_plus_learned`
- `mathlib4::MeasureTheory.Measure.compProd_apply_univ`: solved by `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned`
- `mathlib4::SkewMonoidAlgebra.sum_mul`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`
- `mathlib4::Matrix.dotProductᵣ_eq`: solved by `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned`

### K=2

- `mathlib4::rTensor.inverse_comp_rTensor`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`
- `mathlib4::Nat.Primes.PNat.Prime.ne_one`: solved by `hammer_core_plus_learned`
- `mathlib4::SkewMonoidAlgebra.sum_mul`: solved by `solve_by_elim_core`, `solve_by_elim_core_plus_learned`

### K=3

- `mathlib4::Nat.Primes.PNat.Prime.ne_one`: solved by `hammer_core_plus_learned`

### K=4

- `mathlib4::Nat.Primes.PNat.Prime.ne_one`: solved by `hammer_core_plus_learned`

## Readout

- OOF fixed greedy K=2 reaches 48/230; residual adaptive K=2 reaches 45/230 (NB) and 46/230 (kNN).
- OOF fixed greedy K=3 reaches 48/230; residual adaptive K=3 reaches 50/230 (NB) and 48/230 (kNN).
- Current evidence favors a compute-budgeted typed portfolio as the hard baseline/main mechanism; richer adaptive routing is not yet clearly above that baseline.
