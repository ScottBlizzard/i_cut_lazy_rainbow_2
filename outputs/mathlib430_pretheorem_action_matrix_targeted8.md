# Mathlib 4.30 Replayable-Subset Proof-Action Matrix

- Verdict: `pass_action_dependent`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_100.json`
- Replayable goals evaluated: 8
- Attempts: 48
- Verified attempts: 4
- Non-empty-premise verified attempts: 4
- Goals with any proof: 2
- Goals with non-empty-premise proof: 2
- Action-dependent goals: 2

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 28 |
| `proved` | 4 |
| `rewrite_fail` | 16 |

## By Action

| Action | Verified | Non-empty verified | Attempts |
|---|---:|---:|---:|
| `simp_all_core` | 2 | 2 | 8 |
| `simp_all_core_plus_learned` | 2 | 2 | 8 |
| `simp_rw_core` | 0 | 0 | 8 |
| `simp_rw_core_plus_learned` | 0 | 0 | 8 |
| `solve_by_elim_core` | 0 | 0 | 8 |
| `solve_by_elim_core_plus_learned` | 0 | 0 | 8 |

## By Goal

| Goal | Verified | Non-empty verified | Empty verified | Best |
|---|---:|---:|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 2 | 2 | 0 | `simp_all_core` (0 facts, 1 simps) |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | 0 | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 2 | 2 | 0 | `simp_all_core` (0 facts, 2 simps) |
| `mathlib4::CategoryTheory.Comonad.ComonadicityInternal.comparisonAdjunction_counit_f` | 0 | 0 | 0 | none |
| `mathlib4::Set.Intersecting.insert` | 0 | 0 | 0 | none |
| `mathlib4::nhds_le_of_le` | 0 | 0 | 0 | none |
| `mathlib4::LieAlgebra.InvariantForm.orthogonal_isCompl_toSubmodule` | 0 | 0 | 0 | none |
| `mathlib4::IntermediateField.AlgEquiv.restrictNormal_eq_one_iff` | 0 | 0 | 0 | none |

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

## Readout

- This pilot found at least one action-dependent proof, so the proof-action routing route should be scaled.
