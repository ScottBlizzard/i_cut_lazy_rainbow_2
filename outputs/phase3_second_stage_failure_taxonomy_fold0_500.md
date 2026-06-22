# Phase 3 Second-Stage Failure Taxonomy

- Goals file: `outputs\phase3_second_stage_eval_fold0_goals_500.jsonl`
- Trace result: `outputs\phase3_guardrail_eval_fold0_500.json`

## `rule_far_learned_second_stage`

- Runs: 500
- Unsolved: 42 (8.4%)

### Tags

| Tag | Count |
|---|---:|
| `expert_misrouting_signal` | 28 |
| `best_expert_top96` | 22 |
| `best_expert_top128` | 13 |
| `best_expert_top160` | 6 |
| `fallback_solved_policy_failed` | 5 |
| `base_guardrail_candidate` | 4 |
| `deep_rank_miss` | 1 |
| `last_failure_top96_but_not_selected` | 1 |

### Last Failure Type

| Failure type | Count |
|---|---:|
| `imported_premise_missing` | 41 |
| `missing_bridge` | 1 |

### Missing-Core Rank Stats

| Rank source | Count | Median | Min | Max | Top96 | Top128 | Top160 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `last-failure expert` | 42 | 127.0 | 20 | 227 | 1 | 23 | 34 |
| `best expert` | 42 | 95.5 | 13 | 162 | 22 | 35 | 41 |
| `base` | 42 | 107.0 | 1 | 256 | 19 | 25 | 29 |
| `learned` | 42 | 131.5 | 103 | 234 | 0 | 19 | 31 |

### Representative Cases

- `Matrix.sum_sum_single`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=112/61/49/121
- `GenContFract.IntFractPair.of_one_le_get?_partDen`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=148/50/142/155
- `inv_mul_lt_iff_lt_mul`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=113/79/71/134
- `PiNat.exists_nat_nat_continuous_surjective_of_completeSpace`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=127/96/248/126
- `MeasureTheory.absolutelyContinuous_inv`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=127/74/113/124
- `TopCat.range_pullback_map`: tags=best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=138/134/242/139
- `cfcₙ_apply_mkD`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=112/112/220/112
- `Fin.Fin.Equiv.Perm.sign_eq_prod_prod_Iio`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=117/109/201/109
- `CategoryTheory.IsUniversalColimit.nonempty_isColimit_of_pullbackCone_right`: tags=expert_misrouting_signal,best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=155/128/175/173
- `cot_pi_mul_contDiffWithinAt`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=176/76/157/171
- `Polynomial.natDegree_primPart`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=101/101/106/103
- `RootPairing.ne_neg`: tags=best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=146/133/256/133
- `Polynomial.smeval_commute_left`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=123/47/40/132
- `Function.Injective.wOppSide_map_iff`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=118/107/37/136
- `Polynomial.natDegree_eraseLead`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=125/66/104/129
- `Polynomial.natDegree_taylor`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=186/159/191/175
- `AlgebraicTopology.DoldKan.PInfty_comp_map_mono_eq_zero`: tags=expert_misrouting_signal,base_guardrail_candidate,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=142/58/1/147
- `AlgebraicGeometry.ExistsHomHomCompEqCompAux.Scheme.exists_isQuasiAffine_of_isLimit`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=146/93/85/152
- `SimpleGraph.Walk.support_dropUntil_suffix_support`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=221/95/85/227
- `bernoulli'PowerSeries_mul_exp_sub_one`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=107/102/247/105

## `rule_far_learned_second_stage_final_base_guardrail_8`

- Runs: 500
- Unsolved: 42 (8.4%)

### Tags

| Tag | Count |
|---|---:|
| `expert_misrouting_signal` | 25 |
| `best_expert_top96` | 22 |
| `best_expert_top128` | 13 |
| `best_expert_top160` | 6 |
| `last_failure_top96_but_not_selected` | 4 |
| `fallback_solved_policy_failed` | 3 |
| `base_guardrail_candidate` | 1 |
| `deep_rank_miss` | 1 |

### Last Failure Type

| Failure type | Count |
|---|---:|
| `imported_premise_missing` | 41 |
| `missing_bridge` | 1 |

### Missing-Core Rank Stats

| Rank source | Count | Median | Min | Max | Top96 | Top128 | Top160 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `last-failure expert` | 42 | 121.5 | 19 | 227 | 4 | 26 | 34 |
| `best expert` | 42 | 95.5 | 13 | 162 | 22 | 35 | 41 |
| `base` | 42 | 111.0 | 11 | 256 | 17 | 23 | 28 |
| `learned` | 42 | 126.0 | 87 | 231 | 4 | 22 | 32 |

### Representative Cases

- `Matrix.sum_sum_single`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=112/61/49/121
- `GenContFract.IntFractPair.of_one_le_get?_partDen`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=115/50/142/99
- `inv_mul_lt_iff_lt_mul`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=113/79/71/134
- `PiNat.exists_nat_nat_continuous_surjective_of_completeSpace`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=127/96/248/126
- `MeasureTheory.absolutelyContinuous_inv`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=127/74/113/124
- `TopCat.range_pullback_map`: tags=best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=138/134/242/139
- `cfcₙ_apply_mkD`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=112/112/220/112
- `Fin.Fin.Equiv.Perm.sign_eq_prod_prod_Iio`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=117/109/201/109
- `CategoryTheory.IsUniversalColimit.nonempty_isColimit_of_pullbackCone_right`: tags=expert_misrouting_signal,best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=155/128/175/173
- `cot_pi_mul_contDiffWithinAt`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=176/76/157/171
- `Polynomial.natDegree_primPart`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=101/101/106/103
- `RootPairing.ne_neg`: tags=best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=146/133/256/133
- `Polynomial.smeval_commute_left`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=123/47/40/132
- `Function.Injective.wOppSide_map_iff`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=118/107/37/136
- `Polynomial.natDegree_eraseLead`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=125/66/104/129
- `Polynomial.natDegree_taylor`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=186/159/191/175
- `AlgebraicGeometry.ExistsHomHomCompEqCompAux.Scheme.exists_isQuasiAffine_of_isLimit`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=146/93/85/152
- `SimpleGraph.Walk.support_dropUntil_suffix_support`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=221/95/85/227
- `bernoulli'PowerSeries_mul_exp_sub_one`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=107/102/247/105
- `RatFunc.valuation_isEquiv_infty_or_adic`: tags=fallback_solved_policy_failed,expert_misrouting_signal,base_guardrail_candidate,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=136/37/11/141

