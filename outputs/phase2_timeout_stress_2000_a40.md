# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `one_shot` | 2000 | 57.0% | 0.0% | 1.00 | 28.4 | 0.03s | 4.0% | 0.0% |
| `rule_far_failure_type_only` | 2000 | 60.2% | 7.5% | 1.83 | 41.9 | 0.06s | 23.9% | 0.0% |
| `rule_far_full` | 2000 | 100.0% | 100.0% | 1.79 | 40.1 | 0.06s | 22.5% | 0.0% |
| `rule_far_no_core_tags` | 2000 | 59.7% | 6.2% | 1.83 | 42.8 | 0.08s | 46.1% | 0.0% |
| `rule_far_no_core_timeout_shrink` | 2000 | 69.3% | 28.6% | 1.82 | 42.7 | 0.06s | 23.5% | 0.0% |
| `topk_equal_budget` | 2000 | 43.8% | 0.0% | 1.00 | 42.9 | 0.04s | 56.2% | 0.0% |
| `topk_expansion` | 2000 | 59.7% | 6.2% | 1.83 | 50.4 | 0.09s | 46.1% | 0.0% |
| `visible_feature_rerank` | 2000 | 43.8% | 0.0% | 1.00 | 42.9 | 0.04s | 56.2% | 0.0% |

## Failure Type Counts

- `one_shot`: {'missing_bridge': 264, 'timeout': 79, 'rewrite_direction': 172, 'type_mismatch': 211, 'typeclass_missing': 133}
- `rule_far_failure_type_only`: {'missing_bridge': 573, 'timeout': 875, 'rewrite_direction': 327, 'type_mismatch': 424, 'typeclass_missing': 250}
- `rule_far_full`: {'missing_bridge': 264, 'timeout': 806, 'rewrite_direction': 172, 'type_mismatch': 211, 'typeclass_missing': 133}
- `rule_far_no_core_tags`: {'missing_bridge': 264, 'timeout': 1691, 'rewrite_direction': 172, 'type_mismatch': 211, 'typeclass_missing': 133}
- `rule_far_no_core_timeout_shrink`: {'missing_bridge': 488, 'timeout': 853, 'type_mismatch': 375, 'rewrite_direction': 300, 'typeclass_missing': 230}
- `topk_equal_budget`: {'timeout': 1125}
- `topk_expansion`: {'missing_bridge': 264, 'timeout': 1691, 'rewrite_direction': 172, 'type_mismatch': 211, 'typeclass_missing': 133}
- `visible_feature_rerank`: {'timeout': 1125}
