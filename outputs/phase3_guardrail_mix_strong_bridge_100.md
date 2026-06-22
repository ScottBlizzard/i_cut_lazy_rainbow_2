# Phase 1 Analysis: phase1_mathlib_trace_core

> Trace-grounded Mathlib results evaluate proof-core recovery, not full proof reconstruction.

| Policy | Goals | Verified success | First-failure recovery | Avg attempts | Avg premises | Avg time | Timeout rate | Recon-fail rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `rule_far_learned_second_stage` | 100 | 72.0% | 68.5% | 2.48 | 79.4 | 0.15s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_base_mix_200` | 100 | 71.0% | 67.4% | 2.46 | 78.7 | 0.14s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_base_mix_400` | 100 | 69.0% | 65.2% | 2.45 | 78.4 | 0.14s | 0.0% | 0.0% |
| `rule_far_learned_second_stage_base_mix_800` | 100 | 63.0% | 58.4% | 2.41 | 77.1 | 0.14s | 0.0% | 0.0% |

## Failure Type Counts

- `rule_far_learned_second_stage`: {'imported_premise_missing': 131, 'type_mismatch': 21, 'rewrite_direction': 9, 'missing_bridge': 13, 'typeclass_missing': 2}
- `rule_far_learned_second_stage_base_mix_200`: {'imported_premise_missing': 132, 'type_mismatch': 20, 'rewrite_direction': 9, 'missing_bridge': 12, 'typeclass_missing': 2}
- `rule_far_learned_second_stage_base_mix_400`: {'imported_premise_missing': 135, 'type_mismatch': 18, 'missing_bridge': 12, 'rewrite_direction': 9, 'typeclass_missing': 2}
- `rule_far_learned_second_stage_base_mix_800`: {'imported_premise_missing': 141, 'type_mismatch': 15, 'rewrite_direction': 8, 'missing_bridge': 11, 'typeclass_missing': 3}
