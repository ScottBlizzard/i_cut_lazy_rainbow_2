# Prompt for GPT Pro

You are an expert ML/NLP/formal-reasoning researcher and an adversarial ICLR area-chair-level reviewer. I will give you two files:

1. `paper.pdf`: the current draft of a paper titled "Failure Feedback as Conditional Evidence for Lean Premise Selection".
2. `gptpro_oral_upgrade_brief.md`: a detailed project briefing with experiment history, current claims, limitations, and possible upgrade directions.

Your task is not to polish prose. Your task is to think deeply about how to make this work an **ICLR main-track Oral-level paper**. Do not turn it into an evaluation paper, benchmark paper, tool paper, dataset paper, or workshop-style engineering report.

You must do all of the following:

1. Read the paper and the briefing carefully.
2. Search the latest relevant literature before forming a final opinion. Prioritize primary sources: arXiv, OpenReview, official project pages, papers with code, conference proceedings, and official GitHub repos.
3. Compare against the strongest current work in Lean theorem proving, premise selection, retrieval-augmented proving, Lean hammers, proof repair, compiler feedback, verifier feedback, and process supervision.
4. Be willing to recommend any of the following if justified:
   - keep the current idea and upgrade experiments/theory;
   - pivot the main claim;
   - reframe the paper around a deeper insight;
   - turn current results into a supporting phenomenon for a stronger method;
   - push a more theoretical version;
   - discard the current direction and restart from a stronger oral-level idea.

Hard constraints:

- This must remain an ICLR main-track research paper.
- Do not recommend a benchmark/evaluation-only paper.
- Do not accept trace-core recovery as sufficient for oral-level claims unless you give a strong conceptual/theoretical reason.
- Do not treat the current LeanSearch-style proxy baseline as equivalent to full LeanSearch v2.
- Do not hide that the learned retriever and second-stage controller use traced proof-core supervision.
- Do not overvalue tiny heuristic improvements like final-base8; it is a focused ablation unless you can make it conceptually central.

Key current facts to keep in mind:

- Local Mathlib trace-core: `rule_far_no_core_tags` 95.7% vs top-k expansion 91.5%.
- Local real Lean bridge: 72.0% bridge verified vs top-k expansion 43.0%.
- Timeout stress: equal-budget top-k drops to 43.8%; timeout shrink reaches 69.3%.
- Imported-core learned second-stage: 92.4% vs learned+base fallback 87.0%.
- Four split mean: final-base8 92.9% vs fallback 86.3%.
- 200-goal imported bridge: final-base8 53.5% bridge verified vs fallback 44.5%.
- Remaining bridge misses: 0/17 candidate-pool misses; mostly rank/calibration misses.
- Main limitation: current evidence is trace-core recovery plus replay bridge subset, not full end-to-end theorem proving.

Please produce a markdown report with the following structure:

## 1. Executive Verdict

- Current paper score for ICLR main track.
- Current oral probability.
- Current accept probability.
- One-sentence reason it is not oral yet.
- Whether you recommend: keep, pivot, upgrade, or restart.

## 2. Literature Search and Threat Model

For every important paper/system you find, include:

- title
- year/date
- venue/status
- link
- what it claims
- why it threatens or supports this paper
- what comparison or wording this paper needs

At minimum, check LeanSearch v2, LeanHammer / Premise Selection for a Lean Hammer, LeanDojo/ReProver, APRIL, process-verified RL via Lean, tree/structure-based premise selection, and recent Lean feedback or proof repair work.

## 3. What Is the Oral-Level Idea?

Answer explicitly:

- Is "failure feedback as conditional evidence" enough?
- If not, what stronger claim should replace it?
- What is the Lean theorem proving equivalent of "restoration lies" from mechanistic interpretability?
- Can we build a conceptual hierarchy like coverage -> search tractability -> replayability -> proof success?
- What would make this insight surprising rather than expected?

## 4. Route Evaluation

Evaluate these routes:

- A: Keep current idea and add end-to-end proof success.
- B: Reframe as "retrieval recall / proof-core coverage lies".
- C: Develop a deeper theory of conditional proof search.
- D: Build a learned calibrated expert-gate method.
- E: Pivot to failure-supervised action/model training.
- F: Keep current project as solid accept rather than oral.
- G: Any new route you discover from literature search.

For each route, give:

- oral potential
- feasibility
- required experiments
- theoretical depth
- novelty risk
- baseline risk
- kill criteria

## 5. Recommended Strategy

Choose one primary strategy and one backup strategy. Explain why.

Define:

- new main claim
- new title options
- central figure/table
- minimum decisive experiment
- strongest expected reviewer objection and answer

## 6. Required Experiments

Give an execution-ready experiment table:

- experiment name
- goal
- exact protocol
- baselines
- metrics
- expected positive outcome
- negative outcome interpretation
- estimated difficulty
- priority

Be specific. Do not say "run more experiments" generically.

## 7. Theory Upgrade

Propose the strongest theoretical framework:

- definitions
- assumptions
- propositions/theorems
- proof sketches
- empirical predictions
- how theory changes the paper story

If theory cannot be made deep enough, say so clearly.

## 8. Paper Rewrite Plan

Give a section-by-section rewrite:

- Abstract
- Introduction
- Related Work
- Method
- Experiments
- Theory
- Limitations
- Appendix

Say which existing tables/figures to keep, drop, merge, or replace.

## 9. Decision Tree

Give a concrete decision tree:

- If the decisive experiment succeeds, do X.
- If it partially succeeds, do Y.
- If it fails, pivot to Z.
- If literature search shows the idea is already covered, restart with W.

## 10. Final Action Plan for the Coding Agent

Produce a concise but complete plan that I can hand to a coding agent. It should include:

- files to edit
- scripts/experiments to implement
- outputs to generate
- reports to update
- paper sections to rewrite
- stopping criteria

Be honest and adversarial. The goal is not to make us feel good; the goal is to maximize the chance of an ICLR Oral-level main-track paper.

