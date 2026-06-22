# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `rule_far_learned_second_stage` | 100 | 72.0% | 68.5% | 2.48 | 79.4 | 0.15s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 100 | 73.0% | 69.7% | 2.48 | 79.4 | 0.15s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e4` | 100 | 73.0% | 69.7% | 2.48 | 79.4 | 0.15s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e8` | 100 | 72.0% | 68.5% | 2.48 | 79.4 | 0.15s | 0.0% | 0.0% |

## Failure Type Counts

- `rule_far_learned_second_stage`: {'imported_premise_missing': 131, 'type_mismatch': 21, 'rewrite_direction': 9, 'missing_bridge': 13, 'typeclass_missing': 2}
- `rule_far_learned_second_stage_final_base_guardrail_8`: {'imported_premise_missing': 132, 'type_mismatch': 20, 'rewrite_direction': 9, 'missing_bridge': 12, 'typeclass_missing': 2}
- `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e4`: {'imported_premise_missing': 132, 'type_mismatch': 20, 'rewrite_direction': 9, 'missing_bridge': 12, 'typeclass_missing': 2}
- `rule_far_learned_second_stage_final_hybrid_guardrail_b8_e8`: {'imported_premise_missing': 134, 'type_mismatch': 19, 'rewrite_direction': 9, 'missing_bridge': 12, 'typeclass_missing': 2}
