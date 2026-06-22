# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- New policy: `rule_far_learned_second_stage_final_bt_expert_guardrail_16`
- Goals: 500
- Same solved: 456 (91.2%)
- Same failed: 36 (7.2%)
- New-only solved: 1
- Base-only solved: 7

## New-Only Solved

- `mathlib4::MeasureTheory.Measure.integral_isMulLeftInvariant_isMulRightInvariant_combo`; base_failure=type_mismatch, premises 96 -> 96

## Base-Only Solved

- `mathlib4::MeasureTheory.AECover.integral_deriv_smul_comp_Ioi`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::Nat.Primes.PNat.Prime.ne_one`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::PowerSeries.le_weightedOrder_subst`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::WeierstrassCurve.Jacobian.addY_neg`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::WeierstrassCurve.Jacobian.neg_of_Z_ne_zero`; new_failure=imported_premise_missing, premises 96 -> 96
- `mathlib4::equicontinuousWithinAt_iInf_rng`; new_failure=type_mismatch, premises 96 -> 96

