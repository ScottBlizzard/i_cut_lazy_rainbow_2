# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_490.json`
- Pool mode: `strict_aesop`
- Result action suffix: `_filtered`
- Replayable goals evaluated: 115
- Attempts: 575
- Verified attempts: 6
- Non-empty-premise verified attempts: 6
- Goals with any proof: 2
- Goals with non-empty-premise proof: 2
- Action-dependent goals: 2

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 562 |
| `proved` | 6 |
| `search_fail` | 4 |
| `simp_fail` | 3 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `aesop_core_plus_learned16_filtered` | 2 | 2 | 115 |
| `aesop_core_plus_learned_filtered` | 2 | 2 | 115 |
| `hammerCore_core_plus_learned_filtered` | 0 | 0 | 115 |
| `hammer_core_plus_learned16_filtered` | 2 | 2 | 115 |
| `solve_by_elim_core_filtered` | 0 | 0 | 115 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Submodule.mem_ideal_smul_span_iff_exists_sum'` | 0 | 0 | 0 | none |
| `mathlib4::equicontinuousWithinAt_iInf_rng` | 0 | 0 | 0 | none |
| `mathlib4::rTensorHomEquivHomRTensor_apply` | 0 | 0 | 0 | none |
| `mathlib4::CharTwo.add_self_eq_zero` | 0 | 0 | 0 | none |
| `mathlib4::MvPowerSeries.coeff_mul_prod_one_sub_of_lt_order` | 0 | 0 | 0 | none |
| `mathlib4::Matrix.sum_mulVec_of_mem_colStochastic` | 0 | 0 | 0 | none |
| `mathlib4::continuousWithinAt_singleton` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.span_singleton_mul_right_unit` | 0 | 0 | 0 | none |
| `mathlib4::LightCondensed.free_lightProfinite_internallyProjective_iff_tensor_condition'` | 0 | 0 | 0 | none |
| `mathlib4::Fin.finsetImage_val_Ici` | 0 | 0 | 0 | none |
| `mathlib4::InnerProductGeometry.sin_angle_sub_mul_norm_of_inner_eq_zero` | 0 | 0 | 0 | none |
| `mathlib4::Real.smul_map_volume_mul_right` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.average_const` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | 0 | 0 | 0 | none |
| `mathlib4::Finset.insert_Ioc_sub_one_right_eq_Ioc` | 0 | 0 | 0 | none |
| `mathlib4::Set.preimage_iInter` | 3 | 3 | 0 | `hammer_core_plus_learned16_filtered` (16 facts, 0 simps) |
| `mathlib4::Matrix.dotProductᵣ_eq` | 0 | 0 | 0 | none |
| `mathlib4::Multiset.filter_cons` | 0 | 0 | 0 | none |
| `mathlib4::NormedAddCommGroup.summable_imp_tendsto_of_complete` | 0 | 0 | 0 | none |
| `mathlib4::Matrix.J_transpose` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.Adjunction.Equivalence.isAccessibleCategory` | 0 | 0 | 0 | none |
| `mathlib4::IsFoelner.isFoelner_iff_tendsto` | 0 | 0 | 0 | none |
| `mathlib4::Measurable.setLIntegral_kernel_prod_right` | 0 | 0 | 0 | none |
| `mathlib4::MvPolynomial.MvPolynomial.rename_comp_toMvPolynomial` | 0 | 0 | 0 | none |
| `mathlib4::CHSH_id` | 0 | 0 | 0 | none |
| `mathlib4::UpperSet.LowerSet.lowerClosure_prod` | 0 | 0 | 0 | none |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | 0 | 0 | 0 | none |
| `mathlib4::SimpleGraph.ediam_eq_top_iff_radius_eq_top` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.mul_X_add_natCast_comp` | 0 | 0 | 0 | none |
| `mathlib4::Finset.biUnion_inter` | 0 | 0 | 0 | none |
| `mathlib4::CFC.monotone_rpow` | 0 | 0 | 0 | none |
| `mathlib4::isMinOn_Ioi_of_deriv` | 0 | 0 | 0 | none |
| `mathlib4::ProbabilityTheory.IdentDistrib.memLp_snd` | 0 | 0 | 0 | none |
| `mathlib4::Set.Finset.maximal_iff_forall_insert` | 0 | 0 | 0 | none |
| `mathlib4::HasStrictFDerivAt.hasStrictFDerivAt_implicitFunctionOfProdDomain` | 0 | 0 | 0 | none |
| `mathlib4::Finsupp.linearCombination_restrict` | 0 | 0 | 0 | none |
| `mathlib4::IsMulFreimanIso.mul_eq_mul` | 0 | 0 | 0 | none |
| `mathlib4::Multiset.card_coe` | 0 | 0 | 0 | none |
| `mathlib4::AddChar.to_mulShift_inj_of_isPrimitive` | 0 | 0 | 0 | none |
| `mathlib4::AddChar.zmod_char_primitive_of_eq_one_only_at_zero` | 0 | 0 | 0 | none |
| `mathlib4::HomologicalComplex₂.totalAux.totalAux.ι_D₂` | 0 | 0 | 0 | none |
| `mathlib4::Localization.fg` | 0 | 0 | 0 | none |
| `mathlib4::IntermediateField.Normal.minpoly_eq_iff_mem_orbit` | 0 | 0 | 0 | none |
| `mathlib4::IsTranscendenceBasis.mvPolynomial'` | 0 | 0 | 0 | none |
| `mathlib4::Nat.fermatNumber_strictMono` | 0 | 0 | 0 | none |
| `mathlib4::Affine.Simplex.face_restrict` | 0 | 0 | 0 | none |
| `mathlib4::HomologicalComplex.comp_pOpcycles_eq_zero_iff_up_to_refinements` | 0 | 0 | 0 | none |
| `mathlib4::IsCyclotomicExtension.adjoin_roots_cyclotomic_eq_adjoin_nth_roots` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.NatTrans.app_sum` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.Jacobian.addY_neg` | 0 | 0 | 0 | none |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | 0 | 0 | 0 | none |
| `mathlib4::Finset.Fin.prod_Ioo_cast` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft` | 0 | 0 | 0 | none |
| `mathlib4::Nat.frequently_atTop_modEq_one` | 0 | 0 | 0 | none |
| `mathlib4::Subalgebra.IsAlgebraic.tower_top_of_subalgebra_le` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.height_le_ringKrullDim_of_isPrime` | 0 | 0 | 0 | none |
| `mathlib4::Real.sign_apply_eq` | 0 | 0 | 0 | none |
| `mathlib4::Equiv.Perm.apply_mem_support` | 0 | 0 | 0 | none |
| `mathlib4::Multiset.Subset.ndinter_eq_left` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.Core.Functor.Iso.coreWhiskerLeft` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicGeometry.Scheme.mem_overGrothendieckTopology` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | 0 | 0 | 0 | none |
| `mathlib4::classifyingSpaceUniversalCover.Rep.standardComplex.d_of` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.restrictScalars_sInf` | 0 | 0 | 0 | none |
| `mathlib4::map_le_lineMap_iff_slope_le_slope_left` | 0 | 0 | 0 | none |
| `mathlib4::contMDiffAt_iff_source` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.ObjectProperty.trW_of_op` | 0 | 0 | 0 | none |
| `mathlib4::Nat.Function.Involutive.Even.neg_one_zpow` | 0 | 0 | 0 | none |
| `mathlib4::intervalIntegral.FTCFilter.integral_hasStrictDerivAt_left` | 0 | 0 | 0 | none |
| `mathlib4::Filter.blimsup_eq_iInf_biSup_of_nat` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.Projective.polynomialY_eq` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.Submodule.Submodule.Submodule.Submodule.LinearMap.map_restrict` | 0 | 0 | 0 | none |
| `mathlib4::NumberField.InfinitePlace.IsUnramified.of_restrictScalars` | 0 | 0 | 0 | none |
| `mathlib4::Nat.count_le_card` | 0 | 0 | 0 | none |
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.TaggedPrepartition.forall_mem_single` | 0 | 0 | 0 | none |
| `mathlib4::IsUltrametricDist.norm_tprod_le_of_forall_le_of_nonneg` | 0 | 0 | 0 | none |
| `mathlib4::Filter.IsBoundedUnder.mono_le` | 0 | 0 | 0 | none |
| `mathlib4::Matroid.eRk_le_eRank` | 0 | 0 | 0 | none |
| `mathlib4::Equiv.Perm.VectorsProdEqOne.filter_parts_partition_eq_cycleType` | 0 | 0 | 0 | none |
| `mathlib4::HurwitzZeta.differentiableAt_completedHurwitzZetaEven` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | 0 | 0 | 0 | none |
| `mathlib4::Matroid.uniqueBaseOn_self` | 0 | 0 | 0 | none |
| `mathlib4::Multiset.revzip_powersetAux'` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | 0 | 0 | 0 | none |
| `mathlib4::SSet.Truncated.HomotopicR.symm` | 0 | 0 | 0 | none |
| `mathlib4::RingHom.CodescendsAlong.includeRight` | 0 | 0 | 0 | none |
| `mathlib4::Wbtw.dist_add_dist` | 0 | 0 | 0 | none |
| `mathlib4::Ordnode.size_balance'` | 0 | 0 | 0 | none |
| `mathlib4::Module.Basis.Module.rank_zero_iff_of_free` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.ObjectProperty.SerreClassLocalization.inverseImage_monomorphisms` | 0 | 0 | 0 | none |
| `mathlib4::Finset.max'_singleton` | 0 | 0 | 0 | none |
| `mathlib4::Set.exists_eq_singleton_iff_nonempty_subsingleton` | 0 | 0 | 0 | none |
| `mathlib4::EReal.mul_div_cancel` | 0 | 0 | 0 | none |
| `mathlib4::Multiset.disjoint_add_left` | 0 | 0 | 0 | none |
| `mathlib4::Ordnode.emem_iff_mem_toList` | 0 | 0 | 0 | none |
| `mathlib4::borel_eq_generateFrom_Ico` | 0 | 0 | 0 | none |
| `mathlib4::Mathlib.Tactic.Algebra.rat_ofNat_smul_1` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicIndependent.lift_trdeg_le_of_injective` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.evalEval_intCast` | 0 | 0 | 0 | none |
| `mathlib4::Cube.insertAt_boundary` | 0 | 0 | 0 | none |
| `mathlib4::SeparationQuotient.uniformContinuous_dom₂` | 0 | 0 | 0 | none |
| `mathlib4::GroupExtension.Section.mul_inv_mul_mul_mem_range_inl` | 0 | 0 | 0 | none |
| `mathlib4::GenContFract.exists_s_b_of_partDen` | 0 | 0 | 0 | none |
| `mathlib4::SimpleGraph.EdgeLabeling.TopEdgeLabeling.toTopEdgeLabeling_labelGraph` | 0 | 0 | 0 | none |
| `mathlib4::PadicInt.PadicInt.mahlerSeries_apply` | 0 | 0 | 0 | none |
| `mathlib4::Mathlib.Tactic.FieldSimp.NF.eval_cons_mul_eval_cons_neg` | 0 | 0 | 0 | none |
| `mathlib4::Set.image2_iUnion₂_right` | 3 | 3 | 0 | `hammer_core_plus_learned16_filtered` (19 facts, 0 simps) |
| `mathlib4::MonoidAlgebra.LaurentPolynomial.comul_T` | 0 | 0 | 0 | none |
| `mathlib4::Nat.range_eq_Icc_zero_sub_one` | 0 | 0 | 0 | none |
| `mathlib4::Matrix.blockDiagonal_add` | 0 | 0 | 0 | none |
| `mathlib4::Nat.Partrec.Nat.Partrec.Code.Nat.Partrec.Code.Nat.Partrec.Code.eval_prec_zero` | 0 | 0 | 0 | none |
| `mathlib4::EuclideanGeometry.angle_midpoint_eq_pi` | 0 | 0 | 0 | none |
| `mathlib4::NNReal.tendsto_rpow_atTop` | 0 | 0 | 0 | none |
| `mathlib4::Subgroup.Commensurable.commensurable_inv` | 0 | 0 | 0 | none |
| `mathlib4::RatFunc.InftyValuation.map_mul'` | 0 | 0 | 0 | none |

## Availability

| Goal | Checked | Available | Failed | Target/alias | Aesop-safe available | Aesop-unsafe available | Simp-safe available | Simp-unsafe available |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mathlib4::Submodule.mem_ideal_smul_span_iff_exists_sum'` | 32 | 32 | 0 | 0 | 30 | 2 | 7 | 25 |
| `mathlib4::equicontinuousWithinAt_iInf_rng` | 34 | 34 | 0 | 0 | 20 | 14 | 4 | 30 |
| `mathlib4::rTensorHomEquivHomRTensor_apply` | 33 | 33 | 0 | 0 | 14 | 19 | 16 | 17 |
| `mathlib4::CharTwo.add_self_eq_zero` | 33 | 33 | 0 | 0 | 29 | 4 | 7 | 26 |
| `mathlib4::MvPowerSeries.coeff_mul_prod_one_sub_of_lt_order` | 32 | 32 | 0 | 1 | 23 | 9 | 3 | 29 |
| `mathlib4::Matrix.sum_mulVec_of_mem_colStochastic` | 33 | 33 | 0 | 0 | 25 | 8 | 8 | 25 |
| `mathlib4::continuousWithinAt_singleton` | 32 | 32 | 0 | 0 | 31 | 1 | 8 | 24 |
| `mathlib4::Ideal.span_singleton_mul_right_unit` | 33 | 33 | 0 | 0 | 30 | 3 | 14 | 19 |
| `mathlib4::LightCondensed.free_lightProfinite_internallyProjective_iff_tensor_condition'` | 34 | 34 | 0 | 0 | 5 | 29 | 5 | 29 |
| `mathlib4::Fin.finsetImage_val_Ici` | 32 | 32 | 0 | 0 | 26 | 6 | 27 | 5 |
| `mathlib4::InnerProductGeometry.sin_angle_sub_mul_norm_of_inner_eq_zero` | 33 | 33 | 0 | 0 | 31 | 2 | 4 | 29 |
| `mathlib4::Real.smul_map_volume_mul_right` | 33 | 33 | 0 | 0 | 29 | 4 | 22 | 11 |
| `mathlib4::MeasureTheory.average_const` | 32 | 32 | 0 | 0 | 27 | 5 | 11 | 21 |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | 34 | 34 | 0 | 0 | 13 | 21 | 12 | 22 |
| `mathlib4::Finset.insert_Ioc_sub_one_right_eq_Ioc` | 33 | 33 | 0 | 0 | 31 | 2 | 12 | 21 |
| `mathlib4::Set.preimage_iInter` | 32 | 16 | 16 | 0 | 15 | 1 | 2 | 14 |
| `mathlib4::Matrix.dotProductᵣ_eq` | 32 | 32 | 0 | 0 | 18 | 14 | 7 | 25 |
| `mathlib4::Multiset.filter_cons` | 34 | 34 | 0 | 0 | 26 | 8 | 10 | 24 |
| `mathlib4::NormedAddCommGroup.summable_imp_tendsto_of_complete` | 32 | 32 | 0 | 0 | 16 | 16 | 3 | 29 |
| `mathlib4::Matrix.J_transpose` | 33 | 33 | 0 | 0 | 20 | 13 | 9 | 24 |
| `mathlib4::CategoryTheory.Adjunction.Equivalence.isAccessibleCategory` | 32 | 32 | 0 | 0 | 16 | 16 | 2 | 30 |
| `mathlib4::IsFoelner.isFoelner_iff_tendsto` | 32 | 32 | 0 | 0 | 27 | 5 | 5 | 27 |
| `mathlib4::Measurable.setLIntegral_kernel_prod_right` | 32 | 32 | 0 | 0 | 29 | 3 | 4 | 28 |
| `mathlib4::MvPolynomial.MvPolynomial.rename_comp_toMvPolynomial` | 32 | 32 | 0 | 0 | 17 | 15 | 11 | 21 |
| `mathlib4::CHSH_id` | 32 | 32 | 0 | 0 | 11 | 21 | 11 | 21 |
| `mathlib4::UpperSet.LowerSet.lowerClosure_prod` | 32 | 32 | 0 | 0 | 23 | 9 | 14 | 18 |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | 33 | 33 | 0 | 3 | 23 | 10 | 12 | 21 |
| `mathlib4::SimpleGraph.ediam_eq_top_iff_radius_eq_top` | 33 | 33 | 0 | 0 | 29 | 4 | 10 | 23 |
| `mathlib4::Polynomial.mul_X_add_natCast_comp` | 33 | 33 | 0 | 0 | 27 | 6 | 28 | 5 |
| `mathlib4::Finset.biUnion_inter` | 32 | 32 | 0 | 0 | 29 | 3 | 11 | 21 |
| `mathlib4::CFC.monotone_rpow` | 33 | 33 | 0 | 0 | 28 | 5 | 1 | 32 |
| `mathlib4::isMinOn_Ioi_of_deriv` | 34 | 34 | 0 | 0 | 27 | 7 | 1 | 33 |
| `mathlib4::ProbabilityTheory.IdentDistrib.memLp_snd` | 32 | 32 | 0 | 0 | 5 | 27 | 2 | 30 |
| `mathlib4::Set.Finset.maximal_iff_forall_insert` | 32 | 32 | 0 | 1 | 29 | 3 | 5 | 27 |
| `mathlib4::HasStrictFDerivAt.hasStrictFDerivAt_implicitFunctionOfProdDomain` | 34 | 34 | 0 | 0 | 22 | 12 | 7 | 27 |
| `mathlib4::Finsupp.linearCombination_restrict` | 32 | 32 | 0 | 0 | 20 | 12 | 12 | 20 |
| `mathlib4::IsMulFreimanIso.mul_eq_mul` | 32 | 32 | 0 | 1 | 25 | 7 | 8 | 24 |
| `mathlib4::Multiset.card_coe` | 33 | 33 | 0 | 0 | 19 | 14 | 20 | 13 |
| `mathlib4::AddChar.to_mulShift_inj_of_isPrimitive` | 32 | 32 | 0 | 0 | 23 | 9 | 6 | 26 |
| `mathlib4::AddChar.zmod_char_primitive_of_eq_one_only_at_zero` | 32 | 32 | 0 | 0 | 24 | 8 | 11 | 21 |
| `mathlib4::HomologicalComplex₂.totalAux.totalAux.ι_D₂` | 32 | 32 | 0 | 0 | 5 | 27 | 6 | 26 |
| `mathlib4::Localization.fg` | 34 | 34 | 0 | 0 | 6 | 28 | 11 | 23 |
| `mathlib4::IntermediateField.Normal.minpoly_eq_iff_mem_orbit` | 32 | 32 | 0 | 0 | 27 | 5 | 7 | 25 |
| `mathlib4::IsTranscendenceBasis.mvPolynomial'` | 32 | 32 | 0 | 0 | 21 | 11 | 4 | 28 |
| `mathlib4::Nat.fermatNumber_strictMono` | 32 | 32 | 0 | 0 | 29 | 3 | 7 | 25 |
| `mathlib4::Affine.Simplex.face_restrict` | 33 | 33 | 0 | 0 | 19 | 14 | 20 | 13 |
| `mathlib4::HomologicalComplex.comp_pOpcycles_eq_zero_iff_up_to_refinements` | 33 | 33 | 0 | 1 | 26 | 7 | 10 | 23 |
| `mathlib4::IsCyclotomicExtension.adjoin_roots_cyclotomic_eq_adjoin_nth_roots` | 34 | 34 | 0 | 0 | 21 | 13 | 12 | 22 |
| `mathlib4::CategoryTheory.NatTrans.app_sum` | 32 | 32 | 0 | 0 | 1 | 31 | 23 | 9 |
| `mathlib4::WeierstrassCurve.Jacobian.addY_neg` | 36 | 36 | 0 | 0 | 10 | 26 | 5 | 31 |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | 32 | 32 | 0 | 0 | 10 | 22 | 8 | 24 |
| `mathlib4::Finset.Fin.prod_Ioo_cast` | 33 | 33 | 0 | 0 | 20 | 13 | 13 | 20 |
| `mathlib4::CategoryTheory.MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft` | 32 | 32 | 0 | 0 | 11 | 21 | 10 | 22 |
| `mathlib4::Nat.frequently_atTop_modEq_one` | 33 | 33 | 0 | 0 | 30 | 3 | 7 | 26 |
| `mathlib4::Subalgebra.IsAlgebraic.tower_top_of_subalgebra_le` | 32 | 32 | 0 | 0 | 25 | 7 | 4 | 28 |
| `mathlib4::Ideal.height_le_ringKrullDim_of_isPrime` | 33 | 33 | 0 | 0 | 26 | 7 | 6 | 27 |
| `mathlib4::Real.sign_apply_eq` | 32 | 32 | 0 | 0 | 31 | 1 | 14 | 18 |
| `mathlib4::Equiv.Perm.apply_mem_support` | 33 | 33 | 0 | 0 | 31 | 2 | 12 | 21 |
| `mathlib4::Multiset.Subset.ndinter_eq_left` | 33 | 33 | 0 | 0 | 28 | 5 | 12 | 21 |
| `mathlib4::CategoryTheory.Core.Functor.Iso.coreWhiskerLeft` | 32 | 32 | 0 | 0 | 2 | 30 | 23 | 9 |
| `mathlib4::AlgebraicGeometry.Scheme.mem_overGrothendieckTopology` | 33 | 33 | 0 | 0 | 0 | 33 | 7 | 26 |
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | 32 | 32 | 0 | 0 | 9 | 23 | 13 | 19 |
| `mathlib4::classifyingSpaceUniversalCover.Rep.standardComplex.d_of` | 32 | 32 | 0 | 0 | 27 | 5 | 18 | 14 |
| `mathlib4::Submodule.restrictScalars_sInf` | 32 | 32 | 0 | 0 | 22 | 10 | 8 | 24 |
| `mathlib4::map_le_lineMap_iff_slope_le_slope_left` | 33 | 33 | 0 | 0 | 31 | 2 | 7 | 26 |
| `mathlib4::contMDiffAt_iff_source` | 33 | 33 | 0 | 0 | 26 | 7 | 2 | 31 |
| `mathlib4::CategoryTheory.ObjectProperty.trW_of_op` | 33 | 33 | 0 | 0 | 17 | 16 | 0 | 33 |
| `mathlib4::Nat.Function.Involutive.Even.neg_one_zpow` | 33 | 33 | 0 | 0 | 32 | 1 | 19 | 14 |
| `mathlib4::intervalIntegral.FTCFilter.integral_hasStrictDerivAt_left` | 32 | 32 | 0 | 0 | 28 | 4 | 3 | 29 |
| `mathlib4::Filter.blimsup_eq_iInf_biSup_of_nat` | 32 | 32 | 0 | 0 | 28 | 4 | 13 | 19 |
| `mathlib4::WeierstrassCurve.Projective.polynomialY_eq` | 32 | 32 | 0 | 0 | 13 | 19 | 1 | 31 |
| `mathlib4::Submodule.Submodule.Submodule.Submodule.Submodule.LinearMap.map_restrict` | 32 | 32 | 0 | 0 | 22 | 10 | 17 | 15 |
| `mathlib4::NumberField.InfinitePlace.IsUnramified.of_restrictScalars` | 35 | 35 | 0 | 1 | 15 | 20 | 4 | 31 |
| `mathlib4::Nat.count_le_card` | 33 | 33 | 0 | 0 | 25 | 8 | 9 | 24 |
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.TaggedPrepartition.forall_mem_single` | 32 | 32 | 0 | 0 | 14 | 18 | 9 | 23 |
| `mathlib4::IsUltrametricDist.norm_tprod_le_of_forall_le_of_nonneg` | 32 | 32 | 0 | 0 | 29 | 3 | 3 | 29 |
| `mathlib4::Filter.IsBoundedUnder.mono_le` | 32 | 32 | 0 | 0 | 28 | 4 | 3 | 29 |
| `mathlib4::Matroid.eRk_le_eRank` | 33 | 33 | 0 | 0 | 25 | 8 | 10 | 23 |
| `mathlib4::Equiv.Perm.VectorsProdEqOne.filter_parts_partition_eq_cycleType` | 33 | 33 | 0 | 0 | 24 | 9 | 10 | 23 |
| `mathlib4::HurwitzZeta.differentiableAt_completedHurwitzZetaEven` | 34 | 34 | 0 | 0 | 13 | 21 | 5 | 29 |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | 33 | 33 | 0 | 0 | 18 | 15 | 11 | 22 |
| `mathlib4::Matroid.uniqueBaseOn_self` | 32 | 32 | 0 | 0 | 21 | 11 | 9 | 23 |
| `mathlib4::Multiset.revzip_powersetAux'` | 32 | 32 | 0 | 0 | 14 | 18 | 9 | 23 |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | 33 | 33 | 0 | 0 | 27 | 6 | 2 | 31 |
| `mathlib4::SSet.Truncated.HomotopicR.symm` | 34 | 34 | 0 | 0 | 7 | 27 | 4 | 30 |
| `mathlib4::RingHom.CodescendsAlong.includeRight` | 32 | 32 | 0 | 1 | 9 | 23 | 6 | 26 |
| `mathlib4::Wbtw.dist_add_dist` | 32 | 32 | 0 | 0 | 13 | 19 | 6 | 26 |
| `mathlib4::Ordnode.size_balance'` | 33 | 33 | 0 | 0 | 0 | 33 | 1 | 32 |
| `mathlib4::Module.Basis.Module.rank_zero_iff_of_free` | 32 | 32 | 0 | 0 | 25 | 7 | 6 | 26 |
| `mathlib4::CategoryTheory.ObjectProperty.SerreClassLocalization.inverseImage_monomorphisms` | 33 | 33 | 0 | 0 | 19 | 14 | 4 | 29 |
| `mathlib4::Finset.max'_singleton` | 33 | 33 | 0 | 0 | 26 | 7 | 16 | 17 |
| `mathlib4::Set.exists_eq_singleton_iff_nonempty_subsingleton` | 32 | 11 | 21 | 0 | 10 | 1 | 4 | 7 |
| `mathlib4::EReal.mul_div_cancel` | 33 | 33 | 0 | 1 | 30 | 3 | 22 | 11 |
| `mathlib4::Multiset.disjoint_add_left` | 33 | 33 | 0 | 0 | 26 | 7 | 19 | 14 |
| `mathlib4::Ordnode.emem_iff_mem_toList` | 32 | 32 | 0 | 0 | 18 | 14 | 7 | 25 |
| `mathlib4::borel_eq_generateFrom_Ico` | 33 | 33 | 0 | 0 | 24 | 9 | 11 | 22 |
| `mathlib4::Mathlib.Tactic.Algebra.rat_ofNat_smul_1` | 33 | 33 | 0 | 0 | 23 | 10 | 6 | 27 |
| `mathlib4::AlgebraicIndependent.lift_trdeg_le_of_injective` | 32 | 32 | 0 | 0 | 27 | 5 | 3 | 29 |
| `mathlib4::Polynomial.evalEval_intCast` | 33 | 33 | 0 | 0 | 22 | 11 | 12 | 21 |
| `mathlib4::Cube.insertAt_boundary` | 32 | 32 | 0 | 0 | 19 | 13 | 8 | 24 |
| `mathlib4::SeparationQuotient.uniformContinuous_dom₂` | 33 | 33 | 0 | 0 | 22 | 11 | 8 | 25 |
| `mathlib4::GroupExtension.Section.mul_inv_mul_mul_mem_range_inl` | 32 | 32 | 0 | 0 | 21 | 11 | 7 | 25 |
| `mathlib4::GenContFract.exists_s_b_of_partDen` | 33 | 33 | 0 | 0 | 25 | 8 | 7 | 26 |
| `mathlib4::SimpleGraph.EdgeLabeling.TopEdgeLabeling.toTopEdgeLabeling_labelGraph` | 32 | 32 | 0 | 0 | 12 | 20 | 8 | 24 |
| `mathlib4::PadicInt.PadicInt.mahlerSeries_apply` | 32 | 32 | 0 | 0 | 27 | 5 | 3 | 29 |
| `mathlib4::Mathlib.Tactic.FieldSimp.NF.eval_cons_mul_eval_cons_neg` | 35 | 35 | 0 | 0 | 14 | 21 | 12 | 23 |
| `mathlib4::Set.image2_iUnion₂_right` | 33 | 21 | 12 | 0 | 18 | 3 | 5 | 16 |
| `mathlib4::MonoidAlgebra.LaurentPolynomial.comul_T` | 33 | 33 | 0 | 0 | 17 | 16 | 11 | 22 |
| `mathlib4::Nat.range_eq_Icc_zero_sub_one` | 32 | 32 | 0 | 0 | 30 | 2 | 13 | 19 |
| `mathlib4::Matrix.blockDiagonal_add` | 33 | 33 | 0 | 0 | 8 | 25 | 19 | 14 |
| `mathlib4::Nat.Partrec.Nat.Partrec.Code.Nat.Partrec.Code.Nat.Partrec.Code.eval_prec_zero` | 32 | 32 | 0 | 0 | 21 | 11 | 9 | 23 |
| `mathlib4::EuclideanGeometry.angle_midpoint_eq_pi` | 32 | 32 | 0 | 0 | 30 | 2 | 19 | 13 |
| `mathlib4::NNReal.tendsto_rpow_atTop` | 33 | 33 | 0 | 1 | 27 | 6 | 9 | 24 |
| `mathlib4::Subgroup.Commensurable.commensurable_inv` | 33 | 33 | 0 | 0 | 20 | 13 | 15 | 18 |
| `mathlib4::RatFunc.InftyValuation.map_mul'` | 33 | 33 | 0 | 0 | 9 | 24 | 6 | 27 |

## Candidate Audit Summary

| Metric | Count |
|---|---:|
| `aesop_safe_fact_available` | 2398 |
| `aesop_unsafe_fact_available` | 1309 |
| `available` | 3707 |
| `learned_candidate` | 3680 |
| `proof_core` | 439 |
| `selected` | 3756 |
| `simp_safe_available` | 1064 |
| `simp_unsafe_available` | 2643 |
| `target_or_alias` | 11 |
| `unavailable` | 49 |

### By Category

| Category | Count |
|---|---:|
| `theorem_like` | 1626 |
| `simp_attr` | 1024 |
| `definition_like` | 892 |
| `class` | 77 |
| `proof_core_only_unknown` | 76 |
| `structure` | 48 |
| `inductive` | 7 |
| `unknown` | 5 |
| `instance` | 1 |

### By Decl Kind

| Decl kind | Count |
|---|---:|
| `theorem` | 1823 |
| `def` | 962 |
| `lemma` | 631 |
| `abbrev` | 126 |
| `class` | 77 |
| `proof_core_only` | 76 |
| `structure` | 48 |
| `inductive` | 7 |
| `unknown` | 5 |
| `instance` | 1 |

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
