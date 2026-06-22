# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_490.json`
- Pool mode: `strict_aesop`
- Result action suffix: `_filtered`
- Replayable goals evaluated: 115
- Attempts: 575
- Verified attempts: 4
- Non-empty-premise verified attempts: 4
- Goals with any proof: 2
- Goals with non-empty-premise proof: 2
- Action-dependent goals: 2

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 545 |
| `proved` | 4 |
| `rewrite_fail` | 1 |
| `search_fail` | 7 |
| `simp_fail` | 4 |
| `sorry_warning` | 14 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `aesop_core_plus_learned16_filtered` | 1 | 1 | 115 |
| `aesop_core_plus_learned_filtered` | 1 | 1 | 115 |
| `hammerCore_core_plus_learned_filtered` | 1 | 1 | 115 |
| `hammer_core_plus_learned16_filtered` | 1 | 1 | 115 |
| `solve_by_elim_core_filtered` | 0 | 0 | 115 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 0 | 0 | 0 | none |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 0 | 0 | 0 | none |
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
| `mathlib4::Units.inv_mul_cancel_left` | 1 | 1 | 0 | `hammerCore_core_plus_learned_filtered` (7 facts, 3 simps) |
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
| `mathlib4::rTensor.inverse_comp_rTensor` | 0 | 0 | 0 | none |
| `mathlib4::LinearEquiv.transvection.det_eq_one` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicGeometry.IsZariskiLocalAtTarget.IsZariskiLocalAtSource.AffineTargetMorphismProperty.IsStableUnderBaseChange.mk` | 0 | 0 | 0 | none |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | 0 | 0 | 0 | none |
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
| `mathlib4::AnalyticWithinAt.congr_of_eventuallyEq` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.cyclotomic_prime_mul_X_sub_one` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.contentIdeal_le_span_content` | 0 | 0 | 0 | none |
| `mathlib4::uniformEquicontinuousOn_finite` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.Ideal.FractionalIdeal.count_coe` | 0 | 0 | 0 | none |
| `mathlib4::Set.mem_pow` | 0 | 0 | 0 | none |
| `mathlib4::DifferentiableWithinAt.hasGradientWithinAt` | 0 | 0 | 0 | none |
| `mathlib4::Seminorm.ball_sup` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.Quotient.LinearMap.range_eq_top_of_cancel` | 0 | 0 | 0 | none |
| `mathlib4::cfcₙHom_of_cfcHom_map_quasispectrum` | 0 | 0 | 0 | none |
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.tag_biUnionTagged` | 0 | 0 | 0 | none |
| `mathlib4::TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.card` | 0 | 0 | 0 | none |
| `mathlib4::DiscreteUniformity.eq_pure_of_cauchy` | 0 | 0 | 0 | none |
| `mathlib4::LightCondensed.internallyProjective_iff_tensor_condition` | 0 | 0 | 0 | none |
| `mathlib4::NumberField.mixedEmbedding.logMap_real` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.AEEqFun.compQuasiMeasurePreserving_toGerm` | 0 | 0 | 0 | none |
| `mathlib4::Matrix.vecMulLinear_transpose` | 0 | 0 | 0 | none |
| `mathlib4::dist_eq_norm_inv_mul'` | 0 | 0 | 0 | none |
| `mathlib4::HomologicalComplex.truncGE'.restrictionToTruncGE'.restrictionToTruncGE'_f_eq_iso_hom_iso_inv` | 0 | 0 | 0 | none |
| `mathlib4::Path.map_coe` | 0 | 0 | 0 | none |
| `mathlib4::Cardinal.continuum_lt_lift` | 0 | 0 | 0 | none |
| `mathlib4::Module.End.invtSubmodule_smul` | 0 | 0 | 0 | none |
| `mathlib4::MonomialOrder.leadingTerm_zero` | 0 | 0 | 0 | none |
| `mathlib4::LSeries.abscissaOfAbsConv_binop_le` | 0 | 0 | 0 | none |
| `mathlib4::AddHom.AddMonoidHom.AddMonoid.End.noZeroDivisors_iff_isDomain_or_subsingleton` | 0 | 0 | 0 | none |
| `mathlib4::ConjRootClass.carrier_zero` | 0 | 0 | 0 | none |
| `mathlib4::MeasurableSpace.isPiSystem_image_Iic` | 0 | 0 | 0 | none |
| `mathlib4::Rat.Nat.dist_cast_rat` | 0 | 0 | 0 | none |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | 0 | 0 | 0 | none |
| `mathlib4::Con.smul` | 0 | 0 | 0 | none |
| `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply` | 0 | 0 | 0 | none |
| `mathlib4::Equiv.Perm.isConj_of_support_equiv` | 0 | 0 | 0 | none |
| `mathlib4::Finsupp.linearCombination_fin_zero` | 0 | 0 | 0 | none |
| `mathlib4::AbsoluteValue.map_units_int_smul` | 0 | 0 | 0 | none |
| `mathlib4::EuclideanGeometry.Sphere.dist_orthogonalProjection_eq_radius_iff_isTangentAt` | 0 | 0 | 0 | none |
| `mathlib4::Set.not_countable_univ_iff` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.localized₀_smul` | 0 | 0 | 0 | none |
| `mathlib4::Filter.EventuallyLE.cardinal_bUnion` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms` | 0 | 0 | 0 | none |
| `mathlib4::SimpleGraph.isExtremal_free_iff` | 0 | 0 | 0 | none |
| `mathlib4::ContinuousLinearMap.MeasureTheory.Lp.smul_zero` | 0 | 0 | 0 | none |
| `mathlib4::ProbabilityTheory.Kernel.isProper_iff_restrict_eq_indicator_smul` | 0 | 0 | 0 | none |
| `mathlib4::Units.map_neg_one` | 3 | 3 | 0 | `hammer_core_plus_learned16_filtered` (13 facts, 0 simps) |
| `mathlib4::List.permutationsAux2_append` | 0 | 0 | 0 | none |
| `mathlib4::Finset.insert_inter` | 0 | 0 | 0 | none |
| `mathlib4::Stirling.stirlingSeq_one` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.MeasurePreserving.withDensity_rnDeriv` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.ofList_cons_smul` | 0 | 0 | 0 | none |
| `mathlib4::Finsupp.card_Iio` | 0 | 0 | 0 | none |
| `mathlib4::Filter.IsBasis.FilterBasis.Filter.IsBasis.HasBasis.tendsto_left_iff` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.span_pair_abs` | 0 | 0 | 0 | none |
| `mathlib4::CompleteLattice.Directed.disjoint_iSup_right` | 0 | 0 | 0 | none |
| `mathlib4::IsOfFinOrder.orderOf_pow` | 0 | 0 | 0 | none |
| `mathlib4::Option.Finset.mem_eraseNone` | 0 | 0 | 0 | none |
| `mathlib4::Nat.Prime.factorization_pow` | 0 | 0 | 0 | none |
| `mathlib4::Path.refl_reparam` | 0 | 0 | 0 | none |
| `mathlib4::Module.support_of_noZeroSMulDivisors` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.OuterMeasure.restrict_sInf_eq_sInf_restrict` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.Module.Finite.Submodule.FG.restrictScalars` | 0 | 0 | 0 | none |
| `mathlib4::Finset.sup'_product_right` | 0 | 0 | 0 | none |
| `mathlib4::intervalIntegral.integral_deriv_mul_eq_sub_of_hasDeriv_right` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.twoTorsionPolynomial_discr_of_char_two` | 0 | 0 | 0 | none |
| `mathlib4::NumberField.rootDiscr_def` | 0 | 0 | 0 | none |
| `mathlib4::mem_rootsOfUnity_prime_pow_mul_iff` | 0 | 0 | 0 | none |
| `mathlib4::TensorProduct.map_add_right` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.MonoidalCategory.Limits.HasColimit.isoOfNatIso_ι_hom_whiskerRight` | 0 | 0 | 0 | none |
| `mathlib4::ENNReal.mul_div_right_comm` | 0 | 0 | 0 | none |

## Availability

| Goal | Checked | Available | Failed | Target/alias | Aesop-safe available | Aesop-unsafe available | Simp-safe available | Simp-unsafe available |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mathlib4::Module.rank_tensorProduct'` | 32 | 32 | 0 | 0 | 29 | 3 | 10 | 22 |
| `mathlib4::FirstOrder.Language.definableFun_const` | 33 | 33 | 0 | 0 | 14 | 19 | 6 | 27 |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 32 | 32 | 0 | 0 | 28 | 4 | 10 | 22 |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 32 | 32 | 0 | 0 | 7 | 25 | 16 | 16 |
| `mathlib4::Set.Intersecting.insert` | 32 | 32 | 0 | 0 | 26 | 6 | 7 | 25 |
| `mathlib4::nhds_le_of_le` | 32 | 32 | 0 | 0 | 31 | 1 | 9 | 23 |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 34 | 34 | 0 | 0 | 18 | 16 | 8 | 26 |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 32 | 32 | 0 | 0 | 21 | 11 | 9 | 23 |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | 32 | 32 | 0 | 0 | 29 | 3 | 8 | 24 |
| `mathlib4::Sym.Sym2.card_image_diag` | 32 | 32 | 0 | 0 | 23 | 9 | 14 | 18 |
| `mathlib4::isChain_preimage_subtypeVal` | 32 | 11 | 21 | 0 | 6 | 5 | 3 | 8 |
| `mathlib4::IsLocalRing.Module.IsLocalRing.linearCombination_bijective_of_flat` | 32 | 32 | 0 | 0 | 25 | 7 | 3 | 29 |
| `mathlib4::Commute.isNilpotent_mul_left_iff` | 33 | 33 | 0 | 0 | 28 | 5 | 6 | 27 |
| `mathlib4::Algebra.Presentation.aeval_comp_val_eq` | 32 | 32 | 0 | 0 | 13 | 19 | 13 | 19 |
| `mathlib4::Projectivization.logHeight_nonneg` | 34 | 34 | 0 | 0 | 26 | 8 | 2 | 32 |
| `mathlib4::WeierstrassCurve.Projective.nonsingular_some` | 37 | 37 | 0 | 0 | 5 | 32 | 2 | 35 |
| `mathlib4::Ideal.injective_algebraMap_quotient_residueField` | 32 | 32 | 0 | 0 | 15 | 17 | 3 | 29 |
| `mathlib4::Nat.descPochhammer_pos` | 33 | 33 | 0 | 0 | 25 | 8 | 10 | 23 |
| `mathlib4::Rep.groupHomology.inhomogeneousChains.iCycles_mk` | 33 | 33 | 0 | 0 | 6 | 27 | 10 | 23 |
| `mathlib4::Stream'.Seq.length_map` | 33 | 33 | 0 | 0 | 11 | 22 | 8 | 25 |
| `mathlib4::Units.inv_mul_cancel_left` | 33 | 8 | 25 | 0 | 6 | 2 | 3 | 5 |
| `mathlib4::CochainComplex.HomComplex.Cochain.rightUnshift_add` | 33 | 33 | 0 | 0 | 3 | 30 | 12 | 21 |
| `mathlib4::CompleteLattice.IsCompactElement.directed_sSup_lt_of_lt` | 32 | 32 | 0 | 0 | 21 | 11 | 2 | 30 |
| `mathlib4::SimpleGraph.Iso.edgeFinset_map` | 32 | 32 | 0 | 0 | 15 | 17 | 8 | 24 |
| `mathlib4::Finset.map_add_right_Ioc` | 32 | 32 | 0 | 0 | 24 | 8 | 15 | 17 |
| `mathlib4::Finset.Fin.prod_Iio_castSucc` | 33 | 33 | 0 | 0 | 28 | 5 | 16 | 17 |
| `mathlib4::Fintype.Finite.bddBelow_range` | 32 | 32 | 0 | 0 | 19 | 13 | 1 | 31 |
| `mathlib4::AlgebraicGeometry.Scheme.Pullback.Triplet.snd_SpecTensorTo_apply` | 32 | 32 | 0 | 0 | 0 | 32 | 7 | 25 |
| `mathlib4::AddCircle.MeasureTheory.fourierBasis_repr` | 32 | 32 | 0 | 0 | 19 | 13 | 5 | 27 |
| `mathlib4::MellinConvergent.cpow_smul` | 33 | 33 | 0 | 0 | 27 | 6 | 3 | 30 |
| `mathlib4::ContinuousMap.norm_smul_const` | 33 | 33 | 0 | 0 | 6 | 27 | 7 | 26 |
| `mathlib4::PMF.mem_support_seq_iff` | 32 | 32 | 0 | 0 | 23 | 9 | 11 | 21 |
| `mathlib4::NNReal.ENNReal.tendsto_nat_floor_div_atTop` | 32 | 32 | 0 | 0 | 28 | 4 | 2 | 30 |
| `mathlib4::rTensor.inverse_comp_rTensor` | 33 | 33 | 0 | 0 | 18 | 15 | 2 | 31 |
| `mathlib4::LinearEquiv.transvection.det_eq_one` | 32 | 32 | 0 | 1 | 21 | 11 | 12 | 20 |
| `mathlib4::AlgebraicGeometry.IsZariskiLocalAtTarget.IsZariskiLocalAtSource.AffineTargetMorphismProperty.IsStableUnderBaseChange.mk` | 32 | 32 | 0 | 1 | 12 | 20 | 7 | 25 |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | 33 | 33 | 0 | 1 | 9 | 24 | 11 | 22 |
| `mathlib4::Set.preimage_mul_preimage_subset` | 32 | 29 | 3 | 0 | 26 | 3 | 13 | 16 |
| `mathlib4::Real.NNReal.Real.rpow_add_rpow_le_add` | 32 | 32 | 0 | 0 | 30 | 2 | 3 | 29 |
| `mathlib4::mem_balancedCore_iff` | 32 | 32 | 0 | 0 | 28 | 4 | 5 | 27 |
| `mathlib4::HomotopicalAlgebra.PrepathObject.symm_p` | 32 | 32 | 0 | 1 | 4 | 28 | 7 | 25 |
| `mathlib4::tendsto_arithGeom_atTop_of_one_lt` | 33 | 33 | 0 | 0 | 28 | 5 | 1 | 32 |
| `mathlib4::Rat.intCast_div` | 34 | 34 | 0 | 0 | 26 | 8 | 11 | 23 |
| `mathlib4::Algebra.FormallySmooth.adjoin_of_algebraicIndependent` | 32 | 32 | 0 | 0 | 21 | 11 | 3 | 29 |
| `mathlib4::Algebra.FormallySmooth.exists_adicCompletionEvalOneₐ_comp_eq` | 32 | 32 | 0 | 0 | 21 | 11 | 10 | 22 |
| `mathlib4::MeasureTheory.Measure.restrict_apply₀'` | 34 | 34 | 0 | 0 | 29 | 5 | 6 | 28 |
| `mathlib4::Finset.subset_biUnion_of_mem` | 32 | 32 | 0 | 1 | 28 | 4 | 10 | 22 |
| `mathlib4::MulAction.IsPretransitive.t1Space_iff` | 32 | 32 | 0 | 0 | 19 | 13 | 5 | 27 |
| `mathlib4::AnalyticWithinAt.congr_of_eventuallyEq` | 32 | 32 | 0 | 0 | 26 | 6 | 5 | 27 |
| `mathlib4::Polynomial.cyclotomic_prime_mul_X_sub_one` | 32 | 32 | 0 | 0 | 26 | 6 | 11 | 21 |
| `mathlib4::Polynomial.contentIdeal_le_span_content` | 34 | 34 | 0 | 0 | 22 | 12 | 11 | 23 |
| `mathlib4::uniformEquicontinuousOn_finite` | 32 | 32 | 0 | 0 | 18 | 14 | 4 | 28 |
| `mathlib4::Ideal.Ideal.FractionalIdeal.count_coe` | 34 | 34 | 0 | 0 | 20 | 14 | 16 | 18 |
| `mathlib4::Set.mem_pow` | 33 | 33 | 0 | 0 | 26 | 7 | 7 | 26 |
| `mathlib4::DifferentiableWithinAt.hasGradientWithinAt` | 33 | 33 | 0 | 0 | 22 | 11 | 8 | 25 |
| `mathlib4::Seminorm.ball_sup` | 34 | 34 | 0 | 0 | 26 | 8 | 10 | 24 |
| `mathlib4::Submodule.Quotient.LinearMap.range_eq_top_of_cancel` | 32 | 32 | 0 | 1 | 21 | 11 | 12 | 20 |
| `mathlib4::cfcₙHom_of_cfcHom_map_quasispectrum` | 33 | 33 | 0 | 0 | 23 | 10 | 7 | 26 |
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.tag_biUnionTagged` | 32 | 32 | 0 | 0 | 12 | 20 | 12 | 20 |
| `mathlib4::TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.WittVector.TruncatedWittVector.card` | 32 | 32 | 0 | 1 | 5 | 27 | 3 | 29 |
| `mathlib4::DiscreteUniformity.eq_pure_of_cauchy` | 34 | 34 | 0 | 0 | 26 | 8 | 5 | 29 |
| `mathlib4::LightCondensed.internallyProjective_iff_tensor_condition` | 34 | 34 | 0 | 0 | 5 | 29 | 5 | 29 |
| `mathlib4::NumberField.mixedEmbedding.logMap_real` | 33 | 33 | 0 | 0 | 9 | 24 | 9 | 24 |
| `mathlib4::MeasureTheory.AEEqFun.compQuasiMeasurePreserving_toGerm` | 32 | 32 | 0 | 0 | 18 | 14 | 7 | 25 |
| `mathlib4::Matrix.vecMulLinear_transpose` | 32 | 32 | 0 | 0 | 17 | 15 | 15 | 17 |
| `mathlib4::dist_eq_norm_inv_mul'` | 32 | 32 | 0 | 0 | 32 | 0 | 7 | 25 |
| `mathlib4::HomologicalComplex.truncGE'.restrictionToTruncGE'.restrictionToTruncGE'_f_eq_iso_hom_iso_inv` | 32 | 32 | 0 | 0 | 2 | 30 | 4 | 28 |
| `mathlib4::Path.map_coe` | 32 | 32 | 0 | 0 | 16 | 16 | 15 | 17 |
| `mathlib4::Cardinal.continuum_lt_lift` | 33 | 33 | 0 | 0 | 28 | 5 | 22 | 11 |
| `mathlib4::Module.End.invtSubmodule_smul` | 34 | 34 | 0 | 0 | 19 | 15 | 9 | 25 |
| `mathlib4::MonomialOrder.leadingTerm_zero` | 33 | 33 | 0 | 0 | 24 | 9 | 16 | 17 |
| `mathlib4::LSeries.abscissaOfAbsConv_binop_le` | 33 | 33 | 0 | 0 | 30 | 3 | 2 | 31 |
| `mathlib4::AddHom.AddMonoidHom.AddMonoid.End.noZeroDivisors_iff_isDomain_or_subsingleton` | 32 | 7 | 25 | 0 | 2 | 5 | 2 | 5 |
| `mathlib4::ConjRootClass.carrier_zero` | 33 | 33 | 0 | 0 | 27 | 6 | 11 | 22 |
| `mathlib4::MeasurableSpace.isPiSystem_image_Iic` | 32 | 32 | 0 | 0 | 24 | 8 | 11 | 21 |
| `mathlib4::Rat.Nat.dist_cast_rat` | 32 | 32 | 0 | 0 | 28 | 4 | 11 | 21 |
| `mathlib4::Equiv.Perm.swap_isSwap_iff` | 32 | 32 | 0 | 0 | 23 | 9 | 14 | 18 |
| `mathlib4::Con.smul` | 32 | 27 | 5 | 0 | 13 | 14 | 7 | 20 |
| `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply` | 32 | 32 | 0 | 0 | 25 | 7 | 7 | 25 |
| `mathlib4::Equiv.Perm.isConj_of_support_equiv` | 32 | 32 | 0 | 0 | 28 | 4 | 11 | 21 |
| `mathlib4::Finsupp.linearCombination_fin_zero` | 32 | 32 | 0 | 0 | 21 | 11 | 22 | 10 |
| `mathlib4::AbsoluteValue.map_units_int_smul` | 33 | 33 | 0 | 0 | 21 | 12 | 13 | 20 |
| `mathlib4::EuclideanGeometry.Sphere.dist_orthogonalProjection_eq_radius_iff_isTangentAt` | 34 | 34 | 0 | 0 | 18 | 16 | 5 | 29 |
| `mathlib4::Set.not_countable_univ_iff` | 33 | 33 | 0 | 0 | 27 | 6 | 6 | 27 |
| `mathlib4::Submodule.localized₀_smul` | 32 | 32 | 0 | 0 | 17 | 15 | 7 | 25 |
| `mathlib4::Filter.EventuallyLE.cardinal_bUnion` | 33 | 33 | 0 | 0 | 25 | 8 | 2 | 31 |
| `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms` | 32 | 32 | 0 | 0 | 18 | 14 | 1 | 31 |
| `mathlib4::SimpleGraph.isExtremal_free_iff` | 32 | 32 | 0 | 0 | 29 | 3 | 7 | 25 |
| `mathlib4::ContinuousLinearMap.MeasureTheory.Lp.smul_zero` | 35 | 35 | 0 | 0 | 24 | 11 | 15 | 20 |
| `mathlib4::ProbabilityTheory.Kernel.isProper_iff_restrict_eq_indicator_smul` | 32 | 32 | 0 | 0 | 29 | 3 | 3 | 29 |
| `mathlib4::Units.map_neg_one` | 32 | 13 | 19 | 1 | 10 | 3 | 6 | 7 |
| `mathlib4::List.permutationsAux2_append` | 32 | 32 | 0 | 0 | 19 | 13 | 18 | 14 |
| `mathlib4::Finset.insert_inter` | 32 | 32 | 0 | 0 | 27 | 5 | 13 | 19 |
| `mathlib4::Stirling.stirlingSeq_one` | 32 | 32 | 0 | 0 | 29 | 3 | 7 | 25 |
| `mathlib4::MeasureTheory.MeasurePreserving.withDensity_rnDeriv` | 33 | 33 | 0 | 0 | 30 | 3 | 6 | 27 |
| `mathlib4::Ideal.ofList_cons_smul` | 33 | 33 | 0 | 0 | 16 | 17 | 9 | 24 |
| `mathlib4::Finsupp.card_Iio` | 32 | 32 | 0 | 1 | 28 | 4 | 8 | 24 |
| `mathlib4::Filter.IsBasis.FilterBasis.Filter.IsBasis.HasBasis.tendsto_left_iff` | 32 | 3 | 29 | 0 | 1 | 2 | 2 | 1 |
| `mathlib4::Ideal.span_pair_abs` | 33 | 33 | 0 | 0 | 19 | 14 | 7 | 26 |
| `mathlib4::CompleteLattice.Directed.disjoint_iSup_right` | 32 | 32 | 0 | 0 | 14 | 18 | 4 | 28 |
| `mathlib4::IsOfFinOrder.orderOf_pow` | 32 | 32 | 0 | 0 | 22 | 10 | 12 | 20 |
| `mathlib4::Option.Finset.mem_eraseNone` | 32 | 32 | 0 | 0 | 26 | 6 | 18 | 14 |
| `mathlib4::Nat.Prime.factorization_pow` | 32 | 32 | 0 | 0 | 23 | 9 | 11 | 21 |
| `mathlib4::Path.refl_reparam` | 32 | 32 | 0 | 0 | 8 | 24 | 7 | 25 |
| `mathlib4::Module.support_of_noZeroSMulDivisors` | 32 | 32 | 0 | 0 | 24 | 8 | 9 | 23 |
| `mathlib4::MeasureTheory.OuterMeasure.restrict_sInf_eq_sInf_restrict` | 33 | 33 | 0 | 1 | 25 | 8 | 5 | 28 |
| `mathlib4::Submodule.Module.Finite.Submodule.FG.restrictScalars` | 32 | 32 | 0 | 2 | 20 | 12 | 6 | 26 |
| `mathlib4::Finset.sup'_product_right` | 34 | 34 | 0 | 0 | 29 | 5 | 12 | 22 |
| `mathlib4::intervalIntegral.integral_deriv_mul_eq_sub_of_hasDeriv_right` | 32 | 32 | 0 | 0 | 28 | 4 | 3 | 29 |
| `mathlib4::WeierstrassCurve.twoTorsionPolynomial_discr_of_char_two` | 32 | 32 | 0 | 0 | 10 | 22 | 4 | 28 |
| `mathlib4::NumberField.rootDiscr_def` | 32 | 32 | 0 | 0 | 11 | 21 | 2 | 30 |
| `mathlib4::mem_rootsOfUnity_prime_pow_mul_iff` | 33 | 33 | 0 | 0 | 23 | 10 | 11 | 22 |
| `mathlib4::TensorProduct.map_add_right` | 32 | 32 | 0 | 0 | 14 | 18 | 9 | 23 |
| `mathlib4::CategoryTheory.MonoidalCategory.Limits.HasColimit.isoOfNatIso_ι_hom_whiskerRight` | 32 | 32 | 0 | 0 | 22 | 10 | 11 | 21 |
| `mathlib4::ENNReal.mul_div_right_comm` | 32 | 32 | 0 | 1 | 29 | 3 | 13 | 19 |

## Candidate Audit Summary

| Metric | Count |
|---|---:|
| `aesop_safe_fact_available` | 2304 |
| `aesop_unsafe_fact_available` | 1310 |
| `available` | 3614 |
| `learned_candidate` | 3680 |
| `proof_core` | 436 |
| `selected` | 3741 |
| `simp_safe_available` | 945 |
| `simp_unsafe_available` | 2669 |
| `target_or_alias` | 13 |
| `unavailable` | 127 |

### By Category

| Category | Count |
|---|---:|
| `theorem_like` | 1642 |
| `definition_like` | 988 |
| `simp_attr` | 903 |
| `class` | 84 |
| `proof_core_only_unknown` | 61 |
| `structure` | 53 |
| `unknown` | 5 |
| `inductive` | 3 |
| `instance` | 2 |

### By Decl Kind

| Decl kind | Count |
|---|---:|
| `theorem` | 1850 |
| `def` | 994 |
| `lemma` | 549 |
| `abbrev` | 140 |
| `class` | 84 |
| `proof_core_only` | 61 |
| `structure` | 53 |
| `unknown` | 5 |
| `inductive` | 3 |
| `instance` | 2 |

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
