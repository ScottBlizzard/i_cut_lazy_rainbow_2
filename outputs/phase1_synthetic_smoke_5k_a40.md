# Phase 1 Analysis: phase1_synthetic_smoke

> Synthetic mock results validate the pipeline only; they are not paper evidence.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `history_only` | 5000 | 18.6% | 2.1% | 2.65 | 84.9 | 0.62s | 0.0% | 59.1% |
| `one_shot` | 5000 | 3.4% | 0.0% | 1.00 | 32.0 | 1.86s | 16.4% | 19.9% |
| `random_retry` | 5000 | 0.3% | 0.2% | 3.00 | 95.9 | 0.70s | 0.0% | 0.1% |
| `rule_far` | 5000 | 87.5% | 85.8% | 2.30 | 49.9 | 2.60s | 9.5% | 25.9% |
| `topk_expansion` | 5000 | 3.5% | 0.0% | 2.93 | 93.8 | 12.65s | 40.9% | 9.3% |

## Failure Type Counts

- `history_only`: {'local_context_missing': 2800, 'reconstruction_failure': 7838, 'missing_bridge': 1693}
- `one_shot`: {'local_context_missing': 1585, 'timeout': 822, 'missing_bridge': 1425, 'reconstruction_failure': 997}
- `random_retry`: {'missing_bridge': 9755, 'local_context_missing': 5214, 'reconstruction_failure': 8, 'timeout': 1}
- `rule_far`: {'local_context_missing': 1548, 'reconstruction_failure': 2978, 'missing_bridge': 1496, 'timeout': 1096}
- `topk_expansion`: {'local_context_missing': 4152, 'timeout': 5988, 'missing_bridge': 2976, 'reconstruction_failure': 1367}
