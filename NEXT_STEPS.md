# NEXT_STEPS

Updated: 2026-06-23

This file only lists unfinished work. Completed experiments and stable results belong in `experiment_report.md`, `analysis/mathlib430_protocol_freeze_evidence_contract.md`, `analysis/mathlib430_evidence_contract_audit.md`, and `analysis/mathlib430_aesop_exact_controls_summary.md`.

## Current Gate

The paper route is still active as an action-conditional evidence-allocation paper, but P0 exact controls rule out the strongest Aesop channel-complementarity wording.

Do not claim:

- "facts and simps are deeply complementary" as the main causal mechanism;
- `oracle_core+retrieved` results as a deployable retriever-only theorem prover;
- matched compute beyond matched Lean-call budget plus empirical wallclock reporting.

Use this safer mainline:

- typed Lean interface compilation matters;
- fixed typed portfolios are strong hard controls;
- homogeneous K=4 controls show typed diversity is better than repeated single-family retries;
- Aesop provides a modest source/exposure/search-sensitivity diagnostic, not the headline causal result.

## P1. Optional External Retriever-Only Anchor

Run only if we want to strengthen deployability beyond the current mechanism-isolation paper.

Candidate route:

1. Freeze the current ACE compiler/action set and budgets.
2. Build a retriever-only candidate source without traced `proof_core`.
3. Compare upstream ranked candidates under:
   - empty/default consumption;
   - best single Lean interface;
   - fixed typed compiler;
   - typed oracle.
4. Report it as a plug-in downstream compiler diagnostic, not as a full LeanSearch/LeanHammer system reproduction.

Go criterion:

- typed compilation adds at least a few verified goals over the same retrieved names under matched Lean-call budget.

No-go handling:

- keep the current paper as an oracle-assisted mechanism study and make external retriever-only validation future work.

## P2. Optional Frozen Fresh Holdout

Run only after the paper text and final action set are frozen.

1. Select a new replayable Mathlib 4.30 goal set not used in action design.
2. Run only the final fixed typed portfolio and the exact controls needed for claim validation.
3. Do not tune the action set on this holdout.
4. Report it as prospective validation.

Go criterion:

- typed oracle-single gap and fixed K=4 recovery remain visible.

No-go handling:

- present the current 230-goal result as exploratory mechanism evidence and reduce the claimed generality.

## P3. Artifact Cleanup Before Submission

1. Keep exact-control scripts and summaries in git.
2. Keep raw singleton JSON outputs or a compressed archive, but do not require reviewers to inspect 690 files manually.
3. Ensure all paper tables cite canonical summaries.
4. Recompile and visually inspect `iclr2027/paper.pdf` after every final paper edit.
