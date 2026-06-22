# Claim Ledger

更新时间：2026-06-22

用途：记录当前哪些 claim 已被支持、哪些只能作为 proxy evidence、哪些在 oral pivot 前禁止使用。

## Supported Current Claims

| Claim | Evidence | Allowed Use |
|---|---|---|
| Failure-conditioned visible features improve local Mathlib trace-core recovery over static rerank and blind expansion. | Phase 1 2k: `rule_far_no_core_tags` 95.7% vs `topk_expansion` 91.5% and `visible_feature_rerank` 86.5%. | Discovery evidence / appendix / motivation. |
| More premises can hurt under timeout pressure. | Phase 2 timeout: `topk_equal_budget` 43.8% vs `one_shot` 57.0%; timeout shrink 69.3%. | Strong motivating insight; needs real LeanHammer replication for oral main claim. |
| Imported-core local/lexical retrieval is insufficient in our controlled protocol. | Phase 3A: BM25 / controlled iterative lexical policies around 12%. | Diagnostic evidence; must not call this full LeanSearch v2 comparison. |
| Learned second-stage controller improves trace-core recovery over learned+base fallback. | Phase 3D: 92.4% vs 87.0%; Gate 0 four-split aggregate 92.5% vs `learned_base_fallback` 86.4%. | Discovery evidence; not end-to-end proof claim. |
| Failure transcript content causally matters in the current trace-core proxy. | Gate 0 four-split ablation: true failure-conditioned policy 92.5% vs best control 86.4%; fixed/cyclic/shuffled failure-type controls 79.4-85.0%. | Strong proxy evidence for pivot; must be re-tested with verified backend before main claim. |
| Explicit premise interventions can causally change a LeanHammer verified outcome. | Gate 1 LeanHammer smoke: complete premise lists prove two synthetic goals; missing/wrong premise lists fail; recheck passed after environment rebuild. | Infrastructure claim only; justifies verified action-grid experiments. |
| Verified action-grid/oracle-headroom machinery works on synthetic LeanHammer goals. | Gate 2 500 synthetic goals: oracle/true-feedback 80.0%, best static 40.0%, shuffled 27.6%. | Pipeline validation only; not Mathlib paper evidence. |
| Mathlib 4.30 and LeanHammer 4.30 can run in one verified evaluation stack. | `outputs/mathlib_leanhammer_compat_probe_v2.md`: combined `import Mathlib` and `import Hammer` passes in Lean 4.30. | Environment/infrastructure claim; route-A is usable. |
| Explicit premise interventions causally change Mathlib-context LeanHammer outcomes. | `outputs/gate1_mathlib_hammer_smoke.md`: 8 Mathlib-context goals / 32 variants, 0 expectation misses, selector premises `[]`. | Verified smoke claim; stronger than synthetic Gate 1. |
| Generated Mathlib theorem-family action-grid has verified adaptive headroom. | `outputs/gate2_mathlib_hammer_action_grid_100.md`: oracle/true feedback 80.0%, best static 40.0%, first failure 100.0%. | Mechanism evidence only; not final traced-corpus paper evidence. |
| Existing heldout trace corpus is mostly name-compatible with Mathlib 4.30 after cleaning. | `outputs/mathlib430_trace_corpus_preflight_500.md`: theorem exists 98.8%, proof-core complete 99.6%; `outputs/mathlib430_clean_trace_subset_500.md`: 490/500 retained after removing target candidates. | Data-migration evidence only; standalone/pre-theorem replay still required. |
| Naive standalone rewriting is not a viable traced-corpus replay route. | `outputs/mathlib430_standalone_elab_50.md`: only 4/50 cleaned goals elaborate after standalone statement rewriting with `sorry`. | Negative engineering evidence; motivates original-file/pre-theorem replay. |
| Original-file/pre-theorem patch replay harness is technically reachable. | `outputs/mathlib430_pretheorem_patch_probe_3_v3.md`: temporary patched original files run to Hammer/proof-search layer; failures are search/type issues, not import/span failures. | Harness evidence only; no traced-corpus proof success yet. |
| Existing trace goals have a nonempty Mathlib 4.30 replayable subset. | `outputs/mathlib430_pretheorem_original_tactic_probe_300.md`: original traced tactics replay for 143/300 cleaned goals. | Supported as migration/filtering evidence; proof-action success still needs scaled matrix evidence. |
| Current traced-corpus Hammer replay has only weak positives. | `outputs/mathlib430_pretheorem_hammer_matrix_replayable3.md`: 8 verified attempts, but all on one empty-premise-solvable goal. | Engineering signal only; not main-claim evidence. |
| Proof-action routing has scaled verified action-dependent wins on replayable traced-corpus goals. | `outputs/mathlib430_pretheorem_action_matrix_scaled230_merged.md`: oracle 51/230 vs best static 31/230; 22 strict action-dependent goals; 246 verified attempts. | Positive scaled verified pilot; still needs stronger learned/rule policy evidence before adaptive main claim. |
| Extended typed proof-action exposure improves replayable traced-corpus verified success. | `outputs/mathlib430_pretheorem_action_matrix_scaled230_extended_merged.md`: oracle 58/230 vs best static 38/230; 29 strict action-dependent goals; 506 verified attempts; `aesop_core_plus_learned` is best static at 38/230. | Strongest current verified evidence; supports typed proof-action portfolio mainline. |
| `aesop` is an important additional Lean interface for selected evidence. | Extended and Aesop-ablation matrices: `aesop_core_plus_learned` solves 38/230, accounts for 6 of 7 new oracle goals over the previous scaled230 matrix, covers 20/29 strict goals, and has 6 only-family strict cases. | Supported; use as a central mechanism insight. |
| Aesop gains depend on typed exposure, not simply more selected names. | `analysis/mathlib430_aesop_ablation_scaled230.md`: facts+simps solves 38/230, facts-only 5/230, simps-only 4/230; `core+learned32` group coverage falls to 7/230 while `core+learned8/16` reaches 41/230 group coverage. | Supported as mechanism evidence; use for the anti-blind-expansion argument. |
| A low-capacity failure-status adaptive policy already beats fixed retry actions. | `outputs/mathlib430_action_routing_policy_gate_scaled230.md`: coarse status rule and text NB show weak OOF movement but do not beat fixed second action on heldout test. | Unsupported as a strong claim; do not claim yet. |
| Richer offline routing already beats a typed fixed portfolio under matched compute. | Full Aesop-ablation budgeted policy: OOF fixed greedy K=2 reaches 55/230; residual NB/KNN K=2 reach 50/230 and 54/230. K=3 ties fixed at 55/230, and K=4/K=6 remains 57/230 vs oracle 58/230. | Unsupported as a main claim; evidence favors portfolio strength over low-budget learned routing. |
| A typed fixed action portfolio is a strong verified control. | Full Aesop-ablation budgeted policy: after `hammer_empty`, fixed greedy K=2 reaches 55/230 OOF and K=4 reaches 57/230 OOF; train-fitted K=4 reaches the 58/230 oracle. | Supported as a control and likely main method story. |
| Naive rewrite/simp-only template expansion is useful. | `outputs/mathlib430_pretheorem_action_matrix_rewrite48.md`: 0/288 verified. | Unsupported; avoid further blind scaling. |
| Phase 3 gains survive replay-filtered bridge subset. | 200-goal bridge: final-base8 53.5% vs fallback 44.5%; 100-goal bridge: second-stage 47.0% vs fallback 31.0%. | Bridge validation only; not full theorem proving. |
| Broad hand-written expert/guardrail mixing is not promising. | Multiple negative ablations; expert/mix/hard guardrails hurt or fail to improve meaningfully. | Justifies stopping heuristic tuning. |

## Claims Requiring New Evidence

| Claim | Required Evidence |
|---|---|
| Failure-conditioned premise actions improve traced-corpus kernel-verified proof success. | A non-generated Mathlib traced-corpus learned/adaptive policy that beats the fixed typed portfolio under matched compute. |
| Adaptive proof-action routing beats the best static portfolio on real traced-corpus goals. | New evidence is required beyond the full Aesop-ablation budgeted policy, because fixed typed portfolios remain stronger at K=1/K=2 and tie or match at higher budgets. |
| Low-budget adaptive routing can match a larger typed portfolio. | New evidence is required beyond `mathlib430_budgeted_action_policy_scaled230_aesop_ablation.md`, because current K=1/K=2 adaptive policies do not beat fixed typed portfolios. |
| Existing 4.31 trace goals can be safely replayed as 4.30 LeanHammer goals at paper scale. | Larger replayable subset plus action-dependent LeanHammer/proof-action successes. |
| More premises hurt in real LeanHammer search, not only stress proxy. | Real backend search/timeout/reconstruction stats under matched premise actions. |
| Failure transcript content causally matters for verified proof outcomes. | True vs masked/shuffled/fixed failure transcript controls on verified retry outcomes. |
| Current method is competitive with strongest premise systems. | Official LeanHammer / LeanSearch v2 compatible comparison or carefully scoped claim. |

## Prohibited Or Risky Wording

- Do not say current paper solves full theorem proving.
- Do not say bridge verified is end-to-end proof generation.
- Do not call `leansearch_iterative` a LeanSearch v2 baseline.
- Do not imply `learned_base_fallback` is the strongest global premise-selection baseline; it is the strongest in-protocol failure-agnostic baseline.
- Do not present final-base8 as a main method.
- Do not claim rich failure feedback is necessary for kernel-verified proof success until verified masked/shuffled/fixed controls support it.
- Do not use trace-core success as a substitute for proved / kernel-verified success.
- Do not use synthetic LeanHammer Gate 2 as paper main evidence.
- Do not use generated Mathlib theorem-family Gate 2 as final paper main evidence.
- Do not imply current Mathlib 4.31 trace data has already been replayed in LeanHammer; only the Mathlib 4.30 route-A stack is verified.
- Do not use the cleaned trace subset alone as verified evidence; use only replayable-subset proof-action results with kernel-verified outcomes and explicit boundaries.

## New Target Claim

Target oral-level claim, pending evidence:

> After a fixed failed Lean hammer attempt, the failure transcript changes the value ordering of premise-set interventions; a verified action policy can exploit this conditional information to improve kernel-verified proof success over the best equal-compute static portfolio.

Updated target wording after the replayable-subset pilot:

> On replayable Mathlib theorem contexts, the valuable intervention is not merely which premises to add, but how to expose selected names to Lean's reconstruction machinery. Small typed portfolios over Aesop, HammerCore, Hammer, and `solve_by_elim` recover almost all current oracle headroom, and Aesop ablations show that facts+simps exposure is qualitatively different from facts-only, simps-only, or broad 32-name insertion.
