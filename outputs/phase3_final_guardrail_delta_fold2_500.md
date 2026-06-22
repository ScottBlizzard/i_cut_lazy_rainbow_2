# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage`
- New policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- Goals: 500
- Same solved: 468 (93.6%)
- Same failed: 28 (5.6%)
- New-only solved: 2
- Base-only solved: 2

## New-Only Solved

- `mathlib4::Finset.Ico_eq_empty_iff`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::exists_continuousLinearEquiv_fderivWithin_symm_eq`; base_failure=imported_premise_missing, premises 96 -> 96

## Base-Only Solved

- `mathlib4::Convexity.dist_convexCombPair_left`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::le_mul_inv_iff_le`; new_failure=imported_premise_missing, premises 96 -> 96

