# Phase 3 Imported-Core Bridge Replay

> Bridge success means trace-core proof-core recovery plus successful replay of the original traced tactic script in a real Lean process.

- Replay goals: 100
- Replay success: 59/100 (59.0%)
- Trace result: `outputs\phase3_final_guardrail_bridge_100.json`
- Replay result: `outputs\phase3_bridge_replay_100.json`

| Policy | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|---:|
| `rule_far_learned_second_stage` | 100 | 72.0% | 47.0% | 43.8% | 79.4 |
| `rule_far_learned_second_stage_base_guardrail_small` | 100 | 71.0% | 47.0% | 43.8% | 78.4 |
| `rule_far_learned_second_stage_final_base_guardrail_16` | 100 | 71.0% | 47.0% | 43.8% | 79.4 |
| `rule_far_learned_second_stage_final_base_guardrail_32` | 100 | 65.0% | 44.0% | 40.4% | 79.4 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 100 | 73.0% | 49.0% | 46.1% | 79.4 |

## Replay Status Counts

- Overall: {'lean_error': 41, 'verified': 59}
- By category: {'second_stage_over_fallback': 35, 'second_stage_over_expansion': 20, 'fallback_over_second_stage': 8, 'both_fail': 20, 'both_success': 10, 'fallback_fill': 7}

## Category-Level Replay

| Category | Goals | Replay verified |
|---|---:|---:|
| `both_fail` | 20 | 40.0% |
| `both_success` | 10 | 80.0% |
| `fallback_fill` | 7 | 85.7% |
| `fallback_over_second_stage` | 8 | 50.0% |
| `second_stage_over_expansion` | 20 | 65.0% |
| `second_stage_over_fallback` | 35 | 57.1% |

## Failed Replay Examples

- `Asymptotics.isLittleOTVS_iff_isLittleO` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/Asymptotics__isLittleOTVS_iff_isLittleO.lean:770:35: error(lean.unknownIdentifier): Unknown identifier `this`  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `Polynomial.splits_X_sub_C_mul_iff` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/Polynomial__splits_X_sub_C_mul_iff.lean:435:47: error: Application type mismatch: The argument   hf₀ has type   f = 0 but is expected to have type   ?m.95 ≠ 0 in the application   mul_ne_zero (X_sub_C_ne_zero ?m.99) hf₀ /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/Polynomial__splits_X_sub_C_mul_iff.lean:430:0: error: unsolved goals case pos R : Type u_1 inst✝¹ : CommRing R f : R[X] inst
- `MvPowerSeries.coeff_prod` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/MvPowerSeries__coeff_prod.lean:671:2: error: `simp` made no progress  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/SSet__horn₂₀__horn₂₁__horn₂₂__horn__IsCompatible__horn₃₁__ι₂_desc.lean:319:0: error: unsolved goals X : SSet f₀ f₂ f₃ : Δ[2] ⟶ X h₁₂ : stdSimplex.δ 2 ≫ f₀ = stdSimplex.δ 0 ≫ f₃ h₁₃ : stdSimplex.δ 1 ≫ f₀ = stdSimplex.δ 0 ≫ f₂ h₂₃ : stdSimplex.δ 2 ≫ f₂ = stdSimplex.δ 2 ≫ f₃ ⊢ horn.faceι 1 2 ι₂._proof_1 ≫ desc f₀ f₂ f₃ h₁₂ h₁₃ h₂₃ = (stdSimplex.faceSingletonComplIso 2).inv ≫ f₂  warning: batteries: repository '/root/.cach
- `MeasureTheory.Egorov.measure_notConvergentSeq_tendsto_zero` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/MeasureTheory__Egorov__measure_notConvergentSeq_tendsto_zero.lean:83:8: error(lean.synthInstanceFailed): failed to synthesize instance of type class   Nonempty ι  Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command. /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/MeasureTheory__Egorov__measure_notConvergentSeq_tendsto_z
- `compl_riemannZetaZeros_mem_codiscrete` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/compl_riemannZetaZeros_mem_codiscrete.lean:55:2: error: `grind` failed case grind this : ∀ (x : ℂ), ¬x = 1 → ({1}ᶜ ∩ riemannZetaZeros)ᶜ ∈ nhdsWithin x {x}ᶜ x : ℂ hx : x ≠ 1 h : riemannZetaZerosᶜ ∉ nhdsWithin x {x}ᶜ ⊢ False [grind] Goal diagnostics   [facts] Asserted facts     [prop] ∀ (x : ℂ), ¬x = 1 → ({1}ᶜ ∩ riemannZetaZeros)ᶜ ∈ nhdsWithin x {x}ᶜ     [prop] ¬x = 1     [prop] riemannZetaZerosᶜ ∉ nhdsWithin x {x}ᶜ     
- `HurwitzZeta.completedHurwitzZetaEven_one_sub` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/HurwitzZeta__completedHurwitzZetaEven_one_sub.lean:368:2: error: `simp` made no progress  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `BoxIntegral.hasIntegral_GP_pderiv` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/BoxIntegral__hasIntegral_GP_pderiv.lean:166:62: error(lean.unknownIdentifier): Unknown identifier `Hc` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/BoxIntegral__hasIntegral_GP_pderiv.lean:170:17: error(lean.unknownIdentifier): Unknown identifier `x` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/BoxIntegral__hasIntegral_GP_pderiv.lean:171:13: error(lean.un
- `ProbabilityTheory.Kernel.measurable_rnDerivAux` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/ProbabilityTheory__Kernel__measurable_rnDerivAux.lean:123:6: error(lean.unknownIdentifier): Unknown identifier `h_eq` /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/ProbabilityTheory__Kernel__measurable_rnDerivAux.lean:118:0: error: unsolved goals case pos α : Type u_1 γ : Type u_2 mα : MeasurableSpace α mγ : MeasurableSpace γ hαγ : MeasurableSpace.CountableOrCountablyGenerated α γ κ η : 
- `MeasureTheory.Measure.Measure.isProjectiveLimit_infinitePiNat` (second_stage_over_fallback): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase3_bridge_replay_files_100/MeasureTheory__Measure__Measure__isProjectiveLimit_infinitePiNat.lean:211:0: error: unsolved goals case hf X : ℕ → Type u_1 mX : (n : ℕ) → MeasurableSpace (X n) μ : (n : ℕ) → Measure (X n) hμ : ∀ (n : ℕ), IsProbabilityMeasure (μ n) I : Finset ℕ ⊢ Measurable (frestrictLe (I.sup id))  case hg X : ℕ → Type u_1 mX : (n : ℕ) → MeasurableSpace (X n) μ : (n : ℕ) → Measure (X n) hμ : ∀ (n : ℕ), IsProbabilityMeasure (μ n) I : F
