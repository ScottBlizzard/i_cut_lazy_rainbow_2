# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `rule_far_learned_second_stage` | 500 | 91.6% | 83.1% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 500 | 91.6% | 83.1% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_bt_expert_guardrail_16` | 500 | 91.0% | 81.9% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_bt_expert_guardrail_4` | 500 | 91.6% | 83.1% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_bt_expert_guardrail_8` | 500 | 91.4% | 82.7% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e4` | 500 | 91.6% | 83.1% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |

## Failure Type Counts

- `rule_far_learned_second_stage`: {'imported_premise_missing': 278, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_final_base_guardrail_8`: {'imported_premise_missing': 278, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_final_bt_expert_guardrail_16`: {'imported_premise_missing': 282, 'type_mismatch': 27, 'missing_bridge': 37, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_final_bt_expert_guardrail_4`: {'imported_premise_missing': 278, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_final_bt_expert_guardrail_8`: {'imported_premise_missing': 279, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e4`: {'imported_premise_missing': 278, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
