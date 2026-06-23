# Mathlib 4.30 Evidence-Contract Protocol Freeze

Date: 2026-06-23

This freeze supersedes the earlier adaptive-router framing for the current ICLR_2 main-track paper. The working claim is now action-conditional evidence allocation under a frozen Lean 4.30 replay protocol.

## Frozen Inputs

- Trace corpus: `outputs/mathlib430_clean_trace_subset_500.jsonl`
- Replay filter: `outputs/mathlib430_pretheorem_original_tactic_probe_490.json`
- Stable split: `outputs/mathlib430_replayable490_splits.json`
- Main verified matrix: `outputs/mathlib430_pretheorem_action_matrix_scaled230_aesop_ablation_merged.json`
- Evidence-contract audit: `analysis/mathlib430_evidence_contract_audit.md`
- Retrieved-only anchor: `analysis/mathlib430_retrieved_only_anchor_summary.md`
- Deep external review motivating this freeze: `analysis/deep_research_report_evidence_contract_controls.md`

## Split Contract

- Replayable goals evaluated in the main matrix: 230.
- Split policy: SHA256-sorted goal IDs, 60/20/20.
- Train/dev/test sizes: 138 / 46 / 46.
- All fixed portfolio and allocator results must be reported out of fold unless explicitly labelled train-fitted.

## Source-Transparency Contract

The current matrix action names use `core`, but `core` is traced `proof_core`. In paper text and new reports this must be interpreted as `oracle_core`.

Allowed wording:

- "oracle-core plus retrieved evidence"
- "mechanism-isolation setting"
- "matched Lean-call budget"
- "empirical runner-wallclock frontier"

Disallowed wording:

- "deployable retriever-only theorem prover"
- "matched compute" without qualification
- "learned adaptive allocator beats fixed portfolio"
- "core" without defining it as traced proof-core evidence
- "official LeanSearch/LeanHammer reproduction" for the retrieved-only anchor

## Current Verified Baselines

- Main matrix attempts: 11,500.
- Verified attempts: 582.
- Oracle goals: 58/230.
- Best single static action: `aesop_core_plus_learned`, 38/230.
- `hammer_empty`: 29/230.
- `aesop_empty`: 29/230.
- Fixed typed OOF portfolio: K=1 49/230, K=2 55/230, K=3 55/230, K=4 57/230.
- Train-fitted typed K=4: 58/230.

## Provenance Audit

From `analysis/mathlib430_evidence_contract_audit.md`:

- Mean traced `proof_core` size: 3.80 names per goal.
- Mean retrieved top-8 size: 8.00 names per goal.
- Mean retrieved top-32 size: 32.00 names per goal.
- Proof-core names already in retrieved top-8: 552 total.
- Proof-core names already in retrieved top-32: 738 total.
- Proof-core-only outside retrieved top-32: 137 total.

This means the main evidence pool is mixed: it contains both oracle proof-core names and retrieved names. The main mixed matrix is useful for mechanism isolation; the separate P1 anchor below is the retrieved-only downstream compiler result.

## Completed P1 Retrieved-Only Anchor

The downstream compiler anchor removes traced `proof_core` from the candidate source and reruns the full typed action grid with `--candidate-source retrieved_only`.

- Runner: `scripts/run_retrieved_only_anchor_singletons_a40.sh`.
- Raw singleton archive: `outputs/retrieved_only_anchor_jsons.tgz`.
- Merged matrix: `outputs/mathlib430_pretheorem_action_matrix_scaled230_retrieved_only_anchor_merged.md`.
- Budgeted policy: `outputs/mathlib430_budgeted_action_policy_scaled230_retrieved_only_anchor.md`.
- Typed allocator gate: `outputs/mathlib430_typed_allocator_gate_scaled230_retrieved_only_anchor.md`.

Key result:

- Empty Hammer: 29/230.
- Best standalone action: 35/230.
- Typed oracle: 52/230.
- Fixed typed OOF portfolio after `hammer_empty`: K=1 47/230, K=2 50/230, K=3 52/230, K=4 52/230.
- Strict after-`hammer_empty` goals: 23; fixed K=3 covers 23/23.

This passes the external-anchor gate for a downstream retrieved-only evidence compiler. It should not be written as an official full-system LeanSearch or LeanHammer reproduction.

## Completed P0 Offline Controls

- Homogeneous K=4 controls:
  - `aesop_all`: 49/230 OOF.
  - `hammer_only`: 32/230 OOF.
  - `hammerCore_only`: 41/230 OOF.
  - `simplification_only`: 41/230 OOF.
  - `solve_by_elim_only`: 34/230 OOF.
  - Full typed grid: 57/230 OOF.
- Random full-grid K=4 over 100 seeds: mean 41.9/230, median 42/230, range 31-56.
- Empirical runner-wallclock frontier:
  - `aesop_core_plus_learned` after `hammer_empty`: 49/230 at 1.87 calls and 16.36 seconds average.
  - Full typed train-fitted K=2: 55/230 at 2.66 calls and 26.37 seconds average.
  - Full typed train-fitted K=4: 58/230 at 4.18 calls and 40.07 seconds average.

## Completed P0 Exact Controls

The exact-control runner now supports:

- `--candidate-source oracle_plus_retrieved`
- `--candidate-source retrieved_only`
- `--candidate-source oracle_core_only`

The final P0 run used singleton shards on A40:

- 230 goals x 3 source modes x 9 essential Aesop actions = 690 JSON outputs.
- Source modes: `oracle_plus_retrieved`, `retrieved_only`, `oracle_core_only`.
- Runner: `scripts/run_aesop_exact_controls_essential_singletons_a40.sh`.
- Summary: `analysis/mathlib430_aesop_exact_controls_summary.md`.

Essential actions:

- empty Aesop;
- joint `aesop_core_plus_learned`;
- facts-only and simps-only;
- identity-matched joint exposure;
- swapped channel exposure;
- count-matched facts-only and simps-only exposure;
- deterministic random-split exposure.

Key exact-control result:

- Empty Aesop: 29/230.
- `oracle_core+retrieved`, joint facts+simps: 38/230.
- `oracle_core+retrieved`, identity: 36/230.
- `oracle_core+retrieved`, simps-only: 35/230.
- `oracle_core+retrieved`, facts-only: 32/230.
- `retrieved-only`, joint facts+simps: 34/230.
- `oracle-core-only`, joint facts+simps: 35/230.

## Gate For Paper Rewrite

P0 is a no-go for the strongest Aesop causal mechanism:

- identity and simps-only controls explain most of the lift over empty Aesop;
- joint-only over exact single-channel controls is only 2 goals in `oracle_core+retrieved`;
- source composition is modest rather than decisive, since retrieved-only reaches 34/230 and oracle-core-only reaches 35/230.

The paper can still keep the action-conditional evidence-allocation mainline because the typed action grid, fixed portfolio, homogeneous K=4 controls, and wallclock frontier remain intact. The Aesop section must be written as a source/exposure/search-sensitivity diagnostic rather than a strong facts-versus-simps complementarity result.
