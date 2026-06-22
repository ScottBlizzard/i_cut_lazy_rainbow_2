# Policy Delta Analysis

- Base policy: `learned_base_fallback`
- New policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- Goals: 100
- Same solved: 39 (39.0%)
- Same failed: 21 (21.0%)
- New-only solved: 34
- Base-only solved: 6
- Replay-verified new-only solved: 20
- Replay-verified base-only solved: 2

## New-Only Solved

- `Asymptotics.isLittleOTVS_iff_isLittleO`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `BoxIntegral.hasIntegral_GP_pderiv`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `CategoryTheory.Arrow.mk_eq_mk_iff`, replay_success=True, category=second_stage_over_fallback; base_failure=rewrite_direction, premises 96 -> 96
- `CategoryTheory.IsPullback.IsPushout.Limits.preservesLimitsOfShape_walkingCospan_of_forall_isPullback`, replay_success=True, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 87 -> 96
- `CategoryTheory.ObjectProperty.SerreClassLocalization.inverseImage_monomorphisms`, replay_success=True, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 64
- `CategoryTheory.ObjectProperty.triangEnvelopeIter_add'`, replay_success=True, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 84 -> 96
- `CharTwo.add_self_eq_zero`, replay_success=True, category=second_stage_over_fallback; base_failure=missing_bridge, premises 96 -> 64
- `Complex.HadamardThreeLines.norm_mul_invInterpStrip_le_one_of_mem_verticalClosedStrip`, replay_success=True, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 96
- `ContinuousOn.if'`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 94 -> 96
- `EuclideanGeometry.Sphere.dist_orthogonalProjection_eq_radius_iff_isTangentAt`, replay_success=True, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `Finset.Fin.prod_Iio_castSucc`, replay_success=True, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 64
- `HurwitzZeta.completedHurwitzZetaEven_one_sub`, replay_success=False, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 64
- `HurwitzZeta.differentiableAt_completedHurwitzZetaEven`, replay_success=True, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 96
- `IntermediateField.Lifts.exists_algHom_adjoin_of_splits_of_aeval`, replay_success=True, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 92 -> 96
- `LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule`, replay_success=True, category=second_stage_over_fallback; base_failure=missing_bridge, premises 95 -> 96
- `LightCondensed.internallyProjective_iff_tensor_condition`, replay_success=True, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 64
- `Mathlib.Tactic.Algebra.rat_ofNat_smul_1`, replay_success=True, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 64
- `Mathlib.Tactic.FieldSimp.NF.eval_cons_mul_eval_cons_neg`, replay_success=True, category=second_stage_over_fallback; base_failure=rewrite_direction, premises 96 -> 96
- `MeasureTheory.Egorov.measure_notConvergentSeq_tendsto_zero`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `MeasureTheory.Measure.Measure.isProjectiveLimit_infinitePiNat`, replay_success=False, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 64
- `MonoidAlgebra.LaurentPolynomial.comul_T`, replay_success=True, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `MvPowerSeries.coeff_prod`, replay_success=False, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 96
- `Nat.Nat.prime_of_pow_sub_one_prime`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `NumberField.InfinitePlace.IsUnramified.of_restrictScalars`, replay_success=True, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 96
- `NumberField.mixedEmbedding.fundamentalCone.compactSet_eq_union_aux₂`, replay_success=False, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 64
- `Polynomial.splits_X_sub_C_mul_iff`, replay_success=False, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 96
- `ProbabilityTheory.Kernel.measurable_rnDerivAux`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `RestrictedProduct.isOpen_forall_mem`, replay_success=True, category=second_stage_over_fallback; base_failure=rewrite_direction, premises 96 -> 64
- `SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `Seminorm.ball_sup`, replay_success=True, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 96 -> 96
- `SimpleGraph.ediam_eq_top_iff_radius_eq_top`, replay_success=True, category=second_stage_over_fallback; base_failure=type_mismatch, premises 96 -> 96
- `WeierstrassCurve.Jacobian.addY_neg`, replay_success=True, category=both_fail; base_failure=imported_premise_missing, premises 96 -> 96
- `associatedPrimes.finite`, replay_success=False, category=second_stage_over_fallback; base_failure=missing_bridge, premises 96 -> 64
- `compl_riemannZetaZeros_mem_codiscrete`, replay_success=False, category=second_stage_over_fallback; base_failure=imported_premise_missing, premises 93 -> 96

## Base-Only Solved

- `ENNReal.tendsto_nhds_of_Icc`, replay_success=True, category=fallback_fill; new_failure=imported_premise_missing, premises 96 -> 96
- `Equiv.succ_embeddingFinSucc_fst_symm_apply`, replay_success=False, category=fallback_over_second_stage; new_failure=imported_premise_missing, premises 69 -> 96
- `FreeGroup.IsCyclicallyReduced.reduceCyclically.reduce_flatten_replicate_succ`, replay_success=False, category=fallback_over_second_stage; new_failure=imported_premise_missing, premises 91 -> 96
- `Multiset.Subset.ndinter_eq_left`, replay_success=True, category=fallback_over_second_stage; new_failure=imported_premise_missing, premises 75 -> 96
- `MvPolynomial.isNilpotent_iff`, replay_success=False, category=fallback_over_second_stage; new_failure=imported_premise_missing, premises 74 -> 96
- `Polynomial.rootMultiplicity_eq_natTrailingDegree'`, replay_success=False, category=fallback_over_second_stage; new_failure=imported_premise_missing, premises 96 -> 96

