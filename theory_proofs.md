# Theoretical Foundations: Closed-Loop Premise Optimization

> 版本：2026-06-17 初始理论蓝图  
> 目标：把 FAR-Hammer 从工程系统升级成有理论骨架的方法论文。每个命题都要包含：定义、假设、直觉证明、经验预测、当前证据、待补实验。

---

## 0. Executive Summary

本文理论主张不是“失败信息有用”这么泛，而是：

1. **Premise coverage is not search quality.** proof core 被覆盖不代表 hammer search 可控。
2. **Search quality is not verified success.** ATP/search 成功不代表 Lean reconstruction 成功。
3. **More premises can hurt.** 扩大 top-k 可能增加 proof-core recall，也可能引起 timeout/search explosion/reconstruction ambiguity。
4. **Failure traces are counterfactual supervision.** 失败 trace 约束下一轮 premise utility posterior。
5. **Closed-loop premise optimization is a budgeted decision problem.** 每次 prover call 都昂贵，应该最大化 fixed-budget verified success。

---

## 1. Formal Setup

### 1.1 Goal, premises, and prover

Let \(g\) be a Lean proof goal. Let \(\mathcal{A}(g)\) denote accessible premises under Lean's namespace/import/local context rules.

A premise selector outputs:

\[
P_t \subset \mathcal{A}(g),\quad |P_t|\le k_t.
\]

A prover/hammer backend returns:

\[
y_t = \operatorname{Prover}(g, P_t, B_t)
\]

where \(B_t\) is a time/search budget and \(y_t\) includes:

- verified success/failure;
- backend status;
- failure trace \(F_t\);
- reconstruction status;
- optional proof core if successful.

### 1.2 Three evidence axes

**Premise coverage \(P\).**  
Whether selected premises contain proof-critical lemmas.

**Search-space quality \(S\).**  
Whether the premise set induces a tractable search and reconstruction space.

**Verified success \(V\).**  
Whether Lean kernel accepts the final proof.

The core hierarchy is:

\[
P \nRightarrow S,\quad S \nRightarrow V.
\]

### 1.3 Closed-loop policy

\[
P_{t+1}=\pi_\theta(g,P_{\le t},F_t,H_t,B_{\le t})
\]

Objective:

\[
\max_\pi \mathbb{E}[\mathbf{1}\{V=1\}]
\quad
\text{s.t.}\quad \sum_t B_t\le B.
\]

---

## 2. Proposition 1: Coverage Does Not Imply Search Quality

### Claim

A premise set can contain the proof core while still making hammer search fail due to noise, search explosion, or reconstruction ambiguity.

### Assumptions

1. A proof core \(C^\star\subseteq \mathcal{A}(g)\) exists.
2. Search cost increases with irrelevant or broad premises.
3. The backend has finite time/search budget.

### Statement

There exist \(P_1,P_2\) such that:

\[
C^\star \subseteq P_1 \subset P_2
\]

but:

\[
\operatorname{Prover}(g,P_1,B)=\text{success},\quad
\operatorname{Prover}(g,P_2,B)=\text{timeout/fail}.
\]

### Proof sketch

Adding premises preserves coverage but can increase branching factor and generated clauses. Under fixed budget, search may spend budget on irrelevant derivations and fail before reaching the proof core.

### Empirical predictions

1. Top-k expansion has non-monotonic success curves.
2. Timeout rate rises after a certain premise budget.
3. FAR shrink actions improve timeout subset.

### Current evidence

Pending Phase 1.

---

## 3. Proposition 2: Failure Trace Reduces Premise Utility Uncertainty

### Claim

If failure types are statistically associated with missing/noisy/reconstruction-hostile premise patterns, then failure traces reduce uncertainty over the utility of candidate premises.

### Setup

Let \(U(p;g)\) be latent premise utility. A one-shot retriever estimates:

\[
q_0(p)=P(U(p;g)=1\mid g).
\]

After failure:

\[
q_t(p)=P(U(p;g)=1\mid g,F_t,P_{\le t}).
\]

### Statement

If \(I(U;F_t\mid g,P_t)>0\), then:

\[
H(U\mid g,P_t,F_t) < H(U\mid g,P_t).
\]

### Interpretation

Failure traces are useful exactly when they carry mutual information about premise utility or premise-set noise.

### Empirical predictions

1. Failure-conditioned rerank outperforms history-only rerank.
2. Coarse failure type already beats random retry.
3. Structured trace beats message-only when parser is accurate.

### Current evidence

Pending Phase 1 ablation.

---

## 4. Proposition 3: More Premises Can Hurt

### Claim

Proof success is not monotonic in premise budget.

### Statement

Let \(K=|P|\). There can exist \(K_1<K_2<K_3\) such that:

\[
\text{success}(K_1)<\text{success}(K_2)>\text{success}(K_3).
\]

### Mechanism

- Low \(K\)：missing core premises。
- Medium \(K\)：core covered, search tractable。
- High \(K\)：noise dominates, timeout/reconstruction failure rises。

### Empirical predictions

1. Budget curve has a peak or plateau, not monotonic increase.
2. FAR selects smaller sets in timeout regimes.
3. FAR proof-core precision exceeds top-k expansion.

### Current evidence

Pending premise budget curve.

---

## 5. Proposition 4: Reconstruction Is a Separate Axis

### Claim

An external prover may find a proof that is hard or impossible to reconstruct in Lean with the selected premises.

### Statement

There exist \(P\) and backend proof \(\rho\) such that:

\[
\operatorname{ATP}(g,P)=\text{success}
\]

but:

\[
\operatorname{LeanRecon}(g,P,\rho)=\text{fail}.
\]

### Empirical predictions

1. ATP success but Lean fail is a measurable subset.
2. Recon-aware premise score lowers this subset.
3. Some premises are high ATP utility but low Lean reconstruction utility.

### Current evidence

Pending reconstruction subset experiment.

---

## 6. Proposition 5: Local Context Failure Is Failure-Amplified

### Claim

Local/user premises may be underweighted by global retrievers, but failure traces can reveal when local bridge lemmas are missing.

### Empirical predictions

1. FAR gain is larger on miniCTX/local project than full Mathlib average.
2. Local premise boost is most useful after first failure.
3. Local boost without failure is weaker than failure-triggered local boost.

### Current evidence

Pending miniCTX/local experiment.

---

## 7. Theory-to-Experiment Map

| Theory claim | Experiment | Status |
|---|---|---|
| \(P\nRightarrow S\) | proof-core coverage vs timeout/redundancy | pending |
| more premises can hurt | premise budget curve | pending |
| failure trace has information | failure ablation | pending |
| reconstruction separate | ATP success vs Lean reconstruction | pending |
| local context gain | miniCTX/local subset | pending |
| closed-loop budget advantage | fixed-budget main table | pending |

---

## 8. Claim-Evidence Constraints

Paper writing must obey:

1. Do not claim failure trace always helps; report where it helps.
2. Do not call a premise necessary unless remove-one/proof-core evidence supports it.
3. Do not report retrieval recall as proof success.
4. Do not compare methods under unequal prover calls or wall-clock.
5. Do not hide backend/protocol sensitivity; audit it.
6. Do not position against APOLLO/OProver as proof generator; our object is premise set optimization.

