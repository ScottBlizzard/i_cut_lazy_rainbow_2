# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `one_shot` | 2000 | 58.0% | 0.0% | 1.00 | 28.4 | 0.03s | 0.0% | 0.0% |
| `rule_far_failure_type_only` | 2000 | 91.5% | 79.9% | 1.62 | 46.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_full` | 2000 | 98.3% | 96.0% | 1.47 | 42.9 | 0.06s | 0.0% | 0.0% |
| `rule_far_no_core_tags` | 2000 | 95.7% | 89.7% | 1.52 | 45.1 | 0.07s | 0.0% | 0.0% |
| `topk_equal_budget` | 2000 | 75.7% | 0.0% | 1.00 | 42.9 | 0.05s | 0.0% | 0.0% |
| `topk_expansion` | 2000 | 91.5% | 79.9% | 1.62 | 46.9 | 0.08s | 0.0% | 0.0% |
| `visible_feature_rerank` | 2000 | 86.5% | 0.0% | 1.00 | 42.9 | 0.05s | 0.0% | 0.0% |

## Failure Type Counts

- `one_shot`: {'missing_bridge': 286, 'rewrite_direction': 183, 'type_mismatch': 227, 'typeclass_missing': 145}
- `rule_far_failure_type_only`: {'missing_bridge': 457, 'rewrite_direction': 312, 'type_mismatch': 381, 'typeclass_missing': 256}
- `rule_far_full`: {'missing_bridge': 301, 'rewrite_direction': 250, 'type_mismatch': 246, 'typeclass_missing': 177}
- `rule_far_no_core_tags`: {'missing_bridge': 359, 'rewrite_direction': 268, 'type_mismatch': 310, 'typeclass_missing': 197}
- `topk_equal_budget`: {'rewrite_direction': 107, 'missing_bridge': 140, 'type_mismatch': 140, 'typeclass_missing': 99}
- `topk_expansion`: {'missing_bridge': 457, 'rewrite_direction': 312, 'type_mismatch': 381, 'typeclass_missing': 256}
- `visible_feature_rerank`: {'missing_bridge': 76, 'type_mismatch': 72, 'typeclass_missing': 54, 'rewrite_direction': 68}
