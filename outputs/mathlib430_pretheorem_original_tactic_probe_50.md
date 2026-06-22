# Mathlib 4.30 Pre-Theorem Original-Tactic Probe

- Verdict: `pass`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_clean_trace_subset_500.jsonl`
- Goals checked: 50
- Original tactic replay verified: 25

## Status Counts

| Status | Count |
|---|---:|
| `unknown_identifier` | 12 |
| `type_mismatch` | 3 |
| `simp_fail` | 2 |
| `verified` | 25 |
| `tactic_fail` | 4 |
| `rewrite_fail` | 3 |
| `invalid_source_span` | 1 |

## Results

| Goal | Status | Time |
|---|---|---:|
| `mathlib4::Submodule.Module.Finite.of_equiv_equiv` | `unknown_identifier` | 6.10s |
| `mathlib4::finsum_mem_mul` | `type_mismatch` | 14.33s |
| `mathlib4::AlgebraicGeometry.HasAffineProperty.affineAnd_le_affineAnd` | `simp_fail` | 10.79s |
| `mathlib4::Ideal.IsDedekindDomain.ramificationIdx_ne_zero` | `unknown_identifier` | 6.47s |
| `mathlib4::Module.rank_tensorProduct'` | `verified` | 7.28s |
| `mathlib4::FirstOrder.Language.definableFun_const` | `verified` | 4.29s |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | `verified` | 4.77s |
| `mathlib4::Ideal.IsNoetherianRing.of_prime` | `unknown_identifier` | 3.65s |
| `mathlib4::Polynomial.splits_X_sub_C_mul_iff` | `tactic_fail` | 8.86s |
| `mathlib4::LocalizedModule.LocalizedModule.IsLocalizedModule.lift_comp` | `tactic_fail` | 21.89s |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | `verified` | 5.06s |
| `mathlib4::Matrix.Matrix.pow_eq_aeval_mod_charpoly` | `rewrite_fail` | 7.06s |
| `mathlib4::QuadraticMap.QuadraticMap.LinearMap.BilinMap.QuadraticMap.associated_comp` | `tactic_fail` | 24.42s |
| `mathlib4::Set.LeftInvOn.RightInvOn.InvOn.Function.Set.SurjOn.exists_subset_injOn_image_eq` | `unknown_identifier` | 4.97s |
| `mathlib4::tprod_setProd_singleton_right` | `type_mismatch` | 22.12s |
| `mathlib4::Set.Intersecting.insert` | `verified` | 2.95s |
| `mathlib4::HurwitzZeta.hasSum_int_hurwitzZetaOdd` | `unknown_identifier` | 6.77s |
| `mathlib4::nhds_le_of_le` | `verified` | 3.29s |
| `mathlib4::Nat.Partrec.Nat.Partrec.Code.encode_lt_pair` | `unknown_identifier` | 12.78s |
| `mathlib4::MvPolynomial.le_degrees_add_left` | `unknown_identifier` | 6.47s |
| `mathlib4::Filter.liminf_le_of_frequently_le'` | `unknown_identifier` | 5.45s |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | `verified` | 5.93s |
| `mathlib4::RingHom.FormallyUnramified.ofLocalizationSpanTarget` | `unknown_identifier` | 4.41s |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | `verified` | 7.10s |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | `verified` | 6.29s |
| `mathlib4::Sym.Sym2.card_image_diag` | `verified` | 4.25s |
| `mathlib4::CategoryTheory.MorphismProperty.ContainsIdentities.naturalityProperty.IsMultiplicative.multiplicativeClosure_eq_self` | `unknown_identifier` | 4.27s |
| `mathlib4::Ideal.height_le_iff_exists_minimalPrimes` | `type_mismatch` | 8.02s |
| `mathlib4::isChain_preimage_subtypeVal` | `verified` | 3.20s |
| `mathlib4::IsLocalRing.Module.IsLocalRing.linearCombination_bijective_of_flat` | `verified` | 22.25s |
| `mathlib4::Sym.map_id'` | `unknown_identifier` | 4.03s |
| `mathlib4::Commute.isNilpotent_mul_left_iff` | `verified` | 3.51s |
| `mathlib4::Algebra.Presentation.aeval_comp_val_eq` | `verified` | 8.32s |
| `mathlib4::Submonoid.mem_biSup_of_directedOn` | `rewrite_fail` | 6.88s |
| `mathlib4::Projectivization.logHeight_nonneg` | `verified` | 4.48s |
| `mathlib4::WeierstrassCurve.Projective.nonsingular_some` | `verified` | 8.38s |
| `mathlib4::Function.locallyFinsuppWithin.restrict_posPart` | `invalid_source_span` | 0.00s |
| `mathlib4::Ideal.injective_algebraMap_quotient_residueField` | `verified` | 9.53s |
| `mathlib4::Submodule.mem_orthogonal_singleton_iff_inner_left` | `unknown_identifier` | 11.63s |
| `mathlib4::Nat.descPochhammer_pos` | `verified` | 4.37s |
| `mathlib4::HahnSeries.HahnModule.HahnSeries.orderTop_self_sub_one_pos_iff` | `rewrite_fail` | 22.20s |
| `mathlib4::Rep.groupHomology.inhomogeneousChains.iCycles_mk` | `verified` | 8.81s |
| `mathlib4::Stream'.Seq.length_map` | `verified` | 3.95s |
| `mathlib4::Units.inv_mul_cancel_left` | `verified` | 4.03s |
| `mathlib4::CochainComplex.HomComplex.Cochain.rightUnshift_add` | `verified` | 8.44s |
| `mathlib4::CompleteLattice.IsCompactElement.directed_sSup_lt_of_lt` | `verified` | 5.32s |
| `mathlib4::SimpleGraph.Iso.edgeFinset_map` | `verified` | 5.55s |
| `mathlib4::Set.Set.eval_image_pi_of_notMem` | `simp_fail` | 5.04s |
| `mathlib4::AnalyticWithinAt.pow` | `tactic_fail` | 40.15s |
| `mathlib4::Finset.map_add_right_Ioc` | `verified` | 3.05s |

## Readout

- At least one cleaned traced theorem can be replayed in the original Mathlib 4.30 file context, so corpus migration is not globally broken.
- Remaining negative Hammer results should be debugged as action/premise/backend limitations on the replayable subset.
