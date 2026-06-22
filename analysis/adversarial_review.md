# Adversarial Review

> 日期：2026-06-17  
> 模式：严格 ICLR reviewer 预审。当前是项目启动版，主要记录预期攻击点。

## Executive Judgment

当前 idea 有潜力，但必须避免三个风险：

1. 被看成 LeanSearch/LeanHammer 的小增量。
2. 被看成 proof repair / LLM agent feedback 的重复。
3. 实验只证明多试几次有效，而不是 failure-conditioned signal 有效。

## Five-Dimension Review

### 1. Contribution

| Question | Risk | Required fix |
|---|---|---|
| 新知识是什么？ | 只是 adaptive retrieval | 写成 closed-loop premise optimization + P/S/V hierarchy |
| 反直觉在哪里？ | failure helps 太普通 | 强调 more premises can hurt |
| 和 LeanHammer 区别？ | LeanHammer 已很强 | post-failure premise distribution update |
| 和 LeanSearch v2 区别？ | 都是 iterative retrieval | LeanSearch 是 sketch-reflect；我们是 prover-failure-conditioned |

### 2. Soundness

| Risk | Required evidence |
|---|---|
| baseline budget 不公平 | fixed wall-clock/calls/premise budget |
| failure parser 错 | parser accuracy audit |
| Lean environment 漂移 | commit/protocol logging |
| proof-core labels 不可靠 | remove-one/minimal set audit |

### 3. Experimental Strength

必须有：

- LeanHammer/LeanSearch/ReProver baselines。
- first-failure recovery。
- budget curves。
- failure ablations。
- local/miniCTX。
- reconstruction subset。

### 4. Evaluation Completeness

Reviewer 会问：

- 是不是只在 Mathlib toy subset？
- 是不是只对 timeout 有效？
- 是不是 LeanSearch candidate pool 足够就能解决？
- 是不是加大 top-k 就一样？

### 5. Method Design

最需要证明：

> failure trace changes the next premise distribution in a useful, interpretable, and budget-efficient way.

## Current Verdict Simulation

## 2026-06-20 Updated Adversarial Review

New positive evidence:

- The corrected 500-goal feature-aware Mathlib trace-core table is strong:
  - `rule_far_no_core_tags`: 97.0% success, 92.9% FFR, 44.4 avg premises.
  - `topk_expansion`: 91.6% success, 80.0% FFR, 46.2 avg premises.
  - `visible_feature_rerank`: 88.4% success, 0.0% FFR, 43.5 avg premises.
- This gives a clean answer to "is this just static reranking?": no, static visible-feature reranking is materially weaker than failure-conditioned visible-feature reranking.
- It also gives a cleaner answer to "is this just more premises?": no, the best less-oracle FAR variant uses fewer average premises than blind top-k expansion.

New risks:

- The current table is still trace-core recovery, not verified Lean reconstruction.
- The trace-core failure type is synthesized from proof-core metadata, so a reviewer can still ask whether real Lean failure messages provide equally useful supervision.
- The corrected table has no timeout failures, so timeout claims are not supported by this run.
- The candidate pool is same-file; global/imported retrieval and LeanSearch-style candidate pools are not yet tested.

Reviewer-critical fixes before paper submission:

1. Run the 2k trace-core scale-up to show the result is not a 500-goal sample accident.
2. Add feature-group ablations so the method does not look like hand-tuned string overlap.
3. Run a real reconstruction bridge on 50-100 disagreement goals.
4. Add a timeout stress subset or real backend timeout analysis.
5. Compare against stronger retrieval baselines once available: LeanSearch v2, LeanHammer-style premise selection, ReProver retriever.

Current verdict:

- Trace-core idea score improved: the method now has a real less-oracle positive result, not just an oracle upper bound.
- Main remaining rejection risk is external validity: trace-core recovery must be connected to verified Lean proof reconstruction.

## 2026-06-20 2k Scale-Up Review

The 2k scale-up reduces the "small sample" rejection risk.

- `rule_far_no_core_tags`: 95.7% success, 89.7% FFR, 45.1 avg premises.
- `topk_expansion`: 91.5% success, 79.9% FFR, 46.9 avg premises.
- `visible_feature_rerank`: 86.5% success, 0.0% FFR, 42.9 avg premises.
- `rule_far_full`: 98.3% success, 96.0% FFR, 42.9 avg premises.

Updated reviewer stance:

- The trace-core method is no longer the weak part of the project.
- The reviewer will now attack realism: synthetic failure labels, same-file candidates, and lack of verified reconstruction.
- Therefore the next experiment should not be "more trace-core scale"; it should be the real reconstruction bridge and feature-group ablations.

## 2026-06-20 Reconstruction Bridge Review

The real Lean replay bridge removes the largest Phase 1 realism objection.

- 100 disagreement-heavy goals were selected from the 2k trace-core result.
- 86/100 original traced tactic scripts replayed successfully through `lake env lean`.
- On the bridge set, `rule_far_no_core_tags` has 72.0% bridge verified success, compared with 43.0% for `topk_expansion` and 33.0% for static `visible_feature_rerank`.

Remaining reviewer risks after Phase 1:

- The bridge set is intentionally disagreement-heavy, so it should be described as a diagnostic bridge, not as the final benchmark distribution.
- The replay backend uses original traced tactic scripts. It verifies that trace-core recovered premises align with replayable Lean proofs, but it is not yet an autonomous proof search benchmark.
- Candidate pools are still same-file; global retrieval and stronger external baselines remain open.

Updated verdict:

- Phase 1 feasibility is complete.
- The idea is strong enough to move into Phase 2 baselines and full paper-matrix experiments.

## 2026-06-20 Feature-Group Review

The feature-group ablation addresses the "hand-tuned string trick" critique.

- Name/namespace features explain most of the less-oracle gain: FAR name-only is 95.0% vs all-feature FAR 95.7%.
- Static name reranking is only 85.3%, so the key contribution is not just name overlap; it is failure-conditioned reuse of visible features.
- Statement-only and declaration-only static rerankers are weak, but their FAR versions still beat blind expansion. This supports the closed-loop framing: weak candidate features become useful after a failure identifies the next retrieval regime.

Remaining risk:

- The current feature importance may be specific to same-file candidates. A global/imported retriever could shift the relative value of namespace and statement features.

## 2026-06-20 Timeout Stress Review

The timeout stress result gives the paper its strongest counterintuitive mechanism.

- Under timeout pressure, static top-k/equal-budget and static feature rerank drop to 43.8%, below one-shot.
- Blind top-k expansion only reaches 59.7% and has a 46.1% timeout rate.
- `rule_far_no_core_timeout_shrink` reaches 69.3% and cuts timeout rate to 23.5%.

Reviewer framing:

- Present this as a stress/mechanism experiment, not as the default benchmark.
- It supports the claim "more premises are not monotonically better" and justifies why a failure-aware controller needs action-specific updates rather than generic retry.

## 2026-06-20 Global Imported-Core Review

This is the first Phase 3 result that directly attacks the same-file-candidate assumption.

- The generated 2k dataset requires at least one real imported proof-core premise per goal.
- Average imported proof-core premises: 4.26 per goal.
- Average imported candidates: 188.6 per goal.
- Static same-file prior fails: `same_file_prior_rerank` is 2.1%.
- Static visible features fail: `visible_feature_rerank` is 2.4%.
- BM25/LeanSearch-style iterative retrieval is better but still weak: `bm25_expansion` and `leansearch_iterative` are both 11.9%.
- `rule_far_bm25` is 12.2%, only a small gain over BM25 expansion.
- `rule_far_full` is 55.7%, so the task is not impossible; the non-oracle retriever is the bottleneck.

Adversarial reviewer take:

- This result weakens any claim that the current visible-feature FAR already solves global Mathlib premise selection.
- It strengthens the paper if framed honestly: same-file recovery is real, timeout non-monotonicity is real, but global imported retrieval requires a stronger learned retriever.
- A reviewer will ask why `rule_far_full` is much higher. The answer must be that it is an upper bound showing recoverable headroom, not a deployable method.
- The next credible response is not another hand-tuned reranker. It is a learned/global retriever trained on traced proof-core membership, followed by the same failure-aware control loop.

Updated risk:

- Main paper table should not lead with Phase 3 imported-core no-core results yet.
- Phase 3 should currently be presented as an external-validity stress and next-experiment driver unless a learned retriever closes the gap.

Next reviewer-facing fix:

1. Train a lightweight learned retriever on the Phase 3 goal file.
2. Compare `learned_retriever_rerank`, `learned_retriever_expansion`, and `rule_far_learned` against BM25/LeanSearch-style baselines.
3. Report how much of the 55.7% `rule_far_full` upper-bound gap is closed without oracle tags.

## 2026-06-20 Learned Global Retriever Review

The learned retriever result changes the Phase 3 verdict.

- Heldout 500 imported-core goals.
- `bm25_expansion`: 12.8% success.
- `leansearch_iterative`: 12.2% success.
- `learned_rerank`: 64.2% success.
- `learned_expansion`: 84.0% success.
- `rule_far_learned`: 84.4% success.
- `rule_far_full`: 55.6% success.

Positive reviewer-facing interpretation:

- The imported-core setting is not a dead end.
- The Phase 3 failure was a weak global retriever bottleneck, and traced proof-core membership provides strong supervision.
- A simple logistic retriever is already enough to beat BM25/LeanSearch-style baselines by a large margin on heldout goals.
- The result is useful for the paper because it connects FAR to a scalable learned retriever rather than hand-tuned same-file heuristics.

New reviewer attack:

- The core FAR controller gain over learned expansion is currently tiny: 84.4% vs 84.0%.
- A reviewer can say the new result is mostly "learned retriever wins", not "failure-aware control wins".
- `rule_far_full` is no longer a clean upper bound in this setting; it should be described as an oracle-tag hand controller, not as the maximum possible result.

Required response:

- Promote learned retrieval into the method, but do not overclaim the current `rule_far_learned` controller.
- Build a failure-specific learned controller and compare directly against `learned_expansion`.
- The new strongest paper path is:
  1. learned global retriever fixes imported-core retrieval;
  2. failure-aware control gives additional gains under timeout, reconstruction, and failure-specific reranking;
  3. same-file/local and imported-core settings become two complementary regimes rather than one replacing the other.

## 2026-06-20 Learned Controller Ablation Review

The controller ablation raises the benchmark and tightens the claim.

- `learned_expansion`: 84.0%.
- `learned_base_fallback`: 87.0%.
- `rule_far_learned_failure_specific`: 87.0%.
- `rule_far_learned_failure_specific` uses slightly fewer average premises than fallback, but has the same success and FFR.

Reviewer-facing interpretation:

- Positive: the imported-core result improves again, and the method now has an honest strong non-oracle baseline at 87.0%.
- Negative: hand-written failure-specific control is not yet producing an independent success-rate gain over learned+base fallback.
- The next experiment must be a learned second-stage controller trained on failed attempts. Without that, the imported-core story is "learned retriever plus fallback", not "failure-aware control is essential."

Updated reviewer risk:

- Do not claim the Phase 3C controller proves FAR beats all learned baselines.
- Phase 3C should be read as the motivation for the Phase 3D second-stage failure-conditioned ranker, not as the final controller result.

## 2026-06-21 Learned Second-Stage Controller Review

The second-stage controller result materially improves the paper story.

- Heldout 500 imported-core goals.
- `learned_expansion`: 84.0% success, 67.7% FFR, 57.7 avg premises.
- `learned_base_fallback`: 87.0% success, 73.8% FFR, 57.6 avg premises.
- `rule_far_learned_failure_specific`: 87.0% success, 73.8% FFR, 57.0 avg premises.
- `rule_far_learned_second_stage`: 92.4% success, 84.7% FFR, 53.9 avg premises.

Reviewer-facing interpretation:

- Positive: the strongest failure-aware controller now beats the strongest failure-agnostic fallback by +5.4 success points and +10.9 FFR.
- Positive: the gain comes with fewer average premises, so the result is not a trivial budget increase.
- Positive: the controller is learned from failed first attempts, which directly matches the paper's failure-aware premise-selection thesis.
- Remaining limitation: the result is trace-core recovery and uses trace-core labels for retriever/controller training, so it must be framed before full Lean replay as a proof-core recovery result.

Old reviewer attack now weakened:

- The attack "this is only a learned retriever result" is no longer sufficient, because `rule_far_learned_second_stage` beats both `learned_expansion` and `learned_base_fallback`.
- The attack "failure-specific control only matches fallback" applies to Phase 3C, not Phase 3D.

New reviewer attacks:

- Split artifact: the 1500/500 heldout split may be favorable.
- Trace-core artifact: success means proof-core coverage, not guaranteed proof reconstruction.
- Supervision cost: both retriever and second-stage controller rely on traced proof-core labels.
- Generality: current failure-specific models are validated on imported-core Mathlib goals, not yet on a broader theorem-proving benchmark suite.

Required response:

1. Run at least one alternate split and report variance or deltas for the three strongest methods.
2. Build a Phase 3 bridge replay set, especially examples where `rule_far_learned_second_stage` succeeds and `learned_base_fallback` fails.
3. Audit the remaining 7.6% failures by candidate coverage, ranking error, failure-type parse, and timeout/reconstruction artifact.
4. In the paper, state the method as trace-supervised failure-aware premise selection unless the bridge replay converts enough examples to verified Lean success.

## 2026-06-21 Split-Stability Fold0 Review

The first split-stability repeat supports the Phase 3D result.

- Alternate split: fold0 uses the original first 500 imported-core goals as heldout and trains on the remaining 1500.
- The learned retriever is weaker on fold0: `learned_expansion` drops from 84.0% to 79.0%.
- `learned_base_fallback` drops from 87.0% to 83.6%.
- `rule_far_learned_second_stage` stays high: 92.4% on the original heldout split and 91.6% on fold0.
- Fold0 second-stage gain over fallback is +8.0 success points, +16.2 FFR, and -3.4 average premises.

Reviewer-facing interpretation:

- Positive: the main controller effect survives a harder alternate heldout split.
- Positive: the effect is larger when the retriever/fallback baseline is weaker, which supports the idea that failure-aware second-stage ranking is doing real work.
- Positive: the result is not bought by more premises; second-stage uses fewer average premises than fallback on both splits.

Updated reviewer risk:

- Split artifact is now lower risk, though more folds would still help final variance reporting.
- The dominant remaining risk is trace-core validity: reviewers can still ask whether proof-core recovery translates to real Lean proof reconstruction.
- The next high-value experiment is Phase 3 bridge replay, not another hand-tuned controller.

Required response:

1. Build the Phase 3 bridge replay set.
2. Keep fold1/fold2 as optional variance runs for the final paper.
3. Report original heldout and fold0 together in any split-stability paragraph; do not cite only the better 92.4% number.

项目启动前：idea score 6-7，取决于 Phase 1 是否跑出 first-failure recovery 和 more-premises-hurt 曲线。  
强版本目标：7-8，前提是 LeanSearch/LeanHammer 强 baseline 正面打，并且 proof-core/reconstruction 分析完整。
