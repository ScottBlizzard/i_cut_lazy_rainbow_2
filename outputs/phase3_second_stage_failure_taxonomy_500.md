# Phase 3 Second-Stage Failure Taxonomy

- Goals file: `outputs\phase3_second_stage_eval_goals_500.jsonl`
- Trace result: `outputs\phase3_guardrail_eval_500.json`

## `rule_far_learned_second_stage`

- Runs: 500
- Unsolved: 38 (7.6%)

### Tags

| Tag | Count |
|---|---:|
| `best_expert_top96` | 20 |
| `expert_misrouting_signal` | 19 |
| `best_expert_top128` | 13 |
| `fallback_solved_policy_failed` | 8 |
| `base_guardrail_candidate` | 6 |
| `last_failure_top96_but_not_selected` | 5 |
| `best_expert_top160` | 4 |
| `deep_rank_miss` | 1 |

### Last Failure Type

| Failure type | Count |
|---|---:|
| `imported_premise_missing` | 34 |
| `type_mismatch` | 2 |
| `typeclass_missing` | 1 |
| `missing_bridge` | 1 |

### Missing-Core Rank Stats

| Rank source | Count | Median | Min | Max | Top96 | Top128 | Top160 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `last-failure expert` | 38 | 116.5 | 6 | 240 | 5 | 22 | 32 |
| `best expert` | 38 | 93.5 | 6 | 189 | 20 | 33 | 37 |
| `base` | 38 | 85.0 | 1 | 245 | 20 | 21 | 23 |
| `learned` | 38 | 125.0 | 92 | 231 | 1 | 22 | 28 |

### Representative Cases

- `WeierstrassCurve.Projective.nonsingular_some`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=207/132/77/209
- `MeasureTheory.Measure.integral_isMulLeftInvariant_isMulRightInvariant_combo`: tags=last_failure_top96_but_not_selected,best_expert_top96; last=type_mismatch; ranks last/best/base/learned=6/6/63/204
- `StandardEtalePair.Algebra.IsStandardEtale.of_surjective`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=151/61/30/162
- `Ideal.ramificationIdx'_pos`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=169/142/92/176
- `tendsto_arithGeom_atTop_of_one_lt`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=117/108/195/108
- `Monoid.exponent_eq_iSup_orderOf`: tags=best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=138/135/224/135
- `Rat.intCast_div`: tags=expert_misrouting_signal,best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=142/114/157/134
- `Equiv.succ_embeddingFinSucc_fst_symm_apply`: tags=fallback_solved_policy_failed,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=102/79/23/125
- `WeierstrassCurve.Jacobian.neg_of_Z_ne_zero`: tags=fallback_solved_policy_failed,expert_misrouting_signal,base_guardrail_candidate,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=131/66/1/116
- `AffineSubspace.SSameSide.oangle_sign_eq`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=199/155/245/203
- `LieModule.weight_vector_multiplication`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=105/105/239/110
- `SchwartzMap.lineDerivOp_fourier_eq`: tags=best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=108/92/233/107
- `ContinuousMultilinearMap.hasFTaylorSeriesUpTo_iteratedFDeriv`: tags=best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=115/95/239/115
- `Polynomial.map_under_lt_comap_of_weaklyQuasiFiniteAt`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=115/20/30/125
- `AffineSpace.StarConvex.smul_vadd_mem_of_isClosed_of_mem_asymptoticCone`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=117/98/245/98
- `FreeGroup.IsCyclicallyReduced.reduceCyclically.reduce_flatten_replicate_succ`: tags=fallback_solved_policy_failed,expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=101/73/30/111
- `ruzsaSzemerediNumberNat_asymptotic_lower_bound`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=116/112/174/112
- `Finset.sup'_product_right`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=138/58/42/141
- `AlgebraicGeometry.isCommMonObj_of_isProper_of_isIntegral_tensorObj_of_isAlgClosed`: tags=expert_misrouting_signal,best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=240/112/216/119
- `equicontinuousWithinAt_iInf_rng`: tags=fallback_solved_policy_failed,last_failure_top96_but_not_selected,base_guardrail_candidate,best_expert_top96; last=type_mismatch; ranks last/best/base/learned=26/20/8/122

## `rule_far_learned_second_stage_final_base_guardrail_8`

- Runs: 500
- Unsolved: 37 (7.4%)

### Tags

| Tag | Count |
|---|---:|
| `best_expert_top96` | 19 |
| `expert_misrouting_signal` | 16 |
| `best_expert_top128` | 13 |
| `last_failure_top96_but_not_selected` | 6 |
| `fallback_solved_policy_failed` | 6 |
| `best_expert_top160` | 4 |
| `base_guardrail_candidate` | 2 |
| `deep_rank_miss` | 1 |

### Last Failure Type

| Failure type | Count |
|---|---:|
| `imported_premise_missing` | 35 |
| `type_mismatch` | 1 |
| `typeclass_missing` | 1 |

### Missing-Core Rank Stats

| Rank source | Count | Median | Min | Max | Top96 | Top128 | Top160 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `last-failure expert` | 37 | 115.0 | 6 | 240 | 6 | 23 | 31 |
| `best expert` | 37 | 95.0 | 6 | 189 | 19 | 32 | 36 |
| `base` | 37 | 157.0 | 9 | 254 | 16 | 17 | 19 |
| `learned` | 37 | 125.0 | 77 | 209 | 3 | 23 | 28 |

### Representative Cases

- `WeierstrassCurve.Projective.nonsingular_some`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=207/132/77/209
- `MeasureTheory.Measure.integral_isMulLeftInvariant_isMulRightInvariant_combo`: tags=last_failure_top96_but_not_selected,best_expert_top96; last=type_mismatch; ranks last/best/base/learned=6/6/63/204
- `StandardEtalePair.Algebra.IsStandardEtale.of_surjective`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=151/61/30/162
- `Ideal.ramificationIdx'_pos`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=169/142/92/176
- `tendsto_arithGeom_atTop_of_one_lt`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=117/108/195/108
- `Monoid.exponent_eq_iSup_orderOf`: tags=best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=138/135/224/135
- `Rat.intCast_div`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=114/114/157/125
- `Equiv.succ_embeddingFinSucc_fst_symm_apply`: tags=fallback_solved_policy_failed,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=102/79/23/125
- `DiscreteUniformity.eq_pure_of_cauchy`: tags=last_failure_top96_but_not_selected,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=94/91/203/91
- `AffineSubspace.SSameSide.oangle_sign_eq`: tags=expert_misrouting_signal,best_expert_top160; last=imported_premise_missing; ranks last/best/base/learned=199/155/245/203
- `LieModule.weight_vector_multiplication`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=105/105/239/110
- `SchwartzMap.lineDerivOp_fourier_eq`: tags=best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=108/92/233/107
- `ContinuousMultilinearMap.hasFTaylorSeriesUpTo_iteratedFDeriv`: tags=best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=115/95/239/115
- `Polynomial.map_under_lt_comap_of_weaklyQuasiFiniteAt`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=115/20/30/125
- `AffineSpace.StarConvex.smul_vadd_mem_of_isClosed_of_mem_asymptoticCone`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=117/98/245/98
- `FreeGroup.IsCyclicallyReduced.reduceCyclically.reduce_flatten_replicate_succ`: tags=fallback_solved_policy_failed,expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=101/73/30/111
- `ruzsaSzemerediNumberNat_asymptotic_lower_bound`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=116/112/174/112
- `Finset.sup'_product_right`: tags=expert_misrouting_signal,best_expert_top96; last=imported_premise_missing; ranks last/best/base/learned=138/58/42/141
- `AlgebraicGeometry.isCommMonObj_of_isProper_of_isIntegral_tensorObj_of_isAlgClosed`: tags=expert_misrouting_signal,best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=240/112/216/119
- `FermatLastTheoremForThreeGen.Solution.associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b`: tags=best_expert_top128; last=imported_premise_missing; ranks last/best/base/learned=99/99/221/113

