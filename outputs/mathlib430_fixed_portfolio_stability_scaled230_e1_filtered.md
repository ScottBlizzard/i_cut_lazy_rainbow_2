# Mathlib 4.30 Fixed Portfolio Stability

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_e1_filtered_merged.json`
- Splits: `outputs\mathlib430_replayable490_splits.json`
- Goals: 230
- Strict action-dependent oracle goals: 29
- Best static action: `aesop_core_plus_learned`

## 5-Fold OOF Totals

| K | Fixed greedy | Empty | Oracle | Strict fixed | Strict oracle |
|---:|---:|---:|---:|---:|---:|
| 1 | 49/230 (21.3%) | 29/230 (12.6%) | 58/230 (25.2%) | 20/29 (69.0%) | 29/29 (100.0%) |
| 2 | 55/230 (23.9%) | 29/230 (12.6%) | 58/230 (25.2%) | 26/29 (89.7%) | 29/29 (100.0%) |
| 3 | 55/230 (23.9%) | 29/230 (12.6%) | 58/230 (25.2%) | 26/29 (89.7%) | 29/29 (100.0%) |
| 4 | 57/230 (24.8%) | 29/230 (12.6%) | 58/230 (25.2%) | 28/29 (96.6%) | 29/29 (100.0%) |
| 5 | 57/230 (24.8%) | 29/230 (12.6%) | 58/230 (25.2%) | 28/29 (96.6%) | 29/29 (100.0%) |
| 6 | 57/230 (24.8%) | 29/230 (12.6%) | 58/230 (25.2%) | 28/29 (96.6%) | 29/29 (100.0%) |

## Per-Fold Fixed Greedy

| Fold | K | Fixed | Empty | Oracle | Actions |
|---:|---:|---:|---:|---:|---|
| 0 | 1 | 10/46 | 8/46 | 12/46 | `aesop_core_plus_learned` |
| 0 | 2 | 12/46 | 8/46 | 12/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` |
| 0 | 3 | 12/46 | 8/46 | 12/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core` |
| 0 | 4 | 12/46 | 8/46 | 12/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `hammer_core_plus_learned16` |
| 0 | 5 | 12/46 | 8/46 | 12/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `hammer_core_plus_learned16`, `aesop_core` |
| 0 | 6 | 12/46 | 8/46 | 12/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `hammer_core_plus_learned16`, `aesop_core`, `aesop_core_facts` |
| 1 | 1 | 8/46 | 4/46 | 9/46 | `aesop_core_plus_learned` |
| 1 | 2 | 8/46 | 4/46 | 9/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` |
| 1 | 3 | 8/46 | 4/46 | 9/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16` |
| 1 | 4 | 9/46 | 4/46 | 9/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core` |
| 1 | 5 | 9/46 | 4/46 | 9/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core` |
| 1 | 6 | 9/46 | 4/46 | 9/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core`, `aesop_core_facts` |
| 2 | 1 | 16/46 | 9/46 | 19/46 | `aesop_core_plus_learned` |
| 2 | 2 | 18/46 | 9/46 | 19/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` |
| 2 | 3 | 18/46 | 9/46 | 19/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16` |
| 2 | 4 | 19/46 | 9/46 | 19/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core` |
| 2 | 5 | 19/46 | 9/46 | 19/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core` |
| 2 | 6 | 19/46 | 9/46 | 19/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core`, `aesop_core_facts` |
| 3 | 1 | 10/46 | 7/46 | 11/46 | `aesop_core_plus_learned` |
| 3 | 2 | 11/46 | 7/46 | 11/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` |
| 3 | 3 | 11/46 | 7/46 | 11/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core` |
| 3 | 4 | 11/46 | 7/46 | 11/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `hammer_core_plus_learned16` |
| 3 | 5 | 11/46 | 7/46 | 11/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `hammer_core_plus_learned16`, `aesop_core` |
| 3 | 6 | 11/46 | 7/46 | 11/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `hammer_core_plus_learned16`, `aesop_core`, `aesop_core_facts` |
| 4 | 1 | 5/46 | 1/46 | 7/46 | `aesop_core_plus_learned` |
| 4 | 2 | 6/46 | 1/46 | 7/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` |
| 4 | 3 | 6/46 | 1/46 | 7/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core` |
| 4 | 4 | 6/46 | 1/46 | 7/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `aesop_core` |
| 4 | 5 | 6/46 | 1/46 | 7/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `aesop_core`, `aesop_core_facts` |
| 4 | 6 | 6/46 | 1/46 | 7/46 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `solve_by_elim_core`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned16` |

## Train-Fitted Portfolios

| K | All success | Strict success | Actions |
|---:|---:|---:|---|
| 1 | 49/230 | 20/29 | `aesop_core_plus_learned` |
| 2 | 55/230 | 26/29 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned` |
| 3 | 56/230 | 27/29 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16` |
| 4 | 58/230 | 29/29 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core` |
| 5 | 58/230 | 29/29 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core` |
| 6 | 58/230 | 29/29 | `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, `solve_by_elim_core`, `aesop_core`, `aesop_core_facts` |

