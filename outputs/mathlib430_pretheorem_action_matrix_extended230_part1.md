# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_490.json`
- Replayable goals evaluated: 115
- Attempts: 1840
- Verified attempts: 138
- Non-empty-premise verified attempts: 122
- Goals with any proof: 29
- Goals with non-empty-premise proof: 29
- Action-dependent goals: 14

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 654 |
| `proved` | 138 |
| `rewrite_fail` | 15 |
| `search_fail` | 731 |
| `simp_fail` | 163 |
| `sorry_warning` | 77 |
| `timeout` | 43 |
| `typeclass_or_inference` | 15 |
| `unknown_identifier` | 4 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `aesop_core_plus_learned` | 21 | 21 | 115 |
| `aesop_core_plus_learned16` | 21 | 21 | 115 |
| `aesop_empty` | 15 | 0 | 115 |
| `hammerCore_core_plus_learned16` | 6 | 6 | 115 |
| `hammerCore_core_plus_learned32` | 6 | 6 | 115 |
| `hammer_core_plus_learned16` | 18 | 18 | 115 |
| `hammer_core_plus_learned32` | 18 | 18 | 115 |
| `linarith_empty` | 0 | 0 | 115 |
| `nlinarith_empty` | 0 | 0 | 115 |
| `norm_num_empty` | 1 | 0 | 115 |
| `omega_empty` | 0 | 0 | 115 |
| `ring_nf_empty` | 0 | 0 | 115 |
| `simp_all_core_plus_learned16` | 12 | 12 | 115 |
| `simp_all_core_plus_learned32` | 12 | 12 | 115 |
| `solve_by_elim_core_plus_learned16` | 4 | 4 | 115 |
| `solve_by_elim_core_plus_learned32` | 4 | 4 | 115 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Submodule.mem_ideal_smul_span_iff_exists_sum'` | 0 | 0 | 0 | none |
| `mathlib4::equicontinuousWithinAt_iInf_rng` | 0 | 0 | 0 | none |
| `mathlib4::rTensorHomEquivHomRTensor_apply` | 0 | 0 | 0 | none |
| `mathlib4::CharTwo.add_self_eq_zero` | 0 | 0 | 0 | none |
| `mathlib4::MvPowerSeries.coeff_mul_prod_one_sub_of_lt_order` | 0 | 0 | 0 | none |
| `mathlib4::Matrix.sum_mulVec_of_mem_colStochastic` | 0 | 0 | 0 | none |
| `mathlib4::continuousWithinAt_singleton` | 6 | 6 | 0 | `simp_all_core_plus_learned16` (0 facts, 3 simps) |
| `mathlib4::Ideal.span_singleton_mul_right_unit` | 0 | 0 | 0 | none |
| `mathlib4::LightCondensed.free_lightProfinite_internallyProjective_iff_tensor_condition'` | 0 | 0 | 0 | none |
| `mathlib4::Fin.finsetImage_val_Ici` | 0 | 0 | 0 | none |
| `mathlib4::InnerProductGeometry.sin_angle_sub_mul_norm_of_inner_eq_zero` | 0 | 0 | 0 | none |
| `mathlib4::Real.smul_map_volume_mul_right` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.average_const` | 4 | 4 | 0 | `simp_all_core_plus_learned16` (0 facts, 12 simps) |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | 2 | 2 | 0 | `hammerCore_core_plus_learned16` (11 facts, 18 simps) |
| `mathlib4::Finset.insert_Ioc_sub_one_right_eq_Ioc` | 0 | 0 | 0 | none |
| `mathlib4::Set.preimage_iInter` | 3 | 2 | 1 | `hammer_core_plus_learned16` (16 facts, 0 simps) |
| `mathlib4::Matrix.dotProductᵣ_eq` | 4 | 4 | 0 | `simp_all_core_plus_learned16` (0 facts, 10 simps) |
| `mathlib4::Multiset.filter_cons` | 3 | 2 | 1 | `hammer_core_plus_learned16` (20 facts, 0 simps) |
| `mathlib4::NormedAddCommGroup.summable_imp_tendsto_of_complete` | 2 | 2 | 0 | `aesop_core_plus_learned` (12 facts, 6 simps) |
| `mathlib4::Matrix.J_transpose` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.Adjunction.Equivalence.isAccessibleCategory` | 0 | 0 | 0 | none |
| `mathlib4::IsFoelner.isFoelner_iff_tendsto` | 0 | 0 | 0 | none |
| `mathlib4::Measurable.setLIntegral_kernel_prod_right` | 0 | 0 | 0 | none |
| `mathlib4::MvPolynomial.MvPolynomial.rename_comp_toMvPolynomial` | 5 | 4 | 1 | `hammer_core_plus_learned16` (13 facts, 0 simps) |
| `mathlib4::CHSH_id` | 0 | 0 | 0 | none |
| `mathlib4::UpperSet.LowerSet.lowerClosure_prod` | 3 | 2 | 1 | `hammer_core_plus_learned16` (17 facts, 0 simps) |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | 4 | 4 | 0 | `hammer_core_plus_learned16` (6 facts, 0 simps) |
| `mathlib4::SimpleGraph.ediam_eq_top_iff_radius_eq_top` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.mul_X_add_natCast_comp` | 0 | 0 | 0 | none |
| `mathlib4::Finset.biUnion_inter` | 5 | 4 | 1 | `hammer_core_plus_learned16` (17 facts, 0 simps) |
| `mathlib4::CFC.monotone_rpow` | 0 | 0 | 0 | none |
| `mathlib4::isMinOn_Ioi_of_deriv` | 2 | 2 | 0 | `hammer_core_plus_learned16` (23 facts, 0 simps) |
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
| `mathlib4::Affine.Simplex.face_restrict` | 7 | 6 | 1 | `hammer_core_plus_learned16` (16 facts, 0 simps) |
| `mathlib4::HomologicalComplex.comp_pOpcycles_eq_zero_iff_up_to_refinements` | 0 | 0 | 0 | none |
| `mathlib4::IsCyclotomicExtension.adjoin_roots_cyclotomic_eq_adjoin_nth_roots` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.NatTrans.app_sum` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.Jacobian.addY_neg` | 0 | 0 | 0 | none |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | 4 | 4 | 0 | `simp_all_core_plus_learned16` (0 facts, 17 simps) |
| `mathlib4::Finset.Fin.prod_Ioo_cast` | 5 | 4 | 1 | `hammer_core_plus_learned16` (15 facts, 0 simps) |
| `mathlib4::CategoryTheory.MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft` | 0 | 0 | 0 | none |
| `mathlib4::Nat.frequently_atTop_modEq_one` | 0 | 0 | 0 | none |
| `mathlib4::Subalgebra.IsAlgebraic.tower_top_of_subalgebra_le` | 0 | 0 | 0 | none |
| `mathlib4::Ideal.height_le_ringKrullDim_of_isPrime` | 0 | 0 | 0 | none |
| `mathlib4::Real.sign_apply_eq` | 2 | 2 | 0 | `aesop_core_plus_learned` (6 facts, 6 simps) |
| `mathlib4::Equiv.Perm.apply_mem_support` | 9 | 8 | 1 | `hammer_core_plus_learned16` (9 facts, 0 simps) |
| `mathlib4::Multiset.Subset.ndinter_eq_left` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.Core.Functor.Iso.coreWhiskerLeft` | 5 | 4 | 1 | `hammer_core_plus_learned16` (5 facts, 0 simps) |
| `mathlib4::AlgebraicGeometry.Scheme.mem_overGrothendieckTopology` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | 4 | 4 | 0 | `simp_all_core_plus_learned16` (0 facts, 16 simps) |
| `mathlib4::classifyingSpaceUniversalCover.Rep.standardComplex.d_of` | 0 | 0 | 0 | none |
| `mathlib4::Submodule.restrictScalars_sInf` | 3 | 2 | 1 | `hammer_core_plus_learned16` (12 facts, 0 simps) |
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
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.TaggedPrepartition.forall_mem_single` | 8 | 6 | 2 | `hammer_core_plus_learned16` (11 facts, 0 simps) |
| `mathlib4::IsUltrametricDist.norm_tprod_le_of_forall_le_of_nonneg` | 0 | 0 | 0 | none |
| `mathlib4::Filter.IsBoundedUnder.mono_le` | 0 | 0 | 0 | none |
| `mathlib4::Matroid.eRk_le_eRank` | 0 | 0 | 0 | none |
| `mathlib4::Equiv.Perm.VectorsProdEqOne.filter_parts_partition_eq_cycleType` | 0 | 0 | 0 | none |
| `mathlib4::HurwitzZeta.differentiableAt_completedHurwitzZetaEven` | 0 | 0 | 0 | none |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | 8 | 8 | 0 | `simp_all_core_plus_learned16` (0 facts, 16 simps) |
| `mathlib4::Matroid.uniqueBaseOn_self` | 11 | 10 | 1 | `hammer_core_plus_learned16` (12 facts, 0 simps) |
| `mathlib4::Multiset.revzip_powersetAux'` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | 6 | 6 | 0 | `hammer_core_plus_learned16` (7 facts, 0 simps) |
| `mathlib4::SSet.Truncated.HomotopicR.symm` | 0 | 0 | 0 | none |
| `mathlib4::RingHom.CodescendsAlong.includeRight` | 0 | 0 | 0 | none |
| `mathlib4::Wbtw.dist_add_dist` | 0 | 0 | 0 | none |
| `mathlib4::Ordnode.size_balance'` | 0 | 0 | 0 | none |
| `mathlib4::Module.Basis.Module.rank_zero_iff_of_free` | 0 | 0 | 0 | none |
| `mathlib4::CategoryTheory.ObjectProperty.SerreClassLocalization.inverseImage_monomorphisms` | 0 | 0 | 0 | none |
| `mathlib4::Finset.max'_singleton` | 11 | 10 | 1 | `hammer_core_plus_learned16` (18 facts, 0 simps) |
| `mathlib4::Set.exists_eq_singleton_iff_nonempty_subsingleton` | 0 | 0 | 0 | none |
| `mathlib4::EReal.mul_div_cancel` | 0 | 0 | 0 | none |
| `mathlib4::Multiset.disjoint_add_left` | 0 | 0 | 0 | none |
| `mathlib4::Ordnode.emem_iff_mem_toList` | 0 | 0 | 0 | none |
| `mathlib4::borel_eq_generateFrom_Ico` | 0 | 0 | 0 | none |
| `mathlib4::Mathlib.Tactic.Algebra.rat_ofNat_smul_1` | 0 | 0 | 0 | none |
| `mathlib4::AlgebraicIndependent.lift_trdeg_le_of_injective` | 0 | 0 | 0 | none |
| `mathlib4::Polynomial.evalEval_intCast` | 4 | 4 | 0 | `simp_all_core_plus_learned16` (0 facts, 12 simps) |
| `mathlib4::Cube.insertAt_boundary` | 0 | 0 | 0 | none |
| `mathlib4::SeparationQuotient.uniformContinuous_dom₂` | 0 | 0 | 0 | none |
| `mathlib4::GroupExtension.Section.mul_inv_mul_mul_mem_range_inl` | 0 | 0 | 0 | none |
| `mathlib4::GenContFract.exists_s_b_of_partDen` | 0 | 0 | 0 | none |
| `mathlib4::SimpleGraph.EdgeLabeling.TopEdgeLabeling.toTopEdgeLabeling_labelGraph` | 3 | 2 | 1 | `hammer_core_plus_learned16` (9 facts, 0 simps) |
| `mathlib4::PadicInt.PadicInt.mahlerSeries_apply` | 0 | 0 | 0 | none |
| `mathlib4::Mathlib.Tactic.FieldSimp.NF.eval_cons_mul_eval_cons_neg` | 0 | 0 | 0 | none |
| `mathlib4::Set.image2_iUnion₂_right` | 3 | 2 | 1 | `hammer_core_plus_learned16` (19 facts, 0 simps) |
| `mathlib4::MonoidAlgebra.LaurentPolynomial.comul_T` | 0 | 0 | 0 | none |
| `mathlib4::Nat.range_eq_Icc_zero_sub_one` | 0 | 0 | 0 | none |
| `mathlib4::Matrix.blockDiagonal_add` | 0 | 0 | 0 | none |
| `mathlib4::Nat.Partrec.Nat.Partrec.Code.Nat.Partrec.Code.Nat.Partrec.Code.eval_prec_zero` | 0 | 0 | 0 | none |
| `mathlib4::EuclideanGeometry.angle_midpoint_eq_pi` | 0 | 0 | 0 | none |
| `mathlib4::NNReal.tendsto_rpow_atTop` | 0 | 0 | 0 | none |
| `mathlib4::Subgroup.Commensurable.commensurable_inv` | 0 | 0 | 0 | none |
| `mathlib4::RatFunc.InftyValuation.map_mul'` | 2 | 2 | 0 | `aesop_core_plus_learned` (10 facts, 9 simps) |

## Availability

| Goal | Checked | Available | Failed |
|---|---:|---:|---:|
| `mathlib4::Submodule.mem_ideal_smul_span_iff_exists_sum'` | 32 | 17 | 15 |
| `mathlib4::equicontinuousWithinAt_iInf_rng` | 34 | 24 | 10 |
| `mathlib4::rTensorHomEquivHomRTensor_apply` | 33 | 22 | 11 |
| `mathlib4::CharTwo.add_self_eq_zero` | 33 | 6 | 27 |
| `mathlib4::MvPowerSeries.coeff_mul_prod_one_sub_of_lt_order` | 32 | 24 | 8 |
| `mathlib4::Matrix.sum_mulVec_of_mem_colStochastic` | 33 | 22 | 11 |
| `mathlib4::continuousWithinAt_singleton` | 32 | 5 | 27 |
| `mathlib4::Ideal.span_singleton_mul_right_unit` | 33 | 21 | 12 |
| `mathlib4::LightCondensed.free_lightProfinite_internallyProjective_iff_tensor_condition'` | 34 | 34 | 0 |
| `mathlib4::Fin.finsetImage_val_Ici` | 32 | 19 | 13 |
| `mathlib4::InnerProductGeometry.sin_angle_sub_mul_norm_of_inner_eq_zero` | 33 | 31 | 2 |
| `mathlib4::Real.smul_map_volume_mul_right` | 33 | 33 | 0 |
| `mathlib4::MeasureTheory.average_const` | 32 | 22 | 10 |
| `mathlib4::CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | 34 | 20 | 14 |
| `mathlib4::Finset.insert_Ioc_sub_one_right_eq_Ioc` | 33 | 15 | 18 |
| `mathlib4::Set.preimage_iInter` | 32 | 16 | 16 |
| `mathlib4::Matrix.dotProductᵣ_eq` | 32 | 14 | 18 |
| `mathlib4::Multiset.filter_cons` | 34 | 25 | 9 |
| `mathlib4::NormedAddCommGroup.summable_imp_tendsto_of_complete` | 32 | 17 | 15 |
| `mathlib4::Matrix.J_transpose` | 33 | 15 | 18 |
| `mathlib4::CategoryTheory.Adjunction.Equivalence.isAccessibleCategory` | 32 | 16 | 16 |
| `mathlib4::IsFoelner.isFoelner_iff_tendsto` | 32 | 24 | 8 |
| `mathlib4::Measurable.setLIntegral_kernel_prod_right` | 32 | 14 | 18 |
| `mathlib4::MvPolynomial.MvPolynomial.rename_comp_toMvPolynomial` | 32 | 25 | 7 |
| `mathlib4::CHSH_id` | 32 | 5 | 27 |
| `mathlib4::UpperSet.LowerSet.lowerClosure_prod` | 32 | 25 | 7 |
| `mathlib4::Nat.Primes.PNat.Prime.ne_one` | 33 | 7 | 26 |
| `mathlib4::SimpleGraph.ediam_eq_top_iff_radius_eq_top` | 33 | 23 | 10 |
| `mathlib4::Polynomial.mul_X_add_natCast_comp` | 33 | 25 | 8 |
| `mathlib4::Finset.biUnion_inter` | 32 | 21 | 11 |
| `mathlib4::CFC.monotone_rpow` | 33 | 22 | 11 |
| `mathlib4::isMinOn_Ioi_of_deriv` | 34 | 27 | 7 |
| `mathlib4::ProbabilityTheory.IdentDistrib.memLp_snd` | 32 | 20 | 12 |
| `mathlib4::Set.Finset.maximal_iff_forall_insert` | 32 | 16 | 16 |
| `mathlib4::HasStrictFDerivAt.hasStrictFDerivAt_implicitFunctionOfProdDomain` | 34 | 21 | 13 |
| `mathlib4::Finsupp.linearCombination_restrict` | 32 | 23 | 9 |
| `mathlib4::IsMulFreimanIso.mul_eq_mul` | 32 | 9 | 23 |
| `mathlib4::Multiset.card_coe` | 33 | 24 | 9 |
| `mathlib4::AddChar.to_mulShift_inj_of_isPrimitive` | 32 | 14 | 18 |
| `mathlib4::AddChar.zmod_char_primitive_of_eq_one_only_at_zero` | 32 | 16 | 16 |
| `mathlib4::HomologicalComplex₂.totalAux.totalAux.ι_D₂` | 32 | 9 | 23 |
| `mathlib4::Localization.fg` | 34 | 18 | 16 |
| `mathlib4::IntermediateField.Normal.minpoly_eq_iff_mem_orbit` | 32 | 21 | 11 |
| `mathlib4::IsTranscendenceBasis.mvPolynomial'` | 32 | 13 | 19 |
| `mathlib4::Nat.fermatNumber_strictMono` | 32 | 9 | 23 |
| `mathlib4::Affine.Simplex.face_restrict` | 33 | 22 | 11 |
| `mathlib4::HomologicalComplex.comp_pOpcycles_eq_zero_iff_up_to_refinements` | 33 | 13 | 20 |
| `mathlib4::IsCyclotomicExtension.adjoin_roots_cyclotomic_eq_adjoin_nth_roots` | 34 | 29 | 5 |
| `mathlib4::CategoryTheory.NatTrans.app_sum` | 32 | 9 | 23 |
| `mathlib4::WeierstrassCurve.Jacobian.addY_neg` | 36 | 25 | 11 |
| `mathlib4::TopCat.pullbackIsoProdSubtype_inv_snd` | 32 | 21 | 11 |
| `mathlib4::Finset.Fin.prod_Ioo_cast` | 33 | 18 | 15 |
| `mathlib4::CategoryTheory.MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft` | 32 | 8 | 24 |
| `mathlib4::Nat.frequently_atTop_modEq_one` | 33 | 21 | 12 |
| `mathlib4::Subalgebra.IsAlgebraic.tower_top_of_subalgebra_le` | 32 | 17 | 15 |
| `mathlib4::Ideal.height_le_ringKrullDim_of_isPrime` | 33 | 18 | 15 |
| `mathlib4::Real.sign_apply_eq` | 32 | 6 | 26 |
| `mathlib4::Equiv.Perm.apply_mem_support` | 33 | 10 | 23 |
| `mathlib4::Multiset.Subset.ndinter_eq_left` | 33 | 33 | 0 |
| `mathlib4::CategoryTheory.Core.Functor.Iso.coreWhiskerLeft` | 32 | 12 | 20 |
| `mathlib4::AlgebraicGeometry.Scheme.mem_overGrothendieckTopology` | 33 | 15 | 18 |
| `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom` | 32 | 18 | 14 |
| `mathlib4::classifyingSpaceUniversalCover.Rep.standardComplex.d_of` | 32 | 25 | 7 |
| `mathlib4::Submodule.restrictScalars_sInf` | 32 | 14 | 18 |
| `mathlib4::map_le_lineMap_iff_slope_le_slope_left` | 33 | 21 | 12 |
| `mathlib4::contMDiffAt_iff_source` | 33 | 9 | 24 |
| `mathlib4::CategoryTheory.ObjectProperty.trW_of_op` | 33 | 10 | 23 |
| `mathlib4::Nat.Function.Involutive.Even.neg_one_zpow` | 33 | 31 | 2 |
| `mathlib4::intervalIntegral.FTCFilter.integral_hasStrictDerivAt_left` | 32 | 6 | 26 |
| `mathlib4::Filter.blimsup_eq_iInf_biSup_of_nat` | 32 | 18 | 14 |
| `mathlib4::WeierstrassCurve.Projective.polynomialY_eq` | 32 | 13 | 19 |
| `mathlib4::Submodule.Submodule.Submodule.Submodule.Submodule.LinearMap.map_restrict` | 32 | 30 | 2 |
| `mathlib4::NumberField.InfinitePlace.IsUnramified.of_restrictScalars` | 35 | 25 | 10 |
| `mathlib4::Nat.count_le_card` | 33 | 21 | 12 |
| `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.TaggedPrepartition.forall_mem_single` | 32 | 22 | 10 |
| `mathlib4::IsUltrametricDist.norm_tprod_le_of_forall_le_of_nonneg` | 32 | 20 | 12 |
| `mathlib4::Filter.IsBoundedUnder.mono_le` | 32 | 11 | 21 |
| `mathlib4::Matroid.eRk_le_eRank` | 33 | 14 | 19 |
| `mathlib4::Equiv.Perm.VectorsProdEqOne.filter_parts_partition_eq_cycleType` | 33 | 25 | 8 |
| `mathlib4::HurwitzZeta.differentiableAt_completedHurwitzZetaEven` | 34 | 19 | 15 |
| `mathlib4::WeierstrassCurve.j_eq_zero_iff'` | 33 | 20 | 13 |
| `mathlib4::Matroid.uniqueBaseOn_self` | 32 | 14 | 18 |
| `mathlib4::Multiset.revzip_powersetAux'` | 32 | 21 | 11 |
| `mathlib4::MeasureTheory.Measure.AbsolutelyContinuous.add_right'` | 33 | 8 | 25 |
| `mathlib4::SSet.Truncated.HomotopicR.symm` | 34 | 7 | 27 |
| `mathlib4::RingHom.CodescendsAlong.includeRight` | 32 | 10 | 22 |
| `mathlib4::Wbtw.dist_add_dist` | 32 | 16 | 16 |
| `mathlib4::Ordnode.size_balance'` | 33 | 25 | 8 |
| `mathlib4::Module.Basis.Module.rank_zero_iff_of_free` | 32 | 16 | 16 |
| `mathlib4::CategoryTheory.ObjectProperty.SerreClassLocalization.inverseImage_monomorphisms` | 33 | 25 | 8 |
| `mathlib4::Finset.max'_singleton` | 33 | 21 | 12 |
| `mathlib4::Set.exists_eq_singleton_iff_nonempty_subsingleton` | 32 | 11 | 21 |
| `mathlib4::EReal.mul_div_cancel` | 33 | 32 | 1 |
| `mathlib4::Multiset.disjoint_add_left` | 33 | 21 | 12 |
| `mathlib4::Ordnode.emem_iff_mem_toList` | 32 | 19 | 13 |
| `mathlib4::borel_eq_generateFrom_Ico` | 33 | 33 | 0 |
| `mathlib4::Mathlib.Tactic.Algebra.rat_ofNat_smul_1` | 33 | 17 | 16 |
| `mathlib4::AlgebraicIndependent.lift_trdeg_le_of_injective` | 32 | 15 | 17 |
| `mathlib4::Polynomial.evalEval_intCast` | 33 | 19 | 14 |
| `mathlib4::Cube.insertAt_boundary` | 32 | 6 | 26 |
| `mathlib4::SeparationQuotient.uniformContinuous_dom₂` | 33 | 15 | 18 |
| `mathlib4::GroupExtension.Section.mul_inv_mul_mul_mem_range_inl` | 32 | 11 | 21 |
| `mathlib4::GenContFract.exists_s_b_of_partDen` | 33 | 7 | 26 |
| `mathlib4::SimpleGraph.EdgeLabeling.TopEdgeLabeling.toTopEdgeLabeling_labelGraph` | 32 | 18 | 14 |
| `mathlib4::PadicInt.PadicInt.mahlerSeries_apply` | 32 | 14 | 18 |
| `mathlib4::Mathlib.Tactic.FieldSimp.NF.eval_cons_mul_eval_cons_neg` | 35 | 8 | 27 |
| `mathlib4::Set.image2_iUnion₂_right` | 33 | 21 | 12 |
| `mathlib4::MonoidAlgebra.LaurentPolynomial.comul_T` | 33 | 18 | 15 |
| `mathlib4::Nat.range_eq_Icc_zero_sub_one` | 32 | 9 | 23 |
| `mathlib4::Matrix.blockDiagonal_add` | 33 | 18 | 15 |
| `mathlib4::Nat.Partrec.Nat.Partrec.Code.Nat.Partrec.Code.Nat.Partrec.Code.eval_prec_zero` | 32 | 13 | 19 |
| `mathlib4::EuclideanGeometry.angle_midpoint_eq_pi` | 32 | 24 | 8 |
| `mathlib4::NNReal.tendsto_rpow_atTop` | 33 | 31 | 2 |
| `mathlib4::Subgroup.Commensurable.commensurable_inv` | 33 | 21 | 12 |
| `mathlib4::RatFunc.InftyValuation.map_mul'` | 33 | 17 | 16 |

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
