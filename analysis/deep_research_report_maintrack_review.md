# ICLR 主会严审式深度评估报告

## 总判断

这篇稿子**不是该推倒重来**，但也**远不到 oral**。它已经有一个真正像 ICLR main-track 的核心机制结果：在 Lean 里，“选到哪些 names”并不够，**同一批 names 经过不同 proof-action interface 暴露给证明器，效果会发生剧烈变化**；在当前 replayable Mathlib 预定理上下文上，一个小的 typed proof-action portfolio 确实几乎吃掉了现有 oracle headroom。更具体地说，当前稿件主结果是：230 个 replayable traced-corpus goal 上，typed action grid 达到 58/230，最佳单一动作是 38/230；固定四步 portfolio 的 OOF 达到 57/230，train-fitted 达到 58/230；Aesop 的 facts+simps 暴露能做到 38/230，而 facts-only 只有 5/230，simps-only 只有 4/230，32-name 暴露还会显著变差。这个结果**有机制性，也有反直觉性**，它比“调了几个 tactic”强得多。citeturn13view0turn14view0turn1view0turn2view0turn5view1turn5view3

但以**今天这份 paper**的状态，我不会把它评成“稳主会”，更不会评 oral。原因不是 idea 完全不行，而是**最强证据仍是一个 fixed portfolio on a replayable subset**，不是一个学到的 policy，也不是一个强 system-vs-system 胜利；同时理论部分目前基本是解释性 proposition，不是会让 oral 审稿人眼前一亮的理论推进；再加上外部 baseline 还没有官方复现，评审非常容易把它打成“有意思但还偏工程/局部机制观察”。仓库里的 adversarial review、NEXT_STEPS 和当前 paper 自己都已经把这些风险写得很明白。citeturn1view0turn2view3turn15view0

我的一句话结论是：**这条线可以继续，而且应该继续强化 typed proof-action portfolio；但必须把它从“portfolio engineering”改造成“typed interface mechanism paper”，并且在投稿前至少补齐 interface filtering + stability reporting 这两块，否则主会仍然偏危险。**citeturn1view0turn3view0turn13view0

## 最可能被拒的五个原因

**第一，审稿人会说：这不是一个方法，只是一个固定重试列表。** 当前 strongest verified policy 仍然是固定 portfolio，而低容量 adaptive policy 并没有稳定打败它；paper 里也明确写了“adaptive routing 还不是 supported main claim”。这意味着如果你没有把“typed interface is the intervention”讲到足够锋利，评审会直接把它读成“试了 Aesop、HammerCore、solve_by_elim 等几个动作的组合”，然后给出“engineering but limited novelty”的评价。这是头号风险。citeturn1view0turn2view3turn13view0turn14view0

**第二，绝对成功率和评测范围都不够强。** 论文主结果是 58/230，约四分之一；而 230 只是 490 个 cleaned traces 里的 replayable subset。paper 自己也明确承认它不是 open-ended theorem proving benchmark，只是在 pre-theorem replay harness 上测 kernel-verified action success。这个范围界定是诚实的，但在 main-track 审稿里，评审很容易把它理解成“效应存在，但数据面太窄，绝对性能也不够 convincing”。citeturn13view0turn14view0turn15view0turn3view2turn5view0

**第三，缺失强外部 baseline，尤其缺 official system-to-system reproduction。** 现在 paper 和 claim ledger 都反复强调，BM25/iterative lexical rows 只是受控 proxy，不是 LeanSearch v2 正式复现；也没有官方 LeanHammer/LeanSearch v2 系统级对比。因此评审很容易质疑：你到底是在发现一个普适机制，还是只是在你自己的 harness 里找到了一个局部现象？如果这点不处理，哪怕主张是“orthogonal to retrieval”，也仍然会被问“为什么我该相信这不是 harness-specific artifact”。citeturn1view0turn13view0turn14view0turn5view0

**第四，Aesop 机制结果仍可能被攻击为 interface-poisoning artifact，而不是干净的 typed effect。** adversarial review 已经把这点写出来了：facts-only / simps-only / 32-name 失败，可能部分来自 invalid names、unsafe rule insertion、target leakage filtering 或 wrong-interface exposure，而不仅仅是“typed semantics”本身。换句话说，当前结果虽然有意义，但还不够“clean”。这也是为什么 E1 interface filtering gate 被排在第一优先级。citeturn1view0turn3view0

**第五，论文仍有“两个项目缝在一起”的气味，理论也偏浅。** 当前主线应该是 verified typed proof-action paper，但正文仍保留 trace-core discovery controller、guardrail proposition、imported-core 发现线索等内容；paper 自己的 self-review 也承认 method names 很长、fixed portfolio 可能看起来太简单、replayable subset 太窄。更致命的是，理论部分的 proposition 以条件互信息恒等式、预算非单调性、guardrail intuition 为主，更多是合理解释，不是强理论贡献。对 oral 级别审稿人来说，这会被读成：**idea 有意思，但“写了理论外形”的经验论文，不是理论-方法双强论文。** citeturn1view0turn14view0turn15view0

## 主线是否足够与 oral 差距

我的判断是：**typed proof-action portfolio 这条主线，足够构成 ICLR main-track 论文的“种子”，但还不够构成今天这份稿子的“安全主会版本”；它离 oral 更明显不够。** 如果你把 paper 明确收束成一个**机制论文**，主张“selected evidence has interface type in Lean”，并用 Aesop facts+simps 这个强机制反例加上 fixed-budget near-oracle portfolio 作为主证据，那么它是可以站在 main track 上的；但要站稳，至少还缺三样东西：**更干净的因果隔离**，也就是把 invalid/unsafe exposure 清掉；**更 robust 的 portfolio 统计**，也就是 per-fold paired stability，不要只给 aggregate；以及**更可信的外部锚点**，哪怕只是有限、诚实、范围受限的官方系统比较或更明确的 orthogonality framing。citeturn1view0turn3view0turn13view0turn14view0

如果不补这三块，当前主线最容易被读成：“一个很好的 internal finding，但还没完成从 lab insight 到 conference contribution 的转化。” 换句话说，**它不是不够新，而是不够硬。** 现在 strongest evidence 已经表明 typed exposure matters，甚至表明 Aesop 的 facts+simps 联合暴露和 blind 32-name 扩张之间有强非单调性；但作为 main-track 论文，评审还要看到：这不是一个脆弱 artifact，不是某个 hand-picked retry schedule，也不是只在作者自己的 harness 里成立。citeturn5view1turn5view3turn1view0turn13view0

按**当前稿件状态**，我给以下分数，分数不是“idea 是否可爱”，而是“如果现在投，按 ICLR 严格主会/口头报告尺子怎么打”：  
- **Idea：7.5/10。** “premise utility is interface-typed” 这件事是 sharp 的，而且 Aesop facts+simps vs facts-only/simps-only 的对比确实有反直觉价值。citeturn13view0turn14view0turn1view0  
- **Theory：4.5/10。** 当前 proposition 主要是解释性壳体：条件互信息恒等式、预算非单调性、guardrail 直觉；它们能支撑 narrative，但不像 oral 级理论贡献。citeturn14view0  
- **Method novelty：6.0/10。** typed action formulation 本身有新意，但 strongest verified result 仍然是 fixed sequence，adaptive policy 还没有赢下 matched-compute baseline，所以方法层面的“algorithmic novelty”没有被完全坐实。citeturn1view0turn2view3turn14view0  
- **Empirical strength：5.5/10。** kernel-verified、真实 Lean/Mathlib 环境、机制 ablation 都是加分项；但 230 replayable goals、58/230 的绝对成功率、缺 official 外部基线，这三点把上限压住了。citeturn13view0turn14view0turn3view2turn5view0  
- **Writing clarity：6.0/10。** 现在已经比旧 trace-core 主线清楚得多，但正文仍残留 discovery project 的影子，method names 也偏长，评审不够容易一眼看懂“什么是 main claim，什么是 discovery evidence”。citeturn1view0turn15view0  
- **Overall oral chance：3.5/10。** 不是因为 idea 不够，而是 oral 通常要求你在 idea、method 与 evidence 三者里至少有两项非常强；现在最强的是 mechanism insight，method 与 external empirical anchoring 还不够。citeturn1view0turn14view0turn15view0

所以，对问题二和问题三的合并回答是：**主线有 main-track 潜力，但当前成稿不够“安全主会”，更远未到 oral。oral 的差距主要不在 idea，而在 theory depth、method undeniability、empirical closure。** citeturn1view0turn14view0turn15view0

## 实验清单与 E1 E2 E3 的优先级

如果你的目标是“这篇 paper 必须走 ICLR main track，不接受 evaluation-only 降级”，那么实验必须按“**能不能直接关闭 reviewer attack**”来排，而不是按“是否好玩”来排。按这个标准，我把实验分成三层。citeturn1view0turn3view0turn2view3

**必须做，否则 paper 站不住的实验/分析**只有两类半。第一类是 **E1 interface filtering gate**：把 selected names 的 resolve/survival 记录下来，加入 target theorem / alias / same-file-later leak guards，把 theorem facts、simp-eligible lemmas、definitions、classes、instances、constructors、namespaces 分开，并且避免把 definitions/classes/instances 当作 Aesop unsafe theorem-like rules 乱塞进去。这个实验不是锦上添花，而是直接回应“你那个 Aesop 机制会不会只是 invalid insertion artifact”的质疑；同时它还有机会真正提高 oracle 或 fixed portfolio ceiling。第二类是 **E2 paired portfolio stability table**：必须把 K=1/2/3/4 的 per-fold 结果、paired wins/losses 对最佳单动作与 hammer_empty、strict-goal coverage、only-family counts 都做出来。现在 aggregate OOF 57/230 很好看，但 review-proof 不够。那“半类”是 **泄漏与 survival-rate 的显式审计**，它可以做成 E1 的一部分，但一定要出现在主文或 appendix，因为这是当前机制 claim 最软的一处。citeturn1view0turn3view0turn2view3

**高收益但不是 submission blocker 的实验**有三类。第一类是**有限、诚实的官方系统比较**：如果一周内能在 replayable subset 上复现一个干净且受控的 LeanSearch v2 / LeanHammer 外部对照，那会明显提高 paper 的说服力；但前提是必须是真复现，不是再包装一次 lexical proxy。如果做不到干净复现，就不要用半吊子版本污染主表。第二类是 **E3 stronger adaptive gate**，但只在 E1 之后做：仓库已经明确写了，当前 NB/kNN 没有清晰打败 fixed typed portfolio，只有在 E1 产生新的 action diversity、提升 oracle ceiling 或引入新的 only-family positives 时，才值得投入更强 router。第三类是**适度扩 replayable coverage**，但 only if method improvements plateau 之后还需要降低“subset 太小”的攻击强度；当前 NEXT_STEPS 已经明确说，默认不要先扩，因为瓶颈不是数据量，而是接口过滤和 policy strength。citeturn1view0turn2view3turn3view0turn13view0

**应该停止的分支**也很明确。第一，**naive `simp only` / `rw` 模板扩展**应立即停止，因为 48-goal negative branch 是 0/288 verified，主失败是 rewrite_fail 与 simp_fail；NEXT_STEPS 也明确写了，在没有 typed rewrite-direction selector 之前，不要继续。第二，**`simp_rw` 扩张**也应该停，除非先做 rewrite-direction selector。第三，**手工 expert/base mixing 和弱 adaptive 小修小补**应停，因为 imported-core 发现线已经显示这类 hand-tuned expert-insertion policy 不稳定或有害；在当前周期里继续磨这些，会把资源从更重要的 verified typed-interface clean-up 上拉走。citeturn2view3turn4view8turn4view4turn15view0

在 E1、E2、E3 三者中，**优先级必须是 E1 > E2 > E3**。E1 第一，因为它同时回应 R1 和 R4：既能把“固定 portfolio 看起来像工程”的故事提升为“typed exposure mechanism”的更干净因果证据，又有机会真正抬高 58/230 ceiling；E2 第二，因为它投入低、收益高，能立即让当前 fixed-portfolio result 更 review-proof；E3 最后，因为当前仓库证据已经说得很清楚——弱 adaptive 不够，只有在 E1 先创造了新的 headroom 或 action diversity 之后，才值得训练更强路由器。现在先做 E3，多半只是把 negative result 再做一遍。citeturn1view0turn3view0turn2view3turn5view3

## 应该强化什么以及不该怎么 pivot

我的建议是：**继续强化 typed proof-action portfolio，不要现在 pivot 到更大、更散的叙事。** 具体说，主方向应该是“**typed interface mechanism + filtered exposure + strong fixed-budget control**”，而不是“更深理论”“更强 adaptive routing”“更大 system comparison”三选一式地大转弯。原因很简单：仓库里目前最硬的 verified 新信号就是 typed exposure 本身，尤其是 Aesop facts+simps 的联合作用和 32-name 的反直觉退化；这是你已经真正拿在手里的东西。相反，更强 adaptive routing 现在还没有支撑证据；更大 system comparison 目前也没有 official reproduction；更深理论则没有任何迹象表明一周内能写出足够强的新理论来托住 oral 级审稿。citeturn13view0turn14view0turn1view0turn2view3

所以我的战略建议不是“死守当前文案”，而是**把项目从“portfolio paper”抬升成“interface-typing paper”**。这意味着：固定 portfolio 只是证据，不是灵魂；灵魂是“selected names 的 utility 取决于被赋予的 proof-action type”。在这个框架下，E1 变成 clean causal validation，E2 变成 robustness/stability validation，而 E3 只是条件性追击。这个顺序既最省时间，也最符合仓库里已经积累的证据结构。citeturn1view0turn3view0turn13view0

如果你非要考虑 pivot，我只接受**很小的、附录级的 pivot**：做一个有限 official-system comparison 作为 external anchor，而不是把全文改写成 benchmark 或 leaderboard 论文。至于**推倒重来**，我不建议。理由是：你现在最不该做的就是把已经非常罕见的强机制结果扔掉，去追一个还没有证据的“更大词”。Aesop facts+simps 38/230 对 5/230、4/230 的差距，本身就是一个值得主会认真看的现象；问题不是它不够好，而是你还没有把它包成足够难以拒绝的论文。citeturn5view1turn1view0turn14view0

## 冲 oral 的重写方案

如果你要按 oral 的标准来重写，我会把 title、abstract、core claim、method 和 experiment layout 全部压回到一个更锋利的中心：**typed evidence exposure**。现在的标题“Premise Selection Is Not Enough: Typed Proof-Action Portfolios for Lean”已经比旧故事对，但还不够强。我会优先用下面这个版本：**Typed Evidence, Not Just Retrieved Evidence: Budgeted Proof-Action Portfolios for Lean**。这个标题比现在更明确地点出：贡献不是“选得更好”，而是“证据必须以正确接口类型进入 Lean”。如果你想更机制导向，可以备选：**The Interface Type of Evidence in Lean Proof Search**。这些改法都严格贴着当前 paper 的已支持主张，而不是扩张到未支持的 adaptive or system-level claim。citeturn13view0turn14view0turn1view0

我会把 abstract 改成下面这种写法，注意其中只保留当前已支持的数字和边界，不夹带任何“adaptive 已成立”或“系统已领先”的话：

> **Abstract.** Premise retrieval in Lean is incomplete unless retrieved names are assigned to the proof interface that consumes them. We study typed proof-action selection, where the same candidate names can be exposed as Hammer facts, HammerCore inputs, simp lemmas, Aesop facts/simps, or elimination facts under a fixed Lean-call budget. In a Mathlib 4.30 + LeanHammer 4.30 pre-theorem replay harness on 230 replayable theorem contexts, the typed action grid reaches 58 kernel-verified proofs, versus 38 for the best single action. A fixed four-retry typed portfolio reaches 57 out of fold and 58 when train-fitted, recovering nearly all observed oracle headroom. The strongest mechanism result is counterintuitive: for Aesop, exposing selected names jointly as facts and simp lemmas solves 38 goals, while facts-only solves 5, simps-only solves 4, and broader 32-name exposure degrades sharply. These results show that in Lean, evidence utility is interface-typed: selecting the right names is not enough unless they are routed through the right proof action. We present this as a verified interface-mechanism result, not as a claim that adaptive routing or full-system theorem proving has already been solved. citeturn13view0turn14view0turn5view1turn5view3

**core claim** 也要收紧成一句话，不要现在这个稿子里时不时散出 discovery project 的味道。我建议主 claim 就写成：**In Lean, premise utility is interface-typed: under matched proof-search budgets, routing selected names through the correct proof-action interface matters enough to nearly saturate observed replay-time oracle headroom, and Aesop exposes a sharply non-monotone mechanism.** 这句话的好处是它把“近 oracle”“Aesop 机制”“budgeted proof search”绑在一起，同时不越过 claim ledger 里那些明确禁止的话。citeturn2view1turn5view0turn13view0

**method section** 也需要改结构。现在 paper 已经把 typed proof action 提前了，但我还会继续做三件事：第一，把 formal definition 提前，并把“proof action = interface + chosen names”作为全篇唯一 intervention object；第二，把 fixed portfolio 直接定义成 hardest control，而不是看起来像“随手找的 heuristic”；第三，把 trace-core discovery controllers 从 main method 里降级为 motivation/discovery appendix，只在正文留一句“它们启发了 budget non-monotonicity 与 fixed-budget controls”。否则评审会在阅读中不断被拉回旧项目。citeturn13view0turn14view0turn1view0

**experiment layout** 我会改成极其简单的四段式。第一张主表：230 replayable goals 上的 typed action grid、best single action、fixed K=2/K=4 OOF、oracle。第二张机制表：Aesop facts-only / simps-only / facts+simps 与 8/16/32 暴露预算。第三张 robustness 表：E1 filtering 前后、candidate survival rate、invalid/unsafe exposure 审计、paired wins/losses 和 per-fold stability。第四张边界表：adaptive router 未胜过 fixed portfolio、external proxies 不是 official LeanSearch v2、evaluation 仅限 replayable subset。Phase 1/3 trace-core 与 bridge 全部放到 appendix，作为“为什么我们想到这件事”的发现链，而不是正文核心。citeturn1view0turn3view0turn13view0turn15view0

## Claim 边界与一周执行计划

现在可以**强写**的 claim 只有三类。第一，**typed proof-action exposure matters beyond premise ranking**；第二，**在 230 replayable Mathlib theorem contexts 上，小的 fixed typed portfolio 几乎吃掉了当前观察到的 oracle headroom**；第三，**Aesop 的关键不是多 names，而是 facts+simps 的联合 typed exposure，facts-only、simps-only 与 32-name blind insertion 都明显更差**。这些都已经被 paper、claim ledger 与 experiment report 多方对齐支持。citeturn2view1turn5view0turn13view0turn14view0turn5view1turn5view3

必须**谨慎写**的 claim 有四类。第一，**“more premises can hurt”** 必须限定在固定 proof-search 预算、具体接口和当前 replay harness 下；不要把它写成普遍真理。第二，**与 retrieval 系统的关系**只能写成 orthogonal/complementary，不要暗示已经 system-level 超过 LeanSearch v2。第三，**adaptive routing 的前景**只能写成 next target，不是 current achievement。第四，**对更广泛 Lean proving 的外推**必须显式加 replayable subset、pre-theorem context、非 open-ended benchmark 这些边界。citeturn1view0turn13view0turn14view0turn5view0

现在**绝对不能写**的 claim 也很清楚。不能写“我们击败了官方 LeanSearch v2 / LeanHammer 系统”；不能写“adaptive failure-conditioned routing beats matched fixed typed portfolios”；不能写“当前结果等价于 full theorem proving success”；也不能把 Aesop ablation 解释成一个已经排除了 invalid insertion / unsafe-rule artifact 的纯语义定理。claim ledger 和 adversarial review 都已经明确把这些列为 unsupported 或 future work。citeturn1view0turn5view0turn13view0

最后是一周内的**具体执行计划**。这个计划只做高杠杆动作，不做“看起来勤奋”的噪音实验。citeturn3view0turn2view3

- **周一：完成 E1 的 instrumentation 与过滤实现。** 必做输出：每个 goal、每个 interface 的 candidate survival rate；invalid/unknown_identifier 计数；definitions/classes/instances/constructors/namespaces 的 typed 分桶；target theorem / alias / same-file-later leak guards。**Stop/Go 标准：**如果到周一结束都还拿不到 survival-rate 审计，就停止所有 adaptive 新实验，因为你连最核心的 artifact 攻击都没法回答。citeturn1view0turn3view0

- **周二到周三：只重跑高价值 family 的 filtered ablation。** 只跑 `aesop_core_plus_learned`、`aesop_core_plus_learned16`、`hammerCore_core_plus_learned`、`hammer_core_plus_learned16`、`solve_by_elim_core`。**Stop/Go 标准：**如果 filtered 版本把 oracle 从 58 提到至少 60，或者把 fixed K=4 OOF 从 57 提到 58，那么它立刻升格为 main-table result；如果 oracle 不涨，但 invalid exposure 大幅下降、Aesop 差异仍然存在，那它至少成为强 robustness ablation；如果它既不涨 ceiling、也不能显著干净化机制解释，只是 reshuffle successes，就停止继续扩更多 filtering variants。citeturn1view0turn3view0turn5view3

- **周四：完成 E2 paired stability table。** 必做输出：per-fold K=1/2/3/4，paired wins/losses vs best single action 和 `hammer_empty`，strict-goal coverage，only-family counts，尤其是 Aesop 的 only-family strict cases。**Stop/Go 标准：**如果 portfolio 优势高度集中在单个 fold 或 paired wins 非常不稳，那么正文必须降调，改成“strong but split-sensitive”；如果 per-fold 形状稳定，就把“hard control”这件事写进 abstract 和 intro。citeturn1view0turn3view0turn13view0

- **周五：条件性决定是否进入 E3 stronger adaptive gate。** 只有在 E1 之后出现了新 oracle headroom、新 only-family positives 或更干净的 interface diversity 时，才训练更强 adaptive router；feature 必须至少包括 first failure type / stderr cluster、interface survival rates、nonempty channels、namespace / statement features。**Stop/Go 标准：**如果新 router 不能 beat fixed K=2，或者不能用更少 Lean calls match fixed K=4，就一律不进 main text，最多 appendix 一句 negative result。citeturn1view0turn3view0turn2view3

- **周六：大改论文结构。** 具体改动：abstract 和 intro 全删 adaptive 成功语气；related work 明写 lexical rows 不是 LeanSearch v2 official reproduction；method 只保留 typed action 正文，trace-core discovery controllers 下放 appendix；results 主文只保留四张表——main verified table、Aesop mechanism table、E1 robustness table、E2 stability table。**Stop/Go 标准：**如果你删不掉 discovery baggage，就说明你还没有真正接受这篇 paper 的主线已经变了。citeturn1view0turn13view0turn15view0

- **周日：claim scrub 与投稿阈值判断。** 我会用三个阈值来决定是否进入“可投主会”状态：其一，E1 至少要产出一个可写进正文的 robustness 结论；其二，E2 必须证明 fixed portfolio 不是 aggregate 幻觉；其三，全文所有 claim 必须与 claim ledger 一致，不出现 system-level 胜利、adaptive 已成立、full theorem proving 之类的越界表述。**Go 标准：**满足这三点，就可以以“typed interface mechanism paper”姿态冲主会；**No-Go 标准：**如果 E1 和 E2 都没有新增说服力，那就不要硬冲 oral 叙事，应把目标调整为“有希望的 main-track 机制稿”，并彻底放弃任何 adaptive 或系统级夸张写法。citeturn2view1turn5view0turn1view0turn3view0

最苛刻但也最实用的一句话是：**你现在不是缺故事，你是缺把故事变成“无法轻易被 reviewer 一句话抹掉”的清洁证据。** 先把 typed exposure 证明干净，再谈 oral。citeturn1view0turn3view0turn14view0