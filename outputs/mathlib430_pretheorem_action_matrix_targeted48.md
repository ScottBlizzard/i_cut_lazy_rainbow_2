# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_100.json`
- Replayable goals evaluated: 48
- Attempts: 288
- Verified attempts: 8
- Non-empty-premise verified attempts: 8
- Goals with any proof: 4
- Goals with non-empty-premise proof: 4
- Action-dependent goals: 4

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 78 |
| `proved` | 8 |
| `rewrite_fail` | 91 |
| `search_fail` | 81 |
| `simp_fail` | 3 |
| `sorry_warning` | 22 |
| `typeclass_or_inference` | 1 |
| `unknown_identifier` | 4 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `simp_all_core` | 2 | 2 | 48 |
| `simp_all_core_plus_learned` | 2 | 2 | 48 |
| `simp_rw_core` | 0 | 0 | 48 |
| `simp_rw_core_plus_learned` | 0 | 0 | 48 |
| `solve_by_elim_core` | 2 | 2 | 48 |
| `solve_by_elim_core_plus_learned` | 2 | 2 | 48 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 2 | 2 | 0 | `simp_all_core` (0 facts, 1 simps) |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 2 | 2 | 0 | `simp_all_core` (0 facts, 2 simps) |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 0 | 0 | 0 | none |
| `mathlib4::Set.Intersecting.insert` | 0 | 0 | 0 | none |
| `mathlib4::nhds_le_of_le` | 0 | 0 | 0 | none |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 0 | 0 | 0 | none |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 0 | 0 | 0 | none |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | 0 | 0 | 0 | none |
| `mathlib4::Sym.Sym2.card_image_diag` | 0 | 0 | 0 | none |
| `mathlib4::isChain_preimage_subtypeVal` | 0 | 0 | 0 | none |
| `mathlib4::IsLocalRing.Module.IsLocalRing.linearCombination_bijective_of_flat` | 0 | 0 | 0 | none |
| `mathlib4::Commute.isNilpotent_mul_left_iff` | 0 | 0 | 0 | none |
| `mathlib4::Algebra.Presentation.aeval_comp_val_eq` | 0 | 0 | 0 | none |
| `mathlib4::Projectivization.logHeight_nonneg` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.Projective.nonsingular_some` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.injective_algebraMap_quotient_residueField` | 0 | 0 | 0 | none |
| `mathlib4::Nat.descPochhammer_pos` | 0 | 0 | 0 | none |
| `mathlib4::Rep.groupHomology.inhomogeneousChains.iCycles_mk` | 0 | 0 | 0 | none |
| `mathlib4::Stream'.Seq.length_map` | 0 | 0 | 0 | none |
| `mathlib4::Units.inv_mul_cancel_left` | 0 | 0 | 0 | none |
| `mathlib4::CochainComplex.HomComplex.Cochain.rightUnshift_add` | 0 | 0 | 0 | none |
| `mathlib4::CompleteLattice.IsCompactElement.directed_sSup_lt_of_lt` | 0 | 0 | 0 | none |
| `mathlib4::SimpleGraph.Iso.edgeFinset_map` | 0 | 0 | 0 | none |
| `mathlib4::Finset.map_add_right_Ioc` | 0 | 0 | 0 | none |
| `mathlib4::Finset.Fin.prod_Iio_castSucc` | 0 | 0 | 0 | none |
| `mathlib4::Fintype.Finite.bddBelow_range` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicGeometry.Scheme.Pullback.Triplet.snd_SpecTensorTo_apply` | 0 | 0 | 0 | none |
| `mathlib4::AddCircle.MeasureTheory.fourierBasis_repr` | 0 | 0 | 0 | none |
| `mathlib4::MellinConvergent.cpow_smul` | 0 | 0 | 0 | none |
| `mathlib4::ContinuousMap.norm_smul_const` | 0 | 0 | 0 | none |
| `mathlib4::PMF.mem_support_seq_iff` | 0 | 0 | 0 | none |
| `mathlib4::NNReal.ENNReal.tendsto_nat_floor_div_atTop` | 0 | 0 | 0 | none |
| `mathlib4::rTensor.inverse_comp_rTensor` | 2 | 2 | 0 | `solve_by_elim_core` (3 facts, 0 simps) |
| `mathlib4::LinearEquiv.transvection.det_eq_one` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicGeometry.IsZariskiLocalAtTarget.IsZariskiLocalAtSource.AffineTargetMorphismProperty.IsStableUnderBaseChange.mk` | 0 | 0 | 0 | none |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | 2 | 2 | 0 | `solve_by_elim_core` (4 facts, 0 simps) |
| `mathlib4::Set.preimage_mul_preimage_subset` | 0 | 0 | 0 | none |
| `mathlib4::Real.NNReal.Real.rpow_add_rpow_le_add` | 0 | 0 | 0 | none |
| `mathlib4::mem_balancedCore_iff` | 0 | 0 | 0 | none |
| `mathlib4::HomotopicalAlgebra.PrepathObject.symm_p` | 0 | 0 | 0 | none |
| `mathlib4::tendsto_arithGeom_atTop_of_one_lt` | 0 | 0 | 0 | none |
| `mathlib4::Rat.intCast_div` | 0 | 0 | 0 | none |
| `mathlib4::Algebra.FormallySmooth.adjoin_of_algebraicIndependent` | 0 | 0 | 0 | none |
| `mathlib4::Algebra.FormallySmooth.exists_adicCompletionEvalOneₐ_comp_eq` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.restrict_apply₀'` | 0 | 0 | 0 | none |
| `mathlib4::Finset.subset_biUnion_of_mem` | 0 | 0 | 0 | none |
| `mathlib4::MulAction.IsPretransitive.t1Space_iff` | 0 | 0 | 0 | none |

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
| `mathlib4::Finset.Fin.prod_Iio_castSucc` | 33 | 19 | 14 |
| `mathlib4::Fintype.Finite.bddBelow_range` | 32 | 12 | 20 |
| `mathlib4::AlgebraicGeometry.Scheme.Pullback.Triplet.snd_SpecTensorTo_apply` | 32 | 22 | 10 |
| `mathlib4::AddCircle.MeasureTheory.fourierBasis_repr` | 32 | 32 | 0 |
| `mathlib4::MellinConvergent.cpow_smul` | 33 | 7 | 26 |
| `mathlib4::ContinuousMap.norm_smul_const` | 33 | 26 | 7 |
| `mathlib4::PMF.mem_support_seq_iff` | 32 | 17 | 15 |
| `mathlib4::NNReal.ENNReal.tendsto_nat_floor_div_atTop` | 32 | 26 | 6 |
| `mathlib4::rTensor.inverse_comp_rTensor` | 33 | 22 | 11 |
| `mathlib4::LinearEquiv.transvection.det_eq_one` | 32 | 32 | 0 |
| `mathlib4::AlgebraicGeometry.IsZariskiLocalAtTarget.IsZariskiLocalAtSource.AffineTargetMorphismProperty.IsStableUnderBaseChange.mk` | 32 | 16 | 16 |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | 33 | 13 | 20 |
| `mathlib4::Set.preimage_mul_preimage_subset` | 32 | 29 | 3 |
| `mathlib4::Real.NNReal.Real.rpow_add_rpow_le_add` | 32 | 26 | 6 |
| `mathlib4::mem_balancedCore_iff` | 32 | 10 | 22 |
| `mathlib4::HomotopicalAlgebra.PrepathObject.symm_p` | 32 | 6 | 26 |
| `mathlib4::tendsto_arithGeom_atTop_of_one_lt` | 33 | 23 | 10 |
| `mathlib4::Rat.intCast_div` | 34 | 18 | 16 |
| `mathlib4::Algebra.FormallySmooth.adjoin_of_algebraicIndependent` | 32 | 24 | 8 |
| `mathlib4::Algebra.FormallySmooth.exists_adicCompletionEvalOneₐ_comp_eq` | 32 | 21 | 11 |
| `mathlib4::MeasureTheory.Measure.restrict_apply₀'` | 34 | 11 | 23 |
| `mathlib4::Finset.subset_biUnion_of_mem` | 32 | 17 | 15 |
| `mathlib4::MulAction.IsPretransitive.t1Space_iff` | 32 | 17 | 15 |

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
