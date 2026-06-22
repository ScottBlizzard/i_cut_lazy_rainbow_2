# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage`
- New policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- Goals: 500
- Same solved: 455 (91.0%)
- Same failed: 39 (7.8%)
- New-only solved: 3
- Base-only solved: 3

## New-Only Solved

- `mathlib4::Algebraic.cardinalMk_lift_le_mul`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::AlgebraicTopology.DoldKan.PInfty_comp_map_mono_eq_zero`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::DirichletCharacter.completedLFunction_modOne_eq`; base_failure=imported_premise_missing, premises 96 -> 96

## Base-Only Solved

- `mathlib4::Matrix.derivative_det_one_add_X_smul_aux`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::MeasurableSet.inter`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::Subgroup.IsComplement.finite_right_iff`; new_failure=imported_premise_missing, premises 96 -> 96

