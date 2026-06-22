# Overall verdict

**一句话结论：新 framing 已经足以构成 ICLR main-track 方法论文的身份，但当前证据包还不足以安全支撑这个身份。**

“Action-Conditional Evidence Allocation”明显强于“typed proof-action portfolio”。后者描述的是一个最终产物——固定动作序列；前者定义的是一个独立决策问题——把候选证据编译为带接口类型的 Lean evidence program。论文题目、摘要和引言已经基本完成这个概念升级，并且正确地把 fixed (K=4) portfolio 降为 hard control，而不是 adaptive method。

但目前版本仍是 **borderline，略偏 weak reject**。主要不是因为 idea 不够新，而是因为三个关键实验口径尚未被充分披露或控制：

1. 当前最强动作中的 `core` 实际来自 traced `proof_core`，而非普通可部署 retriever。
2. Aesop 的 38/230 现象还没有排除空 Aesop、名称身份、规则数量和 source composition 等混杂因素。
3. 当前 protocol 严格匹配的是 Lean call 数，不是已经证实的总 compute；Hammer 有内部 5 秒 wallclock 限制，而 runner 的外层 timeout 默认可达 180 秒。

我的当前内部评分：

| 维度             |                  当前分数 |
| -------------- | --------------------: |
| Idea / framing |                8.0/10 |
| 方法身份清晰度        |                6.0/10 |
| 机制证据           |                6.5/10 |
| 实验 soundness   |                5.0/10 |
| 泛化与外部有效性       |                4.5/10 |
| Theory         |                5.0/10 |
| 写作与结构          |                5.5/10 |
| 可复现性           |                5.0/10 |
| **Overall**    | **5.0/10，borderline** |

主观结果判断：

* **当前提交**：约 35–45% main-track accept；oral 低于 5%。
* **完成文中列出的 submission-blocking controls**：可上升到 6.5–7/10，进入 solid accept 区间。
* **再加 retriever-only external anchor、冻结的新 corpus，以及真正干净的 channel mechanism control**：才开始具有 10–20% 左右的 oral discussion potential。

---

# Biggest remaining rejection risks

## 1. 最严重：headline result 是 oracle-assisted，但论文没有明确披露

代码中的 `selected_names_for_check` 直接构造：

[
\texttt{proof_core} + \texttt{learned candidates},
]

随后 `fact_core` 和 `simp_core` 都由 traced `proof_core` 构成；`core+learned8` 因此是 ground-truth proof-core names 与 learned names 的组合，而不是单纯 retriever 输出。

这是一个很大的 reviewer-facing transparency risk。当前正文说“retrieved names must be compiled”，但最强结果实际回答的是：

> 给定部分 oracle proof evidence 和 learned evidence，如何将它们编译到 Lean 接口？

这个设置可以很好地做 **mechanism isolation**，但不能被呈现为可部署 premise-selection method。

更重要的是，Aesop 结果显示：

* `core+learned8`, facts+simps：38
* `core`, facts+simps：4
* `learned8`, facts+simps：4

因此真正出现的现象不只是 channel interaction，而是明显的：

[
\text{source composition} \times \text{channel assignment}
]

高阶交互。

这不是坏结果。它甚至可能使论文更有趣：**可用 evidence program 需要同时组合不同证据来源和不同消费通道。** 但必须透明写出，不能继续让 `core` 看起来像普通 retriever core。

---

## 2. Aesop counterfactual 很强，但尚未构成干净的 causal mechanism

现有结果足以证明一个真实而显著的 Lean 现象：

* joint facts+simps 远强于任一 single channel；
* top-32 比 top-8 差；
* 接口配置对 kernel-verified success 有一阶影响。

但它暂时不能单独证明“complementary channels”是唯一机制，原因有四个。

第一，facts pool 与 simps pool 只匹配 source 和 budget，不保证包含相同 names；报告本身已经明确承认这个 caveat。

第二，joint arm 注册了两个通道，通常具有比 single arm 更多的总规则数量。

第三，最重要的缺失基线是 **`aesop_empty = 29/230`**。当前主表突出 38 对 5/4，但真正的默认 Aesop 比较是 38 对 29，而不是 38 对 5。

这不否定结果：它说明增加一个不合适的单通道会严重 poison search，而正确双通道不仅恢复默认能力，还新增一些目标。但“34 joint-only”只是相对于两个 single-channel controls，并不表示有 34 个目标是相对于 empty Aesop 新增的。

第四，`core+learned8` 有效，而 core-only、learned-only 几乎无效。因此不能只写成“facts 与 simps complementary”；更准确的是：

> **某些 source compositions 只有在 joint typed exposure 下才能形成有效的 Aesop search program。**

现有 Aesop 结果足以成为主机制动机，但还差一组严格 controls 才足以支撑 main-track 的 causal wording。

---

## 3. “Matched compute”表述过强

当前固定 portfolio 与 learned allocators 的确匹配了 retry 数，并报告了平均 Lean calls；这足以叫：

> matched Lean-call budget / matched attempt budget

但暂时不足以叫 matched compute。Aesop、Hammer、HammerCore、simp 的实际运行代价可能非常不同。

这会产生一个直接 reviewer objection：

> 57/230 是否只是因为 portfolio 获得了更多昂贵 Aesop search，而不是因为 typed allocation？

必须增加累计 wallclock、CPU time 或 Lean heartbeat budget 的成功曲线。否则全文统一把 “matched-compute” 改成 “matched-call”。

---

## 4. 仍缺少真正 matched-budget 的 untyped/homogeneous portfolio

58/230 oracle 对 38/230 best single 是有用的 action-space diagnostic，但不是 compute-matched comparison：oracle 看过完整 action grid，best single 只运行一次。

当前 (K=4) table 很好地控制了 fixed versus learned router，却没有完全回答：

> typed diversity 是否优于同样四次调用的 untyped 或 single-interface retry schedule？

需要计算或补跑：

* Hammer-only (K=4) portfolio；
* Aesop-only (K=4) portfolio；
* simplification-only (K=4) portfolio；
* 同一 interface、不同 top-(k) 的 homogeneous portfolio；
* random interface portfolio；
* full typed (K=4)。

这组 control 比继续训练另一个 classifier 更重要。

---

## 5. OOF 并没有控制 action-space 的 researcher overfitting

固定 portfolio 是 5-fold OOF 选择的，这很好；但 50-action grid、接口家族、top-8/16/32 预算和具体组合是在当前 230 goals 上逐步开发出来的。

因此 OOF 只控制了：

> 在已有 action set 中选择 portfolio。

它没有控制：

> action set 本身是如何在同一批数据上被设计出来的。

在 submission 前必须冻结 action/compiler，然后在一个未用于 action design 的 corpus 上做 prospective run。

---

## 6. 正文结构仍像“两篇论文拼在一起”

虽然摘要和引言已经切换到新主线，但正文在 typed matrix 和 Aesop 之后仍连续保留：

* local trace-core recovery；
* timeout stress；
* imported-core global retrieval；
* split stability and bridge；
* 混合新旧故事的大型 diagnosis table。

这些部分目前仍占据大量 main-text 注意力。

Reviewer 不会只根据你写了“supporting evidence”就自动把它们当 supporting evidence。版面结构本身在表达 contribution hierarchy。现在的结构仍会触发：

> There are two partially connected papers here.

---

## 7. 当前 theory 主要是在形式化直觉，而不是解释结果

现有 mutual-information proposition 基本是 entropy identity；它把 interface (\tau) 当成一个可观察条件变量，但在该问题中 (\tau) 是一个需要选择的 intervention。

“Complementary channels”命题是 existential statement；“larger premise sets can hurt”也是相对容易构造的存在性结论。最后的 narrow guardrail proposition属于旧 trace-core 故事，应当移除。

理论目前足以防止“完全没有分析”的评价，但不足以提高 paper ceiling。

---

# Whether the new framing is strong enough

**概念上足够，当前实证实现还没有完全跟上。**

新 framing 比旧 framing 强，原因是：

| 旧 framing                 | 新 framing                                             |
| ------------------------- | ----------------------------------------------------- |
| 方法对象是 action sequence     | 方法对象是 evidence-to-interface assignment                |
| 容易被理解为 tactic retry list  | 是 retrieval 之后的独立决策层                                  |
| fixed portfolio 是论文主角     | fixed portfolio 是 allocation principle 的 hard control |
| novelty 依赖具体 Lean tactics | novelty 可推广为 typed evidence compiler                  |
| 学不到 router 就显得失败          | learned router 可以诚实成为未跨过的 boundary                    |

最值得保留的核心句是：

> **Retrieved evidence has an interface type.**

但要让 reviewer 真正接受这个 framing，正文必须把 method object 写成显式的 **typed evidence IR/compiler**，而不是主要展示若干长 action names。

建议标题改为以下两者之一：

> **Evidence Has Interface Type: Action-Conditional Evidence Compilation for Lean**

或

> **Compiling Retrieved Premises into Lean Proof Interfaces**

“Compilation”可能比“Allocation”更适合当前结果，因为你已经证明的是一个 rule-based compiler/interface mechanism，而不是一个成功的 learned allocator。

同时，`\tap = ACE-Hammer` 这个名字也建议改掉。方法覆盖 Aesop、simp、HammerCore 和 `solve_by_elim`，称为 Hammer 容易让人误判范围。使用 **ACE-Lean** 或直接 **ACE** 更清楚。

---

# Required paper edits

## 1. 在摘要和 protocol 中明确区分两层结果

必须写明：

> The primary mechanism matrix uses traced proof-core names as an oracle-assisted core pool, combined with learned candidates, to isolate post-retrieval interface effects.

然后把 eventual external retriever-only experiment称为：

> deployment-facing plug-in evaluation.

这是 submission-blocking disclosure。隐藏或模糊这一点会比绝对成功率低更危险。

---

## 2. 定义真正的 typed evidence program

建议用以下变量替代目前过于抽象的 (a=(\tau,P))：

[
z_{p,\tau}\in{0,1},
]

其中 (z_{p,\tau}=1) 表示名字 (p) 被分配到接口 (\tau)。同一个名字允许多标签分配，因此 joint facts+simps 不是两个独立 retry，而是一个 typed program。

约束写成：

[
\sum_p z_{p,\tau}\le b_\tau,\qquad
C(z)\mapsto \text{Lean tactic syntax},
]

并列出 compiler 的真实映射：

* Hammer facts；
* HammerCore simp/fact pairs；
* Aesop safe facts；
* Aesop simp rules；
* simplifier lemmas；
* elimination facts。

同时明确区分：

* candidate provenance；
* channel eligibility；
* channel assignment；
* outer action schedule。

---

## 3. 把主结果表重构为 reviewer 可比较的预算阶梯

主表建议只保留：

| 方法                        |            总调用数 | OOF verified |
| ------------------------- | --------------: | -----------: |
| Empty Hammer              |               1 |       29/230 |
| Best single typed action  |               1 |       38/230 |
| Empty + fixed typed (K=1) |               2 |       49/230 |
| Empty + fixed typed (K=2) |               3 |       55/230 |
| Empty + fixed typed (K=4) |               5 |       57/230 |
| Typed-grid oracle         | diagnostic only |       58/230 |

其中 58 必须明确标为 diagnostic oracle，而非 compute-matched method。

Train-fitted 58/230 移到 appendix；正文只强调 OOF 57。

---

## 4. 重写 Aesop 主表

主表必须加入：

* `aesop_empty = 29`；
* joint vs empty 的 paired gains/losses；
* strict joint successes：empty fail、joint success；
* joint failures：empty success、joint fail；
* identity-matched 和 rule-count-matched controls。

不要再让 38 vs 5/4 成为唯一视觉比较，因为这会被有经验的 reviewer 立即指出遗漏默认 Aesop。

---

## 5. E1 只作为 robustness boundary

建议正文写成一段：

> **Syntactic admissibility is not sufficient for interface utility.** Most selected names resolve in the pre-theorem context, and strict theorem/simp filtering contributes no new oracle goals, but it destroys most successful compiled programs. Thus the gains are not primarily an unknown-identifier cleanup effect, while coarse declaration metadata is insufficient to recover tactic-specific utility.

E1 显示 7321/7497 names 可用，filtered-only oracle 只有 4/230，combined oracle仍为58，而且没有新增 oracle goal。

但还要诚实写出：same-file-later declaration filtering 尚未完成，因为缺少 candidate declaration spans。

正文一段即可；完整 action table 和 category audit 放 appendix。

---

## 6. Allocator gate 写成“当前 feature frontier”，不是一般负结论

建议用一句精确表述：

> Current goal, failure, and pool features do not improve the fixed portfolio frontier. Residual logistic regression gains one goal over fixed greedy at (K=3), but neither exceeds 57/230 nor reaches that result with fewer than four retries.

因为数据中 residual logreg 在 (K=3) 是 56，而 fixed 是55；不能笼统说 learned allocator 在所有预算都不赢。它真正没有做到的是：

* 不超过最终 57；
* 不把 57 压缩到 (K\le3)；
* 不 beat fixed (K=4)。

正文保留一句 boundary，完整 classifier table 移 appendix。

---

## 7. 扩充 related work 中的“tactic selection / portfolio”防线

LeanHammer、LeanSearch v2 和 LeanDojo可以支撑“现有主轴主要是 retrieval/premise selection”的定位；外部 anchor 也适合基于这些系统构造。([arXiv][1])

但还必须主动讨论 tactic-selection 和 tactic-portfolio 先例，例如 TacticToe。区别应当写成：

> Prior work selects tactics and tactic sequences; ACE conditions the representation and role of the same evidence on the consuming interface, including multi-channel assignment inside a single tactic invocation.

否则 reviewer 会替你写出“这只是 tactic portfolio”的 related-work objection。([arXiv][2])

---

# Required experiments, with go/no-go criteria

| 优先级    | 实验                                                                             | Go 标准                                                              | No-go 后的处理                                                                    |
| ------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **P0** | Pool provenance decomposition：retrieved-only、oracle-core-only、oracle+retrieved | retrieved-only仍有明确 typed gap；所有 headline 数字能按 provenance 解释        | 若效果仅存在于 oracle+retrieved，论文必须降为 oracle-assisted mechanism study               |
| **P0** | Aesop empty/identity/count matched controls                                    | joint 相对 empty 和 best single 有显著 paired gain；至少10个严格新增目标；两个预算上方向一致 | 若同名同计数后消失，删除“complementary channels”，改为“interface-induced search sensitivity” |
| **P0** | Homogeneous (K=4) portfolio                                                    | typed (K=4) 明显优于最佳单接口 (K=4)                                        | 若持平，fixed portfolio engineering 风险仍然很高                                        |
| **P0** | Wallclock/heartbeat frontier                                                   | 在统一预算下 (K=4) 仍接近57，且typed方法位于 Pareto frontier                      | 若优势依赖明显更高 Aesop compute，全文只能声称 matched calls                                  |
| **P1** | External retriever-only anchor                                                 | 至少增加5个verified goals、paired CI不跨0，并且总compute增幅不超过约10%              | 无增益则不能声称可部署 post-retrieval method                                             |
| **P1** | Frozen fresh holdout                                                           | typed oracle–single gap至少约5pp；fixed (K=4) 回收大部分该gap                | gap消失则现有 action space 很可能过拟合230 goals                                         |
| **P2** | Aesop trace/proof-term mechanism cases                                         | 5–10个joint-strict goals中能观察到 simp 与 safe-fact 两类作用                 | 若只使用一类规则，弱化“complementarity”因果解释                                              |
| **P3** | Learned allocator rerun                                                        | (K\le3) 达到 fixed (K=4)，或 (K=4) 显著超过57，且在fresh holdout成立            | 否则永久留 appendix/future work                                                    |

统计上至少补：

* per-goal paired wins/losses；
* McNemar exact test 或 paired bootstrap；
* Wilson/bootstrap confidence intervals；
* per-fold results；
* success versus cumulative time，而不只是 aggregate count。

---

# External anchor：是否必须以及如何设计

**以当前 `proof_core` provenance 而言，至少一个 retriever-only external anchor 对 solid accept 基本是必须的。**

最优先选择 **LeanHammer premise selector**，原因是你已经在 LeanHammer 4.30 环境中运行，集成风险最低。LeanSearch-style ranked lists可以作为第二 source，但不需要把整个 LeanSearch v2 system复现。

正确设计不是把官方论文数字塞入当前主表，而是：

1. 冻结一个 upstream retriever。
2. 对每个 goal 导出同一批 top-(k) names。
3. 禁止加入 traced `proof_core`。
4. 比较：

   * upstream 默认/untyped consumption；
   * best single Lean interface；
   * fixed typed compiler；
   * typed oracle。
5. 相同 name identities、相同 call/time budget。
6. 单独放在 **Retriever-agnostic plug-in anchor** 小节。

这样不会污染机制主表：

* Table 1：oracle-assisted mechanism isolation；
* Table 2：retriever-only deployment anchor。

不要把它描述成“我们复现 LeanSearch v2”或“系统级击败 LeanHammer”。只声称：

> Given the same upstream ranked candidates, typed compilation improves downstream kernel-verified success.

---

# Replayable corpus：是否扩，以及优先级

答案是：

* **立即优先于 corpus expansion 的，是 disclosure、Aesop exact controls、homogeneous portfolio control 和 compute accounting。**
* **但在最终 submission 前，一个冻结的新 holdout 高于继续 polishing allocator。**

不要优先把当前 490 traces 再反复挖得更深。更有价值的是：

1. 先冻结 compiler、action set、budgets 和 analysis script；
2. 再从未参与 action design 的文件、theorem families 或另一 Mathlib snapshot 构造新 replayable corpus；
3. 只运行一次，不根据新结果修改 action set；
4. 将新结果作为 prospective validation。

对 main-track，300–500个新的 replayable goals 已经会明显改善可信度。对 oral，最好再有一个不同 retriever或不同 Mathlib snapshot，使结果不是单一 corpus × 单一 evidence source 的现象。

---

# Theory upgrades needed

## 1. 用 intervention/potential-outcome formulation 替换 MI identity

定义：

[
Y_g(z;B)\in{0,1}
]

为 goal (g) 在 typed assignment (z) 和搜索预算 (B) 下的 kernel-verified potential outcome。

接口条件化 utility 应是边际 intervention effect：

[
u_g(p,\tau\mid z)
=================

Y_g(z+e_{p,\tau};B)-Y_g(z;B),
]

而不是仅仅 (P(U\mid p,\tau))。这个定义自然允许：

* 同一个 name 在不同 interface 中符号相反；
* utility 依赖当前 program；
* facts 和 simps 产生 interaction；
* adding more evidence 具有负边际效应。

---

## 2. 给出 interface-agnostic policy 的严格可分离性定理

可以证明一个很短但真正有关的方法定理：

> 当至少两个接口对候选 names 存在 utility ranking reversal 时，任何基于单一 scalar name score 的 interface-agnostic policy，在某个 goal distribution 上都被 typed allocation policy 严格支配。

这直接形式化“name ranking is insufficient”。

---

## 3. 用 interaction contrast 定义 complementary channels

加入空基线后定义：

[
\Delta_{f,s}
============

Y(F,S)-Y(F,\varnothing)-Y(\varnothing,S)+Y(\varnothing,\varnothing).
]

在 corpus 上报告平均 (\mathbb{E}[\Delta_{f,s}]) 和 paired confidence interval。

只有在 identity/count-matched controls 下仍为正，才称为 complementary-channel effect。

---

## 4. 形式化 bounded-search interference

不要只说“存在 (P_1\subset P_2) 使更大集合失败”。给一个确定性的有限搜索树构造：

* 成功路径深度为 (d)；
* 新规则在搜索顺序中产生 (m) 个优先分支；
* 当 (m) 消耗完预算 (B) 时，成功路径不再被访问。

这会直接解释 top-32 collapse，而不是泛泛地说 timeout。

---

## 5. 区分 inner allocation 与 outer portfolio

这是当前理论最值得加入的结构：

* 对固定 action success sets (S_a)，portfolio coverage

[
F(A)=\left|\bigcup_{a\in A} S_a\right|
]

是 monotone submodular；greedy fixed portfolio 因而是一个自然且很强的 maximum-coverage control。

* 但 action 内部的 evidence allocation (z\mapsto Y_g(z)) 由于 interference 与 complementarity，通常是 non-monotone、non-submodular。

这个区分能统一解释：

* 为什么 fixed greedy (K=4) 几乎饱和 oracle；
* 为什么 name budget 不是单调的；
* 为什么 adaptive outer routing当前没有 headroom；
* 为什么真正困难的方法问题在 inner typed compiler。

删除当前 guardrail proposition；它属于旧论文。

---

# What to delete or move to appendix

## 从正文彻底删除

* `Claim-Evidence Map` 这种内部审稿式表格；
* appendix 中的 `Claim-Evidence Self-Review`；
* narrow guardrail proposition；
* FAR 的大量 method detail；
* imported-core learned controller 的主表；
* bridge stability 主表；
* guardrail/expert-mixing diagnosis rows；
* train-fitted (K=4=58) 的重点宣传；
* controlled LeanSearch lexical proxy 的正文比较；
* 大段 canonical output file path 列表。

这些内容会使文章显得像自动生成的研究日志或 rebuttal memo，而不是完成态方法论文。

## 移到 appendix

* 完整 50-action matrix；
* E1 candidate category audit；
* 全部 allocator classifier rows；
* per-fold portfolio stability；
* top-8/16/32完整 action list；
* joint-only theorem names；
* replay migration failure taxonomy；
* trace-core timeout result；
* bridge sanity check；
* generated theorem-family pilots。

## 正文最多保留的 trace-core 内容

一小段 discovery path：

> Earlier trace-core experiments revealed failure-conditioned budget sensitivity and motivated testing whether evidence must be exposed through different Lean interfaces. These experiments are reported in the appendix; all primary claims in this paper use kernel-verified pre-theorem actions.

最多再保留一个 appendix overview table。不要继续让 trace-core 和 verified typed actions平级。

---

# Exact step-by-step execution plan for Codex

## Phase 0：冻结 protocol 与暴露 provenance

1. 创建 `analysis/final_protocol_freeze.md`，记录：

   * 当前 git commit；
   * 230-goal IDs 和 split hash；
   * canonical action set；
   * top-(k) budgets；
   * timeout/heartbeat；
   * 所有 go/no-go thresholds。

2. 修改 `run_mathlib430_pretheorem_action_matrix.py`：

   * 添加 `--candidate-source retrieved_only|oracle_core_only|oracle_plus_retrieved`；
   * 输出每个 action 的 `proof_core_count`、`retrieved_count`、overlap；
   * 将 action names 中的 `core` 重命名为 `oracle_core`；
   * 禁止论文产物继续使用含糊的 `core_plus_learned` 名称。

3. 生成：

   * `outputs/mathlib430_canonical_typed_grid_oracle_assisted.{json,md}`
   * `outputs/mathlib430_canonical_typed_grid_retrieved_only.{json,md}`
   * `analysis/mathlib430_candidate_provenance_audit.md`

4. 检查 headline 58、38、57分别来自哪些 provenance。任何变化立即同步到 paper，不允许沿用旧数字。

## Phase 1：完成 Aesop 的严格因果 controls

5. 在 runner 中添加四类 Aesop experiment modes：

   * `typed_pool_matched`
   * `identity_matched`
   * `registration_count_matched`
   * `hash_random_channel_split`

6. 每类都运行：

   * empty；
   * facts-only；
   * simps-only；
   * facts+simps；
   * swapped/random assignment。

7. 对 source 做完整 factorial：

   * oracle-core-only；
   * retrieved-only；
   * oracle+retrieved。

8. 输出：

   * paired outcome matrix；
   * empty-relative gains/losses；
   * strict joint-only count；
   * interaction contrast (\Delta_{f,s})；
   * bootstrap CI / McNemar test。

9. 生成：

   * `analysis/mathlib430_aesop_exact_channel_controls.md`
   * `outputs/mathlib430_aesop_exact_channel_controls.json`

10. Gate：

    * controls 通过：保留“complementary typed channels”；
    * controls 不通过：统一改写为“interface-conditioned search interference”，不再使用强 causal complementarity wording。

## Phase 2：补齐真正的预算控制

11. 从现有 matrix 计算或补跑：

* Aesop-only (K=4)；
* Hammer-only (K=4)；
* HammerCore-only (K=4)；
* simplifier-only (K=4)；
* random typed (K=4)；
* full typed (K=4)。

12. 在所有 attempt 中记录：

* process wallclock；
* CPU time；
* Lean heartbeat，如可用；
* cumulative policy time；
* first-success stopping cost。

13. 生成：

* `outputs/mathlib430_homogeneous_vs_typed_portfolios.md`
* `outputs/mathlib430_success_compute_frontier.md`

14. 在结果出来之前，paper 全文将 “matched compute” 改为 “matched Lean-call budget”。

## Phase 3：做 retriever-only external anchor

15. 优先接入 LeanHammer premise selector：

* 固定 top-8/16/32 lists；
* 保存原始 ranked names 和 selector version；
* 禁止 `proof_core` 注入；
* 运行同一 typed compiler 和同一 call/time budget。

16. 同表比较：

* selector + default Hammer；
* selector + best single interface；
* selector + homogeneous (K=4)；
* selector + typed (K=4)；
* typed oracle。

17. 可行时用 LeanSearch-style ranked lists重复，但单独标为 upstream retriever plug-in，不称作 full-system reproduction。

18. 生成：

* `outputs/external_retriever_typed_compiler_anchor.{json,md}`
* `analysis/external_anchor_protocol.md`

19. Gate：

* paired gain显著且至少新增5个verified goals：进入正文；
* 无增益：保留 appendix，并将论文明确限制为 oracle-assisted mechanism study。

## Phase 4：冻结新 holdout

20. 在看到新 corpus 结果前冻结：

* compiler；
* canonical actions；
* portfolio order；
* all budgets；
* analysis script；
* success thresholds。

21. 从未用于 action design 的文件、theorem families 或另一 Mathlib snapshot构造新的 replayable corpus。

22. 新 corpus 只运行一次；任何后续修改都必须标为 post-hoc，不并入 primary result。

23. 生成：

* `analysis/fresh_holdout_protocol.md`
* `outputs/fresh_holdout_typed_allocation.{json,md}`

## Phase 5：理论和论文重写

24. 重写 formulation：

* typed assignment matrix；
* compiler；
* intervention outcome；
* channel budgets；
* provenance。

25. 用三条理论替换现有四条 proposition：

* typed policy strict dominance；
* complementary-channel interaction；
* bounded-search non-monotonicity。
  另加一个 fixed-portfolio submodularity lemma作为 control justification。

26. 正文重排为：

27. Introduction

28. Related Work

29. Typed Evidence Compilation

30. Mechanism Evaluation Protocol

31. Canonical Typed Results

32. Aesop Counterfactual Mechanism

33. Retriever-Only External Anchor

34. Theory and Analysis

35. Limitations

36. Conclusion

37. 将所有 trace-core、bridge、E1 full audit、allocator details移到 appendix。

38. 删除 claim-evidence self-review、研究日志式 wording 和旧 method branding。

## Phase 6：artifact hardening

29. 当前 repo 明确排除了大型 raw JSON/JSONL，因此现在是 review package，不是完整 reproducible artifact。

30. 最终 release 必须补：

* compressed raw result matrices；
* goal/split hashes；
* exact commands；
* Mathlib/LeanHammer commit hashes；
* environment lock；
* generated Lean files或可重生成 manifest；
* checksums；
* 一键生成 paper tables 的 script。

31. 最终提交 gate：

* **Aesop exact controls失败**：删除 complementary-channel 主张；
* **retriever-only anchor失败**：论文定性为 mechanism study，oral ambition取消；
* **fresh holdout gap消失**：重新评估整条主线；
* **三项均通过**：以 strong main-track method paper提交。

---

最精确的最终判断是：

> **Framing is ready; the evidential contract is not yet ready.**

不要再投入精力训练另一个低容量 allocator。当前最有价值的工作依次是：披露 oracle provenance、完成 Aesop exact controls、补齐 homogeneous/time-matched controls、做 retriever-only anchor、再跑冻结的新 holdout。完成这些后，“evidence has interface type”会从一个非常好的观察，真正升级为一篇可信的 ICLR 方法论文。

说明：内容审查基于完整 `paper.tex` 与仓库实验材料；GitHub raw PDF 在当前环境未能完成逐页视觉渲染，因此未对最终 PDF 的浮动体、分页和字体做独立版面检查。

[1]: https://arxiv.org/abs/2506.07477 "https://arxiv.org/abs/2506.07477"
[2]: https://arxiv.org/abs/1804.00595 "https://arxiv.org/abs/1804.00595"
