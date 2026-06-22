# Mathlib 4.30 Aesop Exact Source/Channel Controls

Date: 2026-06-23

## Inputs

- Files: 690
- `outputs\mathlib430_aesop_exact_controls_oracle_core_only_essential1_g000.json`
- `outputs\mathlib430_aesop_exact_controls_oracle_core_only_essential1_g001.json`
- `outputs\mathlib430_aesop_exact_controls_oracle_core_only_essential1_g002.json`
- `outputs\mathlib430_aesop_exact_controls_oracle_core_only_essential1_g003.json`
- `outputs\mathlib430_aesop_exact_controls_oracle_core_only_essential1_g004.json`
- ...
- `outputs\mathlib430_aesop_exact_controls_retrieved_only_essential1_g225.json`
- `outputs\mathlib430_aesop_exact_controls_retrieved_only_essential1_g226.json`
- `outputs\mathlib430_aesop_exact_controls_retrieved_only_essential1_g227.json`
- `outputs\mathlib430_aesop_exact_controls_retrieved_only_essential1_g228.json`
- `outputs\mathlib430_aesop_exact_controls_retrieved_only_essential1_g229.json`

## Mode: `oracle_core_only`

- Goals: 230
- Attempts: 2070

| Action | Exposure | Success | Gain vs empty | Loss vs empty | Net | Avg facts | Avg simps |
|---|---|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | `typed-both` | 35/230 (15.2%) | 16 | 10 | 6 | 3.80 | 3.80 |
| `aesop_core_plus_learned_identity` | `identity-both` | 35/230 (15.2%) | 16 | 10 | 6 | 3.80 | 3.80 |
| `aesop_core_plus_learned_swapped` | `swapped` | 35/230 (15.2%) | 16 | 10 | 6 | 3.80 | 3.80 |
| `aesop_core_plus_learned_countmatched_simps` | `simps-only` | 33/230 (14.3%) | 14 | 10 | 4 | 0.00 | 3.80 |
| `aesop_core_plus_learned_simps` | `simps-only` | 33/230 (14.3%) | 14 | 10 | 4 | 0.00 | 3.80 |
| `aesop_core_plus_learned_random_split` | `random-split` | 32/230 (13.9%) | 9 | 6 | 3 | 1.83 | 1.97 |
| `aesop_core_plus_learned_countmatched_facts` | `facts-only` | 31/230 (13.5%) | 2 | 0 | 2 | 3.80 | 0.00 |
| `aesop_core_plus_learned_facts` | `facts-only` | 31/230 (13.5%) | 2 | 0 | 2 | 3.80 | 0.00 |
| `aesop_empty` | `empty` | 29/230 (12.6%) | - | - | - | 0.00 | 0.00 |

### Matched Triples

| Base | Joint | Facts | Simps | Identity | Swapped | Count facts | Count simps | Random split | Joint-only |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | 35 | 31 | 33 | 35 | 35 | 31 | 33 | 32 | 1 |

## Mode: `oracle_plus_retrieved`

- Goals: 230
- Attempts: 2070

| Action | Exposure | Success | Gain vs empty | Loss vs empty | Net | Avg facts | Avg simps |
|---|---|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | `typed-both` | 38/230 (16.5%) | 20 | 11 | 9 | 9.41 | 7.86 |
| `aesop_core_plus_learned_identity` | `identity-both` | 36/230 (15.7%) | 18 | 11 | 7 | 8.87 | 8.87 |
| `aesop_core_plus_learned_countmatched_simps` | `simps-only` | 35/230 (15.2%) | 17 | 11 | 6 | 0.00 | 12.09 |
| `aesop_core_plus_learned_simps` | `simps-only` | 35/230 (15.2%) | 17 | 11 | 6 | 0.00 | 7.86 |
| `aesop_core_plus_learned_swapped` | `swapped` | 33/230 (14.3%) | 14 | 10 | 4 | 7.86 | 9.41 |
| `aesop_core_plus_learned_countmatched_facts` | `facts-only` | 32/230 (13.9%) | 3 | 0 | 3 | 12.09 | 0.00 |
| `aesop_core_plus_learned_facts` | `facts-only` | 32/230 (13.9%) | 3 | 0 | 3 | 9.41 | 0.00 |
| `aesop_core_plus_learned_random_split` | `random-split` | 32/230 (13.9%) | 10 | 7 | 3 | 6.01 | 6.08 |
| `aesop_empty` | `empty` | 29/230 (12.6%) | - | - | - | 0.00 | 0.00 |

### Matched Triples

| Base | Joint | Facts | Simps | Identity | Swapped | Count facts | Count simps | Random split | Joint-only |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | 38 | 32 | 35 | 36 | 33 | 32 | 35 | 32 | 2 |

## Mode: `retrieved_only`

- Goals: 230
- Attempts: 2070

| Action | Exposure | Success | Gain vs empty | Loss vs empty | Net | Avg facts | Avg simps |
|---|---|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | `typed-both` | 34/230 (14.8%) | 16 | 11 | 5 | 6.58 | 6.92 |
| `aesop_core_plus_learned_countmatched_simps` | `simps-only` | 33/230 (14.3%) | 15 | 11 | 4 | 0.00 | 11.28 |
| `aesop_core_plus_learned_simps` | `simps-only` | 32/230 (13.9%) | 14 | 11 | 3 | 0.00 | 6.92 |
| `aesop_core_plus_learned_swapped` | `swapped` | 32/230 (13.9%) | 3 | 0 | 3 | 6.92 | 6.58 |
| `aesop_core_plus_learned_identity` | `identity-both` | 31/230 (13.5%) | 13 | 11 | 2 | 7.73 | 7.73 |
| `aesop_core_plus_learned_countmatched_facts` | `facts-only` | 30/230 (13.0%) | 1 | 0 | 1 | 11.28 | 0.00 |
| `aesop_core_plus_learned_facts` | `facts-only` | 30/230 (13.0%) | 1 | 0 | 1 | 6.58 | 0.00 |
| `aesop_core_plus_learned_random_split` | `random-split` | 29/230 (12.6%) | 7 | 7 | 0 | 5.65 | 5.63 |
| `aesop_empty` | `empty` | 29/230 (12.6%) | - | - | - | 0.00 | 0.00 |

### Matched Triples

| Base | Joint | Facts | Simps | Identity | Swapped | Count facts | Count simps | Random split | Joint-only |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | 34 | 30 | 32 | 31 | 32 | 30 | 33 | 29 | 1 |

## Readout

- Use this report to decide whether the Aesop mechanism is typed channel assignment, source composition, rule count, or identity exposure.
- Keep `oracle_core` wording unless the `retrieved_only` mode independently supports the same phenomenon.
