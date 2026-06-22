# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage`
- New policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- Goals: 500
- Same solved: 461 (92.2%)
- Same failed: 33 (6.6%)
- New-only solved: 6
- Base-only solved: 0

## New-Only Solved

- `mathlib4::Asymptotics.isBigO_iff_exists_eq_mul`; base_failure=type_mismatch, premises 96 -> 96
- `mathlib4::Finset.Ioc_union_Ioc_eq_Ioc`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::GenContFract.of_correctness_of_nth_stream_eq_none`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::Left.mul_pos`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::Polynomial.evalEval_finsetSum`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::Ring.krullDimLE_one_iff`; base_failure=imported_premise_missing, premises 96 -> 96

## Base-Only Solved


