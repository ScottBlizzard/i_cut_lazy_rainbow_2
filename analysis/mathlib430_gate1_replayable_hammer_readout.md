# Mathlib 4.30 Gate1 Replayable-Subset Readout

Date: 2026-06-22

## Completed Diagnostics

- `outputs/mathlib430_pretheorem_original_tactic_probe_10.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_10.md`
- `outputs/mathlib430_pretheorem_hammer_matrix_replayable3.json`
- `outputs/mathlib430_pretheorem_hammer_matrix_replayable3.md`

## Original-Tactic Replay Probe

10 cleaned Mathlib 4.30 trace goals were patched into their original pre-theorem file context and replayed with the traced tactic script.

Result:

| Status | Count |
|---|---:|
| `verified` | 3 |
| `unknown_identifier` | 3 |
| `type_mismatch` | 1 |
| `simp_fail` | 1 |
| `tactic_fail` | 2 |

Replay-verified goals:

- `mathlib4::Module.rank_tensorProduct'`
- `mathlib4::FirstOrder.Language.definableFun_const`
- `mathlib4::MeasureTheory.Measure.compProd_apply_univ`

Interpretation:

- The Mathlib 4.31 to 4.30 corpus migration is not globally broken.
- We have a valid replayable subset for further verified proof-action experiments.
- Non-replayable rows should not be mixed into Hammer failure analysis until span/context/migration issues are filtered out.

## Hammer Matrix On Replayable Subset

A 90-attempt matrix was run on the 3 replay-verified goals:

- 6 premise sets: `empty`, `proof_core`, `proof_core_plus_learned8`, `learned16`, `base8`, `same_file8_plus_core`.
- 5 Hammer configurations: `aesop_5`, `aesop_10`, `aesop_grind_10`, `grind_only_10`, `auto_aesop_10`.

Result:

| Metric | Value |
|---|---:|
| Replayable goals evaluated | 3 |
| Hammer attempts | 90 |
| Verified Hammer attempts | 8 |
| Goals with at least one Hammer proof | 1 |

Status counts:

| Status | Count |
|---|---:|
| `proved` | 8 |
| `search_fail` | 12 |
| `unknown_identifier` | 16 |
| `lean_error` | 36 |
| `sorry_warning` | 18 |

Goal-level readout:

| Goal | Verified Hammer Attempts | Best Attempt |
|---|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 8 | `empty` / `aesop_10` / 0 premises |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 0 | none |

## Important Interpretation

This is a partial Gate1 pass, not yet a paper-level success.

Positive:

- End-to-end patched Mathlib 4.30 + LeanHammer proof replay can succeed on a real traced theorem.
- Original tactic replay provides a principled filter for selecting valid traced-corpus goals.

Negative:

- The current Hammer positives are not premise-dependent: `Module.rank_tensorProduct'` is solved even with an empty premise list.
- The two more informative replayable goals are not solved by the current Hammer configurations.
- Adding broad candidate sets often hurts because many candidate names are unavailable in the Mathlib 4.30 file context or are not usable as Aesop unsafe rules.

## Next Technical Moves

1. Build a larger replayable subset with the original-tactic probe, likely 50 to 100 cleaned goals.
2. Add premise-context filtering before Hammer attempts:
   - remove names unavailable in the patched file context;
   - separate theorem-like facts from definitions/classes/instances;
   - keep a separate `simp_candidate` pool.
3. Add proof-action templates beyond `hammer [facts]`:
   - `hammer [facts]` for Aesop/Auto/Grind style facts;
   - `simp [simp_candidates]` and `simpa [simp_candidates]` for definitional/simp-heavy goals;
   - optionally `hammerCore [simp_candidates] [facts]` if LeanHammer exposes the simp-lemma list reliably.
4. Rerun the matrix on the replayable subset and require a stricter pass:
   - at least several non-empty-premise successes;
   - at least one goal where feedback/action changes the verified outcome;
   - no circular target candidate leakage.

## Current Risk Assessment

The route is still alive, but the strongest version is likely not "premise selection for `hammer [facts]` only." The evidence is pointing toward a stronger and more defensible action-space claim:

> Failure-aware proof-action routing should decide not only which premises to expose, but also how to expose them to Lean reconstruction: as facts, simp lemmas, rewrite lemmas, local context, or fallback proof actions.

That direction better explains the current failures and may produce a harder, more counterintuitive paper story: more retrieved premises can actively damage reconstruction unless the system routes them through the right proof interface.

## Scaled Update: 50 Replay / 25 Action-Matrix

New outputs:

- `outputs/mathlib430_pretheorem_original_tactic_probe_50.md`
- `outputs/mathlib430_pretheorem_action_matrix_replayable10.md`
- `outputs/mathlib430_pretheorem_action_matrix_replayable25.md`

Replay scale:

- 50 cleaned trace goals probed.
- 25/50 original traced tactics replay in Mathlib 4.30 pre-theorem context.

Proof-action matrix scale:

- 25 replayable goals.
- 275 action attempts.
- 22 verified attempts.
- 17 non-empty-premise verified attempts.
- 6 goals with any proof.
- 3 strict action-dependent goals.

Strict action-dependent positives:

| Goal | Passing non-empty action | Core readout |
|---|---|---|
| `MeasureTheory.Measure.compProd_apply_univ` | `simp_core` / `simpa_core` | core names work as simp lemmas, not Hammer facts |
| `Projectivization.logHeight_nonneg` | `hammerCore_core_plus_learned` | learned additions help when routed through HammerCore simp/fact inputs |
| `Units.inv_mul_cancel_left` | `hammerCore_core` | compact core works through HammerCore interface |

This upgrades the route from "partial Gate 1" to "positive pilot." It is still not final paper evidence because the scale is small and the policy is oracle/action-grid style, but it gives a concrete mainline for the next round.

## Larger Update: 100 Replay / 48 Action-Matrix

New outputs:

- `outputs/mathlib430_pretheorem_original_tactic_probe_100.md`
- `outputs/mathlib430_pretheorem_action_matrix_replayable48.md`
- `outputs/mathlib430_pretheorem_action_matrix_rewrite48.md`

Replay scale:

- 100 cleaned trace goals probed.
- 48/100 original traced tactics replay in Mathlib 4.30 pre-theorem context.

Main proof-action matrix:

- 48 replayable goals.
- 528 action attempts.
- 30 verified attempts.
- 21 non-empty-premise verified attempts.
- 8 goals with any proof.
- Best static action: 5/48.
- Oracle action-grid headroom: 8/48.
- Oracle gap over best static: +3 goals / +6.25 pp.
- Strict action-dependent goals: 3.

Negative extension:

- `simp only` and naive `rw` / `rw; simp` templates: 0/288 verified.
- Dominant statuses: 197 `rewrite_fail`, 64 `simp_fail`, 24 `sorry_warning`.

Current decision:

- Continue proof-action routing.
- Stop naive rewrite-template expansion.
- Improve typed routing for the successful families: `simp/simpa`, `hammerCore [simp] [facts]`, and compact Hammer fact lists.

## Targeted Typed-Action Update

New outputs:

- `outputs/mathlib430_pretheorem_action_matrix_targeted48.md`

Targeted action families:

- `simp_all_core`
- `simp_all_core_plus_learned`
- `simp_rw_core`
- `simp_rw_core_plus_learned`
- `solve_by_elim_core`
- `solve_by_elim_core_plus_learned`

Result:

- 48 replayable goals.
- 288 targeted attempts.
- 8 verified attempts.
- 4 goals with any targeted proof.
- 2 new strict positives not solved by the prior 48-goal main matrix.

New strict positives:

| Goal | Passing Action | Core Readout |
|---|---|---|
| `rTensor.inverse_comp_rTensor` | `solve_by_elim_core` | `LinearMap.range`, `rTensor.inverse`, and `rTensor.inverse_of_rightInverse_comp_rTensor` work as compact elimination facts |
| `SkewMonoidAlgebra.sum_mul` | `solve_by_elim_core` | `Finset.sum_mul` plus relevant structure names work through elimination |

Combined readout:

- Oracle proof-action grid: 10/48.
- Best static action: 5/48.
- Oracle gap: +5 goals / +10.42 pp.
- Strict action-dependent goals: 5.

Current decision update:

- `solve_by_elim` should be included in the next scaled action matrix.
- `simp_all` mostly duplicates existing simp-style positives.
- `simp_rw` has no current positive evidence and should not be blindly scaled.

## Scaled Replay Update

New outputs:

- `outputs/mathlib430_pretheorem_original_tactic_probe_300.md`

Result:

- 300 cleaned trace goals probed.
- 143 original traced tactics replay in the Mathlib 4.30 pre-theorem context.
- Replay rate: 47.7%, consistent with the 48/100 result.

Scaled action-matrix result:

- `outputs/mathlib430_pretheorem_action_matrix_scaled230_merged.md`
- 230 replayable goals from the full 490-goal cleaned subset.
- 3450 action attempts.
- 246 verified attempts.
- 205 non-empty-premise verified attempts.
- Oracle: 51/230.
- Best static: 31/230 (`hammer_core_plus_learned`).
- Empty baseline: 29/230 (`hammer_empty`).
- Strict action-dependent goals: 22.

Decision:

- The scaled oracle-headroom gate passes.
- Current low-capacity routing is not yet enough; `outputs/mathlib430_action_routing_policy_gate_scaled230.md` shows fixed typed portfolios are strong controls.
- Move to richer low-budget routing or reframe the method as a compute-budgeted typed proof-action portfolio.
- Keep excluding naive `rw`, `simp only`, and untyped `simp_rw` scaling.
