# Mathlib 4.30 E1 Strict Interface Filtering

Date: 2026-06-22

## Setup

- Baseline matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- Filtered part: `outputs\mathlib430_pretheorem_action_matrix_e1_filtered230_part0.json`
- Filtered part: `outputs\mathlib430_pretheorem_action_matrix_e1_filtered230_part1.json`
- Filter mode: `strict_aesop`
- Filtered actions use suffix: `_filtered`

## Oracle Readout

| Metric | Count |
|---|---:|
| Baseline oracle | 58 / 230 (25.2%) |
| Filtered-only oracle | 4 / 230 (1.7%) |
| Combined oracle | 58 / 230 (25.2%) |
| New oracle goals from filtering | 0 |

## Filtered Actions

| Filtered action | Source action | Filtered goals | Source goals | Kept | New vs source | Lost vs source |
|---|---|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned16_filtered` | `aesop_core_plus_learned16` | 3 | 37 | 1 | 2 | 36 |
| `aesop_core_plus_learned_filtered` | `aesop_core_plus_learned` | 3 | 38 | 1 | 2 | 37 |
| `hammer_core_plus_learned16_filtered` | `hammer_core_plus_learned16` | 3 | 32 | 3 | 0 | 29 |
| `hammerCore_core_plus_learned_filtered` | `hammerCore_core_plus_learned` | 1 | 18 | 1 | 0 | 17 |

## New Oracle Goals

- None.

## Candidate Audit

| Metric | Count |
|---|---:|
| `aesop_safe_fact_available` | 4702 |
| `aesop_unsafe_fact_available` | 2619 |
| `available` | 7321 |
| `learned_candidate` | 7360 |
| `proof_core` | 875 |
| `selected` | 7497 |
| `simp_safe_available` | 2009 |
| `simp_unsafe_available` | 5312 |
| `target_or_alias` | 24 |
| `unavailable` | 176 |

### By Category

| Category | Count |
|---|---:|
| `theorem_like` | 3268 |
| `simp_attr` | 1927 |
| `definition_like` | 1880 |
| `class` | 161 |
| `proof_core_only_unknown` | 137 |
| `structure` | 101 |
| `inductive` | 10 |
| `unknown` | 10 |
| `instance` | 3 |

### By Decl Kind

| Decl kind | Count |
|---|---:|
| `theorem` | 3673 |
| `def` | 1956 |
| `lemma` | 1180 |
| `abbrev` | 266 |
| `class` | 161 |
| `proof_core_only` | 137 |
| `structure` | 101 |
| `inductive` | 10 |
| `unknown` | 10 |
| `instance` | 3 |

## Readout

- Filtering does not raise oracle headroom, but it provides a cleaner robustness/mechanism audit.
