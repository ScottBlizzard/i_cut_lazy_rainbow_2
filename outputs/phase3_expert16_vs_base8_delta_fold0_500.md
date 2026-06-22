# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- New policy: `rule_far_learned_second_stage_final_bt_expert_guardrail_16`
- Goals: 500
- Same solved: 453 (90.6%)
- Same failed: 40 (8.0%)
- New-only solved: 2
- Base-only solved: 5

## New-Only Solved

- `mathlib4::MeasurableEmbedding.variation_map`; base_failure=missing_bridge, premises 96 -> 96
- `mathlib4::MeasurableSet.inter`; base_failure=imported_premise_missing, premises 96 -> 96

## Base-Only Solved

- `mathlib4::Algebraic.cardinalMk_lift_le_mul`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::AlgebraicTopology.DoldKan.PInfty_comp_map_mono_eq_zero`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::DirichletCharacter.completedLFunction_modOne_eq`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::Filter.map_const_principal_coprod_map_id_principal`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::NumberField.InfinitePlace.isReal_comap_iff`; new_failure=imported_premise_missing, premises 96 -> 96

