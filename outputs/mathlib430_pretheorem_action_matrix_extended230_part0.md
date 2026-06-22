# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_490.json`
- Replayable goals evaluated: 115
- Attempts: 1840
- Verified attempts: 122
- Non-empty-premise verified attempts: 105
- Goals with any proof: 28
- Goals with non-empty-premise proof: 28
- Action-dependent goals: 14

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 717 |
| `proved` | 122 |
| `rewrite_fail` | 4 |
| `search_fail` | 653 |
| `simp_fail` | 152 |
| `sorry_warning` | 108 |
| `timeout` | 54 |
| `typeclass_or_inference` | 6 |
| `unknown_identifier` | 24 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `aesop_core_plus_learned` | 17 | 17 | 115 |
| `aesop_core_plus_learned16` | 16 | 16 | 115 |
| `aesop_empty` | 14 | 0 | 115 |
| `hammerCore_core_plus_learned16` | 9 | 9 | 115 |
| `hammerCore_core_plus_learned32` | 9 | 9 | 115 |
| `hammer_core_plus_learned16` | 14 | 14 | 115 |
| `hammer_core_plus_learned32` | 14 | 14 | 115 |
| `linarith_empty` | 0 | 0 | 115 |
| `nlinarith_empty` | 0 | 0 | 115 |
| `norm_num_empty` | 3 | 0 | 115 |
| `omega_empty` | 0 | 0 | 115 |
| `ring_nf_empty` | 0 | 0 | 115 |
| `simp_all_core_plus_learned16` | 6 | 6 | 115 |
| `simp_all_core_plus_learned32` | 6 | 6 | 115 |
| `solve_by_elim_core_plus_learned16` | 7 | 7 | 115 |
| `solve_by_elim_core_plus_learned32` | 7 | 7 | 115 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 6 | 4 | 2 | `hammer_core_plus_learned16` (17 facts, 0 simps) |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 4 | 4 | 0 | `simp_all_core_plus_learned16` (0 facts, 6 simps) |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 4 | 3 | 1 | `hammer_core_plus_learned16` (8 facts, 0 simps) |
| `mathlib4::Set.Intersecting.insert` | 0 | 0 | 0 | none |
| `mathlib4::nhds_le_of_le` | 0 | 0 | 0 | none |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 0 | 0 | 0 | none |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 0 | 0 | 0 | none |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | 0 | 0 | 0 | none |
| `mathlib4::Sym.Sym2.card_image_diag` | 0 | 0 | 0 | none |
| `mathlib4::isChain_preimage_subtypeVal` | 0 | 0 | 0 | none |
| `mathlib4::IsLocalRing.Module.IsLocalRing.linearCombination_bijective_of_flat` | 0 | 0 | 0 | none |
| `mathlib4::Commute.isNilpotent_mul_left_iff` | 0 | 0 | 0 | none |
| `mathlib4::Algebra.Presentation.aeval_comp_val_eq` | 5 | 4 | 1 | `hammer_core_plus_learned16` (11 facts, 0 simps) |
| `mathlib4::Projectivization.logHeight_nonneg` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.Projective.nonsingular_some` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.injective_algebraMap_quotient_residueField` | 0 | 0 | 0 | none |
| `mathlib4::Nat.descPochhammer_pos` | 0 | 0 | 0 | none |
| `mathlib4::Rep.groupHomology.inhomogeneousChains.iCycles_mk` | 0 | 0 | 0 | none |
| `mathlib4::Stream'.Seq.length_map` | 0 | 0 | 0 | none |
| `mathlib4::Units.inv_mul_cancel_left` | 2 | 2 | 0 | `hammerCore_core_plus_learned16` (7 facts, 5 simps) |
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
| `mathlib4::PMF.mem_support_seq_iff` | 4 | 2 | 2 | `hammer_core_plus_learned16` (15 facts, 0 simps) |
| `mathlib4::NNReal.ENNReal.tendsto_nat_floor_div_atTop` | 0 | 0 | 0 | none |
| `mathlib4::rTensor.inverse_comp_rTensor` | 2 | 2 | 0 | `solve_by_elim_core_plus_learned16` (15 facts, 0 simps) |
| `mathlib4::LinearEquiv.transvection.det_eq_one` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicGeometry.IsZariskiLocalAtTarget.IsZariskiLocalAtSource.AffineTargetMorphismProperty.IsStableUnderBaseChange.mk` | 0 | 0 | 0 | none |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | 2 | 2 | 0 | `solve_by_elim_core_plus_learned16` (10 facts, 0 simps) |
| `mathlib4::Set.preimage_mul_preimage_subset` | 0 | 0 | 0 | none |
| `mathlib4::Real.NNReal.Real.rpow_add_rpow_le_add` | 0 | 0 | 0 | none |
| `mathlib4::mem_balancedCore_iff` | 2 | 2 | 0 | `aesop_core_plus_learned` (8 facts, 7 simps) |
| `mathlib4::HomotopicalAlgebra.PrepathObject.symm_p` | 3 | 2 | 1 | `hammer_core_plus_learned16` (3 facts, 0 simps) |
| `mathlib4::tendsto_arithGeom_atTop_of_one_lt` | 0 | 0 | 0 | none |
| `mathlib4::Rat.intCast_div` | 0 | 0 | 0 | none |
| `mathlib4::Algebra.FormallySmooth.adjoin_of_algebraicIndependent` | 0 | 0 | 0 | none |
| `mathlib4::Algebra.FormallySmooth.exists_adicCompletionEvalOneₐ_comp_eq` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.restrict_apply₀'` | 0 | 0 | 0 | none |
| `mathlib4::Finset.subset_biUnion_of_mem` | 0 | 0 | 0 | none |
| `mathlib4::MulAction.IsPretransitive.t1Space_iff` | 0 | 0 | 0 | none |
| `mathlib4::AnalyticWithinAt.congr_of_eventuallyEq` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.cyclotomic_prime_mul_X_sub_one` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.contentIdeal_le_span_content` | 0 | 0 | 0 | none |
| `mathlib4::uniformEquicontinuousOn_finite` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.Ideal.FractionalIdeal.count_coe` | 0 | 0 | 0 | none |
| `mathlib4::Set.mem_pow` | 0 | 0 | 0 | none |
| `mathlib4::DifferentiableWithinAt.hasGradientWithinAt` | 0 | 0 | 0 | none |
| `mathlib4::Seminorm.ball_sup` | 5 | 4 | 1 | `hammer_core_plus_learned16` (19 facts, 0 simps) |
| `mathlib4::Submodule.Quotient.LinearMap.range_eq_top_of_cancel` | 0 | 0 | 0 | none |
| `mathlib4::cfcₙHom_of_cfcHom_map_quasispectrum` | 0 | 0 | 0 | none |
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.tag_biUnionTagged` | 0 | 0 | 0 | none |
| `mathlib4::TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.card` | 0 | 0 | 0 | none |
| `mathlib4::DiscreteUniformity.eq_pure_of_cauchy` | 0 | 0 | 0 | none |
| `mathlib4::LightCondensed.internallyProjective_iff_tensor_condition` | 0 | 0 | 0 | none |
| `mathlib4::NumberField.mixedEmbedding.logMap_real` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.AEEqFun.compQuasiMeasurePreserving_toGerm` | 0 | 0 | 0 | none |
| `mathlib4::Matrix.vecMulLinear_transpose` | 0 | 0 | 0 | none |
| `mathlib4::dist_eq_norm_inv_mul'` | 2 | 2 | 0 | `hammerCore_core_plus_learned16` (2 facts, 2 simps) |
| `mathlib4::HomologicalComplex.truncGE'.restrictionToTruncGE'.restrictionToTruncGE'_f_eq_iso_hom_iso_inv` | 0 | 0 | 0 | none |
| `mathlib4::Path.map_coe` | 11 | 10 | 1 | `hammer_core_plus_learned16` (13 facts, 0 simps) |
| `mathlib4::Cardinal.continuum_lt_lift` | 0 | 0 | 0 | none |
| `mathlib4::Module.End.invtSubmodule_smul` | 0 | 0 | 0 | none |
| `mathlib4::MonomialOrder.leadingTerm_zero` | 6 | 4 | 2 | `hammer_core_plus_learned16` (18 facts, 0 simps) |
| `mathlib4::LSeries.abscissaOfAbsConv_binop_le` | 0 | 0 | 0 | none |
| `mathlib4::AddHom.AddMonoidHom.AddMonoid.End.noZeroDivisors_iff_isDomain_or_subsingleton` | 0 | 0 | 0 | none |
| `mathlib4::ConjRootClass.carrier_zero` | 3 | 2 | 1 | `hammer_core_plus_learned16` (14 facts, 0 simps) |
| `mathlib4::MeasurableSpace.isPiSystem_image_Iic` | 0 | 0 | 0 | none |
| `mathlib4::Rat.Nat.dist_cast_rat` | 9 | 8 | 1 | `hammer_core_plus_learned16` (11 facts, 0 simps) |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | 2 | 2 | 0 | `hammerCore_core_plus_learned16` (14 facts, 11 simps) |
| `mathlib4::Con.smul` | 0 | 0 | 0 | none |
| `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply` | 2 | 2 | 0 | `aesop_core_plus_learned` (12 facts, 8 simps) |
| `mathlib4::Equiv.Perm.isConj_of_support_equiv` | 0 | 0 | 0 | none |
| `mathlib4::Finsupp.linearCombination_fin_zero` | 0 | 0 | 0 | none |
| `mathlib4::AbsoluteValue.map_units_int_smul` | 0 | 0 | 0 | none |
| `mathlib4::EuclideanGeometry.Sphere.dist_orthogonalProjection_eq_radius_iff_isTangentAt` | 0 | 0 | 0 | none |
| `mathlib4::Set.not_countable_univ_iff` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.localized₀_smul` | 0 | 0 | 0 | none |
| `mathlib4::Filter.EventuallyLE.cardinal_bUnion` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms` | 2 | 2 | 0 | `aesop_core_plus_learned` (13 facts, 9 simps) |
| `mathlib4::SimpleGraph.isExtremal_free_iff` | 0 | 0 | 0 | none |
| `mathlib4::ContinuousLinearMap.MeasureTheory.Lp.smul_zero` | 0 | 0 | 0 | none |
| `mathlib4::ProbabilityTheory.Kernel.isProper_iff_restrict_eq_indicator_smul` | 0 | 0 | 0 | none |
| `mathlib4::Units.map_neg_one` | 5 | 4 | 1 | `hammer_core_plus_learned16` (13 facts, 0 simps) |
| `mathlib4::List.permutationsAux2_append` | 0 | 0 | 0 | none |
| `mathlib4::Finset.insert_inter` | 5 | 4 | 1 | `hammer_core_plus_learned16` (10 facts, 0 simps) |
| `mathlib4::Stirling.stirlingSeq_one` | 4 | 4 | 0 | `hammerCore_core_plus_learned16` (9 facts, 9 simps) |
| `mathlib4::MeasureTheory.MeasurePreserving.withDensity_rnDeriv` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.ofList_cons_smul` | 0 | 0 | 0 | none |
| `mathlib4::Finsupp.card_Iio` | 6 | 6 | 0 | `simp_all_core_plus_learned16` (0 facts, 8 simps) |
| `mathlib4::Filter.IsBasis.FilterBasis.Filter.IsBasis.HasBasis.tendsto_left_iff` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.span_pair_abs` | 6 | 6 | 0 | `simp_all_core_plus_learned16` (0 facts, 8 simps) |
| `mathlib4::CompleteLattice.Directed.disjoint_iSup_right` | 0 | 0 | 0 | none |
| `mathlib4::IsOfFinOrder.orderOf_pow` | 0 | 0 | 0 | none |
| `mathlib4::Option.Finset.mem_eraseNone` | 0 | 0 | 0 | none |
| `mathlib4::Nat.Prime.factorization_pow` | 3 | 2 | 1 | `hammer_core_plus_learned16` (19 facts, 0 simps) |
| `mathlib4::Path.refl_reparam` | 7 | 6 | 1 | `hammer_core_plus_learned16` (11 facts, 0 simps) |
| `mathlib4::Module.support_of_noZeroSMulDivisors` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.OuterMeasure.restrict_sInf_eq_sInf_restrict` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.Module.Finite.Submodule.FG.restrictScalars` | 0 | 0 | 0 | none |
| `mathlib4::Finset.sup'_product_right` | 0 | 0 | 0 | none |
| `mathlib4::intervalIntegral.integral_deriv_mul_eq_sub_of_hasDeriv_right` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.twoTorsionPolynomial_discr_of_char_two` | 0 | 0 | 0 | none |
| `mathlib4::NumberField.rootDiscr_def` | 8 | 8 | 0 | `simp_all_core_plus_learned16` (0 facts, 12 simps) |
| `mathlib4::mem_rootsOfUnity_prime_pow_mul_iff` | 0 | 0 | 0 | none |
| `mathlib4::TensorProduct.map_add_right` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.MonoidalCategory.Limits.HasColimit.isoOfNatIso_ι_hom_whiskerRight` | 0 | 0 | 0 | none |
| `mathlib4::ENNReal.mul_div_right_comm` | 2 | 2 | 0 | `solve_by_elim_core_plus_learned16` (15 facts, 0 simps) |

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
| `mathlib4::AnalyticWithinAt.congr_of_eventuallyEq` | 32 | 16 | 16 |
| `mathlib4::Polynomial.cyclotomic_prime_mul_X_sub_one` | 32 | 23 | 9 |
| `mathlib4::Polynomial.contentIdeal_le_span_content` | 34 | 25 | 9 |
| `mathlib4::uniformEquicontinuousOn_finite` | 32 | 20 | 12 |
| `mathlib4::Ideal.Ideal.FractionalIdeal.count_coe` | 34 | 27 | 7 |
| `mathlib4::Set.mem_pow` | 33 | 17 | 16 |
| `mathlib4::DifferentiableWithinAt.hasGradientWithinAt` | 33 | 15 | 18 |
| `mathlib4::Seminorm.ball_sup` | 34 | 22 | 12 |
| `mathlib4::Submodule.Quotient.LinearMap.range_eq_top_of_cancel` | 32 | 7 | 25 |
| `mathlib4::cfcₙHom_of_cfcHom_map_quasispectrum` | 33 | 30 | 3 |
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.tag_biUnionTagged` | 32 | 18 | 14 |
| `mathlib4::TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.card` | 32 | 18 | 14 |
| `mathlib4::DiscreteUniformity.eq_pure_of_cauchy` | 34 | 20 | 14 |
| `mathlib4::LightCondensed.internallyProjective_iff_tensor_condition` | 34 | 34 | 0 |
| `mathlib4::NumberField.mixedEmbedding.logMap_real` | 33 | 17 | 16 |
| `mathlib4::MeasureTheory.AEEqFun.compQuasiMeasurePreserving_toGerm` | 32 | 16 | 16 |
| `mathlib4::Matrix.vecMulLinear_transpose` | 32 | 11 | 21 |
| `mathlib4::dist_eq_norm_inv_mul'` | 32 | 2 | 30 |
| `mathlib4::HomologicalComplex.truncGE'.restrictionToTruncGE'.restrictionToTruncGE'_f_eq_iso_hom_iso_inv` | 32 | 8 | 24 |
| `mathlib4::Path.map_coe` | 32 | 21 | 11 |
| `mathlib4::Cardinal.continuum_lt_lift` | 33 | 9 | 24 |
| `mathlib4::Module.End.invtSubmodule_smul` | 34 | 6 | 28 |
| `mathlib4::MonomialOrder.leadingTerm_zero` | 33 | 26 | 7 |
| `mathlib4::LSeries.abscissaOfAbsConv_binop_le` | 33 | 26 | 7 |
| `mathlib4::AddHom.AddMonoidHom.AddMonoid.End.noZeroDivisors_iff_isDomain_or_subsingleton` | 32 | 7 | 25 |
| `mathlib4::ConjRootClass.carrier_zero` | 33 | 16 | 17 |
| `mathlib4::MeasurableSpace.isPiSystem_image_Iic` | 32 | 10 | 22 |
| `mathlib4::Rat.Nat.dist_cast_rat` | 32 | 15 | 17 |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | 32 | 18 | 14 |
| `mathlib4::Con.smul` | 32 | 27 | 5 |
| `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply` | 32 | 21 | 11 |
| `mathlib4::Equiv.Perm.isConj_of_support_equiv` | 32 | 19 | 13 |
| `mathlib4::Finsupp.linearCombination_fin_zero` | 32 | 13 | 19 |
| `mathlib4::AbsoluteValue.map_units_int_smul` | 33 | 13 | 20 |
| `mathlib4::EuclideanGeometry.Sphere.dist_orthogonalProjection_eq_radius_iff_isTangentAt` | 34 | 21 | 13 |
| `mathlib4::Set.not_countable_univ_iff` | 33 | 19 | 14 |
| `mathlib4::Submodule.localized₀_smul` | 32 | 18 | 14 |
| `mathlib4::Filter.EventuallyLE.cardinal_bUnion` | 33 | 15 | 18 |
| `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms` | 32 | 22 | 10 |
| `mathlib4::SimpleGraph.isExtremal_free_iff` | 32 | 32 | 0 |
| `mathlib4::ContinuousLinearMap.MeasureTheory.Lp.smul_zero` | 35 | 28 | 7 |
| `mathlib4::ProbabilityTheory.Kernel.isProper_iff_restrict_eq_indicator_smul` | 32 | 4 | 28 |
| `mathlib4::Units.map_neg_one` | 32 | 13 | 19 |
| `mathlib4::List.permutationsAux2_append` | 32 | 6 | 26 |
| `mathlib4::Finset.insert_inter` | 32 | 14 | 18 |
| `mathlib4::Stirling.stirlingSeq_one` | 32 | 9 | 23 |
| `mathlib4::MeasureTheory.MeasurePreserving.withDensity_rnDeriv` | 33 | 28 | 5 |
| `mathlib4::Ideal.ofList_cons_smul` | 33 | 17 | 16 |
| `mathlib4::Finsupp.card_Iio` | 32 | 19 | 13 |
| `mathlib4::Filter.IsBasis.FilterBasis.Filter.IsBasis.HasBasis.tendsto_left_iff` | 32 | 3 | 29 |
| `mathlib4::Ideal.span_pair_abs` | 33 | 18 | 15 |
| `mathlib4::CompleteLattice.Directed.disjoint_iSup_right` | 32 | 24 | 8 |
| `mathlib4::IsOfFinOrder.orderOf_pow` | 32 | 17 | 15 |
| `mathlib4::Option.Finset.mem_eraseNone` | 32 | 22 | 10 |
| `mathlib4::Nat.Prime.factorization_pow` | 32 | 22 | 10 |
| `mathlib4::Path.refl_reparam` | 32 | 25 | 7 |
| `mathlib4::Module.support_of_noZeroSMulDivisors` | 32 | 22 | 10 |
| `mathlib4::MeasureTheory.OuterMeasure.restrict_sInf_eq_sInf_restrict` | 33 | 26 | 7 |
| `mathlib4::Submodule.Module.Finite.Submodule.FG.restrictScalars` | 32 | 23 | 9 |
| `mathlib4::Finset.sup'_product_right` | 34 | 24 | 10 |
| `mathlib4::intervalIntegral.integral_deriv_mul_eq_sub_of_hasDeriv_right` | 32 | 8 | 24 |
| `mathlib4::WeierstrassCurve.twoTorsionPolynomial_discr_of_char_two` | 32 | 13 | 19 |
| `mathlib4::NumberField.rootDiscr_def` | 32 | 17 | 15 |
| `mathlib4::mem_rootsOfUnity_prime_pow_mul_iff` | 33 | 22 | 11 |
| `mathlib4::TensorProduct.map_add_right` | 32 | 10 | 22 |
| `mathlib4::CategoryTheory.MonoidalCategory.Limits.HasColimit.isoOfNatIso_ι_hom_whiskerRight` | 32 | 6 | 26 |
| `mathlib4::ENNReal.mul_div_right_comm` | 32 | 15 | 17 |

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
