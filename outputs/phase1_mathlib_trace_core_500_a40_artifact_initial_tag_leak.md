# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `history_only` | 500 | 100.0% | 0.0% | 1.00 | 28.9 | 0.03s | 0.0% | 0.0% |
| `one_shot` | 500 | 58.0% | 0.0% | 1.00 | 28.9 | 0.03s | 42.0% | 0.0% |
| `random_retry` | 500 | 71.0% | 38.0% | 1.75 | 49.9 | 0.05s | 53.8% | 0.0% |
| `rule_far` | 500 | 100.0% | 100.0% | 1.09 | 28.9 | 0.03s | 7.9% | 0.0% |
| `topk_expansion` | 500 | 91.6% | 80.0% | 1.59 | 46.2 | 0.07s | 42.5% | 0.0% |

## Failure Type Counts

- `history_only`: {}
- `one_shot`: {'timeout': 210}
- `random_retry`: {'timeout': 472, 'type_mismatch': 17, 'missing_bridge': 20, 'typeclass_missing': 5, 'rewrite_direction': 8}
- `rule_far`: {'timeout': 43}
- `topk_expansion`: {'timeout': 338}
