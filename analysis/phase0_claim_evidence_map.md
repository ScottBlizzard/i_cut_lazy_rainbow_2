# Phase 0 Claim-Evidence Map

> 日期：2026-06-17  
> 范围：FAR-Hammer 论文初始 claim 审计。当前尚无实验结果，本文件记录每个 claim 需要什么证据。

## Abstract / Introduction Claims

| Claim | Required evidence | Status |
|---|---|---|
| One-shot premise selection is insufficient | LeanHammer/LeanSearch baseline + first-failure subset | pending |
| More premises can hurt | premise budget curve + timeout/reconstruction metrics | pending |
| Failure trace provides counterfactual supervision | failure ablation: history-only/type/message/structured | pending |
| FAR improves verified success under fixed budget | main fixed-budget experiment | pending |
| FAR improves first-failure recovery | E2 first-failure recovery table | pending |
| FAR selects premise sets closer to proof core | remove-one/proof-core attribution | pending |
| Gains are strongest in local/unseen contexts | miniCTX/local project subset | pending |
| Reconstruction is a separate axis | ATP success vs Lean reconstruction audit | pending |

## Reviewer Questions

| Question | Planned answer | Status |
|---|---|---|
| Is this just retry? | random retry/top-k expansion under same budget | pending |
| Is this just LeanSearch v2? | LeanSearch standard/reasoning baseline | pending |
| Is this proof repair? | no proof text repair; premise set/search-space optimization | conceptual |
| Is failure trace really needed? | no-failure/history-only/failure-type/full ablation | pending |
| Are baselines fair? | fixed calls/wall-clock/premise budget audit | pending |
| Does retrieval recall translate to proof success? | P/S/V evidence hierarchy | pending |

## 2026-06-20 Claim-Evidence Update

| Claim | Evidence | Status |
|---|---|---|
| One-shot premise selection is insufficient | 500 Mathlib trace-core goals: `one_shot` success 58.0% | supported for trace-core |
| Blind top-k expansion helps but is not optimal | `topk_expansion` success 91.6%, FFR 80.0%, avg premises 46.2 | supported for trace-core |
| Static visible-feature reranking is not enough | `visible_feature_rerank` success 88.4%, lower than `rule_far_no_core_tags` 97.0% | supported for trace-core |
| Failure-conditioned visible features improve recovery | `rule_far_no_core_tags` success 97.0%, FFR 92.9%, avg premises 44.4 | supported for trace-core |
| Oracle trace tags define remaining upper bound | `rule_far_full` success 98.8%, only +1.8 over no-core | supported for trace-core |
| FAR improves verified Lean success | No full Lean reconstruction result yet | needs evidence |
| FAR improves timeout behavior | Corrected feature-aware table has 0.0% timeout rate | needs separate timeout stress evidence |

## 2026-06-20 2k Evidence Update

| Claim | 2k Evidence | Status |
|---|---|---|
| Failure-conditioned visible features improve trace-core recovery | `rule_far_no_core_tags` 95.7% success vs `topk_expansion` 91.5% | supported for trace-core |
| Dynamic failure conditioning beats static visible reranking | `rule_far_no_core_tags` 95.7% vs `visible_feature_rerank` 86.5% | supported for trace-core |
| The effect is not a 500-goal sample accident | 500 result 97.0%, 2k result 95.7% | supported for trace-core |
| Oracle candidate labels still leave headroom | `rule_far_full` 98.3% vs no-core 95.7% | supported for trace-core |
| Verified proof improvement | No real reconstruction result yet | needs evidence |

## 2026-06-20 Reconstruction Bridge Evidence

| Claim | Bridge Evidence | Status |
|---|---|---|
| Trace-core gains survive a real Lean replay filter | On 100 disagreement-heavy bridge goals, `rule_far_no_core_tags` bridge verified success is 72.0% vs `topk_expansion` 43.0% | supported as bridge evidence |
| Static visible reranking is insufficient | `visible_feature_rerank` bridge verified success is 33.0% vs no-core FAR 72.0% | supported as bridge evidence |
| Oracle upper bound still exists | `rule_far_full` bridge verified success is 79.0% vs no-core FAR 72.0% | supported as bridge evidence |
| Original traced proofs replay in real Lean often enough for bridge use | 86/100 selected goals replay through `lake env lean` | supported |
| Full verified proving benchmark improvement | Current bridge is disagreement-heavy and replay-based, not a full random verified proving benchmark | still needs Phase 2 evidence |

## 2026-06-20 Feature-Group Evidence

| Claim | Evidence | Status |
|---|---|---|
| Static visible features are not sufficient | Static all-feature rerank is 86.5%, below `topk_expansion` 91.5% and FAR all-feature 95.7% | supported for trace-core |
| Name/namespace morphology is the strongest visible feature | FAR name-only reaches 95.0%, close to all-feature FAR 95.7% | supported for trace-core |
| Statement and declaration features are weak alone but useful when conditioned on failure | Static statement/decl are 77.6%/78.3%; FAR statement/decl are 92.8%/92.6% | supported for trace-core |
| Failure-conditioned feature use is necessary | FAR all-feature 95.7% vs static all-feature 86.5% | supported for trace-core |

## 2026-06-20 Timeout Stress Evidence

| Claim | Evidence | Status |
|---|---|---|
| More premises can be non-monotonic under timeout pressure | Static top-k/equal-budget drops to 43.8% with 56.2% timeout, below one-shot 57.0% | supported in stress setting |
| Blind top-k expansion is weak under timeout stress | `topk_expansion` 59.7% success, 46.1% timeout | supported in stress setting |
| Timeout-conditioned shrink helps | `rule_far_no_core_timeout_shrink` 69.3% success, 28.6% FFR, 23.5% timeout | supported in stress setting |
| Default expand-style no-core FAR has a timeout boundary | `rule_far_no_core_tags` matches top-k at 59.7% under timeout stress | supported as boundary condition |

## 2026-06-20 Global Imported-Core Evidence

| Claim | Evidence | Status |
|---|---|---|
| Same-file candidate assumptions do not cover global Mathlib retrieval | Imported-core dataset has avg 4.26 imported proof-core premises and avg 188.6 imported candidates per goal | supported as stress dataset |
| Same-file prior is a brittle shortcut | `same_file_prior_rerank` is only 2.1% success on imported-core goals | supported in imported-core stress |
| Lexical/global retrieval is stronger but insufficient | `bm25_expansion` and `leansearch_iterative` reach 11.9%, while `bm25_rerank` is 7.0% | supported in imported-core stress |
| Current visible-feature no-core FAR does not transfer to imported-core retrieval | `rule_far_no_core_tags` is 4.7%, below BM25 expansion | supported as limitation |
| Imported-core goals are recoverable with better candidate-side signal | `rule_far_full` reaches 55.7%, far above BM25/FAR-no-core | supported as oracle upper-bound/headroom |
| Learned/global retriever is required for main global claim | Gap between `rule_far_full` 55.7% and `rule_far_bm25` 12.2% in the initial stress test | resolved by Phase 3B/3D |

## 2026-06-20 Learned Global Retriever Evidence

| Claim | Evidence | Status |
|---|---|---|
| Imported-core failure was a retriever bottleneck, not a hard idea ceiling | Heldout 500: `learned_expansion` 84.0% vs `bm25_expansion` 12.8% | strongly supported for trace-core |
| Supervised proof-core labels produce a much stronger global retriever | Learned all-core@96 is 84.0% vs base all-core@96 2.6% | strongly supported |
| Static learned retrieval is already a strong baseline | `learned_rerank` 64.2% success at 56 premises | supported |
| Dynamic learned expansion adds substantial recovery | `learned_expansion` 84.0% vs `learned_rerank` 64.2% | supported |
| Current learned FAR wrapper is not yet much better than learned expansion | `rule_far_learned` 84.4% vs `learned_expansion` 84.0% | limitation / next controller target |
| Old trace-tag full controller is not an absolute upper bound in imported-core Phase 3B | `learned_expansion` 84.0% and `rule_far_learned` 84.4% exceed `rule_far_full` 55.6% | update wording |

## 2026-06-20 Learned Controller Ablation Evidence

| Claim | Evidence | Status |
|---|---|---|
| Learned+base fallback is the strongest failure-agnostic imported-core baseline | `learned_base_fallback` reaches 87.0% success and 73.8% FFR | supported |
| Pure learned expansion is not the final strong baseline | `learned_base_fallback` 87.0% vs `learned_expansion` 84.0% | supported |
| Current hand-written failure-specific learned controller is not enough | `rule_far_learned_failure_specific` matches fallback at 87.0% but does not exceed it | limitation |
| A learned second-stage controller is needed to test the controller claim | Strongest non-FAR fallback matched the hand-written failure-specific controller | resolved by Phase 3D below |

## 2026-06-21 Learned Second-Stage Controller Evidence

| Claim | Evidence | Status |
|---|---|---|
| Failure-conditioned learned control beats the strongest imported-core fallback | `rule_far_learned_second_stage` reaches 92.4% success vs `learned_base_fallback` 87.0% | strongly supported for heldout trace-core |
| The gain is not only from using more premises | `rule_far_learned_second_stage` uses 53.9 avg premises vs 57.6 for `learned_base_fallback` | supported |
| Failure-aware recovery improves substantially over fallback | FFR is 84.7% for `rule_far_learned_second_stage` vs 73.8% for `learned_base_fallback` | strongly supported |
| Learned second-stage scoring is better than hand-written failure-specific scheduling | `rule_far_learned_second_stage` 92.4% vs `rule_far_learned_failure_specific` 87.0% | supported |
| The imported-core story now has a positive controller contribution | Best controller improves +8.4 over `learned_expansion` and +5.4 over `learned_base_fallback` | supported, needs split stability |
| The current result is still trace-core recovery rather than full proof reconstruction | Evaluation uses traced proof-core membership on heldout imported-core goals | limitation / bridge required |

## 2026-06-21 Split-Stability Fold0 Evidence

| Claim | Evidence | Status |
|---|---|---|
| The second-stage gain is not a one-split artifact | Fold0 `rule_far_learned_second_stage` reaches 91.6% vs 92.4% on the original heldout split | supported by one alternate fold |
| The controller remains strong when retrieval is harder | Fold0 `learned_expansion` drops to 79.0%, but second-stage remains 91.6% | strongly supported for fold0 |
| Failure-conditioned control beats fallback more clearly on fold0 | Fold0 second-stage 91.6% vs `learned_base_fallback` 83.6% | supported |
| The gain is premise-efficient on fold0 | Fold0 second-stage uses 54.3 avg premises vs fallback 57.7 | supported |
| More fold coverage would help final variance reporting | Only one alternate fold has been run so far | optional additional evidence |

Paper-safe current wording:

> In imported-core Mathlib trace-core recovery, a learned second-stage controller conditioned on the first failed attempt improves over the strongest learned+base fallback on the original heldout split (92.4% vs 87.0%) and on an alternate heldout fold (91.6% vs 83.6%), while using fewer average premises in both cases. This supports the central claim that failure feedback is useful beyond static learned retrieval and failure-agnostic fallback, while still requiring Lean replay validation before making full proof-reconstruction claims.

Unsupported wording to avoid:

- "FAR improves full random verified Lean proof success" until a random verified benchmark is run.
- "FAR fixes timeouts" until a timeout-specific subset or real backend shows it.
- "Failure type alone is enough" because the current best gain comes from failure type plus visible candidate features.
- "Current no-core FAR solves global imported retrieval" because Phase 3 shows it does not yet.
- "Failure-aware control is fully solved" because Phase 3D/3E still need real Lean replay checks and broader benchmark coverage.
- "The second-stage controller is independent of trace-core supervision" because both retriever and controller currently use traced proof-core labels for training.
- "The result directly proves full proof reconstruction success" because Phase 3D is still a trace-core recovery benchmark.
