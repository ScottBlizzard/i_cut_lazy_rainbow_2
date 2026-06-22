# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `history_only` | 500 | 73.6% | 37.1% | 1.66 | 47.3 | 0.05s | 0.0% | 0.0% |
| `one_shot` | 500 | 58.0% | 0.0% | 1.00 | 28.9 | 0.03s | 0.0% | 0.0% |
| `random_retry` | 500 | 71.0% | 38.0% | 1.75 | 49.9 | 0.05s | 0.0% | 0.0% |
| `rule_far_failure_type_only` | 500 | 91.6% | 80.0% | 1.59 | 46.2 | 0.07s | 0.0% | 0.0% |
| `rule_far_full` | 500 | 98.8% | 97.1% | 1.47 | 42.7 | 0.06s | 0.0% | 0.0% |
| `rule_far_no_core_tags` | 500 | 97.0% | 92.9% | 1.50 | 44.4 | 0.07s | 0.0% | 0.0% |
| `topk_equal_budget` | 500 | 80.0% | 0.0% | 1.00 | 43.5 | 0.05s | 0.0% | 0.0% |
| `topk_expansion` | 500 | 91.6% | 80.0% | 1.59 | 46.2 | 0.07s | 0.0% | 0.0% |
| `visible_feature_rerank` | 500 | 88.4% | 0.0% | 1.00 | 43.5 | 0.05s | 0.0% | 0.0% |

## Failure Type Counts

- `history_only`: {'type_mismatch': 147, 'missing_bridge': 142, 'typeclass_missing': 77, 'rewrite_direction': 94}
- `one_shot`: {'type_mismatch': 67, 'typeclass_missing': 43, 'rewrite_direction': 41, 'missing_bridge': 59}
- `random_retry`: {'rewrite_direction': 119, 'type_mismatch': 164, 'typeclass_missing': 77, 'missing_bridge': 162}
- `rule_far_failure_type_only`: {'type_mismatch': 102, 'typeclass_missing': 70, 'rewrite_direction': 76, 'missing_bridge': 90}
- `rule_far_full`: {'type_mismatch': 69, 'typeclass_missing': 52, 'rewrite_direction': 56, 'missing_bridge': 63}
- `rule_far_no_core_tags`: {'type_mismatch': 84, 'typeclass_missing': 54, 'rewrite_direction': 55, 'missing_bridge': 74}
- `topk_equal_budget`: {'type_mismatch': 32, 'rewrite_direction': 23, 'typeclass_missing': 21, 'missing_bridge': 24}
- `topk_expansion`: {'type_mismatch': 102, 'typeclass_missing': 70, 'rewrite_direction': 76, 'missing_bridge': 90}
- `visible_feature_rerank`: {'type_mismatch': 16, 'missing_bridge': 15, 'rewrite_direction': 12, 'typeclass_missing': 15}
