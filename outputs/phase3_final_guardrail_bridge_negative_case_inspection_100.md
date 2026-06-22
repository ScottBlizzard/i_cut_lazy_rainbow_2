# Phase 3 Bridge Negative-Case Inspection

This report inspects replay-verified misses where the second-stage controller did not recover trace-core proof cores.

## Summary

- Inspected cases: 10
- Candidate-pool miss cases: 0
- Second-stage dropped a fallback-selected core premise: 2
- Second-stage dropped an expansion-selected core premise: 2

### Groups

| Group | Count |
|---|---:|
| `fallback_bridge_over_second_stage` | 2 |
| `premise_selection_miss_second_stage_other` | 1 |
| `replay_verified_both_fail` | 7 |

### Reasons

| Reason | Count |
|---|---:|
| `failure_conditioned_rank_miss` | 8 |
| `second_stage_dropped_expansion_core` | 2 |
| `budget_or_path_miss_with_core_ranked_in_top96` | 2 |
| `second_stage_dropped_fallback_core` | 2 |

### Second-Stage Failure Types

| Failure type | Count |
|---|---:|
| `imported_premise_missing` | 10 |

### Missed-Core Rank Stats

| Rank source | Count | Median | Min | Max | Top64 | Top96 |
|---|---:|---:|---:|---:|---:|---:|
| `best second-stage` | 11 | 115.0 | 94 | 207 | 0 | 2 |
| `learned` | 11 | 125.0 | 77 | 209 | 0 | 2 |
| `base` | 11 | 119.0 | 9 | 254 | 4 | 5 |

## Case Details

### `fallback_bridge_over_second_stage`

- `Multiset.Subset.ndinter_eq_left` (fallback_over_second_stage, `fallback_bridge_over_second_stage`)
  - reasons: `second_stage_dropped_fallback_core`, `failure_conditioned_rank_miss`
  - core: 3/4 selected by second-stage; 4/4 by fallback; 3/4 by expansion
  - failure types: `imported_premise_missing`
  - missed `List.Subset.inter_eq_left`: learned_rank=179, base_rank=9, second_stage_ranks=imported_premise_missing:177, fallback=True, expansion=False, same_file=False, kind=theorem
- `ENNReal.tendsto_nhds_of_Icc` (fallback_fill, `fallback_bridge_over_second_stage`)
  - reasons: `second_stage_dropped_fallback_core`, `second_stage_dropped_expansion_core`, `budget_or_path_miss_with_core_ranked_in_top96`
  - core: 6/7 selected by second-stage; 7/7 by fallback; 7/7 by expansion
  - failure types: `imported_premise_missing`
  - missed `Filter.Tendsto.mono_right`: learned_rank=77, base_rank=254, second_stage_ranks=imported_premise_missing:94, fallback=True, expansion=True, same_file=False, kind=theorem

### `premise_selection_miss_second_stage_other`

- `DiscreteUniformity.eq_pure_of_cauchy` (second_stage_over_fallback, `premise_selection_miss_second_stage_other`)
  - reasons: `second_stage_dropped_expansion_core`, `budget_or_path_miss_with_core_ranked_in_top96`
  - core: 4/5 selected by second-stage; 4/5 by fallback; 5/5 by expansion
  - failure types: `imported_premise_missing`
  - missed `SetRel.exists_eq_singleton_of_prod_subset_id`: learned_rank=91, base_rank=203, second_stage_ranks=imported_premise_missing:94, fallback=False, expansion=True, same_file=False, kind=lemma

### `replay_verified_both_fail`

- `HasProd.mul_disjoint` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 4/5 selected by second-stage; 4/5 by fallback; 4/5 by expansion
  - failure types: `imported_premise_missing`
  - missed `Set.mulIndicator_union_of_disjoint`: learned_rank=125, base_rank=37, second_stage_ranks=imported_premise_missing:115, fallback=False, expansion=False, same_file=False, kind=theorem
- `FermatLastTheoremForThreeGen.Solution.associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 9/10 selected by second-stage; 9/10 by fallback; 9/10 by expansion
  - failure types: `imported_premise_missing`
  - missed `IsCyclotomicExtension.Rat.Three.eta_sq`: learned_rank=113, base_rank=221, second_stage_ranks=imported_premise_missing:99, fallback=False, expansion=False, same_file=False, kind=lemma
- `tendsto_arithGeom_atTop_of_one_lt` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 6/7 selected by second-stage; 6/7 by fallback; 6/7 by expansion
  - failure types: `imported_premise_missing`
  - missed `Filter.Tendsto.atTop_mul_const`: learned_rank=108, base_rank=195, second_stage_ranks=imported_premise_missing:117, fallback=False, expansion=False, same_file=False, kind=theorem
- `SSet.Truncated.HomotopicR.symm` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 4/5 selected by second-stage; 4/5 by fallback; 4/5 by expansion
  - failure types: `imported_premise_missing`
  - missed `SSet.Truncated.Edge.CompStruct.idComp`: learned_rank=130, base_rank=64, second_stage_ranks=imported_premise_missing:135, fallback=False, expansion=False, same_file=False, kind=def
- `WeierstrassCurve.Projective.nonsingular_some` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 7/9 selected by second-stage; 7/9 by fallback; 6/9 by expansion
  - failure types: `imported_premise_missing`
  - missed `WeierstrassCurve.Affine.nonsingular_iff'`: learned_rank=148, base_rank=77, second_stage_ranks=imported_premise_missing:137, fallback=False, expansion=False, same_file=False, kind=lemma
  - missed `WeierstrassCurve.Projective.nonsingular_iff`: learned_rank=209, base_rank=28, second_stage_ranks=imported_premise_missing:207, fallback=False, expansion=False, same_file=True, kind=lemma
- `Rat.intCast_div` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 3/4 selected by second-stage; 3/4 by fallback; 2/4 by expansion
  - failure types: `imported_premise_missing`
  - missed `Int.cast_mul`: learned_rank=125, base_rank=157, second_stage_ranks=imported_premise_missing:114, fallback=False, expansion=False, same_file=False, kind=lemma
- `Polynomial.Splits.monomial` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 2/3 selected by second-stage; 2/3 by fallback; 2/3 by expansion
  - failure types: `imported_premise_missing`
  - missed `Polynomial.C_mul_X_pow_eq_monomial`: learned_rank=99, base_rank=119, second_stage_ranks=imported_premise_missing:101, fallback=False, expansion=False, same_file=False, kind=theorem

## Interpretation

- Candidate-pool misses are benchmark/candidate-generation ceiling cases, not controller failures.
- Fallback-core drops are the actionable controller weakness: the failure-conditioned scorer can improve positives while still needing a fallback-preservation guardrail.
- Rank misses indicate the second-stage model did not learn enough signal for the observed failure type; these are the best targets for bridge-replay hybrid ablations.
