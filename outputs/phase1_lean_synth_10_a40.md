# Phase 1 Analysis: phase1_real_fixed_budget

> Synthetic mock results validate the pipeline only; they are not paper evidence.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `one_shot` | 10 | 60.0% | 0.0% | 1.00 | 32.0 | 6.75s | 0.0% | 40.0% |
| `rule_far` | 10 | 100.0% | 100.0% | 1.40 | 34.1 | 11.27s | 0.0% | 28.6% |
| `topk_expansion` | 10 | 100.0% | 100.0% | 1.50 | 46.8 | 12.26s | 0.0% | 33.3% |

## Failure Type Counts

- `one_shot`: {'reconstruction_failure': 4}
- `rule_far`: {'reconstruction_failure': 4}
- `topk_expansion`: {'reconstruction_failure': 5}
