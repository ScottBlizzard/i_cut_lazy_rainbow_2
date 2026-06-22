# GPT Pro Brief: How to Upgrade ICLR_2 Toward ICLR Oral

更新时间：2026-06-21  
项目目录：`D:\ICLR_2`  
当前论文 PDF：`D:\ICLR_2\iclr2027\paper.pdf`  
当前论文源文件：`D:\ICLR_2\iclr2027\paper.tex`  
当前实验总报告：`D:\ICLR_2\experiment_report.md`

## 0. 任务边界

请把这篇文章当作 **ICLR main track** 论文来审视和升级。不要把它降级成 evaluation paper、benchmark paper、tool paper、dataset paper 或 workshop-style engineering report。

允许的升级方式很宽：

- 保留当前 idea，但重构理论、实验和故事线。
- 将当前 idea 升级成更强、更反直觉、更普适的问题。
- 将当前结果作为一个子现象，转向一个更有 oral 潜力的新主线。
- 如果你判断当前方向上限不足，可以建议推倒重来，但必须给出可执行的新方向和最小验证路径。
- 所有判断必须建立在继续搜索最新论文基础上，尤其是 Lean theorem proving、premise selection、retrieval-augmented proving、proof repair、compiler feedback、process supervision、formal reasoning with verifiers 等方向。

请不要只做语言润色。目标是判断：这篇论文如何才能到 ICLR Oral 级别。

## 1. 当前论文一句话

当前 ICLR_2 的主线是：

> Failure feedback is conditional evidence for premise selection: after a failed Lean proof attempt, the right premise update is not always blind expansion; failure-conditioned control can improve premise recovery over static retrieval, top-k expansion, and learned+base fallback.

当前标题：

> Failure Feedback as Conditional Evidence for Lean Premise Selection

当前方法名：

> FAR-Hammer

当前论文最强 claim：

- Lean premise selection 不应该是 one-shot retrieval。
- 失败反馈不是日志，而是条件证据。
- 更多 premise 可能在 timeout/replay pressure 下反而伤害 proof search。
- 在强 learned retriever 和 learned+base fallback 之上，failure-conditioned second-stage controller 仍然能提升 imported-core trace-core recovery。
- 这些 gains 在 real Lean replay bridge subset 中仍保留一部分。

## 2. 当前 paper 的结构

当前 `paper.pdf` 已经是完整草稿，10 页左右，包含：

1. Abstract
2. Introduction
3. Related Work
4. Problem Formulation
5. Method
6. Experiments
7. Theory and Analysis
8. Limitations
9. Conclusion
10. Appendix: source list, feature ablation, global retrieval negative stress, bridge taxonomy, guardrail/expert-mix ablations, self-review

当前主文图表：

- 一个 closed-loop premise controller pipeline figure。
- Table 1: main claim-evidence map。
- Table 2: local trace-core + replay bridge。
- Table 3: timeout stress。
- Table 4: imported-core heldout。
- Table 5: split stability + 200-goal bridge。
- Table 6: diagnosis / ablation summary。

当前 paper 写作已经尽量避免过强 claim，明确说：

- 主结果是 trace-supervised premise recovery，不是 full theorem proving。
- bridge verified 是 trace-core recovery + original traced tactic replay，不是完整自动证明生成。
- BM25 / LeanSearch-style rows 是我们 protocol 内的 controlled retrieval policies，不是完整复现 LeanSearch v2 system。

## 3. 实验全貌

下面是实验过程的 condensed but detailed 版本。请把它当作 reviewer-facing evidence inventory，而不是只看当前 paper 的压缩版表格。

### Phase 1: Same-file / local Mathlib trace-core recovery

目标：验证 failure-aware premise selection 是否优于静态检索和盲目扩展。

数据：

- 2,000 Mathlib local/same-file trace-core goals。
- Metric: trace-core success, first-failure recovery (FFR), average unique premises。
- Trace-core success 表示 selected premise set 覆盖 traced proof core；这不是 full proof reconstruction。

核心结果：

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `one_shot` | 58.0% | 0.0% | 28.4 |
| `topk_equal_budget` | 75.7% | 0.0% | 42.9 |
| `visible_feature_rerank` | 86.5% | 0.0% | 42.9 |
| `topk_expansion` | 91.5% | 79.9% | 46.9 |
| `rule_far_failure_type_only` | 91.5% | 79.9% | 46.9 |
| `rule_far_no_core_tags` | 95.7% | 89.7% | 45.1 |
| `rule_far_full` oracle-style ref | 98.3% | 96.0% | 42.9 |

解释：

- Failure-conditioned visible features 比 blind top-k expansion 高 +4.2 points。
- 比 static visible-feature rerank 高 +9.2 points。
- Failure type alone 只等于 top-k expansion，说明不是“知道 failure type”本身有效，而是 failure type 与 candidate features 的条件交互有效。

Canonical outputs:

- `outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.json`
- `outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.md`

### Phase 1 Bridge: real Lean replay filter

目标：检查 Phase 1 trace-core gains 是否完全脱离 real Lean execution。

设置：

- 100 disagreement-heavy bridge goals。
- Original traced tactic replay success: 86/100。
- Bridge verified = trace-core success AND original traced tactic replay succeeds in real Lean。

核心结果：

| Method | Trace-core | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|
| `one_shot` | 13.0% | 10.0% | 0.0% | 31.1 |
| `visible_feature_rerank` | 38.0% | 33.0% | 0.0% | 52.9 |
| `topk_expansion` | 54.0% | 43.0% | 37.9% | 81.0 |
| `rule_far_no_core_tags` | 85.0% | 72.0% | 71.3% | 75.7 |
| `rule_far_full` oracle-style ref | 92.0% | 79.0% | 79.3% | 67.6 |

解释：

- Phase 1 bridge 是强支持证据：failure-conditioned local controller 不只是 trace-core artifact。
- 但它还是 disagreement-heavy subset，不是 random full theorem proving benchmark。

Canonical outputs:

- `outputs/phase1_reconstruction_bridge_report_100.md`
- `outputs/phase1_reconstruction_bridge_replay_100.json`

### Phase 2: feature-group ablation

目标：解释哪些 visible features 真的有用，以及 failure conditioning 是否必要。

核心结果：

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `visible_feature_name_rerank` | 85.3% | 0.0% | 42.9 |
| `visible_feature_statement_rerank` | 77.6% | 0.0% | 42.9 |
| `visible_feature_decl_rerank` | 78.3% | 0.0% | 42.9 |
| `visible_feature_rerank` | 86.5% | 0.0% | 42.9 |
| `rule_far_no_core_decl_features` | 92.6% | 82.4% | 46.2 |
| `rule_far_no_core_statement_features` | 92.8% | 82.9% | 46.4 |
| `rule_far_no_core_name_features` | 95.0% | 88.1% | 45.4 |
| `rule_far_no_core_tags` | 95.7% | 89.7% | 45.1 |

解释：

- Name/namespace morphology 是最强 visible feature。
- Statement/decl features 静态很弱，但 failure-conditioned 后有明显提升。
- 这支持“failure event changes feature utility”，而不是“某组 feature 静态就足够”。

Canonical outputs:

- `outputs/phase2_feature_group_ablation_2000_a40.md`

### Phase 2: timeout stress

目标：验证核心反直觉 insight：more premises can hurt。

设置：

- 2,000 local goals。
- Timeout-first stress backend。
- Metric includes timeout rate。

核心结果：

| Method | Success | FFR | Avg premises | Timeout rate |
|---|---:|---:|---:|---:|
| `one_shot` | 57.0% | 0.0% | 28.4 | 4.0% |
| `topk_equal_budget` | 43.8% | 0.0% | 42.9 | 56.2% |
| `visible_feature_rerank` | 43.8% | 0.0% | 42.9 | 56.2% |
| `topk_expansion` | 59.7% | 6.2% | 50.4 | 46.1% |
| `rule_far_no_core_tags` | 59.7% | 6.2% | 42.8 | 46.1% |
| `rule_far_no_core_timeout_shrink` | 69.3% | 28.6% | 42.7 | 23.5% |
| `rule_far_full` oracle-style ref | 100.0% | 100.0% | 40.1 | 22.5% |

解释：

- Equal-budget top-k 比 one-shot 更差，这是当前最反直觉的结果之一。
- Timeout-conditioned shrink 是重要机制证据：failure feedback 不只是加更多 premise，而是能选择 shrink / precision retry。

Canonical outputs:

- `outputs/phase2_timeout_stress_2000_a40.md`

### Phase 3A: imported-core global retrieval stress

目标：测试 local/same-file controller 是否能扩展到全局 imported premises。

数据：

- 2,000 imported-core goals。
- Avg imported proof-core premises: 4.26。
- Avg imported candidates: 188.6。
- Avg same-file candidates: 50.9。
- Avg total candidates: 239.5。

核心结果：

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `one_shot` | 1.1% | 0.0% | 32.0 |
| `same_file_prior_rerank` | 2.1% | 0.0% | 56.0 |
| `visible_feature_rerank` | 2.4% | 0.0% | 56.0 |
| `bm25_rerank` | 7.0% | 0.0% | 56.0 |
| `leansearch_iterative` | 11.9% | 8.3% | 91.9 |
| `bm25_expansion` | 11.9% | 8.3% | 92.2 |
| `rule_far_bm25` | 12.2% | 8.7% | 92.2 |
| `rule_far_no_core_tags` | 4.7% | 3.6% | 94.9 |
| `rule_far_full` old oracle ref | 55.7% | 55.2% | 86.6 |

解释：

- 这是重要负结果：local no-core FAR 不能直接解决 global imported retrieval。
- BM25/LeanSearch-style lexical policies only around 12% in our controlled candidate-pool protocol。
- 这个阶段说明：如果 paper 要在 global/imported setting 做主 claim，必须加入 learned/global retriever。

风险：

- `leansearch_iterative` 是 protocol 内的 controlled policy，不是完整复现 LeanSearch v2 system。
- Reviewer 可能认为 baseline 不公平或过弱；当前 paper 已经加了边界说明，但 Oral 级别可能需要更强外部对比。

Canonical outputs:

- `outputs/phase3_global_retrieval_2000_a40.md`

### Phase 3B: learned global retriever

目标：确认 imported-core 失败是不是 retriever bottleneck。

设置：

- Train/eval split: 1500/500。
- Learned retriever trained from traced proof-core labels。

Retriever recall:

| Ranker | All-core@32 | All-core@56 | All-core@96 | Mean core recall@96 |
|---|---:|---:|---:|---:|
| `base_score` | 1.4% | 1.6% | 2.6% | 26.7% |
| `learned_score` | 50.4% | 64.2% | 84.0% | 96.3% |

Heldout result:

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `bm25_expansion` | 12.8% | 8.4% | 91.5 |
| `leansearch_iterative` | 12.2% | 7.8% | 91.4 |
| `rule_far_bm25` | 13.0% | 8.8% | 91.5 |
| `learned_rerank` | 64.2% | 0.0% | 56.0 |
| `learned_expansion` | 84.0% | 67.7% | 57.7 |
| `rule_far_learned` | 84.4% | 68.5% | 57.4 |
| `rule_far_full` old oracle ref | 55.6% | 55.0% | 86.6 |

解释：

- Imported-core failure 是 retriever bottleneck，不是 idea ceiling。
- Learned retrieval 恢复了任务可行性。
- 但 `rule_far_learned` over `learned_expansion` 的 controller gain 很小，不能作为最终主贡献。

Canonical outputs:

- `outputs/phase3_learned_retriever_eval_500_a40.md`

### Phase 3C: learned+base fallback as strong baseline

目标：构造强 failure-agnostic baseline。

核心结果：

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `learned_rerank` | 64.2% | 0.0% | 56.0 |
| `learned_expansion` | 84.0% | 67.7% | 57.7 |
| `rule_far_learned` | 84.4% | 68.5% | 57.4 |
| `learned_base_fallback` | 87.0% | 73.8% | 57.6 |
| `rule_far_learned_failure_specific` | 87.0% | 73.8% | 57.0 |

解释：

- `learned_base_fallback` 是当前最强 failure-agnostic baseline。
- 手写 failure-specific learned controller 没超过 fallback。
- 这迫使我们训练 learned second-stage controller。

Canonical outputs:

- `outputs/phase3_learned_controller_ablation_500_a40.md`

### Phase 3D: learned second-stage controller

目标：测试真正的 failure-conditioned learned controller 是否超过 strong fallback。

核心结果：

| Method | Success | FFR | Avg premises |
|---|---:|---:|---:|
| `learned_rerank` | 64.2% | 0.0% | 56.0 |
| `learned_expansion` | 84.0% | 67.7% | 57.7 |
| `learned_base_fallback` | 87.0% | 73.8% | 57.6 |
| `rule_far_learned_failure_specific` | 87.0% | 73.8% | 57.0 |
| `rule_far_learned_second_stage` | 92.4% | 84.7% | 53.9 |

解释：

- Main positive result: +5.4 success over learned+base fallback。
- FFR +10.9 points。
- Avg premises lower: 53.9 vs 57.6。
- 这是当前 paper 最关键的 positive controller evidence。

Canonical outputs:

- `outputs/phase3_second_stage_controller_eval_500_a40.md`

### Phase 3E: split stability

目标：确认 Phase 3D 不是 one-split artifact。

四个 500-goal split 汇总：

| Split | Fallback success | Second-stage success | Final-base8 success |
|---|---:|---:|---:|
| original | 87.0% | 92.4% | 92.6% |
| fold0 | 83.6% | 91.6% | 91.6% |
| fold1 | 86.0% | 92.2% | 93.4% |
| fold2 | 88.8% | 94.0% | 94.0% |
| mean | 86.3% | 92.5% | 92.9% |

Aggregate:

| Policy | Success mean | Success std | FFR mean | Avg premises mean |
|---|---:|---:|---:|---:|
| `learned_base_fallback` | 86.3% | 1.9 | 70.7% | 55.9 |
| `rule_far_learned_second_stage` | 92.5% | 0.9 | 84.0% | 52.5 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 92.9% | 0.9 | 84.8% | 52.5 |

解释：

- Second-stage gain stable across splits。
- Final-base8 是 small focused ablation，不是新主方法。

Canonical outputs:

- `outputs/phase3_split_stability_summary_4x500.md`

### Phase 3 bridge replay: 100 and 200 goal subsets

目标：验证 imported-core trace-core gains 是否经过 real Lean replay filter 后仍存在。

100-goal bridge:

- original second-stage bridge verified: 47.0%
- learned_base_fallback bridge verified: 31.0%
- final-base8 bridge verified: 49.0%

200-goal bridge:

| Policy | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|
| `learned_expansion` | 60.0% | 38.5% | 24.5% | 72.8 |
| `learned_base_fallback` | 67.5% | 44.5% | 33.1% | 69.9 |
| `rule_far_learned_second_stage` | 81.0% | 52.5% | 44.6% | 66.2 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 81.5% | 53.5% | 46.0% | 66.2 |

Key delta:

- Final-base8 vs fallback: +9.0 bridge verified points。
- Final-base8 vs original second-stage: +1.0 bridge verified point。
- Final-base8 uses 3.6 fewer avg premises than fallback。

Bridge replay status:

- Replay goals: 200。
- Original traced tactic replay success: 124/200 = 62.0%。

Selected categories:

- `second_stage_over_fallback`: 34
- `second_stage_over_expansion`: 30
- `fallback_over_second_stage`: 6
- `both_fail`: 31
- `both_success`: 20
- `fallback_fill`: 79

Bridge failure taxonomy:

| Primary replay tag | Count |
|---|---:|
| replay verified | 124 |
| unknown identifier | 30 |
| other Lean error | 13 |
| typeclass | 8 |
| unsolved goals | 7 |
| simp no progress | 6 |
| tactic failed | 5 |
| type mismatch | 5 |
| sorry context | 2 |

Negative-case inspection on 200 bridge:

- Inspected replay-verified trace misses: 17。
- Candidate-pool miss cases: 0。
- Fallback-selected core drops: 2。
- Expansion-selected core drops: 3。
- Failure-conditioned rank misses: 15。
- Second-stage failure type: all 17 are `imported_premise_missing`。

解释：

- Bridge confirms gain survives a real Lean replay filter。
- But absolute bridge verified is only 53.5% on a disagreement-heavy subset。
- It is not full proof reconstruction。
- Remaining misses are mostly rank/calibration misses, not candidate-generation ceiling。

Canonical outputs:

- `outputs/phase3_bridge_report_200.md`
- `outputs/phase3_bridge_failure_taxonomy_200.md`
- `outputs/phase3_bridge_negative_case_inspection_200.md`

### Guardrail and expert-mix negative experiments

目标：诊断 residual failures 后，尝试能不能手写提升 controller。

尝试过的方向：

- Hard base guardrail。
- Soft base-score mix。
- Imported-failure multi-expert max。
- Final-only base guardrail top8/top16/top32。
- Final-only expert guardrails。
- Final-only hybrid base+expert guardrails。

结论：

- Broad hard guardrails hurt bridge trace-core: 72.0% -> 63.0% / 60.0%。
- Soft base-score mixing low alpha 基本 inert，高 alpha harmful。
- Multi-expert imported-failure routing harmful: bridge trace-core drops to 62.0%。
- Final expert guardrail-16 在 original/fold0/bridge 都不如 final-base8。
- Final-base8 is best small focused rescue: tiny high-base rescue only on final retry。

解释：

- 这是有用的 negative evidence。
- 它说明不是随便加 heuristic 就能更强。
- 也说明 remaining headroom 可能需要 learned calibrated expert gate，而不是手写 rule。

## 4. 当前最硬主线

当前最硬、最安全的主线是：

> Failed proof search provides conditional evidence for premise utility. Under fixed proof-search budgets, failure-conditioned premise selection can outperform static retrieval, blind expansion, and learned+base fallback, while using fewer premises. The strongest version learns a second-stage controller conditioned on the first failure; its gains are stable across splits and survive a real Lean replay bridge.

这个主线的优势：

- 有清楚反直觉点：more premises can hurt。
- 有机制解释：failure event changes posterior over premise utility。
- 有从 local -> timeout -> imported-core -> split stability -> replay bridge 的完整实验链。
- 有 negative ablations，说明不是手写调参堆出来的。

这个主线的不足：

- 仍然像 strong system/method paper，而不是一眼改变领域认知的 oral paper。
- 主结果多数是 trace-core recovery。
- Bridge 是 subset validation，不是 end-to-end theorem proving。
- Strongest external competitors没有完整 system-level 对比。
- Learned retriever / controller 使用 traced proof-core labels，监督设定较强。

## 5. 为什么目前还不像 ICLR Oral

请不要只说“还需要更多实验”。更具体地说，目前有以下问题：

### 5.1 Oral-level novelty 不够尖锐

当前 idea 是合理且有价值的，但 reviewer 可能会觉得：

- Proof failure feedback is useful 是 intuitively expected。
- Proof repair / process feedback / RL with verifier feedback 已经在快速发展。
- 我们的贡献更像 premise-selection-specific implementation，而不是新范式。

需要升级成更尖锐的 insight，例如：

- Failure feedback is useful only when it is treated as conditional evidence with a non-monotonic budget model。
- More retrieval can be harmful even when proof-core recall improves。
- Failure-conditioned control has a theory of when to expand, shrink, preserve fallback, or give up。
- There is a formal separation between premise coverage, search tractability, replayability, and proof success。

### 5.2 Evaluation boundary is the main ceiling

当前最大硬伤：

- Trace-core success is not proof success。
- Bridge replay uses original traced tactic scripts。
- Bridge subset is disagreement-heavy, not a random theorem proving benchmark。

这会让 reviewer 觉得：

- This is not a full Lean prover improvement。
- Maybe it is only a supervised premise-recovery artifact。
- Maybe gains do not translate to actual proof generation。

要冲 oral，可能需要至少一个更接近 full proving 的 validation：

- Plug into a real Lean hammer/prover loop。
- Show proof success gains on random heldout Lean goals。
- Or show failure-conditioned retrieval improves a strong existing prover/retriever system in a controlled end-to-end way。

### 5.3 Baseline risk is nontrivial

当前 strongest related work：

- LeanSearch v2 has global premise retrieval and downstream proof-generation evaluation。
- LeanHammer directly targets premise selection for hammers。
- LeanDojo/ReProver is standard retrieval-augmented theorem proving infrastructure。
- APRIL and process-verified RL show compiler/verifier feedback as supervision signal。

Reviewer may ask:

- Why not compare to full LeanSearch v2?
- Why not plug into LeanHammer?
- Is your `leansearch_iterative` just a weak proxy?
- Is your method really better than proof repair / feedback-conditioned LLM systems, or just solving a narrower trace-core task?

### 5.4 The theory is currently suggestive, not deep

Current theory:

- Failure feedback reduces uncertainty if it has mutual information with premise utility。
- Premise coverage is not monotonic in premise budget。
- Narrow guardrail can help when learned controller suppresses base rescue premises。

This is useful, but not oral-level deep. To upgrade:

- Need sharper formalism: controlled decision problem, posterior update, budgeted risk, non-monotonic success curve, conditions for shrink vs expand。
- Need theory make falsifiable predictions matched to experiments。
- Need maybe a theorem/separation: coverage recall can increase while verified/replay success decreases under bounded search。

## 6. Comparison to ICLR_1 and lessons to import

ICLR_1 project: `D:\ICLR_1`

ICLR_1 paper title:

> When Restoration Lies: Behavioral Effect Alone Is Insufficient Evidence of Mechanism in Causal Interpretability

ICLR_1 is stronger because:

- Its core insight is more immediately provocative: behavioral restoration can lie。
- It introduces a clean evidence hierarchy: Restoration, Validity, Mechanism Alignment。
- It has a strong failure mode: answer smuggling。
- It has independent mechanism validation: Name Mover Head evidence。
- It has a geometric/theoretical account: conditional manifold, normal displacement, mechanism fiber。
- Negative/repair results deepen the idea instead of just limiting it。

What ICLR_2 should learn:

1. Find the equivalent of `behavior restoration lies` in Lean premise selection.
   - Maybe: proof-core coverage lies.
   - Maybe: retrieval recall lies.
   - Maybe: replay-verified trace-core lies.
   - Maybe: more premises lie.

2. Separate evidence axes as a conceptual contribution.
   Current possible axes:
   - Premise coverage
   - Search tractability
   - Replayability
   - Full proof success
   - Failure-conditioned recoverability

3. Identify a named mechanism/failure mode.
   Current candidates:
   - Premise stuffing
   - Failure-agnostic fallback trap
   - Retrieval-recall illusion
   - Search-space poisoning
   - Replay fragility
   - Conditional premise posterior shift

4. Add independent validation analogous to NMH.
   For ICLR_2, this could be:
   - Actual proof success in Lean hammer loop。
   - Independent proof reconstruction success。
   - Removing selected premises and measuring proof breakage。
   - Prover search statistics showing search-space poisoning。
   - Cross-prover consistency: Duper/Aesop/Lean-auto style backend।

## 7. Recent literature context that GPT Pro must update

I did a lightweight online check on 2026-06-21. GPT Pro must do a deeper literature search before making final recommendations.

Known important references:

1. LeanSearch v2: Global Premise Retrieval for Lean 4 Theorem Proving  
   Link: https://arxiv.org/abs/2605.13137  
   Why important: strongest direct competitor on global premise retrieval. Reports reasoning mode recovering 46.1% ground-truth premise groups within 10 candidates and downstream proof success gains in a fixed prover loop.

2. Learning to Repair Lean Proofs from Compiler Feedback / APRIL  
   Link: https://arxiv.org/abs/2602.02990  
   Why important: feedback-conditioned supervision for Lean proof repair; could attack our novelty if we say “failure feedback is useful” too broadly.

3. Process-Verified Reinforcement Learning for Theorem Proving via Lean  
   Link: https://openreview.net/forum?id=P00k4DFaXF  
   Also arXiv appears at: https://arxiv.org/html/2606.20068v1  
   Why important: Lean as symbolic process oracle with fine-grained tactic-level feedback; directly adjacent to “failure feedback as supervision”.

4. LeanDojo / ReProver  
   Link: https://arxiv.org/abs/2306.15626  
   Why important: standard infrastructure and retrieval-augmented theorem proving baseline.

5. Premise Selection for a Lean Hammer  
   Link: https://arxiv.org/abs/2506.07477  
   Why important: direct Lean hammer premise-selection competitor.

6. LeanHammer project page  
   Link: https://cmu-l3.github.io/lean-hammer/  
   Why important: practical Lean hammer system; likely important for end-to-end evaluation positioning.

7. Tree-Based Premise Selection for Lean4  
   Link found in search: NeurIPS 2025 paper PDF.  
   Why important: structural premise selection; may be a baseline or related work depending on final direction.

GPT Pro should also search:

- “Lean theorem proving compiler feedback 2026”
- “Lean 4 premise selection retrieval 2026”
- “LeanSearch v2 benchmark reasoning mode”
- “LeanHammer premise selection ICLR 2026”
- “Lean proof repair compiler feedback APRIL”
- “formal theorem proving process supervision Lean verifier feedback”
- “retrieval augmented theorem proving Lean benchmark proof success”
- “Duper Lean premise selection hammer”

## 8. Potential oral-upgrade routes to evaluate

Please evaluate all routes below. Do not assume current paper must survive unchanged.

### Route A: Keep current idea, add end-to-end proof success

Hypothesis:

> The current paper becomes main-track strong if we show failure-conditioned premise selection improves actual Lean hammer/prover success, not only trace-core recovery.

Needed:

- Integrate FAR-Hammer with a real prover loop.
- Compare against LeanSearch v2 / LeanHammer / ReProver-style retrieval if feasible.
- Random heldout goal set, not only disagreement-heavy bridge.
- Report proof success, timeout, reconstruction failure, premise budget, wall-clock/calls.

Risk:

- Engineering heavy.
- Gains may shrink.
- If absolute proof success is low, story may still not reach oral.

### Route B: Reframe as “retrieval recall lies”

Hypothesis:

> The oral-level insight is not just failure feedback, but that premise-retrieval recall can be misleading under bounded proof search; failure feedback identifies when recall should be traded for search tractability.

Needed:

- Show cases where higher proof-core recall / more premises reduce replay/proof success。
- Build a formal hierarchy analogous to ICLR_1:
  - Coverage
  - Search tractability
  - Replayability
  - Verified proof success
- Add independent search-statistics evidence。

Risk:

- May become more diagnostic/evaluation-like unless paired with a strong method.

### Route C: Turn failure feedback into a theory of conditional proof search

Hypothesis:

> The method is less important than the formal framework: proof search failures define conditional posterior updates over missing/noisy premises under bounded search.

Needed:

- Formal model of premise utility with missing-premise and noise/search-cost terms。
- Theorem: blind expansion can be dominated by failure-conditioned shrink/rerank under certain cost structure。
- Empirical predictions mapped to Phase 1/2/3:
  - failure type alone insufficient
  - feature utility changes after failure
  - timeout shrink works
  - base guardrail helps only late/narrow

Risk:

- Theory may remain too simple unless made precise and predictive。

### Route D: Build a learned calibrated expert-gate method

Hypothesis:

> Current residual failures show hand-written expert mixing fails; a learned calibrated gate over retriever experts could be the real method contribution.

Evidence for feasibility:

- 200-bridge negative inspection: 0 candidate-pool misses, 15/17 rank misses.
- Base rank still useful in 9/19 missed-core top96 cases.
- Existing hand-written expert insertion hurts, suggesting learned calibration is needed.

Needed:

- Train gate to choose among learned score, base score, BM25, same-file/local, failure-specific expert。
- Use replay-aware or failure-aware labels if possible。
- Ablate learned gate vs hand-written expert-mix negative results。

Risk:

- Could become incremental if not framed as solving a precise failure mode。
- Needs strong evidence over current final-base8。

### Route E: Pivot to failure-supervised data/model training

Hypothesis:

> Failure traces should supervise not only premise reranking but a model that predicts proof-search bottleneck classes and decides retrieval actions.

Possible main contribution:

- A “failure-conditioned action model” that chooses expand/shrink/fallback/retrieve/import/local/repair。
- Stronger relation to APRIL and process-verified RL, but still focused on premise selection。

Needed:

- Build dataset of failure states and successful recovery actions。
- Train action predictor。
- End-to-end or bridge validation。

Risk:

- Larger project; overlaps with proof repair/process supervision。

### Route F: Push current paper only to solid accept, not oral

Hypothesis:

> Current evidence is enough for a solid main-track submission after baseline and wording improvements, but not worth chasing oral at high cost.

Needed:

- Strengthen related work and baseline discussion。
- Add random bridge sanity check。
- Add one external baseline or clearer LeanSearch comparison。
- Polish theory and figures。

Risk:

- May under-shoot the user’s goal。

## 9. Questions GPT Pro should answer

Please answer these explicitly:

1. What is the strongest possible oral-level version of this work?
2. Is the current central claim strong enough, or should the paper pivot?
3. What is the most promising “ICLR_1-style” conceptual hierarchy for this domain?
4. What is the Lean equivalent of “restoration lies”?
5. Which experiment would most increase oral probability per unit time?
6. Which experiment is expensive but decisive?
7. Which current experiments should be removed from main paper or moved to appendix?
8. Which current claims are over-safe and can be made sharper?
9. Which claims are too risky and should be weakened?
10. What recent papers most threaten novelty?
11. What recent papers can support positioning?
12. Does the project need end-to-end theorem proving success to be oral-level?
13. If yes, what is the minimal end-to-end experiment?
14. If no, what conceptual/theoretical upgrade can compensate?
15. Should we continue current direction, substantially pivot, or restart?

## 10. Desired output from GPT Pro

Please produce a markdown file that can be handed back to the coding agent for execution. It should include:

1. Executive verdict:
   - current paper score
   - oral probability
   - accept probability
   - top reason it is not oral yet

2. Literature map:
   - latest related papers searched
   - direct competitors
   - adjacent feedback/proof repair/process supervision work
   - how each threatens or supports this paper

3. Recommended main-track upgrade strategy:
   - choose one primary route
   - explain why alternatives are weaker
   - define the new central claim

4. Required experiments:
   - exact experiment name
   - purpose
   - expected outcome
   - what outcome would kill the idea
   - estimated difficulty
   - priority order

5. Theory upgrade:
   - new formal definitions
   - propositions/theorems
   - proof sketches
   - empirical predictions

6. Paper rewrite plan:
   - new title options
   - new abstract outline
   - section-by-section rewrite
   - figures/tables to keep/drop/add

7. Decision tree:
   - if experiment A succeeds, do X
   - if A fails but B succeeds, do Y
   - if both fail, pivot/restart plan

8. Concrete execution plan:
   - Phase 0 literature search
   - Phase 1 minimum decisive experiment
   - Phase 2 method upgrade
   - Phase 3 theory/writing integration

## 11. Important warnings for GPT Pro

- Do not recommend turning this into a benchmark/evaluation paper.
- Do not accept trace-core recovery as sufficient for oral-level claims unless you provide a strong conceptual reason.
- Do not treat LeanSearch-style local proxy as equivalent to full LeanSearch v2 system.
- Do not hide the supervised traced proof-core training assumption.
- Do not overvalue small heuristic gains like final-base8; it is a focused ablation, not the core idea.
- Do not propose “run more random experiments” without specifying how the result changes the paper’s claim.
- Do not assume the current paper must be preserved. If a pivot is best, say so clearly.

