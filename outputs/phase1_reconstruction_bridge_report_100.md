# Phase 1 Reconstruction Bridge

> Bridge success means trace-core proof-core recovery plus successful replay of the original traced tactic script in a real Lean process.

- Replay goals: 100
- Replay success: 86/100 (86.0%)

| Policy | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|---:|
| `one_shot` | 100 | 13.0% | 10.0% | 0.0% | 31.1 |
| `rule_far_failure_type_only` | 100 | 54.0% | 43.0% | 37.9% | 81.0 |
| `rule_far_full` | 100 | 92.0% | 79.0% | 79.3% | 67.6 |
| `rule_far_no_core_tags` | 100 | 85.0% | 72.0% | 71.3% | 75.7 |
| `topk_equal_budget` | 100 | 22.0% | 16.0% | 0.0% | 52.9 |
| `topk_expansion` | 100 | 54.0% | 43.0% | 37.9% | 81.0 |
| `visible_feature_rerank` | 100 | 38.0% | 33.0% | 0.0% | 52.9 |

## Replay Status Counts

- Overall: {'verified': 86, 'lean_error': 14}
- By category: {'far_over_topk': 35, 'far_over_static': 35, 'oracle_gap': 15, 'all_success_control': 15}

## Failed Replay Examples

- `CochainComplex.HomComplex.Cochain.δ_shape` (far_over_topk): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/CochainComplex__HomComplex__Cochain__δ_shape.lean:423:0: error: unsolved goals case a C : Type u inst✝¹ : Category.{v, u} C inst✝ : Preadditive C F G : CochainComplex C ℤ n m : ℤ hnm : ¬n + 1 = m z : Cochain F G n p q : ℤ hpq : p + m = q ⊢ ¬(ComplexShape.up ℤ).Rel p (p + m - n)  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/math
- `SkewPolynomial.monomial_one_right_eq_X_pow` (far_over_topk): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/SkewPolynomial__monomial_one_right_eq_X_pow.lean:305:2: error: `simp` made no progress  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `MeasureTheory.SimpleFunc.finset_sup_apply` (far_over_topk): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/MeasureTheory__SimpleFunc__finset_sup_apply.lean:725:9: error(lean.synthInstanceFailed): failed to synthesize instance of type class   DecidableEq γ  Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command. /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/MeasureTheory__SimpleFunc__finset_sup_ap
- `SimpleGraph.Subgraph.ConnectedComponent.Walk.IsPath.IsCycle.Subgraph.connected_induce_top_sup` (far_over_static): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/SimpleGraph__Subgraph__ConnectedComponent__Walk__IsPath__IsCycle__Subgraph__connected_induce_top_sup.lean:551:2: error: `simp` made no progress /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/SimpleGraph__Subgraph__ConnectedComponent__Walk__IsPath__IsCycle__Subgraph__connected_induce_top_sup.lean:550:8: warning: This simp argument is unused:   uH  Hint: Omit i
- `Affine.Simplex.exists_forall_signedInfDist_eq_iff_excenterExists_and_eq_excenter` (far_over_static): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/Affine__Simplex__exists_forall_signedInfDist_eq_iff_excenterExists_and_eq_excenter.lean:939:35: error(lean.unknownIdentifier): Unknown identifier `h'`  warning: batteries: repository '/root/.cache/lean_dojo/gitpython-mathlib4_current-64a930d1015bab6c2bf24f885c7d3403c160cc28/mathlib4_current/.lake/packages/batteries' has local changes
- `Perfection.PerfectionMap.ModP.ModP.PreTilt.valAux_mul` (far_over_static): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/Perfection__PerfectionMap__ModP__ModP__PreTilt__valAux_mul.lean:748:32: error(lean.unknownIdentifier): Unknown identifier `f` /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/Perfection__PerfectionMap__ModP__ModP__PreTilt__valAux_mul.lean:748:63: error(lean.unknownIdentifier): Unknown identifier `hf` /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconst
- `List.aestronglyMeasurable_prod` (far_over_static): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/List__aestronglyMeasurable_prod.lean:423:2: warning: declaration uses `sorry` /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/List__aestronglyMeasurable_prod.lean:429:8: error: typeclass instance problem is stuck   One ?m.22  Note: Lean will not try to resolve this typeclass instance problem because the type argument to `One` is a metavariable. This argument m
- `MeasureTheory.VectorMeasure.integral_map` (far_over_static): `lean_error`;  u_6 mX : MeasurableSpace X inst✝⁵ : NormedAddCommGroup E inst✝⁴ : NormedSpace ℝ E inst✝³ : NormedAddCommGroup F inst✝² : NormedSpace ℝ F inst✝¹ : NormedAddCommGroup G inst✝ : NormedSpace ℝ G f : X → E μ : VectorMeasure X F B : E →L[ℝ] F →L[ℝ] G ⊢ NNReal.mk ‖B‖ ⋯ ≤ ‖B‖₊ /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/MeasureTheory__VectorMeasure__integral_map.lean:636:8: warning: This simp argument is unused:   ← coe_nnnorm  Hint: Omit it from the sim
- `Polynomial.resultant_self` (far_over_static): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/Polynomial__resultant_self.lean:592:42: error(lean.unknownIdentifier): Unknown identifier `hf` /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/Polynomial__resultant_self.lean:590:0: error: unsolved goals case pos R : Type u_1 inst✝ : CommRing R f : R[X] h : f.natDegree = 0 ⊢ f.resultant f = 0 ^ f.natDegree  case neg R : Type u_1 inst✝ : CommRing R f : R[X] h :
- `finprod_cond_eq_prod_of_cond_iff` (oracle_gap): `lean_error`; /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/finprod_cond_eq_prod_of_cond_iff.lean:458:2: warning: declaration uses `sorry` /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/finprod_cond_eq_prod_of_cond_iff.lean:466:62: error(lean.unknownIdentifier): Unknown identifier `this` /workspace/thymic_project/paper/iclr_2/outputs/phase1_reconstruction_bridge_replay_files_100/finprod_cond_eq_prod_of_cond_iff.lean:4
