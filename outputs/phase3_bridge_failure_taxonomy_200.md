# Phase 3 Bridge Failure Taxonomy

This report separates real Lean replay failures from premise-selection misses on the 100-goal Phase 3 bridge subset.

## Summary

- Bridge goals: 200
- Replay verified: 124/200 (62.0%)
- Second-stage gains over fallback supported by replay: 20
- Second-stage gains over expansion supported by replay: 32
- Replay-verified goals missed by second-stage trace-core: 17
- Second-stage trace-core successes blocked by replay failure: 56

## Policy-Level Misses

| Policy | Goals | Trace success | Bridge verified | Replay-verified trace miss | Avg premises |
|---|---:|---:|---:|---:|---:|
| `learned_expansion` | 200 | 60.0% | 38.5% | 47 | 72.8 |
| `learned_base_fallback` | 200 | 67.5% | 44.5% | 35 | 69.9 |
| `rule_far_learned_second_stage` | 200 | 81.0% | 52.5% | 19 | 66.2 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 200 | 81.5% | 53.5% | 17 | 66.2 |

## Primary Replay Failure Taxonomy

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 124 | 62.0% |
| `replay_unknown_identifier` | 30 | 15.0% |
| `replay_other_lean_error` | 13 | 6.5% |
| `replay_typeclass` | 8 | 4.0% |
| `replay_unsolved_goals` | 7 | 3.5% |
| `replay_simp_no_progress` | 6 | 3.0% |
| `replay_tactic_failed` | 5 | 2.5% |
| `replay_type_mismatch` | 5 | 2.5% |
| `replay_sorry_context` | 2 | 1.0% |

## Multi-Label Replay Failure Signals

| Signal | Count |
|---|---:|
| `replay_verified` | 124 |
| `replay_unknown_identifier` | 30 |
| `replay_unsolved_goals` | 19 |
| `replay_other_lean_error` | 13 |
| `replay_typeclass` | 10 |
| `replay_type_mismatch` | 9 |
| `replay_simp_no_progress` | 8 |
| `replay_sorry_context` | 8 |
| `replay_tactic_failed` | 5 |

## Primary Failure By Bridge Category

### `both_fail`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 15 | 48.4% |
| `replay_unknown_identifier` | 8 | 25.8% |
| `replay_other_lean_error` | 4 | 12.9% |
| `replay_typeclass` | 3 | 9.7% |
| `replay_tactic_failed` | 1 | 3.2% |

### `both_success`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 13 | 65.0% |
| `replay_unknown_identifier` | 3 | 15.0% |
| `replay_sorry_context` | 1 | 5.0% |
| `replay_other_lean_error` | 1 | 5.0% |
| `replay_tactic_failed` | 1 | 5.0% |
| `replay_typeclass` | 1 | 5.0% |

### `fallback_fill`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 53 | 67.1% |
| `replay_unknown_identifier` | 11 | 13.9% |
| `replay_other_lean_error` | 5 | 6.3% |
| `replay_type_mismatch` | 3 | 3.8% |
| `replay_simp_no_progress` | 2 | 2.5% |
| `replay_unsolved_goals` | 2 | 2.5% |
| `replay_tactic_failed` | 2 | 2.5% |
| `replay_typeclass` | 1 | 1.3% |

### `fallback_over_second_stage`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_unknown_identifier` | 3 | 50.0% |
| `replay_verified` | 2 | 33.3% |
| `replay_unsolved_goals` | 1 | 16.7% |

### `second_stage_over_expansion`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 21 | 70.0% |
| `replay_other_lean_error` | 3 | 10.0% |
| `replay_typeclass` | 2 | 6.7% |
| `replay_type_mismatch` | 1 | 3.3% |
| `replay_simp_no_progress` | 1 | 3.3% |
| `replay_sorry_context` | 1 | 3.3% |
| `replay_unsolved_goals` | 1 | 3.3% |

### `second_stage_over_fallback`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 20 | 58.8% |
| `replay_unknown_identifier` | 5 | 14.7% |
| `replay_unsolved_goals` | 3 | 8.8% |
| `replay_simp_no_progress` | 3 | 8.8% |
| `replay_tactic_failed` | 1 | 2.9% |
| `replay_typeclass` | 1 | 2.9% |
| `replay_type_mismatch` | 1 | 2.9% |

## Key Positive Cases

- Replay-verified second-stage-over-fallback cases: 20
- `Finset.Fin.prod_Iio_castSucc` (second_stage_over_fallback)
- `NumberField.InfinitePlace.IsUnramified.of_restrictScalars` (second_stage_over_fallback)
- `MonoidAlgebra.LaurentPolynomial.comul_T` (second_stage_over_fallback)
- `IntermediateField.Lifts.exists_algHom_adjoin_of_splits_of_aeval` (second_stage_over_fallback)
- `CategoryTheory.IsPullback.IsPushout.Limits.preservesLimitsOfShape_walkingCospan_of_forall_isPullback` (second_stage_over_fallback)
- `LightCondensed.internallyProjective_iff_tensor_condition` (second_stage_over_fallback)
- `LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` (second_stage_over_fallback)
- `RestrictedProduct.isOpen_forall_mem` (second_stage_over_fallback)
- `SimpleGraph.ediam_eq_top_iff_radius_eq_top` (second_stage_over_fallback)
- `CategoryTheory.ObjectProperty.triangEnvelopeIter_add'` (second_stage_over_fallback)
- `Mathlib.Tactic.Algebra.rat_ofNat_smul_1` (second_stage_over_fallback)
- `CategoryTheory.ObjectProperty.SerreClassLocalization.inverseImage_monomorphisms` (second_stage_over_fallback)
- `Mathlib.Tactic.FieldSimp.NF.eval_cons_mul_eval_cons_neg` (second_stage_over_fallback)
- `EuclideanGeometry.Sphere.dist_orthogonalProjection_eq_radius_iff_isTangentAt` (second_stage_over_fallback)
- `WeierstrassCurve.Jacobian.addY_neg` (second_stage_over_fallback)

## Key Negative Cases

### Replay verified, but second-stage trace-core failed

- `Multiset.Subset.ndinter_eq_left` (fallback_over_second_stage), fallback_solved=True, expansion_solved=False
- `ENNReal.tendsto_nhds_of_Icc` (fallback_over_second_stage), fallback_solved=True, expansion_solved=True
- `FermatLastTheoremForThreeGen.Solution.associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b` (both_fail), fallback_solved=False, expansion_solved=False
- `LightCondensed.free_lightProfinite_internallyProjective_iff_tensor_condition'` (both_fail), fallback_solved=False, expansion_solved=False
- `Matrix.J_transpose` (both_fail), fallback_solved=False, expansion_solved=False
- `DiscreteUniformity.eq_pure_of_cauchy` (both_fail), fallback_solved=False, expansion_solved=True
- `tendsto_arithGeom_atTop_of_one_lt` (both_fail), fallback_solved=False, expansion_solved=False
- `Rat.intCast_div` (both_fail), fallback_solved=False, expansion_solved=False
- `SchwartzMap.lineDerivOp_fourier_eq` (both_fail), fallback_solved=False, expansion_solved=False
- `AffineSpace.StarConvex.smul_vadd_mem_of_isClosed_of_mem_asymptoticCone` (both_fail), fallback_solved=False, expansion_solved=False
- `Finset.max'_singleton` (both_fail), fallback_solved=False, expansion_solved=False
- `SimpleGraph.Walk.isHamiltonianCycle_iff_isCycle_and_length_eq` (both_fail), fallback_solved=False, expansion_solved=False
- `SSet.Truncated.HomotopicR.symm` (both_fail), fallback_solved=False, expansion_solved=False
- `WeierstrassCurve.Projective.nonsingular_some` (both_fail), fallback_solved=False, expansion_solved=False
- `Finset.sup'_product_right` (both_fail), fallback_solved=False, expansion_solved=False

### Second-stage trace-core succeeded, but replay failed

- `BoxIntegral.hasIntegral_GP_pderiv` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/BoxIntegral__hasIntegral_GP_pderiv.lean:166:62: error(lean.unknownIdentifier): Unknown identifier `Hc` /workspace/thymic_project/paper/iclr_2/outputs/phase3_br...
- `MeasureTheory.Measure.Measure.isProjectiveLimit_infinitePiNat` (second_stage_over_fallback): `replay_unsolved_goals`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/MeasureTheory__Measure__Measure__isProjectiveLimit_infinitePiNat.lean:211:0: error: unsolved goals case hf X : ℕ → Type u_1 mX : (n : ℕ) → MeasurableSpace (X n...
- `ProbabilityTheory.Kernel.measurable_rnDerivAux` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/ProbabilityTheory__Kernel__measurable_rnDerivAux.lean:123:6: error(lean.unknownIdentifier): Unknown identifier `h_eq` /workspace/thymic_project/paper/iclr_2/ou...
- `compl_riemannZetaZeros_mem_codiscrete` (second_stage_over_fallback): `replay_tactic_failed`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/compl_riemannZetaZeros_mem_codiscrete.lean:55:2: error: `grind` failed case grind this : ∀ (x : ℂ), ¬x = 1 → ({1}ᶜ ∩ riemannZetaZeros)ᶜ ∈ nhdsWithin x {x}ᶜ x :...
- `SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc` (second_stage_over_fallback): `replay_unsolved_goals`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/SSet__horn₂₀__horn₂₁__horn₂₂__horn__IsCompatible__horn₃₁__ι₂_desc.lean:319:0: error: unsolved goals X : SSet f₀ f₂ f₃ : Δ[2] ⟶ X h₁₂ : stdSimplex.δ 2 ≫ f₀ = st...
- `associatedPrimes.finite` (second_stage_over_fallback): `replay_simp_no_progress`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/associatedPrimes__finite.lean:162:2: error: `simp` made no progress warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d10...
- `MvPowerSeries.coeff_prod` (second_stage_over_fallback): `replay_simp_no_progress`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/MvPowerSeries__coeff_prod.lean:671:2: error: `simp` made no progress warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1...
- `Nat.Nat.prime_of_pow_sub_one_prime` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/Nat__Nat__prime_of_pow_sub_one_prime.lean:207:8: error(lean.unknownIdentifier): Unknown identifier `ha2` warning: batteries: repository '/root/.cache/lean_dojo...
- `MeasureTheory.Egorov.measure_notConvergentSeq_tendsto_zero` (second_stage_over_fallback): `replay_typeclass`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/MeasureTheory__Egorov__measure_notConvergentSeq_tendsto_zero.lean:83:8: error(lean.synthInstanceFailed): failed to synthesize instance of type class Nonempty ι...
- `Polynomial.splits_X_sub_C_mul_iff` (second_stage_over_fallback): `replay_unsolved_goals`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/Polynomial__splits_X_sub_C_mul_iff.lean:435:47: error: Application type mismatch: The argument hf₀ has type f = 0 but is expected to have type ?m.95 ≠ 0 in the...
- `Asymptotics.isLittleOTVS_iff_isLittleO` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/Asymptotics__isLittleOTVS_iff_isLittleO.lean:770:35: error(lean.unknownIdentifier): Unknown identifier `this` warning: batteries: repository '/root/.cache/lean...
- `NumberField.mixedEmbedding.fundamentalCone.compactSet_eq_union_aux₂` (second_stage_over_fallback): `replay_type_mismatch`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/NumberField__mixedEmbedding__fundamentalCone__compactSet_eq_union_aux₂.lean:776:2: error: Type mismatch: After simplification, term hy w₀ (Set.mem_univ w₀) has...
- `HurwitzZeta.completedHurwitzZetaEven_one_sub` (second_stage_over_fallback): `replay_simp_no_progress`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/HurwitzZeta__completedHurwitzZetaEven_one_sub.lean:368:2: error: `simp` made no progress warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathl...
- `ContinuousOn.if'` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/ContinuousOn__if'.lean:55:4: error(lean.unknownIdentifier): Unknown identifier `this` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files...
- `Ideal.height_le_iff_exists_minimalPrimes` (second_stage_over_expansion): `replay_type_mismatch`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/Ideal__height_le_iff_exists_minimalPrimes.lean:308:2: error: Type mismatch: After simplification, term Cardinal.toENat.monotone' hI has type Cardinal.toENat (S...

## Paper Interpretation

- The bridge subset supports the controller gain: replay-verified second-stage-over-fallback cases exist in substantial number.
- Many lost bridge cases are replay failures after trace-core success, so they should be treated as replay/context fragility unless deeper inspection shows premise-specific invalidity.
- The subset is disagreement-heavy; report it as bridge validation, not as a full proof reconstruction benchmark.
