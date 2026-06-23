# NEXT_STEPS

Updated: 2026-06-23

This file only lists unfinished work. Completed experiments and stable results belong in `experiment_report.md`, `analysis/mathlib430_protocol_freeze_evidence_contract.md`, `analysis/mathlib430_evidence_contract_audit.md`, `analysis/mathlib430_aesop_exact_controls_summary.md`, and `analysis/mathlib430_retrieved_only_anchor_summary.md`.

## Current Gate

The paper route is active as an action-conditional evidence-allocation paper. P0 exact controls rule out the strongest Aesop channel-complementarity wording, P1 retrieved-only anchor supports the downstream typed-compiler claim without traced `proof_core`, and the frozen fresh-holdout gate now passes on two disjoint folds.

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
- two fresh heldout retrieved-only folds confirm the frozen typed portfolio effect: combined empty Hammer 30/432, best singleton 54/432, frozen K=3/K=4 portfolio 67/432, tested-action oracle 68/432;
- Aesop provides a modest source/exposure/search-sensitivity diagnostic, not the headline causal result.

## P1. Paper Revision

The remaining work is writing, not more experiments.

1. Rewrite Abstract/Introduction around typed evidence allocation and the frozen holdout validation.
2. Add a compact fresh-holdout table using `analysis/mathlib430_fresh_holdout_summary.md`.
3. Keep the retrieved-only anchor and fresh holdout distinct:
   - anchor: larger fixed 230-goal mechanism/deployability check with the full retrieved-only typed grid;
   - holdout: prospective frozen action-subset validation on two disjoint folds.
4. Make every headline claim point to either the main matrix, retrieved-only anchor, or fresh holdout table.

Do not add more experiments unless paper revision reveals a specific unsupported claim. In particular, do not run fold2 just to add volume; fold0 and fold1 already establish the prospective validation direction.

## P2. Artifact Cleanup Before Submission

1. Keep exact-control scripts and summaries in git.
2. Keep raw singleton JSON outputs or compressed archives, but do not require reviewers to inspect hundreds of files manually.
3. Ensure all paper tables cite canonical summaries.
4. Recompile and visually inspect `iclr2027/paper.pdf` after every final paper edit.
