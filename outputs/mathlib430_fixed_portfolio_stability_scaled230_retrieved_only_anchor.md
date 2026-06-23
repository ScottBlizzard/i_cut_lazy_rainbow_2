# Mathlib 4.30 Fixed Portfolio Stability

- Matrix: `outputs/mathlib430_pretheorem_action_matrix_scaled230_retrieved_only_anchor_merged.json`
- Splits: `outputs/mathlib430_replayable490_splits.json`
- Goals: 230
- Strict action-dependent oracle goals: 23
- Best static action: `aesop_learned32`

## 5-Fold OOF Totals

| K | Fixed greedy | Empty | Oracle | Strict fixed | Strict oracle |
|---:|---:|---:|---:|---:|---:|
| 1 | 47/230 (20.4%) | 29/230 (12.6%) | 52/230 (22.6%) | 18/23 (78.3%) | 23/23 (100.0%) |
| 2 | 50/230 (21.7%) | 29/230 (12.6%) | 52/230 (22.6%) | 21/23 (91.3%) | 23/23 (100.0%) |
| 3 | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) | 23/23 (100.0%) | 23/23 (100.0%) |
| 4 | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) | 23/23 (100.0%) | 23/23 (100.0%) |
| 5 | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) | 23/23 (100.0%) | 23/23 (100.0%) |
| 6 | 52/230 (22.6%) | 29/230 (12.6%) | 52/230 (22.6%) | 23/23 (100.0%) | 23/23 (100.0%) |

## Per-Fold Fixed Greedy

| Fold | K | Fixed | Empty | Oracle | Actions |
|---:|---:|---:|---:|---:|---|
| 0 | 1 | 10/46 | 8/46 | 10/46 | `aesop_core_plus_learned16` |
| 0 | 2 | 10/46 | 8/46 | 10/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped` |
| 0 | 3 | 10/46 | 8/46 | 10/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned` |
| 0 | 4 | 10/46 | 8/46 | 10/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core` |
| 0 | 5 | 10/46 | 8/46 | 10/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts` |
| 0 | 6 | 10/46 | 8/46 | 10/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned` |
| 1 | 1 | 8/46 | 4/46 | 8/46 | `aesop_core_plus_learned16` |
| 1 | 2 | 8/46 | 4/46 | 8/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped` |
| 1 | 3 | 8/46 | 4/46 | 8/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned` |
| 1 | 4 | 8/46 | 4/46 | 8/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core` |
| 1 | 5 | 8/46 | 4/46 | 8/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts` |
| 1 | 6 | 8/46 | 4/46 | 8/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned` |
| 2 | 1 | 15/46 | 9/46 | 18/46 | `aesop_core_plus_learned16` |
| 2 | 2 | 17/46 | 9/46 | 18/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped` |
| 2 | 3 | 18/46 | 9/46 | 18/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned` |
| 2 | 4 | 18/46 | 9/46 | 18/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core` |
| 2 | 5 | 18/46 | 9/46 | 18/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts` |
| 2 | 6 | 18/46 | 9/46 | 18/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned` |
| 3 | 1 | 9/46 | 7/46 | 9/46 | `aesop_core_plus_learned16` |
| 3 | 2 | 9/46 | 7/46 | 9/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped` |
| 3 | 3 | 9/46 | 7/46 | 9/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned` |
| 3 | 4 | 9/46 | 7/46 | 9/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core` |
| 3 | 5 | 9/46 | 7/46 | 9/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts` |
| 3 | 6 | 9/46 | 7/46 | 9/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned` |
| 4 | 1 | 5/46 | 1/46 | 7/46 | `aesop_core_plus_learned16` |
| 4 | 2 | 6/46 | 1/46 | 7/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped` |
| 4 | 3 | 7/46 | 1/46 | 7/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned` |
| 4 | 4 | 7/46 | 1/46 | 7/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core` |
| 4 | 5 | 7/46 | 1/46 | 7/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts` |
| 4 | 6 | 7/46 | 1/46 | 7/46 | `aesop_core_plus_learned16`, `aesop_core_plus_learned_swapped`, `hammerCore_core_plus_learned`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned` |

## Train-Fitted Portfolios

| K | All success | Strict success | Actions |
|---:|---:|---:|---|
| 1 | 47/230 | 18/23 | `aesop_core_plus_learned16` |
| 2 | 49/230 | 20/23 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned` |
| 3 | 52/230 | 23/23 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped` |
| 4 | 52/230 | 23/23 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core` |
| 5 | 52/230 | 23/23 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core`, `aesop_core_facts` |
| 6 | 52/230 | 23/23 | `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `aesop_core_plus_learned_swapped`, `aesop_core`, `aesop_core_facts`, `aesop_core_plus_learned` |
