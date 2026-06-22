# Mathlib 4.30 Evidence Contract Audit

Date: 2026-06-23

Supersession note: the Aesop channel-causal interpretation in this audit was
stress-tested by the later exact singleton P0 controls in
`analysis/mathlib430_aesop_exact_controls_summary.md`. The exact P0 controls
supersede the earlier broad-ablation wording: the supported readout is modest
source/exposure/search sensitivity, not a large isolated facts-versus-simps
complementarity effect.

## Inputs

- `outputs\mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json` (`sha256=b4cd35366ebe...`)
- `outputs\mathlib430_replayable490_splits.json` (`sha256=c4dff90b6ce6...`)
- `outputs\mathlib430_clean_trace_subset_500.jsonl` (`sha256=3ee697f63ab0...`)
- Goals: 230
- Matrix attempts: 11500

## Protocol Readout

- `core` in the current action names is traced `proof_core`; this audit therefore relabels it as `oracle_core` in interpretation.
- Current headline results should be described as a mechanism-isolation setting over oracle-core plus retrieved evidence, not as a deployable retriever-only premise selector.
- Existing timing is runner wallclock per Lean attempt. It supports matched Lean-call and empirical wallclock frontier wording, but not a formal heartbeat-normalized compute claim.

## Trace Provenance

| Quantity per goal | Mean | Median | Sum |
|---|---:|---:|---:|
| `proof_core` | 3.80 | 3.0 | 875 |
| `retrieved_top8` | 8.00 | 8.0 | 1840 |
| `retrieved_top32` | 32.00 | 32.0 | 7360 |
| `proof_core_in_top8` | 2.40 | 2.0 | 552 |
| `proof_core_in_top32` | 3.21 | 3.0 | 738 |
| `proof_core_only_top32` | 0.60 | 0.0 | 137 |

## Action Provenance

| Action | Verified | Avg facts | Avg simps | Oracle-core names | Retrieved top-8 names | Retrieved top-32 names | Unknown | Avg time(s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | 38 | 9.41 | 7.86 | 1750 | 1898 | 3697 | 0 | 8.92 |
| `aesop_core_plus_learned16` | 37 | 12.88 | 10.40 | 1750 | 1898 | 5081 | 0 | 9.41 |
| `hammer_core_plus_learned16` | 32 | 12.88 | 0.00 | 875 | 864 | 2825 | 0 | 8.56 |
| `hammer_core_plus_learned32` | 32 | 14.05 | 0.00 | 875 | 864 | 3095 | 0 | 8.55 |
| `hammer_core_plus_learned` | 31 | 9.41 | 0.00 | 875 | 864 | 2027 | 0 | 8.67 |
| `aesop_empty` | 29 | 0.00 | 0.00 | 0 | 0 | 0 | 0 | 7.99 |
| `hammer_core_facts` | 29 | 3.80 | 0.00 | 875 | 552 | 738 | 0 | 8.50 |
| `hammer_empty` | 29 | 0.00 | 0.00 | 0 | 0 | 0 | 0 | 8.31 |
| `hammerCore_core_plus_learned` | 18 | 9.41 | 7.86 | 1750 | 1898 | 3697 | 0 | 13.29 |
| `simp_all_core_plus_learned16` | 18 | 0.00 | 10.40 | 875 | 1034 | 2256 | 0 | 8.17 |
| `simp_all_core_plus_learned32` | 18 | 0.00 | 10.97 | 875 | 1034 | 2386 | 0 | 8.19 |
| `simp_all_core_plus_learned` | 17 | 0.00 | 7.86 | 875 | 1034 | 1670 | 0 | 8.34 |
| `simp_core_plus_learned` | 16 | 0.00 | 7.86 | 875 | 1034 | 1670 | 0 | 8.08 |
| `simpa_core_plus_learned` | 16 | 0.00 | 7.86 | 875 | 1034 | 1670 | 0 | 8.06 |
| `hammerCore_core_plus_learned16` | 15 | 12.88 | 10.40 | 1750 | 1898 | 5081 | 0 | 12.88 |
| `hammerCore_core_plus_learned32` | 15 | 14.05 | 10.97 | 1750 | 1898 | 5481 | 0 | 12.80 |
| `hammerCore_core` | 14 | 3.80 | 3.80 | 1750 | 1104 | 1476 | 0 | 12.03 |
| `simp_all_core` | 14 | 0.00 | 3.80 | 875 | 552 | 738 | 0 | 8.36 |
| `simp_core` | 14 | 0.00 | 3.80 | 875 | 552 | 738 | 0 | 8.07 |
| `simpa_core` | 14 | 0.00 | 3.80 | 875 | 552 | 738 | 0 | 8.05 |
| `solve_by_elim_core` | 11 | 3.80 | 0.00 | 875 | 552 | 738 | 0 | 8.83 |
| `solve_by_elim_core_plus_learned` | 11 | 9.41 | 0.00 | 875 | 864 | 2027 | 0 | 9.42 |
| `solve_by_elim_core_plus_learned16` | 11 | 12.88 | 0.00 | 875 | 864 | 2825 | 0 | 9.83 |
| `solve_by_elim_core_plus_learned32` | 11 | 14.05 | 0.00 | 875 | 864 | 3095 | 0 | 9.87 |
| `simp_empty` | 6 | 0.00 | 0.00 | 0 | 0 | 0 | 0 | 7.75 |
| `simpa_empty` | 6 | 0.00 | 0.00 | 0 | 0 | 0 | 0 | 7.81 |
| `aesop_core_facts` | 5 | 3.80 | 0.00 | 875 | 552 | 738 | 0 | 2.39 |
| `aesop_core_plus_learned16_facts` | 5 | 12.88 | 0.00 | 875 | 864 | 2825 | 0 | 2.50 |
| `aesop_core_plus_learned32_facts` | 5 | 14.05 | 0.00 | 875 | 864 | 3095 | 0 | 2.45 |
| `aesop_core_plus_learned_facts` | 5 | 9.41 | 0.00 | 875 | 864 | 2027 | 0 | 2.48 |

## Aesop Exact-Available Controls

| Action | Source | Exposure | Success | Gain vs empty | Loss vs empty | Net | McNemar p | Bootstrap delta CI |
|---|---|---|---:|---:|---:|---:|---:|---|
| `aesop_core_plus_learned` | `oracle_core+retrieved8` | `facts+simps` | 38 | 20 | 11 | 9 | 0.1496 | [-0.004, 0.087] |
| `aesop_core_plus_learned16` | `oracle_core+retrieved16` | `facts+simps` | 37 | 20 | 12 | 8 | 0.2153 | [-0.013, 0.083] |
| `aesop_empty` | `empty` | `empty` | 29 | - | - | - | - | - |
| `aesop_core_facts` | `oracle_core` | `facts-only` | 5 | 0 | 24 | -24 | 0.0000 | [-0.148, -0.070] |
| `aesop_core_plus_learned16_facts` | `oracle_core+retrieved16` | `facts-only` | 5 | 0 | 24 | -24 | 0.0000 | [-0.148, -0.070] |
| `aesop_core_plus_learned32_facts` | `oracle_core+retrieved32` | `facts-only` | 5 | 0 | 24 | -24 | 0.0000 | [-0.148, -0.070] |
| `aesop_core_plus_learned_facts` | `oracle_core+retrieved8` | `facts-only` | 5 | 0 | 24 | -24 | 0.0000 | [-0.148, -0.070] |
| `aesop_learned16_facts` | `retrieved16` | `facts-only` | 5 | 0 | 24 | -24 | 0.0000 | [-0.148, -0.070] |
| `aesop_learned32_facts` | `retrieved32` | `facts-only` | 5 | 0 | 24 | -24 | 0.0000 | [-0.148, -0.070] |
| `aesop_learned8_facts` | `retrieved8` | `facts-only` | 5 | 0 | 24 | -24 | 0.0000 | [-0.148, -0.070] |
| `aesop_core` | `oracle_core` | `facts+simps` | 4 | 2 | 27 | -25 | 0.0000 | [-0.157, -0.070] |
| `aesop_core_plus_learned_simps` | `oracle_core+retrieved8` | `simps-only` | 4 | 2 | 27 | -25 | 0.0000 | [-0.157, -0.070] |
| `aesop_core_simps` | `oracle_core` | `simps-only` | 4 | 2 | 27 | -25 | 0.0000 | [-0.157, -0.070] |
| `aesop_learned8` | `retrieved8` | `facts+simps` | 4 | 2 | 27 | -25 | 0.0000 | [-0.157, -0.070] |
| `aesop_learned8_simps` | `retrieved8` | `simps-only` | 4 | 2 | 27 | -25 | 0.0000 | [-0.157, -0.070] |
| `aesop_core_plus_learned16_simps` | `oracle_core+retrieved16` | `simps-only` | 3 | 2 | 28 | -26 | 0.0000 | [-0.161, -0.070] |
| `aesop_core_plus_learned32` | `oracle_core+retrieved32` | `facts+simps` | 3 | 2 | 28 | -26 | 0.0000 | [-0.161, -0.070] |
| `aesop_core_plus_learned32_simps` | `oracle_core+retrieved32` | `simps-only` | 3 | 2 | 28 | -26 | 0.0000 | [-0.161, -0.070] |
| `aesop_learned16` | `retrieved16` | `facts+simps` | 3 | 2 | 28 | -26 | 0.0000 | [-0.161, -0.070] |
| `aesop_learned16_simps` | `retrieved16` | `simps-only` | 3 | 2 | 28 | -26 | 0.0000 | [-0.161, -0.070] |
| `aesop_learned32` | `retrieved32` | `facts+simps` | 3 | 2 | 28 | -26 | 0.0000 | [-0.161, -0.070] |
| `aesop_learned32_simps` | `retrieved32` | `simps-only` | 3 | 2 | 28 | -26 | 0.0000 | [-0.161, -0.070] |

### Joint Channel Triples

| Joint action | Joint | Facts | Simps | Single union | Joint-only vs singles | New vs empty | Poisoned vs empty |
|---|---:|---:|---:|---:|---:|---:|---:|
| `aesop_core_plus_learned` | 38 | 5 | 4 | 7 | 34 | 20 | 11 |
| `aesop_core_plus_learned16` | 37 | 5 | 3 | 7 | 34 | 20 | 12 |
| `aesop_core` | 4 | 5 | 4 | 7 | 0 | 2 | 27 |
| `aesop_learned8` | 4 | 5 | 4 | 7 | 0 | 2 | 27 |
| `aesop_core_plus_learned32` | 3 | 5 | 3 | 7 | 0 | 2 | 28 |
| `aesop_learned16` | 3 | 5 | 3 | 7 | 0 | 2 | 28 |
| `aesop_learned32` | 3 | 5 | 3 | 7 | 0 | 2 | 28 |

## Homogeneous K=4 Portfolio Controls

| Group | # actions | OOF K=1 | OOF K=2 | OOF K=3 | OOF K=4 | Avg calls K=4 | Avg wallclock K=4(s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `aesop_all` | 22 | 49/230 | 49/230 | 49/230 | 49/230 | 4.23 | 28.06 |
| `aesop_nonempty` | 21 | 49/230 | 49/230 | 49/230 | 49/230 | 4.23 | 28.06 |
| `full_action_grid` | 49 | 49/230 | 55/230 | 55/230 | 57/230 | 4.18 | 39.08 |
| `hammerCore_only` | 4 | 41/230 | 41/230 | 41/230 | 41/230 | 4.34 | 50.71 |
| `hammer_only` | 4 | 29/230 | 31/230 | 32/230 | 32/230 | 4.47 | 38.89 |
| `raw_arith_norm_only` | 5 | 29/230 | 29/230 | 29/230 | 29/230 | 4.50 | 34.77 |
| `simplification_only` | 12 | 41/230 | 41/230 | 41/230 | 41/230 | 4.34 | 35.41 |
| `solve_by_elim_only` | 4 | 34/230 | 34/230 | 34/230 | 34/230 | 4.43 | 41.32 |
| `typed_nonempty_grid` | 41 | 49/230 | 55/230 | 55/230 | 57/230 | 4.18 | 39.08 |

- Random full-grid K=4 over 100 seeds: mean 41.9/230, median 42/230, range 31-56.

## First-Success Wallclock Frontier

| Policy | K | Success | Strict success | Avg calls | Avg time(s) | Median time(s) | P90 time(s) | First-success leaders |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `full_action_grid_train_fitted` | 4 | 58/230 | 29/29 | 4.18 | 40.07 | 30.71 | 86.40 | `hammer_empty`:29, `aesop_core_plus_learned`:20, `hammerCore_core_plus_learned`:6 |
| `typed_nonempty_grid_train_fitted` | 4 | 58/230 | 29/29 | 4.18 | 40.07 | 30.71 | 86.40 | `hammer_empty`:29, `aesop_core_plus_learned`:20, `hammerCore_core_plus_learned`:6 |
| `full_action_grid_train_fitted` | 3 | 56/230 | 27/29 | 3.42 | 33.12 | 24.59 | 65.92 | `hammer_empty`:29, `aesop_core_plus_learned`:20, `hammerCore_core_plus_learned`:6 |
| `typed_nonempty_grid_train_fitted` | 3 | 56/230 | 27/29 | 3.42 | 33.12 | 24.59 | 65.92 | `hammer_empty`:29, `aesop_core_plus_learned`:20, `hammerCore_core_plus_learned`:6 |
| `full_action_grid_train_fitted` | 2 | 55/230 | 26/29 | 2.66 | 26.37 | 19.26 | 54.13 | `hammer_empty`:29, `aesop_core_plus_learned`:20, `hammerCore_core_plus_learned`:6 |
| `typed_nonempty_grid_train_fitted` | 2 | 55/230 | 26/29 | 2.66 | 26.37 | 19.26 | 54.13 | `hammer_empty`:29, `aesop_core_plus_learned`:20, `hammerCore_core_plus_learned`:6 |
| `aesop_all_train_fitted` | 1 | 49/230 | 20/29 | 1.87 | 16.36 | 12.47 | 29.53 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_core_plus_learned` | 1 | 49/230 | 20/29 | 1.87 | 16.36 | 12.47 | 29.53 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_nonempty_train_fitted` | 1 | 49/230 | 20/29 | 1.87 | 16.36 | 12.47 | 29.53 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `full_action_grid_train_fitted` | 1 | 49/230 | 20/29 | 1.87 | 16.36 | 12.47 | 29.53 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `typed_nonempty_grid_train_fitted` | 1 | 49/230 | 20/29 | 1.87 | 16.36 | 12.47 | 29.53 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_all_train_fitted` | 2 | 49/230 | 20/29 | 2.66 | 18.33 | 14.65 | 33.09 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_nonempty_train_fitted` | 2 | 49/230 | 20/29 | 2.66 | 18.33 | 14.65 | 33.09 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_all_train_fitted` | 3 | 49/230 | 20/29 | 3.45 | 20.20 | 16.24 | 34.86 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_nonempty_train_fitted` | 3 | 49/230 | 20/29 | 3.45 | 20.20 | 16.24 | 34.86 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_all_train_fitted` | 4 | 49/230 | 20/29 | 4.23 | 28.06 | 22.54 | 54.32 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `aesop_nonempty_train_fitted` | 4 | 49/230 | 20/29 | 4.23 | 28.06 | 22.54 | 54.32 | `hammer_empty`:29, `aesop_core_plus_learned`:20 |
| `simplification_only_train_fitted` | 1 | 41/230 | 12/29 | 1.87 | 15.75 | 12.37 | 26.74 | `hammer_empty`:29, `simp_all_core_plus_learned`:12 |
| `hammerCore_only_train_fitted` | 1 | 41/230 | 12/29 | 1.87 | 19.67 | 13.90 | 42.74 | `hammer_empty`:29, `hammerCore_core_plus_learned`:12 |
| `simplification_only_train_fitted` | 2 | 41/230 | 12/29 | 2.70 | 22.05 | 18.21 | 38.79 | `hammer_empty`:29, `simp_all_core_plus_learned`:12 |

## Paper Implications

- Submission text must replace `core` with `oracle_core` or explicitly define it as traced proof-core evidence.
- The cleanest current main claim is about action-conditional evidence allocation under a frozen oracle-core-plus-retrieved evidence pool.
- Aesop's strong result should be written as a source-composition by channel-assignment interaction, not merely facts versus simps complementarity.
- The strongest compute-safe wording is `matched Lean-call budget`; empirical wallclock numbers can be reported as a secondary frontier.
