# ICLR Oral Upgrade Report  
## Failure Feedback as Conditional Evidence for Lean Premise Selection

**Assessment date:** 2026-06-21  
**Target:** ICLR 2027 main track, Oral-level ambition  
**Inputs reviewed:** `paper(3).pdf`, `gptpro_oral_upgrade_brief.md`, and `gptpro_oral_upgrade_prompt.md`  
**Literature window checked:** primary sources available through 2026-06-21

---

## 1. Executive Verdict

### Current assessment

| Item | Verdict |
|---|---|
| Current ICLR main-track score | **4/10 — weak reject** |
| Current Oral probability | **~1%** |
| Current accept probability | **~30%** |
| Recommendation | **Substantial pivot-and-upgrade; do not restart yet** |
| One-sentence reason it is not Oral | **The strongest gains are on trace-supervised proof-core recovery, while neither the replay bridge nor the current baselines establish that failure-conditioned premise control improves kernel-verified theorem proving over an equal-compute static LeanHammer portfolio.** |

The draft is coherent, unusually honest about scope, and contains a real phenomenon. The local result, timeout-shrink result, learned second-stage gain, split stability, and negative expert-mixing studies form a credible discovery package. The problem is not that the experiments are sloppy. The problem is that the **main causal object and the main evaluation object are still misaligned with the claim reviewers care about**.

The current paper says that a failed proof attempt provides conditional evidence about premise utility. Yet:

1. Most success labels are whether a selected set covers a **human traced proof core**, not whether a prover independently finds and verifies a proof.
2. The learned retriever and second-stage controller are both trained using traced proof-core supervision.
3. “Bridge verified” is a conjunction of trace-core recovery and replayability of a known script. Unless the selected premise set is actually injected into and causally constrains that replay, it is a filtered proxy rather than an intervention on proof execution.
4. The disagreement-heavy bridge set is useful for diagnosis but cannot estimate random held-out theorem-proving performance.
5. The timeout result appears to use a stress backend. It motivates non-monotonicity, but it does not by itself show real LeanHammer search-space poisoning.
6. The imported controller’s causal dependence on the **content of failure feedback** is not yet isolated. Failure-type-only matches expansion locally, and the inspected imported misses share one coarse failure type. A learned second-stage model may be exploiting the failed premise set, rank profile, or retry stage rather than semantic information in the failure signal.

That last point is a near-term kill test. Before expensive system integration, run a matched **true-feedback versus masked-feedback versus shuffled-feedback** experiment with the same architecture and data. If true feedback does not win, the correct claim is “adaptive second-stage reranking after failure,” not “failure feedback is conditional evidence.”

### Recommended direction

Do **not** throw away the current project. Instead, demote its current trace-core results to mechanism and pretraining evidence, and rebuild the main paper around:

> **Verified adaptive premise interventions:** after a fixed first hammer failure, choose among premise-set actions—shrink, expand, switch selector, interleave experts, rescue, or stop—using the observed failure transcript. Train the action policy on counterfactual, kernel-verified retry outcomes rather than traced proof-core labels, and test it against the best equal-compute static portfolio on random held-out Lean goals.

This preserves the best insight in the current work while changing the paper from a trace-recovery method into a claim about **the value of online information under bounded proof search**.

---

## 2. Literature Search and Threat Model

### 2.1 Reviewer threat model

A strong reviewer will attack the paper along six axes.

| Threat | Likely reviewer question | Required response |
|---|---|---|
| **Direct-system validity** | Why is this not evaluated inside the official LeanHammer pipeline? | Integrate the method with official LeanHammer and report kernel-verified solve rate. |
| **Budget fairness** | Does the method win only because it gets retries or more wall-clock? | Compare to the best static multi-\(k\), multi-selector portfolio with identical calls and total wall-clock. |
| **Metric validity** | Why should human proof-core coverage predict a prover’s proof success? | Make proof success primary; quantify coverage–success discordance rather than assuming alignment. |
| **Feedback causality** | Is the gain actually due to failure content, or merely a second learned stage? | True/masked/shuffled/counterfactual-feedback controls with identical capacity and history. |
| **Novelty crowding** | Compiler/verifier feedback is already central in APRIL, APOLLO, OProver, VERITAS, and process-verified RL. What is new? | Narrow the novelty to per-instance, online premise-set intervention for a hammer, with a formal adaptive-versus-static separation. |
| **Historical prior** | ATP systems have long used feedback, axiom schedules, and learned premise selection. | Cite MaLARea, ATPboost, stateful premise selection, and strategy scheduling; claim a Lean-specific online conditional intervention problem, not invention of feedback loops. |

### 2.2 Primary literature map

The table below separates direct competitors from adjacent work. Links point to primary papers, OpenReview pages, official project pages, or official repositories.

| Work | Date / venue / status | What it claims | Why it threatens or supports this paper | Required comparison or wording |
|---|---|---|---|---|
| **[Premise Selection for a Lean Hammer](https://openreview.net/forum?id=m04JJNeRK6)**; [paper](https://arxiv.org/abs/2506.07477); [LeanHammer repo](https://github.com/JOSHCLUNE/LeanHammer) | ICLR 2026 **Oral** | Introduces LeanPremise and the first end-to-end domain-general Lean hammer; evaluates on held-out Mathlib and miniCTX-v2 with kernel-verified proof rate, multiple hammer settings, and tuned premise counts. | This is the strongest direct competitor and the evaluation standard the current paper does not meet. It also tunes the number of premises, so “more premises can hurt” is not new by itself. The repository exposes a premise-selection API and detailed traces, making integration feasible. | Use official LeanHammer as the primary backend. Compare against its default selector, MePo, tuned static \(k\), and an equal-compute static portfolio. State that the novelty is **feedback-conditioned per-goal intervention after a failed call**, not premise selection, retrying, or tuning \(k\). |
| **[LeanSearch v2: Global Premise Retrieval for Lean 4 Theorem Proving](https://arxiv.org/abs/2605.13137)**; [repo](https://github.com/frenzymath/LeanSearch-v2) | arXiv, May 2026 | Standard embedding-reranker mode and a reasoning mode for global whole-theorem premise retrieval; reports stronger group recovery and downstream proof success in a fixed prover loop. | It is the strongest threat to claims about global imported-premise retrieval. Its reasoning mode is a real iterative decompose/retrieve/filter/judge system, not a lexical expansion heuristic. | Rename the current `leansearch_iterative` row to **controlled iterative lexical proxy** or remove it. Never present it as LeanSearch v2. Where protocol-compatible, use official LeanSearch v2 standard/reasoning output as a frozen selector expert, with retrieval cost accounted for. |
| **[LeanDojo: Theorem Proving with Retrieval-Augmented Language Models](https://openreview.net/forum?id=g7OX2sOJtn)** | NeurIPS 2023 Datasets & Benchmarks **Oral** | Open infrastructure, fine-grained proof/premise annotations, a large Lean benchmark, and ReProver, a retrieval-augmented tactic prover. | Establishes the standard trace-supervised retrieval/proving setting and a recognized end-to-end baseline. | Position trace-core data as standard supervision, but acknowledge that a second-stage controller trained to recover the human route is stronger supervision than a verifier-outcome controller. Consider a ReProver transfer experiment only after LeanHammer. |
| **[Magnushammer: A Transformer-Based Approach to Premise Selection](https://openreview.net/forum?id=oYjPk8mqAV)** | ICLR 2024 Poster | Strong neural premise selection for Isabelle/Sledgehammer; shows large proof-success gains and complementarity with a language-model prover. | Demonstrates that a premise-selection paper can be top-tier when it has end-to-end proof impact, scale, and a strong retrieval contribution. It also reinforces that recall metrics alone are not enough. | Cite as broader hammer precedent. Do not imply Lean premise control is the first learned hammer adaptation. |
| **[Tree-Based Premise Selection for Lean4](https://openreview.net/forum?id=omyNP89YW6)** | NeurIPS 2025 Poster | Training-free structural premise selection using expression trees, WL screening, tree edit distance, and related structural measures. | Provides a credible non-neural, structurally distinct selector expert. It raises the baseline bar for “visible features” and makes an expert-gating route more plausible. | Include it as a frozen structural expert in a selector-switch action if code and version permit. At minimum, compare conceptually and avoid claiming name/statement features cover structural premise selection. |
| **[Assisting Mathematical Formalization with a Learning-based Premise Retriever](https://arxiv.org/abs/2501.13959)** | arXiv, Jan. 2025 | Formal-language BERT pretraining, bi-encoder retrieval, cross-encoder reranking, and integration with a tactic generator. | Another learned Lean premise retriever with downstream proving, weakening novelty claims around two-stage learned retrieval. | Say the contribution is not another retriever or reranker. Freeze a strong first-stage selector and study post-failure action value. |
| **[LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction](https://openreview.net/forum?id=eTmOwvvRu9)** | TMLR, accepted Dec. 2025 | Predicts proof progress and improves ReProver best-first search on Mathlib. | Supports the premise that post-state signals can guide search, but threatens broad claims that static retrieval is the only alternative. | Contrast proof-state search guidance with **premise-set interventions after a hammer failure**. Consider progress features only as optional controller inputs, not a main contribution. |
| **[REAL-Prover: Retrieval Augmented Lean Prover for Mathematical Reasoning](https://arxiv.org/abs/2505.20613)** | arXiv v3, Nov. 2025 | Open retrieval-augmented stepwise Lean prover with results on ProofNet and FATE-M. | Shows a crowded retrieval-augmented proving landscape and that downstream proof success is standard. | Do not market “retrieval plus proving” as novel. Use it for positioning, not as the primary direct baseline. |
| **[Duper: A Proof-Producing Superposition Theorem Prover for Dependent Type Theory](https://doi.org/10.4230/LIPIcs.ITP.2024.10)**; [repo](https://github.com/leanprover-community/duper) | ITP 2024 | Proof-producing superposition prover for Lean, designed for direct tactic use and hammer reconstruction. | Supports the need to analyze backend-specific search and reconstruction behavior. | Report which LeanHammer backend consumes each premise set and whether gains transfer across Zipperposition/Duper/Aesop-related modes. |
| **[Lean-auto: An Interface between Lean 4 and Automated Theorem Provers](https://arxiv.org/abs/2505.14929)** | CAV-era work / arXiv 2025 | Sound translation interface from Lean 4 to ATPs and general ATP-based automation. | Makes actual end-to-end premise injection possible and highlights translation/reconstruction failure as separate from retrieval. | Log translation, ATP, and reconstruction outcomes separately. Do not collapse them into a generic missing-premise label. |
| **[Learning to Repair Lean Proofs from Compiler Feedback](https://arxiv.org/abs/2602.02990)** (APRIL) | arXiv v2, Mar. 2026 | Supervised proof repair from erroneous proof text and compiler diagnostics, with a large error/repair dataset. | Directly occupies the broad statement “Lean failure feedback is useful supervision.” | Restrict novelty to premise-action selection for a hammer. Explicitly say FAR-Hammer does not edit proof text and is not a general proof-repair method. |
| **[Process-Verified Reinforcement Learning for Theorem Proving via Lean](https://openreview.net/forum?id=P00k4DFaXF)** | ICLR 2026 Poster | Uses Lean as a symbolic process oracle, with tactic-level verified feedback and first-error credit assignment during RL. | Occupies verifier feedback as a training signal and gives a much broader learning story. | Do not claim first use of Lean failures as supervision. Emphasize counterfactual action outcomes for bounded premise control. |
| **[APOLLO: Automated LLM and Lean Collaboration for Advanced Formal Reasoning](https://openreview.net/forum?id=fxDCgOruk0)**; [repo](https://github.com/aziksh-ospanov/APOLLO) | NeurIPS 2025 Poster | Modular compiler-guided proof repair and automated solver/LLM collaboration under a controlled attempt budget. | Shows that compiler-guided iterative repair already yields large end-to-end gains. | Contrast its proof-text/subgoal repair actions with a fixed-backend premise intervention action space. |
| **[OProver: A Unified Framework for Agentic Formal Theorem Proving](https://arxiv.org/abs/2605.17283)** | arXiv, May 2026 | Large proof/feedback/retrieval corpus, multi-round compiler-feedback repair, retrieval grounding, and strong whole-proof results. | A severe novelty threat to any generic “feedback-conditioned refinement” framing. Its ablations directly show feedback and retrieval synergy. | State that the paper studies a narrower control problem where the proof generator/backend is frozen and only the premise interface changes. Include a same-capacity feedback ablation. |
| **[VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving](https://arxiv.org/abs/2606.19399)** | arXiv, June 2026 | Two-phase verifier-guided proof search with critic-guided MCTS, monotonic preservation of first-phase successes, and compute-aware analysis. | A severe threat to “feedback plus a second stage” and to the claim that flat additional attempts can hurt. It already gives a baseline-preserving two-phase design. | Do not use “monotonic two-stage feedback search” as the novelty. Differentiate by proving **adaptive premise-action value** under a fixed hammer and matched compute. |
| **[Optimizing the Cost-Quality Tradeoff of Agentic Theorem Provers in Lean](https://arxiv.org/abs/2606.04883)** | arXiv v2, June 2026 | A control plane observes failed trajectories and routes whether to continue or terminate/restart based on cost and success estimates. | Directly threatens a generic learned action-router story. | The action space must remain premise-specific: shrink, expand, selector switch, rescue, or abstain. The central result must be action-rank crossing among premise interventions, not generic retry allocation. |
| **[Distilling LLM Feedback for Lean Theorem Proving](https://arxiv.org/abs/2605.30861)** | arXiv, May 2026 | Distills privileged feedback into token-level training and improves pass@\(k\) scaling. | Reinforces that “feedback as supervision” is a crowded general theme. | Mention as adjacent process supervision. Avoid broad feedback-learning claims. |
| **[What Helps Agentic Lean Provers? A Trace-Level Attribution Study](https://openreview.net/forum?id=ShhLinF41r)** | ICML 2026 AI4Math Workshop Poster | Trace-level ablations suggest compiler feedback helps while richer retrieval/tools do not automatically improve proof success. | Supports the need for attribution and controlled ablations, but is not a direct premise-selection competitor. | Use it to motivate true/masked/shuffled feedback controls and route-level attribution. Do not rely on it as a primary baseline. |
| **[ATPboost: Learning Premise Selection in Binary Setting with ATP Feedback](https://arxiv.org/abs/1802.03375)** | IJCAR-era work / arXiv 2018 | Interleaves ATP runs with learning premise relevance from discovered proofs. | Historical prior for premise learning from ATP feedback. | Explicitly distinguish **cross-problem/offline learning from successful proofs** from **within-problem online adaptation to a failed call**. |
| **[MaLARea: A Metasystem for Automated Reasoning in Large Theories](https://ceur-ws.org/Vol-257/05_Urban.pdf)** | 2007 workshop/proceedings era | Cycles ATP attempts, learned axiom relevance, axiom-count schedules, and time schedules across large-theory problems. | Historical prior for adaptive axiom limits, retries, and learned prover control. | Do not claim that closed-loop premise scheduling is conceptually unprecedented. Claim a modern Lean, per-instance, failure-conditioned and kernel-verified formulation. |
| **[Stateful Premise Selection by Recurrent Neural Networks](https://arxiv.org/abs/2004.08212)** | LPAR-era work / arXiv 2020 | Sequentially selects premises with an evolving state rather than independent top-\(k\) ranking. | Threatens language such as “the first stateful premise selector.” | Say the state is specifically the **observed prover failure transcript** and the action is an intervention on a complete premise set. |
| **[SorryDB: Can AI Provers Complete Real-World Lean Theorems?](https://arxiv.org/abs/2603.02668)** | arXiv, Mar. 2026 | Dynamic real-world Lean tasks from active projects; reports that iterative feedback is a major performance factor. | Supports external validity but can pull the work toward benchmark engineering. | Use only as a secondary transfer set after the main Mathlib/miniCTX-v2 result. Do not make dataset evaluation the contribution. |

### 2.3 The most dangerous novelty collision

The following broad claim is no longer defensible as a headline:

> “Failure feedback is useful for theorem proving.”

APRIL, process-verified RL, APOLLO, OProver, VERITAS, feedback distillation, and cost-aware routing all occupy that space. The historical ATP literature also prevents claiming a new feedback loop for premise selection in general.

The remaining defensible novelty is narrower and stronger:

> **For a fixed Lean hammer and fixed first attempt, the failure transcript changes which premise-set intervention has highest verified value; this per-instance action-rank crossing creates a measurable adaptive advantage over every failure-agnostic equal-compute portfolio.**

That claim is not established by the current paper, but it is testable.

### 2.4 Baseline wording that must change now

1. Rename `leansearch_iterative` to **`controlled_iterative_lexical`** or **`lexical_expansion_proxy`**.
2. Remove “LeanSearch-style” from table labels. A footnote is not sufficient when the method name visually suggests a system comparison.
3. Refer to LeanSearch v2 as a separate published system with standard and reasoning modes.
4. Call `learned_base_fallback` the strongest **in-protocol failure-agnostic baseline**, not the strongest global premise-selection baseline.
5. Call bridge success a **replay-filtered trace-recovery metric** unless the selected premise set is actually passed to the prover/replay process.
6. State in the abstract or method that both the first-stage retriever and current second-stage controller use traced proof-core supervision.

---

## 3. What Is the Oral-Level Idea?

### 3.1 Is “failure feedback as conditional evidence” enough?

**No.**

It is a good organizing intuition, but by 2026 it is too expected and too broad. A reviewer can accept the intuition while rejecting the paper because:

- failure feedback already powers proof repair, agentic search, process supervision, and routing;
- the current experiments do not isolate the incremental information in the failure signal;
- trace-core coverage is an indirect target;
- the adaptive method is not compared against the strongest static use of the same compute.

The stronger idea is not merely that feedback contains information. The stronger idea is:

> **Failure has operational value only when it changes the ranking of available actions. In bounded proof search, failures reveal a latent search regime, and different regimes require qualitatively different premise interventions.**

This is sharper than a mutual-information statement. Positive mutual information can exist without changing the optimal action and therefore without improving proof success.

### 3.2 Stronger replacement claim

Recommended new main claim:

> **Under a fixed LeanHammer backend and compute budget, traced-premise coverage is neither sufficient nor necessary for kernel-verified proof success. A first failed call reveals which premise intervention—shrink, expand, switch selector, rescue, or stop—has highest conditional value. A controller trained on counterfactual verified retry outcomes captures this adaptive value and outperforms the best equal-compute static portfolio on random held-out goals.**

This claim has four parts that must all be tested:

1. **Metric separation:** traced-route coverage and proof success disagree.
2. **Action-rank crossing:** different failures imply different best retry actions.
3. **Feedback causality:** true feedback beats masked and shuffled feedback.
4. **System impact:** the learned policy improves verified proof rate or the solve-rate/compute frontier.

### 3.3 Lean’s equivalent of “restoration lies”

The best phrase is:

> **Proof-core coverage lies.**

More precise wording for the paper:

> **Human trace-core coverage is not proof success.**

It “lies” in two directions:

- **Not sufficient:** a premise set can contain every premise in a human trace and still cause timeout, translation failure, reconstruction failure, or search explosion under a bounded backend.
- **Not necessary:** a prover can find a different verified proof using premises outside the human trace, so failure to recover that trace does not imply theorem-proving failure.

This is stronger than “retrieval recall lies” because it identifies the exact target currently used by the paper. It must not be presented as a discovery that irrelevant premises can hurt; hammer researchers have known that for years. The surprising part must be the **frequency, direction, and actionability of trace/proof discordance in a modern Lean hammer**.

### 3.4 Evidence hierarchy

Use the following hierarchy as a conceptual contribution. It is an **evidence hierarchy**, not a chain of logical implications.

| Level | Name | Question | Current paper status |
|---:|---|---|---|
| 0 | **Accessibility** | Is a useful premise present in the candidate pool? | Strong on inspected bridge misses: 0/17 pool misses, but on a selected subset. |
| 1 | **Traced-route coverage** | Does the selected set contain the premises used by one known human proof? | Main current metric. |
| 2 | **Replay compatibility** | Does a known script still replay in the current environment? | Current bridge filter. |
| 3 | **Search tractability** | Can the chosen backend explore the induced search space within the fixed budget? | Only indirectly/synthetically tested now. |
| 4 | **Independent verified success** | Does the backend discover a kernel-verified proof from the supplied premises? | Missing as a main result. |
| 5 | **Conditional intervention value** | Given a failure transcript, which premise action maximizes verified reward per compute? | Proposed Oral-level contribution. |

A cleaner name for the mismatch is **the coverage illusion**:

> A selector looks better because it recovers more of a reference proof, while the actual bounded prover is no more likely—or is less likely—to verify the theorem.

### 3.5 What would make the insight surprising?

The paper becomes surprising only if it shows all or most of the following:

1. **Real reversal:** on actual LeanHammer calls, increasing trace-core recall or premise count causes a meaningful number of success-to-failure flips at matched time.
2. **Alternative-proof quadrant:** a nontrivial number of verified proofs occur without full human trace-core coverage.
3. **Static portfolio defeated:** an adaptive policy beats the best globally tuned schedule that uses the same number of calls, selectors, premise budgets, and wall-clock.
4. **Shrink is essential:** some failures are recovered only by removing premises; expansion-only policies leave verified solves on the table.
5. **Failure content matters:** true failure transcripts beat masked, shuffled, or generic “attempt failed” tokens with identical model capacity.
6. **Action crossing is large:** the oracle per-goal action policy has a substantial gap over the best fixed action. If the oracle gap is tiny, there is no Oral-level adaptive-control problem.
7. **Transfer:** the same learned policy or policy family improves a second selector, LeanHammer mode, or miniCTX-v2 split without retuning on test labels.

---

## 4. Route Evaluation

Scores below refer to **potential if executed well**, not current evidence.

| Route | Oral potential | Feasibility | Required experiments | Theoretical depth | Novelty risk | Baseline risk | Kill criteria |
|---|---:|---:|---|---|---|---|---|
| **A. Keep current idea and add end-to-end proof success** | 6/10 | 7/10 | Official LeanHammer integration; random held-out goals; equal-compute static schedules; miniCTX-v2 transfer | Moderate unless paired with a value-of-information framework | Medium: feedback is crowded | High: LeanHammer default and tuned portfolios may erase gains | <2 pp verified gain; confidence interval crosses zero; gain disappears under matched calls/wall-clock |
| **B. Reframe as “retrieval recall / proof-core coverage lies”** | 3/10 alone; 7/10 with a method | 8/10 | Real coverage–success quadrants; success-to-failure intervention pairs; backend search statistics; alternative proof extraction | Moderate if it proves non-necessity/non-sufficiency and predicts reversals | High if merely diagnostic; classical ATP already knows premise overload | Medium | Discordant cases are rare, synthetic, or cannot be repaired by a principled policy |
| **C. Develop a deeper theory of conditional proof search** | 3/10 alone; 7/10 paired | 6/10 | Counterfactual action matrix; oracle adaptive gap; feedback ablations; budget sweep | Potentially strong: value of information, regime separation, gate regret | Medium: generic contextual decision theory is standard | Medium | Optimal actions do not cross by failure state; theory only restates mutual information or existence |
| **D. Build a learned calibrated expert-gate method** | 5/10 | 6/10 | Frozen experts; counterfactual verified labels; calibration; oracle headroom; selector-transfer | Moderate | High: routing/cascades are crowded; cost-router paper is close | High: a static union/interleave may match it | Oracle expert gap <3 pp; learned gate captures <30% of oracle gap; gains require test-set tuning |
| **E. Pivot to failure-supervised action/model training** | 7/10 | 4/10 | Failure-action dataset; action model; end-to-end proof success; feedback causality; generalization | Moderate to strong | Very high due OProver, VERITAS, APRIL, process RL | High | Contribution becomes generic proof repair or generic agent routing; no premise-specific advantage |
| **F. Keep current project as a solid accept rather than Oral** | 1/10 | 9/10 | Random bridge sanity; stronger wording; true/masked feedback ablation; one official external baseline | Limited | Medium | Medium | Even accept route is weak if feedback ablation fails or proxy naming remains misleading |
| **G. Verified counterfactual premise interventions** **(recommended)** | **8/10** | **6/10** | Full action grid after fixed failure; verified-outcome policy; equal-compute LeanHammer test; coverage-discordance map; transfer | **Strong if centered on adaptive value and action-rank crossing** | Medium: action routing is known, but premise-specific counterfactual control is narrower | High but addressable with static portfolios and official systems | Oracle adaptive gap <3 pp; true feedback no better than shuffled; learned policy <2 pp over best static; no transfer |
| **H. Restart around backend-agnostic failure semantics** | 7/10 | 2/10 | Unified failure representation across LeanHammer, ReProver, and LLM prover; intervention transfer | Potentially strong | Very high and broad | Extreme | No cross-backend invariants; engineering overwhelms scientific claim |

### Route-by-route adversarial comments

#### A: End-to-end alone is necessary but not sufficient

This is the minimum credible upgrade. It could produce a strong main-track paper, but not automatically an Oral. A 2–3 point proof-rate gain from another retriever/controller can be viewed as a competent system improvement. Oral potential requires the causal and conceptual result: a feedback-conditioned policy separates from every equal-compute static portfolio.

#### B: “Coverage lies” must remain attached to an intervention

A pure diagnosis paper risks becoming evaluation work, which violates the project goal and has limited Oral upside. Use the hierarchy to explain why the old target is insufficient, then introduce a method that acts on the discovered mismatch.

#### C: Theory should formalize **action value**, not entropy

The current mutual-information proposition is true but nearly tautological. The useful theoretical quantity is the gap between:

\[
\mathbb{E}_F\left[\max_a \mu_a(F)\right]
\quad \text{and} \quad
\max_a \mathbb{E}_F[\mu_a(F)],
\]

where \(a\) is a premise intervention and \(\mu_a(F)\) is verified utility after failure \(F\). This gap is zero unless action rankings cross across failure states.

#### D: A calibrated gate is only interesting if the experts have counterfactual complementarity

The 0/17 pool-miss result suggests ranking headroom, but it does not establish expert complementarity. First collect the full action-outcome matrix. If the per-goal oracle over learned, base, MePo, structural, expand, and shrink actions barely beats the best static action, stop. Do not spend another cycle hand-designing expert mixtures.

#### E: Keep the pivot narrow

A general “failure-supervised action model” collides with agentic theorem proving. It becomes defensible if the proof generator and backend remain frozen and the only learned control is over premise interventions.

#### F: Solid accept route

The current work can plausibly become a stronger main-track submission without an Oral push, but only after fixing causal attribution and proxy naming. A reasonable accept-oriented version would treat trace-core recovery as the task, make no system-level LeanSearch comparison, add random bridge data, and soften all general proof-search claims.

#### G: Why it is the best route

It reuses the current infrastructure, turns the strongest limitation into the new contribution, has an early oracle kill test, and creates a clean theory–experiment alignment. It also offers a direct answer to the strongest reviewer: “Does this improve actual Lean proving, or only recover the proof trace?”

---

## 5. Recommended Strategy

### 5.1 Primary strategy: Verified Adaptive Premise Interventions

Working method name:

> **APIC-Hammer: Adaptive Premise Intervention Control for LeanHammer**

The name is optional; the scientific object is more important than branding.

#### New main claim

> After a fixed failed LeanHammer call, the best next premise set is failure-dependent and non-monotonic. A controller trained on counterfactual kernel-verified retry outcomes—not human trace-core labels—selects premise interventions that improve verified theorem-solving over the strongest static equal-compute portfolio.

#### Why this is better than the current story

- It makes **verified proof success** the target.
- It removes the strongest supervision critique from the second-stage controller.
- It forces fair comparison to static retries.
- It turns “more premises can hurt” from a synthetic observation into a real action-selection problem.
- It provides a nontrivial theory: the value of feedback exists only when conditional action rankings cross.
- It remains a method paper, not a benchmark paper.
- It is distinguishable from proof repair and agentic generation because the proof backend is frozen.

### 5.2 Backup strategy: End-to-end FAR-Hammer + coverage-illusion analysis

If the verified-outcome action dataset is too costly, retain the current controller but:

1. integrate it with official LeanHammer;
2. make verified proof success primary;
3. compare to equal-compute static portfolios;
4. add true/masked/shuffled feedback controls;
5. use the coverage hierarchy as the conceptual frame;
6. move most trace-core experiments to the appendix.

This backup can become a strong accept. Its Oral ceiling is lower because the controller still optimizes a traced route.

### 5.3 Title options

Ranked from safest to most provocative:

1. **Proof-Core Coverage Is Not Proof Success: Failure-Conditioned Premise Interventions for Lean Hammers**
2. **When More Premises Hurt: Adaptive Premise Control for Lean Hammers**
3. **Beyond Retrieval Recall: Verified Failure-Conditioned Premise Control in Lean**
4. **Failure Reveals the Search Regime: Closed-Loop Premise Selection for Lean Hammers**
5. **Adaptive Premise Interventions under Bounded Proof Search**
6. **The Coverage Illusion in Lean Premise Selection**

Avoid using “lies” in the final title unless the real end-to-end reversal evidence is overwhelming.

### 5.4 Central figure

Replace the current page-3 pipeline diagram with a two-panel figure.

**Panel A: Coverage–success discordance**

A 2×2 matrix over real LeanHammer calls:

| | Verified failure | Verified success |
|---|---:|---:|
| Full human trace-core covered | **Coverage illusion** | Expected alignment |
| Human trace-core not covered | Expected failure | **Alternative proof** |

Annotate counts and representative pairs where adding premises raises trace-core coverage but changes success from 1 to 0.

**Panel B: Adaptive action loop**

Fixed initial selector → first LeanHammer call → structured transcript → action gate → one of `{shrink, expand, selector swap, interleave, rescue, abstain}` → kernel verification.

The visual should make clear that the controller changes only the premise interface, not the theorem, proof generator, or backend.

### 5.5 Central table

The primary table must be end-to-end and equal-compute:

| Policy | Mathlib verified % | miniCTX-v2 verified % | FFR | Median wall-clock | Calls | Timeout % |
|---|---:|---:|---:|---:|---:|---:|
| LeanHammer default | | | | | | |
| Best static \(k\) | | | | | | |
| Best static multi-action portfolio | | | | | | |
| Blind expansion | | | | | | |
| Current trace-supervised controller | | | | | | |
| APIC, masked feedback | | | | | | |
| APIC, shuffled feedback | | | | | | |
| **APIC, true feedback** | | | | | | |
| Oracle adaptive action | | | | | | |

Do not lead with the 92.9% trace-core number after this pivot.

### 5.6 Minimum decisive experiment

**Primary benchmark:** the official LeanHammer Mathlib-test split if reproducible, plus a separately frozen random held-out set of at least 500 theorems grouped by module.

**Protocol:**

- First attempt is identical for every method.
- One or two retries are allowed.
- Every method gets the same maximum number of LeanHammer calls and the same total wall-clock cap.
- The static portfolio is tuned on validation and can use the same action set in a fixed order.
- Controller training uses only training/validation counterfactual retry outcomes.
- Test goals are never used to choose actions, thresholds, \(k\), or experts.
- Primary metric is kernel-verified proof success.
- Use paired bootstrap confidence intervals and an exact paired test such as McNemar.
- Run the official LeanHammer `auto` or premise-sensitive mode as the mechanistic primary, then confirm in `full`.

**Success threshold for the Oral route:**

- at least **+4.0 absolute verified proof-rate points** over the strongest equal-compute static portfolio on the primary set;
- paired 95% confidence interval excluding zero;
- true feedback clearly above masked and shuffled feedback;
- positive result on miniCTX-v2 or a second frozen selector/backend mode;
- no worse compute frontier.

A smaller gain can still support a main-track paper, but not the intended Oral story.

### 5.7 Strongest expected reviewer objection and answer

**Objection:**  
“This is just a supervised router that gets extra attempts. LeanHammer already tunes premise count, agentic provers already use feedback, and your policy may simply memorize which retry action works.”

**Answer required by the experiments:**  
All methods receive the same initial attempt, action set, calls, and wall-clock. The strongest baseline is a validation-tuned static portfolio over the same actions. The controller is trained on kernel-verified counterfactual outcomes, split by theorem/module, and tested on untouched goals. True feedback is compared to masked and within-stratum shuffled feedback under the same architecture. The paper measures the oracle adaptive gap and action-rank crossings, showing that no fixed schedule can realize the observed gains. Transfer to a second selector or miniCTX-v2 demonstrates that the policy is not a lookup table.

---

## 6. Required Experiments

### 6.1 Execution-ready experiment table

| Priority | Experiment | Goal | Exact protocol | Baselines | Metrics | Expected positive outcome | Negative outcome interpretation | Difficulty |
|---:|---|---|---|---|---|---|---|---|
| **P0** | **Feedback-content causal ablation on current pipeline** | Determine whether current gains actually come from failure information | On all four existing 500-goal splits, retrain/evaluate identical second-stage models with: true failure fields; failure fields masked; failure label replaced by generic FAILED; labels shuffled within split and matched by first-attempt budget/rank profile; history-only; goal/candidate-only. Keep seeds, features, and supervision identical. | Current second-stage, learned+base fallback | Trace success, FFR, paired per-goal delta, calibration | True feedback wins by at least 2–3 pp consistently and shuffled feedback loses most of the gain | If masked/shuffled matches true feedback, the current paper has not established conditional evidence; rename the method and do not build theory around feedback semantics | **S** |
| **P0** | **LeanHammer integration smoke test** | Verify that premise sets can be injected and failures parsed reliably | Pin Lean, Mathlib, LeanHammer, premise server/model versions. Run 100 validation theorems in `auto` and `full`. Inject custom premise lists using the official premise-selection API. Enable premise/debug/ATP/Aesop traces. Save exact command, premise set, statuses, elapsed time, and proof term/check result. | Official default LeanHammer; fixed custom selector | Reproduction stability, parse coverage, verified success, error taxonomy | ≥95% of calls produce machine-readable terminal status; custom premise interventions change the actual backend query; successful proofs kernel-check | If selected sets cannot be causally injected or traces are too incomplete, the project cannot support the proposed claim without Lean-side engineering | **M** |
| **P0** | **Counterfactual action-grid pilot** | Measure whether an adaptive problem exists before training a gate | On 300 validation goals that fail the common first attempt, run every pre-registered action under identical retry budget: keep; shrink-0.5; shrink-0.75; expand-1.5; expand-2.0; MePo swap/interleave; structural selector swap if available; base-rescue-8; stop. Hold backend fixed. | Best single action; best fixed two-action schedule | Per-action verified success, cost, pairwise complementarity, oracle adaptive success, action-rank crossing rate | Oracle per-goal action is ≥5 pp above best static action and ≥3 pp above best static schedule; shrink uniquely recovers a visible subset | If oracle gap <3 pp, no learned controller can produce an Oral-level adaptive win with this action set; redesign actions once, then stop | **M/L** |
| **P0** | **Strong static portfolio construction** | Prevent a false win from extra retries | On validation only, enumerate fixed schedules using exactly the same number of calls and actions as the adaptive policy. Optimize solve rate subject to the same total wall-clock, and separately optimize utility \(success-\lambda cost\). Freeze one schedule per budget before test. | Single best \(k\); blind expansion; LeanPremise+MePo accumulation; random action schedule | Verified success, wall-clock, calls, Pareto frontier | Static portfolio is strong but leaves a measurable oracle adaptive gap | If a simple fixed schedule matches the oracle or learned policy, failure-conditioned control is unnecessary | **M** |
| **P0** | **Verified-action controller training** | Replace traced-core supervision for the second-stage decision | Collect full action outcomes on 1,500–3,000 training/validation failures. Train a small cost-sensitive action-value model to predict \(P(success\mid x,F,a)\) and expected cost. Inputs: goal/retriever statistics, first premise set, parsed failure/status, elapsed time, backend search statistics. Exclude trace-core labels. Calibrate on a held-out validation partition. | Majority action; best static action; trace-supervised current controller; uncalibrated model | Top-action accuracy, expected utility, Brier/ECE, captured oracle gap | Captures ≥50% of oracle adaptive gap; calibrated policy beats best static on validation | Poor capture means feedback representation or action set is inadequate; do not compensate with test-time heuristics | **L** |
| **P0** | **Decisive equal-compute Mathlib end-to-end test** | Establish actual theorem-proving improvement | Use official 500-theorem Mathlib-test where possible, plus ≥500 untouched random held-out theorems grouped by module. Identical first call. Allow fixed retry count. Match total wall-clock and calls. Run LeanHammer premise-sensitive mode and confirm in `full`. Freeze all choices. | Official default; tuned single \(k\); best static schedule; blind expansion; LeanPremise+MePo static portfolio; current fallback; masked/shuffled gate | Kernel-verified solve rate, FFR, wall-clock, CPU, calls, timeout, translation/ATP/reconstruction status, unique premises | ≥4 pp over strongest static portfolio, CI excludes 0; true feedback wins; positive `full` confirmation | <2 pp or no significance means no Oral-level system claim; only cost-frontier or diagnostic story remains | **XL** |
| **P1** | **Coverage–success discordance map** | Validate “proof-core coverage is not proof success” on real backend runs | For every goal-action pair in the action grid, compute human trace-core coverage only as a diagnostic, plus verified success. Count four quadrants and paired changes where coverage rises while success falls, or coverage falls while success rises. Manually audit 30 examples. | N/A; compare actions within goal | Quadrant rates, conditional success, reversal counts, search stats | Substantial covered-fail and uncovered-success mass; real intervention reversals; patterns predict action choice | If coverage and success are almost perfectly aligned, the conceptual pivot is weak and the current trace-core target is less problematic than claimed | **M** |
| **P1** | **Real search-space poisoning instrumentation** | Replace synthetic timeout evidence with backend evidence | For nested premise sets \(P_k\subset P_{2k}\), run same backend, seed, and budget. Log generated/processed clauses, active/passive set sizes, heartbeats, translation time, reconstruction time, and terminal status. Analyze success-to-timeout flips. | Small \(k\), large \(k\), shrink after timeout | Verified success, timeout, search statistics, clause growth | Larger sets raise coverage yet cause real search/reconstruction failures; shrink recovers a meaningful subset | If no real reversals appear, remove strong “more premises hurt” language and treat timeout stress as synthetic only | **M/L** |
| **P1** | **True versus shuffled transcript under matched strata** | Rule out distribution leakage in feedback | Shuffle full parsed transcripts only among goals matched on initial selector, premise count, score histogram, elapsed-time bin, and coarse terminal class. Also permute individual fields. Evaluate frozen gate. | True, masked, generic-failure, coarse-label, full-shuffled | Verified solve rate and action agreement | Fine-grained true transcript provides additional gain beyond coarse failure occurrence | If coarse class or no feedback suffices, simplify claim to conditional control based on state/history rather than rich failure evidence | **M** |
| **P1** | **miniCTX-v2 transfer** | Show generalization beyond Mathlib training distribution | Train/tune only on Mathlib. Evaluate non-Mathlib miniCTX-v2 splits used by LeanHammer. Keep action grid and thresholds fixed. Report per-project results and aggregate. | LeanHammer default, static schedule, masked gate | Verified success, FFR, cost | Positive aggregate delta and no catastrophic project-level regressions | Failure implies overfitting to Mathlib trace/failure statistics; Oral probability falls sharply | **L/XL** |
| **P1** | **Selector/expert transfer** | Show the policy is not tied to one retriever | Repeat with frozen LeanPremise, MePo, and one structurally distinct selector; alternatively use LeanSearch v2 standard output where protocol-compatible. Train either one shared gate with selector ID or leave-one-selector-out. | Per-selector tuned static schedule | Verified success, relative gain, action distribution | Adaptive advantage persists for at least two selectors; leave-one-out retains part of gain | Gain only on the in-house retriever suggests correction of its idiosyncratic errors rather than a general principle | **L** |
| **P1** | **Backend-mode transfer** | Test whether feedback policy reflects search regime rather than one parser artifact | Primary evaluation in LeanHammer `auto`/premise-sensitive mode; secondary in `full`, and optionally isolated Aesop/Duper/Zipperposition pathways. Keep premise actions identical where possible. | Static schedule per mode | Verified success, status breakdown, action calibration | Same qualitative expand/shrink routing and positive delta in a second mode | Backend-specific gain is acceptable for a strong system paper but weakens the general theory and title | **L** |
| **P1** | **Budget sweep and adaptive-value curve** | Test theory predictions about bounded search | Evaluate at 25%, 50%, 100%, and 200% of the primary call/time budget. Refit no test parameters. Plot default, best static, learned adaptive, oracle adaptive. | Same policies | Solve rate, cost frontier, oracle/static gap | Adaptive gap is largest at constrained intermediate budgets and shrinks at very large budgets | No budget region with separation means the action policy has little practical value | **M/L** |
| **P1** | **Alternative-proof analysis** | Establish that trace-core recovery is not necessary | For verified successes without full human trace-core coverage, extract backend-used premises or reconstructed proof dependencies. Confirm that a different valid route was found and rule out trace extraction bugs. | Human trace core | Number of genuine alternative proofs, dependency overlap | Nontrivial verified alternative routes; trace core is demonstrably route-specific | If all cases are trace-label errors, only non-sufficiency remains; weaken “neither necessary nor sufficient” | **M** |
| **P2** | **Random bridge continuity check** | Preserve continuity with current results without overclaiming | Sample 500 random goals before selecting disagreements. Report current trace-core and replay-filter metrics for all policies, with subset-selection procedure fixed. | Current baselines | Trace core, replay filter, selection prevalence | Ordering broadly persists but with smaller, honest effect sizes | If effect vanishes, current bridge result is selection-amplified and should move entirely to appendix | **S/M** |
| **P2** | **Residual calibration study** | Test the current 0/17 pool-miss diagnosis at scale | On all replay-verified and end-to-end failures, compute candidate coverage at large \(K\), rank of useful/used premises where available, confidence, and action regret. | Current final-base8, verified gate | Pool miss, rank miss, calibration error | Rank/calibration remains dominant and is reduced by verified gate | Candidate generation dominates at scale, requiring a retriever contribution rather than a controller paper | **M** |

### 6.2 Order of execution

The first four experiments are a funnel:

1. **Does current feedback content matter?**
2. **Can LeanHammer premise interventions be executed and observed?**
3. **Is there oracle adaptive headroom?**
4. **Can a learned policy capture it?**

Do not proceed to a large test run until the oracle action-grid pilot shows sufficient headroom.

### 6.3 Statistical requirements

- Freeze the test set and action grid before final evaluation.
- Split by theorem and preferably by module/import cluster to reduce near-duplicate leakage.
- Use theorem-level paired bootstrap confidence intervals.
- Use McNemar’s exact test for paired success differences.
- Report absolute points, not only relative improvement.
- Report the number of goals solved uniquely by each policy.
- Report all compute: wall-clock, CPU/GPU, Lean calls, ATP calls, and retrieval latency.
- For multiple budgets or modes, predeclare one primary comparison and treat the rest as supporting.
- Do not select the best seed on test. Report all seeds or deterministic training plus bootstrap uncertainty.

---

## 7. Theory Upgrade

### 7.1 Why the current theory is insufficient

The existing propositions are not wrong, but they are too weak:

- The mutual-information identity only says information reduces entropy when it is informative.
- The existence of \(P_1\subset P_2\) where the larger set times out is nearly definitional under a bounded search model.
- The guardrail proposition is a verbal description of one heuristic ablation.

None of these explains when feedback changes the optimal action, quantifies available adaptive gain, or predicts the shape of the experimental results.

### 7.2 Proposed formal framework

Fix an initial premise-selection and prover policy \(\pi_0\). For goal \(G\), it produces premise set \(P_0\), transcript \(T_0\), and either success or failure. Condition on first-attempt failure.

Let:

- \(X\): goal, candidate, retriever, and first-attempt summary available before seeing the failure;
- \(F=\phi(T_0)\): parsed failure observation;
- \(\mathcal{A}\): finite set of retry premise interventions;
- \(P_a=m_a(P_0,X,F)\): premise set induced by action \(a\);
- \(Y_a\in\{0,1\}\): potential outcome that the fixed backend returns a kernel-verified proof under action \(a\);
- \(C_a\ge 0\): cost of action \(a\);
- \(R_a=Y_a-\lambda C_a\): utility;
- \(\mu_a(x,f)=\mathbb{E}[R_a\mid X=x,F=f]\).

A **static retry policy** chooses \(a\) from \(X\) but not \(F\). A **failure-adaptive policy** chooses \(a\) from \((X,F)\).

For a clean theoretical comparison, absorb any fixed multi-call schedule into one compound action. This lets the static baseline use the same number of calls and actions as the adaptive policy.

### 7.3 Theorem 1: Value of failure information

Define:

\[
V_{\text{adaptive}}
=
\mathbb{E}_{X,F}\left[\max_{a\in\mathcal{A}}\mu_a(X,F)\right],
\]

and

\[
V_{\text{static}}
=
\mathbb{E}_{X}\left[
\max_{a\in\mathcal{A}}
\mathbb{E}_{F\mid X}[\mu_a(X,F)]
\right].
\]

Then:

\[
V_{\text{adaptive}}\ge V_{\text{static}}.
\]

The inequality is strict on any set of \(X\) with positive probability for which the utility-maximizing action changes across failure observations and the crossing has nonzero margin.

**Proof sketch.** For fixed \(X=x\), the expectation of a maximum is at least the maximum of expectations:

\[
\mathbb{E}_{F\mid x}\max_a\mu_a(x,F)
\ge
\max_a\mathbb{E}_{F\mid x}\mu_a(x,F).
\]

Integrate over \(X\). Strictness follows when no single action is optimal almost surely over \(F\).

**Why this matters.** It replaces “failure has mutual information” with a falsifiable operational condition: **conditional action rankings must cross**.

### 7.4 Corollary: Oracle adaptive headroom

Given full counterfactual action outcomes on validation goals, estimate:

\[
\widehat{\Delta}_{\text{adapt}}
=
\frac{1}{n}\sum_i\max_a R_{ia}
-
\max_a\frac{1}{n}\sum_i R_{ia}.
\]

This is the maximum empirical advantage available to any failure-conditioned gate over the best single static action in the logged action set. Extend the second term to the best fixed compound schedule for the true baseline.

This statistic should be computed **before model development**. It is a principled kill criterion.

### 7.5 Theorem 2: Expand–shrink separation

Consider two latent regimes after the initial failure:

- \(M\): useful information is missing; expansion succeeds and shrink fails.
- \(O\): the selected set overloads bounded search; shrink succeeds and expansion fails.

Let \(\Pr(M)=p\). A static one-action policy succeeds with at most:

\[
\max(p,1-p).
\]

Suppose a failure classifier predicts the regime correctly with probability \(q\), and the controller chooses expand for \(M\) and shrink for \(O\). Under symmetric classification accuracy, the adaptive success is \(q\). For \(p=1/2\), the adaptive advantage is:

\[
q-\frac{1}{2}.
\]

**Proof sketch.** Direct enumeration of the two regimes and two actions.

**Empirical prediction.** The adaptive advantage increases with regime heterogeneity and failure-classification accuracy; it disappears if all failures want the same action or feedback is independent of regime.

### 7.6 Theorem 3: Trace-core coverage is neither sufficient nor necessary

Let \(H\) be the premise set used by one human trace, and let \(S_B(P)\) denote whether a fixed backend verifies the theorem from premise set \(P\) under budget \(B\).

**Non-sufficiency.** There exist \(P\supseteq H\) such that \(S_B(P)=0\), because additional premises can cause bounded search or reconstruction to exceed \(B\), even though \(H\subseteq P\).

**Non-necessity.** If the theorem has an alternative proof core \(H'\) with \(H\nsubseteq H'\), there can exist \(P\supseteq H'\) with \(H\nsubseteq P\) and \(S_B(P)=1\).

**Proof sketch.** Construct a backend whose branching cost grows with irrelevant premises for the first statement. For the second, use a theorem with two independent derivations.

**Important qualification.** This theorem concerns coverage of **one reference trace**, not the existence of some sufficient premise set.

### 7.7 Theorem 4: Regret of a learned action gate

Suppose a learned model estimates all conditional action values with uniform error:

\[
|\widehat{\mu}_a(x,f)-\mu_a(x,f)|\le\epsilon
\quad \forall a,x,f.
\]

Let \(\widehat{\pi}(x,f)=\arg\max_a\widehat{\mu}_a(x,f)\), and let \(\pi^*\) be the Bayes-optimal adaptive action. Then the pointwise utility regret is at most \(2\epsilon\), and therefore expected regret is at most \(2\epsilon\).

**Proof sketch.** The estimated value of the selected action is at least that of the optimal action; apply the two estimation-error bounds.

**Empirical prediction.** Better calibration should close the gap to the oracle action policy. This gives a principled role for the residual rank/calibration analysis.

### 7.8 Optional model of bounded premise count

For regime \(r\), write verified success at premise count \(k\) as:

\[
S_r(k)=C_r(k)\,Q_r(k),
\]

where \(C_r(k)\) is the probability that a sufficient route is represented and \(Q_r(k)\) is the conditional probability that the backend finds and reconstructs a proof within budget. Typically \(C_r(k)\) is nondecreasing while \(Q_r(k)\) can decrease. Their product need not be monotone and can have a regime-dependent optimum.

This is useful intuition, but it should remain secondary to the action-value theory.

### 7.9 Empirical predictions generated by the theory

1. Shuffling failure transcripts within matched strata reduces performance.
2. Timeout/resource-out-like transcripts route disproportionately to shrink actions.
3. Missing-symbol or low-coverage-like transcripts route to expansion or selector switch.
4. The adaptive/static gap is largest at intermediate budgets.
5. At very large budgets, overload failures become rarer and the gap shrinks.
6. Goals with high action-value margin are easier to route and better calibrated.
7. The action oracle gap upper-bounds the learned gain.
8. A static union of all experts can underperform conditional expert selection.
9. Trace-core coverage and verified success have substantial off-diagonal mass.
10. If candidate accessibility is saturated, residual regret shifts to ranking, calibration, and backend tractability.

### 7.10 How theory changes the paper story

Old story:

> Failure has mutual information with premise utility, so condition a reranker on failure.

New story:

> A failed attempt creates a contextual decision problem. Feedback is useful only when it changes which intervention is optimal. We measure the oracle adaptive value, train a verified-outcome gate, prove its relation to static policies, and validate predicted expand/shrink/action-crossing behavior in a real Lean hammer.

This theory is deep enough for a strong paper **only if** the end-to-end action matrix shows a sizable adaptive gap and the learned policy captures it. Without that empirical separation, the theory is standard decision theory applied to a small heuristic.

---

## 8. Paper Rewrite Plan

### 8.1 Abstract

The abstract should contain five sentences in this order:

1. **Problem:** premise retrieval metrics optimize a reference route, but bounded hammer success depends jointly on coverage and search tractability.
2. **Phenomenon:** on real LeanHammer calls, trace-core coverage is neither sufficient nor necessary for verified success, and larger premise sets can reverse successes.
3. **Method:** after a fixed first failure, APIC-Hammer selects a premise intervention using the failure transcript; the second-stage policy is trained on counterfactual kernel-verified retry outcomes.
4. **Main result:** report verified solve-rate gain over the strongest equal-compute static portfolio on Mathlib and transfer.
5. **Mechanism:** true-feedback ablations, action-rank crossing, and expand/shrink routing establish that the gain is adaptive rather than extra compute.

Do not put 92.9% trace-core success in the opening abstract after the pivot. It can appear as supporting evidence in the appendix.

### 8.2 Introduction

#### Paragraph 1: The misaligned objective

Start from LeanHammer and the practical interface: a selector supplies premises to a bounded symbolic backend. State that retrieval quality and proof success are related but not identical.

#### Paragraph 2: Coverage illusion

Introduce the two failure directions:

- full human trace-core coverage but no verified proof;
- verified proof without full human trace-core coverage.

Use one real example from the new audit.

#### Paragraph 3: Failure as action information

The first failed call is not simply another label. It reveals which intervention is worth spending the remaining budget on.

#### Paragraph 4: Method

Describe fixed first attempt, structured transcript, finite intervention set, verified-outcome gate, and equal-compute evaluation.

#### Paragraph 5: Contributions

Use four contributions:

1. evidence hierarchy and real coverage–success discordance;
2. formal adaptive-versus-static value framework;
3. verified counterfactual premise intervention policy;
4. end-to-end LeanHammer gains and causal feedback ablations.

### 8.3 Related Work

Reorganize into four subsections:

1. **Lean hammers and premise selection:** LeanHammer first, then LeanSearch v2, LeanDojo/ReProver, Lean State Search, Tree-Based Premise Selection, Lean-auto/Duper.
2. **Learning and stateful premise selection:** Magnushammer, ATPboost, MaLARea, stateful RNN premise selection.
3. **Verifier feedback and proof repair:** APRIL, process-verified RL, APOLLO, OProver, VERITAS, feedback distillation.
4. **Adaptive computation and routing:** cost-quality router, progress prediction.

The current related-work section understates the directness of LeanHammer and omits historical feedback-based premise-selection systems. Fix both.

### 8.4 Problem Formulation

Replace trace-core recovery as the primary objective with:

\[
\max_\pi \mathbb{E}\left[\mathbf{1}\{\text{kernel-verified proof}\}
-\lambda\,\text{cost}\right]
\]

under a fixed initial policy and retry budget.

Define:

- static compound schedule;
- adaptive policy;
- intervention action set;
- failure transcript;
- verified reward;
- trace-core coverage as a diagnostic auxiliary variable.

### 8.5 Method

#### 8.5.1 Frozen initial selector and backend

Specify the exact LeanHammer version, mode, premise selector, premise count, timeout, and seed behavior.

#### 8.5.2 Failure representation

List exactly what is parsed:

- terminal class;
- elapsed time;
- ATP status;
- generated/processed clauses if available;
- translation/reconstruction status;
- Aesop/Duper/Zipperposition traces;
- first-set score/count statistics.

Distinguish native feedback from derived features.

#### 8.5.3 Intervention action set

Pre-register actions and justify each by a distinct failure hypothesis. Do not add actions after test inspection.

#### 8.5.4 Counterfactual data collection

Explain that every action is executed on training/validation failures, yielding full-information verified labels.

#### 8.5.5 Action-value model and calibration

Use a simple, inspectable model first. Report calibration and the cost utility. Avoid a large architecture contribution unless needed.

#### 8.5.6 Inference

One diagram and pseudocode: fixed first call, parse, gate, retry, verify.

### 8.6 Experiments

Use this order:

1. **Can trace-core coverage predict proof success?** Coverage quadrants.
2. **Is there adaptive headroom?** Best static vs oracle adaptive action.
3. **Main end-to-end result.** Equal-compute Mathlib test.
4. **Does feedback content matter?** True/masked/shuffled.
5. **Mechanism.** Action routing, real search statistics, shrink/expand cases.
6. **Transfer.** miniCTX-v2 and second selector/backend.
7. **Continuity with prior trace-core experiments.** One compact summary, remainder appendix.

### 8.7 Theory

Move theory before or immediately after the method. Include:

- value-of-failure theorem;
- expand–shrink separation;
- trace-core non-sufficiency/non-necessity;
- gate regret;
- empirical predictions table.

Remove the current entropy proposition from the main text. It can be a brief related observation in the appendix.

### 8.8 Limitations

State explicitly:

- action-grid logging is expensive;
- policy is conditional on the fixed initial selector/backend;
- parsed failures may be backend-specific;
- the initial retriever may still use human proof traces;
- the verified second-stage controller does not eliminate training-distribution leakage risks;
- miniCTX-v2 and Mathlib do not cover all Lean practice;
- alternative proof extraction may be incomplete;
- the method is not a general proof-repair agent.

### 8.9 Appendix

Move the following current content to the appendix as discovery/continuity evidence:

- 2k local trace-core table;
- local replay-filter bridge;
- imported-core lexical stress;
- four-split trace-core stability;
- feature-group ablations;
- broad guardrail and expert-mix negative results;
- final-base8;
- current bridge taxonomy;
- oracle `rule_far_full`;
- all controlled proxy baselines.

Add:

- exact action grid;
- all static schedule enumeration;
- full compute accounting;
- data schema;
- all hyperparameters;
- all failure parser rules;
- theorem lists and split hashes;
- per-goal outcomes;
- significance tests;
- qualitative examples;
- environment lockfile.

### 8.10 Existing figures and tables: keep, drop, merge, replace

| Current item | Action | Reason |
|---|---|---|
| Page-3 closed-loop pipeline figure | **Replace** | Too generic; does not show verified action labels or coverage–success mismatch. |
| Table 1 claim–evidence map | **Drop from main** | Reads like a defense memo and is dominated by proxy metrics. |
| Table 2 local trace core + bridge | **Move to appendix** | Useful discovery evidence, not main theorem-proving result. |
| Table 3 timeout stress | **Keep only as a small motivating panel if replicated on real LeanHammer; otherwise appendix** | Synthetic/stress evidence cannot carry the central claim. |
| Table 4 imported heldout | **Move to appendix** | Trace-core task and supervised controller. |
| Table 5 split stability + bridge | **Move to appendix or merge into continuity table** | Strong internal stability but weak external target. |
| Table 6 diagnosis summary | **Move to appendix** | Useful for method history, but final-base8 should not look central. |
| Current theory propositions | **Replace** | Too shallow and not decision-relevant. |
| Final-base8 discussion | **Demote sharply** | A focused rescue ablation, not a contribution. |
| New Figure 1 | **Add** | Coverage–success 2×2 plus adaptive loop. |
| New Main Table | **Add** | Equal-compute verified proof success. |
| New Figure 2 | **Add** | Static, oracle adaptive, and learned adaptive budget curves. |
| New Table 2 | **Add** | True/masked/shuffled feedback causal ablation. |
| New Figure 3 | **Add** | Action routing and calibration by failure class. |

### 8.11 Claims to sharpen

- “Static trace-recall optimization can be misaligned with bounded verified proof success.”
- “The first failure changes the value ordering of premise interventions.”
- “A failure-adaptive policy beats the best static use of the same actions and compute.”
- “Shrink is a necessary action on a measurable subset of real backend failures.”
- “Human trace-core coverage is route-specific and not a theorem-proving endpoint.”

### 8.12 Claims to weaken or remove

- “Failure feedback consistently improves” unless true-feedback controls establish this.
- Any implication that the current lexical proxy reproduces LeanSearch v2.
- Any general claim about proof repair, agentic proving, or verifier feedback.
- “Real Lean bridge validates practical proof reconstruction” unless selected premises causally enter replay.
- “More premises hurt” as a novel observation. The novelty must be conditional selection of when to shrink.
- Any presentation of final-base8 as a core method.

---

## 9. Decision Tree

### Gate 0: Does current failure content matter?

**Run:** true vs generic-failure vs masked vs matched-shuffled feedback on the existing four splits.

- **True feedback clearly wins:** proceed.
- **Only generic failure occurrence wins:** reframe as post-failure adaptive control; do not claim rich failure evidence.
- **Masked/shuffled matches true:** drop “failure feedback as conditional evidence.” The second stage is a retry-conditioned reranker. Continue only if end-to-end adaptive action value remains strong.
- **All second-stage variants match fallback:** stop the current controller line.

### Gate 1: Can premise interventions be made causal in LeanHammer?

- **Yes, with reliable traces:** proceed to action-grid pilot.
- **Premises are injected but failure instrumentation is weak:** use terminal status, time, and query statistics; keep theory modest.
- **Selected sets do not causally control the backend/replay:** rewrite the bridge claim immediately and prioritize Lean-side integration.
- **Integration is infeasible within schedule:** take backup Route A+B or submit an accept-oriented trace-recovery paper.

### Gate 2: Is there oracle adaptive headroom?

Compute the per-goal oracle over the pre-registered action grid and compare it to the best static equal-compute schedule.

- **Oracle gap ≥5 pp:** strong adaptive-control problem; train verified gate.
- **Oracle gap 3–5 pp:** viable main-track route; Oral requires unusually high gate capture and transfer.
- **Oracle gap <3 pp:** one action-grid redesign is allowed, motivated by failure analysis.
- **Still <3 pp:** kill Route G. Static scheduling is sufficient for this backend/action set.

### Gate 3: Does the learned verified gate capture the oracle gap?

- **Captures ≥50% of oracle gap and is calibrated:** run frozen final tests.
- **Captures 25–50%:** improve representation/calibration once; do not add ad hoc test heuristics.
- **Captures <25%:** the method contribution is weak. Consider a simpler rule-based policy only if theory predicts it and validation supports it.
- **Gate needs trace-core labels to work:** supervision critique remains; backup route only.

### Gate 4: Decisive end-to-end result

- **≥4 pp over strongest static equal-compute baseline, CI excludes 0, true feedback wins, transfer positive:** execute full Oral pivot. Rewrite title, abstract, theory, and main tables around verified adaptive interventions.
- **2–4 pp, significant, plus a strong compute-frontier or transfer result:** pursue a strong main-track paper with moderate Oral ambition. Use the coverage illusion as framing, but avoid grand claims.
- **<2 pp or not significant:** do not headline theorem-proving improvement. Consider a theory/mechanism paper only if coverage–success discordance is large and a reproducible intervention fixes it.
- **Static portfolio matches adaptive:** failure-conditioned control has no demonstrated value; retain current work as an ablation or stop.
- **Masked/shuffled gate matches true gate:** adaptive state features, not failure semantics, drive the result. Rename and narrow the paper.
- **Gain exists only on disagreement-heavy subsets:** reject the effect as selection-amplified for the main claim.

### Gate 5: Literature collision

If a new paper appears that already demonstrates online, per-goal, failure-conditioned premise-set actions in LeanHammer with equal-compute proof success:

- do not make a cosmetic distinction;
- restart around one of:
  1. a formal and empirical decomposition of adaptive value across selectors/backends;
  2. backend-agnostic failure representations that transfer without retraining;
  3. counterfactual offline policy evaluation for theorem-proving interventions;
  4. a substantially different causal question.

Do not retreat to “we used a different feature set.”

---

## 10. Final Action Plan for the Coding Agent

The paths below are proposed additions under `D:\ICLR_2`; adapt names to the repository’s actual layout without changing the experimental contracts.

### Phase 0: Freeze environment and claims

#### Files to edit

- `D:\ICLR_2\iclr2027\paper.tex`
- `D:\ICLR_2\experiment_report.md`
- `D:\ICLR_2\README.md` or project runbook
- `lean-toolchain`
- `lakefile.lean` / `lake-manifest.json`
- new: `configs/leanhammer_env.yaml`
- new: `configs/action_grid_v1.yaml`
- new: `configs/eval_primary.yaml`

#### Tasks

1. Pin exact Lean, Mathlib, LeanHammer, premise-selection server/model, ATP, and Python package versions.
2. Rename the current LeanSearch-like proxy everywhere.
3. Add a claim ledger to `experiment_report.md`:
   - supported now;
   - requires end-to-end result;
   - prohibited wording.
4. Freeze theorem splits and write SHA-256 hashes.
5. Reserve the final test set; do not run action-grid sweeps on it.

#### Output

- `outputs/environment_manifest.md`
- `outputs/split_manifest.json`
- `outputs/claim_ledger.md`

### Phase 1: Cheap causal and integration gates

#### Scripts to implement

- `experiments/current_pipeline/run_feedback_ablation.py`
- `analysis/paired_significance.py`
- `lean/AdaptivePremise/CustomSelector.lean`
- `lean/AdaptivePremise/TraceHarness.lean`
- `experiments/leanhammer/run_smoke.py`
- `experiments/leanhammer/parse_hammer_traces.py`

#### Required functionality

`run_feedback_ablation.py` must support:

- `--feedback true`
- `--feedback generic`
- `--feedback masked`
- `--feedback shuffled`
- `--feedback matched-shuffled`
- fixed model seed and split
- per-goal output, not only aggregate output

`TraceHarness.lean` must:

- install a custom `Lean.LibrarySuggestions` selector;
- pass an explicit ordered premise list;
- record the actual premises reaching LeanHammer;
- enable relevant `trace.hammer.*`, `trace.auto.*`, and Aesop traces;
- serialize terminal status and proof verification;
- distinguish translation, ATP, reconstruction, timeout, and tactic failures.

#### Outputs

- `outputs/feedback_causal_ablation_4x500.json`
- `outputs/feedback_causal_ablation_4x500.md`
- `outputs/leanhammer_integration_smoke.jsonl`
- `outputs/leanhammer_integration_smoke.md`

#### Stop conditions

- Stop the rich-feedback claim if true feedback does not beat matched-shuffled feedback.
- Stop LeanHammer route if custom premise sets cannot be shown to alter the actual prover query.

### Phase 2: Counterfactual verified action data

#### Scripts to implement

- `experiments/leanhammer/build_goal_manifest.py`
- `experiments/leanhammer/run_initial_attempts.py`
- `experiments/leanhammer/run_action_grid.py`
- `experiments/leanhammer/resume_action_grid.py`
- `experiments/leanhammer/validate_proofs.py`
- `analysis/action_oracle.py`
- `analysis/action_complementarity.py`
- `analysis/coverage_success_discordance.py`
- `analysis/search_poisoning_stats.py`

#### Action configuration

`configs/action_grid_v1.yaml` should define, without test-time edits:

- `keep`
- `shrink_050`
- `shrink_075`
- `expand_150`
- `expand_200`
- `mepo_swap`
- `mepo_interleave`
- `structural_swap` if available
- `base_rescue_8`
- `stop`

Each action record must include:

- goal ID and source module;
- initial premise list and scores;
- action premise list and scores;
- exact command/backend mode;
- parsed failure transcript;
- verified outcome;
- wall-clock and CPU;
- ATP calls;
- search statistics;
- proof term or reconstruction artifact;
- human trace-core coverage as optional diagnostic;
- environment hash.

#### Outputs

- `outputs/action_grid_train.jsonl`
- `outputs/action_grid_valid.jsonl`
- `outputs/action_grid_schema.json`
- `outputs/action_oracle_report.md`
- `outputs/action_complementarity.md`
- `outputs/coverage_success_discordance.md`
- `outputs/search_poisoning_stats.md`

#### Stop conditions

- Compute the best static action and best static compound schedule.
- Stop Route G if oracle adaptive gain remains below 3 pp after one predeclared action-grid revision.
- Do not invent new guardrails after looking at test outcomes.

### Phase 3: Verified action gate

#### Files/scripts

- `models/verified_action_gate.py`
- `models/features.py`
- `models/calibration.py`
- `train/train_verified_gate.py`
- `eval/eval_verified_gate.py`
- `analysis/gate_regret.py`
- `analysis/calibration_report.py`

#### Model contract

Inputs may include:

- goal and candidate summary;
- score histogram and top-margin features;
- first premise-set size/composition;
- failure terminal class;
- raw or embedded failure text where stable;
- elapsed time;
- clause/search/reconstruction statistics;
- selector/backend ID.

Inputs must not include:

- test labels;
- human trace-core membership;
- future retry outcomes;
- theorem identifiers that permit lookup memorization.

Train separate heads or models for:

- \(P(Y_a=1\mid X,F,a)\);
- expected cost \(E[C_a\mid X,F,a]\).

Select action by calibrated expected utility. Start with gradient-boosted trees or a small MLP before trying a large language model.

#### Outputs

- `outputs/verified_gate_valid.md`
- `outputs/verified_gate_calibration.md`
- `outputs/verified_gate_oracle_gap.md`
- `checkpoints/verified_gate_v1/`

#### Stop conditions

- Continue only if the gate captures at least 50% of oracle headroom or produces a clear Pareto improvement.
- No hand-coded final-base rescue may be added after test inspection.
- If calibration fails, fix calibration on validation; do not tune thresholds on test.

### Phase 4: Frozen end-to-end evaluation

#### Scripts

- `experiments/leanhammer/run_equal_compute_eval.py`
- `experiments/leanhammer/run_static_portfolio.py`
- `experiments/leanhammer/run_minictx_transfer.py`
- `experiments/leanhammer/run_budget_sweep.py`
- `analysis/mcnemar_test.py`
- `analysis/paired_bootstrap.py`
- `analysis/unique_solves.py`
- `analysis/compute_frontier.py`

#### Required policies

1. Official LeanHammer default.
2. Validation-tuned single static \(k\).
3. Validation-tuned static multi-action schedule.
4. Blind expansion schedule.
5. Static LeanPremise+MePo union/interleave.
6. Current learned+base fallback.
7. Current trace-supervised second stage.
8. Verified gate with masked feedback.
9. Verified gate with matched-shuffled feedback.
10. Verified gate with true feedback.
11. Oracle adaptive action, clearly labeled as an upper bound.

#### Primary outputs

- `outputs/e2e_mathlib_equal_compute.jsonl`
- `outputs/e2e_mathlib_equal_compute.md`
- `outputs/e2e_minictx_transfer.jsonl`
- `outputs/e2e_minictx_transfer.md`
- `outputs/budget_frontier.md`
- `outputs/paired_significance.md`
- `outputs/unique_solves.md`
- `outputs/failure_action_routing.md`

#### Final stop criteria

The Oral rewrite proceeds only if:

- true-feedback verified gate beats the strongest static equal-compute policy by at least 4 absolute points on the primary test;
- paired uncertainty excludes zero;
- masked and shuffled feedback are materially worse;
- at least one transfer setting is positive;
- compute is matched or the new policy dominates the cost–solve frontier.

A strong-accept rewrite may proceed with a 2–4 point significant gain plus a strong compute frontier.

Below 2 points, or with no causal feedback gap, stop the Oral route.

### Phase 5: Paper rewrite

#### `paper.tex` section plan

1. **Abstract:** verified result first; trace-core diagnostics last.
2. **Introduction:** coverage illusion → conditional action value → method/result.
3. **Related Work:** LeanHammer and LeanSearch v2 first; historical ATP feedback included.
4. **Problem:** static versus adaptive compound action under verified reward.
5. **Method:** frozen backend, failure parser, action grid, verified gate.
6. **Theory:** value of failure, regime separation, coverage separation, regret.
7. **Experiments:** discordance, oracle headroom, main result, causal ablation, transfer.
8. **Limitations:** backend/action dependence, data cost, remaining trace-supervised first stage.
9. **Conclusion:** adaptive premise intervention, not generic feedback.
10. **Appendix:** all current trace-core and bridge results.

#### Figures/tables to generate

- `figures/coverage_success_quadrants.pdf`
- `figures/adaptive_pipeline.pdf`
- `figures/budget_frontier.pdf`
- `figures/action_routing.pdf`
- `tables/e2e_main.tex`
- `tables/feedback_ablation.tex`
- `tables/oracle_headroom.tex`
- `tables/transfer.tex`

#### Report updates

Update `experiment_report.md` after every gate with:

- protocol;
- exact command;
- environment hash;
- aggregate result;
- per-goal output path;
- claim consequence;
- proceed/stop decision.

### Final instruction to the coding agent

Treat the current 95.7%, 92.9%, and 53.5% results as **supporting discovery evidence**, not as the target to optimize further. Do not run another cycle of broad hand-written expert mixing. The next unit of progress is a verified, equal-compute action-value experiment. The project should stop early if the oracle adaptive gap or true-feedback causal gap is absent.

---

## Bottom Line

The current project is not an Oral paper because it has not shown that its central signal changes actual proof success, and the generic feedback novelty is already crowded. The most promising upgrade is not a larger retriever, another guardrail, or more trace-core splits. It is to establish a new scientific object:

> **the conditional value of premise interventions after a failed, bounded LeanHammer call.**

If that value is large, learnable from real failure transcripts, and visible in kernel-verified proof success against an equal-compute static portfolio, the work has a credible Oral-level story. If any of those conditions fail, the project should narrow to a solid main-track paper or stop the direction rather than hide behind additional proxy experiments.
