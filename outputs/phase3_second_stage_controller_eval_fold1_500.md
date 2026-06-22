# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 500 | 86.0% | 67.4% | 1.62 | 54.1 | 0.08s | 0.0% | 0.0% |
| `learned_expansion` | 500 | 81.0% | 55.8% | 1.72 | 54.9 | 0.09s | 0.0% | 0.0% |
| `learned_rerank` | 500 | 69.6% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `rule_far_full` | 500 | 55.6% | 55.2% | 2.55 | 86.9 | 0.14s | 0.0% | 0.0% |
| `rule_far_learned_failure_specific` | 500 | 86.4% | 68.4% | 1.62 | 53.2 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage` | 500 | 92.2% | 81.9% | 1.60 | 51.3 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 500 | 93.4% | 84.7% | 1.60 | 51.3 | 0.08s | 0.0% | 0.0% |

## Failure Type Counts

- `learned_base_fallback`: {'imported_premise_missing': 228, 'missing_bridge': 60, 'rewrite_direction': 29, 'type_mismatch': 30, 'typeclass_missing': 32}
- `learned_expansion`: {'imported_premise_missing': 231, 'missing_bridge': 80, 'rewrite_direction': 42, 'type_mismatch': 47, 'typeclass_missing': 53}
- `learned_rerank`: {'imported_premise_missing': 74, 'rewrite_direction': 17, 'missing_bridge': 26, 'typeclass_missing': 21, 'type_mismatch': 14}
- `rule_far_full`: {'imported_premise_missing': 705, 'type_mismatch': 80, 'typeclass_missing': 46, 'missing_bridge': 105, 'rewrite_direction': 59}
- `rule_far_learned_failure_specific`: {'imported_premise_missing': 228, 'missing_bridge': 58, 'rewrite_direction': 29, 'type_mismatch': 30, 'typeclass_missing': 35}
- `rule_far_learned_second_stage`: {'imported_premise_missing': 220, 'missing_bridge': 45, 'rewrite_direction': 25, 'type_mismatch': 24, 'typeclass_missing': 27}
- `rule_far_learned_second_stage_final_base_guardrail_8`: {'imported_premise_missing': 216, 'missing_bridge': 45, 'rewrite_direction': 25, 'type_mismatch': 23, 'typeclass_missing': 26}
