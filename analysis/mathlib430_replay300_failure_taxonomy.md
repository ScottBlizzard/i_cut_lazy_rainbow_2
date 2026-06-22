# Mathlib 4.30 Replay-300 Failure Taxonomy

Date: 2026-06-22

Source:

- `outputs/mathlib430_pretheorem_original_tactic_probe_300.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_300.md`

## Summary

300 cleaned trace goals were patched into their original Mathlib 4.30 pre-theorem file context and replayed with the traced original tactic script.

| Status | Count | Working Interpretation |
|---|---:|---|
| `verified` | 143 | replayable subset for proof-action experiments |
| `unknown_identifier` | 59 | name migration, namespace/context drift, or local notation drift |
| `tactic_fail` | 36 | tactic behavior changed or traced script relies on unavailable local state |
| `type_mismatch` | 22 | theorem statement/context changed enough to invalidate replay |
| `parse_error` | 11 | source patching / syntax drift / unicode-sensitive declaration shape |
| `typeclass_or_inference` | 9 | local instance/context drift |
| `rewrite_fail` | 8 | rewrite lemma/direction/context drift |
| `invalid_source_span` | 7 | trace span cannot be patched safely |
| `simp_fail` | 3 | simp-set or local simp context drift |
| `no_by_proof_marker` | 2 | declaration/proof shape not supported by the current patcher |

Replay rate is 143/300 = 47.7%, consistent with the earlier 48/100 probe. This makes the replayable subset stable enough for scaled proof-action evaluation.

## Representative Failures

`unknown_identifier` examples:

- `Submodule.Module.Finite.of_equiv_equiv`
- `Ideal.IsDedekindDomain.ramificationIdx_ne_zero`
- `Ideal.IsNoetherianRing.of_prime`
- `Set.LeftInvOn.RightInvOn.InvOn.Function.Set.SurjOn.exists_subset_injOn_image_eq`
- `HurwitzZeta.hasSum_int_hurwitzZetaOdd`

`tactic_fail` examples:

- `Polynomial.splits_X_sub_C_mul_iff`
- `LocalizedModule.LocalizedModule.IsLocalizedModule.lift_comp`
- `QuadraticMap.QuadraticMap.LinearMap.BilinMap.QuadraticMap.associated_comp`
- `AnalyticWithinAt.pow`
- `gronwallBound_mono`

`type_mismatch` examples:

- `finsum_mem_mul`
- `tprod_setProd_singleton_right`
- `Ideal.height_le_iff_exists_minimalPrimes`
- `ZSpan.discreteTopology_pi_basisFun`
- `Subgroup.mem_centralizer_iff_commutator_eq_one'`

## Decision

- Use only replay-verified goals for proof-action success/failure claims.
- Do not treat non-replayable goals as proof-action failures.
- If more training/evaluation data is needed after the 143-goal matrix, the highest-return replay-harness fixes are likely:
  - name/context normalization for `unknown_identifier`;
  - local instance/context reconstruction for `typeclass_or_inference`;
  - safer patching for `parse_error`, `invalid_source_span`, and `no_by_proof_marker`.
