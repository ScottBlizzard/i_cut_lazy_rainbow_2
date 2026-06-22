# Phase 3 Imported-Core Bridge Replay

> Bridge success means trace-core proof-core recovery plus successful replay of the original traced tactic script in a real Lean process.

- Replay goals: 200
- Replay success: 124/200 (62.0%)
- Trace result: `/workspace/thymic_project/paper/iclr_2/outputs/phase3_final_guardrail_eval_500_a40.json`
- Replay result: `/workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_200.json`

| Policy | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|---:|
| `learned_expansion` | 200 | 60.0% | 38.5% | 24.5% | 72.8 |
| `learned_base_fallback` | 200 | 67.5% | 44.5% | 33.1% | 69.9 |
| `rule_far_learned_second_stage` | 200 | 81.0% | 52.5% | 44.6% | 66.2 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 200 | 81.5% | 53.5% | 46.0% | 66.2 |

## Key Delta

- Bridge verified delta, second-stage minus fallback: +8.0 points
- Bridge FFR delta, second-stage minus fallback: +11.5 points
- Avg premise delta, second-stage minus fallback: -3.6
- Bridge verified delta, final-base8 minus fallback: +9.0 points
- Bridge FFR delta, final-base8 minus fallback: +12.9 points
- Avg premise delta, final-base8 minus fallback: -3.6

## Replay Status Counts

- Overall: {'verified': 124, 'lean_error': 76}
- By category: {'second_stage_over_fallback': 34, 'second_stage_over_expansion': 30, 'fallback_over_second_stage': 6, 'both_fail': 31, 'both_success': 20, 'fallback_fill': 79}

## Category-Level Replay

| Category | Goals | Replay verified |
|---|---:|---:|
| `both_fail` | 31 | 48.4% |
| `both_success` | 20 | 65.0% |
| `fallback_fill` | 79 | 67.1% |
| `fallback_over_second_stage` | 6 | 33.3% |
| `second_stage_over_expansion` | 30 | 70.0% |
| `second_stage_over_fallback` | 34 | 58.8% |

## Failed Replay Examples

- `BoxIntegral.hasIntegral_GP_pderiv` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/BoxIntegral__hasIntegral_GP_pderiv.lean:166:62: error(lean.unknownIdentifier): Unknown identifier `Hc` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/BoxIntegral__hasIntegral_GP_pderiv.lean:170:17: error(lean.unknownIdentifier): Unknown identifier `x` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/BoxIntegral__hasIntegral_GP_pderiv.lean:171:13: error(lean.un
- `MeasureTheory.Measure.Measure.isProjectiveLimit_infinitePiNat` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/MeasureTheory__Measure__Measure__isProjectiveLimit_infinitePiNat.lean:211:0: error: unsolved goals case hf X : ℕ → Type u_1 mX : (n : ℕ) → MeasurableSpace (X n) μ : (n : ℕ) → Measure (X n) hμ : ∀ (n : ℕ), IsProbabilityMeasure (μ n) I : Finset ℕ ⊢ Measurable (frestrictLe (I.sup id))  case hg X : ℕ → Type u_1 mX : (n : ℕ) → MeasurableSpace (X n) μ : (n : ℕ) → Measure (X n) hμ : ∀ (n : ℕ), IsProbabilityMeasure (μ n) I : F
- `ProbabilityTheory.Kernel.measurable_rnDerivAux` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/ProbabilityTheory__Kernel__measurable_rnDerivAux.lean:123:6: error(lean.unknownIdentifier): Unknown identifier `h_eq` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/ProbabilityTheory__Kernel__measurable_rnDerivAux.lean:118:0: error: unsolved goals case pos α : Type u_1 γ : Type u_2 mα : MeasurableSpace α mγ : MeasurableSpace γ hαγ : MeasurableSpace.CountableOrCountablyGenerated α γ κ η : 
- `compl_riemannZetaZeros_mem_codiscrete` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/compl_riemannZetaZeros_mem_codiscrete.lean:55:2: error: `grind` failed case grind this : ∀ (x : ℂ), ¬x = 1 → ({1}ᶜ ∩ riemannZetaZeros)ᶜ ∈ nhdsWithin x {x}ᶜ x : ℂ hx : x ≠ 1 h : riemannZetaZerosᶜ ∉ nhdsWithin x {x}ᶜ ⊢ False [grind] Goal diagnostics   [facts] Asserted facts     [prop] ∀ (x : ℂ), ¬x = 1 → ({1}ᶜ ∩ riemannZetaZeros)ᶜ ∈ nhdsWithin x {x}ᶜ     [prop] ¬x = 1     [prop] riemannZetaZerosᶜ ∉ nhdsWithin x {x}ᶜ     
- `SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/SSet__horn₂₀__horn₂₁__horn₂₂__horn__IsCompatible__horn₃₁__ι₂_desc.lean:319:0: error: unsolved goals X : SSet f₀ f₂ f₃ : Δ[2] ⟶ X h₁₂ : stdSimplex.δ 2 ≫ f₀ = stdSimplex.δ 0 ≫ f₃ h₁₃ : stdSimplex.δ 1 ≫ f₀ = stdSimplex.δ 0 ≫ f₂ h₂₃ : stdSimplex.δ 2 ≫ f₂ = stdSimplex.δ 2 ≫ f₃ ⊢ horn.faceι 1 2 ι₂._proof_1 ≫ desc f₀ f₂ f₃ h₁₂ h₁₃ h₂₃ = (stdSimplex.faceSingletonComplIso 2).inv ≫ f₂  warning: batteries: repository '/root/.cach
- `associatedPrimes.finite` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/associatedPrimes__finite.lean:162:2: error: `simp` made no progress  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `MvPowerSeries.coeff_prod` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/MvPowerSeries__coeff_prod.lean:671:2: error: `simp` made no progress  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `Nat.Nat.prime_of_pow_sub_one_prime` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/Nat__Nat__prime_of_pow_sub_one_prime.lean:207:8: error(lean.unknownIdentifier): Unknown identifier `ha2`  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `MeasureTheory.Egorov.measure_notConvergentSeq_tendsto_zero` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/MeasureTheory__Egorov__measure_notConvergentSeq_tendsto_zero.lean:83:8: error(lean.synthInstanceFailed): failed to synthesize instance of type class   Nonempty ι  Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command. /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/MeasureTheory__Egorov__measure_notConvergentSeq_tendsto_z
- `Polynomial.splits_X_sub_C_mul_iff` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/Polynomial__splits_X_sub_C_mul_iff.lean:435:47: error: Application type mismatch: The argument   hf₀ has type   f = 0 but is expected to have type   ?m.95 ≠ 0 in the application   mul_ne_zero (X_sub_C_ne_zero ?m.99) hf₀ /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_200/Polynomial__splits_X_sub_C_mul_iff.lean:430:0: error: unsolved goals case pos R : Type u_1 inst✝¹ : CommRing R f : R[X] inst
