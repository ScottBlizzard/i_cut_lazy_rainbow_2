# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bm25_expansion` | 2000 | 11.9% | 8.3% | 2.88 | 92.2 | 0.18s | 0.0% | 0.0% |
| `bm25_rerank` | 2000 | 7.0% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `bm25_same_file_prior_expansion` | 2000 | 12.0% | 8.6% | 2.88 | 92.3 | 0.18s | 0.0% | 0.0% |
| `bm25_same_file_prior_rerank` | 2000 | 7.0% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `leansearch_iterative` | 2000 | 11.9% | 8.3% | 2.87 | 91.9 | 0.18s | 0.0% | 0.0% |
| `one_shot` | 2000 | 1.1% | 0.0% | 1.00 | 32.0 | 0.03s | 0.0% | 0.0% |
| `rule_far_bm25` | 2000 | 12.2% | 8.7% | 2.88 | 92.2 | 0.18s | 0.0% | 0.0% |
| `rule_far_failure_type_only` | 2000 | 3.1% | 2.0% | 2.97 | 95.1 | 0.19s | 0.0% | 0.0% |
| `rule_far_full` | 2000 | 55.7% | 55.2% | 2.53 | 86.6 | 0.14s | 0.0% | 0.0% |
| `rule_far_no_core_tags` | 2000 | 4.7% | 3.6% | 2.96 | 94.9 | 0.18s | 0.0% | 0.0% |
| `same_file_prior_expansion` | 2000 | 4.0% | 2.9% | 2.96 | 94.8 | 0.19s | 0.0% | 0.0% |
| `same_file_prior_rerank` | 2000 | 2.1% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `topk_equal_budget` | 2000 | 1.6% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |
| `topk_expansion` | 2000 | 3.1% | 2.0% | 2.97 | 95.1 | 0.19s | 0.0% | 0.0% |
| `visible_feature_rerank` | 2000 | 2.4% | 0.0% | 1.00 | 56.0 | 0.06s | 0.0% | 0.0% |

## Failure Type Counts

- `bm25_expansion`: {'imported_premise_missing': 5406, 'missing_bridge': 28, 'rewrite_direction': 32, 'type_mismatch': 32, 'typeclass_missing': 27}
- `bm25_rerank`: {'imported_premise_missing': 1824, 'missing_bridge': 10, 'rewrite_direction': 10, 'typeclass_missing': 6, 'type_mismatch': 9}
- `bm25_same_file_prior_expansion`: {'imported_premise_missing': 5437, 'missing_bridge': 24, 'rewrite_direction': 24, 'type_mismatch': 27, 'typeclass_missing': 18}
- `bm25_same_file_prior_rerank`: {'imported_premise_missing': 1830, 'missing_bridge': 8, 'rewrite_direction': 8, 'typeclass_missing': 5, 'type_mismatch': 8}
- `leansearch_iterative`: {'imported_premise_missing': 5408, 'missing_bridge': 27, 'rewrite_direction': 26, 'type_mismatch': 25, 'typeclass_missing': 21}
- `one_shot`: {'imported_premise_missing': 1966, 'missing_bridge': 6, 'type_mismatch': 4, 'rewrite_direction': 2}
- `rule_far_bm25`: {'imported_premise_missing': 5399, 'missing_bridge': 27, 'rewrite_direction': 32, 'type_mismatch': 32, 'typeclass_missing': 26}
- `rule_far_failure_type_only`: {'imported_premise_missing': 5832, 'missing_bridge': 14, 'type_mismatch': 19, 'typeclass_missing': 7, 'rewrite_direction': 7}
- `rule_far_full`: {'imported_premise_missing': 2787, 'missing_bridge': 407, 'type_mismatch': 334, 'typeclass_missing': 193, 'rewrite_direction': 231}
- `rule_far_no_core_tags`: {'imported_premise_missing': 5728, 'typeclass_missing': 20, 'missing_bridge': 29, 'type_mismatch': 29, 'rewrite_direction': 13}
- `same_file_prior_expansion`: {'imported_premise_missing': 5820, 'missing_bridge': 6, 'type_mismatch': 7, 'typeclass_missing': 8, 'rewrite_direction': 6}
- `same_file_prior_rerank`: {'imported_premise_missing': 1947, 'missing_bridge': 3, 'type_mismatch': 2, 'typeclass_missing': 4, 'rewrite_direction': 1}
- `topk_equal_budget`: {'imported_premise_missing': 1955, 'missing_bridge': 5, 'type_mismatch': 6, 'rewrite_direction': 2, 'typeclass_missing': 1}
- `topk_expansion`: {'imported_premise_missing': 5832, 'missing_bridge': 14, 'type_mismatch': 19, 'typeclass_missing': 7, 'rewrite_direction': 7}
- `visible_feature_rerank`: {'imported_premise_missing': 1932, 'missing_bridge': 6, 'type_mismatch': 6, 'typeclass_missing': 5, 'rewrite_direction': 3}
