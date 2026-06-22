# Mathlib 4.30 Replayable-Subset Hammer Matrix

- Verdict: `pass`
- Replay filter: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_pretheorem_original_tactic_probe_10.json`
- Replayable goals evaluated: 3
- Hammer attempts: 90
- Verified Hammer attempts: 8
- Goals with at least one Hammer proof: 1

## Status Counts

| Status | Count |
|---|---:|
| `lean_error` | 36 |
| `proved` | 8 |
| `search_fail` | 12 |
| `sorry_warning` | 18 |
| `unknown_identifier` | 16 |

## By Config

| Config | Verified | Attempts |
|---|---:|---:|
| `aesop_10` | 2 | 18 |
| `aesop_5` | 2 | 18 |
| `aesop_grind_10` | 2 | 18 |
| `auto_aesop_10` | 2 | 18 |
| `grind_only_10` | 0 | 18 |

## By Premise Set

| Premise set | Verified | Attempts |
|---|---:|---:|
| `base8` | 0 | 15 |
| `empty` | 4 | 15 |
| `learned16` | 0 | 15 |
| `proof_core` | 4 | 15 |
| `proof_core_plus_learned8` | 0 | 15 |
| `same_file8_plus_core` | 0 | 15 |

## By Goal

| Goal | Verified attempts | Best attempt |
|---|---:|---|
| `mathlib4::Module.rank_tensorProduct'` | 8 | `empty` / `aesop_10` / 0 premises |
| `mathlib4::FirstOrder.Language.definableFun_const` | 0 | none |
| `mathlib4::MeasureTheory.Measure.compProd_apply_univ` | 0 | none |

## Readout

- Hammer has at least one positive proof on a replayable traced theorem; scale this route on a larger replayable subset.
