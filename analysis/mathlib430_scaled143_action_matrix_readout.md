# Mathlib 4.30 Scaled-143 Proof-Action Matrix Readout

Date: 2026-06-22

Canonical outputs:

- `outputs/mathlib430_pretheorem_original_tactic_probe_300.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_300.md`
- `outputs/mathlib430_pretheorem_action_matrix_scaled143.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled143.md`
- `outputs/log_mathlib430_pretheorem_action_matrix_scaled143.txt`

## Protocol

- Replay filter: original traced tactics must replay in the Mathlib 4.30 original-file/pre-theorem context.
- Replay scale: 143 replayable goals from 300 cleaned trace goals.
- Action grid: 15 typed action families, excluding the previously failed naive `rw` and `simp only` templates.
- Attempts: 143 x 15 = 2145.

Included actions:

- `hammer_empty`
- `hammer_core_facts`
- `hammer_core_plus_learned`
- `simp_empty`
- `simp_core`
- `simp_core_plus_learned`
- `simpa_empty`
- `simpa_core`
- `simpa_core_plus_learned`
- `simp_all_core`
- `simp_all_core_plus_learned`
- `solve_by_elim_core`
- `solve_by_elim_core_plus_learned`
- `hammerCore_core`
- `hammerCore_core_plus_learned`

## Headline Result

| Metric | Value |
|---|---:|
| replayable goals evaluated | 143 |
| attempts | 2145 |
| verified attempts | 150 |
| non-empty-premise verified attempts | 124 |
| goals with any proof | 35 / 143 |
| goals with non-empty-premise proof | 35 / 143 |
| best static action | 19 / 143 (`hammer_core_plus_learned`) |
| empty baseline | 18 / 143 (`hammer_empty`) |
| oracle proof-action grid | 35 / 143 |
| oracle gap over best static | +16 goals / +11.19 pp |
| strict action-dependent goals | 17 |

Interpretation:

- The 48-goal result was not a sampling accident. Scaling to 143 replayable goals increases strict action-dependent wins from 5 to 17.
- The strongest claim is no longer just "premises help." The data says proof success depends on the interface used to expose evidence: Hammer facts, simp lemmas, HammerCore mixed inputs, or elimination facts.
- The next required experiment is a learned or rule-based routing policy under matched compute, compared against best static and shuffled/masked controls.

## By Action

| Action | Verified Goals |
|---|---:|
| `hammer_core_plus_learned` | 19 |
| `hammer_core_facts` | 18 |
| `hammer_empty` | 18 |
| `hammerCore_core_plus_learned` | 14 |
| `hammerCore_core` | 11 |
| `simp_core` | 8 |
| `simp_core_plus_learned` | 8 |
| `simpa_core` | 8 |
| `simpa_core_plus_learned` | 8 |
| `simp_all_core` | 8 |
| `simp_all_core_plus_learned` | 8 |
| `solve_by_elim_core` | 7 |
| `solve_by_elim_core_plus_learned` | 7 |
| `simp_empty` | 4 |
| `simpa_empty` | 4 |

## Strict Action-Dependent Goals

Strict means: no empty action proves the goal, but at least one non-empty typed action proves it.

| Goal | Best Passing Action | Facts | Simps |
|---|---|---:|---:|
| `MeasureTheory.Measure.compProd_apply_univ` | `simp_core_plus_learned` | 0 | 6 |
| `Projectivization.logHeight_nonneg` | `hammerCore_core_plus_learned` | 12 | 8 |
| `Units.inv_mul_cancel_left` | `hammerCore_core_plus_learned` | 7 | 5 |
| `rTensor.inverse_comp_rTensor` | `solve_by_elim_core` | 3 | 0 |
| `SkewMonoidAlgebra.sum_mul` | `solve_by_elim_core` | 4 | 0 |
| `dist_eq_norm_inv_mul'` | `hammerCore_core_plus_learned` | 2 | 2 |
| `Equiv.Perm.swap_isSwap_iff` | `hammerCore_core_plus_learned` | 10 | 8 |
| `Stirling.stirlingSeq_one` | `hammerCore_core` | 7 | 7 |
| `Finsupp.card_Iio` | `simpa_core` | 0 | 2 |
| `Ideal.span_pair_abs` | `simp_core` | 0 | 4 |
| `NumberField.rootDiscr_def` | `simp_core` | 0 | 3 |
| `ENNReal.mul_div_right_comm` | `hammerCore_core` | 1 | 1 |
| `continuousWithinAt_singleton` | `simp_core` | 0 | 3 |
| `MeasureTheory.average_const` | `simp_all_core_plus_learned` | 0 | 9 |
| `CategoryTheory.Limits.pullbackSymmetry_inv_comp_fst` | `hammerCore_core_plus_learned` | 11 | 10 |
| `Matrix.dotProductᵣ_eq` | `simp_core` | 0 | 4 |
| `Nat.Primes.PNat.Prime.ne_one` | `hammer_core_plus_learned` | 6 | 0 |

## Decision

This passes the scaled oracle-headroom gate. Continue to a verified routing-policy experiment:

1. Build per-goal action labels from `outputs/mathlib430_pretheorem_action_matrix_scaled143.json`.
2. Train or hand-prototype a policy on the 85-goal train split.
3. Evaluate on dev/test against:
   - best static action;
   - empty-only baseline;
   - fixed portfolio schedule;
   - shuffled or masked failure/action features if available.
4. Report both all-goal oracle and strict action-dependent subsets.

Do not return to naive rewrite expansion. The current data supports typed proof-action routing, not untyped template proliferation.

## Policy Gate Update

Additional outputs:

- `outputs/mathlib430_action_routing_policy_gate_status_rule.json`
- `outputs/mathlib430_action_routing_policy_gate_status_rule.md`

Readout:

- Coarse first-failure-status routing ties the best fixed second action on the 30-goal test split and underperforms it in 5-fold out-of-fold evaluation.
- Text NB over theorem name and `hammer_empty` output improves train/dev but does not beat the best fixed second action on test or out of fold.
- A train-greedy fixed typed portfolio with four extra actions after `hammer_empty` reaches 35/143, matching the action-grid oracle.

Updated decision:

- Do not claim adaptive policy success yet.
- The current hard evidence supports typed proof-action diversity and a strong compute-success tradeoff.
- The next method gate should test whether richer transcript/goal/action features can match the 3-4 action fixed portfolio while using only one second action.
