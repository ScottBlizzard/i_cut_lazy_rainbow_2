# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_50.json`
- Replayable goals evaluated: 10
- Attempts: 110
- Verified attempts: 16
- Non-empty-premise verified attempts: 12
- Goals with any proof: 3
- Goals with non-empty-premise proof: 3
- Action-dependent goals: 1

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 33 |
| `proved` | 16 |
| `search_fail` | 24 |
| `simp_fail` | 37 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `hammerCore_core` | 0 | 0 | 10 |
| `hammerCore_core_plus_learned` | 0 | 0 | 10 |
| `hammer_core_facts` | 2 | 2 | 10 |
| `hammer_core_plus_learned` | 2 | 2 | 10 |
| `hammer_empty` | 2 | 0 | 10 |
| `simp_core` | 2 | 2 | 10 |
| `simp_core_plus_learned` | 2 | 2 | 10 |
| `simp_empty` | 1 | 0 | 10 |
| `simpa_core` | 2 | 2 | 10 |
| `simpa_core_plus_learned` | 2 | 2 | 10 |
| `simpa_empty` | 1 | 0 | 10 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 9 | 6 | 3 | `hammer_empty` (0 facts, 0 simps) |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 4 | 4 | 0 | `simp_core` (0 facts, 2 simps) |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 3 | 2 | 1 | `hammer_empty` (0 facts, 0 simps) |
| `mathlib4::Set.Intersecting.insert` | 0 | 0 | 0 | none |
| `mathlib4::nhds_le_of_le` | 0 | 0 | 0 | none |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 0 | 0 | 0 | none |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 0 | 0 | 0 | none |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | 0 | 0 | 0 | none |
| `mathlib4::Sym.Sym2.card_image_diag` | 0 | 0 | 0 | none |

## Availability

| Goal | Checked | Available | Failed |
|---|---:|---:|---:|
| `mathlib4::Module.rank_tensorProduct'` | 32 | 22 | 10 |
| `mathlib4::FirstOrder.Language.definableFun_const` | 33 | 17 | 16 |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 32 | 12 | 20 |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 32 | 16 | 16 |
| `mathlib4::Set.Intersecting.insert` | 32 | 16 | 16 |
| `mathlib4::nhds_le_of_le` | 32 | 4 | 28 |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 34 | 11 | 23 |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 32 | 12 | 20 |
| `mathlib4::Complex.Complex.Complex.Gamma_ne_zero_of_re_pos` | 32 | 19 | 13 |
| `mathlib4::Sym.Sym2.card_image_diag` | 32 | 23 | 9 |

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
