# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 500 | 87.0% | 73.8% | 1.73 | 57.6 | 0.09s | 0.0% | 0.0% |
| `learned_expansion` | 500 | 84.0% | 67.7% | 1.80 | 57.7 | 0.09s | 0.0% | 0.0% |
| `learned_rerank` | 500 | 64.2% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `rule_far_full` | 500 | 55.6% | 55.0% | 2.54 | 86.6 | 0.14s | 0.0% | 0.0% |
| `rule_far_learned` | 500 | 84.4% | 68.5% | 1.79 | 57.4 | 0.09s | 0.0% | 0.0% |
| `rule_far_learned_failure_specific` | 500 | 87.0% | 73.8% | 1.74 | 57.0 | 0.09s | 0.0% | 0.0% |
| `rule_far_learned_second_stage` | 500 | 92.4% | 84.7% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |

## Failure Type Counts

- `learned_base_fallback`: {'type_mismatch': 56, 'missing_bridge': 45, 'imported_premise_missing': 278, 'typeclass_missing': 21, 'rewrite_direction': 28}
- `learned_expansion`: {'type_mismatch': 71, 'missing_bridge': 60, 'imported_premise_missing': 272, 'rewrite_direction': 48, 'typeclass_missing': 31}
- `learned_rerank`: {'type_mismatch': 26, 'missing_bridge': 27, 'imported_premise_missing': 97, 'rewrite_direction': 18, 'typeclass_missing': 11}
- `rule_far_full`: {'imported_premise_missing': 692, 'missing_bridge': 98, 'typeclass_missing': 49, 'type_mismatch': 104, 'rewrite_direction': 49}
- `rule_far_learned`: {'type_mismatch': 72, 'missing_bridge': 58, 'imported_premise_missing': 265, 'rewrite_direction': 49, 'typeclass_missing': 31}
- `rule_far_learned_failure_specific`: {'type_mismatch': 57, 'missing_bridge': 45, 'imported_premise_missing': 278, 'typeclass_missing': 23, 'rewrite_direction': 31}
- `rule_far_learned_second_stage`: {'type_mismatch': 40, 'missing_bridge': 35, 'imported_premise_missing': 258, 'rewrite_direction': 25, 'typeclass_missing': 22}
