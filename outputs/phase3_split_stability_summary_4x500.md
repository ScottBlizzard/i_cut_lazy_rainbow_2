# Phase 3 Split-Stability Summary

## Per-Split Results

| Split | Policy | Success | FFR | Avg premises |
|---|---|---:|---:|---:|
| `original` | `learned_base_fallback` | 87.0% | 73.8% | 57.6 |
| `original` | `rule_far_learned_second_stage` | 92.4% | 84.7% | 53.9 |
| `original` | `rule_far_learned_second_stage_final_base_guardrail_8` | 92.6% | 85.1% | 53.9 |
| `fold0` | `learned_base_fallback` | 83.6% | 66.9% | 57.7 |
| `fold0` | `rule_far_learned_second_stage` | 91.6% | 83.1% | 54.3 |
| `fold0` | `rule_far_learned_second_stage_final_base_guardrail_8` | 91.6% | 83.1% | 54.3 |
| `fold1` | `learned_base_fallback` | 86.0% | 67.4% | 54.1 |
| `fold1` | `rule_far_learned_second_stage` | 92.2% | 81.9% | 51.3 |
| `fold1` | `rule_far_learned_second_stage_final_base_guardrail_8` | 93.4% | 84.7% | 51.3 |
| `fold2` | `learned_base_fallback` | 88.8% | 74.5% | 54.0 |
| `fold2` | `rule_far_learned_second_stage` | 94.0% | 86.4% | 50.7 |
| `fold2` | `rule_far_learned_second_stage_final_base_guardrail_8` | 94.0% | 86.4% | 50.7 |

## Aggregate

| Policy | Success mean | Success std | Success min-max | FFR mean | Avg premises mean |
|---|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 86.3% | 1.9 | 83.6%-88.8% | 70.7% | 55.9 |
| `rule_far_learned_second_stage` | 92.5% | 0.9 | 91.6%-94.0% | 84.0% | 52.5 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 92.9% | 0.9 | 91.6%-94.0% | 84.8% | 52.5 |
