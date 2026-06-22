# ICLR 2027 Idea Guide：Learning from Failed Proof Search

> 当前版本：2026-06-17 大改版  
> 项目定位：formal reasoning / neural-symbolic theorem proving / Lean hammer 方法论文  
> 目标会议：ICLR 2027 主会  
> 工作方式：本地 Windows 负责代码、分析、论文写作；服务器负责 Lean/Mathlib 实验、retriever/reranker 训练和大规模 prover calls。  
> 核心升级：本版不再把主线写成“failure-aware premise selection”这个普通增强，而是写成一个更强的闭环优化问题：**failed proof search is counterfactual supervision for premise optimization**。

---

## 0. 一句话版本

现有 Lean premise selectors 和 Lean hammers 通常把 premise selection 当成一次性检索问题：给定 goal，取 top-k premises，然后把它们交给 prover/hammer。这个默认假设太弱，而且在真实 proof search 中经常错：

> **失败后最优策略往往不是检索更多 premises，而是检索更少、更不同、更 reconstruction-friendly 的 premises。Proof failure 不是废样本，而是关于 premise coverage、search noise、reconstruction feasibility 的高信息反事实监督。**

推荐论文题目：

> **Learning from Failed Proof Search: Closed-Loop Premise Optimization for Lean Hammers**

备用题目：

> **When More Premises Hurt: Failure-Conditioned Premise Optimization for Lean Hammers**

系统名：

> **FAR-Hammer**：Failure-Aware Retrieval for Lean Hammers

---

## 1. 从 ICLR_1 迁移过来的论文工作法

`ICLR_1` 的关键经验不是“实验多”，而是它后期形成了一个强论文结构：

1. 一个重要问题。
2. 一个反直觉主张。
3. 一个证据层级，而不是一个孤立指标。
4. 一个理论框架，能解释为什么反直觉现象会出现。
5. 多组实验，每组实验只服务一个 claim。
6. 坏结果分流：bug / artifact、真实 insight、controlled boundary condition。
7. Claim-evidence map，防止 abstract/introduction 里的每句话没有实验支撑。
8. Adversarial review，提前站在严格 reviewer 角度攻击自己。
9. Table/figure audit，保证 JSON、图、表、caption 的数字一致。

这篇 Lean 论文要照这个模式推进。

`ICLR_1` 的 `R/V/A` 证据层级对应到本项目，不是照搬变量名，而是照搬思想：不要把一个 headline 指标当成全部证据。Lean 项目里至少要拆出三根轴：

| 轴 | 含义 | 为什么单独重要 |
|---|---|---|
| `P` Premise coverage | premise set 是否包含 proof core / useful premises | 只看 retrieval recall 容易高估方法 |
| `S` Search-space quality | premise set 是否让 hammer/prover 搜索可控、少 timeout、少 misleading premises | 更多 premise 可能伤害 search |
| `V` Verified success | Lean kernel 最终是否验证成功 | 最终目标，不能被 retrieval metric 代替 |

核心层级：

\[
P \nRightarrow S,\quad S \nRightarrow V,\quad \text{and failure traces help estimate both }P\text{ and }S.
\]

这就是本论文的证据骨架。不要写成“我们提升 recall”，而要写成：

> Premise coverage, search-space quality, and verified proof success are distinct axes. Failed proof search exposes the gap between them.

---

## 2. 最新竞争格局与边界

### 2.1 直接基线：LeanHammer / LeanPremise

**Premise Selection for a Lean Hammer**  
ICLR 2026 Oral / arXiv 2506.07477  
链接：
- https://openreview.net/forum?id=m04JJNeRK6
- https://arxiv.org/abs/2506.07477

已做：

- LeanHammer 是 Lean 的 end-to-end domain-general hammer。
- LeanPremise 是 hammer-aware premise selector。
- 系统结合 premise selection、translation、Aesop、Lean-auto、Zipperposition、Duper/reconstruction。
- 强调可以动态适配 user-specific contexts，包括用户本地 lemma 和训练外 library。
- 相比已有 premise selectors，多解决约 21% goals。

对我们的约束：

- 不能主打“我们也能做 Lean hammer”。
- 不能主打“我们也支持 local premises”。
- 不能只训练一个更强 one-shot retriever。

我们的切口：

> LeanHammer 仍主要把 premise selection 视作 proof attempt 之前的一次性选择。我们研究 proof attempt 失败之后，如何用 failure trace 闭环优化下一轮 premise distribution。

### 2.2 最危险的新对手：LeanSearch v2

**LeanSearch v2: Global Premise Retrieval for Lean 4 Theorem Proving**  
arXiv 2605.13137  
链接：https://arxiv.org/abs/2605.13137

已做：

- 定义 global premise retrieval：为整个 theorem 找一组分散但共同有用的 lemmas。
- standard mode：Mathlib hierarchy-informalized corpus + embedding/reranker。
- reasoning mode：iterative sketch-retrieve-reflect。
- 下游固定 prover loop 中替换 retriever 可提升 proof success。

对我们的约束：

- “iterative retrieval” 已经有人做。
- “global premise set” 已经有人做。

我们的切口：

> LeanSearch v2 的迭代来自 sketch/retrieve/reflect；FAR-Hammer 的迭代来自 verified prover/hammer failure traces。它不是 query-rewrite retrieval，而是 failure-conditioned premise optimization under fixed verification budget。

LeanSearch v2 必须作为强 baseline 或组件：

- LeanSearch standard mode as retriever。
- LeanSearch reasoning-mode-style retry as baseline。
- FAR-Hammer on top of LeanSearch candidates as strong combination。

### 2.3 proof repair / feedback 热区：APOLLO、APRIL、OProver、Process-Verified RL

**APOLLO**  
NeurIPS 2025 Poster  
链接：https://openreview.net/forum?id=fxDCgOruk0

主线：Lean compiler feedback + LLM agent 修 proof text。

**APRIL / Learning to Repair Lean Proofs from Compiler Feedback**  
ICLR 2026 VerifAI Workshop / arXiv 2602.02990  
链接：https://arxiv.org/abs/2602.02990

主线：260k erroneous proof + compiler feedback + repair/explanation target。

**OProver**  
arXiv 2605.17283  
链接：https://arxiv.org/abs/2605.17283

主线：agentic Lean proving，失败尝试、compiler feedback、retrieved verified proofs 都进入 training loop，32B prover 很强。

**Process-Verified RL for Theorem Proving via Lean**  
ICLR 2026 Poster  
链接：https://openreview.net/forum?id=P00k4DFaXF

主线：Lean elaboration 给 tactic-level process reward，用于 RL。

对我们的约束：

- 不能写成“我们也用 Lean feedback”。
- 不能写成 proof repair。
- 不能写成 whole-proof prover。
- 不要和 32B/671B 大模型打榜。

我们的切口：

> 这些方法修 proof text、训练 tactic/whole-proof generator，或把 failure feedback 纳入模型训练。我们修的是 hammer search space：在每次失败后优化下一轮 premise set，使 symbolic backend 在固定预算内更容易找到 Lean-verifiable proof。

### 2.4 搜索指导相关：LeanProgress

**LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction**  
TMLR 2025 / arXiv 2502.17925  
链接：https://arxiv.org/abs/2502.17925

已做：

- 预测 proof 还剩多少步。
- 与 ReProver best-first search 结合，在 Mathlib4 上有约 3.8% 提升。

我们的切口：

> LeanProgress 估计当前 proof state 的进度；FAR-Hammer 估计失败后下一轮 premise set 应该如何改变。两者互补。

LeanProgress 可以做 compatibility baseline：

- LeanProgress only。
- FAR-Hammer only。
- LeanProgress + FAR-Hammer。

### 2.5 结构化 premise selection 与长上下文

相关但非主线：

- LeanDojo / ReProver：NeurIPS 2023 Datasets and Benchmarks Oral，链接 https://arxiv.org/abs/2306.15626
- Tree-Based Premise Selection for Lean4：NeurIPS 2025，结构优先 premise ranking。
- miniCTX / long-context theorem proving：arXiv 2408.03350。
- Lean Workbook / Lean Workbook Plus：LeanProgress 使用的大规模 proof corpus。

用法：

- LeanDojo 是基础设施与数据来源。
- Tree-based premise selector 可做结构 baseline。
- miniCTX/local project 是我们 hard subset 主战场。

---

## 3. 论文核心主张

### 3.1 反直觉主张

领域默认：

> 第一次失败后，最自然的操作是扩大 top-k、调用更多 prover、采样更多 proof。

我们要证明这个默认不可靠：

> **More premises are not monotonically better. In Lean hammer-style proving, failure often indicates that the current premise set is noisy, misleading, reconstruction-unfriendly, or missing a specific local bridge. The right response is not simply more context, but a different premise distribution.**

中文：

> 对 Lean hammer 来说，失败后不一定要加 premise；很多时候要删 premise、换 premise、提高 local/context-specific premise、或选择更容易被 Lean 重建的 premise。

### 3.2 论文一句话 claim

> We formulate Lean hammer premise selection as a closed-loop, fixed-budget optimization problem. We show that failed proof search provides counterfactual supervision about missing, noisy, and reconstruction-hostile premises, enabling failure-conditioned premise controllers to improve verified proof success, search efficiency, and proof-core precision over one-shot retrieval, top-k expansion, random retry, and iterative retrieval baselines.

### 3.3 证据层级：P/S/V

这篇论文不要只看 one-shot top-k recall。我们把证据拆成：

| 轴 | 记号 | 定义 | 典型误区 |
|---|---|---|---|
| Premise coverage | `P` | premise set 是否包含 proof core 或 proof-critical bridge lemmas | top-k recall 高就以为能证明 |
| Search-space quality | `S` | premise set 是否让 ATP/Aesop/Duper/Reconstruction 搜索可控 | 更多 premises 反而造成 timeout/search explosion |
| Verified success | `V` | Lean kernel 是否最终接受 proof | ATP success 不等于 Lean proof success |

核心理论关系：

\[
P \nRightarrow S,\quad S \nRightarrow V,\quad V \text{ is the final target.}
\]

failure trace 的价值：

\[
F_t \Rightarrow \Delta p(p_i\in\text{proof core}),\quad
F_t \Rightarrow \Delta p(P_t\text{ is search-tractable}),\quad
F_t \Rightarrow \Delta p(P_t\text{ is reconstruction-friendly}).
\]

---

## 4. 问题定义

### 4.1 One-shot premise selection

传统设置：

\[
P_0 = R(g)
\]

其中：

- \(g\)：Lean goal / proof state。
- \(R\)：retriever / reranker。
- \(P_0\)：top-k premise set。

然后：

\[
y_0 = \text{Prover}(g, P_0, B_0)
\]

输出 success / failure。

### 4.2 Closed-loop premise optimization

我们的设置：

\[
P_{t+1} = \pi_\theta(g, P_{\le t}, F_t, H_t, B_{\le t})
\]

其中：

- \(P_{\le t}\)：已尝试 premise sets。
- \(F_t\)：failure trace，例如 timeout、unsolved goal、type mismatch、reconstruction failure、failed rewrite、missing instance。
- \(H_t\)：partial search history，例如 backend status、tried tactics、ATP clauses、used premises。
- \(B_{\le t}\)：已消耗预算。
- \(\pi_\theta\)：failure-conditioned controller。

目标：

\[
\max_\pi \mathbb{E}[\mathbf{1}\{\text{Lean verifies proof}\}]
\quad
\text{s.t.}\quad
\sum_t B_t \le B.
\]

### 4.3 和普通 retry 的区别

普通 retry：

\[
P_{t+1} = \text{TopKExpansion}(R(g), k_{t+1})
\]

FAR-Hammer：

\[
P_{t+1} = \text{Select}(s_0(p,g)+s_f(p,g,F_t)-s_h(p,P_{\le t})+s_r(p,\text{reconstructability}))
\]

核心不是多试，而是失败改变 posterior。

---

## 5. 方法设计：FAR-Hammer

### 5.1 系统流程

1. 初始检索：LeanPremise / LeanSearch / ReProver / BM25 / tree-based retriever。
2. 调用 hammer/prover：LeanHammer-style pipeline、Aesop、Duper、Lean-auto、Zipperposition、simp/rw/exact controlled tactics。
3. 结构化记录结果：success/fail、timeout、unsolved goals、backend status、reconstruction status、used premises、failed premises。
4. failure trace parsing / encoding。
5. failure-conditioned reranking。
6. budget controller 决定下一轮：
   - expand：补 bridge/local/typeclass premises；
   - shrink：删 broad/noisy premises；
   - swap：换 theorem family；
   - reconstruct：偏向 Lean-friendly premises；
   - stop：预算不值得继续。
7. Lean kernel verification。

### 5.2 Failure taxonomy

| Failure type | 失败含义 | 预期 action |
|---|---|---|
| missing bridge premise | 当前 premise set 缺关键中间 lemma | 检索 transitive/bridge lemma |
| local context missing | 用户本地 lemma / 当前文件 theorem 没被召回 | boost local declarations |
| timeout/search explosion | premise 太多或太 broad | shrink / diversify / precision rerank |
| reconstruction failure | ATP found proof but Lean reconstruction failed | prefer Lean-friendly premises; reduce external-only lemmas |
| type mismatch | lemma 语义相关但类型无法 unify | type-aware rerank |
| failed rewrite direction | rw/simp 方向不对或 rewrite lemma 不匹配 | retrieve reverse/simp-normal-form lemmas |
| unresolved metavariable/typeclass | 缺 instance / coercion / implicit args | retrieve instances/coercion lemmas |
| repeated unproductive premise family | 多轮都尝试同类 premise 但失败 | history penalty |

### 5.3 Failure-conditioned reranker

候选 premise \(p\) 的分数：

\[
s(p) = s_0(p,g)
+ \lambda_f s_f(p,g,F_t)
- \lambda_h s_h(p,P_{\le t})
+ \lambda_l s_{local}(p)
+ \lambda_r s_{recon}(p)
- \lambda_n s_{noise}(p,P_t).
\]

解释：

- \(s_0\)：base retriever score。
- \(s_f\)：failure-conditioned score。
- \(s_h\)：history penalty，避免重复无效集合。
- \(s_{local}\)：local/user context boost。
- \(s_{recon}\)：Lean reconstruction friendliness。
- \(s_{noise}\)：broad/noisy premise penalty。

### 5.4 Controller 版本

| 版本 | 做什么 | 论文定位 |
|---|---|---|
| Rule-FAR | rule-based failure parser + action table | Phase 1 feasibility |
| Rerank-FAR | failure-conditioned cross-encoder/reranker | 主方法 |
| Budget-FAR | 学习 expand/shrink/swap/stop | 强版本 |
| Recon-FAR | reconstruction-aware premise selection | Oral 冲分项 |

主论文不要太 agentic。优先做：

> Rerank-FAR + Budget-FAR + Recon-FAR。

---

## 6. 训练数据设计

### 6.1 数据来源

| 数据源 | 权重 | 用途 |
|---|---:|---|
| LeanDojo / Mathlib proof states | 30% | 基础 proof state + proof dependency |
| LeanHammer/hammer-style failed attempts | 30% | failure-conditioned supervision |
| LeanSearch v2 / global retrieval tasks | 15% | global premise group baseline |
| miniCTX / local project tasks | 15% | unseen/local context 泛化 |
| synthetic micro-libraries | 10% | controlled failure taxonomy / known proof core |

### 6.2 Label 类型

成功 proof gives:

\[
(g, p^+) \in D_{success}
\]

失败 attempt gives:

\[
(g, P_t, F_t, y_t=\text{fail})
\]

failure-conditioned positive:

- 第一轮失败后，后续成功 proof 新增的 premise。
- 最终 proof core 中出现但第一轮没召回的 premise。
- local lemma 被后续轮次召回并用于 proof。

failure-aware hard negative:

- 出现在 timeout premise set 中的 broad premise。
- 导致 reconstruction failure 的 premise family。
- type-similar but non-unifiable lemma。
- repeated unproductive premises。

counterfactual labels:

- remove-one：移除 premise 后 proof 是否仍成功。
- replace-one：用相近 premise 替换后是否失败。
- shrink-set：删掉部分 premises 是否降低 timeout。

### 6.3 数据格式

统一 JSONL：

```json
{
  "goal_id": "...",
  "goal_state": "...",
  "context_hash": "...",
  "attempt_id": 2,
  "premises": ["A.b", "C.d"],
  "failure_trace": {
    "type": "timeout",
    "backend": "duper",
    "message": "...",
    "unsolved_goals": ["..."],
    "reconstruction": "not_attempted"
  },
  "next_success_premises": ["Local.bridge"],
  "proof_core": ["Local.bridge", "Mathlib.foo"],
  "budget": {"time_s": 10, "premise_k": 64},
  "result": "fail"
}
```

---

## 7. 理论路线

理论目标不是写复杂 theorem 装饰，而是解释反直觉主张。

### Proposition 1：Coverage is not search quality

高 premise coverage 不推出高 search-space quality。随着 premise set 变大，proof core recall 可能增加，但 search branching、ATP clause explosion、reconstruction ambiguity 也增加。

经验预测：

- top-k expansion 在某些区间提高 solved rate，但超过阈值后 timeout 上升。
- FAR-Hammer 在同样 proof-core coverage 下更少 timeout。

### Proposition 2：Failure trace is information

如果 failure type 与 premise set 的缺失/噪音模式相关，那么 \(F_t\) 会降低 premise utility posterior entropy。

经验预测：

- failure-conditioned rerank 比 history-only、random retry、top-k expansion 有更高 second-round recovery。
- coarse failure type 已有收益，structured trace 更强。

### Proposition 3：More premises can hurt

对于 hammer-style backend，premise set size 与 success 不是单调关系。存在 high-noise regime：

\[
|P| \uparrow \Rightarrow \text{timeout probability} \uparrow,\quad
\text{reconstruction success} \downarrow.
\]

经验预测：

- 预算曲线出现倒 U。
- shrink action 在 timeout subset 上有效。

### Proposition 4：Reconstruction is a separate axis

ATP success 不推出 Lean reconstruction success。某些 premise set 对外部 prover 友好，但对 Lean 重建不友好。

经验预测：

- recon-aware reranker 降低 ATP-success-but-Lean-fail 的比例。
- Lean-friendly premise features 能预测 reconstruction success。

### Proposition 5：Local context is a failure-amplified signal

训练外 local premises 在 one-shot retriever 中容易被低估；失败 trace 会提高 local premise posterior。

经验预测：

- miniCTX/local project subset 的 gain 高于 full Mathlib average。
- local boost 在 first-failure subset 上收益最大。

---

## 8. 实验矩阵

### E1 Main：Fixed-budget verified success

问题：

> 同样总预算下，FAR-Hammer 是否比 one-shot / expansion / retry 解出更多 Lean verified proofs？

设置：

- 总 wall-clock 固定：10s / 30s / 60s。
- 总 prover calls 固定：1 / 2 / 3。
- 总 premise budget 固定：64 / 128 / 256。
- one-shot：一次 top-k。
- expansion：逐轮加 top-k。
- FAR：失败后 expand/shrink/swap/rerank。

指标：

- Lean verified success rate。
- time-to-proof。
- solved per second。
- prover calls per solved theorem。

### E2 First-failure recovery

只看第一次失败的 goals：

\[
\text{Recovery} = P(\text{success by round }2/3 \mid \text{round 1 failed})
\]

这是主实验中的主表之一。它直接证明 failure signal 的价值。

Baselines：

- random retry。
- top-k expansion。
- history-only。
- LeanSearch iterative retrieval。
- failure-type-only。
- full FAR。

### E3 Premise budget curve

画 top-16/32/64/128/256。证明：

- one-shot expansion 不单调。
- FAR 在低预算下更 sample-efficient。
- timeout subset 上 shrink 比 expand 更好。

### E4 Time budget curve

5s / 10s / 30s / 60s。证明：

- FAR 不是靠更多时间。
- 同 solved rate 下 FAR 更快。

### E5 Failure signal ablation

| Variant | 去掉什么 |
|---|---|
| no-failure | 只用 base score |
| history-only | 知道试过什么，不知道失败类型 |
| failure-type-only | 只用 coarse taxonomy |
| message encoder | 用 failure text |
| structured trace | 用 backend status + unsolved goals + tried premises |
| full FAR | 全部 |

### E6 Failure taxonomy gain

按 failure type 汇报：

- timeout/search explosion。
- reconstruction failure。
- missing local premise。
- type mismatch。
- unresolved metavariable/typeclass。
- failed rewrite。

目标：

> 找出 failure trace 的高信息区域，而不是声称所有失败都同等有用。

### E7 Local / miniCTX generalization

设置：

- miniCTX。
- local Mathlib project。
- synthetic local library。
- 用户当前文件新增 lemma。

指标：

- local premise recall。
- verified success。
- first-failure recovery。
- local premise usage ratio。

预期：

> FAR 在 local/unseen context 上应显著强于 full average。

### E8 Reconstruction-aware retrieval

只看：

> ATP/prover 找到 candidate proof，但 Lean reconstruction 失败。

比较：

- normal rerank。
- recon-aware rerank。
- smaller premise set。
- Lean-friendly premise score。

指标：

- reconstruction success。
- ATP success but Lean fail rate。
- proof term size / reconstruction time。

### E9 Proof-core attribution

成功 proof 后做 remove-one / shrink-set：

- premise necessary precision。
- redundant premise ratio。
- minimal sufficient premise set size。

主张：

> FAR 选出的 premises 更接近 proof core，而不是简单堆更多 context。

### E10 LeanSearch v2 comparison

必须正面对比：

- LeanSearch standard retrieval。
- LeanSearch reasoning-mode-style iterative retrieval。
- FAR on top of LeanSearch candidate pool。

目的：

> 区分 sketch-reflect iterative retrieval 与 prover-failure-conditioned retrieval。

### E11 Compatibility with LeanProgress

组合：

- LeanProgress only。
- FAR only。
- LeanProgress + FAR。

目的：

> 证明 progress prediction 和 failure-conditioned premise optimization 是互补信号。

### E12 Diagnostic synthetic suite

构造小 Lean libraries：

- missing bridge lemma。
- noisy broad theorem。
- reconstruction-hostile lemma。
- local lemma missing。
- typeclass missing。

这些不是主 benchmark，而是机制解释：

> FAR 为什么在真实任务中有效。

---

## 9. Baselines

必做：

| Baseline | 目的 |
|---|---|
| BM25 / sparse | 最基本 |
| ReProver retriever | LeanDojo 代表 |
| LeanPremise / LeanHammer one-shot | 最关键 |
| LeanSearch v2 standard | 最新 retrieval 强基线 |
| LeanSearch v2 reasoning-style retry | 最新 iterative retrieval 强基线 |
| top-k expansion | 判断是否只是更多 premise |
| random retry | 判断是否只是多试 |
| history-only rerank | 判断 failure trace 是否必要 |
| failure-type-only | 判断 coarse trace 的价值 |
| full FAR-Hammer | 我们 |

可选：

- Tree-based premise selector。
- LeanProgress。
- APOLLO/OProver 不直接比较主结果，但在 related work 中清楚区分。

---

## 10. 坏结果分流规则

这部分必须从第一天写进实验报告。

| 类别 | 判定标准 | 处理 |
|---|---|---|
| Bug / artifact | 环境、Lean version、premise namespace、budget、公平性、parser、batching 改掉后消失 | 修，不写成 insight |
| True insight | seed/model/subset/budget 改变后仍稳定，且有机制解释 | 提升为主发现 |
| Boundary condition | 真实存在但只在特定 backend/subset/budget 下成立 | clean audit 后写成边界 |

可能的 true insights：

- full failure text 不如 coarse failure type。
- timeout 后 shrink 比 expand 更有效。
- local boost 只在 first-failure subset 有用。
- reconstruction-aware rerank 提升 recon success 但不提升 ATP success。
- top-k expansion 提升 coverage 但降低 verified success。

可能的 bug：

- Lean/mathlib 版本不一致。
- accessible premise pool 错误。
- proof state 序列化不同。
- timeout 统计不公平。
- backend 调用次数不一致。
- random retry 其实用了更多 wall-clock。
- parser 把 unrelated Lean error 归到 wrong taxonomy。

---

## 11. 资源升级后的实施路线

当前按 `ICLR_1` 同等级工作方式规划：

- 本地：`D:\ICLR_2`，写代码、分析、paper、审计。
- 4090 服务器：8x RTX 4090，维修期间暂不作为实验依赖；恢复后跑大规模 parallel Lean/prover calls、retriever/reranker grid。
- A40 服务器：2x A40 46GB，当前主实验服务器；已跑通 Phase 1 synthetic mock 和 real Lean wrapper sanity，下一步接 Mathlib/LeanDojo 或 LeanHammer。

### Phase 0：基础设施

1. 建 `src/`，所有脚本输出 JSON 到 `outputs/`，不要写死论文数字。
2. 建 `EXPERIMENT_MANUAL.md`，记录服务器路径、环境、同步命令。
3. 建 `experiment_report.md`，每次实验后更新。
4. 建 `theory_proofs.md`，理论命题与实验预测同步。
5. 建 `analysis/claim_evidence_map.md`，每个 claim 对应证据。
6. 建 `analysis/adversarial_review.md`，模拟 reviewer。

### Phase 1：两周 feasibility

目标不是全系统，而是证明 failure trace 有信息。

最小系统：

- LeanDojo/ReProver 或 LeanHammer-like retriever。
- 1000-5000 Mathlib proof states。
- one-shot top-k。
- 记录 first failure。
- rule-based second round：
  - timeout -> shrink / precision rerank。
  - local missing -> local boost。
  - reconstruction fail -> recon-friendly rerank。
  - type mismatch -> type-aware rerank。

Go 标准：

- first-failure recovery 相对 top-k expansion 提升 5-10%。
- 或同 solved rate 下 time/prover calls 降低 20%。
- 或 timeout subset shrink 明显有效。
- 或 local subset 有 10%+ relative gain。

注意：这不是“降级”判断。若全量 gain 小但 hard subset 很强，主线仍成立。

### Phase 2：主方法

- failure-conditioned reranker。
- failure-aware hard negatives。
- budget controller。
- LeanSearch/LeanHammer strong baselines。
- fixed-budget main tables。

### Phase 3：强版本

- reconstruction-aware reranking。
- proof-core attribution。
- miniCTX/local project。
- LeanProgress compatibility。
- synthetic diagnostic suite。

---

## 12. 论文结构

### Abstract 骨架

> Premise selection is a bottleneck for Lean hammers, but existing systems typically choose premises in a one-shot manner before proof search begins. We argue that failed proof search provides counterfactual supervision for premise optimization: a failure trace reveals not only which premises may be missing, but also which premises make search noisy or reconstruction difficult. We formulate closed-loop premise optimization under fixed verification budgets and introduce FAR-Hammer, a failure-conditioned controller that updates premise sets from prover traces, tried premises, and local context. Across Mathlib-style, LeanHammer, LeanSearch, and local-context evaluations, FAR-Hammer improves first-failure recovery, verified proof success, time-to-proof, and proof-core precision over one-shot retrieval, top-k expansion, random retry, and iterative retrieval baselines. Our analysis shows that more premises are not monotonically better; failure traces often guide the controller to retrieve fewer, different, and more reconstruction-friendly premises.

### Introduction

1. Lean proof automation depends on premise selection。
2. LeanHammer/LeanSearch/LeanDojo 已经很强，但主要在 proof attempt 前选 premise。
3. 真实 proving 是 failure-driven；failure trace 被浪费。
4. 反直觉：失败后不是简单加 premise。
5. 提出 P/S/V 层级与 closed-loop premise optimization。
6. FAR-Hammer 方法与 fixed-budget 实验。
7. 贡献列表。

### Method

1. Problem setup。
2. Failure taxonomy。
3. Failure-conditioned reranker。
4. Budget controller。
5. Training labels。
6. Reconstruction-aware selector。

### Experiments

1. Main fixed-budget verified success。
2. First-failure recovery。
3. Budget curves。
4. Failure ablations。
5. Local/miniCTX。
6. Reconstruction subset。
7. Proof-core attribution。
8. LeanSearch/LeanProgress compatibility。

### Discussion

- Failure trace as counterfactual supervision。
- More premises can hurt。
- Boundary cases。
- Practical reporting checklist for Lean premise selection papers。

---

## 13. Reviewer 风险与预防

| 质疑 | 预防 |
|---|---|
| 只是多试几次 | random retry / top-k expansion / same call budget |
| 只是 LeanSearch iterative retrieval | LeanSearch v2 baseline；强调 prover-failure-conditioned |
| 只是 proof repair | 不生成 corrected proof；修 premise set/search space |
| 只是工程系统 | closed-loop objective + information gain + counterfactual labels |
| LeanHammer 已做 local contexts | local context 不是主新意；主新意是 post-failure posterior update |
| failure trace noisy | ablation：coarse type、message、structured trace；坏结果分流 |
| proof success 提升小 | first-failure recovery、hard subset、efficiency、proof-core precision |
| baseline 不公平 | fixed wall-clock、fixed calls、fixed premise budget、canonical JSON audit |

---

## 14. 完成清单

### 最小强版本

1. Closed-loop premise optimization 问题定义。
2. P/S/V 证据层级。
3. Failure taxonomy + parser。
4. Rule-FAR feasibility。
5. Failure-conditioned reranker。
6. Fixed-budget main experiment。
7. LeanHammer / LeanSearch / ReProver / expansion / retry baselines。
8. First-failure recovery。
9. Local/miniCTX subset。
10. Failure ablation。
11. Efficiency metrics。
12. Claim-evidence map。

### Oral 潜力版本

1. Reconstruction-aware reranking。
2. Proof-core attribution / remove-one ablation。
3. Counterfactual premise labels。
4. LeanProgress compatibility。
5. Diagnostic synthetic suite。
6. Paper-ready demo：user local lemma missed first, failure triggers local boost, second round verified。

---

## 15. 最终判断

这条线可以做强，但必须避免三个弱写法：

1. 弱写法：我们用 failure feedback 改进 Lean proving。  
   强写法：failed proof search is counterfactual supervision for premise optimization。

2. 弱写法：我们提出 adaptive premise selection。  
   强写法：one-shot premise selection conflates premise coverage, search quality, and verified success。

3. 弱写法：我们多轮检索。  
   强写法：more premises can hurt; failure tells us when to shrink, swap, and reconstruct-friendly rerank。

最终主线：

> **Lean hammers should not treat premise selection as one-shot retrieval. Failed proof search exposes the gap between premise coverage, search-space quality, and verified success. FAR-Hammer turns those failures into closed-loop premise optimization under fixed verification budgets.**
