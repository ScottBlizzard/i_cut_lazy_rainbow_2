# Phase 3 Feedback-Causality Gate 0

This ablation tests whether the observed failure type causally affects the second-stage controller. All variants share the same first attempt and scored candidates; controls ignore or corrupt the observed failure type.

## Aggregate

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time |
|---|---:|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 2000 | 86.4% | 70.7% | 1.67 | 55.9 | 0.09s |
| `rule_far_learned_second_stage` | 2000 | 92.5% | 84.0% | 1.64 | 52.5 | 0.08s |
| `rule_far_learned_second_stage_cyclic` | 2000 | 79.4% | 55.7% | 1.74 | 55.8 | 0.09s |
| `rule_far_learned_second_stage_fixed_bridge` | 2000 | 81.3% | 59.8% | 1.72 | 54.9 | 0.09s |
| `rule_far_learned_second_stage_fixed_imported` | 2000 | 82.8% | 62.9% | 1.75 | 55.9 | 0.09s |
| `rule_far_learned_second_stage_fixed_type` | 2000 | 81.3% | 59.8% | 1.72 | 55.2 | 0.09s |
| `rule_far_learned_second_stage_shuffled` | 2000 | 85.0% | 67.9% | 1.73 | 55.5 | 0.09s |

## Gate Readout

- Best control: `learned_base_fallback` at 86.4%.
- True failure-conditioned policy delta over best control: +6.2 pp.
- Verdict: pass.

## Split Results

### original

| Policy | Goals | Verified success | First-failure recovery |
|---|---:|---:|---:|
| `learned_base_fallback` | 500 | 87.0% | 73.8% |
| `rule_far_learned_second_stage` | 500 | 92.4% | 84.7% |
| `rule_far_learned_second_stage_cyclic` | 500 | 78.6% | 56.9% |
| `rule_far_learned_second_stage_fixed_bridge` | 500 | 79.6% | 58.9% |
| `rule_far_learned_second_stage_fixed_imported` | 500 | 85.0% | 69.8% |
| `rule_far_learned_second_stage_fixed_type` | 500 | 79.4% | 58.5% |
| `rule_far_learned_second_stage_shuffled` | 500 | 84.2% | 68.1% |

First-attempt outcomes for the true-policy run:
- `initial_success`: 252
- `imported_premise_missing`: 151
- `missing_bridge`: 31
- `type_mismatch`: 28
- `rewrite_direction`: 21
- `typeclass_missing`: 17

### fold0

| Policy | Goals | Verified success | First-failure recovery |
|---|---:|---:|---:|
| `learned_base_fallback` | 500 | 83.6% | 66.9% |
| `rule_far_learned_second_stage` | 500 | 91.6% | 83.1% |
| `rule_far_learned_second_stage_cyclic` | 500 | 77.2% | 54.0% |
| `rule_far_learned_second_stage_fixed_bridge` | 500 | 79.4% | 58.5% |
| `rule_far_learned_second_stage_fixed_imported` | 500 | 80.2% | 60.1% |
| `rule_far_learned_second_stage_fixed_type` | 500 | 79.6% | 58.9% |
| `rule_far_learned_second_stage_shuffled` | 500 | 84.6% | 69.0% |

First-attempt outcomes for the true-policy run:
- `initial_success`: 252
- `imported_premise_missing`: 152
- `missing_bridge`: 34
- `type_mismatch`: 22
- `typeclass_missing`: 20
- `rewrite_direction`: 20

### fold1

| Policy | Goals | Verified success | First-failure recovery |
|---|---:|---:|---:|
| `learned_base_fallback` | 500 | 86.0% | 67.4% |
| `rule_far_learned_second_stage` | 500 | 92.2% | 81.9% |
| `rule_far_learned_second_stage_cyclic` | 500 | 81.0% | 55.8% |
| `rule_far_learned_second_stage_fixed_bridge` | 500 | 83.2% | 60.9% |
| `rule_far_learned_second_stage_fixed_imported` | 500 | 82.2% | 58.6% |
| `rule_far_learned_second_stage_fixed_type` | 500 | 83.2% | 60.9% |
| `rule_far_learned_second_stage_shuffled` | 500 | 85.8% | 67.0% |

First-attempt outcomes for the true-policy run:
- `initial_success`: 285
- `imported_premise_missing`: 122
- `missing_bridge`: 39
- `type_mismatch`: 21
- `typeclass_missing`: 20
- `rewrite_direction`: 13

### fold2

| Policy | Goals | Verified success | First-failure recovery |
|---|---:|---:|---:|
| `learned_base_fallback` | 500 | 88.8% | 74.5% |
| `rule_far_learned_second_stage` | 500 | 94.0% | 86.4% |
| `rule_far_learned_second_stage_cyclic` | 500 | 80.8% | 56.4% |
| `rule_far_learned_second_stage_fixed_bridge` | 500 | 83.0% | 61.4% |
| `rule_far_learned_second_stage_fixed_imported` | 500 | 83.6% | 62.7% |
| `rule_far_learned_second_stage_fixed_type` | 500 | 83.0% | 61.4% |
| `rule_far_learned_second_stage_shuffled` | 500 | 85.6% | 67.3% |

First-attempt outcomes for the true-policy run:
- `initial_success`: 280
- `imported_premise_missing`: 125
- `missing_bridge`: 31
- `rewrite_direction`: 23
- `typeclass_missing`: 21
- `type_mismatch`: 20
