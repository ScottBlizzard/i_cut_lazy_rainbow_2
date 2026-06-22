# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `learned_base_fallback` | 500 | 87.0% | 73.8% | 1.73 | 57.6 | 0.09s | 0.0% | 0.0% |
| `rule_far_learned_second_stage` | 500 | 92.4% | 84.7% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_base_guardrail_small` | 500 | 92.2% | 84.3% | 1.69 | 54.0 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_base_mix_200` | 500 | 91.6% | 83.1% | 1.71 | 54.6 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_16` | 500 | 92.2% | 84.3% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 500 | 92.6% | 85.1% | 1.68 | 53.9 | 0.08s | 0.0% | 0.0% |

## Failure Type Counts

- `learned_base_fallback`: {'type_mismatch': 56, 'missing_bridge': 45, 'imported_premise_missing': 278, 'typeclass_missing': 21, 'rewrite_direction': 28}
- `rule_far_learned_second_stage`: {'type_mismatch': 40, 'missing_bridge': 35, 'imported_premise_missing': 258, 'rewrite_direction': 25, 'typeclass_missing': 22}
- `rule_far_learned_second_stage_base_guardrail_small`: {'type_mismatch': 39, 'missing_bridge': 33, 'imported_premise_missing': 265, 'typeclass_missing': 22, 'rewrite_direction': 24}
- `rule_far_learned_second_stage_base_mix_200`: {'type_mismatch': 39, 'missing_bridge': 34, 'imported_premise_missing': 277, 'typeclass_missing': 21, 'rewrite_direction': 24}
- `rule_far_learned_second_stage_final_base_guardrail_16`: {'type_mismatch': 39, 'missing_bridge': 34, 'imported_premise_missing': 261, 'rewrite_direction': 25, 'typeclass_missing': 22}
- `rule_far_learned_second_stage_final_base_guardrail_8`: {'type_mismatch': 39, 'missing_bridge': 34, 'imported_premise_missing': 259, 'rewrite_direction': 25, 'typeclass_missing': 22}
