# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `history_only` | 500 | 73.6% | 37.1% | 1.66 | 47.3 | 0.05s | 50.2% | 0.0% |
| `one_shot` | 500 | 58.0% | 0.0% | 1.00 | 28.9 | 0.03s | 42.0% | 0.0% |
| `random_retry` | 500 | 71.0% | 38.0% | 1.75 | 49.9 | 0.05s | 53.8% | 0.0% |
| `rule_far` | 500 | 100.0% | 100.0% | 1.42 | 29.4 | 0.04s | 29.6% | 0.0% |
| `topk_expansion` | 500 | 91.6% | 80.0% | 1.59 | 46.2 | 0.07s | 42.5% | 0.0% |

## Failure Type Counts

- `history_only`: {'timeout': 416, 'missing_bridge': 20, 'typeclass_missing': 3, 'type_mismatch': 18, 'rewrite_direction': 3}
- `one_shot`: {'timeout': 210}
- `random_retry`: {'timeout': 472, 'type_mismatch': 17, 'missing_bridge': 20, 'typeclass_missing': 5, 'rewrite_direction': 8}
- `rule_far`: {'timeout': 210}
- `topk_expansion`: {'timeout': 338}
