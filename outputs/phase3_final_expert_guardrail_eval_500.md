# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `rule_far_learned_second_stage` | 500 | 92.4% | 84.7% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 500 | 92.6% | 85.1% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_bt_expert_guardrail_16` | 500 | 91.4% | 82.7% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_bt_expert_guardrail_4` | 500 | 92.4% | 84.7% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_bt_expert_guardrail_8` | 500 | 92.4% | 84.7% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e4` | 500 | 92.6% | 85.1% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |

## Failure Type Counts

- `rule_far_learned_second_stage`: {'type_mismatch': 40, 'missing_bridge': 35, 'imported_premise_missing': 258, 'rewrite_direction': 25, 'typeclass_missing': 22}
- `rule_far_learned_second_stage_final_base_guardrail_8`: {'type_mismatch': 39, 'missing_bridge': 34, 'imported_premise_missing': 259, 'rewrite_direction': 25, 'typeclass_missing': 22}
- `rule_far_learned_second_stage_final_bt_expert_guardrail_16`: {'type_mismatch': 39, 'missing_bridge': 34, 'imported_premise_missing': 265, 'rewrite_direction': 25, 'typeclass_missing': 22}
- `rule_far_learned_second_stage_final_bt_expert_guardrail_4`: {'type_mismatch': 40, 'missing_bridge': 35, 'imported_premise_missing': 258, 'rewrite_direction': 25, 'typeclass_missing': 22}
- `rule_far_learned_second_stage_final_bt_expert_guardrail_8`: {'type_mismatch': 39, 'missing_bridge': 35, 'imported_premise_missing': 259, 'rewrite_direction': 25, 'typeclass_missing': 22}
- `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e4`: {'type_mismatch': 39, 'missing_bridge': 34, 'imported_premise_missing': 259, 'rewrite_direction': 25, 'typeclass_missing': 22}
