# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage`
- New policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- Goals: 500
- Same solved: 459 (91.8%)
- Same failed: 34 (6.8%)
- New-only solved: 4
- Base-only solved: 3

## New-Only Solved

- `mathlib4::Nat.Primes.PNat.Prime.ne_one`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::WeierstrassCurve.Jacobian.addY_neg`; base_failure=missing_bridge, premises 96 -> 96
- `mathlib4::WeierstrassCurve.Jacobian.neg_of_Z_ne_zero`; base_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::equicontinuousWithinAt_iInf_rng`; base_failure=type_mismatch, premises 96 -> 96

## Base-Only Solved

- `mathlib4::DiscreteUniformity.eq_pure_of_cauchy`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::ENNReal.tendsto_nhds_of_Icc`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::Turing.TM2.TM2to1.addBottom_map`; new_failure=imported_premise_missing, premises 96 -> 96

