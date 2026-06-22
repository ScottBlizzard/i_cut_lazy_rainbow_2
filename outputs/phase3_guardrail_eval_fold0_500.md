# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 500 | 83.6% | 66.9% | 1.72 | 57.7 | 0.09s | 0.0% | 0.0% |
| `rule_far_learned_second_stage` | 500 | 91.6% | 83.1% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_base_guardrail_small` | 500 | 89.8% | 79.4% | 1.69 | 54.2 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_base_mix_200` | 500 | 90.0% | 79.8% | 1.69 | 54.2 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_16` | 500 | 90.0% | 79.8% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 500 | 91.6% | 83.1% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |

## Failure Type Counts

- `learned_base_fallback`: {'imported_premise_missing': 292, 'type_mismatch': 39, 'missing_bridge': 50, 'typeclass_missing': 35, 'rewrite_direction': 28}
- `rule_far_learned_second_stage`: {'imported_premise_missing': 278, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_base_guardrail_small`: {'imported_premise_missing': 286, 'type_mismatch': 26, 'missing_bridge': 38, 'typeclass_missing': 23, 'rewrite_direction': 25}
- `rule_far_learned_second_stage_base_mix_200`: {'imported_premise_missing': 287, 'type_mismatch': 25, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_final_base_guardrail_16`: {'imported_premise_missing': 286, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
- `rule_far_learned_second_stage_final_base_guardrail_8`: {'imported_premise_missing': 278, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
