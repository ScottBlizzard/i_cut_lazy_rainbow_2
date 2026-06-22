# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage`
- New policy: `rule_far_learned_second_stage_final_bt_expert_guardrail_16`
- Goals: 100
- Same solved: 67 (67.0%)
- Same failed: 27 (27.0%)
- New-only solved: 1
- Base-only solved: 5
- Replay-verified new-only solved: 0
- Replay-verified base-only solved: 2

## New-Only Solved

- `MeasureTheory.Measure.integral_isMulLeftInvariant_isMulRightInvariant_combo`, replay_success=False, category=both_fail; base_failure=type_mismatch, premises 96 -> 96

## Base-Only Solved

- `DiscreteUniformity.eq_pure_of_cauchy`, replay_success=True, category=second_stage_over_fallback; new_failure=imported_premise_missing, premises 96 -> 96
- `ENNReal.tendsto_nhds_of_Icc`, replay_success=True, category=fallback_fill; new_failure=imported_premise_missing, premises 96 -> 96
- `PowerSeries.le_weightedOrder_subst`, replay_success=False, category=second_stage_over_expansion; new_failure=imported_premise_missing, premises 96 -> 96
- `SSet.horn₂₀.horn₂₁.horn₂₂.horn.IsCompatible.horn₃₁.ι₂_desc`, replay_success=False, category=second_stage_over_fallback; new_failure=imported_premise_missing, premises 96 -> 96
- `Turing.TM2.TM2to1.addBottom_map`, replay_success=False, category=second_stage_over_fallback; new_failure=imported_premise_missing, premises 96 -> 96

