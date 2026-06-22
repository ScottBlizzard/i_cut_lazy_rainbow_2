# Mathlib 4.30 Pre-Theorem Original-Tactic Probe

- Verdict: `pass`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_clean_trace_subset_500.jsonl`
- Goals checked: 100
- Original tactic replay verified: 48

## Status Counts

| Status | Count |
|---|---:|
| `unknown_identifier` | 22 |
| `type_mismatch` | 11 |
| `simp_fail` | 2 |
| `verified` | 48 |
| `tactic_fail` | 5 |
| `rewrite_fail` | 4 |
| `invalid_source_span` | 2 |
| `typeclass_or_inference` | 6 |

## Results

| Goal | Status | Time |
|---|---|---:|
| `mathlib4::Submodule.Module.Finite.of_equiv_equiv` | `unknown_identifier` | 6.27s |
| `mathlib4::finsum_mem_mul` | `type_mismatch` | 14.45s |
| `mathlib4::AlgebraicGeometry.HasAffineProperty.affineAnd_le_affineAnd` | `simp_fail` | 10.80s |
| `mathlib4::Ideal.IsDedekindDomain.ramificationIdx_ne_zero` | `unknown_identifier` | 6.51s |
| `mathlib4::Module.rank_tensorProduct'` | `verified` | 7.29s |
| `mathlib4::FirstOrder.Language.definableFun_const` | `verified` | 4.13s |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | `verified` | 4.67s |
| `mathlib4::Ideal.IsNoetherianRing.of_prime` | `unknown_identifier` | 3.88s |
| `mathlib4::Polynomial.splits_X_sub_C_mul_iff` | `tactic_fail` | 8.96s |
| `mathlib4::LocalizedModule.LocalizedModule.IsLocalizedModule.lift_comp` | `tactic_fail` | 22.35s |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | `verified` | 5.21s |
| `mathlib4::Matrix.Matrix.pow_eq_aeval_mod_charpoly` | `rewrite_fail` | 7.15s |
| `mathlib4::QuadraticMap.QuadraticMap.LinearMap.BilinMap.QuadraticMap.associated_comp` | `tactic_fail` | 24.06s |
| `mathlib4::Set.LeftInvOn.RightInvOn.InvOn.Function.Set.SurjOn.exists_subset_injOn_image_eq` | `unknown_identifier` | 4.95s |
| `mathlib4::tprod_setProd_singleton_right` | `type_mismatch` | 22.00s |
| `mathlib4::Set.Intersecting.insert` | `verified` | 3.04s |
| `mathlib4::HurwitzZeta.hasSum_int_hurwitzZetaOdd` | `unknown_identifier` | 6.31s |
| `mathlib4::nhds_le_of_le` | `verified` | 3.17s |
| `mathlib4::Nat.Partrec.Nat.Partrec.Code.encode_lt_pair` | `unknown_identifier` | 12.94s |
| `mathlib4::MvPolynomial.le_degrees_add_left` | `unknown_identifier` | 6.40s |
| `mathlib4::Filter.liminf_le_of_frequently_le'` | `unknown_identifier` | 5.34s |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | `verified` | 5.84s |
| `mathlib4::RingHom.FormallyUnramified.ofLocalizationSpanTarget` | `unknown_identifier` | 4.33s |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | `verified` | 7.17s |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | `verified` | 6.23s |
| `mathlib4::Sym.Sym2.card_image_diag` | `verified` | 4.23s |
| `mathlib4::CategoryTheory.MorphismProperty.ContainsIdentities.naturalityProperty.IsMultiplicative.multiplicativeClosure_eq_self` | `unknown_identifier` | 4.01s |
| `mathlib4::Ideal.height_le_iff_exists_minimalPrimes` | `type_mismatch` | 8.13s |
| `mathlib4::isChain_preimage_subtypeVal` | `verified` | 3.32s |
| `mathlib4::IsLocalRing.Module.IsLocalRing.linearCombination_bijective_of_flat` | `verified` | 22.30s |
| `mathlib4::Sym.map_id'` | `unknown_identifier` | 4.07s |
| `mathlib4::Commute.isNilpotent_mul_left_iff` | `verified` | 3.52s |
| `mathlib4::Algebra.Presentation.aeval_comp_val_eq` | `verified` | 8.51s |
| `mathlib4::Submonoid.mem_biSup_of_directedOn` | `rewrite_fail` | 6.79s |
| `mathlib4::Projectivization.logHeight_nonneg` | `verified` | 4.38s |
| `mathlib4::WeierstrassCurve.Projective.nonsingular_some` | `verified` | 8.21s |
| `mathlib4::Function.locallyFinsuppWithin.restrict_posPart` | `invalid_source_span` | 0.00s |
| `mathlib4::Ideal.injective_algebraMap_quotient_residueField` | `verified` | 9.40s |
| `mathlib4::Submodule.mem_orthogonal_singleton_iff_inner_left` | `unknown_identifier` | 11.38s |
| `mathlib4::Nat.descPochhammer_pos` | `verified` | 4.12s |
| `mathlib4::HahnSeries.HahnModule.HahnSeries.orderTop_self_sub_one_pos_iff` | `rewrite_fail` | 22.24s |
| `mathlib4::Rep.groupHomology.inhomogeneousChains.iCycles_mk` | `verified` | 8.83s |
| `mathlib4::Stream'.Seq.length_map` | `verified` | 3.85s |
| `mathlib4::Units.inv_mul_cancel_left` | `verified` | 4.03s |
| `mathlib4::CochainComplex.HomComplex.Cochain.rightUnshift_add` | `verified` | 8.17s |
| `mathlib4::CompleteLattice.IsCompactElement.directed_sSup_lt_of_lt` | `verified` | 5.32s |
| `mathlib4::SimpleGraph.Iso.edgeFinset_map` | `verified` | 5.62s |
| `mathlib4::Set.Set.eval_image_pi_of_notMem` | `simp_fail` | 4.78s |
| `mathlib4::AnalyticWithinAt.pow` | `tactic_fail` | 40.92s |
| `mathlib4::Finset.map_add_right_Ioc` | `verified` | 3.04s |
| `mathlib4::Finset.Fin.prod_Iio_castSucc` | `verified` | 11.51s |
| `mathlib4::Fintype.Finite.bddBelow_range` | `verified` | 3.47s |
| `mathlib4::Ordinal.Cardinal.Cardinal.lift_lt_beth_natCast` | `unknown_identifier` | 5.86s |
| `mathlib4::FirstOrder.Language.Term.LHom.BoundedFormula.LHom.Formula.Sentence.Formula.Theory.BoundedFormula.Formula.realize_exClosure_of_realize_equivSentence` | `unknown_identifier` | 6.30s |
| `mathlib4::AlgebraicGeometry.Scheme.Pullback.Triplet.snd_SpecTensorTo_apply` | `verified` | 7.84s |
| `mathlib4::AddCircle.MeasureTheory.fourierBasis_repr` | `verified` | 9.64s |
| `mathlib4::InnerProductGeometry.angle_smul_smul` | `unknown_identifier` | 5.75s |
| `mathlib4::MellinConvergent.cpow_smul` | `verified` | 7.57s |
| `mathlib4::gronwallBound_mono` | `tactic_fail` | 7.22s |
| `mathlib4::MeasureTheory.isTightMeasureSet_iff_inner_tendsto` | `unknown_identifier` | 5.68s |
| `mathlib4::DerivedCategory.isGE_iff` | `typeclass_or_inference` | 4.42s |
| `mathlib4::ContinuousMap.norm_smul_const` | `verified` | 9.13s |
| `mathlib4::PMF.mem_support_seq_iff` | `verified` | 4.62s |
| `mathlib4::LinearMap.BilinForm.dualSubmodule_dualSubmodule_of_basis` | `typeclass_or_inference` | 6.45s |
| `mathlib4::NNReal.ENNReal.tendsto_nat_floor_div_atTop` | `verified` | 6.22s |
| `mathlib4::Set.ite_inter_self` | `invalid_source_span` | 0.00s |
| `mathlib4::rTensor.inverse_comp_rTensor` | `verified` | 11.68s |
| `mathlib4::ZSpan.discreteTopology_pi_basisFun` | `type_mismatch` | 17.11s |
| `mathlib4::Subgroup.mem_centralizer_iff_commutator_eq_one'` | `type_mismatch` | 4.53s |
| `mathlib4::Set.sInter_eq_biInter` | `rewrite_fail` | 5.72s |
| `mathlib4::differentiableAt_comp_sub` | `type_mismatch` | 28.11s |
| `mathlib4::LinearEquiv.transvection.det_eq_one` | `verified` | 9.82s |
| `mathlib4::NumberField.canonicalEmbedding.NumberField.mixedEmbedding.span_idealLatticeBasis` | `typeclass_or_inference` | 19.99s |
| `mathlib4::WithTop.denselyOrdered_iff` | `type_mismatch` | 14.22s |
| `mathlib4::AlgebraicGeometry.IsZariskiLocalAtTarget.IsZariskiLocalAtSource.AffineTargetMorphismProperty.IsStableUnderBaseChange.mk` | `verified` | 6.24s |
| `mathlib4::SkewMonoidAlgebra.sum_mul` | `verified` | 19.68s |
| `mathlib4::MeasureTheory.Measure.integral_isMulLeftInvariant_isMulRightInvariant_combo` | `type_mismatch` | 15.51s |
| `mathlib4::Ordinal.mul_eq_right_iff_opow_omega0_dvd` | `unknown_identifier` | 3.50s |
| `mathlib4::StandardEtalePair.Algebra.IsStandardEtale.of_surjective` | `typeclass_or_inference` | 20.02s |
| `mathlib4::Ideal.ramificationIdx'_pos` | `unknown_identifier` | 5.81s |
| `mathlib4::KaehlerDifferential.ker_map_of_surjective` | `typeclass_or_inference` | 32.35s |
| `mathlib4::Set.preimage_mul_preimage_subset` | `verified` | 11.17s |
| `mathlib4::Real.NNReal.Real.rpow_add_rpow_le_add` | `verified` | 5.16s |
| `mathlib4::mem_balancedCore_iff` | `verified` | 5.16s |
| `mathlib4::HomotopicalAlgebra.PrepathObject.symm_p` | `verified` | 5.33s |
| `mathlib4::tendsto_arithGeom_atTop_of_one_lt` | `verified` | 4.41s |
| `mathlib4::Module.FinitePresentation.exists_fin` | `type_mismatch` | 15.37s |
| `mathlib4::UniqueMul.set_subsingleton` | `type_mismatch` | 8.48s |
| `mathlib4::SimpleGraph.Iso.minDegree_eq` | `typeclass_or_inference` | 5.75s |
| `mathlib4::Monoid.exponent_eq_iSup_orderOf` | `unknown_identifier` | 7.20s |
| `mathlib4::Rat.intCast_div` | `verified` | 3.11s |
| `mathlib4::Algebra.FormallySmooth.adjoin_of_algebraicIndependent` | `verified` | 4.92s |
| `mathlib4::Algebra.FormallySmooth.exists_adicCompletionEvalOneₐ_comp_eq` | `verified` | 5.19s |
| `mathlib4::MeasureTheory.Measure.restrict_apply₀'` | `verified` | 7.53s |
| `mathlib4::Finset.subset_biUnion_of_mem` | `verified` | 3.56s |
| `mathlib4::MeasureTheory.Measure.InnerRegularWRT.exists_subset_lt_add` | `unknown_identifier` | 6.10s |
| `mathlib4::IsCoprime.intCast` | `type_mismatch` | 4.20s |
| `mathlib4::MulAction.IsPretransitive.t1Space_iff` | `verified` | 11.83s |
| `mathlib4::Finset.map_ofDual_max` | `unknown_identifier` | 4.69s |
| `mathlib4::Polynomial.irreducible_iff_roots_eq_zero_of_degree_le_three` | `unknown_identifier` | 4.02s |

## Readout

- At least one cleaned traced theorem can be replayed in the original Mathlib 4.30 file context, so corpus migration is not globally broken.
- Remaining negative Hammer results should be debugged as action/premise/backend limitations on the replayable subset.
