# Oral Upgrade Execution Plan

更新时间：2026-06-22

来源：`analysis/iclr_oral_upgrade_report.md`

## 0. Decision

采纳 GPT Pro 的核心判断：当前 `ICLR_2` 不应继续围绕 trace-core 小变体调参，也不应把 95.7%、92.9%、53.5% 这些 proxy result 当作最终目标继续包装。当前最有 oral 潜力的路线是把主线 pivot 到：

> Verified adaptive premise interventions: after a fixed first Lean hammer failure, use the observed failure transcript to choose a premise-set action under equal compute, and show that this adaptive policy improves kernel-verified proof success over the best static portfolio.

当前 trace-core / bridge 结果保留为 discovery and continuity evidence，不再作为 oral-level main claim 的最终证据。

## 1. New Main Claim Candidate

Strong version:

> For bounded Lean hammer proof search, the first failure changes the value ordering of premise-set interventions. A failure-conditioned action policy can exploit this information to improve kernel-verified proof success over every failure-agnostic static action portfolio under matched compute.

Weaker fallback:

> Human proof-core coverage and static premise recall are imperfect proxies for bounded verified proof success; failure-conditioned premise actions expose and partially correct this mismatch.

## 2. Immediate Gates

### Gate 0: Does failure content matter in the existing pipeline?

Purpose:

- Test whether the current second-stage gain is truly due to failure information, not merely a second learned stage or retry-conditioned reranking.

Required variants:

- `true`: original failure information.
- `generic`: only know that first attempt failed.
- `masked`: remove failure-type/text fields while preserving goal/history features.
- `shuffled`: random failure information from other failed goals.
- `matched-shuffled`: shuffle within matched coarse category or similar first-attempt profile.

Stop rules:

- If true feedback does not beat matched-shuffled feedback, stop claiming "failure feedback as conditional evidence".
- If masked/shuffled matches true, reframe as adaptive second-stage reranking, not failure semantics.

Status update:

- Completed on 2026-06-21 with `outputs/phase3_feedback_causality_gate0.md`.
- Result: true failure-conditioned policy reaches 92.5% trace-core success over 4x500 goals, beating the best control (`learned_base_fallback`, 86.4%) by +6.2 pp.
- Readout: Gate 0 passes for the trace-core proxy. This supports failure content as conditional evidence, but the same causal test still needs to be repeated on verified LeanHammer/prover outcomes.

### Gate 1: Can premise interventions be causal in LeanHammer?

Purpose:

- Verify that an explicit premise list can be injected into a real Lean hammer/prover loop and that the selected premises actually affect the query and kernel-verified outcome.

Required smoke:

- Use a custom selector or wrapper.
- Log actual premises reaching the backend.
- Log terminal status: proved, timeout, reconstruction failure, type/translation failure, unknown.
- Confirm that changing premise actions changes outcomes on at least a small smoke set.

Stop rules:

- If selected premise sets cannot causally affect the backend/replay process, current bridge evidence must stay a proxy and the oral route is blocked.

Status update:

- Completed minimal LeanHammer smoke on 2026-06-21.
- Result: Gate 1 passes on synthetic LeanHammer goals. Complete explicit premise lists prove; missing/wrong premise lists fail; noisy complete lists still prove.
- Mathlib-context extension completed on 2026-06-21 with `outputs/gate1_mathlib_hammer_smoke.md`.
- Result: 8 Mathlib-context goals / 32 variants, 0 expectation misses; selector premise traces are empty, so the explicit premise list is the controlled variable.
- Important boundary: this proves the intervention mechanism in `import Mathlib` contexts, but not yet on a traced-corpus theorem replay benchmark.

### Gate 2: Is there oracle adaptive headroom?

Purpose:

- Run a pre-registered action grid on first-failure goals and compare per-goal oracle adaptive action against best static equal-compute schedule.

Minimum action grid:

- keep
- shrink_050
- shrink_075
- expand_150
- expand_200
- base_rescue_8
- selector/interleave variants if available
- stop

Stop rules:

- Oracle adaptive gap >= 5 pp: strong oral route.
- 3-5 pp: viable main-track route; oral needs strong learned gate and transfer.
- < 3 pp after one predeclared revision: stop verified adaptive action route.

Status update:

- Completed synthetic verified action-grid pilot on 2026-06-21.
- 500 synthetic LeanHammer goals: oracle adaptive 80.0%, true feedback policy 80.0%, best static 40.0%, shuffled feedback 27.6%.
- Completed generated Mathlib theorem-family verified pilot on 2026-06-21 with `outputs/gate2_mathlib_hammer_action_grid_100.md`.
- 100 Mathlib-context generated theorem-family goals: first failure 100.0%, oracle adaptive 80.0%, true feedback policy 80.0%, best static 40.0%, shuffled feedback 0.0%.
- Readout: Gate 2 machinery passes in a real Mathlib 4.30 + LeanHammer 4.30 environment, but the result is still a generated theorem-family pilot. Traced-corpus verified replay remains required for the final main claim.

### Compatibility Gate: Can Mathlib and LeanHammer run together?

Status update:

- Completed on 2026-06-21 with `outputs/mathlib_leanhammer_compat_probe_v2.md`.
- Route A passes: Mathlib tag `v4.30.0` / commit `c5ea00351c28e24afc9f0f84379aa41082b1188f` imports together with LeanHammer commit `3ef50193c9e80f84930f8f400bfd3c097c5e1fd3` in one Lean 4.30 process.
- Boundary: existing traced datasets were produced from current Mathlib 4.31, so the remaining issue is corpus/replay migration, not basic toolchain compatibility.

### Trace-Corpus Migration Gate

Status update:

- Completed name-level preflight on 2026-06-21 with `outputs/mathlib430_trace_corpus_preflight_500.md`.
- Existing 500-goal heldout trace corpus is mostly Mathlib 4.30-compatible by declaration names: theorem exists 98.8%, all proof-core names exist 99.6%, file exists 99.4%.
- Raw candidate lists contain the target theorem itself for 500/500 goals, so direct `import Mathlib` replay would have circular target-theorem leakage.
- Cleaned subset completed with `outputs/mathlib430_clean_trace_subset_500.md`: 490/500 goals retained after dropping missing 4.30 items and removing target theorem candidates.
- Standalone elaboration probe completed with `outputs/mathlib430_standalone_elab_50.md`: only 4/50 cleaned goals elaborate after naive standalone statement rewriting with `sorry`.
- Original-file/pre-theorem patch probe completed with `outputs/mathlib430_pretheorem_patch_probe_3_v3.md`: temporary patched files now run to Hammer/proof search; 3 sample goals have 0 proved, with 2 `search_fail` and 1 `type_mismatch`.
- Original-tactic replay probe completed with `outputs/mathlib430_pretheorem_original_tactic_probe_10.md`: 3/10 cleaned goals replay in Mathlib 4.30 original-file/pre-theorem context.
- Replayable-subset Hammer matrix completed with `outputs/mathlib430_pretheorem_hammer_matrix_replayable3.md`: 8/90 verified Hammer attempts, but all positives are on one empty-premise-solvable goal.
- Scaled original-tactic replay completed with `outputs/mathlib430_pretheorem_original_tactic_probe_50.md`: 25/50 cleaned goals replay.
- Proof-action routing matrix completed with `outputs/mathlib430_pretheorem_action_matrix_replayable25.md`: 25 replayable goals, 275 attempts, 22 verified attempts, 17 non-empty-premise verified attempts, and 3 strict action-dependent goals.
- Larger original-tactic replay completed with `outputs/mathlib430_pretheorem_original_tactic_probe_100.md`: 48/100 cleaned goals replay.
- 48-goal proof-action matrix completed with `outputs/mathlib430_pretheorem_action_matrix_replayable48.md`: oracle 8/48 vs best static 5/48, 30 verified attempts, 21 non-empty-premise verified attempts, and 3 strict action-dependent goals.
- Naive rewrite/simp-only extension completed with `outputs/mathlib430_pretheorem_action_matrix_rewrite48.md`: 0/288 verified, so this branch should stop.
- Targeted typed action extension completed with `outputs/mathlib430_pretheorem_action_matrix_targeted48.md`: `simp_all` / `simp_rw` / `solve_by_elim` families add 8 verified attempts and 2 new strict positives (`rTensor.inverse_comp_rTensor`, `SkewMonoidAlgebra.sum_mul`).
- Combined 48-goal proof-action readout: oracle 10/48 vs best static 5/48, 5 strict action-dependent goals.
- Scaled original-tactic replay completed with `outputs/mathlib430_pretheorem_original_tactic_probe_300.md`: 143/300 cleaned trace goals replay in Mathlib 4.30 pre-theorem context.
- Scaled 230-goal proof-action matrix completed with `outputs/mathlib430_pretheorem_action_matrix_scaled230_merged.md`: oracle 51/230 vs best static 31/230, 246 verified attempts, 205 non-empty-premise verified attempts, and 22 strict action-dependent goals.
- Routing-policy gate completed with `outputs/mathlib430_action_routing_policy_gate_scaled230.md`: coarse failure-status routing and text NB show weak OOF gains but do not beat fixed second action on heldout test; a fixed two-action typed portfolio after `hammer_empty` reaches 48/230, close to oracle 51/230.
- Budgeted low-compute policy gate completed with `outputs/mathlib430_budgeted_action_policy_scaled230.md`: OOF fixed greedy K=2 reaches 48/230; residual adaptive K=2 reaches 45/230 (NB) / 46/230 (kNN); residual NB K=3 reaches 50/230 but does not cleanly beat the typed-portfolio story because fixed K=4 also reaches 50/230.
- Extended action-family run completed with `outputs/mathlib430_pretheorem_action_matrix_scaled230_extended_merged.md`: oracle improves to 58/230, best static becomes `aesop_core_plus_learned` at 38/230, and strict action-dependent goals increase to 29.
- Extended budgeted policy completed with `outputs/mathlib430_budgeted_action_policy_scaled230_extended.md`: fixed greedy K=2 reaches 55/230 OOF, K=4 reaches 57/230 OOF, and train-fitted K=4 reaches the 58/230 oracle; residual adaptive policies still do not clearly beat fixed typed portfolios.
- Focused Aesop ablation completed with `analysis/mathlib430_aesop_ablation_scaled230.md` and `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.md`: the oracle stays 58/230, but facts+simps solves 38/230 while facts-only solves 5/230 and simps-only solves 4/230; `core+learned32` drops to 7/230 group coverage. This supports a mechanism claim about typed exposure and an anti-blind-expansion claim.
- Full Aesop-ablation budgeted policy completed with `outputs/mathlib430_budgeted_action_policy_scaled230_aesop_ablation.md`: fixed greedy K=2 reaches 55/230 OOF, K=4 reaches 57/230 OOF, and train-fitted K=4 reaches the 58/230 oracle; residual NB/kNN still do not beat the fixed typed portfolio.
- Boundary: this is now strong evidence for a compute-budgeted typed proof-action portfolio, especially `aesop` + `hammerCore` + enlarged Hammer + `solve_by_elim`. It is not yet a full adaptive-policy claim.

## 3. What Not To Do

- Do not run more hand-written guardrail / expert-mix heuristics on trace-core results.
- Do not launch larger bridge replay by default.
- Do not present `leansearch_iterative` or similar lexical expansion proxies as LeanSearch v2.
- Do not treat final-base8 as a central method.
- Do not rewrite the paper around trace-core success as if it were end-to-end theorem proving.
- Do not present generated Mathlib theorem-family Gate 2 as the final paper main result.

## 4. Phase 0 Files To Create Or Maintain

- `outputs/claim_ledger.md`
- `configs/leanhammer_env.yaml`
- `configs/action_grid_v1.yaml`
- `configs/eval_primary.yaml`
- `analysis/oral_upgrade_execution_plan.md`
- `NEXT_STEPS.md`

## 5. Phase 1 Implementation Targets

Scripts proposed by GPT Pro:

- `experiments/current_pipeline/run_feedback_ablation.py`
- `analysis/paired_significance.py`
- `experiments/leanhammer/run_smoke.py`
- `experiments/leanhammer/parse_hammer_traces.py`

Lean integration targets if LeanHammer is installed/available:

- `lean/AdaptivePremise/CustomSelector.lean`
- `lean/AdaptivePremise/TraceHarness.lean`

## 6. Main Paper Rewrite Direction After Gates

Gate 1 and traced-corpus verified-headroom evidence are now sufficient to start rewriting, but the main claim must be updated from "adaptive policy beats static portfolio" to the supported typed-portfolio claim. New paper structure should become:

1. Coverage / retrieval recall can lie under bounded proof search.
2. The same evidence has different value depending on how it is exposed to Lean: facts, simp lemmas, HammerCore inputs, or `solve_by_elim`.
3. A compute-budgeted typed proof-action portfolio recovers nearly all observed traced-corpus verified oracle headroom on the current replayable subset.
4. Aesop ablations provide the counterintuitive mechanism result: facts+simps exposure succeeds, facts-only/simps-only collapse, and broader 32-name exposure hurts.
5. Failure-conditioned adaptive routing remains the oral-upgrade target, but current verified results must present it as unresolved.
6. Trace-core experiments become discovery, motivation, and continuity evidence rather than the main proof of the claim.

## 7. Current Status

Current status as of 2026-06-22:

- GPT Pro report read.
- Pivot accepted in principle.
- Phase 0 protocol files created and dangerous baseline wording partially corrected.
- Gate 0 feedback-causality ablation completed and passed in the trace-core proxy.
- Gate 1 LeanHammer explicit-premise smoke completed and passed on synthetic goals.
- Gate 2 verified action-grid/oracle-headroom pilot completed and passed on synthetic goals.
- Mathlib 4.30 + LeanHammer 4.30 route-A compatibility completed and passed.
- Mathlib-context Gate 1 completed and passed on controlled theorem/context goals.
- Mathlib-context generated theorem-family Gate 2 completed and passed on 100 goals.
- Name-level preflight and target-candidate cleaning completed for the existing 500-goal heldout trace corpus; 490 clean goals remain.
- Traced-corpus typed proof-action evidence is now complete through the Aesop-ablation matrix: oracle 58/230, best static 38/230, strict action-dependent goals 29, fixed typed K=4 OOF 57/230.
- Current blocker for the original GPT Pro oral target: adaptive routing still does not cleanly beat typed fixed portfolios under matched compute.
- Next real task: rewrite the main paper around the expanded typed proof-action portfolio with `aesop` as the key interface, and keep adaptive routing as a future/upgrade experiment unless a materially stronger policy feature set is introduced.
