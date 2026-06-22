# Mathlib 4.30 Pre-Theorem Patch Probe

- Verdict: `probe_completed_no_proofs`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_clean_trace_subset_500.jsonl`
- Goals checked: 3
- Verified by patched Hammer proof: 0

## Status Counts

| Status | Count |
|---|---:|
| `search_fail` | 2 |
| `type_mismatch` | 1 |

## Results

| Goal | Status | Time |
|---|---|---:|
| `mathlib4::Submodule.Module.Finite.of_equiv_equiv` | `search_fail` | 6.59s |
| `mathlib4::finsum_mem_mul` | `type_mismatch` | 15.21s |
| `mathlib4::AlgebraicGeometry.HasAffineProperty.affineAnd_le_affineAnd` | `search_fail` | 11.57s |

## Readout

- This is the first probe of original-file/pre-theorem replay.
- Failure can mean span drift, Hammer search weakness under the controlled options, or true premise insufficiency.
