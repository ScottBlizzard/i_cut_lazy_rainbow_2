# Phase 1 Analysis: phase1_synthetic_smoke

> Synthetic mock results validate the pipeline only; they are not paper evidence.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `history_only` | 100 | 23.0% | 2.5% | 2.57 | 82.2 | 0.60s | 0.0% | 60.7% |
| `one_shot` | 100 | 4.0% | 0.0% | 1.00 | 32.0 | 2.22s | 20.0% | 17.0% |
| `random_retry` | 100 | 0.0% | 0.0% | 3.00 | 96.0 | 0.70s | 0.0% | 0.0% |
| `rule_far` | 100 | 85.0% | 82.8% | 2.28 | 50.1 | 2.52s | 9.2% | 27.6% |
| `topk_expansion` | 100 | 4.0% | 0.0% | 2.92 | 93.4 | 13.81s | 45.2% | 8.6% |

## Failure Type Counts

- `history_only`: {'reconstruction_failure': 156, 'missing_bridge': 35, 'local_context_missing': 43}
- `one_shot`: {'missing_bridge': 29, 'reconstruction_failure': 17, 'local_context_missing': 30, 'timeout': 20}
- `random_retry`: {'missing_bridge': 184, 'local_context_missing': 116}
- `rule_far`: {'reconstruction_failure': 63, 'missing_bridge': 31, 'local_context_missing': 28, 'timeout': 21}
- `topk_expansion`: {'missing_bridge': 60, 'timeout': 132, 'reconstruction_failure': 25, 'local_context_missing': 71}
