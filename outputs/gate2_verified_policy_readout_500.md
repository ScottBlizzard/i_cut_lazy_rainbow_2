# Gate 2 Verified Policy Readout

This report converts the verified action-grid outcomes into policy-level comparisons.

| Policy | Goals | Verified | Success | Avg premises | Avg time | Action counts |
|---|---:|---:|---:|---:|---:|---|
| `verified_true_feedback_policy` | 500 | 400 | 80.0% | 7.8 | 3.88s | `{'expand_150': 100, 'expand_200': 200, 'base_rescue_8': 100, 'second_stage_rescore': 100}` |
| `oracle_adaptive_action` | 500 | 400 | 80.0% | 6.6 | 3.11s | `{'expand_150': 100, 'expand_200': 100, 'base_rescue_8': 100, 'second_stage_rescore': 100, 'stop': 100}` |
| `masked_best_static` | 500 | 200 | 40.0% | 6.0 | 3.88s | `{'expand_200': 500}` |
| `shuffled_feedback_policy` | 500 | 138 | 27.6% | 7.7 | 3.88s | `{'second_stage_rescore': 95, 'expand_150': 114, 'base_rescue_8': 99, 'expand_200': 192}` |
| `fixed_keep` | 500 | 0 | 0.0% | 3.0 | 3.87s | `{'keep': 500}` |
| `fixed_expand_150` | 500 | 100 | 20.0% | 5.0 | 3.88s | `{'expand_150': 500}` |
| `fixed_expand_200` | 500 | 200 | 40.0% | 6.0 | 3.88s | `{'expand_200': 500}` |
| `fixed_base_rescue_8` | 500 | 100 | 20.0% | 11.0 | 3.88s | `{'base_rescue_8': 500}` |
| `fixed_second_stage_rescore` | 500 | 100 | 20.0% | 11.0 | 3.88s | `{'second_stage_rescore': 500}` |

## Gate Readout

- Best static: `fixed_expand_200` at 40.0%.
- True feedback policy: 80.0%.
- Oracle adaptive action: 80.0%.
- True minus best static: +40.0 pp.
- True minus masked best-static: +40.0 pp.
- True minus shuffled feedback: +52.4 pp.

Caveat: the policy signal here is synthetic family metadata, not a learned Mathlib failure-transcript model. Use this as pipeline validation, not paper evidence.
