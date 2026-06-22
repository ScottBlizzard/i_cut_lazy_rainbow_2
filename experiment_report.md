# FAR-Hammer 实验报告

更新时间：2026-06-22

这个文件只保留当前论文可用的实验信息：阶段目的、核心数字、可引用结论、限制和 canonical outputs。早期 smoke test、启动日志、已修复 bug 流水账、已知不可引用 artifact 不再放入主报告。

## 0. 当前总判断

Verified-pivot update:

- The strongest current verified mainline is no longer the old trace-core-only failure-conditioned controller. The paper-level route should now be framed as action-conditional evidence allocation on replayable Mathlib 4.30 theorem contexts.
- The strongest completed verified evidence is the scaled230 typed action matrix: oracle 58/230 vs best static 38/230; strict action-dependent goals 29; fixed typed controls reach 55/230 OOF at K=2 and 57/230 OOF at K=4, with train-fitted K=4 reaching the 58/230 oracle.
- The focused Aesop counterfactual control strengthens the mechanism story: under the same source/budget, `facts+simps` exposure solves 38/230, facts-only solves 5/230, simps-only solves 4/230, the single-channel union solves only 7/230, and 34 goals are joint-only. Increasing facts+simps exposure to 32 names drops to 3/230 and loses 35 of the top-8 successes.
- E1 strict filtering is a robustness boundary, not an improvement: filtered-only oracle is 4/230, combined oracle stays 58/230, and no new oracle goals are added.
- The stronger typed allocator gate is negative for adaptive claims: pure logreg/CNB do not beat fixed, and fixed-prefix residual logreg/CNB only match fixed K=4 at 57/230. Current verified evidence favors a typed evidence-allocation mechanism with fixed typed controls as hard baselines; learned adaptive allocation remains an open target, not a supported main claim.

当前最强 verified 论文主线是：证明失败后的有效干预不只是“多加 premise”，而是必须把同一批证据通过正确的 Lean 接口暴露给搜索/重构机制。当前最硬的主结果应围绕 `aesop`、`hammerCore`、`hammer` 和 `solve_by_elim` 的 compute-budgeted typed proof-action portfolio；failure-conditioned controller 仍作为目标和后续路线，但不能在当前 verified 结果里作为已经成立的主 claim。

最关键结果：

- Phase 1 same-file/local trace-core：`rule_far_no_core_tags` 在 2k 目标上达到 95.7% success / 89.7% FFR，明显超过静态可见特征 rerank 和 blind top-k expansion。
- Phase 1 real Lean bridge：100 个 disagreement-heavy replay goal 上，`rule_far_no_core_tags` 的 bridge verified success 为 72.0%，高于 `topk_expansion` 43.0% 和 `visible_feature_rerank` 33.0%。
- Phase 2 timeout stress：更多 premise 在 timeout 下会反直觉变差；`topk_equal_budget` / `visible_feature_rerank` 只有 43.8%，而 `rule_far_no_core_timeout_shrink` 达到 69.3%。
- Phase 3 imported-core：原始 BM25 / controlled iterative lexical proxy 方法只有约 12%，但 learned retriever + failure-conditioned second stage 达到 92.4%。
- Phase 3 split stability：alternate fold0 中 learned retriever 更弱，但 second-stage controller 仍有 91.6%，高于 `learned_base_fallback` 83.6%。
- Phase 3 bridge replay：200 个 disagreement-heavy imported-core replay goal 上，`rule_far_learned_second_stage_final_base_guardrail_8` bridge verified 为 53.5%，高于原 second-stage 52.5% 和 `learned_base_fallback` 44.5%。
- Verified pivot：LeanHammer 4.30 + Mathlib 4.30 路线已打通；Mathlib-context Gate 1 premise smoke 通过，100-goal verified action-grid theorem-family pilot 中 oracle/true feedback 为 80.0%，best static 为 40.0%。
- Traced-corpus proof-action pilot：230 个 replayable Mathlib theorem context 上，typed action grid 从原始 51/230 oracle 扩展到 58/230 oracle；best static 为 `aesop_core_plus_learned` 的 38/230；严格 action-dependent goals 为 29。
- Budgeted portfolio：在 `hammer_empty` 后，固定 typed portfolio 的 OOF K=2 为 55/230，OOF K=4 为 57/230；train-fitted K=4 达到 58/230 oracle。
- Aesop 机制消融：`facts+simps` 远强于 facts-only/simps-only；single-channel union 只有 7/230，而 facts+simps 有 34 个 joint-only goals；`core+learned8` 明显强于 `core+learned32`，支持“action-conditional evidence allocation”而不是“premise 越多越好”的主线。

当前主要限制：

- 多数主结果仍是 trace-core proof-core recovery，不等于完整 proof reconstruction。
- Phase 1 和 Phase 3 都已有 bridge replay 支撑，但 Phase 3 bridge 仍是 200-goal disagreement-heavy subset，不是完整随机 proof reconstruction benchmark。
- learned retriever 和 second-stage controller 使用 traced proof-core labels 训练；论文必须如实描述监督来源。
- 新的 Mathlib-context LeanHammer Gate 1/2 是生成的 theorem-family pilot，不是 traced-corpus theorem replay；它支持 verified intervention route 可行，但还不能作为最终主实验。
- Traced-corpus proof-action pilot 已有更稳定的 scaled 正信号，但绝对成功率仍低；当前只能强 claim typed proof-action portfolio，不能 claim adaptive routing 已经超过 matched-compute fixed portfolio。

## 1. 协议与指标

Trace-core recovery：给定 traced proof core，如果某次 attempt 的 premise set 覆盖 proof core，则记为 trace-core success。这验证的是 premise recovery，不是自动合成完整证明。

First-failure recovery, FFR：首轮失败后，后续 attempt 能恢复成功的比例。这个指标直接衡量 failure feedback 是否带来修复能力。

Avg premises：每个 goal 平均尝试的 unique premise 数。若 success 更高但 premise 数也大幅更高，论文说服力会下降；因此 Phase 3D/3E 的“更高 success + 更少 premise”很重要。

Bridge verified：trace-core success 与原 traced tactic script 在真实 Lean 进程中 replay 成功同时成立。当前 bridge 是验证 trace-core 结果是否脱离真实 Lean 过远的中间层。

## 2. Phase 1: Same-File / Local Trace-Core

目标：验证 failure-aware premise selection 在 same-file/local Mathlib trace-core recovery 中是否显著优于静态检索和盲目扩展。

Canonical output:

- `outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.json`
- `outputs/phase1_mathlib_trace_core_2000_feature_ablation_a40.md`

核心结果：

| Method | Goals | Success | FFR | Avg premises | 结论 |
|---|---:|---:|---:|---:|---|
| `one_shot` | 2000 | 58.0% | 0.0% | 28.4 | 初始检索基线 |
| `topk_equal_budget` | 2000 | 75.7% | 0.0% | 42.9 | 同预算静态 top-k |
| `visible_feature_rerank` | 2000 | 86.5% | 0.0% | 42.9 | 静态可见特征有效但不足 |
| `topk_expansion` | 2000 | 91.5% | 79.9% | 46.9 | 盲目扩展强 baseline |
| `rule_far_failure_type_only` | 2000 | 91.5% | 79.9% | 46.9 | failure type alone 约等于 top-k expansion |
| `rule_far_no_core_tags` | 2000 | 95.7% | 89.7% | 45.1 | 主 no-core / visible-feature FAR |
| `rule_far_full` | 2000 | 98.3% | 96.0% | 42.9 | trace-tag oracle-style upper reference |

阶段结论：

- `rule_far_no_core_tags` 比 `topk_expansion` 高 +4.2 success points、+9.8 FFR，同时平均 premise 更少。
- `rule_far_no_core_tags` 比 `visible_feature_rerank` 高 +9.2 success points，说明效果不是静态 rerank 能解释的。
- `rule_far_failure_type_only` 没超过 `topk_expansion`，说明仅知道失败类型不够；必须把 failure type 与 candidate features 结合。

## 3. Phase 1 Bridge: Real Lean Replay Filter

目标：在真实 Lean replay 可行子集上复核 Phase 1 trace-core 结果，避免 trace-core 指标完全漂浮。

Canonical outputs:

- `outputs/phase1_reconstruction_bridge_goals_100.jsonl`
- `outputs/phase1_reconstruction_bridge_replay_100.json`
- `outputs/phase1_reconstruction_bridge_report_100.md`

Bridge 设置：

- Replay goals: 100
- Original traced tactic replay success: 86/100 (86.0%)
- Bridge success = trace-core proof-core recovered AND original tactic replay succeeds.

核心结果：

| Method | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|---:|
| `one_shot` | 100 | 13.0% | 10.0% | 0.0% | 31.1 |
| `topk_equal_budget` | 100 | 22.0% | 16.0% | 0.0% | 52.9 |
| `visible_feature_rerank` | 100 | 38.0% | 33.0% | 0.0% | 52.9 |
| `topk_expansion` | 100 | 54.0% | 43.0% | 37.9% | 81.0 |
| `rule_far_failure_type_only` | 100 | 54.0% | 43.0% | 37.9% | 81.0 |
| `rule_far_no_core_tags` | 100 | 85.0% | 72.0% | 71.3% | 75.7 |
| `rule_far_full` | 100 | 92.0% | 79.0% | 79.3% | 67.6 |

阶段结论：

- `rule_far_no_core_tags` 在真实 replay filter 后仍明显强于 blind expansion 和 static reranking。
- 这不是完整 theorem proving benchmark，但足以说明 Phase 1 trace-core gain 与真实 Lean replay 并未脱节。

## 4. Phase 2: Ablations And Stress Tests

目标：拆解哪些可见特征有效，并验证“更多 premise 不一定更好”的反直觉 timeout insight。

### 4.1 Feature-Group Ablation

Canonical outputs:

- `outputs/phase2_feature_group_ablation_2000_a40.json`
- `outputs/phase2_feature_group_ablation_2000_a40.md`

核心结果：

| Method | Success | FFR | Avg premises | 结论 |
|---|---:|---:|---:|---|
| `visible_feature_decl_rerank` | 78.3% | 0.0% | 42.9 | decl-only 静态较弱 |
| `visible_feature_statement_rerank` | 77.6% | 0.0% | 42.9 | statement-only 静态较弱 |
| `visible_feature_name_rerank` | 85.3% | 0.0% | 42.9 | name/namespace 是最强静态组 |
| `rule_far_no_core_decl_features` | 92.6% | 82.4% | 46.2 | failure conditioning 后 decl 有用 |
| `rule_far_no_core_statement_features` | 92.8% | 82.9% | 46.4 | failure conditioning 后 statement 有用 |
| `rule_far_no_core_name_features` | 95.0% | 88.1% | 45.4 | name/namespace 仍最强 |
| `rule_far_no_core_tags` | 95.7% | 89.7% | 45.1 | all visible features 最强 |

阶段结论：

- Name/namespace morphology 是最强可见特征。
- Statement/decl 单独静态效果弱，但在 failure-conditioned setting 中明显变强。
- 这支持“failure type 决定如何使用 candidate features”，而不是“某个静态特征天然强”。

### 4.2 Timeout Stress

Canonical outputs:

- `outputs/phase2_timeout_stress_2000_a40.json`
- `outputs/phase2_timeout_stress_2000_a40.md`

核心结果：

| Method | Success | FFR | Avg premises | Timeout rate | 结论 |
|---|---:|---:|---:|---:|---|
| `one_shot` | 57.0% | 0.0% | 28.4 | 4.0% | 小 premise set 反而稳 |
| `topk_equal_budget` | 43.8% | 0.0% | 42.9 | 56.2% | 更多 premise 触发 timeout |
| `visible_feature_rerank` | 43.8% | 0.0% | 42.9 | 56.2% | 静态 rerank 同样受害 |
| `topk_expansion` | 59.7% | 6.2% | 50.4 | 46.1% | 盲目扩展 timeout 高 |
| `rule_far_no_core_tags` | 59.7% | 6.2% | 42.8 | 46.1% | 默认 no-core FAR 有 timeout 边界 |
| `rule_far_no_core_timeout_shrink` | 69.3% | 28.6% | 42.7 | 23.5% | timeout-conditioned shrink 有效 |

阶段结论：

- 这是重要反直觉结果：在 timeout 压力下，更多 premise 会降低成功率。
- failure-aware controller 不应该总是 expand；timeout 失败应触发 shrink / precision-oriented retry。

## 5. Phase 3: Imported-Core Global Retrieval

目标：打破 same-file/local 假设，验证方法能否处理真实 imported premise bottleneck。

### 5.1 Initial Global Stress

Canonical outputs:

- `outputs/phase3_mathlib_global_imported_core_goals_2000.jsonl`
- `outputs/phase3_global_retrieval_2000_a40.json`
- `outputs/phase3_global_retrieval_2000_a40.md`

Dataset summary:

- 2000 imported-core goals.
- Avg imported proof-core premises: 4.26.
- Avg imported candidates: 188.6.
- Avg same-file candidates: 50.9.
- Avg total candidates: 239.5.

核心结果：

| Method | Goals | Success | FFR | Avg premises | 结论 |
|---|---:|---:|---:|---:|---|
| `one_shot` | 2000 | 1.1% | 0.0% | 32.0 | base retrieval fails globally |
| `same_file_prior_rerank` | 2000 | 2.1% | 0.0% | 56.0 | same-file shortcut fails |
| `visible_feature_rerank` | 2000 | 2.4% | 0.0% | 56.0 | local visible features do not transfer |
| `bm25_expansion` | 2000 | 11.9% | 8.3% | 92.2 | lexical expansion helps but insufficient |
| `controlled_iterative_lexical` (`leansearch_iterative` in code) | 2000 | 11.9% | 8.3% | 91.9 | controlled iterative lexical proxy; not full LeanSearch v2 |
| `rule_far_bm25` | 2000 | 12.2% | 8.7% | 92.2 | failure wrapper alone barely helps BM25 |
| `rule_far_no_core_tags` | 2000 | 4.7% | 3.6% | 94.9 | local no-core features fail globally |
| `rule_far_full` | 2000 | 55.7% | 55.2% | 86.6 | oracle-style trace tags show recoverable headroom |

阶段结论：

- Phase 3 初始结果不是 idea ceiling，而是 global retriever bottleneck。
- same-file/local visible features 不能直接声明解决 imported-core retrieval。
- 必须引入 learned/global retriever。

### 5.2 Learned Global Retriever

Canonical outputs:

- `outputs/phase3_learned_train_goals_1500.jsonl`
- `outputs/phase3_learned_eval_goals_500.jsonl`
- `outputs/phase3_learned_retriever_model_1500_500.json`
- `outputs/phase3_learned_retriever_eval_500_a40.json`
- `outputs/phase3_learned_retriever_eval_500_a40.md`

Retriever recall audit on heldout 500:

| Ranker | All-core@32 | All-core@56 | All-core@96 | Mean core recall@96 |
|---|---:|---:|---:|---:|
| `base_score` | 1.4% | 1.6% | 2.6% | 26.7% |
| `learned_score` | 50.4% | 64.2% | 84.0% | 96.3% |

核心结果：

| Method | Success | FFR | Avg premises | 结论 |
|---|---:|---:|---:|---|
| `bm25_expansion` | 12.8% | 8.4% | 91.5 | lexical baseline |
| `controlled_iterative_lexical` (`leansearch_iterative` in code) | 12.2% | 7.8% | 91.4 | controlled iterative lexical proxy; not full LeanSearch v2 |
| `rule_far_bm25` | 13.0% | 8.8% | 91.5 | BM25 wrapper |
| `learned_rerank` | 64.2% | 0.0% | 56.0 | static learned retriever |
| `learned_expansion` | 84.0% | 67.7% | 57.7 | learned + blind expansion |
| `rule_far_learned` | 84.4% | 68.5% | 57.4 | simple failure wrapper |
| `rule_far_full` | 55.6% | 55.0% | 86.6 | old oracle-tag hand controller, not upper bound here |

阶段结论：

- Learned retriever 将 imported-core success 从约 12-13% 提升到 84.0%。
- 但是 `rule_far_learned` 只比 `learned_expansion` 高 +0.4，说明必须进一步训练真正的 second-stage failure-conditioned controller。

### 5.3 Learned Controller Baselines

Canonical outputs:

- `outputs/phase3_learned_controller_ablation_500_a40.json`
- `outputs/phase3_learned_controller_ablation_500_a40.md`

核心结果：

| Method | Success | FFR | Avg premises | 结论 |
|---|---:|---:|---:|---|
| `learned_expansion` | 84.0% | 67.7% | 57.7 | strong learned baseline |
| `learned_base_fallback` | 87.0% | 73.8% | 57.6 | strongest failure-agnostic fallback |
| `rule_far_learned_failure_specific` | 87.0% | 73.8% | 57.0 | hand-written failure-specific schedule |

阶段结论：

- 强 baseline 从 BM25 / learned expansion 升级为 `learned_base_fallback`。
- 手写 failure-specific schedule 只匹配 fallback，不能证明 controller contribution。
- 下一步必须训练 second-stage controller。

### 5.4 Learned Second-Stage Controller

Canonical outputs:

- `outputs/phase3_second_stage_eval_goals_500.jsonl`
- `outputs/phase3_second_stage_controller_model_1500_500.json`
- `outputs/phase3_second_stage_controller_eval_500_a40.json`
- `outputs/phase3_second_stage_controller_eval_500_a40.md`

Training summary:

- Train/eval split: first 1500 imported-core goals for training, last 500 for heldout evaluation.
- First attempt used by trainer: learned top32.
- Trained one balanced logistic ranker per failure type.
- Failure types with trained models: `imported_premise_missing`, `missing_bridge`, `type_mismatch`, `rewrite_direction`, `typeclass_missing`.
- Initially solved training goals skipped by second-stage training: 818.

核心结果：

| Method | Success | FFR | Avg premises | 结论 |
|---|---:|---:|---:|---|
| `learned_rerank` | 64.2% | 0.0% | 56.0 | static learned retriever |
| `learned_expansion` | 84.0% | 67.7% | 57.7 | pure learned expansion |
| `rule_far_learned` | 84.4% | 68.5% | 57.4 | simple failure wrapper |
| `learned_base_fallback` | 87.0% | 73.8% | 57.6 | strongest non-FAR fallback |
| `rule_far_learned_failure_specific` | 87.0% | 73.8% | 57.0 | hand-written controller |
| `rule_far_learned_second_stage` | 92.4% | 84.7% | 53.9 | learned failure-conditioned controller |
| `rule_far_full` | 55.6% | 55.0% | 86.6 | old oracle-tag hand controller |

阶段结论：

- 这是当前最强正结果：second-stage controller 比 `learned_base_fallback` 高 +5.4 success points、+10.9 FFR，同时 avg premises 更少。
- 这削弱了“只是 learned retriever + fallback”的审稿攻击。
- 结果仍是 trace-core recovery，不能直接写成完整 proof reconstruction success。

### 5.5 Split-Stability Fold0

Canonical outputs:

- `outputs/phase3_learned_eval_fold0_goals_500.jsonl`
- `outputs/phase3_learned_retriever_model_fold0_1500_500.json`
- `outputs/phase3_second_stage_eval_fold0_goals_500.jsonl`
- `outputs/phase3_second_stage_controller_model_fold0_1500_500.json`
- `outputs/phase3_second_stage_controller_eval_fold0_500_a40.json`
- `outputs/phase3_second_stage_controller_eval_fold0_500_a40.md`

Fold0 protocol:

- Fold0 uses the original first 500 imported-core goals as heldout.
- The remaining 1500 goals are used to retrain both learned retriever and second-stage controller.
- This is a split-stability check, not a full k-fold variance table.

Retriever audit on fold0:

| Ranker | All-core@32 | All-core@56 | All-core@96 | Mean core recall@96 |
|---|---:|---:|---:|---:|
| `base_score` | 1.2% | 1.4% | 3.0% | 25.5% |
| `learned_score` | 50.4% | 63.4% | 79.0% | 94.1% |

核心结果：

| Method | Original success | Fold0 success | Fold0 FFR | Fold0 avg premises |
|---|---:|---:|---:|---:|
| `learned_expansion` | 84.0% | 79.0% | 57.7% | 58.4 |
| `learned_base_fallback` | 87.0% | 83.6% | 66.9% | 57.7 |
| `rule_far_learned_failure_specific` | 87.0% | 83.4% | 66.5% | 56.8 |
| `rule_far_learned_second_stage` | 92.4% | 91.6% | 83.1% | 54.3 |

阶段结论：

- Fold0 对 learned retriever 更难：`learned_expansion` 从 84.0% 掉到 79.0%。
- Second-stage controller 几乎稳住：92.4% -> 91.6%。
- Fold0 中 second-stage 比 fallback 高 +8.0 success points、+16.2 FFR，并且 avg premises 更少。
- split artifact 风险下降；下一步重点转为 bridge failure taxonomy 和更广泛 replay 验证。

### 5.5.1 Feedback-Causality Gate 0

Purpose:

- Test whether the observed first-failure type causally affects the learned second-stage controller.
- Keep the first attempt and scored candidates fixed, then compare the true failure-conditioned policy against controls that ignore, fix, cycle, or shuffle the failure type used for second-stage scoring.
- This is still trace-core recovery, not kernel-verified theorem proving.

Canonical outputs:

- `outputs/phase3_feedback_causality_original_500.json`
- `outputs/phase3_feedback_causality_fold0_500.json`
- `outputs/phase3_feedback_causality_fold1_500.json`
- `outputs/phase3_feedback_causality_fold2_500.json`
- `outputs/phase3_feedback_causality_gate0.md`

Aggregate result over 4 heldout 500-goal splits:

| Policy | Goals | Success | FFR | Avg premises | Interpretation |
|---|---:|---:|---:|---:|---|
| `learned_base_fallback` | 2000 | 86.4% | 70.7% | 55.9 | strongest failure-agnostic control in this test |
| `rule_far_learned_second_stage` | 2000 | 92.5% | 84.0% | 52.5 | true observed failure type |
| `rule_far_learned_second_stage_fixed_imported` | 2000 | 82.8% | 62.9% | 55.9 | fixed imported-premise score; ignores observed failure |
| `rule_far_learned_second_stage_fixed_bridge` | 2000 | 81.3% | 59.8% | 54.9 | fixed bridge score; ignores observed failure |
| `rule_far_learned_second_stage_fixed_type` | 2000 | 81.3% | 59.8% | 55.2 | fixed type-mismatch score; ignores observed failure |
| `rule_far_learned_second_stage_cyclic` | 2000 | 79.4% | 55.7% | 55.8 | deterministic wrong failure-type score |
| `rule_far_learned_second_stage_shuffled` | 2000 | 85.0% | 67.9% | 55.5 | seeded random failure-type score |

Stage conclusion:

- Gate 0 passes in the current trace-core setting: true failure-conditioned scoring beats the best control by +6.2 success points and +13.3 FFR points, while using fewer premises.
- The gain is not explained by simply retrying with a generic learned fallback or by using any arbitrary second-stage expert.
- First-attempt failures are not completely single-type: across splits the heldout sets include `imported_premise_missing`, `missing_bridge`, `type_mismatch`, `rewrite_direction`, and `typeclass_missing`.
- This supports the proxy claim that failure transcript content carries conditional information for premise recovery. It does not yet establish the oral-level claim, because Gate 1 must still show that explicit premise interventions causally change a kernel-verified LeanHammer/prover outcome.

### 5.6 Phase 3 Bridge Replay

Canonical outputs:

- `outputs/phase3_bridge_goals_100.jsonl`
- `outputs/phase3_bridge_manifest_100.json`
- `outputs/phase3_bridge_replay_100.json`
- `outputs/phase3_bridge_report_100.md`

Bridge protocol:

- Sample: 100 disagreement-heavy imported-core heldout goals from the Phase 3D eval split.
- Replay success of original traced tactic scripts: 59/100 (59.0%).
- Bridge success = trace-core proof-core recovered AND original tactic replay succeeds.
- Selected buckets: 35 `second_stage_over_fallback`, 20 `second_stage_over_expansion`, 8 `fallback_over_second_stage`, 20 `both_fail`, 10 `both_success`, 7 fallback fill.
- Missing replay metadata: 0.

核心结果：

| Method | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|---:|
| `learned_rerank` | 100 | 14.0% | 11.0% | 0.0% | 56.0 |
| `learned_expansion` | 100 | 37.0% | 24.0% | 18.0% | 88.0 |
| `rule_far_learned` | 100 | 39.0% | 25.0% | 19.1% | 88.0 |
| `learned_base_fallback` | 100 | 45.0% | 31.0% | 25.8% | 82.2 |
| `rule_far_learned_failure_specific` | 100 | 45.0% | 31.0% | 25.8% | 82.3 |
| `rule_far_learned_second_stage` | 100 | 72.0% | 47.0% | 43.8% | 79.4 |
| `rule_far_full` | 100 | 47.0% | 27.0% | 25.5% | 88.3 |

阶段结论：

- Phase 3 bridge subset 保留了 second-stage 的主要优势：bridge verified 比 fallback 高 +16.0 points，bridge FFR 高 +18.0 points。
- Second-stage 同时使用更少 premise：79.4 vs fallback 82.2。
- 这个结果直接削弱“trace-core gain 不能过 real Lean replay filter”的审稿攻击。
- 但 absolute bridge verified 只有 47.0%，且 sample 是 disagreement-heavy，不应写成完整 theorem proving success。
- replay failures 多为原 traced tactic script 在重建上下文中 lean_error；下一步需要 bridge failure taxonomy，区分 replay artifact 与 premise-selection failure。

### 5.7 Phase 3 Bridge Failure Taxonomy

Canonical outputs:

- `outputs/phase3_bridge_failure_taxonomy_100.json`
- `outputs/phase3_bridge_failure_taxonomy_100.md`

Purpose:

- Explain why Phase 3 bridge verified is 47.0% rather than closer to trace-core 72.0%.
- Separate replay/context fragility from true premise-selection misses.
- Identify strong positive replay-supported examples for the paper.

Summary:

| Item | Count | Interpretation |
|---|---:|---|
| Replay verified goals | 59/100 | original traced tactic script replays in Lean |
| Replay-verified second-stage-over-fallback gains | 20 | strongest positive bridge evidence |
| Replay-verified second-stage-over-expansion gains | 23 | second-stage gain also survives vs blind learned expansion |
| Replay-verified goals missed by second-stage trace-core | 12 | real premise-selection negative cases |
| Second-stage trace-core successes blocked by replay failure | 25 | likely replay/context fragility unless deeper inspection says otherwise |

Policy-level miss table:

| Policy | Trace success | Bridge verified | Replay-verified trace miss | Avg premises |
|---|---:|---:|---:|---:|
| `learned_expansion` | 37.0% | 24.0% | 35 | 88.0 |
| `learned_base_fallback` | 45.0% | 31.0% | 28 | 82.2 |
| `rule_far_learned_failure_specific` | 45.0% | 31.0% | 28 | 82.3 |
| `rule_far_learned_second_stage` | 72.0% | 47.0% | 12 | 79.4 |
| `rule_far_full` | 47.0% | 27.0% | 32 | 88.3 |

Primary replay taxonomy:

| Primary tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 59 | 59.0% |
| `replay_unknown_identifier` | 15 | 15.0% |
| `replay_other_lean_error` | 7 | 7.0% |
| `replay_unsolved_goals` | 5 | 5.0% |
| `replay_simp_no_progress` | 5 | 5.0% |
| `replay_typeclass` | 3 | 3.0% |
| `replay_type_mismatch` | 3 | 3.0% |
| `replay_tactic_failed` | 2 | 2.0% |
| `replay_sorry_context` | 1 | 1.0% |

Category-level insight:

- In `second_stage_over_fallback`, 20/35 goals are replay verified. These are the cleanest examples that second-stage creates real Lean-replayable wins over fallback.
- In `second_stage_over_expansion`, 13/20 goals are replay verified, and the outcome-level count gives 23 replay-supported wins over expansion overall.
- In `fallback_over_second_stage`, 4/8 goals are replay verified. These are the most important negative cases for controller/ranker debugging.
- In `both_fail`, 8/20 goals are replay verified. These are proof-core retrieval failures on genuinely replayable goals.

Stage conclusion:

- The bridge subset strengthens the paper: the main controller gain is not only trace-core; it survives a real Lean replay filter on 20 second-stage-over-fallback examples.
- The remaining bridge gap is mixed. Some failures are real premise-selection misses, but 25 cases are second-stage trace-core successes whose original tactic replay fails, which points to replay/context fragility.
- The next method-side check is a hybrid guardrail ablation: the bridge negative cases show that some missed cores are high-base-rank premises dropped by the failure-conditioned scorer.

### 5.8 Phase 3 Bridge Negative-Case Inspection

Canonical outputs:

- `outputs/phase3_bridge_negative_case_inspection_100.json`
- `outputs/phase3_bridge_negative_case_inspection_100.md`

Purpose:

- Inspect the 12 replay-verified goals where `rule_far_learned_second_stage` missed trace-core recovery.
- Separate candidate-pool ceiling, failure-conditioned rank miss, and fallback-core drop.
- Decide whether the next change should fix a bug, strengthen the model, or add a conservative guardrail.

Summary:

| Item | Count | Interpretation |
|---|---:|---|
| Unique replay-verified second-stage misses inspected | 12 | 4 fallback-over-second-stage + 8 both-fail |
| Candidate-pool miss cases | 0 | current negatives are not caused by missing candidates |
| Second-stage dropped a fallback-selected core premise | 7 | actionable controller weakness |
| Second-stage dropped an expansion-selected core premise | 0 | blind expansion is not the missing ingredient |
| Failure-conditioned rank miss | 10 | second-stage scorer often ranks the missed core too low |
| Budget/path miss with core ranked in top96 | 2 | some cases may be recoverable by retry-path/budget changes |

Missed-core rank stats:

| Rank source | Count | Median | Min | Max | Top64 | Top96 |
|---|---:|---:|---:|---:|---:|---:|
| best second-stage rank | 17 | 115.0 | 11 | 207 | 4 | 4 |
| learned rank | 17 | 125.0 | 99 | 231 | 0 | 0 |
| base rank | 17 | 9.0 | 1 | 221 | 12 | 13 |

Stage conclusion:

- This is not a candidate-generation ceiling: every missed proof-core premise is present in the candidate pool.
- The negative cases are mostly an interaction between imported-premise failures and scorer ranking. The first observed failure type is `imported_premise_missing` in all 12 cases.
- The strongest actionable insight is that the failure-conditioned scorer improves many positives, but can suppress high-base-rank premises that fallback keeps. This motivates a `second_stage + base guardrail` ablation, not an idea downgrade.

### 5.9 Phase 3 Guardrail Ablations

Canonical outputs:

- `outputs/phase3_guardrail_eval_500.json`
- `outputs/phase3_guardrail_eval_500.md`
- `outputs/phase3_guardrail_eval_fold0_500.json`
- `outputs/phase3_guardrail_eval_fold0_500.md`
- `outputs/phase3_final_guardrail_bridge_100.json`
- `outputs/phase3_final_guardrail_bridge_report_100.md`
- `outputs/phase3_final_guardrail_bridge_delta_100.md`
- `outputs/phase3_final_guardrail_delta_500.md`
- `outputs/phase3_final_guardrail_delta_fold0_500.md`
- Negative sweeps: `outputs/phase3_guardrail_smoke_bridge_100.md`, `outputs/phase3_guardrail_mix_bridge_100.md`, `outputs/phase3_guardrail_mix_strong_bridge_100.md`, `outputs/phase3_multi_expert_bridge_100.md`, `outputs/phase3_final_expert_guardrail_bridge_100.md`, `outputs/phase3_final_hybrid_guardrail_bridge_100.md`.

Policies tested:

- Hard base guardrail: small/default/wide.
- Soft base-score mix: alpha 0.25/0.5/1/2/4/8.
- Imported-failure multi-expert max and expert guardrails.
- Final-only base guardrail with top8/top16/top32 base rescue.
- Final-only hybrid base+expert guardrail.

Main result:

| Setting | Second-stage | Final base guardrail-8 | Delta |
|---|---:|---:|---:|
| Original heldout trace-core | 92.4% | 92.6% | +0.2 |
| Fold0 trace-core | 91.6% | 91.6% | +0.0 |
| Bridge subset trace-core | 72.0% | 73.0% | +1.0 |
| Bridge verified | 47.0% | 49.0% | +2.0 |
| Bridge FFR | 43.8% | 46.1% | +2.3 |

Delta analysis:

- Bridge 100: final base guardrail-8 has 4 new-only solved cases and 3 base-only solved cases versus the original second-stage policy.
- All 4 new-only solved bridge cases are replay verified: `Nat.Primes.PNat.Prime.ne_one`, `WeierstrassCurve.Jacobian.addY_neg`, `WeierstrassCurve.Jacobian.neg_of_Z_ne_zero`, and `equicontinuousWithinAt_iInf_rng`.
- Among the 3 lost bridge cases, 2 are replay verified and 1 is replay failed; this explains the bridge verified net gain of +2.
- Original heldout: 4 new-only solved and 3 base-only solved, giving 92.6% vs 92.4%.
- Fold0: 3 new-only solved and 3 base-only solved, giving a stable 91.6%.

Four-split stability:

Canonical outputs:

- `outputs/phase3_second_stage_controller_eval_fold1_500.json`
- `outputs/phase3_second_stage_controller_eval_fold1_500.md`
- `outputs/phase3_second_stage_controller_eval_fold2_500.json`
- `outputs/phase3_second_stage_controller_eval_fold2_500.md`
- `outputs/phase3_split_stability_summary_4x500.json`
- `outputs/phase3_split_stability_summary_4x500.md`

| Split | Fallback success | Second-stage success | Final base guardrail-8 success |
|---|---:|---:|---:|
| original | 87.0% | 92.4% | 92.6% |
| fold0 | 83.6% | 91.6% | 91.6% |
| fold1 | 86.0% | 92.2% | 93.4% |
| fold2 | 88.8% | 94.0% | 94.0% |
| mean | 86.3% | 92.5% | 92.9% |

The final base guardrail-8 is stable across all four 500-goal splits: mean success 92.9% with 0.9-point population standard deviation, compared with 86.3% for `learned_base_fallback`.

Final bridge taxonomy:

Canonical outputs:

- `outputs/phase3_final_guardrail_bridge_eval_full_100.json`
- `outputs/phase3_final_guardrail_bridge_report_full_100.md`
- `outputs/phase3_final_guardrail_bridge_failure_taxonomy_100.json`
- `outputs/phase3_final_guardrail_bridge_failure_taxonomy_100.md`
- `outputs/phase3_final_guardrail_bridge_negative_case_inspection_100.json`
- `outputs/phase3_final_guardrail_bridge_negative_case_inspection_100.md`

| Item | Original second-stage | Final base guardrail-8 |
|---|---:|---:|
| Bridge trace-core success | 72.0% | 73.0% |
| Bridge verified | 47.0% | 49.0% |
| Bridge FFR | 43.8% | 46.1% |
| Replay-verified trace misses | 12 | 10 |
| Fallback-core drop cases among replay-verified misses | 7 | 2 |

The final bridge inspection confirms that the guardrail targets the diagnosed failure mode: it reduces replay-verified misses and sharply reduces fallback-core drops without increasing candidate-pool misses.

Negative sweep conclusions:

- Hard guardrail is too aggressive: default/wide guardrails reduce bridge trace-core from 72.0% to 63.0%/60.0%.
- Soft base-score mixing is either inert at low alpha or harmful at high alpha.
- Multi-expert imported-failure routing is harmful when applied broadly: bridge trace-core drops to 62.0%.
- Final-only expert guardrails do not beat final base guardrail-8; b8+e4 only ties it, while larger expert insertion regresses.
- A larger expert-gate pilot also does not justify further work: final expert guardrail-16 drops original from 92.6% to 91.4%, fold0 from 91.6% to 91.0%, and bridge from 73.0% to 68.0% versus final base guardrail-8.

Stage conclusion:

- The best current update is `rule_far_learned_second_stage_final_base_guardrail_8`: keep the learned failure-conditioned controller unchanged for the first retry, then add a tiny high-base rescue only on the final retry.
- This is a small but useful ablation, not a wholesale method replacement. It supports the negative-case diagnosis that late high-base premises can rescue imported-core failures, while aggressive fallback or expert mixing hurts.

### 5.10 Phase 3 Trace-Core Failure Taxonomy

Canonical outputs:

- `outputs/phase3_second_stage_failure_taxonomy_500.json`
- `outputs/phase3_second_stage_failure_taxonomy_500.md`
- `outputs/phase3_second_stage_failure_taxonomy_fold0_500.json`
- `outputs/phase3_second_stage_failure_taxonomy_fold0_500.md`

Original heldout residual failures:

| Policy | Unsolved | Expert-misrouting signal | Best-expert top96 | Fallback solved but policy failed | Base-guardrail candidate |
|---|---:|---:|---:|---:|---:|
| `rule_far_learned_second_stage` | 38/500 | 19 | 20 | 8 | 6 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 37/500 | 16 | 19 | 6 | 2 |

Fold0 residual failures:

| Policy | Unsolved | Expert-misrouting signal | Best-expert top96 | Fallback solved but policy failed | Base-guardrail candidate |
|---|---:|---:|---:|---:|---:|
| `rule_far_learned_second_stage` | 42/500 | 28 | 22 | 5 | 4 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 42/500 | 25 | 22 | 3 | 1 |

Interpretation:

- The final base guardrail reduces the most direct fallback/base failure mode without changing the main behavior.
- Many remaining failures are still not candidate-pool failures: they are often `best_expert_top96` or `expert_misrouting_signal`, but broad multi-expert fixes hurt. This suggests the next serious method improvement should learn a calibrated expert-gating rule rather than manually mixing experts.
- The residual failure taxonomy is good paper material for limitations and future work: the method is strong, but coarse failure labels still underuse useful alternative expert scores.
- The expert-gate direction is not worth further hand-tuned experiments in this cycle. Residuals show theoretical headroom, but all naive expert-insertion policies tested so far are unstable or harmful.

### 5.11 Phase 3 Larger Bridge Replay

Canonical outputs:

- `outputs/phase3_bridge_goals_200.jsonl`
- `outputs/phase3_bridge_manifest_200.json`
- `outputs/phase3_bridge_replay_200.json`
- `outputs/phase3_bridge_report_200.md`
- `outputs/phase3_bridge_failure_taxonomy_200.json`
- `outputs/phase3_bridge_failure_taxonomy_200.md`
- `outputs/phase3_bridge_negative_case_inspection_200.json`
- `outputs/phase3_bridge_negative_case_inspection_200.md`

Bridge setting:

- Replay goals: 200
- Original traced tactic replay success: 124/200 (62.0%)
- Selected categories: 34 `second_stage_over_fallback`, 30 `second_stage_over_expansion`, 6 `fallback_over_second_stage`, 31 `both_fail`, 20 `both_success`, and 79 `fallback_fill`.
- Bridge success = trace-core proof-core recovered AND original tactic replay succeeds.

Main result:

| Policy | Goals | Trace-core success | Bridge verified | Bridge FFR | Avg premises |
|---|---:|---:|---:|---:|---:|
| `learned_expansion` | 200 | 60.0% | 38.5% | 24.5% | 72.8 |
| `learned_base_fallback` | 200 | 67.5% | 44.5% | 33.1% | 69.9 |
| `rule_far_learned_second_stage` | 200 | 81.0% | 52.5% | 44.6% | 66.2 |
| `rule_far_learned_second_stage_final_base_guardrail_8` | 200 | 81.5% | 53.5% | 46.0% | 66.2 |

Key deltas:

- Final-base8 improves bridge verified over fallback by +9.0 points and bridge FFR by +12.9 points, while using 3.6 fewer average premises.
- Final-base8 also improves over the original second-stage policy by +1.0 bridge-verified point and +1.4 bridge-FFR points.
- The replay subset contains 20 replay-verified `second_stage_over_fallback` wins and 32 replay-verified `second_stage_over_expansion` wins.

Failure taxonomy:

| Primary replay tag | Count | Rate |
|---|---:|---:|
| `replay_verified` | 124 | 62.0% |
| `replay_unknown_identifier` | 30 | 15.0% |
| `replay_other_lean_error` | 13 | 6.5% |
| `replay_typeclass` | 8 | 4.0% |
| `replay_unsolved_goals` | 7 | 3.5% |
| `replay_simp_no_progress` | 6 | 3.0% |
| `replay_tactic_failed` | 5 | 2.5% |
| `replay_type_mismatch` | 5 | 2.5% |
| `replay_sorry_context` | 2 | 1.0% |

Negative-case inspection:

| Item | Count | Interpretation |
|---|---:|---|
| Replay-verified trace misses inspected | 17 | final-base8 still misses some real-replay-valid proof cores |
| Candidate-pool miss cases | 0 | remaining misses are not a candidate-generation ceiling |
| Fallback-selected core drops | 2 | the final guardrail largely fixed the original fallback-drop weakness |
| Expansion-selected core drops | 3 | blind expansion contains some recoverable cores but is not reliable enough as the main policy |
| Failure-conditioned rank misses | 15 | remaining headroom is mostly ranking/model calibration, not hand-written routing |
| Missed-core best second-stage rank top96 | 2/19 | many misses sit below the attempted budget |
| Missed-core base rank top96 | 9/19 | base score still carries useful rescue signal in a minority of cases |

Stage conclusion:

- The larger bridge replay confirms that the Phase 3 effect survives a real Lean replay filter: final-base8 beats fallback by +9.0 bridge-verified points and beats the original second-stage by +1.0 point.
- The absolute bridge verified number, 53.5%, should not be written as full theorem-proving success. It is a disagreement-heavy bridge validation of premise recovery under replayable traced tactics.
- The strongest next claim is not "we solve proof reconstruction"; it is that failure-conditioned selection improves trace-supervised imported-premise recovery and that the improvement remains visible after replay filtering.
- No further hand-tuned guardrail/expert-mix experiments are justified by the 200-goal results. Remaining misses point to a learned/calibrated expert gate or richer failure observation, which belongs in future work unless we start a new method cycle.

## 6. 当前可写进论文的 Claim-Evidence

## 6A. Verified LeanHammer Gates After GPT Pro Pivot

Purpose:

- Test the upgraded route proposed by GPT Pro: verified adaptive premise interventions after a failed bounded LeanHammer call.
- Separate infrastructure/pipeline feasibility from Mathlib-scale paper evidence.

### Gate 1: Explicit LeanHammer Premise Intervention

Canonical outputs:

- `outputs/gate1_leanhammer_smoke_results.json`
- `outputs/gate1_leanhammer_smoke_report.md`
- `outputs/gate1_leanhammer_smoke_recheck.json`
- `outputs/gate1_leanhammer_smoke_recheck.md`

Protocol:

- Built LeanHammer on A40 with Lean 4.30.0.
- Used `hammer [premises]` with selector premise counts set to zero, so the explicit premise list is the controlled variable.
- Generated two minimal propositional LeanHammer goals and ran complete/missing/wrong/noisy premise variants.

Result:

| Goal | Complete premise set | Missing/wrong premise set | Extra-noise premise set | Conclusion |
|---|---:|---:|---:|---|
| `prop_chain3` | proved | search_fail | proved | premise list changes verified outcome |
| `prop_conjunction` | proved | search_fail | proved | premise list changes verified outcome |

Stage conclusion:

- Gate 1 passes for the minimal LeanHammer interface: explicit premise interventions can causally change a kernel-verified LeanHammer outcome.
- This is infrastructure evidence, not Mathlib-scale theorem-proving evidence.
- It justifies proceeding to action-grid/oracle-headroom experiments.

### Gate 2: Verified Action-Grid Headroom Pilot

Canonical outputs:

- `outputs/gate2_leanhammer_action_grid_100.json`
- `outputs/gate2_leanhammer_action_grid_100.md`
- `outputs/gate2_leanhammer_action_grid_500.json`
- `outputs/gate2_leanhammer_action_grid_500.md`
- `outputs/gate2_verified_policy_readout_500.md`

Protocol:

- Generated 500 synthetic LeanHammer first-failure goals.
- Each action was evaluated by an actual `lake env lean` / LeanHammer call, not by trace-core coverage.
- Action grid: `keep`, `shrink_050`, `shrink_075`, `expand_150`, `expand_200`, `base_rescue_8`, `base_rescue_16`, `second_stage_rescore`, `stop`.

500-goal result:

| Action / Policy | Verified success | Avg premises | Interpretation |
|---|---:|---:|---|
| `keep` | 0.0% | 3.0 | failed first attempt remains failed |
| `expand_150` | 20.0% | 5.0 | solves easy expansion family |
| `expand_200` | 40.0% | 6.0 | best static action |
| `base_rescue_8` | 20.0% | 11.0 | solves base-rescue family |
| `second_stage_rescore` | 20.0% | 11.0 | solves second-stage family |
| oracle adaptive action | 80.0% | 6.6 | per-goal best action |
| true feedback policy | 80.0% | 7.8 | synthetic feedback family selects action |
| masked best-static policy | 40.0% | 6.0 | best failure-agnostic static control |
| shuffled feedback policy | 27.6% | 7.7 | corrupted feedback control |

Stage conclusion:

- Gate 2 synthetic verified pilot passes: oracle adaptive and true-feedback action selection beat the best static action by +40.0 points.
- The result validates the experiment machinery and the core causal structure: action value depends on post-failure information.
- This must not be used as a paper main result because the goals are synthetic. The next necessary step is Mathlib-scale verified LeanHammer compatibility.

### Mathlib / LeanHammer Compatibility Check

Canonical outputs:

- `outputs/mathlib_leanhammer_compat_probe_v2.json`
- `outputs/mathlib_leanhammer_compat_probe_v2.md`

Finding:

- A40 has current `repos/mathlib4_current` on Lean 4.31.0.
- LeanHammer main/dev currently use Lean 4.30.0; no Lean 4.31 tag was found.
- Route A is now working: `repos/mathlib4_lean430` is pinned to Mathlib tag `v4.30.0` / commit `c5ea00351c28e24afc9f0f84379aa41082b1188f`, and imports together with LeanHammer commit `3ef50193c9e80f84930f8f400bfd3c097c5e1fd3`.
- Combined probe passes in one Lean 4.30 process: `import Mathlib`, `import Hammer`, `#check Nat.add_comm`, and `#check Hammer.evalHammer`.

Stage conclusion:

- The immediate toolchain blocker is solved for Mathlib 4.30 evaluation.
- The remaining paper-level blocker is no longer import compatibility; it is traced-corpus replay: the existing trace data was collected from current Mathlib 4.31, while the verified LeanHammer route currently runs on Mathlib 4.30.

### Mathlib-Context Gate 1: Explicit Premise Intervention

Canonical outputs:

- `outputs/gate1_mathlib_hammer_smoke.json`
- `outputs/gate1_mathlib_hammer_smoke.md`

Protocol:

- Combined Mathlib 4.30 + LeanHammer 4.30 environment.
- Eight Mathlib-context goals over `Nat`, `Int`, and `Set`.
- For each goal, ran complete / empty-or-missing / wrong-theorem / extra-noise variants.
- Backend control: `autoPremises := 0`, `aesopPremises := 0`, `grindPremises := 0`; selector trace shows selector premises are `[]`.

Result:

| Family | Goals | Variants | Expectation misses | Conclusion |
|---|---:|---:|---:|---|
| `Nat` arithmetic theorems | 6 | 24 | 0 | complete/noisy premise lists prove; empty/wrong fail |
| `Int.add_assoc` | 1 | 4 | 0 | same controlled intervention pattern |
| `Set.Subset.trans` context | 1 | 4 | 0 | missing/wrong trans premise fails; complete/noisy succeeds |

Stage conclusion:

- Mathlib-context Gate 1 passes: explicit `hammer [premises]` lists causally change kernel-verified LeanHammer outcomes in a real `import Mathlib` environment.
- This is stronger than the synthetic Gate 1, but still a controlled smoke, not a corpus-scale theorem benchmark.

### Mathlib-Context Gate 2: Verified Action-Grid Headroom

Canonical outputs:

- `outputs/gate2_mathlib_hammer_action_grid_10.json`
- `outputs/gate2_mathlib_hammer_action_grid_10.md`
- `outputs/gate2_mathlib_hammer_action_grid_100.json`
- `outputs/gate2_mathlib_hammer_action_grid_100.md`

Protocol:

- 100 generated Mathlib theorem-family goals, 900 action attempts.
- Every non-stop action is an actual Lean 4.30 + Mathlib 4.30 + LeanHammer call.
- First attempt is deliberately missing the required Mathlib theorem and fails for 100.0% of goals.
- Action grid: `keep`, `shrink_050`, `shrink_075`, `expand_150`, `expand_200`, `base_rescue_8`, `base_rescue_16`, `second_stage_rescore`, `stop`.

100-goal result:

| Action / Policy | Verified success | Interpretation |
|---|---:|---|
| `keep` | 0.0% | first failed premise set remains failed |
| `shrink_050` | 0.0% | shrinking cannot recover missing theorem |
| `shrink_075` | 0.0% | shrinking cannot recover missing theorem |
| `expand_150` | 20.0% | solves one expansion family |
| `expand_200` | 40.0% | best static action |
| `base_rescue_8` | 20.0% | solves base-rescue family |
| `base_rescue_16` | 20.0% | no gain over base-rescue-8 in this pilot |
| `second_stage_rescore` | 20.0% | solves second-stage family |
| oracle adaptive action | 80.0% | per-goal best action |
| true feedback policy | 80.0% | generated failure family selects correct action |
| shuffled feedback policy | 0.0% | corrupted feedback selects wrong action |

Stage conclusion:

- Mathlib-context Gate 2 theorem-family pilot passes: oracle/true feedback beat the best static action by +40.0 points under actual verified LeanHammer calls.
- This supports the route that action value can be conditional on failure information in a real Mathlib environment.
- It must still be scoped as a generated theorem-family pilot. The final paper main evidence still needs traced-corpus verified replay or a clearly justified Mathlib 4.30 evaluation corpus.

### Mathlib 4.30 Trace-Corpus Migration Preflight

Canonical outputs:

- `outputs/mathlib430_trace_corpus_preflight_500.json`
- `outputs/mathlib430_trace_corpus_preflight_500.md`
- `outputs/mathlib430_clean_trace_subset_500.jsonl`
- `outputs/mathlib430_clean_trace_subset_500.md`
- `outputs/mathlib430_standalone_elab_50.json`
- `outputs/mathlib430_standalone_elab_50.md`
- `outputs/mathlib430_pretheorem_patch_probe_3_v3.json`
- `outputs/mathlib430_pretheorem_patch_probe_3_v3.md`

Protocol:

- Audited existing `outputs/phase3_second_stage_eval_goals_500.jsonl` against Mathlib 4.30.
- Checked theorem/proof-core declaration existence with a single Mathlib 4.30 `#check` file.
- Checked original file paths against the Mathlib 4.30 repo.
- Flagged direct circular leakage where the target theorem itself appears in the candidate list.

Preflight result:

| Item | Count | Rate |
|---|---:|---:|
| goals checked | 500 | 100.0% |
| file exists in Mathlib 4.30 | 497 | 99.4% |
| theorem exists in Mathlib 4.30 | 494 | 98.8% |
| all proof-core names exist in Mathlib 4.30 | 498 | 99.6% |
| target theorem in proof core | 0 | 0.0% |
| target theorem in candidate list | 500 | 100.0% |
| clean goals after filtering | 490 | 98.0% |
| standalone elaboration probe | 4/50 | 8.0% |
| pre-theorem patch probe | 0/3 proved | harness runs; proof search/type mismatch remain |

Cleaning:

- Dropped 10 goals: 3 missing file, 6 missing theorem, 1 missing proof-core name.
- Removed the target theorem from candidate lists for the 490 retained goals.

Stage conclusion:

- Mathlib 4.31 to 4.30 name-level migration is mostly feasible for the 500-goal heldout trace corpus.
- The major replay risk is circular target-theorem leakage if we simply import all of Mathlib and use raw candidates; this is now explicitly cleaned.
- Simple standalone declaration elaboration is not enough: only 4/50 sampled cleaned goals elaborate after naive statement rewriting with `sorry`, mostly because real theorem statements depend on original file section variables, namespaces, typeclass context, local notation, or declaration shape.
- A first original-file/pre-theorem patch probe now runs without import/span failures after normalizing Mathlib 4.30 `module/public import` files into temporary non-module probe files. On 3 sample goals, it reaches Hammer/proof checking but gets 2 `search_fail` and 1 `type_mismatch`.
- The next necessary gate is to improve the pre-theorem action/premise/options design, then scale the patch replay beyond 3 goals.

### Mathlib 4.30 Replayable-Subset Diagnostics

Canonical outputs:

- `outputs/mathlib430_pretheorem_original_tactic_probe_10.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_10.md`
- `outputs/mathlib430_pretheorem_original_tactic_probe_50.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_50.md`
- `outputs/mathlib430_pretheorem_original_tactic_probe_100.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_100.md`
- `outputs/mathlib430_pretheorem_original_tactic_probe_300.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_300.md`
- `outputs/mathlib430_pretheorem_original_tactic_probe_490.json`
- `outputs/mathlib430_pretheorem_original_tactic_probe_490.md`
- `outputs/mathlib430_replayable300_goal_ids.txt`
- `outputs/mathlib430_replayable300_splits.json`
- `outputs/mathlib430_replayable490_goal_ids.txt`
- `outputs/mathlib430_replayable490_splits.json`
- `analysis/mathlib430_replay300_failure_taxonomy.md`
- `outputs/mathlib430_pretheorem_hammer_matrix_replayable3.json`
- `outputs/mathlib430_pretheorem_hammer_matrix_replayable3.md`
- `outputs/mathlib430_pretheorem_action_matrix_replayable10.json`
- `outputs/mathlib430_pretheorem_action_matrix_replayable10.md`
- `outputs/mathlib430_pretheorem_action_matrix_replayable25.json`
- `outputs/mathlib430_pretheorem_action_matrix_replayable25.md`
- `outputs/mathlib430_pretheorem_action_matrix_replayable48.json`
- `outputs/mathlib430_pretheorem_action_matrix_replayable48.md`
- `outputs/mathlib430_pretheorem_action_matrix_rewrite48.json`
- `outputs/mathlib430_pretheorem_action_matrix_rewrite48.md`
- `outputs/mathlib430_pretheorem_action_matrix_targeted48.json`
- `outputs/mathlib430_pretheorem_action_matrix_targeted48.md`
- `outputs/mathlib430_pretheorem_action_matrix_scaled143.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled143.md`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_extra87_v2.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_extra87_v2.md`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_merged.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_merged.md`
- `outputs/mathlib430_action_routing_policy_gate_status_rule.json`
- `outputs/mathlib430_action_routing_policy_gate_status_rule.md`
- `outputs/mathlib430_action_routing_policy_gate_scaled230.json`
- `outputs/mathlib430_action_routing_policy_gate_scaled230.md`
- `outputs/mathlib430_budgeted_action_policy_scaled230.json`
- `outputs/mathlib430_budgeted_action_policy_scaled230.md`
- `analysis/mathlib430_strict_action_taxonomy_scaled230.json`
- `analysis/mathlib430_strict_action_taxonomy_scaled230.md`
- `outputs/mathlib430_pretheorem_action_matrix_extended230_part0.json`
- `outputs/mathlib430_pretheorem_action_matrix_extended230_part0.md`
- `outputs/mathlib430_pretheorem_action_matrix_extended230_part1.json`
- `outputs/mathlib430_pretheorem_action_matrix_extended230_part1.md`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_extended_merged.json`
- `outputs/mathlib430_pretheorem_action_matrix_scaled230_extended_merged.md`
- `outputs/mathlib430_budgeted_action_policy_scaled230_extended.json`
- `outputs/mathlib430_budgeted_action_policy_scaled230_extended.md`
- `analysis/mathlib430_strict_action_taxonomy_scaled230_extended.json`
- `analysis/mathlib430_strict_action_taxonomy_scaled230_extended.md`
- `analysis/mathlib430_gate1_replayable_hammer_readout.md`
- `analysis/mathlib430_scaled143_action_matrix_readout.md`

Original-tactic replay scaling:

| Item | Count |
|---|---:|
| cleaned trace goals probed | 10 |
| original tactic replay verified | 3 |
| scaled cleaned trace goals probed | 50 |
| scaled original tactic replay verified | 25 |
| larger cleaned trace goals probed | 100 |
| larger original tactic replay verified | 48 |
| newest cleaned trace goals probed | 300 |
| newest original tactic replay verified | 143 |
| full cleaned trace goals probed | 490 |
| full original tactic replay verified | 230 |

300-goal replay status counts:

| Status | Count |
|---|---:|
| `verified` | 143 |
| `unknown_identifier` | 59 |
| `tactic_fail` | 36 |
| `type_mismatch` | 22 |
| `parse_error` | 11 |
| `typeclass_or_inference` | 9 |
| `rewrite_fail` | 8 |
| `invalid_source_span` | 7 |
| `simp_fail` | 3 |
| `no_by_proof_marker` | 2 |

Replay-verified goals:

- `mathlib4::Module.rank_tensorProduct'`
- `mathlib4::FirstOrder.Language.definableFun_const`
- `mathlib4::MeasureTheory.Measure.compProd_apply_univ`

Hammer matrix on the 3 replay-verified goals:

| Item | Count |
|---|---:|
| Hammer attempts | 90 |
| verified Hammer attempts | 8 |
| goals with at least one Hammer proof | 1 |

Goal-level result:

| Goal | Verified Hammer Attempts | Best Attempt |
|---|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 8 | `empty` / `aesop_10` / 0 premises |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 0 | none |

Stage conclusion:

- This is a partial Gate 1 pass: original-file/pre-theorem replay has real verified goals, and LeanHammer can prove at least one replayable traced theorem in this patched Mathlib 4.30 setup.
- It is not yet paper-level evidence. The current Hammer positive is an easy empty-premise proof, so it does not support a failure-aware premise-intervention claim.
- Broad candidate insertion is currently harmful: `learned16`, `base8`, and `proof_core_plus_learned8` produce many `unknown_identifier`, `lean_error`, and Aesop rule-interpretation failures.
- The next action space should distinguish how selected names are exposed to Lean: facts for `hammer [facts]`, simp lemmas for `simp`/`simpa` or `hammerCore [simp] [facts]`, and theorem-like facts for Aesop/Auto/Grind.
- Scaling original-tactic replay to 300 cleaned goals is stable: 143/300 replay in the Mathlib 4.30 pre-theorem context, almost identical to the first-100 replay rate. This supports using the 143-goal replayable subset for the next action-matrix scale-up.
- Scaling original-tactic replay to the full cleaned subset is stable: 230/490 replay in the Mathlib 4.30 pre-theorem context.
- The 143 replayable goals are exported to `outputs/mathlib430_replayable300_goal_ids.txt` and split with deterministic SHA256(goal_id) ordering into 85 train / 28 dev / 30 test goals in `outputs/mathlib430_replayable300_splits.json`.

Proof-action matrix on the first 25 replay-verified goals:

| Item | Count |
|---|---:|
| replayable goals evaluated | 25 |
| action attempts | 275 |
| verified attempts | 22 |
| non-empty-premise verified attempts | 17 |
| goals with any proof | 6 |
| goals with non-empty-premise proof | 6 |
| action-dependent goals | 3 |

Action-level readout:

| Action | Verified | Non-empty verified |
|---|---:|---:|
| `hammer_empty` | 3 | 0 |
| `hammer_core_facts` | 3 | 3 |
| `hammer_core_plus_learned` | 3 | 3 |
| `simp_core` | 2 | 2 |
| `simpa_core` | 2 | 2 |
| `hammerCore_core` | 1 | 1 |
| `hammerCore_core_plus_learned` | 2 | 2 |

Strict action-dependent positives:

| Goal | Empty Baseline | Passing Non-Empty Action | Readout |
|---|---|---|---|
| `MeasureTheory.Measure.compProd_apply_univ` | fails | `simp_core` / `simpa_core` with `Measure.compProd`, `SFinite` | facts must be exposed as simp lemmas, not Hammer facts |
| `Projectivization.logHeight_nonneg` | fails | `hammerCore_core_plus_learned` | mixed simp/fact interface with learned additions is useful |
| `Units.inv_mul_cancel_left` | fails or warns | `hammerCore_core` | core facts work when routed through `hammerCore [simp] [facts]` |

Scaled stage conclusion:

- The verified pivot should no longer be framed as Hammer-only premise selection. The stronger and better-supported route is proof-action routing: selected names must be exposed through the right Lean interface.
- The most useful counterintuitive result so far is that adding names as generic Hammer facts can fail, while the same or related names succeed as simp lemmas or `hammerCore` simp/fact inputs.
- This is still a pilot: 3 action-dependent goals out of 25 replayable goals is promising but not sufficient for a final main result. The next required scale is 50-100 replayable goals with a pre-registered action grid and empty-baseline accounting.

48-goal proof-action matrix:

| Item | Count / Rate |
|---|---:|
| replayable goals evaluated | 48 |
| action attempts | 528 |
| verified attempts | 30 |
| non-empty-premise verified attempts | 21 |
| goals with any proof | 8 / 48 |
| best static action | 5 / 48 |
| oracle action-grid headroom | 8 / 48 |
| oracle gap over best static | +3 goals / +6.25 pp |
| strict action-dependent goals | 3 |

48-goal strict action-dependent positives:

- `MeasureTheory.Measure.compProd_apply_univ`: `simp_core` / `simpa_core` succeeds where empty baselines fail.
- `Projectivization.logHeight_nonneg`: `hammerCore_core_plus_learned` succeeds where empty baselines fail.
- `Units.inv_mul_cancel_left`: `hammerCore_core` succeeds where empty baselines fail.

Negative action extension:

| Extension | Attempts | Verified | Main Failures |
|---|---:|---:|---|
| `simp only` + naive `rw` / `rw; simp` templates | 288 | 0 | 197 `rewrite_fail`, 64 `simp_fail`, 24 `sorry_warning` |

Targeted typed action extension:

| Extension | Attempts | Verified | Goals With Proof | New Strict Positives |
|---|---:|---:|---:|---:|
| `simp_all`, `simp_rw`, `solve_by_elim` families | 288 | 8 | 4 / 48 | 2 |

New targeted positives:

| Goal | Passing Action | Premise Interface | Readout |
|---|---|---|---|
| `rTensor.inverse_comp_rTensor` | `solve_by_elim_core` | 3 fact names: `LinearMap.range`, `rTensor.inverse`, `rTensor.inverse_of_rightInverse_comp_rTensor` | compact elimination facts prove where prior grid failed |
| `SkewMonoidAlgebra.sum_mul` | `solve_by_elim_core` | 4 fact names: `Finset.sum_mul`, `NonUnitalNonAssocSemiring`, `SkewMonoidAlgebra`, `SkewMonoidAlgebra.sum` | typeclass/structure names can be useful through elimination rather than Hammer facts |

Combined 48-goal proof-action readout:

| Item | Count / Rate |
|---|---:|
| replayable goals evaluated | 48 |
| main + targeted action attempts | 816 |
| goals with any proof | 10 / 48 |
| best static action | 5 / 48 |
| oracle action-grid headroom | 10 / 48 |
| oracle gap over best static | +5 goals / +10.42 pp |
| strict action-dependent goals | 5 |

48-goal conclusion:

- The replayable-subset proof-action grid passes a small but now clearer oracle-headroom gate: oracle action choice solves 10/48 versus 5/48 for the best static action after adding targeted typed actions.
- The absolute success rate is still low. This should be framed as a verified pilot/gate result, not the final main experiment.
- Naive rewrite templates are not worth more blind scaling. Future gains should come from better action taxonomy, stronger candidate typing, local-context-aware filtering, and learned routing over the successful action families.
- `solve_by_elim` is now a confirmed useful action family and should be included in the next scaled matrix; `simp_rw` has no positive evidence so far.

143-goal scaled proof-action matrix:

| Item | Count / Rate |
|---|---:|
| replayable goals evaluated | 143 |
| action attempts | 2145 |
| verified attempts | 150 |
| non-empty-premise verified attempts | 124 |
| goals with any proof | 35 / 143 |
| goals with non-empty-premise proof | 35 / 143 |
| best static action | 19 / 143 (`hammer_core_plus_learned`) |
| empty baseline | 18 / 143 (`hammer_empty`) |
| oracle action-grid headroom | 35 / 143 |
| oracle gap over best static | +16 goals / +11.19 pp |
| strict action-dependent goals | 17 |

Scaled conclusion:

- The 48-goal pilot is confirmed at larger replayable-subset scale: strict action-dependent goals increase from 5 to 17.
- The strongest verified result is now typed proof-action routing, not Hammer-only premise selection.
- The next paper-critical step is a learned or rule-based policy on the prepared 85/28/30 split, evaluated against best static, empty-only, fixed portfolio, and shuffled/masked controls.
- This is still not full theorem proving over all Mathlib trace goals: it is kernel-verified proof-action success on the replayable Mathlib 4.30 subset.

230-goal merged proof-action matrix:

| Item | Count / Rate |
|---|---:|
| replayable goals evaluated | 230 |
| action attempts | 3450 |
| verified attempts | 246 |
| non-empty-premise verified attempts | 205 |
| goals with any proof | 51 / 230 |
| goals with non-empty-premise proof | 51 / 230 |
| best static action | 31 / 230 (`hammer_core_plus_learned`) |
| empty baseline | 29 / 230 (`hammer_empty`) |
| oracle action-grid headroom | 51 / 230 |
| oracle gap over best static | +20 goals / +8.70 pp |
| strict action-dependent goals | 22 |

230-goal conclusion:

- The scaled signal remains positive on the full replayable heldout subset: oracle 51/230 versus best static 31/230.
- Strict action-dependent wins rise to 22 goals, spanning `simp`, `simp_all`, `hammerCore`, `hammer`, and `solve_by_elim` interfaces.
- The additional 87 replayable goals are not just easy empty-baseline wins; they add 5 strict action-dependent goals and preserve the typed-interface story.

Initial routing-policy gate:

| Method | Train | Dev | Test | All |
|---|---:|---:|---:|---:|
| `hammer_empty` only | 11/85 | 4/28 | 3/30 | 18/143 |
| best single action | 12/85 | 4/28 | 3/30 | 19/143 |
| `hammer_empty` -> best fixed second action | 18/85 | 7/28 | 4/30 | 29/143 |
| `hammer_empty` -> coarse status rule | 18/85 | 7/28 | 4/30 | 29/143 |
| `hammer_empty` -> text NB policy | 21/85 | 8/28 | 4/30 | 33/143 |
| oracle action grid | 21/85 | 9/28 | 5/30 | 35/143 |

5-fold out-of-fold policy check:

| Method | Success |
|---|---:|
| `hammer_empty` only | 18/143 |
| train-selected best single action | 12/143 |
| `hammer_empty` -> train-selected best fixed second action | 29/143 |
| `hammer_empty` -> coarse status rule | 25/143 |
| `hammer_empty` -> text NB policy | 28/143 |
| oracle action grid | 35/143 |

Policy-gate conclusion:

- Current low-capacity adaptive policies do not beat the best fixed second action out of fold.
- The strongest control is a fixed typed portfolio: `hammer_empty`, `hammerCore_core_plus_learned`, `hammer_core_plus_learned`, `simp_all_core_plus_learned`, `solve_by_elim_core` reaches 35/143 on this grid, matching oracle with five total attempts.
- This pushes the next method question toward low-budget routing: can a learned transcript/goal/action policy match the 3-4 action portfolio with only one second action, or is the right paper story a typed proof-action portfolio under compute tradeoffs?

230-goal routing-policy gate:

| Method | 5-fold OOF Success |
|---|---:|
| `hammer_empty` only | 29 / 230 |
| train-selected best single action | 29 / 230 |
| `hammer_empty` -> best fixed second action | 38 / 230 |
| `hammer_empty` -> coarse status rule | 40 / 230 |
| `hammer_empty` -> text NB policy | 41 / 230 |
| oracle action grid | 51 / 230 |

230-goal portfolio control:

| Fixed Schedule After `hammer_empty` | Success |
|---|---:|
| `hammerCore_core_plus_learned` | 41 / 230 |
| + `simp_all_core_plus_learned` | 48 / 230 |
| + `solve_by_elim_core` | 50 / 230 |

230-goal policy conclusion:

- The low-budget policies show weak positive movement in 5-fold OOF (text NB 41/230 vs fixed second 38/230), but the heldout test split still only ties the fixed second action.
- A fixed two-action typed portfolio after `hammer_empty` reaches 48/230, very close to the 51/230 oracle; this is the main control any adaptive claim must beat under matched compute.
- Current evidence supports typed proof-action diversity more strongly than learned adaptive routing.

Budgeted policy gate:

| Retry budget after `hammer_empty` | Fixed greedy portfolio | Pure NB | Pure kNN | Fixed-prefix + residual NB | Fixed-prefix + residual kNN | Oracle |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 38 / 230 | 37 / 230 | 34 / 230 | 37 / 230 | 34 / 230 | 51 / 230 |
| 2 | 48 / 230 | 38 / 230 | 35 / 230 | 45 / 230 | 46 / 230 | 51 / 230 |
| 3 | 48 / 230 | 43 / 230 | 41 / 230 | 50 / 230 | 48 / 230 | 51 / 230 |
| 4 | 50 / 230 | 45 / 230 | 46 / 230 | 50 / 230 | 50 / 230 | 51 / 230 |

Strict-goal budgeted readout:

| Retry budget after `hammer_empty` | Fixed greedy strict hits | Residual NB strict hits | Residual kNN strict hits | Oracle |
|---:|---:|---:|---:|---:|
| 1 | 9 / 22 | 8 / 22 | 5 / 22 | 22 / 22 |
| 2 | 19 / 22 | 16 / 22 | 17 / 22 | 22 / 22 |
| 3 | 19 / 22 | 21 / 22 | 19 / 22 | 22 / 22 |
| 4 | 21 / 22 | 21 / 22 | 21 / 22 | 22 / 22 |

Budgeted-gate conclusion:

- The richer offline policy gate does not produce a clean one-retry adaptive win. At K=2, fixed greedy remains stronger than residual NB/kNN.
- There is a useful K=3 residual-NB signal: 50/230 OOF overall and 21/22 strict hits, but this is not enough to claim adaptive routing beats the typed portfolio because fixed K=4 also reaches 50/230 and the oracle is only 51/230.
- The main-method decision is now sharper: either extended action families raise the oracle ceiling, or the paper should pivot toward compute-budgeted typed proof-action portfolios and treat adaptive routing as a secondary or optional component.

Strict action-interface taxonomy:

| Family | Strict goals solved |
|---|---:|
| `hammerCore` | 12 / 22 |
| `simp_all` | 12 / 22 |
| `simp` | 11 / 22 |
| `simpa` | 11 / 22 |
| `solve_by_elim` | 5 / 22 |
| `hammer` | 2 / 22 |

Only-family strict cases:

| Family | Only-family goals |
|---|---:|
| `hammerCore` | 6 |
| `solve_by_elim` | 2 |
| `hammer` | 1 |

Taxonomy conclusion:

- The strict positives are not explainable as "just add more premises." Different Lean interfaces solve partially disjoint subsets.
- `hammerCore` is the largest only-family bucket, while `solve_by_elim` has two only-family wins. This supports a stronger method story around typed exposure/routing of evidence.

Extended action-family run:

| Metric | Previous scaled230 | Extended scaled230 |
|---|---:|---:|
| attempts | 3450 | 7130 |
| verified attempts | 246 | 506 |
| non-empty-premise verified attempts | 205 | 432 |
| oracle goals | 51 / 230 | 58 / 230 |
| best static action | `hammer_core_plus_learned` | `aesop_core_plus_learned` |
| best static goals | 31 / 230 | 38 / 230 |
| strict action-dependent goals | 22 | 29 |

Extended best actions:

| Action | Verified goals |
|---|---:|
| `aesop_core_plus_learned` | 38 |
| `aesop_core_plus_learned16` | 37 |
| `hammer_core_plus_learned16` | 32 |
| `hammer_core_plus_learned32` | 32 |
| `hammer_core_plus_learned` | 31 |

New oracle goals from the extended run:

- `AlgebraicGeometry.IsClosedImmersion.eq_proper_inf_monomorphisms`: `aesop_core_plus_learned`, `aesop_core_plus_learned16`
- `BoxIntegral.Box.MeasureTheory.Measure.BoxIntegral.Box.volume_apply`: `aesop_core_plus_learned`, `aesop_core_plus_learned16`
- `NormedAddCommGroup.summable_imp_tendsto_of_complete`: `aesop_core_plus_learned`, `aesop_core_plus_learned16`
- `RatFunc.InftyValuation.map_mul'`: `aesop_core_plus_learned`, `aesop_core_plus_learned16`
- `Real.sign_apply_eq`: `aesop_core_plus_learned`, `aesop_core_plus_learned16`
- `isMinOn_Ioi_of_deriv`: `hammer_core_plus_learned16`, `hammer_core_plus_learned32`
- `mem_balancedCore_iff`: `aesop_core_plus_learned`, `aesop_core_plus_learned16`

Extended budgeted policy gate:

| Retry budget after `hammer_empty` | Fixed greedy OOF | Residual NB OOF | Residual kNN OOF | Oracle |
|---:|---:|---:|---:|---:|
| 1 | 49 / 230 | 34 / 230 | 44 / 230 | 58 / 230 |
| 2 | 55 / 230 | 51 / 230 | 54 / 230 | 58 / 230 |
| 3 | 55 / 230 | 55 / 230 | 55 / 230 | 58 / 230 |
| 4 | 57 / 230 | 55 / 230 | 57 / 230 | 58 / 230 |
| 5 | 57 / 230 | 57 / 230 | 57 / 230 | 58 / 230 |

Full Aesop-ablation budgeted policy gate:

| Retry budget after `hammer_empty` | Fixed greedy OOF | Residual NB OOF | Residual kNN OOF | Oracle |
|---:|---:|---:|---:|---:|
| 1 | 49 / 230 | 29 / 230 | 44 / 230 | 58 / 230 |
| 2 | 55 / 230 | 50 / 230 | 54 / 230 | 58 / 230 |
| 3 | 55 / 230 | 55 / 230 | 55 / 230 | 58 / 230 |
| 4 | 57 / 230 | 55 / 230 | 57 / 230 | 58 / 230 |
| 5 | 57 / 230 | 57 / 230 | 57 / 230 | 58 / 230 |
| 6 | 57 / 230 | 57 / 230 | 57 / 230 | 58 / 230 |

Extended taxonomy:

| Family | Strict goals solved |
|---|---:|
| `aesop` | 20 / 29 |
| `hammerCore` | 12 / 29 |
| `simp_all` | 12 / 29 |
| `simp` | 11 / 29 |
| `simpa` | 11 / 29 |
| `solve_by_elim` | 5 / 29 |
| `hammer` | 3 / 29 |

Extended conclusion:

- This is a real improvement, not just more attempts: the oracle increases by +7 goals and strict action-dependent goals increase by +7.
- `aesop` is now the strongest single interface and supplies 6 new oracle goals, making "typed exposure through the right Lean interface" a much harder and clearer mainline.
- Generic arithmetic tactics did not help: `omega`, `linarith`, `nlinarith`, and `ring_nf` each have 0 verified goals; `norm_num_empty` only has 4 empty/default-style successes.
- Adaptive routing remains secondary: fixed typed portfolios are still the hard baseline, reaching 55/230 OOF with two retries and 57/230 OOF with four/five retries.

Focused Aesop ablation:

| Aesop variant group | Goals solved by at least one action |
|---|---:|
| `core+learned8` | 41 / 230 |
| `core+learned16` | 41 / 230 |
| `aesop_empty` / other | 29 / 230 |
| `core` | 7 / 230 |
| `core+learned32` | 7 / 230 |
| `learned8/16/32` only | 7 / 230 |

| Exposure | Goals solved by at least one action |
|---|---:|
| facts+simps | 38 / 230 |
| facts-only | 5 / 230 |
| simps-only | 4 / 230 |

Aesop-ablation conclusion:

- The ablation adds no new oracle goals over the extended 58/230 matrix, so it is a mechanism result rather than a ceiling improvement.
- The evidence is still valuable: Aesop succeeds when selected names are exposed jointly as facts and simp lemmas; stripping either channel collapses success.
- `core+learned32` is much worse than `core+learned8/16`, which is a useful anti-more-premises result in the real Lean backend.
- Final method wording should emphasize typed evidence exposure and small-budget portfolios, not blind premise expansion or a currently unproven adaptive router.


| Claim | Evidence | Status |
|---|---|---|
| Failure feedback helps beyond static retrieval in local Mathlib trace-core recovery | Phase 1 2k: `rule_far_no_core_tags` 95.7% vs `visible_feature_rerank` 86.5% | supported |
| Blindly adding premises can hurt under timeout pressure | Phase 2 timeout: `topk_equal_budget` 43.8%, `one_shot` 57.0% | supported |
| Timeout failures need shrink / precision-oriented retry | `rule_far_no_core_timeout_shrink` 69.3% vs `topk_expansion` 59.7% | supported |
| Imported-core retrieval requires learned/global retrieval | Phase 3 initial: BM25 / controlled iterative lexical proxy around 12%, learned expansion 84.0% | supported |
| Failure-conditioned second-stage control beats strong learned fallback | Phase 3D: 92.4% vs `learned_base_fallback` 87.0%; Phase 3E fold0: 91.6% vs 83.6% | strongly supported for trace-core |
| Phase 3 trace-core gains survive a real Lean replay filter | Phase 3 bridge 200: final-base8 bridge verified 53.5% vs fallback 44.5%; original second-stage 52.5%; 20 replay-verified second-stage-over-fallback wins | supported on disagreement-heavy subset |
| Mathlib 4.30 + LeanHammer 4.30 verified environment works | Combined import probe passes with `import Mathlib` and `import Hammer` in one Lean 4.30 process | supported for route-A evaluation |
| Explicit premise lists control Mathlib-context LeanHammer outcomes | Gate 1 Mathlib smoke: 8 goals / 32 variants, 0 expectation misses; selector premises `[]` | supported as verified smoke |
| Verified action-grid headroom exists in generated Mathlib theorem-family goals | Gate 2 Mathlib 100: oracle/true feedback 80.0%, best static 40.0%, first failure 100.0% | supported as generated verified pilot |
| Existing traced-corpus goals have a nonempty replayable subset in Mathlib 4.30 pre-theorem context | Original-tactic probe 10: 3/10 replay verified | supported as a small migration diagnostic |
| Current `hammer [facts]` route already yields premise-dependent traced-corpus wins | Hammer matrix replayable3: 8 verified attempts but all on one empty-premise-solvable goal | unsupported so far |
| Proof-action routing can produce action-dependent traced-corpus verified wins | Scaled230 merged action matrix: oracle 51/230 vs best static 31/230; 22 strict action-dependent goals; 246 verified attempts | supported as a scaled verified pilot |
| Typed proof-action portfolios are currently the strongest verified traced-corpus route | Full scaled230 matrix: oracle 58/230; fixed typed portfolio reaches 55/230 OOF at K=2 and 57/230 OOF at K=4; train-fitted K=4 reaches 58/230 | supported |
| Aesop gains require typed exposure, not just more names | Aesop ablation: facts+simps 38/230, facts-only 5/230, simps-only 4/230; core+learned32 falls to 7/230 group coverage | supported as mechanism evidence |
| Naive rewrite/simp-only template expansion helps the current replayable subset | Rewrite48: 0/288 verified; dominated by `rewrite_fail` / `simp_fail` | unsupported; stop this branch |
| Bridge negatives expose ranking/model-calibration headroom rather than a candidate-set ceiling | 200-goal negative inspection: 0/17 candidate-pool misses; 15/17 failure-conditioned rank misses; only 2 fallback-core drops remain | diagnosed; future method work |
| A tiny final retry base guardrail improves bridge-verified recovery without hurting split stability | Final base guardrail-8: mean 92.9% across four 500-goal splits vs second-stage 92.5% and fallback 86.3%; bridge 200 verified 53.5% vs original second-stage 52.5% | supported as a focused ablation |
| Current results imply full theorem proving success | Not yet; bridge is a replay-filtered subset, not a full proof reconstruction benchmark | unsupported / avoid |

## 7. Paper-Safe Wording

Recommended current wording:

> In imported-core Mathlib trace-core recovery, a learned second-stage controller conditioned on the first failed attempt improves over the strongest learned+base fallback across the original heldout split and alternate splits. A tiny final base-rescue guardrail preserves this trace-core stability, reaching 92.9% mean success across four 500-goal splits. On a 200-goal disagreement-heavy real Lean bridge subset, the final controller improves bridge verified success from 44.5% for learned+base fallback to 53.5%, while using fewer average premises. These results support failure feedback as a useful signal beyond static learned retrieval and failure-agnostic fallback, under trace-supervised premise selection.

Verified-pivot wording:

> We further validate action-conditional evidence allocation in a Mathlib 4.30 + LeanHammer 4.30 environment. On 230 replayable traced-corpus theorem contexts, a typed action grid reaches 58/230 oracle verified proofs versus 38/230 for the best single action. A fixed typed portfolio after `hammer_empty` reaches 55/230 under two retries and 57/230 under four retries out of fold, serving as the strongest matched-compute control. The central counterfactual is Aesop: under the same source budget, facts+simps exposure solves 38/230, facts-only solves 5/230, simps-only solves 4/230, and the single-channel union solves only 7/230. Broader 32-name facts+simps exposure drops to 3/230. These results support typed evidence allocation as the current verified mainline; learned adaptive allocation remains an open target.

Paper rewrite status:

- `iclr2027/paper.tex` now uses action-conditional evidence allocation as the main paper story: retrieved names must be compiled into Lean proof interfaces, not merely ranked.
- The draft treats fixed typed portfolios as strong matched-compute controls and avoids claiming learned adaptive allocation.
- The draft marks controlled lexical retrieval rows as proxies, not LeanSearch v2 reproductions.
- The draft marks trace-core and bridge experiments as supporting discovery evidence, not full theorem-proving claims.
- `analysis/paper_adversarial_review_typed_portfolio.md` records the current reviewer risks and next upgrade experiments.

Aesop counterfactual channel-control update:

- `analysis/mathlib430_aesop_counterfactual_controls.md` analyzes matched Aesop source/budget controls from the full scaled230 Aesop-ablation matrix.
- Best source is `core+learned8`: facts+simps solves 38/230, facts-only solves 5/230, simps-only solves 4/230.
- The union of the two single-channel controls solves only 7/230; facts+simps has 34 joint-only goals, so the result is not just a union of two weak channels.
- Exposure is sharply non-monotonic: `core+learned8` facts+simps solves 38/230, but `core+learned32` facts+simps solves 3/230 and loses 35 of the 38 top-8 successes.
- This is now the central mechanism evidence for the paper: retrieved evidence has to be assigned to the right interface channels.

Typed allocator/compression gate update:

- `outputs/mathlib430_typed_allocator_gate_scaled230_aesop_ablation.md` evaluates stronger learned allocators on the same 230-goal matrix and 5-fold OOF protocol.
- Fixed greedy remains the strongest practical control: K=2 reaches 55/230 OOF, and K=4 reaches 57/230 OOF.
- Pure logreg reaches 47/230 at K=4; unbalanced logreg reaches 49/230 at K=4; pure ComplementNB reaches 39/230 at K=4.
- Fixed-prefix residual logreg/CNB match fixed K=4 at 57/230 but do not beat or compress it to fewer retry slots.
- Readout: learned adaptive allocation remains outside the main claim; the paper should present fixed typed portfolios as hard controls and action-conditional evidence allocation as the supported mechanism.

E1 strict interface filtering update:

- `analysis/mathlib430_e1_strict_interface_filtering.md` compares the full scaled230 baseline against strict filtered variants of the five high-value actions.
- Strict filtering uses `strict_aesop` mode: Aesop safe facts are restricted to resolved theorem/lemma-like names, and simp channels are restricted to `@[simp]` or rewrite-tagged candidates.
- The result is negative for ceiling improvement: filtered-only oracle is 4/230, combined oracle remains 58/230, and no new oracle goals are added.
- The audit is still useful: 7321/7497 selected names are available, only 176 are unavailable, and target/alias hits are 24, so the current main effect is not primarily an unknown-identifier problem.
- The important boundary is that over-cleaning the interface destroys most Aesop successes. The paper should not claim a pure theorem-like/simp-attribute mechanism; it should describe the current result as a real Lean typed-exposure mechanism and report strict filtering as a robustness boundary.

Avoid:

- Do not claim full proof reconstruction success for Phase 3; bridge replay is a filtered subset validation, not a full benchmark.
- Do not present generated Mathlib theorem-family Gate 2 as the final corpus-scale main result.
- Do not describe `rule_far_full` as an absolute upper bound in learned imported-core experiments.
- Do not present Phase 3 initial no-core visible-feature result as competitive globally.
- Do not cite old tag-leak / early ablation artifacts as main evidence.
- Do not claim that adaptive routing beats the fixed typed portfolio; current verified evidence does not support that.

## 8. Current Open Risks

1. The learned retriever and second-stage controller use traced proof-core labels. The paper must frame this as trace-supervised premise selection unless we add a broader unsupervised or online setting.
2. Bridge replay is now a 200-goal disagreement-heavy subset, not a random full proof-reconstruction benchmark. This is enough for bridge validation, but the paper must not present it as end-to-end theorem proving.
3. The new verified Mathlib Gate 2 is generated theorem-family evidence. It validates mechanism and infrastructure, but traced-corpus verified replay is still needed before this can be the main paper result.
4. The replayable-subset action matrix is a positive scaled pilot but not yet an oral-level final method: 29 strict action-dependent goals and oracle 58/230 vs best static 38/230 support the route, but paper-level adaptive claims need a stronger learned or rule-based routing policy against fixed typed-portfolio controls.
5. External baseline coverage still needs tightening for the final paper: current iterative lexical rows are controlled proxies, not full LeanSearch v2; final related-work positioning must be precise.
6. Residual failures show many `best_expert_top96` cases, but naive multi-expert mixing hurts. This is future-work material, not a near-term hand-tuning target.
