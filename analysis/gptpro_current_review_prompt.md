# GPTPro Prompt: Current ICLR_2 Review

Please act as an extremely strict ICLR main-track / oral-level reviewer and
paper strategy advisor. Read the repository carefully, especially:

- `iclr2027/paper.pdf`
- `analysis/paper_adversarial_review_typed_portfolio.md`
- `NEXT_STEPS.md`
- `experiment_report.md`
- `outputs/claim_ledger.md`

The paper must target the ICLR main track. Do not downgrade it into an
evaluation-only or benchmark-only paper.

Current proposed mainline:

> Premise selection is not enough for Lean. Selected names must be typed by the
> proof-action interface that consumes them. A compute-budgeted typed
> proof-action portfolio over Aesop, HammerCore, Hammer, simplification, and
> `solve_by_elim` recovers nearly all current oracle headroom on replayable
> Mathlib theorem contexts. The counterintuitive mechanism is that Aesop
> facts+simps exposure works, facts-only and simps-only mostly fail, and broader
> 32-name exposure can hurt.

Please answer concretely:

1. What are the 5 most likely rejection reasons, ordered by severity?
2. Is the current typed proof-action portfolio story strong enough for an ICLR
   main-track paper? If not, what exactly is missing?
3. How far is the current paper from ICLR oral level? Give scores for idea,
   theory, method novelty, empirical strength, writing clarity, and overall
   oral chance.
4. Which experiments are mandatory before submission, which are high-upside,
   and which should be stopped?
5. Among E1 interface filtering gate, E2 paired portfolio stability, and E3
   stronger adaptive gate, which should be prioritized and why?
6. Should the project continue strengthening typed proof-action portfolios, pivot
   toward deeper theory, pivot toward adaptive routing, pivot toward a larger
   system comparison, or be rebuilt around a different idea?
7. If aiming for oral-level strength, how would you rewrite the title, abstract,
   core claim, method section, and experiment layout?
8. Which claims are currently safe to state strongly, which require careful
   wording, and which must not be stated?
9. Give a concrete one-week execution plan: exact experiments to run, exact
   paper sections to rewrite, and stop/go criteria.

Be harsh and specific. Do not give generic encouragement. Every recommendation
must be grounded in the current paper and evidence files.
