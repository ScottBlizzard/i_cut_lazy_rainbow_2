# Mathlib 4.30 Retrieved-Only Anchor

Date: 2026-06-23

## Setup

- Runner: `scripts/run_retrieved_only_anchor_singletons_a40.sh`
- Candidate source: `--candidate-source retrieved_only`
- Goals: 230 replayable Mathlib 4.30 traced-corpus theorem contexts
- Raw singleton outputs: `outputs/retrieved_only_anchor_jsons.tgz`
- Logs: `outputs/retrieved_only_anchor_logs.tgz`
- Merged matrix: `outputs/mathlib430_pretheorem_action_matrix_scaled230_retrieved_only_anchor_merged.md`
- Budgeted policy: `outputs/mathlib430_budgeted_action_policy_scaled230_retrieved_only_anchor.md`
- Typed allocator gate: `outputs/mathlib430_typed_allocator_gate_scaled230_retrieved_only_anchor.md`
- Fixed stability: `outputs/mathlib430_fixed_portfolio_stability_scaled230_retrieved_only_anchor.md`

## Core Result

| Quantity | Value |
|---|---:|
| Goals | 230 |
| Attempts | 17,020 |
| Verified attempts | 1,397 |
| Non-empty-premise verified attempts | 1,177 |
| Empty Hammer | 29/230 |
| Best standalone action | 35/230 |
| Typed oracle | 52/230 |
| Fixed OOF K=1 after `hammer_empty` | 47/230 |
| Fixed OOF K=2 after `hammer_empty` | 50/230 |
| Fixed OOF K=3 after `hammer_empty` | 52/230 |
| Fixed OOF K=4 after `hammer_empty` | 52/230 |
| Strict after-`hammer_empty` goals | 23 |
| Fixed OOF K=3 strict coverage | 23/23 |

## Best Standalone Actions

| Action | Verified goals |
|---|---:|
| `aesop_core_plus_learned16` | 35 |
| `aesop_core_plus_learned32` | 35 |
| `aesop_learned16` | 35 |
| `aesop_learned32` | 35 |
| `aesop_core_plus_learned` | 34 |
| `aesop_learned8` | 34 |
| `aesop_core_plus_learned_countmatched_simps` | 33 |
| `aesop_learned8_countmatched_simps` | 33 |

## Readout

- P1 passes: typed compilation adds a large verified gain over the same retrieved-only candidate source.
- The result should be described as a downstream retrieved-only compiler anchor, not as a full LeanSearch/LeanHammer system reproduction.
- The strongest concise paper number is: retrieved-only candidates solve 29/230 with `hammer_empty`, 35/230 with the best standalone action, and 52/230 with a fixed typed K=3/K=4 OOF portfolio that reaches the typed oracle.
- Learned adaptive allocation still does not beat or compress the fixed typed control; it remains outside the main claim.
