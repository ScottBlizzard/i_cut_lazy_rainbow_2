# Mathlib 4.30 Action Routing Policy Gate

Date: 2026-06-22

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled143.json`
- Splits: `outputs\mathlib430_replayable300_splits.json`
- Best single action selected on train: `hammer_core_plus_learned`
- Best fixed second action after `hammer_empty`: `hammerCore_core_plus_learned`

Status-rule policy learned on train:

- `__fallback__` -> `hammerCore_core_plus_learned`
- `lean_error` -> `hammerCore_core`
- `search_fail` -> `hammerCore_core_plus_learned`
- `simp_fail` -> `hammerCore_core_plus_learned`
- `sorry_warning` -> `hammerCore_core`

## All Goals

| Split | N | Empty Only | Best Single | Empty -> Best Second | Empty -> Status Rule | Empty -> Text NB | Oracle |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 85 | 11 (12.9%) | 12 (14.1%) | 18 (21.2%) | 18 (21.2%) | 21 (24.7%) | 21 (24.7%) |
| dev | 28 | 4 (14.3%) | 4 (14.3%) | 7 (25.0%) | 7 (25.0%) | 8 (28.6%) | 9 (32.1%) |
| test | 30 | 3 (10.0%) | 3 (10.0%) | 4 (13.3%) | 4 (13.3%) | 4 (13.3%) | 5 (16.7%) |
| all | 143 | 18 (12.6%) | 19 (13.3%) | 29 (20.3%) | 29 (20.3%) | 33 (23.1%) | 35 (24.5%) |

## Strict Action-Dependent Goals

| Split | Strict N | Best Second Hits | Status Rule Hits | Text NB Hits | Oracle |
|---|---:|---:|---:|---:|---:|
| train | 10 | 7 (70.0%) | 7 (70.0%) | 10 (100.0%) | 10 (100.0%) |
| dev | 5 | 3 (60.0%) | 3 (60.0%) | 4 (80.0%) | 5 (100.0%) |
| test | 2 | 1 (50.0%) | 1 (50.0%) | 1 (50.0%) | 2 (100.0%) |
| all | 17 | 11 (64.7%) | 11 (64.7%) | 15 (88.2%) | 17 (100.0%) |

## Train-Greedy Fixed Portfolios

These schedules always run `hammer_empty` first, then a fixed list of second-stage actions selected greedily on train. They test whether the oracle headroom is mostly a generic retry-portfolio effect.

| Split | Extra Actions | Fixed Actions | Success | Strict Hits |
|---|---:|---|---:|---:|
| train | 1 | `hammerCore_core_plus_learned` | 18/85 (21.2%) | 7/10 (70.0%) |
| train | 2 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned` | 19/85 (22.4%) | 8/10 (80.0%) |
| train | 3 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned` | 20/85 (23.5%) | 9/10 (90.0%) |
| train | 4 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 21/85 (24.7%) | 10/10 (100.0%) |
| dev | 1 | `hammerCore_core_plus_learned` | 7/28 (25.0%) | 3/5 (60.0%) |
| dev | 2 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned` | 7/28 (25.0%) | 3/5 (60.0%) |
| dev | 3 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned` | 8/28 (28.6%) | 4/5 (80.0%) |
| dev | 4 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 9/28 (32.1%) | 5/5 (100.0%) |
| test | 1 | `hammerCore_core_plus_learned` | 4/30 (13.3%) | 1/2 (50.0%) |
| test | 2 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned` | 4/30 (13.3%) | 1/2 (50.0%) |
| test | 3 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned` | 5/30 (16.7%) | 2/2 (100.0%) |
| test | 4 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 5/30 (16.7%) | 2/2 (100.0%) |
| all | 1 | `hammerCore_core_plus_learned` | 29/143 (20.3%) | 11/17 (64.7%) |
| all | 2 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned` | 30/143 (21.0%) | 12/17 (70.6%) |
| all | 3 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned` | 33/143 (23.1%) | 15/17 (88.2%) |
| all | 4 | `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` | 35/143 (24.5%) | 17/17 (100.0%) |

## 5-Fold Out-of-Fold Policy Check

| N | Empty Only | Best Single | Empty -> Best Second | Empty -> Status Rule | Empty -> Text NB | Oracle |
|---:|---:|---:|---:|---:|---:|---:|
| 143 | 18 (12.6%) | 12 (8.4%) | 29 (20.3%) | 25 (17.5%) | 28 (19.6%) | 35 (24.5%) |

| Strict N | Best Second Hits | Status Rule Hits | Text NB Hits | Oracle |
|---:|---:|---:|---:|---:|
| 17 | 11 (64.7%) | 7 (41.2%) | 10 (58.8%) | 17 (100.0%) |

## Readout

- The coarse first-failure-status rule ties the best fixed second action on test.
- This is a low-capacity policy gate using only the first `hammer_empty` status; richer failure transcript and goal/action features are still needed before making a strong adaptive-policy claim.
- The text NB policy ties the best fixed second action on test.
