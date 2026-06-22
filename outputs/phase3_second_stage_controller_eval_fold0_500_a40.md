# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 500 | 83.6% | 66.9% | 1.72 | 57.7 | 0.09s | 0.0% | 0.0% |
| `learned_expansion` | 500 | 79.0% | 57.7% | 1.83 | 58.4 | 0.10s | 0.0% | 0.0% |
| `learned_rerank` | 500 | 63.4% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `rule_far_full` | 500 | 53.2% | 52.6% | 2.54 | 86.7 | 0.14s | 0.0% | 0.0% |
| `rule_far_learned` | 500 | 79.4% | 58.5% | 1.82 | 58.4 | 0.10s | 0.0% | 0.0% |
| `rule_far_learned_failure_specific` | 500 | 83.4% | 66.5% | 1.73 | 56.8 | 0.09s | 0.0% | 0.0% |
| `rule_far_learned_second_stage` | 500 | 91.6% | 83.1% | 1.70 | 54.3 | 0.08s | 0.0% | 0.0% |

## Failure Type Counts

- `learned_base_fallback`: {'imported_premise_missing': 292, 'type_mismatch': 39, 'missing_bridge': 50, 'typeclass_missing': 35, 'rewrite_direction': 28}
- `learned_expansion`: {'imported_premise_missing': 286, 'type_mismatch': 52, 'missing_bridge': 81, 'typeclass_missing': 46, 'rewrite_direction': 53}
- `learned_rerank`: {'imported_premise_missing': 101, 'missing_bridge': 29, 'typeclass_missing': 15, 'type_mismatch': 19, 'rewrite_direction': 19}
- `rule_far_full`: {'imported_premise_missing': 707, 'missing_bridge': 109, 'type_mismatch': 76, 'typeclass_missing': 48, 'rewrite_direction': 65}
- `rule_far_learned`: {'imported_premise_missing': 282, 'type_mismatch': 52, 'missing_bridge': 82, 'typeclass_missing': 46, 'rewrite_direction': 53}
- `rule_far_learned_failure_specific`: {'imported_premise_missing': 292, 'type_mismatch': 39, 'missing_bridge': 51, 'typeclass_missing': 36, 'rewrite_direction': 30}
- `rule_far_learned_second_stage`: {'imported_premise_missing': 278, 'type_mismatch': 27, 'missing_bridge': 38, 'typeclass_missing': 21, 'rewrite_direction': 26}
