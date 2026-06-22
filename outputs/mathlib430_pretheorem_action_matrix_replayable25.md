# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_50.json`
- Replayable goals evaluated: 25
- Attempts: 275
- Verified attempts: 22
- Non-empty-premise verified attempts: 17
- Goals with any proof: 6
- Goals with non-empty-premise proof: 6
- Action-dependent goals: 3

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 84 |
| `proved` | 22 |
| `rewrite_fail` | 3 |
| `search_fail` | 64 |
| `simp_fail` | 90 |
| `sorry_warning` | 9 |
| `timeout` | 3 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `hammerCore_core` | 1 | 1 | 25 |
| `hammerCore_core_plus_learned` | 2 | 2 | 25 |
| `hammer_core_facts` | 3 | 3 | 25 |
| `hammer_core_plus_learned` | 3 | 3 | 25 |
| `hammer_empty` | 3 | 0 | 25 |
| `simp_core` | 2 | 2 | 25 |
| `simp_core_plus_learned` | 2 | 2 | 25 |
| `simp_empty` | 1 | 0 | 25 |
| `simpa_core` | 2 | 2 | 25 |
| `simpa_core_plus_learned` | 2 | 2 | 25 |
| `simpa_empty` | 1 | 0 | 25 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 9 | 6 | 3 | `hammer_empty` (0 facts, 0 simps) |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 4 | 4 | 0 | `simp_core` (0 facts, 2 simps) |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 3 | 2 | 1 | `hammer_empty` (0 facts, 0 simps) |
| `mathlib4::Set.Intersecting.insert` | 0 | 0 | 0 | none |
| `mathlib4::nhds_le_of_le` | 0 | 0 | 0 | none |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 0 | 0 | 0 | none |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 0 | 0 | 0 | none |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | 0 | 0 | 0 | none |
| `mathlib4::Sym.Sym2.card_image_diag` | 0 | 0 | 0 | none |
| `mathlib4::isChain_preimage_subtypeVal` | 0 | 0 | 0 | none |
| `mathlib4::IsLocalRing.Module.IsLocalRing.linearCombination_bijective_of_flat` | 0 | 0 | 0 | none |
| `mathlib4::Commute.isNilpotent_mul_left_iff` | 0 | 0 | 0 | none |
| `mathlib4::Algebra.Presentation.aeval_comp_val_eq` | 3 | 2 | 1 | `hammer_empty` (0 facts, 0 simps) |
| `mathlib4::Projectivization.logHeight_nonneg` | 1 | 1 | 0 | `hammerCore_core_plus_learned` (12 facts, 8 simps) |
| `mathlib4::WeierstrassCurve.Projective.nonsingular_some` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.injective_algebraMap_quotient_residueField` | 0 | 0 | 0 | none |
| `mathlib4::Nat.descPochhammer_pos` | 0 | 0 | 0 | none |
| `mathlib4::Rep.groupHomology.inhomogeneousChains.iCycles_mk` | 0 | 0 | 0 | none |
| `mathlib4::Stream'.Seq.length_map` | 0 | 0 | 0 | none |
| `mathlib4::Units.inv_mul_cancel_left` | 2 | 2 | 0 | `hammerCore_core` (3 facts, 3 simps) |
| `mathlib4::CochainComplex.HomComplex.Cochain.rightUnshift_add` | 0 | 0 | 0 | none |
| `mathlib4::CompleteLattice.IsCompactElement.directed_sSup_lt_of_lt` | 0 | 0 | 0 | none |
| `mathlib4::SimpleGraph.Iso.edgeFinset_map` | 0 | 0 | 0 | none |
| `mathlib4::Finset.map_add_right_Ioc` | 0 | 0 | 0 | none |

## Availability

| Goal | Checked | Available | Failed |
|---|---:|---:|---:|
| `mathlib4::Module.rank_tensorProduct'` | 32 | 22 | 10 |
| `mathlib4::FirstOrder.Language.definableFun_const` | 33 | 17 | 16 |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 32 | 12 | 20 |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 32 | 16 | 16 |
| `mathlib4::Set.Intersecting.insert` | 32 | 16 | 16 |
| `mathlib4::nhds_le_of_le` | 32 | 4 | 28 |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 34 | 11 | 23 |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 32 | 12 | 20 |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | 32 | 19 | 13 |
| `mathlib4::Sym.Sym2.card_image_diag` | 32 | 23 | 9 |
| `mathlib4::isChain_preimage_subtypeVal` | 32 | 11 | 21 |
| `mathlib4::IsLocalRing.Module.IsLocalRing.linearCombination_bijective_of_flat` | 32 | 20 | 12 |
| `mathlib4::Commute.isNilpotent_mul_left_iff` | 33 | 30 | 3 |
| `mathlib4::Algebra.Presentation.aeval_comp_val_eq` | 32 | 25 | 7 |
| `mathlib4::Projectivization.logHeight_nonneg` | 34 | 21 | 13 |
| `mathlib4::WeierstrassCurve.Projective.nonsingular_some` | 37 | 21 | 16 |
| `mathlib4::Ideal.injective_algebraMap_quotient_residueField` | 32 | 9 | 23 |
| `mathlib4::Nat.descPochhammer_pos` | 33 | 26 | 7 |
| `mathlib4::Rep.groupHomology.inhomogeneousChains.iCycles_mk` | 33 | 8 | 25 |
| `mathlib4::Stream'.Seq.length_map` | 33 | 15 | 18 |
| `mathlib4::Units.inv_mul_cancel_left` | 33 | 8 | 25 |
| `mathlib4::CochainComplex.HomComplex.Cochain.rightUnshift_add` | 33 | 16 | 17 |
| `mathlib4::CompleteLattice.IsCompactElement.directed_sSup_lt_of_lt` | 32 | 13 | 19 |
| `mathlib4::SimpleGraph.Iso.edgeFinset_map` | 32 | 28 | 4 |
| `mathlib4::Finset.map_add_right_Ioc` | 32 | 11 | 21 |

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
