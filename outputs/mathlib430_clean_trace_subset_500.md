# Mathlib 4.30 Clean Trace Subset

- Input: `/workspace/thymic_project/paper/iclr_2/outputs/phase3_second_stage_eval_goals_500.jsonl`
- Preflight: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_trace_corpus_preflight_500.json`
- Output JSONL: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_clean_trace_subset_500.jsonl`
- Input goals: 500
- Clean goals: 490
- Dropped goals: 10
- Removed circular target candidates: 490

## Drop Reasons

| Reason | Count |
|---|---:|
| `missing_file_in_mathlib430` | 3 |
| `missing_theorem_in_mathlib430` | 6 |
| `missing_proof_core_in_mathlib430` | 1 |

## Readout

- This subset removes direct target-theorem leakage from candidate lists.
- It is only a data-cleaning step. Standalone elaboration and pre-theorem replay are still required before this becomes a verified traced-corpus benchmark.
