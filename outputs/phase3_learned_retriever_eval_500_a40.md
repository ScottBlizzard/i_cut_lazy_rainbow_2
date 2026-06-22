# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bm25_expansion` | 500 | 12.8% | 8.4% | 2.86 | 91.5 | 0.18s | 0.0% | 0.0% |
| `bm25_rerank` | 500 | 8.2% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `bm25_same_file_prior_expansion` | 500 | 12.8% | 8.6% | 2.86 | 91.6 | 0.18s | 0.0% | 0.0% |
| `leansearch_iterative` | 500 | 12.2% | 7.8% | 2.86 | 91.4 | 0.18s | 0.0% | 0.0% |
| `learned_expansion` | 500 | 84.0% | 67.7% | 1.80 | 57.7 | 0.09s | 0.0% | 0.0% |
| `learned_rerank` | 500 | 64.2% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `one_shot` | 500 | 1.4% | 0.0% | 1.00 | 32.0 | 0.03s | 0.0% | 0.0% |
| `rule_far_bm25` | 500 | 13.0% | 8.8% | 2.86 | 91.5 | 0.18s | 0.0% | 0.0% |
| `rule_far_full` | 500 | 55.6% | 55.0% | 2.54 | 86.6 | 0.14s | 0.0% | 0.0% |
| `rule_far_learned` | 500 | 84.4% | 68.5% | 1.79 | 57.4 | 0.09s | 0.0% | 0.0% |
| `rule_far_no_core_tags` | 500 | 4.6% | 3.2% | 2.96 | 94.8 | 0.18s | 0.0% | 0.0% |
| `same_file_prior_rerank` | 500 | 2.8% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `topk_equal_budget` | 500 | 1.6% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `visible_feature_rerank` | 500 | 2.4% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |

## Failure Type Counts

- `bm25_expansion`: {'imported_premise_missing': 1346, 'type_mismatch': 8, 'missing_bridge': 2, 'typeclass_missing': 5, 'rewrite_direction': 4}
- `bm25_rerank`: {'imported_premise_missing': 454, 'type_mismatch': 3, 'typeclass_missing': 1, 'rewrite_direction': 1}
- `bm25_same_file_prior_expansion`: {'imported_premise_missing': 1354, 'type_mismatch': 5, 'missing_bridge': 1, 'typeclass_missing': 4, 'rewrite_direction': 4}
- `leansearch_iterative`: {'imported_premise_missing': 1351, 'type_mismatch': 7, 'typeclass_missing': 5, 'missing_bridge': 2, 'rewrite_direction': 2}
- `learned_expansion`: {'type_mismatch': 71, 'missing_bridge': 60, 'imported_premise_missing': 272, 'rewrite_direction': 48, 'typeclass_missing': 31}
- `learned_rerank`: {'type_mismatch': 26, 'missing_bridge': 27, 'imported_premise_missing': 97, 'rewrite_direction': 18, 'typeclass_missing': 11}
- `one_shot`: {'imported_premise_missing': 488, 'type_mismatch': 3, 'missing_bridge': 1, 'rewrite_direction': 1}
- `rule_far_bm25`: {'imported_premise_missing': 1343, 'type_mismatch': 9, 'missing_bridge': 1, 'typeclass_missing': 7, 'rewrite_direction': 4}
- `rule_far_full`: {'imported_premise_missing': 692, 'missing_bridge': 98, 'typeclass_missing': 49, 'type_mismatch': 104, 'rewrite_direction': 49}
- `rule_far_learned`: {'type_mismatch': 72, 'missing_bridge': 58, 'imported_premise_missing': 265, 'rewrite_direction': 49, 'typeclass_missing': 31}
- `rule_far_no_core_tags`: {'imported_premise_missing': 1429, 'type_mismatch': 13, 'missing_bridge': 5, 'rewrite_direction': 5, 'typeclass_missing': 3}
- `same_file_prior_rerank`: {'imported_premise_missing': 484, 'type_mismatch': 1, 'typeclass_missing': 1}
- `topk_equal_budget`: {'imported_premise_missing': 485, 'type_mismatch': 4, 'typeclass_missing': 1, 'missing_bridge': 1, 'rewrite_direction': 1}
- `visible_feature_rerank`: {'imported_premise_missing': 481, 'type_mismatch': 4, 'typeclass_missing': 1, 'missing_bridge': 1, 'rewrite_direction': 1}
