# NEXT_STEPS

Updated: 2026-06-23

This file only lists unfinished work. Completed experiments and stable results belong in `experiment_report.md`, `analysis/mathlib430_protocol_freeze_evidence_contract.md`, `analysis/mathlib430_evidence_contract_audit.md`, `analysis/mathlib430_aesop_exact_controls_summary.md`, and `analysis/mathlib430_retrieved_only_anchor_summary.md`.

## Current Gate

The paper route is active as an action-conditional evidence-allocation paper. P0 exact controls rule out the strongest Aesop channel-complementarity wording, while P1 retrieved-only anchor supports the downstream typed-compiler claim without traced `proof_core`.

Do not claim:

- "facts and simps are deeply complementary" as the main causal mechanism;
- `oracle_core+retrieved` results as deployable evidence without the separate retrieved-only anchor;
- the retrieved-only anchor as a full LeanSearch/LeanHammer system reproduction;
- matched compute beyond matched Lean-call budget plus empirical wallclock reporting.

Use this safer mainline:

- typed Lean interface compilation matters;
- fixed typed portfolios are strong hard controls;
- homogeneous K=4 controls show typed diversity is better than repeated single-family retries;
- retrieved-only candidates still benefit from typed compilation: empty Hammer 29/230, best standalone action 35/230, fixed typed K=3/K=4 OOF 52/230;
- Aesop provides a modest source/exposure/search-sensitivity diagnostic, not the headline causal result.

## P1. Optional Frozen Fresh Holdout

Run only after the paper text and final action set are frozen.

1. Select a new replayable Mathlib 4.30 goal set not used in action design.
2. Run only the final fixed typed portfolio and the exact controls needed for claim validation.
3. Do not tune the action set on this holdout.
4. Report it as prospective validation.

Go criterion:

- typed oracle-single gap and fixed K=4 recovery remain visible.

No-go handling:

- present the current 230-goal result as exploratory mechanism evidence and reduce the claimed generality.

## P2. Artifact Cleanup Before Submission

1. Keep exact-control scripts and summaries in git.
2. Keep raw singleton JSON outputs or compressed archives, but do not require reviewers to inspect hundreds of files manually.
3. Ensure all paper tables cite canonical summaries.
4. Recompile and visually inspect `iclr2027/paper.pdf` after every final paper edit.
