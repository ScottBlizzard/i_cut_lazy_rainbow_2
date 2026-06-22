# Mathlib 4.30 Aesop Counterfactual Channel Controls

Date: 2026-06-23

## Setup

- Matrix: `outputs\mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- Goals: 230
- Control type: matched Aesop source/budget with channel removed or combined.
- Caveat: fact and simp pools are matched by source/budget and goal, but they are typed pools; they are not assumed to contain identical names.

## Headline

- Best matched source is `core+learned8`: facts+simps solves 38/230 (16.5%), facts-only solves 5/230, and simps-only solves 4/230.
- The union of the two single-channel controls solves 7/230; joint exposure has 34 joint-only goals and 3 single-channel-only misses.
- Joint exposure beats the better single channel by 33 goals for the best source.

## Matched Channel Controls

| Source | Facts+simps | Facts-only | Simps-only | Single-channel union | Joint-only | Single-only not joint | Joint gain over best single |
|---|---:|---:|---:|---:|---:|---:|---:|
| `core` | 4/230 | 5/230 | 4/230 | 7/230 | 0 | 3 | -1 |
| `core+learned8` | 38/230 | 5/230 | 4/230 | 7/230 | 34 | 3 | 33 |
| `core+learned16` | 37/230 | 5/230 | 3/230 | 7/230 | 34 | 4 | 32 |
| `core+learned32` | 3/230 | 5/230 | 3/230 | 7/230 | 0 | 4 | -2 |
| `learned8` | 4/230 | 5/230 | 4/230 | 7/230 | 0 | 3 | -1 |
| `learned16` | 3/230 | 5/230 | 3/230 | 7/230 | 0 | 4 | -2 |
| `learned32` | 3/230 | 5/230 | 3/230 | 7/230 | 0 | 4 | -2 |

## Exposure-Budget Non-Monotonicity

| Family | Exposure | K=8 | K=16 | K=32 | Lost 8->32 | Gained 8->32 |
|---|---|---:|---:|---:|---:|---:|
| `core+learned` | `facts+simps` | 38/230 | 37/230 | 3/230 | 35 | 0 |
| `core+learned` | `facts-only` | 5/230 | 5/230 | 5/230 | 0 | 0 |
| `core+learned` | `simps-only` | 4/230 | 3/230 | 3/230 | 1 | 0 |
| `learned` | `facts+simps` | 4/230 | 3/230 | 3/230 | 1 | 0 |
| `learned` | `facts-only` | 5/230 | 5/230 | 5/230 | 0 | 0 |
| `learned` | `simps-only` | 4/230 | 3/230 | 3/230 | 1 | 0 |

## Representative Joint-Only Goals

### `core+learned8`

`mathlib4::Affine.Simplex.face_restrict`, `mathlib4::Algebra.Presentation.aeval_comp_val_eq`, `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms`, `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply`, `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.TaggedPrepartition.forall_mem_single`, `mathlib4::CategoryTheory.Core.Functor.Iso.coreWhiskerLeft`, `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom`, `mathlib4::Equiv.Perm.apply_mem_support`, `mathlib4::Finset.Fin.prod_Ioo_cast`, `mathlib4::Finset.biUnion_inter`, `mathlib4::Finset.insert_inter`, `mathlib4::Finset.max'_singleton`, ... (+22)

### `core+learned16`

`mathlib4::Affine.Simplex.face_restrict`, `mathlib4::Algebra.Presentation.aeval_comp_val_eq`, `mathlib4::AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms`, `mathlib4::BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply`, `mathlib4::BoxIntegral.TaggedPrepartition.Prepartition.TaggedPrepartition.forall_mem_single`, `mathlib4::CategoryTheory.Core.Functor.Iso.coreWhiskerLeft`, `mathlib4::CategoryTheory.Limits.inr_zeroCoprodIso_hom`, `mathlib4::Equiv.Perm.apply_mem_support`, `mathlib4::Finset.Fin.prod_Ioo_cast`, `mathlib4::Finset.biUnion_inter`, `mathlib4::Finset.insert_inter`, `mathlib4::Finset.max'_singleton`, ... (+22)

## Readout

- This is the paper-critical counterfactual control: for the same Aesop source/budget, removing either channel largely destroys the best result.
- The result supports an action-conditional evidence-allocation thesis: selected evidence must be compiled into the interface channels that can consume it.
- The non-monotonic K=8/16/32 rows support the anti-blind-expansion claim: more exposed names can hurt.
