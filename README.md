# ICLR_2 Review Package

This repository is a curated review package for the current ICLR_2 paper draft.
It is intended for GPTPro / collaborator review, not as a full raw experiment
artifact dump.

## Start Here

1. `iclr2027/paper.pdf` - current compiled paper draft.
2. `analysis/paper_adversarial_review_typed_portfolio.md` - skeptical review of
   the current typed proof-action portfolio story.
3. `NEXT_STEPS.md` - current unfinished experiment and writing plan.
4. `experiment_report.md` - consolidated experiment report.
5. `outputs/claim_ledger.md` - claim/evidence boundaries.

## Main Current Story

The current defensible mainline is:

> Premise selection in Lean is incomplete unless selected names are assigned to
> the proof-action interface that consumes them. On replayable Mathlib 4.30
> theorem contexts, typed action portfolios over Aesop, HammerCore, Hammer,
> simplification, and `solve_by_elim` recover nearly all current oracle
> headroom. Aesop facts+simps exposure is the strongest mechanism evidence:
> facts+simps works, facts-only and simps-only mostly fail, and broader 32-name
> insertion can hurt.

The current paper does not claim that adaptive routing beats fixed typed
portfolios. That remains a future gate.

## What Is Included

- Paper source and compiled PDF under `iclr2027/`.
- Analysis and review notes under `analysis/`.
- Markdown experiment summaries under `outputs/`.
- Source scripts under `src/`.
- Small configuration files under `configs/`.

## What Is Excluded

- Large raw `outputs/*.json` and `outputs/*.jsonl` files.
- Third-party Lean dependencies under `external/`.
- Related-paper PDFs under `papers/*.pdf`.

These exclusions keep the repository reviewable and avoid pushing multi-GB raw
artifacts or redistributing third-party papers.
