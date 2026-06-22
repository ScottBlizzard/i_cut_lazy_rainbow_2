# Mathlib 4.30 Pre-Theorem Original-Tactic Probe

- Verdict: `pass`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_clean_trace_subset_500.jsonl`
- Goals checked: 10
- Original tactic replay verified: 3

## Status Counts

| Status | Count |
|---|---:|
| `unknown_identifier` | 3 |
| `type_mismatch` | 1 |
| `simp_fail` | 1 |
| `verified` | 3 |
| `tactic_fail` | 2 |

## Results

| Goal | Status | Time |
|---|---|---:|
| `mathlib4::Submodule.Module.Finite.of_equiv_equiv` | `unknown_identifier` | 6.06s |
| `mathlib4::finsum_mem_mul` | `type_mismatch` | 14.06s |
| `mathlib4::AlgebraicGeometry.HasAffineProperty.affineAnd_le_affineAnd` | `simp_fail` | 10.93s |
| `mathlib4::Ideal.IsDedekindDomain.ramificationIdx_ne_zero` | `unknown_identifier` | 6.59s |
| `mathlib4::Module.rank_tensorProduct'` | `verified` | 7.11s |
| `mathlib4::FirstOrder.Language.definableFun_const` | `verified` | 4.18s |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | `verified` | 4.70s |
| `mathlib4::Ideal.IsNoetherianRing.of_prime` | `unknown_identifier` | 3.80s |
| `mathlib4::Polynomial.splits_X_sub_C_mul_iff` | `tactic_fail` | 9.02s |
| `mathlib4::LocalizedModule.LocalizedModule.IsLocalizedModule.lift_comp` | `tactic_fail` | 22.53s |

## Readout

- At least one cleaned traced theorem can be replayed in the original Mathlib 4.30 file context, so corpus migration is not globally broken.
- Remaining negative Hammer results should be debugged as action/premise/backend limitations on the replayable subset.
