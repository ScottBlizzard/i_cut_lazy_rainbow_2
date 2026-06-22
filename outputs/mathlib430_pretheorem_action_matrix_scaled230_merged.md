# Mathlib 4.30 Scaled-230 Merged Proof-Action Matrix

Date: 2026-06-22

Inputs:

- `outputs\mathlib430_pretheorem_action_matrix_scaled143.json`
- `outputs\mathlib430_pretheorem_action_matrix_scaled230_extra87_v2.json`

## Summary

| Metric | Value |
|---|---:|
| goals | 230 |
| attempts | 3450 |
| verified attempts | 246 |
| non-empty-premise verified attempts | 205 |
| oracle goals | 51 / 230 |
| non-empty-premise proof goals | 51 / 230 |
| best static action | `hammer_core_plus_learned` |
| best static goals | 31 / 230 |
| oracle gap over best static | +20 goals / +8.70 pp |
| strict action-dependent goals | 22 |

## By Action

| Action | Verified Goals | Verified Attempts | Attempts |
|---|---:|---:|---:|
| `hammer_core_plus_learned` | 31 | 31 | 230 |
| `hammer_core_facts` | 29 | 29 | 230 |
| `hammer_empty` | 29 | 29 | 230 |
| `hammerCore_core_plus_learned` | 18 | 18 | 230 |
| `simp_all_core_plus_learned` | 17 | 17 | 230 |
| `simp_core_plus_learned` | 16 | 16 | 230 |
| `simpa_core_plus_learned` | 16 | 16 | 230 |
| `hammerCore_core` | 14 | 14 | 230 |
| `simp_all_core` | 14 | 14 | 230 |
| `simp_core` | 14 | 14 | 230 |
| `simpa_core` | 14 | 14 | 230 |
| `solve_by_elim_core` | 11 | 11 | 230 |
| `solve_by_elim_core_plus_learned` | 11 | 11 | 230 |
| `simp_empty` | 6 | 6 | 230 |
| `simpa_empty` | 6 | 6 | 230 |

## Strict Action-Dependent Goals

| Goal | Best Action | Facts | Simps |
|---|---|---:|---:|
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | `simp_core` | 0 | 3 |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | `hammerCore_core_plus_learned` | 11 | 10 |
| `mathlib4::ENNReal.mul_div_right_comm` | `hammerCore_core` | 1 | 1 |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | `hammerCore_core_plus_learned` | 10 | 8 |
| `mathlib4::Finsupp.card_Iio` | `simpa_core` | 0 | 2 |
| `mathlib4::Ideal.span_pair_abs` | `simp_core` | 0 | 4 |
| `mathlib4::Matrix.dotProductᵣ_eq` | `simp_core` | 0 | 4 |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | `simp_all_core_plus_learned` | 0 | 3 |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | `simp_core_plus_learned` | 0 | 6 |
| `mathlib4::MeasureTheory.average_const` | `simp_all_core_plus_learned` | 0 | 9 |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | `hammer_core_plus_learned` | 6 | 0 |
| `mathlib4::NumberField.rootDiscr_def` | `simp_core` | 0 | 3 |
| `mathlib4::Polynomial.evalEval_intCast` | `simp_all_core` | 0 | 2 |
| `mathlib4::Projectivization.logHeight_nonneg` | `hammerCore_core_plus_learned` | 12 | 8 |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | `solve_by_elim_core` | 4 | 0 |
| `mathlib4::Stirling.stirlingSeq_one` | `hammerCore_core` | 7 | 7 |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | `simp_core` | 0 | 5 |
| `mathlib4::Units.inv_mul_cancel_left` | `hammerCore_core_plus_learned` | 7 | 5 |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | `solve_by_elim_core_plus_learned` | 9 | 0 |
| `mathlib4::continuousWithinAt_singleton` | `simp_core` | 0 | 3 |
| `mathlib4::dist_eq_norm_inv_mul'` | `hammerCore_core_plus_learned` | 2 | 2 |
| `mathlib4::rTensor.inverse_comp_rTensor` | `solve_by_elim_core` | 3 | 0 |
