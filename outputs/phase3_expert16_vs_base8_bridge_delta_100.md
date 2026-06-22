# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- New policy: `rule_far_learned_second_stage_final_bt_expert_guardrail_16`
- Goals: 100
- Same solved: 67 (67.0%)
- Same failed: 26 (26.0%)
- New-only solved: 1
- Base-only solved: 6
- Replay-verified new-only solved: 0
- Replay-verified base-only solved: 4

## New-Only Solved

- `MeasureTheory.Measure.integral_isMulLeftInvariant_isMulRightInvariant_combo`, replay_success=False, category=both_fail; base_failure=type_mismatch, premises 96 -> 96

## Base-Only Solved

- `Nat.Primes.PNat.Prime.ne_one`, replay_success=True, category=fallback_over_second_stage; new_failure=imported_premise_missing, premises 96 -> 96
- `PowerSeries.le_weightedOrder_subst`, replay_success=False, category=second_stage_over_expansion; new_failure=imported_premise_missing, premises 96 -> 96
- `SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc`, replay_success=False, category=second_stage_over_fallback; new_failure=imported_premise_missing, premises 96 -> 96
- `WeierstrassCurve.Jacobian.addY_neg`, replay_success=True, category=both_fail; new_failure=imported_premise_missing, premises 96 -> 96
- `WeierstrassCurve.Jacobian.neg_of_Z_ne_zero`, replay_success=True, category=fallback_over_second_stage; new_failure=imported_premise_missing, premises 96 -> 96
- `equicontinuousWithinAt_iInf_rng`, replay_success=True, category=fallback_over_second_stage; new_failure=type_mismatch, premises 96 -> 96

