# Mathlib 4.30 Focused Aesop Ablation

Date: 2026-06-22

## Setup

- Ablation matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- Baseline matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_extended_merged.json`
- Goals: 230
- Aesop ablation actions: 22

## By Action

| Action | Source | Exposure | Verified goals | Attempts |
|---|---|---|---:|---:|
| `aesop_core_plus_learned` | `core+learned8` | `facts+simps` | 38 / 230 (16.5%) | 230 |
| `aesop_core_plus_learned16` | `core+learned16` | `facts+simps` | 37 / 230 (16.1%) | 230 |
| `aesop_empty` | `other` | `other` | 29 / 230 (12.6%) | 230 |
| `aesop_core_facts` | `core` | `facts-only` | 5 / 230 (2.2%) | 230 |
| `aesop_core_plus_learned16_facts` | `core+learned16` | `facts-only` | 5 / 230 (2.2%) | 230 |
| `aesop_core_plus_learned32_facts` | `core+learned32` | `facts-only` | 5 / 230 (2.2%) | 230 |
| `aesop_core_plus_learned_facts` | `core+learned8` | `facts-only` | 5 / 230 (2.2%) | 230 |
| `aesop_learned16_facts` | `learned16` | `facts-only` | 5 / 230 (2.2%) | 230 |
| `aesop_learned32_facts` | `learned32` | `facts-only` | 5 / 230 (2.2%) | 230 |
| `aesop_learned8_facts` | `learned8` | `facts-only` | 5 / 230 (2.2%) | 230 |
| `aesop_core` | `core` | `facts+simps` | 4 / 230 (1.7%) | 230 |
| `aesop_core_plus_learned_simps` | `core+learned8` | `simps-only` | 4 / 230 (1.7%) | 230 |
| `aesop_core_simps` | `core` | `simps-only` | 4 / 230 (1.7%) | 230 |
| `aesop_learned8` | `learned8` | `facts+simps` | 4 / 230 (1.7%) | 230 |
| `aesop_learned8_simps` | `learned8` | `simps-only` | 4 / 230 (1.7%) | 230 |
| `aesop_core_plus_learned16_simps` | `core+learned16` | `simps-only` | 3 / 230 (1.3%) | 230 |
| `aesop_core_plus_learned32` | `core+learned32` | `facts+simps` | 3 / 230 (1.3%) | 230 |
| `aesop_core_plus_learned32_simps` | `core+learned32` | `simps-only` | 3 / 230 (1.3%) | 230 |
| `aesop_learned16` | `learned16` | `facts+simps` | 3 / 230 (1.3%) | 230 |
| `aesop_learned16_simps` | `learned16` | `simps-only` | 3 / 230 (1.3%) | 230 |
| `aesop_learned32` | `learned32` | `facts+simps` | 3 / 230 (1.3%) | 230 |
| `aesop_learned32_simps` | `learned32` | `simps-only` | 3 / 230 (1.3%) | 230 |

## By Source

| Source pool | Goals solved by at least one action |
|---|---:|
| `core+learned16` | 41 / 230 (17.8%) |
| `core+learned8` | 41 / 230 (17.8%) |
| `other` | 29 / 230 (12.6%) |
| `core` | 7 / 230 (3.0%) |
| `core+learned32` | 7 / 230 (3.0%) |
| `learned16` | 7 / 230 (3.0%) |
| `learned32` | 7 / 230 (3.0%) |
| `learned8` | 7 / 230 (3.0%) |

## By Exposure

| Exposure | Goals solved by at least one action |
|---|---:|
| `facts+simps` | 38 / 230 (16.5%) |
| `other` | 29 / 230 (12.6%) |
| `facts-only` | 5 / 230 (2.2%) |
| `simps-only` | 4 / 230 (1.7%) |

## New Goals Over Baseline

- None.

## Readout

- This report isolates whether Aesop gains come from fact rules, simp rules, or their combination.
- Use it to decide whether the final method should expose selected names to Aesop as facts, simp lemmas, or both.
