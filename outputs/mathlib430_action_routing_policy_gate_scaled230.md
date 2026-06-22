# Mathlib 4.30 Action Routing Policy Gate

Date: 2026-06-22

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_merged.json`
- Splits: `outputs\mathlib430_replayable490_splits.json`
- Best single action selected on train: `hammer_core_plus_learned`
- Best fixed second action after `hammer_empty`: `hammerCore_core_plus_learned`

Status-rule policy learned on train:

- `__fallback__` -> `hammerCore_core_plus_learned`
- `lean_error` -> `hammerCore_core`
- `rewrite_fail` -> `hammerCore_core`
- `search_fail` -> `simp_all_core_plus_learned`
- `simp_fail` -> `hammerCore_core_plus_learned`
- `sorry_warning` -> `hammerCore_core`
- `timeout` -> `hammerCore_core`

## All Goals

| Split | N | Empty Only | Best Single | Empty -> Best Second | Empty -> Status Rule | Empty -> Text NB | Oracle |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 138 | 16 (11.6%) | 17 (12.3%) | 24 (17.4%) | 26 (18.8%) | 30 (21.7%) | 30 (21.7%) |
| dev | 46 | 8 (17.4%) | 9 (19.6%) | 10 (21.7%) | 11 (23.9%) | 11 (23.9%) | 13 (28.3%) |
| test | 46 | 5 (10.9%) | 5 (10.9%) | 7 (15.2%) | 6 (13.0%) | 7 (15.2%) | 8 (17.4%) |
| all | 230 | 29 (12.6%) | 31 (13.5%) | 41 (17.8%) | 43 (18.7%) | 48 (20.9%) | 51 (22.2%) |

## Strict Action-Dependent Goals

| Split | Strict N | Best Second Hits | Status Rule Hits | Text NB Hits | Oracle |
|---|---:|---:|---:|---:|---:|
| train | 14 | 8 (57.1%) | 10 (71.4%) | 14 (100.0%) | 14 (100.0%) |
| dev | 5 | 2 (40.0%) | 3 (60.0%) | 3 (60.0%) | 5 (100.0%) |
| test | 3 | 2 (66.7%) | 1 (33.3%) | 2 (66.7%) | 3 (100.0%) |
| all | 22 | 12 (54.5%) | 14 (63.6%) | 19 (86.4%) | 22 (100.0%) |

## Train-Greedy Fixed Portfolios

These schedules always run `hammer_empty` first, then a fixed list of second-stage actions selected greedily on train. They test whether the oracle headroom is mostly a generic retry-portfolio effect.

| Split | Extra Actions | Fixed Actions | Success | Strict Hits |
|---|---:|---|---:|---:|
| train | 1 | `hammerCore_core_plus_learned` | 24/138 (17.4%) | 8/14 (57.1%) |
| train | 2 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned` | 29/138 (21.0%) | 13/14 (92.9%) |
| train | 3 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 30/138 (21.7%) | 14/14 (100.0%) |
| train | 4 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core`, `hammerCore_core` | 30/138 (21.7%) | 14/14 (100.0%) |
| dev | 1 | `hammerCore_core_plus_learned` | 10/46 (21.7%) | 2/5 (40.0%) |
| dev | 2 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned` | 11/46 (23.9%) | 3/5 (60.0%) |
| dev | 3 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 12/46 (26.1%) | 4/5 (80.0%) |
| dev | 4 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core`, `hammerCore_core` | 12/46 (26.1%) | 4/5 (80.0%) |
| test | 1 | `hammerCore_core_plus_learned` | 7/46 (15.2%) | 2/3 (66.7%) |
| test | 2 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned` | 8/46 (17.4%) | 3/3 (100.0%) |
| test | 3 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 8/46 (17.4%) | 3/3 (100.0%) |
| test | 4 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core`, `hammerCore_core` | 8/46 (17.4%) | 3/3 (100.0%) |
| all | 1 | `hammerCore_core_plus_learned` | 41/230 (17.8%) | 12/22 (54.5%) |
| all | 2 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned` | 48/230 (20.9%) | 19/22 (86.4%) |
| all | 3 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 50/230 (21.7%) | 21/22 (95.5%) |
| all | 4 | `hammerCore_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core`, `hammerCore_core` | 50/230 (21.7%) | 21/22 (95.5%) |

## 5-Fold Out-of-Fold Policy Check

| N | Empty Only | Best Single | Empty -> Best Second | Empty -> Status Rule | Empty -> Text NB | Oracle |
|---:|---:|---:|---:|---:|---:|---:|
| 230 | 29 (12.6%) | 29 (12.6%) | 38 (16.5%) | 40 (17.4%) | 41 (17.8%) | 51 (22.2%) |

| Strict N | Best Second Hits | Status Rule Hits | Text NB Hits | Oracle |
|---:|---:|---:|---:|---:|
| 22 | 9 (40.9%) | 11 (50.0%) | 12 (54.5%) | 22 (100.0%) |

## Readout

- The coarse first-failure-status rule does not beat the best fixed second action on test.
- This is a low-capacity policy gate using only the first `hammer_empty` status; richer failure transcript and goal/action features are still needed before making a strong adaptive-policy claim.
- The text NB policy ties the best fixed second action on test.
