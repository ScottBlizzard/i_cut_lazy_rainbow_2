# Mathlib 4.30 Strict Action-Dependent Taxonomy

Date: 2026-06-22

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_merged.json`
- Goals in matrix: 230
- Strict action-dependent goals: 22
- Strict means `hammer_empty` fails but at least one non-empty or non-default proof-action succeeds.

## Family Coverage

| Family | Strict goals solved |
|---|---:|
| `hammerCore` | 12 / 22 (54.5%) |
| `simp_all` | 12 / 22 (54.5%) |
| `simp` | 11 / 22 (50.0%) |
| `simpa` | 11 / 22 (50.0%) |
| `solve_by_elim` | 5 / 22 (22.7%) |
| `hammer` | 2 / 22 (9.1%) |

## Only-Family Cases

| Family | Goals where this is the only successful family |
|---|---:|
| `hammerCore` | 6 |
| `solve_by_elim` | 2 |
| `hammer` | 1 |

## Action Coverage

| Action | Strict goals solved |
|---|---:|
| `hammerCore_core_plus_learned` | 12 |
| `simp_all_core_plus_learned` | 12 |
| `simp_core_plus_learned` | 11 |
| `simpa_core_plus_learned` | 11 |
| `hammerCore_core` | 9 |
| `simp_all_core` | 9 |
| `simp_core` | 9 |
| `simpa_core` | 9 |
| `solve_by_elim_core` | 5 |
| `solve_by_elim_core_plus_learned` | 5 |
| `hammer_core_plus_learned` | 2 |

## Per-Goal Details

| Goal | Families | Verified actions | Facts / Simps |
|---|---|---|---|
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | `simp`, `simp_all`, `simpa` | `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 0f/3s, 0f/9s, 0f/3s, 0f/9s, 0f/3s, 0f/9s |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | `hammerCore` | `hammerCore_core_plus_learned` | 11f/10s |
| `mathlib4::ENNReal.mul_div_right_comm` | `hammerCore`, `solve_by_elim` | `hammerCore_core`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `solve_by_elim_core_plus_learned` | 1f/1s, 8f/5s, 1f/0s, 8f/0s |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | `hammerCore` | `hammerCore_core_plus_learned` | 10f/8s |
| `mathlib4::Finsupp.card_Iio` | `hammerCore`, `simp`, `simp_all`, `simpa` | `hammerCore_core`, `hammerCore_core_plus_learned`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 2f/2s, 9f/8s, 0f/2s, 0f/8s, 0f/2s, 0f/8s, 0f/2s, 0f/8s |
| `mathlib4::Ideal.span_pair_abs` | `hammerCore`, `simp`, `simp_all`, `simpa` | `hammerCore_core`, `hammerCore_core_plus_learned`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 4f/4s, 12f/8s, 0f/4s, 0f/8s, 0f/4s, 0f/8s, 0f/4s, 0f/8s |
| `mathlib4::Matrix.dotProductᵣ_eq` | `simp`, `simp_all`, `simpa` | `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 0f/4s, 0f/9s, 0f/4s, 0f/9s, 0f/4s, 0f/9s |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | `hammer`, `simp_all` | `hammer_core_plus_learned`, `simp_all_core_plus_learned` | 7f/0s, 0f/3s |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | `simp`, `simp_all`, `simpa` | `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 0f/2s, 0f/6s, 0f/2s, 0f/6s, 0f/2s, 0f/6s |
| `mathlib4::MeasureTheory.average_const` | `simp`, `simp_all`, `simpa` | `simp_all_core_plus_learned`, `simp_core_plus_learned`, `simpa_core_plus_learned` | 0f/9s, 0f/9s, 0f/9s |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | `hammer` | `hammer_core_plus_learned` | 6f/0s |
| `mathlib4::NumberField.rootDiscr_def` | `hammerCore`, `simp`, `simp_all`, `simpa`, `solve_by_elim` | `hammerCore_core`, `hammerCore_core_plus_learned`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned`, `solve_by_elim_core`, `solve_by_elim_core_plus_learned` | 3f/3s, 9f/8s, 0f/3s, 0f/8s, 0f/3s, 0f/8s, 0f/3s, 0f/8s, 3f/0s, 9f/0s |
| `mathlib4::Polynomial.evalEval_intCast` | `simp`, `simp_all`, `simpa` | `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 0f/2s, 0f/9s, 0f/2s, 0f/9s, 0f/2s, 0f/9s |
| `mathlib4::Projectivization.logHeight_nonneg` | `hammerCore` | `hammerCore_core_plus_learned` | 12f/8s |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | `solve_by_elim` | `solve_by_elim_core`, `solve_by_elim_core_plus_learned` | 4f/0s, 10f/0s |
| `mathlib4::Stirling.stirlingSeq_one` | `hammerCore` | `hammerCore_core`, `hammerCore_core_plus_learned` | 7f/7s, 9f/8s |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | `simp`, `simp_all`, `simpa` | `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 0f/5s, 0f/11s, 0f/5s, 0f/11s, 0f/5s, 0f/11s |
| `mathlib4::Units.inv_mul_cancel_left` | `hammerCore` | `hammerCore_core`, `hammerCore_core_plus_learned` | 3f/3s, 7f/5s |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | `hammerCore`, `simp`, `simp_all`, `simpa`, `solve_by_elim` | `hammerCore_core`, `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `simp_core_plus_learned`, `simpa_core_plus_learned`, `solve_by_elim_core`, `solve_by_elim_core_plus_learned` | 1f/1s, 9f/9s, 0f/9s, 0f/9s, 0f/9s, 1f/0s, 9f/0s |
| `mathlib4::continuousWithinAt_singleton` | `hammerCore`, `simp`, `simp_all`, `simpa` | `hammerCore_core`, `hammerCore_core_plus_learned`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 3f/3s, 5f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s |
| `mathlib4::dist_eq_norm_inv_mul'` | `hammerCore` | `hammerCore_core`, `hammerCore_core_plus_learned` | 2f/2s, 2f/2s |
| `mathlib4::rTensor.inverse_comp_rTensor` | `solve_by_elim` | `solve_by_elim_core`, `solve_by_elim_core_plus_learned` | 3f/0s, 11f/0s |

## Readout

- The largest only-family bucket is `hammerCore` with 6 strict goals.
- The strict positives are not a single-premise-budget effect: different Lean interfaces solve disjoint subsets of replayable theorem contexts.
