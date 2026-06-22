# Phase 3 Bridge Failure Taxonomy

This report separates real Lean replay failures from premise-selection misses on the 100-goal Phase 3 bridge subset.

## Summary

- Bridge goals: 100
- Replay verified: 59/100 (59.0%)
- Second-stage gains over fallback supported by replay: 20
- Second-stage gains over expansion supported by replay: 23
- Replay-verified goals missed by second-stage trace-core: 12
- Second-stage trace-core successes blocked by replay failure: 25

## Policy-Level Misses

| Policy | Goals | Trace success | Bridge verified | Replay-verified trace miss | Avg premises |
|---|---:|---:|---:|---:|---:|
| `learned_rerank` | 100 | 14.0% | 11.0% | 48 | 56.0 |
| `learned_expansion` | 100 | 37.0% | 24.0% | 35 | 88.0 |
| `rule_far_learned` | 100 | 39.0% | 25.0% | 34 | 88.0 |
| `learned_base_fallback` | 100 | 45.0% | 31.0% | 28 | 82.2 |
| `rule_far_learned_failure_specific` | 100 | 45.0% | 31.0% | 28 | 82.3 |
| `rule_far_learned_second_stage` | 100 | 72.0% | 47.0% | 12 | 79.4 |
| `rule_far_full` | 100 | 47.0% | 27.0% | 32 | 88.3 |

## Primary Replay Failure Taxonomy

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 59 | 59.0% |
| `replay_unknown_identifier` | 15 | 15.0% |
| `replay_other_lean_error` | 7 | 7.0% |
| `replay_unsolved_goals` | 5 | 5.0% |
| `replay_simp_no_progress` | 5 | 5.0% |
| `replay_typeclass` | 3 | 3.0% |
| `replay_type_mismatch` | 3 | 3.0% |
| `replay_tactic_failed` | 2 | 2.0% |
| `replay_sorry_context` | 1 | 1.0% |

## Multi-Label Replay Failure Signals

| Signal | Count |
|---|---:|
| `replay_verified` | 59 |
| `replay_unknown_identifier` | 15 |
| `replay_unsolved_goals` | 10 |
| `replay_simp_no_progress` | 7 |
| `replay_other_lean_error` | 7 |
| `replay_type_mismatch` | 6 |
| `replay_typeclass` | 4 |
| `replay_sorry_context` | 4 |
| `replay_tactic_failed` | 2 |

## Primary Failure By Bridge Category

### `both_fail`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 8 | 40.0% |
| `replay_unknown_identifier` | 7 | 35.0% |
| `replay_other_lean_error` | 2 | 10.0% |
| `replay_typeclass` | 2 | 10.0% |
| `replay_tactic_failed` | 1 | 5.0% |

### `both_success`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 8 | 80.0% |
| `replay_other_lean_error` | 1 | 10.0% |
| `replay_simp_no_progress` | 1 | 10.0% |

### `fallback_fill`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 6 | 85.7% |
| `replay_type_mismatch` | 1 | 14.3% |

### `fallback_over_second_stage`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 4 | 50.0% |
| `replay_unknown_identifier` | 3 | 37.5% |
| `replay_unsolved_goals` | 1 | 12.5% |

### `second_stage_over_expansion`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 13 | 65.0% |
| `replay_other_lean_error` | 3 | 15.0% |
| `replay_simp_no_progress` | 1 | 5.0% |
| `replay_unsolved_goals` | 1 | 5.0% |
| `replay_type_mismatch` | 1 | 5.0% |
| `replay_sorry_context` | 1 | 5.0% |

### `second_stage_over_fallback`

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 20 | 57.1% |
| `replay_unknown_identifier` | 5 | 14.3% |
| `replay_unsolved_goals` | 3 | 8.6% |
| `replay_simp_no_progress` | 3 | 8.6% |
| `replay_typeclass` | 1 | 2.9% |
| `replay_tactic_failed` | 1 | 2.9% |
| `replay_other_lean_error` | 1 | 2.9% |
| `replay_type_mismatch` | 1 | 2.9% |

## Key Positive Cases

- Replay-verified second-stage-over-fallback cases: 20
- `SimpleGraph.ediam_eq_top_iff_radius_eq_top` (second_stage_over_fallback)
- `DiscreteUniformity.eq_pure_of_cauchy` (second_stage_over_fallback)
- `IntermediateField.Lifts.exists_algHom_adjoin_of_splits_of_aeval` (second_stage_over_fallback)
- `EuclideanGeometry.Sphere.dist_orthogonalProjection_eq_radius_iff_isTangentAt` (second_stage_over_fallback)
- `LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` (second_stage_over_fallback)
- `CategoryTheory.Arrow.mk_eq_mk_iff` (second_stage_over_fallback)
- `MonoidAlgebra.LaurentPolynomial.comul_T` (second_stage_over_fallback)
- `RestrictedProduct.isOpen_forall_mem` (second_stage_over_fallback)
- `NumberField.InfinitePlace.IsUnramified.of_restrictScalars` (second_stage_over_fallback)
- `CategoryTheory.ObjectProperty.triangEnvelopeIter_add'` (second_stage_over_fallback)
- `Seminorm.ball_sup` (second_stage_over_fallback)
- `Complex.HadamardThreeLines.norm_mul_invInterpStrip_le_one_of_mem_verticalClosedStrip` (second_stage_over_fallback)
- `LightCondensed.internallyProjective_iff_tensor_condition` (second_stage_over_fallback)
- `CategoryTheory.IsPullback.IsPushout.Limits.preservesLimitsOfShape_walkingCospan_of_forall_isPullback` (second_stage_over_fallback)
- `Mathlib.Tactic.Algebra.rat_ofNat_smul_1` (second_stage_over_fallback)

## Key Negative Cases

### Replay verified, but second-stage trace-core failed

- `WeierstrassCurve.Jacobian.neg_of_Z_ne_zero` (fallback_over_second_stage), fallback_solved=True, expansion_solved=False
- `Multiset.Subset.ndinter_eq_left` (fallback_over_second_stage), fallback_solved=True, expansion_solved=False
- `equicontinuousWithinAt_iInf_rng` (fallback_over_second_stage), fallback_solved=True, expansion_solved=False
- `Nat.Primes.PNat.Prime.ne_one` (fallback_over_second_stage), fallback_solved=True, expansion_solved=False
- `HasProd.mul_disjoint` (both_fail), fallback_solved=False, expansion_solved=False
- `FermatLastTheoremForThreeGen.Solution.associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b` (both_fail), fallback_solved=False, expansion_solved=False
- `WeierstrassCurve.Jacobian.addY_neg` (both_fail), fallback_solved=False, expansion_solved=False
- `tendsto_arithGeom_atTop_of_one_lt` (both_fail), fallback_solved=False, expansion_solved=False
- `SSet.Truncated.HomotopicR.symm` (both_fail), fallback_solved=False, expansion_solved=False
- `WeierstrassCurve.Projective.nonsingular_some` (both_fail), fallback_solved=False, expansion_solved=False
- `Rat.intCast_div` (both_fail), fallback_solved=False, expansion_solved=False
- `Polynomial.Splits.monomial` (both_fail), fallback_solved=False, expansion_solved=False

### Second-stage trace-core succeeded, but replay failed

- `Asymptotics.isLittleOTVS_iff_isLittleO` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/Asymptotics__isLittleOTVS_iff_isLittleO.lean:770:35: error(lean.unknownIdentifier): Unknown identifier `this` warning: batteries: repository '/root/.cache/lean...
- `Polynomial.splits_X_sub_C_mul_iff` (second_stage_over_fallback): `replay_unsolved_goals`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/Polynomial__splits_X_sub_C_mul_iff.lean:435:47: error: Application type mismatch: The argument hf₀ has type f = 0 but is expected to have type ?m.95 ≠ 0 in the...
- `MvPowerSeries.coeff_prod` (second_stage_over_fallback): `replay_simp_no_progress`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/MvPowerSeries__coeff_prod.lean:671:2: error: `simp` made no progress warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1...
- `SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc` (second_stage_over_fallback): `replay_unsolved_goals`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/SSet__horn₂₀__horn₂₁__horn₂₂__horn__IsCompatible__horn₃₁__ι₂_desc.lean:319:0: error: unsolved goals X : SSet f₀ f₂ f₃ : Δ[2] ⟶ X h₁₂ : stdSimplex.δ 2 ≫ f₀ = st...
- `MeasureTheory.Egorov.measure_notConvergentSeq_tendsto_zero` (second_stage_over_fallback): `replay_typeclass`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/MeasureTheory__Egorov__measure_notConvergentSeq_tendsto_zero.lean:83:8: error(lean.synthInstanceFailed): failed to synthesize instance of type class Nonempty ι...
- `compl_riemannZetaZeros_mem_codiscrete` (second_stage_over_fallback): `replay_tactic_failed`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/compl_riemannZetaZeros_mem_codiscrete.lean:55:2: error: `grind` failed case grind this : ∀ (x : ℂ), ¬x = 1 → ({1}ᶜ ∩ riemannZetaZeros)ᶜ ∈ nhdsWithin x {x}ᶜ x :...
- `HurwitzZeta.completedHurwitzZetaEven_one_sub` (second_stage_over_fallback): `replay_simp_no_progress`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/HurwitzZeta__completedHurwitzZetaEven_one_sub.lean:368:2: error: `simp` made no progress warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathl...
- `BoxIntegral.hasIntegral_GP_pderiv` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/BoxIntegral__hasIntegral_GP_pderiv.lean:166:62: error(lean.unknownIdentifier): Unknown identifier `Hc` /workspace/thymic_project/paper/iclr_2/outputs/phase3_br...
- `ProbabilityTheory.Kernel.measurable_rnDerivAux` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/ProbabilityTheory__Kernel__measurable_rnDerivAux.lean:123:6: error(lean.unknownIdentifier): Unknown identifier `h_eq` /workspace/thymic_project/paper/iclr_2/ou...
- `MeasureTheory.Measure.Measure.isProjectiveLimit_infinitePiNat` (second_stage_over_fallback): `replay_unsolved_goals`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/MeasureTheory__Measure__Measure__isProjectiveLimit_infinitePiNat.lean:211:0: error: unsolved goals case hf X : ℕ → Type u_1 mX : (n : ℕ) → MeasurableSpace (X n...
- `ContinuousOn.if'` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/ContinuousOn__if'.lean:55:4: error(lean.unknownIdentifier): Unknown identifier `this` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files...
- `Nat.Nat.prime_of_pow_sub_one_prime` (second_stage_over_fallback): `replay_unknown_identifier`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/Nat__Nat__prime_of_pow_sub_one_prime.lean:207:8: error(lean.unknownIdentifier): Unknown identifier `ha2` warning: batteries: repository '/root/.cache/lean_dojo...
- `associatedPrimes.finite` (second_stage_over_fallback): `replay_simp_no_progress`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/associatedPrimes__finite.lean:162:2: error: `simp` made no progress warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d10...
- `Turing.TM2.TM2to1.addBottom_map` (second_stage_over_fallback): `replay_other_lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/Turing__TM2__TM2to1__addBottom_map.lean:371:2: error: Tactic `rfl` failed: The left-hand side ListBlank.map { f := Prod.snd, map_pt' := ⋯ } (addBottom L) is no...
- `NumberField.mixedEmbedding.fundamentalCone.compactSet_eq_union_aux₂` (second_stage_over_fallback): `replay_type_mismatch`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/NumberField__mixedEmbedding__fundamentalCone__compactSet_eq_union_aux₂.lean:776:2: error: Type mismatch: After simplification, term hy w₀ (Set.mem_univ w₀) has...

## Paper Interpretation

- The bridge subset supports the controller gain: replay-verified second-stage-over-fallback cases exist in substantial number.
- Many lost bridge cases are replay failures after trace-core success, so they should be treated as replay/context fragility unless deeper inspection shows premise-specific invalidity.
- The subset is disagreement-heavy; report it as bridge validation, not as a full proof reconstruction benchmark.
