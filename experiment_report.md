# ICLR_2 Experiment Report

Updated: 2026-06-23

This report keeps the useful experimental record for the current paper. The current paper route is action-conditional evidence allocation for Lean proof reconstruction. Earlier failure-aware premise-selection results remain useful background, but they are no longer the main verified claim.

## 0. Current Paper-Level Readout

The strongest verified route is not an adaptive learned router. It is a typed proof-action/evidence-allocation mechanism:

- A frozen Mathlib 4.30 replayable subset has 230 verified replay goals.
- The full action matrix has 11,500 Lean attempts and 582 verified attempts.
- The action-grid oracle solves 58/230 goals.
- The best single static action is `aesop_core_plus_learned`, solving 38/230 goals.
- `hammer_empty` and `aesop_empty` each solve 29/230 goals.
- Fixed typed portfolios solve 49/230 at K=1, 55/230 at K=2, 55/230 at K=3, and 57/230 at K=4 out of fold.
- A train-fitted K=4 typed portfolio reaches the 58/230 oracle.

Important transparency point:

- In the current action names, `core` means traced `proof_core`; in paper wording it must be called `oracle_core` unless explicitly defined otherwise.
- The main result is therefore a mechanism-isolation result over `oracle_core + retrieved` evidence, not a deployable retriever-only theorem prover.

Canonical files:

- `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.md`
- `outputs/mathlib430_budgeted_action_policy_scaled230_aesop_ablation.md`
- `outputs/mathlib430_typed_allocator_gate_scaled230_aesop_ablation.md`
- `analysis/mathlib430_protocol_freeze_evidence_contract.md`
- `analysis/mathlib430_evidence_contract_audit.md`
- `analysis/mathlib430_aesop_exact_controls_summary.md`

## 1. Replayable Mathlib 4.30 Subset

Goal: move from trace-level proxy metrics to real Lean replayable theorem contexts.

Canonical files:

- `outputs/mathlib430_clean_trace_subset_500.jsonl`
- `outputs/mathlib430_pretheorem_original_tactic_probe_490.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_490.md`
- `outputs/mathlib430_replayable490_splits.json`

Result:

- 230/490 cleaned trace goals replay under the original traced tactic script.
- The stable split uses SHA256-sorted goal IDs with 138 train, 46 dev, and 46 test goals.
- All OOF portfolio/policy results should use this split or a deterministic fold split over these 230 goals.

## 2. Main Action Matrix

Goal: test whether the same evidence must be compiled into different Lean proof interfaces rather than only ranked as premises.

Canonical files:

- `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.md`

Core result:

| Metric | Value |
|---|---:|
| Goals | 230 |
| Attempts | 11,500 |
| Verified attempts | 582 |
| Non-empty-premise verified attempts | 508 |
| Oracle goals | 58/230 |
| Best static action | `aesop_core_plus_learned` |
| Best static goals | 38/230 |
| Strict action-dependent goals | 29 |

Best static actions:

| Action | Verified goals |
|---|---:|
| `aesop_core_plus_learned` | 38 |
| `aesop_core_plus_learned16` | 37 |
| `hammer_core_plus_learned16` | 32 |
| `hammer_core_plus_learned32` | 32 |
| `hammer_core_plus_learned` | 31 |
| `aesop_empty` | 29 |
| `hammer_core_facts` | 29 |
| `hammer_empty` | 29 |

Interpretation:

- The oracle gap over the best single action is +20 goals.
- The useful intervention is not "add more names"; it is choosing the Lean action/interface and the channel through which evidence is consumed.
- The 38/230 Aesop result is strong but must be compared against `aesop_empty=29/230`, not only against facts-only/simps-only controls.

## 3. Aesop Channel/Source Mechanism

Goal: isolate whether Aesop succeeds because of facts, simp lemmas, source composition, or their interaction.

Canonical files:

- `analysis/mathlib430_aesop_exact_controls_summary.json`
- `analysis/mathlib430_aesop_exact_controls_summary.md`
- `outputs/aesop_exact_essential1_jsons.tgz`
- `outputs/aesop_exact_essential1_mds.tgz`
- `analysis/mathlib430_evidence_contract_audit.json`
- `analysis/mathlib430_evidence_contract_audit.md`

Exact P0 results:

| Source / exposure | Verified goals | Gain vs empty | Loss vs empty | Net |
|---|---:|---:|---:|---:|
| Empty Aesop | 29/230 | - | - | - |
| `oracle_core+retrieved`, joint facts+simps | 38/230 | 20 | 11 | +9 |
| `oracle_core+retrieved`, identity | 36/230 | 18 | 11 | +7 |
| `oracle_core+retrieved`, simps-only | 35/230 | 17 | 11 | +6 |
| `oracle_core+retrieved`, facts-only | 32/230 | 3 | 0 | +3 |
| `oracle_core+retrieved`, random split | 32/230 | 10 | 7 | +3 |
| `retrieved-only`, joint facts+simps | 34/230 | 16 | 11 | +5 |
| `oracle-core-only`, joint facts+simps | 35/230 | 16 | 10 | +6 |

Matched-triple readout:

- In the `oracle_core+retrieved` source mode, joint facts+simps is best at 38/230.
- Exact controls explain most of the old apparent channel-complementarity story: identity is 36/230, simps-only is 35/230, facts-only is 32/230, and joint-only over exact single-channel controls is only 2 goals.
- Source composition has a modest effect: `retrieved-only` reaches 34/230, `oracle-core-only` reaches 35/230, and the mixed source reaches 38/230.
- The deployable-source anchor is nonzero (`retrieved-only` 34/230), but it is not yet a full external retriever-only theorem-proving result.

Interpretation:

- P0 is a no-go for strong causal wording such as "Aesop facts and simps are deeply complementary."
- The paper should instead say: Aesop is source/exposure/search sensitive; joint oracle-core plus retrieved exposure is the best Aesop row, but the margin over exact controls is modest.
- The main paper route should lean on typed portfolio diversity, homogeneous K=4 controls, wallclock accounting, and transparent oracle-core provenance.

## 4. Homogeneous Portfolio Controls

Goal: answer whether typed diversity beats four calls from one action family.

Canonical file:

- `analysis/mathlib430_evidence_contract_audit.md`

OOF K=4 results:

| Portfolio group | OOF K=4 |
|---|---:|
| Full typed action grid | 57/230 |
| Typed non-empty grid | 57/230 |
| Aesop-only | 49/230 |
| HammerCore-only | 41/230 |
| Simplification-only | 41/230 |
| Solve-by-elim-only | 34/230 |
| Hammer-only | 32/230 |
| Raw arithmetic/normalization-only | 29/230 |

Random full-grid K=4 over 100 seeds:

- Mean: 41.9/230.
- Median: 42/230.
- Range: 31-56.

Interpretation:

- The fixed typed portfolio is not merely "try Aesop four times."
- Typed diversity is the best current verified budgeted control.
- Random portfolios can approach but do not reliably match the greedy typed portfolio.

## 5. Compute/Cost Accounting

Goal: avoid unsupported "matched compute" claims.

Canonical file:

- `analysis/mathlib430_evidence_contract_audit.md`

Empirical runner-wallclock frontier:

| Policy | Success | Avg calls | Avg time |
|---|---:|---:|---:|
| `hammer_empty` | 29/230 | 1.00 | 8.31s |
| `aesop_core_plus_learned` after empty | 49/230 | 1.87 | 16.36s |
| Full typed train-fitted K=2 | 55/230 | 2.66 | 26.37s |
| Full typed train-fitted K=4 | 58/230 | 4.18 | 40.07s |

Interpretation:

- The paper can claim matched Lean-call budget.
- It can report empirical runner-wallclock as a secondary frontier.
- It should not claim heartbeat-normalized matched compute unless a new heartbeat experiment is added.

## 6. Typed Allocator Gate

Goal: test whether learned adaptive action allocation beats the fixed typed portfolio.

Canonical files:

- `outputs/mathlib430_typed_allocator_gate_scaled230_aesop_ablation.json`
- `outputs/mathlib430_typed_allocator_gate_scaled230_aesop_ablation.md`

Results:

- Fixed greedy OOF K=4: 57/230.
- Pure logistic regression K=4: 47/230.
- Unbalanced logistic regression K=4: 49/230.
- ComplementNB K=4: 39/230.
- Fixed-prefix residual logreg/CNB match fixed K=4 at 57/230 but do not beat or compress it.

Interpretation:

- Learned adaptive allocation is not supported as the current main claim.
- It remains a future direction only if a stronger feature set beats the fixed typed control.

## 7. Strict Filtering Boundary

Goal: test whether stricter theorem-like/simp-attr filtering fixes premise poisoning.

Canonical files:

- `analysis/mathlib430_e1_strict_interface_filtering.json`
- `analysis/mathlib430_e1_strict_interface_filtering.md`

Results:

- Filtered-only oracle: 4/230.
- Combined oracle: 58/230.
- New oracle goals: 0.
- Selected names mostly available: 7321/7497.
- Target/alias hits: 24.

Interpretation:

- Broad strict filtering over-cleans and destroys successes.
- This is a useful negative robustness boundary, not a method improvement.

## 8. Legacy Failure-Aware Premise Selection Results

These results motivated the project but should not dominate the current paper.

Useful historical takeaways:

- Same-file/local trace-core recovery showed failure-aware expansion can beat static top-k/rerank controls.
- Timeout stress showed the counterintuitive result that adding more premises can reduce success under timeout pressure.
- Bridge replay showed some trace-core gains survive real Lean replay filters.
- Imported-core global retrieval showed learned second-stage scoring can help recover traced proof-core labels.

Limitations:

- These are mostly trace-core/proof-core recovery results.
- They do not by themselves prove theorem reconstruction competitiveness.
- They use traced proof-core labels and should be appendix/background unless the paper is fully reframed again.

Representative canonical files:

- `outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.md`
- `outputs/phase1_reconstruction_bridge_report_100.md`
- `outputs/phase2_timeout_stress_2000_a40.md`
- `outputs/phase3_imported_core_*`

## 9. Completed P0 Exact Controls

The exact Aesop source/channel controls were run on A40 as 690 one-goal singleton jobs:

- 230 goals x 3 source modes x 9 essential Aesop actions.
- Source modes: `oracle_plus_retrieved`, `retrieved_only`, `oracle_core_only`.
- Actions: empty, joint, facts-only, simps-only, identity, swapped, count-matched facts, count-matched simps, and deterministic random split.

Canonical summary:

```bash
python src/summarize_mathlib430_aesop_exact_controls.py \
  --inputs outputs/mathlib430_aesop_exact_controls_*_essential1_g*.json \
  --out-json analysis/mathlib430_aesop_exact_controls_summary.json \
  --out-md analysis/mathlib430_aesop_exact_controls_summary.md
```

Conclusion:

- Strong Aesop channel-complementarity is not supported by the exact controls.
- The paper remains viable as an action-conditional evidence-allocation paper, but the Aesop subsection must be written as a modest mechanism/boundary rather than the headline causal result.
