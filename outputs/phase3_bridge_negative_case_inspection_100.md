# Phase 3 Bridge Negative-Case Inspection

This report inspects replay-verified misses where the second-stage controller did not recover trace-core proof cores.

## Summary

- Inspected cases: 12
- Candidate-pool miss cases: 0
- Second-stage dropped a fallback-selected core premise: 7
- Second-stage dropped an expansion-selected core premise: 0

### Groups

| Group | Count |
|---|---:|
| `fallback_bridge_over_second_stage` | 4 |
| `replay_verified_both_fail` | 8 |

### Reasons

| Reason | Count |
|---|---:|
| `failure_conditioned_rank_miss` | 10 |
| `second_stage_dropped_fallback_core` | 7 |
| `budget_or_path_miss_with_core_ranked_in_top96` | 2 |

### Second-Stage Failure Types

| Failure type | Count |
|---|---:|
| `imported_premise_missing` | 12 |
| `type_mismatch` | 1 |
| `missing_bridge` | 1 |

### Missed-Core Rank Stats

| Rank source | Count | Median | Min | Max | Top64 | Top96 |
|---|---:|---:|---:|---:|---:|---:|
| `best second-stage` | 17 | 115.0 | 11 | 207 | 4 | 4 |
| `learned` | 17 | 125.0 | 99 | 231 | 0 | 0 |
| `base` | 17 | 9.0 | 1 | 221 | 12 | 13 |

## Case Details

### `fallback_bridge_over_second_stage`

- `WeierstrassCurve.Jacobian.neg_of_Z_ne_zero` (fallback_over_second_stage, `fallback_bridge_over_second_stage`)
  - reasons: `second_stage_dropped_fallback_core`, `failure_conditioned_rank_miss`
  - core: 3/4 selected by second-stage; 4/4 by fallback; 3/4 by expansion
  - failure types: `imported_premise_missing`
  - missed `WeierstrassCurve.Jacobian.negY_of_Z_ne_zero`: learned_rank=116, base_rank=1, second_stage_ranks=imported_premise_missing:131, fallback=True, expansion=False, same_file=False, kind=lemma
- `Multiset.Subset.ndinter_eq_left` (fallback_over_second_stage, `fallback_bridge_over_second_stage`)
  - reasons: `second_stage_dropped_fallback_core`, `failure_conditioned_rank_miss`
  - core: 3/4 selected by second-stage; 4/4 by fallback; 3/4 by expansion
  - failure types: `imported_premise_missing`
  - missed `List.Subset.inter_eq_left`: learned_rank=179, base_rank=9, second_stage_ranks=imported_premise_missing:177, fallback=True, expansion=False, same_file=False, kind=theorem
- `equicontinuousWithinAt_iInf_rng` (fallback_over_second_stage, `fallback_bridge_over_second_stage`)
  - reasons: `second_stage_dropped_fallback_core`, `budget_or_path_miss_with_core_ranked_in_top96`
  - core: 7/8 selected by second-stage; 8/8 by fallback; 7/8 by expansion
  - failure types: `imported_premise_missing`, `type_mismatch`
  - missed `equicontinuousWithinAt_iff_continuousWithinAt`: learned_rank=122, base_rank=8, second_stage_ranks=imported_premise_missing:121, type_mismatch:26, fallback=True, expansion=False, same_file=True, kind=theorem
- `Nat.Primes.PNat.Prime.ne_one` (fallback_over_second_stage, `fallback_bridge_over_second_stage`)
  - reasons: `second_stage_dropped_fallback_core`, `failure_conditioned_rank_miss`
  - core: 0/1 selected by second-stage; 1/1 by fallback; 0/1 by expansion
  - failure types: `imported_premise_missing`
  - missed `Nat.Prime.ne_one`: learned_rank=107, base_rank=3, second_stage_ranks=imported_premise_missing:107, fallback=True, expansion=False, same_file=False, kind=theorem

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
- `WeierstrassCurve.Jacobian.addY_neg` (both_fail, `replay_verified_both_fail`)
  - reasons: `second_stage_dropped_fallback_core`, `budget_or_path_miss_with_core_ranked_in_top96`
  - core: 1/4 selected by second-stage; 3/4 by fallback; 1/4 by expansion
  - failure types: `imported_premise_missing`, `missing_bridge`
  - missed `WeierstrassCurve.Jacobian.addX_neg`: learned_rank=202, base_rank=6, second_stage_ranks=imported_premise_missing:204, missing_bridge:16, fallback=True, expansion=False, same_file=True, kind=lemma
  - missed `WeierstrassCurve.Jacobian.addZ_neg`: learned_rank=120, base_rank=4, second_stage_ranks=imported_premise_missing:127, missing_bridge:11, fallback=True, expansion=False, same_file=True, kind=lemma
  - missed `WeierstrassCurve.Jacobian.negAddY_neg`: learned_rank=231, base_rank=1, second_stage_ranks=imported_premise_missing:228, missing_bridge:20, fallback=True, expansion=False, same_file=True, kind=lemma
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
  - reasons: `second_stage_dropped_fallback_core`, `failure_conditioned_rank_miss`
  - core: 6/9 selected by second-stage; 7/9 by fallback; 6/9 by expansion
  - failure types: `imported_premise_missing`
  - missed `WeierstrassCurve.Affine.nonsingular_iff'`: learned_rank=148, base_rank=77, second_stage_ranks=imported_premise_missing:137, fallback=False, expansion=False, same_file=False, kind=lemma
  - missed `WeierstrassCurve.Projective.equation_some`: learned_rank=133, base_rank=4, second_stage_ranks=imported_premise_missing:118, fallback=True, expansion=False, same_file=True, kind=lemma
  - missed `WeierstrassCurve.Projective.nonsingular_iff`: learned_rank=209, base_rank=28, second_stage_ranks=imported_premise_missing:207, fallback=False, expansion=False, same_file=True, kind=lemma
- `Rat.intCast_div` (both_fail, `replay_verified_both_fail`)
  - reasons: `second_stage_dropped_fallback_core`, `failure_conditioned_rank_miss`
  - core: 2/4 selected by second-stage; 3/4 by fallback; 2/4 by expansion
  - failure types: `imported_premise_missing`
  - missed `Int.cast_mul`: learned_rank=125, base_rank=157, second_stage_ranks=imported_premise_missing:114, fallback=False, expansion=False, same_file=False, kind=lemma
  - missed `Rat.intCast_div_self`: learned_rank=134, base_rank=6, second_stage_ranks=imported_premise_missing:142, fallback=True, expansion=False, same_file=True, kind=theorem
- `Polynomial.Splits.monomial` (both_fail, `replay_verified_both_fail`)
  - reasons: `failure_conditioned_rank_miss`
  - core: 2/3 selected by second-stage; 2/3 by fallback; 2/3 by expansion
  - failure types: `imported_premise_missing`
  - missed `Polynomial.C_mul_X_pow_eq_monomial`: learned_rank=99, base_rank=119, second_stage_ranks=imported_premise_missing:101, fallback=False, expansion=False, same_file=False, kind=theorem

## Interpretation

- Candidate-pool misses are benchmark/candidate-generation ceiling cases, not controller failures.
- Fallback-core drops are the actionable controller weakness: the failure-conditioned scorer can improve positives while still needing a fallback-preservation guardrail.
- Rank misses indicate the second-stage model did not learn enough signal for the observed failure type; these are the best targets for bridge-replay hybrid ablations.
