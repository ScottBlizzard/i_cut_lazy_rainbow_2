# 对 ScottBlizzard/iclr_2 的深度研究判断

## 我读完这些材料后对项目的总体结论

这个仓库已经相当明确地把项目从旧的 failure-conditioned trace-core 叙事，转向了一个新的、更可 defend 的主线：**premise selection 在 Lean 里并不充分，关键还在于把同一批证据以正确的 proof-action / tactic interface 类型化地暴露给 Lean 的不同搜索与重构机制**。README、`NEXT_STEPS.md`、`experiment_report.md` 和 `paper.tex` 四处都在重复这一点，而且都主动收缩了 claim：当前支持的是 **typed proof-action portfolio / typed evidence exposure**，而不是 adaptive routing 已经胜过固定策略，也不是“开放式 theorem proving 已被解决”。仓库中 `paper.pdf` 作为当前编译稿存在于 `iclr2027/`，`paper.tex` 的题目已经直接定成 *Premise Selection Is Not Enough: Typed Proof-Action Portfolios for Lean*，这说明作者自己已经意识到真正有机会进入 ICLR main-track 的，是“后检索接口决策”这个方法问题，而不是旧的 trace-core controller 故事。citeturn1view0turn2view0turn2view1turn6view0turn10view0turn11view0

如果只问一句最核心判断，我的答案是：**这条 typed proof-action portfolio 主线，作为 ICLR main-track 方法论文是“有生路的”，但以当前形态还不够 oral；它必须从“固定 portfolio 很强”升级成“接口条件化的证据分配是一个独立且可证明的算法问题”，否则很容易被审稿人降级成 clever engineering / fixed retry list。** 造成这个结论的原因很直接：一方面，项目已经拿到了一个非常像“机制论文”的硬结果——在 230 个 replayable Mathlib 4.30 theorem contexts 上，typed action grid 的 oracle 是 58/230，而 best single action 只有 38/230；与此同时，Aesop 的 facts+simps 暴露能做 38/230，但 facts-only 只有 5/230，simps-only 只有 4/230，加入到 32 个名字反而明显变差。另一方面，预算化固定 portfolio K=4 的 out-of-fold 已经到 57/230，离 58/230 oracle 只差 1 个目标，导致“学一个 adaptive router”现在几乎没有足够 headroom 可讲。换句话说，**机制发现是强的，policy learning 是弱的**。citeturn17view1turn17view0turn5view1turn4view0turn6view0

更重要的是，放到外部研究图景里看，这个判断也成立。LeanDojo、LeanHammer、LeanSearch v2、LeanProgress、miniCTX 这些近年的代表性工作分别在开放基础设施、端到端 hammer、全局 premise retrieval、search guidance、长上下文 benchmark 等方向提出了明确方法轴或大规模评测轴；其中 miniCTX 甚至是 ICLR 2025 Oral。和它们相比，你这个项目真正新、且能够站住的方法轴，不是“再试几种 tactic”，而是**把 retrieval 之后的 interface assignment 本身提升为一等公民，并证明它对验证成功率有一阶影响**。只要论文一直沿着这条线讲，它是 main-track；如果主文稿再滑回“我们有一个 fixed retry list，很接近 oracle”，那就非常危险。citeturn16search8turn16search2turn16search1turn19search0turn19search11

还有一个很实际的观察：你指定的两份 `deep-research-report` 文件，本质上只是三句 executive summary，几乎没有超出 abstract 的新增分析；它们更多是在重复“58 vs 38、57 OOF、facts+simps 强”这组结论，而不是提供更深的 reviewer-facing argument。也就是说，**真正有价值的材料是 `paper.tex`、`experiment_report.md`、`NEXT_STEPS.md`、`paper_adversarial_review_typed_portfolio.md`、E1 strict filtering 文档，以及 action matrix / portfolio stability 结果**；那两份 deep-research report 本身不构成新的证据资产。citeturn3view0turn3view1turn2view0turn2view1turn4view0

## 这条 typed proof-action portfolio 主线到底强不强

我认为这条主线**足够强到值得继续，而且比“premise selection 改进版”强得多**，原因在于它已经满足了一个好方法论文最难得的条件：**反直觉、可验证、并且和现有主流轴线正交。** 现有 Lean 相关工作普遍把重点放在“找到哪些名字”这一层：LeanDojo 把 premise access 与 retrieval-augmented proving 数据化；LeanHammer 的贡献点是动态 premise selection 与 symbolic search/reconstruction 集成；LeanSearch v2 进一步把问题提升为 global premise retrieval。你这个项目实际上提出的是下一层问题：**同样是已选出的名字，进入 Hammer、HammerCore、Aesop、simp、solve_by_elim 的方式不同，验证结果也会显著不同**。这不是调参式增量，而是对“证据是什么”的定义本身做了 refinement：证据不是无类型集合，而是**带 interface type 的可执行暴露**。这点在 `paper.tex` 的 abstract/introduction 里已经表达得很清楚。citeturn6view0turn16search8turn16search2turn16search1

更关键的是，当前 strongest signal 的形状非常像可以打动 ICLR 审稿人的“counterintuitive mechanism”。Aesop 本身就是一个基于规则集进行搜索的 Lean tactic，官方文档和论文都强调它会根据规则和索引结构进行 proof search；在这样的机制下，同一批名字被作为普通 facts、simp lemmas、或者两者同时注入，本来就应该对搜索树结构和归约行为产生不同影响。你的 ablation 不是一个模糊的“multi-tactic ensemble works”，而是一个很尖锐的现象：**facts+simps 有效，而 facts-only / simps-only 近乎坍塌；再把候选扩大到 32 个名字又会退化。** 这与 Aesop 的规则搜索特性高度一致，因此是可信的机制证据，而不是只靠单一随机 seed 的偶然现象。citeturn17view0turn17view1turn16search3turn16search11turn16search15

但这条主线现在的上限，也确实被一个事实卡住了：**目前最好的“方法”在实验上看起来还是一个固定 portfolio，而不是一个学习到的算法。** `paper_adversarial_review_typed_portfolio.md` 自己就把这件事列为最高风险，而且我同意这个判断。现在的 fixed greedy K=4 out-of-fold 是 57/230，train-fitted K=4 达到 58/230 oracle；strict goals 上 OOF 已覆盖 28/29，train-fitted 覆盖 29/29。这个结果本身当然很强，但它给论文带来两面性：它说明 interface typing 的效应很大，同时也说明 **adaptive policy 的剩余空间太小**。一个审稿人很自然会问：既然固定四步几乎全拿到了，为什么这不是“我们试了几种 Lean tactic，排了一个好顺序”？如果不能把“为什么必须 typed，而不是 simply portfolioed”讲得非常硬，这就是最大降级点。citeturn5view1turn4view0turn6view0

因此，我建议把论文主线进一步升级为：

**不是“typed portfolio 很强”，而是“evidence has interface type；在固定验证预算下，证据的最优使用方式是 action-conditional allocation，而不是 untyped ranking 或 blind top-k expansion”。**

这个表述比当前标题更 method-like，也更有机会把 fixed portfolio 从“工程实现”抬升为“一个由更一般原理诱导出来的强控制组”。当前仓库已经有足够证据支撑这个升级方向，但还没有把它完全做出来。citeturn6view0turn4view0turn17view1

## E1 strict interface filtering 的负结果真正意味着什么

E1 strict filtering **没有削弱主线，反而澄清了主线的真正含义**。从结果看，strict filtering 的 filtered-only oracle 只有 4/230，combined oracle 仍然是 58/230，没有新增 oracle goal；`aesop_core_plus_learned` 和 `aesop_core_plus_learned16` 从原先 38、37 个 solved goals 直接掉到 3，`hammer_core_plus_learned16` 从 32 掉到 3，`hammerCore_core_plus_learned` 从 18 掉到 1。与此同时，candidate audit 显示，在 7497 个 selected 候选里，`unavailable` 只有 176 个，而 `available` 有 7321 个；类别上 `theorem_like` 3268、`definition_like` 1880、`simp_attr` 1927，`target_or_alias` 仅 24。再结合 e1-filtered stability 文件里固定 portfolio frontier 完全没动，还是 best static `aesop_core_plus_learned`，OOF K=4 仍是 57/230、train-fitted K=4 仍是 58/230，可以比较明确地得出结论：**当前 strict filtering 并没有发现“原先结果主要靠脏名字或目标泄漏撑起来”，它更像是一个过强过滤，把原本有用的 typed exposure 一起切掉了。** 这是基于结果和 audit 计数做出的推断。citeturn4view1turn5view1

所以，E1 不能作为“主线被打脸”的证据；更合适的写法是把它变成 **robustness boundary / mechanism audit**。它说明两件事。第一，主效应不是“只要把 invalid identifier 清理掉，所有问题就解决了”；因为一方面 invalid / unavailable 的量级并不大，另一方面 filtering 没带来任何 oracle 增益。第二，**typed exposure 的有效性非常脆弱**：你不能用过于粗暴的“安全化”规则替换掉原有暴露，否则会直接把 interfaced evidence 的有效通路也一并移除。这反而让你的方法论更明确：问题不是简单的 filtering，而是**如何做 interface-aware evidence assignment，在保证 candidate 合法性的同时不摧毁 tactic-specific utility**。citeturn4view1turn5view1turn2view0

这意味着 E1 在论文中的位置应当非常克制。它不应该成为 headline，也不应该写成“我们发现 strict filtering 失败了”这种 negative-result 口吻。最好的用法是：在 mechanism / robustness 小节里用一段话加一个表说明，**清理无效项本身并不足以解释 typed-action gains；过强安全过滤会伤害有效暴露，因此核心问题是 interface-conditioned evidence design，而不是 syntactic sanitization。** 这会让 E1 成为“边界条件”而不是“主结果挫败”。citeturn4view1turn4view0

我还会更进一步：E1 的真正价值在于给理论升级提供素材。你完全可以把它组织成一个更有力的结论——**“合法性过滤不是充分条件，真正关键的是可消化性 exposure”**。这是个很好的 main-track paper 味道：简单清洗无用，必须做机制匹配。只要写法得当，这比“我们试过 filtering，但没提升”强得多。citeturn4view1turn7view0

## 当前实验里哪些是真的论文资产，哪些只是工程噪声

真正有主文价值的实验，我会只保留四组。

第一组，是 **typed action grid 的主表**。这张表必须成为正文第一主表，因为它直接回答论文最重要的问题：在同一个 replay harness 里，typed action space 的 oracle 是多少，best single action 是多少，gap 有多大。你现在的关键数是 58/230 oracle、38/230 best static、gap +20 goals、strict action-dependent goals 29。这张表已经足够像一篇方法论文的核心结果。citeturn17view1turn6view0

第二组，是 **预算化固定 portfolio 的 matched-compute 表**。这里最重要的不是 train-fitted 58/230，而是 out-of-fold 的 K=1/2/4 曲线：49/230、55/230、57/230，以及 strict goals 覆盖从 20/29 提升到 28/29。它能说明两件事：一是 typed action diversity 的功能性是真实的；二是在相同 Lean-call budget 下，这个方法不是靠“无限重试”赢的。尤其是 K=2 到 55/230 这个结果，其实比很多人想象中更有价值，因为它显示很小预算已经覆盖了大部分有效头部动作。citeturn5view1

第三组，是 **Aesop facts/simps exposure ablation**。这是你最像 oral 的那块材料。`facts+simps` 38/230，facts-only 5/230，simps-only 4/230；源池从 core+learned8/16 到 core+learned32 又出现明显退化；source-level group coverage 也显示 core+learned8/16 到 41/230，而 core+learned32 只有 7/230。这个 phenomenon 不是 “Aesop 好”，而是 “Aesop 作为一个 interface，对 evidence channel 和 exposure budget 极其敏感”。如果论文只能保住一块机制证据，我会保这一块。citeturn17view0turn17view1

第四组，是 **E1 作为 robustness boundary 的附属表**。我不会把它放进 main table，但我会保留一张小表，说明 strict filtering filtered-only oracle 只有 4/230、combined oracle 不变、新增 0，同时 candidate audit 里 unavailable 很少。这张表的使命不是“展示新 SOTA”，而是防止 reviewer 把 Aesop 结果解释成 invalid-name artifact。citeturn4view1turn5view1

相对而言，我会明确降级为 supporting / appendix 的，是旧的 trace-core 线。`paper.tex` 附录里还保留了大量 Phase 1、Phase 2、Phase 3 的表：本地 trace-core ablation、imported-core lexical stress、bridge taxonomy、guardrail mixing 等。它们当然不是无用，尤其是“premise budget non-monotonic”与“failure feedback useful”这两个发现，的确是现在 typed-action 主线的发现来源。但它们不应该再和 verified typed-action 结果平起平坐。仓库自己的 adversarial review 也已经意识到了这一点，认为如果这些 trace-core 结果还以主结果姿态出现，会让论文看起来像“两篇半成品强行合并”。我完全同意。citeturn8view0turn4view0turn2view1

至于纯工程噪声，我会更狠一些。`NEXT_STEPS.md` 已经明确写了不要继续 naive `rw` / `simp only`，因为 rewrite48 分支 0/288 verified；不要再回去做 Hammer-only；不要把 generated theorem-family Gate 2 当 final main experiment；不要在当前 NB/kNN 结构上继续低容量 adaptive rerun。仓库里那两份三句版 deep-research summary，我也不会再引用。换句话说，**凡是不直接支撑“typed evidence exposure is the method”这句 thesis 的材料，都应该挤到 appendix 或直接删除。** 现在对你最宝贵的不是多，而是主线纯度。citeturn2view0turn4view0turn3view0turn3view1

## 当前 paper 的最大审稿风险，以及最可能到达 oral 的论文形态

如果让我只写一个最大的审稿风险，我会写：

**“This is a fixed portfolio paper masquerading as a method paper.”**

这是最高风险，不是因为 fixed portfolio 弱，而是因为它太强了。K=4 OOF 57/230、train-fitted 58/230，几乎吃掉全部 oracle headroom，会让 reviewer 很自然地觉得：这篇论文真正做的可能只是找到了一组好用的 Lean actions 顺序，而不是提出了一个可推广的方法。仓库自己的 adversarial review 也把这一点列为 R1，而且明确说 fixed portfolio 可能被看成 engineering unless the interface mechanism remains central。这个诊断非常准确。citeturn5view1turn4view0

第二大风险是 **evaluation scope 太窄，且口径容易被误读**。`paper.tex` 已经诚实写出：主评测只在 230/490 replayable cleaned traces 的 pre-theorem replay harness 上进行，不是 open-ended theorem proving benchmark，也不是所有 Mathlib theorem。问题不在于这个设置错误，而在于 theorem proving 审稿人会天然拿它去和 LeanDojo、LeanHammer、LeanSearch v2、miniCTX 这类更大、更公开、更“benchmark-like”的工作对比。LeanHammer 在摘要里强调端到端 domain-general hammer，并报告对现有 premise selectors 的 21% 相对提升；LeanSearch v2 甚至给出独立 benchmark 和固定 prover loop 的 downstream proof success；miniCTX 是 context-rich benchmark，且已到 ICLR Oral。你现在的方法如果没有一个更清楚的“orthogonality story”，很容易被质疑：为什么不直接和这些系统正面对打。citeturn6view0turn16search2turn16search1turn19search11turn16search8

第三大风险是 **理论部分还不够“方法论文级别”**。`paper.tex` 当前理论部分主要是三条 proposition sketch：条件互信息解释 typed actions 为什么应当有用、premise coverage 非单调、以及 narrow guardrail 更好。这些都不假，但目前更像“把直觉写成命题”，还没形成 reviewer 会记住的理论 punchline。尤其 oral 级别论文，理论不一定要很长，但通常需要一句能留下来的反直觉机制定理。你现在最有潜力的其实不是 mutual information 那条，而是：**在固定搜索预算和 interface-specific interference 下，最优策略不是 global top-k，而是按 channel 分配证据；而且更大的 untyped set 可能系统性变差。** 这才是能直接映射实验的理论句子。citeturn7view0turn8view0

因此，我认为**现在最可能到达 oral 的论文形态**不是“typed portfolio beats best single action”，而是下面这个更强的形态：

**Action-Conditional Evidence Allocation for Lean: retrieved names must be partitioned across proof interfaces, because interface-conditioned utility and interference dominate untyped ranking under fixed proof-search budgets.**

这种形态下，fixed portfolio 只是一个 baseline / instantiation；真正的核心方法是“对同一批 retrieved names 进行 typed assignment / typed exposure compilation”。如果你能再做到以下三件事中的任意两件，oral 才开始变得现实：其一，一个学习到的 typed allocator 在 matched compute 下真正 beat 或 compress fixed K=4；其二，把同一 retriever 接入 LeanHammer 或 LeanSearch v2 的 downstream loop，证明 typed interface module 有独立增益；其三，把理论升级成能解释 facts+simps 协同、32-name 退化、strict filtering 无增益的统一机制框架。没有这些，项目仍然更像 strong main-track / borderline-to-solid accept，而不是 oral。citeturn16search2turn16search1turn19search0turn19search11turn4view0

## 我建议继续当前方向，但要立刻改成更强的新 idea

我的建议不是推倒重来，而是**继续当前方向，但把“fixed typed portfolio”升级成“action-conditional evidence allocation / typed evidence compiler”**。这是最省仓库资产、同时最可能把论文从工程味中拉出来的办法。现有数据已经说明：同一批名字通过不同接口进入 Lean，价值差异巨大；Aesop 的双通道暴露比单通道强得多；盲目扩大名字数会伤害结果；简单过滤又会把有效暴露切没。把这些统一起来，最自然的新 idea 就是：

**retrieval 之后，不应只预测一个名字排序，而应预测一个 typed evidence program：哪些名字给 Hammer，哪些给 HammerCore，哪些给 simp，哪些给 Aesop facts，哪些给 Aesop simps，哪些直接丢弃。**

这比当前“portfolio”强，因为它把 method object 从“排动作顺序”变成了“编译 evidence into interfaces”。它也比完全另起炉灶安全，因为所有核心现象都已经在你的数据里出现了。citeturn6view0turn17view0turn17view1turn4view1

如果你认为当前方向的上限仍然不够高，我给出的 alternative main-track idea 也仍然围绕同一机制，但比现在更像一篇独立方法论文：

**Counterfactual Typed Exposure Learning**：给定同一 candidate pool，学习 interface-specific assignment，并通过 counterfactual controls 证明“性能提升来自 channel assignment，而不是 candidate pool quality”。这条线的好处是，你可以设计非常强的对照：同一份 top-k 名字，随机打乱 facts/simps 分配；同一份名字，只改 channel，不改 identities；同一 retriever，只替换 downstream typed compiler。只要这些对照成立，审稿人就更难把论文误读成“你只是找到了一个好顺序”。citeturn17view0turn17view1turn16search2turn16search1

相应地，哪些 claim 应删、哪些该强化，也很清楚。

应该删除的 claim，有四类。其一，**任何 adaptive routing 已经胜过 fixed portfolio 的暗示**；仓库和论文都已承认 NB/kNN 没有赢。其二，**任何接近 open-ended theorem proving、full-system competitiveness、或 official LeanSearch v2 reproduction 的表述**；当前并没有这样的实验。其三，**任何把 generated theorem-family pilot 当 final main experiment 的倾向**；`NEXT_STEPS.md` 明确反对。其四，**任何把 trace-core 结果写成当前 verified main result 的结构**。citeturn4view0turn2view0turn6view0

应该强化的 claim，也有四条。第一，**evidence utility is interface-typed**。第二，**under fixed Lean-call budgets, small typed portfolios recover nearly all current oracle headroom**。第三，**Aesop requires complementary facts+simps exposure; single-channel exposure collapses**。第四，**more retrieved names are not monotonically better because proof interfaces exhibit interference / budget sensitivity**。这四条是你现在最硬、最一致、也最能解释实验的 claim。citeturn17view1turn17view0turn5view1turn6view0

## Codex 可直接执行的计划

**Recommended paper main thesis**

把论文主论点改成：**在 Lean 中，premise retrieval 之后还存在一个独立的方法问题——action-conditional evidence allocation。被检索出的名字不是一个无类型集合；它们必须被分配到 Hammer、HammerCore、simp、Aesop facts、Aesop simps、solve_by_elim 等不同接口，否则同一批证据可能从有用变成无效甚至有害。** 当前 fixed typed portfolio 只是这个原则的一个强 baseline，不是最终主角。citeturn6view0turn17view0turn17view1

**Key insight / counterintuitive claim**

最值得打的反直觉 claim 是：**在 Aesop 中，更“完整”的证据暴露并不一定更好；把同一批名字同时作为 facts 和 simp lemmas 暴露，远强于只走单通道，而继续扩大到 32 个名字反而显著恶化。** 这意味着问题不再是“找更多对的 lemma”，而是“把合适的 lemma 以合适的 channel 暴露给合适的 interface”。这也是整篇论文最像 ICLR oral 风格的一句发现。citeturn17view0turn17view1turn16search15

**Required experiments**

1. **Gate experiment：typed evidence allocator vs fixed portfolio。**  
   用现在的 candidate pool 和 replay harness，训练一个比 NB/kNN 明显更强的 action-conditional allocator。输入至少要包括 goal/statement features、namespace、candidate survival by interface、first-failure stderr cluster、哪些 channel 非空；输出不是下一动作标签，而是接口条件化的 evidence assignment 或者动作分布。成功标准不是“略优于随机”，而是 **matched compute 下超过 fixed K=4，或达到 57/230 但用更少 calls**。如果做不到，adaptive 继续退出主 claim。citeturn2view0turn4view0turn5view1

2. **Counterfactual assignment control。**  
   固定同一批 top-k names，只改变 channel assignment：facts-only、simps-only、facts+simps、随机分配、shuffled 分配、budget-preserving 错配。目标是证明 gains 真的来自 interface assignment，而不是候选本身质量。这个实验比“再加一种 tactic”有价值得多。现有 Aesop ablation 已经是雏形，但还需要更系统的 counterfactual control。citeturn17view0turn17view1

3. **External plug-in evaluation。**  
   至少选一个外部强 baseline 作为 upstream retriever / prover substrate，优先是 LeanHammer 或 LeanSearch v2 所对应的 retrieval setup，证明你的 typed interface module 是 orthogonal improvement，而不是只能在自家 harness 里成立。这里不要求把所有系统完整复现，但至少要让 reviewer 看到“同一个 retriever，加了 typed exposure compiler 后 downstream verified success 更好”。否则 external-baseline 风险始终存在。citeturn16search2turn16search1

4. **Paired stability and compression table。**  
   继续保留 K=1/2/3/4 的 per-fold paired wins/losses，但把叙事改成 compression：**多少 oracle headroom 可以被一个小型 typed portfolio 吸收；多少 strict goals 需要哪类 interface；是否存在 only-family goals。** 这个表不是新 idea，但它是 reviewer-proofing 必需品。citeturn5view1turn2view0

5. **Replayable subset expansion only after the above gates.**  
   不要先冲更多数据。`NEXT_STEPS.md` 的判断是对的：当前瓶颈先不是样本数，而是 framing、filtering、policy strength。只有当 allocator / external plug-in 已经成型，才值得扩大 replayable coverage。citeturn2view0turn4view0

**Required theory**

理论部分建议重写成三条更“像 theorem”的机制结论，而不是保留现在偏直觉化的 sketch propositions。  
第一条是 **interface-conditioned utility theorem**：若接口变量对名字效用携带正条件信息，则任何 interface-agnostic ranking 在某些分布上都会被 action-conditional policy 严格支配。  
第二条是 **interference under bounded search theorem**：在固定预算下，存在 \(P_1 \subset P_2\) 使得 \(P_1\) 成功而 \(P_2\) 失败；并进一步把失败原因形式化为 branching / rewrite / reconstruction interference，而不仅是“timeout 可能发生”。  
第三条是 **complementary-channel theorem**：当 facts channel 与 simp channel 分别作用于不同的可证明性子机制时，双通道联合暴露可严格强于任一单通道；但单通道过宽暴露会因 interference 出现性能下降。第三条应直接对接 facts+simps 38/230、facts-only 5/230、simps-only 4/230、32-name 退化这些现象。citeturn7view0turn8view0turn17view0turn17view1

**Required figures and tables**

正文里我建议必须有六个可视化资产。  
其一，一张总览图：retriever 输出 names，typed evidence compiler 将它们分发到不同接口，再进入 Lean kernel verification。  
其二，主表：single best 38/230、oracle 58/230、strict 29。  
其三，budget curve：K=1/2/4 的 OOF performance 和 strict coverage。  
其四，Aesop channel ablation 条形图：facts-only / simps-only / facts+simps / wider 32-name。  
其五，counterfactual channel-assignment 表：同一 names，不同赋型。  
其六，boundary figure：E1 strict filtering 不增加 oracle，但 filtered variants collapse，说明纯过滤不是答案。citeturn17view1turn5view1turn17view0turn4view1

**Claims to remove**

删除以下表述：  
- “adaptive routing beats fixed typed portfolios”；  
- “competitive with full Lean theorem proving systems”；  
- “official LeanSearch v2 comparison exists”；  
- “generated theorem-family gate is final evaluation”；  
- “trace-core results are the main verified contribution”；  
- “more premises generally help”。citeturn4view0turn2view0turn6view0

**Claims to strengthen**

强化以下表述：  
- “premise evidence has an interface type”；  
- “typed exposure matters beyond premise ranking”；  
- “small typed portfolios nearly saturate current oracle headroom under matched compute”；  
- “Aesop requires complementary facts+simps exposure”；  
- “broader insertion can be harmful because Lean interfaces are budget- and channel-sensitive”；  
- “strict filtering shows cleanup alone does not recover gains”。citeturn17view1turn17view0turn5view1turn4view1

**Risks and kill criteria**

最高风险仍是“看起来像 fixed retry engineering”。第二风险是 replayable subset scope 与缺乏外部基线。第三风险是理论太薄。对应的 kill criteria 我会设得非常明确：  
- 如果更强 allocator 在 matched compute 下既**不能 beat fixed K=4，也不能明显 compress 到更少 calls**，那 adaptive 内容不要再碰主文；  
- 如果 external plug-in 实验做不出来，就必须彻底放弃任何 competitiveness 语气；  
- 如果 counterfactual assignment control 不能复现 typed channel effect，那 oral ambition 应当立即下调；  
- 如果扩到更多 replayable goals 后 58 vs 38 这类 interface gap 显著消失，就要重新评估主线是否只是 subset artifact。citeturn4view0turn5view1turn17view1

**Step-by-step execution plan**

1. 先重写题目、摘要、引言与方法段落，把“typed proof-action portfolio”升级成“action-conditional evidence allocation”，并把 fixed portfolio 明确降级为 strong control，不再当主 method identity。citeturn6view0turn4view0  
2. 把正文结果裁剪到四部分：typed action grid、budgeted portfolio、Aesop channel ablation、E1 robustness boundary；其余 trace-core/bridge 结果全部移到 appendix，只保留一段“discovery path”说明。citeturn17view1turn5view1turn17view0turn4view1turn8view0  
3. 立刻做 counterfactual channel-assignment controls，优先在 Aesop 上完成，因为这是最强机制证据。citeturn17view0turn17view1  
4. 在现有 230-goal harness 上训练更强 allocator；如果一周内看不到 beat/compress fixed portfolio 的迹象，停止再做低容量 router 试验。citeturn2view0turn4view0  
5. 做一个最小 external plug-in：固定一个 upstream retriever，把 typed evidence compiler 接到 LeanHammer 或 LeanSearch-style pipeline 后面，比较 downstream verified success。citeturn16search2turn16search1  
6. 重写理论，把当前 sketch propositions 改成三条直接对应实验的机制命题，并在文末 limitations 里保留 scope、subset、no official full-system comparison、adaptive 未胜 fixed 这四个诚实边界。citeturn8view0turn4view0  
7. 最后再决定 oral ambition：如果上面第 3 到第 5 步至少命中两项，论文可以冲高；如果只保住现在的 fixed portfolio + ablation story，那我建议把目标设为**强 main-track accept**，不要过度押注 oral。citeturn4view0turn19search11turn16search2turn16search1

我的最终建议非常明确：**继续当前方向，但不要再把“typed proof-action portfolio”停留在 fixed portfolio 层面。把它提升为“action-conditional evidence allocation”这件事，本项目才真正有机会从一篇不错的方法稿，跨到强 ICLR main-track 甚至接近 oral 的形态。** 现在最值钱的不是再跑更多噪声实验，而是把已经出现的机制信号组织成一个更强、更统一、并且更可证明的方法故事。citeturn17view0turn17view1turn5view1turn4view0