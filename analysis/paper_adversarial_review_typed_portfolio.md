# Typed Proof-Action Portfolio Paper: Adversarial Review

Updated: 2026-06-22

Purpose: give the next writer or experiment runner a complete reviewer-facing view of the current paper after the Mathlib 4.30 verified pivot. This document is intentionally critical. It separates what is already supported from what still needs evidence before the paper can credibly target ICLR oral-level strength.

## Current Mainline

The strongest defensible mainline is:

> Premise selection in Lean is incomplete unless selected names are assigned to the proof-action interface that consumes them. On replayable Mathlib 4.30 theorem contexts, a small typed portfolio over Aesop, HammerCore, Hammer, simplification, and `solve_by_elim` recovers nearly all current oracle headroom, and Aesop ablations show a counterintuitive mechanism: facts+simps exposure works, facts-only and simps-only mostly fail, and broader 32-name insertion can hurt.

This is stronger than the old trace-core-only story because it is kernel-verified in Lean. It is also more honest than claiming adaptive failure-conditioned routing, because current verified routing experiments show that fixed typed portfolios are still the hard baseline.

## Claim-Evidence Map

| Claim | Evidence | Status | Paper Use |
|---|---|---|---|
| Typed proof-action exposure matters beyond premise ranking. | Full scaled230 Aesop-ablation matrix: oracle 58/230 vs best single action 38/230. | Supported | Main claim. |
| Small fixed typed portfolios recover almost all current oracle headroom. | Budgeted policy: fixed greedy K=4 OOF 57/230; train-fitted K=4 58/230. | Supported | Main result, but phrase as portfolio strength rather than adaptive intelligence. |
| Aesop needs typed fact/simp exposure. | Facts+simps 38/230; facts-only 5/230; simps-only 4/230. | Strongly supported | Central mechanism / counterintuitive insight. |
| More selected names are not always better. | Aesop core+learned8/16 group coverage 41/230; core+learned32 only 7/230. Timeout stress also supports non-monotonicity. | Supported | Main mechanism plus supporting trace-core evidence. |
| Adaptive failure-conditioned routing beats matched fixed portfolios. | Current NB/kNN residual policies do not beat fixed typed portfolios. | Unsupported | Do not claim. Future work or next experiment only. |
| The system is competitive with full LeanSearch v2 / LeanHammer public systems. | No official system-to-system reproduction yet. | Unsupported | Avoid. Related work only. |
| The method solves open-ended theorem proving. | Evaluation is replayable pre-theorem context; 230/490 cleaned traces replay. | Unsupported | Avoid. |

## Main Rejection Risks

### R1. "This is just a fixed portfolio, not a method."

Severity: high.

Why a reviewer may say it:

- The best verified policy is currently a fixed sequence after `hammer_empty`.
- Low-capacity adaptive policies do not beat that fixed control.
- A fixed portfolio can look like engineering rather than research if the mechanism is not made explicit.

Current defense:

- The method's intervention space is the typed action, not a raw retry schedule.
- The surprising result is not merely "try Aesop too"; it is that the same names behave differently as facts, simp rules, HammerCore inputs, or elimination facts.
- The Aesop ablation is strong mechanism evidence: facts+simps works, either channel alone collapses, and broader exposure hurts.

Needed paper edits:

- State early that the contribution is the typed proof-action formulation and measured interface mechanism.
- Do not overemphasize low-capacity adaptive routing.
- Present fixed portfolio as the strongest current control and as evidence that interface typing is a large effect.

Useful next experiment:

- Interface filtering gate: remove invalid / unsafe Aesop names, split definitions/classes/instances from theorem facts, and measure whether the fixed portfolio oracle rises above 58/230.

### R2. "The absolute success rate is low."

Severity: high.

Why a reviewer may say it:

- 58/230 is only 25.2% on the replayable subset.
- The replayable subset is 230/490 cleaned traces, not all traces.

Current defense:

- This is not a full prover leaderboard; it isolates proof-action exposure in original-file pre-theorem contexts.
- The comparison is within the same harness: best single action 38/230, fixed K=4 57/230, oracle 58/230.
- The strict action-dependent subset has 29 goals where `hammer_empty` fails but a typed non-default action succeeds.

Needed paper edits:

- Keep the replayable-subset boundary explicit in abstract/introduction/limitations.
- Avoid language like "solves theorem proving" or "competitive prover".

Useful next experiment:

- Increase replayable coverage only if method improvements plateau. The current bottleneck is more likely action/interface filtering than more data.

### R3. "Missing strong external baselines."

Severity: medium to high.

Why a reviewer may say it:

- Related work includes LeanSearch v2 and LeanHammer premise selection, but the main table does not compare against official systems.
- Controlled lexical rows are not full LeanSearch v2.

Current defense:

- The paper studies post-retrieval interface choice, a different axis from global retrieval.
- The baseline inside the verified harness is strong: best single action and fixed typed portfolios under matched Lean-call budgets.

Needed paper edits:

- Explicitly say that BM25 / iterative lexical rows are controlled proxies, not LeanSearch v2 reproductions.
- Emphasize orthogonality: retrieval ranks names; typed proof-action selection decides how names enter Lean search.

Useful next experiment:

- If time allows, add a limited official-system comparison on the replayable subset. If not, keep claims scoped and do not pretend this comparison exists.

### R4. "Aesop ablation might be an artifact of invalid name insertion."

Severity: medium.

Why a reviewer may say it:

- Facts-only/simps-only and 32-name variants may fail due to invalid identifiers, unsafe rule insertion, or target leakage filtering rather than a clean interface effect.

Current defense:

- All variants are kernel-checked in the same pre-theorem harness.
- The comparison is still meaningful because it tests actual Lean interface exposure, including failure modes from bad exposure.

Needed paper edits:

- Phrase the result as "typed exposure through a real Lean interface" rather than a pure semantic theorem about facts/simps.

Useful next experiment:

- Add a filtering ablation:
  - visible-name survival rate per interface;
  - remove target theorem and aliases;
  - exclude definitions/classes/instances from unsafe Aesop rule channels;
  - compare old vs filtered Aesop variants on the same 230 goals.

### R5. "Trace-core experiments distract from the verified main claim."

Severity: medium.

Why a reviewer may say it:

- The paper still contains many trace-core tables from the old project.
- If these appear as equal-status main results, the story can feel like two papers.

Current defense:

- Trace-core results explain how the idea was discovered and why premise budgets/failure feedback matter.
- The current draft already labels them as supporting discovery evidence.

Needed paper edits:

- Keep verified typed-action results before trace-core results.
- Make trace-core rows supporting evidence, appendix, or motivation.

Useful next experiment:

- None. This is mainly writing discipline.

## Strongest Reviewer-Facing Story

The strongest story is a counterintuitive mechanism paper:

1. Reviewers expect premise selection to be about finding more relevant names.
2. Lean reconstruction shows this is incomplete because selected names must enter a specific proof interface.
3. The same evidence can be useful, inert, or harmful depending on whether it is passed as Hammer facts, HammerCore inputs, simp lemmas, Aesop facts/simps, or elimination facts.
4. A small typed portfolio recovers nearly all current oracle headroom.
5. The main Aesop mechanism is sharply non-obvious: facts+simps works; facts-only and simps-only collapse; broad 32-name exposure hurts.

This is a better ICLR main-track story than "we built a benchmark" or "we tuned a retry list."

## Exact Next Experiments Worth Doing

### E1. Interface Filtering Gate

Goal: test whether cleaner typed exposure raises the oracle or fixed portfolio above the current 58/230 ceiling.

Implementation:

- For every selected name, record whether it resolves in the pre-theorem context.
- Add target theorem / alias / same-file-later leak guards.
- Split names into theorem facts, simp-eligible lemmas, definitions, classes, instances, constructors, and namespaces.
- For Aesop, avoid sending definitions/classes/instances as unsafe theorem-like rules unless the generated syntax is known safe.
- Re-run only the high-value action families first:
  - `aesop_core_plus_learned` filtered facts+simps;
  - `aesop_core_plus_learned16` filtered facts+simps;
  - `hammerCore_core_plus_learned`;
  - `hammer_core_plus_learned16`;
  - `solve_by_elim_core`.

Stop condition:

- If filtered actions do not add oracle goals and only reshuffle existing successes, do not continue large-scale filtering variants.

### E2. Paired Portfolio Stability Table

Goal: make the current fixed-portfolio result more review-proof.

Implementation:

- Report per-fold fixed K=1/2/3/4 performance, not only aggregate OOF.
- Report paired wins/losses versus best single action and `hammer_empty`.
- Report strict-goal coverage by action family and by only-family cases.

Stop condition:

- If no new method is added, this is a reporting task, not a new experiment.

### E3. Stronger Adaptive Gate Only After E1

Goal: avoid wasting runs on weak NB/kNN variants.

Implementation:

- Only train a new adaptive router if E1 creates new action diversity or raises oracle headroom.
- Candidate features must include:
  - first failure type / stderr clusters;
  - action-family historical success;
  - candidate survival rates by interface;
  - theorem namespace and statement features;
  - which channels were nonempty after filtering.
- Evaluate against fixed typed portfolios under the same number of Lean calls.

Stop condition:

- If it cannot beat fixed K=2 or match fixed K=4 with fewer calls, keep it out of the main claim.

## Paper Edits To Prioritize

1. Abstract and introduction must not claim adaptive routing.
2. The first table should be the verified typed-action claim-evidence map.
3. The method section must define typed actions as the intervention, not as an implementation detail.
4. The experiment section must say that controlled lexical rows are not LeanSearch v2.
5. The limitations must openly state:
   - replayable subset is 230/490 cleaned traces;
   - no official full-system comparison yet;
   - fixed portfolio is currently stronger than low-capacity adaptive routing.
6. The appendix self-review should include the risk that a fixed portfolio may look too simple, and the response should be the Aesop mechanism ablation.

## Current Score Estimate

These are internal planning scores, not paper claims.

| Dimension | Current Score | Why |
|---|---:|---|
| Idea sharpness | 7.5/10 | Typed interface exposure is meaningful and counterintuitive, especially Aesop facts+simps vs facts-only/simps-only. |
| Theory depth | 5.5/10 | Current propositions formalize intuition but are not deep enough for oral by themselves. |
| Verified experiment strength | 6.5/10 | Kernel-verified and real Mathlib, but 230-goal replayable subset and no official external comparison. |
| Mechanism evidence | 8/10 | Aesop ablation is clean and surprising. |
| Adaptive-method novelty | 4/10 | Current adaptive policies do not beat fixed typed portfolio. |
| ICLR main-track viability | 6.5/10 | Viable if framed as typed proof-action mechanism, not as a full prover. |
| ICLR oral viability | 4.5/10 | Needs a stronger adaptive policy, larger verified corpus, or deeper theory/official baseline comparison. |

## Bottom Line

Do not downgrade the idea into "we tried more tactics." The hard version is:

> Premise evidence has an interface type. The paper proves this empirically in real Lean replay by showing that a name set's value changes sharply depending on the proof-action channel, and that a small typed portfolio nearly saturates current oracle headroom.

The next meaningful upgrade is not more blind actions. It is cleaner typed exposure plus a policy that can beat or compress the fixed typed portfolio under matched Lean-call budgets.
