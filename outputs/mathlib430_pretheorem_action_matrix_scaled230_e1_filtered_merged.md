# Mathlib 4.30 Scaled-230 Merged Proof-Action Matrix

Date: 2026-06-22

Inputs:

- `outputs\mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- `outputs\mathlib430_pretheorem_action_matrix_e1_filtered230_part0.json`
- `outputs\mathlib430_pretheorem_action_matrix_e1_filtered230_part1.json`

## Summary

| Metric | Value |
|---|---:|
| goals | 230 |
| attempts | 12650 |
| verified attempts | 592 |
| non-empty-premise verified attempts | 518 |
| oracle goals | 58 / 230 |
| non-empty-premise proof goals | 58 / 230 |
| best static action | `aesop_core_plus_learned` |
| best static goals | 38 / 230 |
| oracle gap over best static | +20 goals / +8.70 pp |
| strict action-dependent goals | 29 |

## By Action

| Action | Verified Goals | Verified Attempts | Attempts |
|---|---:|---:|---:|
| `aesop_core_plus_learned` | 38 | 38 | 230 |
| `aesop_core_plus_learned16` | 37 | 37 | 230 |
| `hammer_core_plus_learned16` | 32 | 32 | 230 |
| `hammer_core_plus_learned32` | 32 | 32 | 230 |
| `hammer_core_plus_learned` | 31 | 31 | 230 |
| `aesop_empty` | 29 | 29 | 230 |
| `hammer_core_facts` | 29 | 29 | 230 |
| `hammer_empty` | 29 | 29 | 230 |
| `hammerCore_core_plus_learned` | 18 | 18 | 230 |
| `simp_all_core_plus_learned16` | 18 | 18 | 230 |
| `simp_all_core_plus_learned32` | 18 | 18 | 230 |
| `simp_all_core_plus_learned` | 17 | 17 | 230 |
| `simp_core_plus_learned` | 16 | 16 | 230 |
| `simpa_core_plus_learned` | 16 | 16 | 230 |
| `hammerCore_core_plus_learned16` | 15 | 15 | 230 |
| `hammerCore_core_plus_learned32` | 15 | 15 | 230 |
| `hammerCore_core` | 14 | 14 | 230 |
| `simp_all_core` | 14 | 14 | 230 |
| `simp_core` | 14 | 14 | 230 |
| `simpa_core` | 14 | 14 | 230 |
| `solve_by_elim_core` | 11 | 11 | 230 |
| `solve_by_elim_core_plus_learned` | 11 | 11 | 230 |
| `solve_by_elim_core_plus_learned16` | 11 | 11 | 230 |
| `solve_by_elim_core_plus_learned32` | 11 | 11 | 230 |
| `simp_empty` | 6 | 6 | 230 |
| `simpa_empty` | 6 | 6 | 230 |
| `aesop_core_facts` | 5 | 5 | 230 |
| `aesop_core_plus_learned16_facts` | 5 | 5 | 230 |
| `aesop_core_plus_learned32_facts` | 5 | 5 | 230 |
| `aesop_core_plus_learned_facts` | 5 | 5 | 230 |
| `aesop_learned16_facts` | 5 | 5 | 230 |
| `aesop_learned32_facts` | 5 | 5 | 230 |
| `aesop_learned8_facts` | 5 | 5 | 230 |
| `aesop_core` | 4 | 4 | 230 |
| `aesop_core_plus_learned_simps` | 4 | 4 | 230 |
| `aesop_core_simps` | 4 | 4 | 230 |
| `aesop_learned8` | 4 | 4 | 230 |
| `aesop_learned8_simps` | 4 | 4 | 230 |
| `norm_num_empty` | 4 | 4 | 230 |
| `aesop_core_plus_learned16_filtered` | 3 | 3 | 230 |
| `aesop_core_plus_learned16_simps` | 3 | 3 | 230 |
| `aesop_core_plus_learned32` | 3 | 3 | 230 |
| `aesop_core_plus_learned32_simps` | 3 | 3 | 230 |
| `aesop_core_plus_learned_filtered` | 3 | 3 | 230 |
| `aesop_learned16` | 3 | 3 | 230 |
| `aesop_learned16_simps` | 3 | 3 | 230 |
| `aesop_learned32` | 3 | 3 | 230 |
| `aesop_learned32_simps` | 3 | 3 | 230 |
| `hammer_core_plus_learned16_filtered` | 3 | 3 | 230 |
| `hammerCore_core_plus_learned_filtered` | 1 | 1 | 230 |
| `linarith_empty` | 0 | 0 | 230 |
| `nlinarith_empty` | 0 | 0 | 230 |
| `omega_empty` | 0 | 0 | 230 |
| `ring_nf_empty` | 0 | 0 | 230 |
| `solve_by_elim_core_filtered` | 0 | 0 | 230 |

## Strict Action-Dependent Goals

| Goal | Best Action | Facts | Simps |
|---|---|---:|---:|
| `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms` | `aesop_core_plus_learned` | 13 | 9 |
| `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply` | `aesop_core_plus_learned16` | 18 | 9 |
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | `simp_all_core_plus_learned16` | 0 | 16 |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | `hammerCore_core_plus_learned16` | 11 | 18 |
| `mathlib4::ENNReal.mul_div_right_comm` | `solve_by_elim_core_plus_learned16` | 15 | 0 |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | `hammerCore_core_plus_learned32` | 14 | 11 |
| `mathlib4::Finsupp.card_Iio` | `simp_all_core_plus_learned32` | 0 | 8 |
| `mathlib4::Ideal.span_pair_abs` | `aesop_core_plus_learned16` | 16 | 8 |
| `mathlib4::Matrix.dotProductᵣ_eq` | `aesop_core_plus_learned` | 9 | 9 |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | `aesop_core_plus_learned16` | 7 | 3 |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | `aesop_core_plus_learned` | 10 | 6 |
| `mathlib4::MeasureTheory.average_const` | `aesop_core_plus_learned` | 10 | 9 |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | `hammer_core_plus_learned16` | 6 | 0 |
| `mathlib4::NormedAddCommGroup.summable_imp_tendsto_of_complete` | `aesop_core_plus_learned16` | 15 | 6 |
| `mathlib4::NumberField.rootDiscr_def` | `solve_by_elim_core_plus_learned16` | 9 | 0 |
| `mathlib4::Polynomial.evalEval_intCast` | `simp_all_core_plus_learned16` | 0 | 12 |
| `mathlib4::Projectivization.logHeight_nonneg` | `hammerCore_core_plus_learned` | 12 | 8 |
| `mathlib4::RatFunc.InftyValuation.map_mul'` | `aesop_core_plus_learned` | 10 | 9 |
| `mathlib4::Real.sign_apply_eq` | `aesop_core_plus_learned` | 6 | 6 |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | `solve_by_elim_core_plus_learned32` | 10 | 0 |
| `mathlib4::Stirling.stirlingSeq_one` | `aesop_core_plus_learned` | 9 | 8 |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | `simp_all_core_plus_learned32` | 0 | 18 |
| `mathlib4::Units.inv_mul_cancel_left` | `hammerCore_core_plus_learned_filtered` | 7 | 3 |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | `aesop_core_plus_learned16` | 10 | 16 |
| `mathlib4::continuousWithinAt_singleton` | `aesop_core_plus_learned` | 5 | 3 |
| `mathlib4::dist_eq_norm_inv_mul'` | `hammerCore_core_plus_learned32` | 2 | 2 |
| `mathlib4::isMinOn_Ioi_of_deriv` | `hammer_core_plus_learned32` | 27 | 0 |
| `mathlib4::mem_balancedCore_iff` | `aesop_core_plus_learned` | 8 | 7 |
| `mathlib4::rTensor.inverse_comp_rTensor` | `solve_by_elim_core_plus_learned32` | 15 | 0 |
