# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 500 | 88.8% | 74.5% | 1.61 | 54.0 | 0.08s | 0.0% | 0.0% |
| `learned_expansion` | 500 | 82.4% | 60.0% | 1.71 | 54.6 | 0.09s | 0.0% | 0.0% |
| `learned_rerank` | 500 | 71.8% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `rule_far_full` | 500 | 58.4% | 58.1% | 2.50 | 86.2 | 0.14s | 0.0% | 0.0% |
| `rule_far_learned_failure_specific` | 500 | 88.8% | 74.5% | 1.62 | 53.4 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage` | 500 | 94.0% | 86.4% | 1.58 | 50.7 | 0.07s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 500 | 94.0% | 86.4% | 1.58 | 50.7 | 0.07s | 0.0% | 0.0% |

## Failure Type Counts

- `learned_base_fallback`: {'imported_premise_missing': 223, 'typeclass_missing': 34, 'missing_bridge': 47, 'rewrite_direction': 26, 'type_mismatch': 29}
- `learned_expansion`: {'imported_premise_missing': 217, 'typeclass_missing': 57, 'missing_bridge': 63, 'rewrite_direction': 48, 'type_mismatch': 56}
- `learned_rerank`: {'imported_premise_missing': 68, 'typeclass_missing': 19, 'missing_bridge': 20, 'rewrite_direction': 15, 'type_mismatch': 19}
- `rule_far_full`: {'imported_premise_missing': 683, 'type_mismatch': 74, 'missing_bridge': 95, 'typeclass_missing': 50, 'rewrite_direction': 58}
- `rule_far_learned_failure_specific`: {'imported_premise_missing': 223, 'typeclass_missing': 35, 'missing_bridge': 49, 'rewrite_direction': 26, 'type_mismatch': 33}
- `rule_far_learned_second_stage`: {'imported_premise_missing': 204, 'typeclass_missing': 26, 'missing_bridge': 38, 'rewrite_direction': 27, 'type_mismatch': 27}
- `rule_far_learned_second_stage_final_base_guardrail_8`: {'imported_premise_missing': 204, 'typeclass_missing': 26, 'missing_bridge': 38, 'rewrite_direction': 27, 'type_mismatch': 27}
