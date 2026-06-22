# Policy Delta Analysis

- Base policy: `rule_far_learned_second_stage`
- New policy: `rule_far_learned_second_stage_final_base_guardrail_8`
- Goals: 100
- Same solved: 69 (69.0%)
- Same failed: 24 (24.0%)
- New-only solved: 4
- Base-only solved: 3
- Replay-verified new-only solved: 4
- Replay-verified base-only solved: 2

## New-Only Solved

- `Nat.Primes.PNat.Prime.ne_one`, replay_success=True, category=fallback_over_second_stage; base_failure=imported_premise_missing, premises 96 -> 96
- `WeierstrassCurve.Jacobian.addY_neg`, replay_success=True, category=both_fail; base_failure=missing_bridge, premises 96 -> 96
- `WeierstrassCurve.Jacobian.neg_of_Z_ne_zero`, replay_success=True, category=fallback_over_second_stage; base_failure=imported_premise_missing, premises 96 -> 96
- `equicontinuousWithinAt_iInf_rng`, replay_success=True, category=fallback_over_second_stage; base_failure=type_mismatch, premises 96 -> 96

## Base-Only Solved

- `DiscreteUniformity.eq_pure_of_cauchy`, replay_success=True, category=second_stage_over_fallback; new_failure=imported_premise_missing, premises 96 -> 96
- `ENNReal.tendsto_nhds_of_Icc`, replay_success=True, category=fallback_fill; new_failure=imported_premise_missing, premises 96 -> 96
- `Turing.TM2.TM2to1.addBottom_map`, replay_success=False, category=second_stage_over_fallback; new_failure=imported_premise_missing, premises 96 -> 96

