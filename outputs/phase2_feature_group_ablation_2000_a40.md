# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `one_shot` | 2000 | 58.0% | 0.0% | 1.00 | 28.4 | 0.03s | 0.0% | 0.0% |
| `rule_far_failure_type_only` | 2000 | 91.5% | 79.9% | 1.62 | 46.9 | 0.07s | 0.0% | 0.0% |
| `rule_far_full` | 2000 | 98.3% | 96.0% | 1.47 | 42.9 | 0.06s | 0.0% | 0.0% |
| `rule_far_no_core_decl_features` | 2000 | 92.6% | 82.4% | 1.59 | 46.2 | 0.07s | 0.0% | 0.0% |
| `rule_far_no_core_name_features` | 2000 | 95.0% | 88.1% | 1.54 | 45.4 | 0.07s | 0.0% | 0.0% |
| `rule_far_no_core_name_statement_features` | 2000 | 95.2% | 88.6% | 1.54 | 45.4 | 0.07s | 0.0% | 0.0% |
| `rule_far_no_core_statement_features` | 2000 | 92.8% | 82.9% | 1.60 | 46.4 | 0.07s | 0.0% | 0.0% |
| `rule_far_no_core_tags` | 2000 | 95.7% | 89.7% | 1.52 | 45.1 | 0.06s | 0.0% | 0.0% |
| `topk_equal_budget` | 2000 | 75.7% | 0.0% | 1.00 | 42.9 | 0.04s | 0.0% | 0.0% |
| `topk_expansion` | 2000 | 91.5% | 79.9% | 1.62 | 46.9 | 0.07s | 0.0% | 0.0% |
| `visible_feature_decl_rerank` | 2000 | 78.3% | 0.0% | 1.00 | 42.9 | 0.04s | 0.0% | 0.0% |
| `visible_feature_name_rerank` | 2000 | 85.3% | 0.0% | 1.00 | 42.9 | 0.04s | 0.0% | 0.0% |
| `visible_feature_name_statement_rerank` | 2000 | 85.2% | 0.0% | 1.00 | 42.9 | 0.04s | 0.0% | 0.0% |
| `visible_feature_rerank` | 2000 | 86.5% | 0.0% | 1.00 | 42.9 | 0.04s | 0.0% | 0.0% |
| `visible_feature_statement_rerank` | 2000 | 77.6% | 0.0% | 1.00 | 42.9 | 0.04s | 0.0% | 0.0% |

## Failure Type Counts

- `one_shot`: {'missing_bridge': 286, 'rewrite_direction': 183, 'type_mismatch': 227, 'typeclass_missing': 145}
- `rule_far_failure_type_only`: {'missing_bridge': 457, 'rewrite_direction': 312, 'type_mismatch': 381, 'typeclass_missing': 256}
- `rule_far_full`: {'missing_bridge': 301, 'rewrite_direction': 250, 'type_mismatch': 246, 'typeclass_missing': 177}
- `rule_far_no_core_decl_features`: {'missing_bridge': 426, 'rewrite_direction': 306, 'type_mismatch': 364, 'typeclass_missing': 239}
- `rule_far_no_core_name_features`: {'missing_bridge': 372, 'rewrite_direction': 273, 'type_mismatch': 325, 'typeclass_missing': 208}
- `rule_far_no_core_name_statement_features`: {'missing_bridge': 373, 'rewrite_direction': 268, 'type_mismatch': 321, 'typeclass_missing': 205}
- `rule_far_no_core_statement_features`: {'missing_bridge': 422, 'rewrite_direction': 303, 'type_mismatch': 380, 'typeclass_missing': 248}
- `rule_far_no_core_tags`: {'missing_bridge': 359, 'rewrite_direction': 268, 'type_mismatch': 310, 'typeclass_missing': 197}
- `topk_equal_budget`: {'rewrite_direction': 107, 'missing_bridge': 140, 'type_mismatch': 140, 'typeclass_missing': 99}
- `topk_expansion`: {'missing_bridge': 457, 'rewrite_direction': 312, 'type_mismatch': 381, 'typeclass_missing': 256}
- `visible_feature_decl_rerank`: {'rewrite_direction': 95, 'missing_bridge': 126, 'type_mismatch': 127, 'typeclass_missing': 86}
- `visible_feature_name_rerank`: {'missing_bridge': 83, 'type_mismatch': 76, 'typeclass_missing': 61, 'rewrite_direction': 74}
- `visible_feature_name_statement_rerank`: {'missing_bridge': 86, 'type_mismatch': 75, 'typeclass_missing': 61, 'rewrite_direction': 75}
- `visible_feature_rerank`: {'missing_bridge': 76, 'type_mismatch': 72, 'typeclass_missing': 54, 'rewrite_direction': 68}
- `visible_feature_statement_rerank`: {'rewrite_direction': 96, 'missing_bridge': 134, 'type_mismatch': 125, 'typeclass_missing': 93}
