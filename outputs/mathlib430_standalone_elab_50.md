# Mathlib 4.30 Standalone Elaboration Probe

- Verdict: `pass`
- Input: `/workspace/thymic_project/paper/iclr_2/outputs/mathlib430_clean_trace_subset_500.jsonl`
- Goals checked: 50
- Elaborated: 4 (8.0%)

## Status Counts

| Status | Count |
|---|---:|
| `elaborated` | 4 |
| `unknown_identifier` | 21 |
| `syntax_or_parse` | 6 |
| `typeclass_or_inference` | 15 |
| `lean_error` | 4 |

## Readout

- This only checks standalone statement elaboration with `sorry`.
- Failures usually mean the theorem depends on original file section variables, namespaces, local notation, or attributes; a pre-theorem file-patching replay harness may still handle them.
