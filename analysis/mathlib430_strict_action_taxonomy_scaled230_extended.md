# Mathlib 4.30 Strict Action-Dependent Taxonomy

Date: 2026-06-22

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_extended_merged.json`
- Goals in matrix: 230
- Strict action-dependent goals: 29
- Strict means `hammer_empty` fails but at least one non-empty or non-default proof-action succeeds.

## Family Coverage

| Family | Strict goals solved |
|---|---:|
| `aesop` | 20 / 29 (69.0%) |
| `hammerCore` | 12 / 29 (41.4%) |
| `simp_all` | 12 / 29 (41.4%) |
| `simp` | 11 / 29 (37.9%) |
| `simpa` | 11 / 29 (37.9%) |
| `solve_by_elim` | 5 / 29 (17.2%) |
| `hammer` | 3 / 29 (10.3%) |

## Only-Family Cases

| Family | Goals where this is the only successful family |
|---|---:|
| `aesop` | 6 |
| `hammerCore` | 5 |
| `solve_by_elim` | 2 |
| `hammer` | 1 |

## Action Coverage

| Action | Strict goals solved |
|---|---:|
| `aesop_core_plus_learned` | 20 |
| `aesop_core_plus_learned16` | 20 |
| `hammerCore_core_plus_learned` | 12 |
| `simp_all_core_plus_learned` | 12 |
| `simp_all_core_plus_learned16` | 12 |
| `simp_all_core_plus_learned32` | 12 |
| `simp_core_plus_learned` | 11 |
| `simpa_core_plus_learned` | 11 |
| `hammerCore_core_plus_learned16` | 10 |
| `hammerCore_core_plus_learned32` | 10 |
| `hammerCore_core` | 9 |
| `simp_all_core` | 9 |
| `simp_core` | 9 |
| `simpa_core` | 9 |
| `solve_by_elim_core` | 5 |
| `solve_by_elim_core_plus_learned` | 5 |
| `solve_by_elim_core_plus_learned16` | 5 |
| `solve_by_elim_core_plus_learned32` | 5 |
| `hammer_core_plus_learned16` | 3 |
| `hammer_core_plus_learned32` | 3 |
| `hammer_core_plus_learned` | 2 |

## Per-Goal Details

| Goal | Families | Verified actions | Facts / Simps |
|---|---|---|---|
| `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms` | `aesop` | `aesop_core_plus_learned`, `aesop_core_plus_learned16` | 13f/9s, 19f/9s |
| `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply` | `aesop` | `aesop_core_plus_learned`, `aesop_core_plus_learned16` | 12f/8s, 18f/9s |
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | `aesop`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 7f/9s, 7f/16s, 0f/3s, 0f/9s, 0f/16s, 0f/18s, 0f/3s, 0f/9s, 0f/3s, 0f/9s |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | `hammerCore` | `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32` | 11f/10s, 11f/18s, 11f/19s |
| `mathlib4::ENNReal.mul_div_right_comm` | `hammerCore`, `solve_by_elim` | `hammerCore_core`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32` | 1f/1s, 8f/5s, 1f/0s, 8f/0s, 15f/0s, 15f/0s |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | `hammerCore` | `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32` | 10f/8s, 14f/11s, 14f/11s |
| `mathlib4::Finsupp.card_Iio` | `aesop`, `hammerCore`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 9f/8s, 16f/8s, 2f/2s, 9f/8s, 16f/8s, 16f/8s, 0f/2s, 0f/8s, 0f/8s, 0f/8s, 0f/2s, 0f/8s, 0f/2s, 0f/8s |
| `mathlib4::Ideal.span_pair_abs` | `aesop`, `hammerCore`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 12f/8s, 16f/8s, 4f/4s, 12f/8s, 16f/8s, 16f/8s, 0f/4s, 0f/8s, 0f/8s, 0f/8s, 0f/4s, 0f/8s, 0f/4s, 0f/8s |
| `mathlib4::Matrix.dotProductᵣ_eq` | `aesop`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 9f/9s, 9f/10s, 0f/4s, 0f/9s, 0f/10s, 0f/10s, 0f/4s, 0f/9s, 0f/4s, 0f/9s |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | `aesop`, `hammer`, `simp_all` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammer_core_plus_learned`, `hammer_core_plus_learned16`, `hammer_core_plus_learned32`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32` | 7f/3s, 7f/3s, 7f/0s, 7f/0s, 7f/0s, 0f/3s, 0f/3s, 0f/3s |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | `aesop`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 10f/6s, 10f/6s, 0f/2s, 0f/6s, 0f/6s, 0f/6s, 0f/2s, 0f/6s, 0f/2s, 0f/6s |
| `mathlib4::MeasureTheory.average_const` | `aesop`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core_plus_learned`, `simpa_core_plus_learned` | 10f/9s, 18f/12s, 0f/9s, 0f/12s, 0f/12s, 0f/9s, 0f/9s |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | `aesop`, `hammer` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammer_core_plus_learned`, `hammer_core_plus_learned16`, `hammer_core_plus_learned32` | 6f/2s, 6f/2s, 6f/0s, 6f/0s, 6f/0s |
| `mathlib4::NormedAddCommGroup.summable_imp_tendsto_of_complete` | `aesop` | `aesop_core_plus_learned`, `aesop_core_plus_learned16` | 12f/6s, 15f/6s |
| `mathlib4::NumberField.rootDiscr_def` | `aesop`, `hammerCore`, `simp`, `simp_all`, `simpa`, `solve_by_elim` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned`, `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32` | 9f/8s, 9f/12s, 3f/3s, 9f/8s, 9f/12s, 9f/12s, 0f/3s, 0f/8s, 0f/12s, 0f/12s, 0f/3s, 0f/8s, 0f/3s, 0f/8s, 3f/0s, 9f/0s, 9f/0s, 9f/0s |
| `mathlib4::Polynomial.evalEval_intCast` | `aesop`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 10f/9s, 15f/12s, 0f/2s, 0f/9s, 0f/12s, 0f/12s, 0f/2s, 0f/9s, 0f/2s, 0f/9s |
| `mathlib4::Projectivization.logHeight_nonneg` | `hammerCore` | `hammerCore_core_plus_learned` | 12f/8s |
| `mathlib4::RatFunc.InftyValuation.map_mul'` | `aesop` | `aesop_core_plus_learned`, `aesop_core_plus_learned16` | 10f/9s, 10f/11s |
| `mathlib4::Real.sign_apply_eq` | `aesop` | `aesop_core_plus_learned`, `aesop_core_plus_learned16` | 6f/6s, 6f/6s |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | `solve_by_elim` | `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32` | 4f/0s, 10f/0s, 10f/0s, 10f/0s |
| `mathlib4::Stirling.stirlingSeq_one` | `aesop`, `hammerCore` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32` | 9f/8s, 9f/9s, 7f/7s, 9f/8s, 9f/9s, 9f/9s |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | `aesop`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 9f/11s, 9f/17s, 0f/5s, 0f/11s, 0f/17s, 0f/18s, 0f/5s, 0f/11s, 0f/5s, 0f/11s |
| `mathlib4::Units.inv_mul_cancel_left` | `hammerCore` | `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32` | 3f/3s, 7f/5s, 7f/5s, 7f/5s |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | `aesop`, `hammerCore`, `simp`, `simp_all`, `simpa`, `solve_by_elim` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core_plus_learned`, `simpa_core_plus_learned`, `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32` | 9f/9s, 10f/16s, 1f/1s, 9f/9s, 10f/16s, 10f/16s, 0f/9s, 0f/16s, 0f/16s, 0f/9s, 0f/9s, 1f/0s, 9f/0s, 10f/0s, 10f/0s |
| `mathlib4::continuousWithinAt_singleton` | `aesop`, `hammerCore`, `simp`, `simp_all`, `simpa` | `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32`, `simp_all_core`, `simp_all_core_plus_learned`, `simp_all_core_plus_learned16`, `simp_all_core_plus_learned32`, `simp_core`, `simp_core_plus_learned`, `simpa_core`, `simpa_core_plus_learned` | 5f/3s, 5f/3s, 3f/3s, 5f/3s, 5f/3s, 5f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s, 0f/3s |
| `mathlib4::dist_eq_norm_inv_mul'` | `hammerCore` | `hammerCore_core`, `hammerCore_core_plus_learned`, `hammerCore_core_plus_learned16`, `hammerCore_core_plus_learned32` | 2f/2s, 2f/2s, 2f/2s, 2f/2s |
| `mathlib4::isMinOn_Ioi_of_deriv` | `hammer` | `hammer_core_plus_learned16`, `hammer_core_plus_learned32` | 23f/0s, 27f/0s |
| `mathlib4::mem_balancedCore_iff` | `aesop` | `aesop_core_plus_learned`, `aesop_core_plus_learned16` | 8f/7s, 8f/7s |
| `mathlib4::rTensor.inverse_comp_rTensor` | `solve_by_elim` | `solve_by_elim_core`, `solve_by_elim_core_plus_learned`, `solve_by_elim_core_plus_learned16`, `solve_by_elim_core_plus_learned32` | 3f/0s, 11f/0s, 15f/0s, 15f/0s |

## Readout

- The largest only-family bucket is `aesop` with 6 strict goals.
- The strict positives are not a single-premise-budget effect: different Lean interfaces solve disjoint subsets of replayable theorem contexts.
