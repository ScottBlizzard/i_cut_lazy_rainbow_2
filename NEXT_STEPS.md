# NEXT_STEPS

Updated: 2026-06-22

This file only keeps unfinished work after the Mathlib 4.30 verified pivot. Completed trace-core, bridge, generated Gate 1/2, Mathlib compatibility, cleaning, replay diagnostics, and current proof-action pilots are recorded in `experiment_report.md`.

## Current Judgment

The route is alive, but not yet paper-strong.

- Original-file/pre-theorem replay is feasible at useful scale: `outputs/mathlib430_pretheorem_original_tactic_probe_490.md` verified 230/490 original traced tactic scripts.
- Hammer-only is weak because the first traced-corpus positive is empty-premise-solvable.
- Proof-action routing is the live route: the original scaled230 matrix had oracle 51/230 vs best static 31/230 and 22 strict action-dependent goals; the extended matrix `outputs/mathlib430_pretheorem_action_matrix_scaled230_extended_merged.md` improves this to oracle 58/230 vs best static 38/230 and 29 strict action-dependent goals.
- Full Aesop-ablation matrix `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.md` keeps the oracle at 58/230 and confirms the same 29 strict action-dependent goals; it is mechanism evidence, not a ceiling increase.
- Naive `simp only` / `rw` expansion is a dead branch for now: `outputs/mathlib430_pretheorem_action_matrix_rewrite48.md` has 0/288 verified.
- `solve_by_elim` is now a confirmed useful action family; `simp_rw` has no positive evidence so far.
- Low-capacity adaptive policies are still not enough: `outputs/mathlib430_action_routing_policy_gate_scaled230.md` shows text NB is only weakly better than fixed second action out of fold and ties it on the heldout test split.
- Budgeted policy gate is now complete through the Aesop-ablation matrix. OOF fixed greedy K=2 reaches 55/230, K=4 reaches 57/230, and the oracle is 58/230; residual adaptive policies still do not clearly beat the fixed typed portfolio.
- Fixed typed portfolio is now the strongest verified route: `aesop_core_plus_learned`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, and `solve_by_elim_core` reach 58/230 train-fitted and 57/230 OOF.
- The extended action run is complete. `aesop_core_plus_learned` is the new best static action with 38/230 verified goals.
- The focused `aesop` ablation is complete. `facts+simps` solves 38/230, while facts-only solves 5/230 and simps-only solves 4/230; `core+learned32` drops to 7/230 group coverage, so broad insertion is harmful.
- Broad candidate insertion still damages reconstruction unless names are filtered and routed through the right interface.
- `iclr2027/paper.tex` has been rewritten around the typed proof-action portfolio mainline and compiled to `iclr2027/paper.pdf`. The current paper claim is scoped as a verified interface-mechanism result, not as adaptive routing or a full theorem-proving leaderboard.
- `analysis/paper_adversarial_review_typed_portfolio.md` records the current reviewer risks, claim-evidence map, and exact next experiments.
- `analysis/deep_research_report_maintrack_review.md` independently agrees with the current strategic order: do not restart, strengthen the typed interface-mechanism paper, run E1 interface filtering first, run E2 paired stability second, and only attempt E3 adaptive routing if E1 creates new headroom or action diversity.
- E1 strict interface filtering is complete: `analysis/mathlib430_e1_strict_interface_filtering.md` shows filtered-only oracle 4/230, combined oracle still 58/230, and no new oracle goals. The audit is useful because names are mostly available (7321/7497) and target/alias hits are low (24), but strict theorem-like/simp-attr filtering over-cleans the interface and destroys most Aesop successes.

## P1. Stabilize The Replayable Subset

Goal: expand the replayable subset beyond the first 100 cleaned trace goals, then create stable evaluation splits.

Pending:

1. Do not expand replay beyond 490 cleaned goals by default; current bottleneck is method framing, typed-interface filtering, and policy strength, not lack of a larger replayable subset.
2. Taxonomize replay failures into migration/span drift, tactic drift, typeclass/context drift, and downstream file breakage only if more replayable data is needed.

## P2. Fix Premise Exposure

Goal: prevent invalid or wrong-interface premises from poisoning Lean reconstruction.

Completed:

1. Ran the strict interface filtering gate on the 230 replayable goals for `aesop_core_plus_learned`, `aesop_core_plus_learned16`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned16`, and `solve_by_elim_core`.
2. Added context visibility / candidate survival audit to `src/run_mathlib430_pretheorem_action_matrix.py`.
3. Split selected names into audit categories:
   - fact candidates for `hammer [facts]`;
   - simp candidates for `simp [lemmas]` / `simpa [lemmas]`;
   - HammerCore simp/fact pairs;
   - definitions/classes/instances that should not be sent to Aesop as unsafe rules.
4. Added target theorem / alias guards for the strict filtering audit. Same-file-later declaration filtering still lacks candidate declaration spans and should not be claimed as complete.
5. Recorded candidate survival rates per goal and per interface in the E1 outputs.

Pending:

1. Do not continue stricter theorem-like/simp-attr filtering variants as a mainline: E1 did not add oracle goals and reduced filtered-only oracle to 4/230.
2. If filtering is revisited, use it as a more surgical diagnostic, not as another broad strict policy. Candidate declaration spans would be needed before claiming same-file-later leak filtering.

## P3. Improve Proof-Action Routing

Current pilot:

- 230 replayable goals.
- 11500 full scaled action attempts after Aesop ablation.
- 582 verified attempts.
- 508 non-empty-premise verified attempts.
- Oracle 58/230 vs best static 38/230.
- 29 strict action-dependent goals.
- Budgeted policy gate: fixed greedy K=2 reaches 55/230 OOF, fixed greedy K=4 reaches 57/230 OOF, train-fitted K=4 reaches 58/230. Residual NB/kNN do not clearly beat the typed portfolio baseline.
- 48-goal negative branch remains valid: naive rewrite/simp-only attempts had 0/288 verified.

Pending:

1. Keep the paper mainline fixed as `aesop`-augmented typed proof-action portfolios unless a new verified experiment changes the evidence.
2. Produce a paired portfolio stability table: per-fold K=1/2/3/4, paired wins/losses versus best single action and `hammer_empty`, strict-only coverage, and only-family counts. The lightweight output `outputs/mathlib430_fixed_portfolio_stability_scaled230_e1_filtered.md` already provides the first fixed-greedy per-fold table; extend it with clearer paired win/loss summaries for paper use.
3. Treat E1 as a robustness boundary: strict filtering is useful evidence against unknown-identifier/target-leak explanations, but it does not improve the method.
4. Do not continue naive `rw` / `simp only` templates without a typed rewrite-direction selector.
5. Do not scale `simp_rw` unless a typed rewrite-direction selector is added.

## P4. Traced-Corpus Verified Gate 2

Prerequisite: convert the current oracle headroom, 58/230 vs 38/230, into a policy gain under matched compute.

Pending:

1. Report paired stability for fixed typed portfolios versus oracle, while clearly marking the replayable-subset boundary.
2. Only add true/masked/shuffled controls if a new policy first beats fixed typed portfolios under matched compute.

## P5. Verified Failure-Conditioned Policy

Prerequisite: P4 has enough oracle headroom.

Pending:

1. Do not claim a verified failure-conditioned policy until it beats fixed typed portfolios under matched compute.
2. Train a new failure transcript -> action policy only if the feature set is materially stronger than the current NB/kNN policy; current evidence does not justify another low-capacity rerun.
3. Compare true feedback with masked, shuffled, fixed, cyclic, and failure-agnostic controls only after item 2 has a plausible positive.
4. Separate semantic failure-transcript gain from generic retry-portfolio gain.

Prepared inputs:

- `analysis/deep_research_report_maintrack_review.md`
- `analysis/mathlib430_e1_strict_interface_filtering.md`
- `analysis/paper_adversarial_review_typed_portfolio.md`
- `outputs/mathlib430_replayable490_goal_ids.txt`
- `outputs/mathlib430_replayable490_splits.json` with 138 train / 46 dev / 46 test goals.
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_merged.json`
- `outputs/mathlib430_budgeted_action_policy_scaled230.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_extended_merged.json`
- `outputs/mathlib430_budgeted_action_policy_scaled230_extended.json`
- `analysis/mathlib430_strict_action_taxonomy_scaled230_extended.md`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- `outputs/mathlib430_budgeted_action_policy_scaled230_aesop_ablation.json`
- `analysis/mathlib430_strict_action_taxonomy_scaled230_aesop_ablation.md`
- `analysis/mathlib430_aesop_ablation_scaled230.md`

## Do Not Do

- Do not present generated Mathlib theorem-family Gate 2 as the final main experiment.
- Do not count empty-premise Hammer successes as evidence for premise intervention.
- Do not go back to Hammer-only unless proof-action routing fails after typed routing improvements.
- Do not continue naive `rw` / `simp only` expansion.
- Do not mix non-replayable trace goals into proof-action failure analysis.
- Do not describe bridge replay as full theorem proving.
