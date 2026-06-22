# FAR-Hammer Source Layout

This directory is the local master copy for experiment code. Use `D:\ICLR_2\push.ps1` to sync to 4090, or `D:\ICLR_2\push.ps1 -Server A40` while 4090 is under repair.

Planned modules:

| Path | Purpose |
|---|---|
| `config.py` | paths, budgets, backend settings |
| `schema.py` | structured JSON output dataclasses |
| `retrievers/` | BM25, ReProver, LeanSearch, LeanPremise wrappers |
| `provers/` | Lean/hammer/prover attempt wrappers |
| `failure_parser.py` | failure taxonomy parser |
| `far_controller.py` | expand/shrink/swap/stop controller |
| `reranker.py` | failure-conditioned reranker |
| `eval_fixed_budget.py` | main fixed-budget evaluation |
| `analyze_outputs.py` | result aggregation and paper tables |

No experiment output should be written inside `src/`; write all results to `../outputs/`.

## Phase 1 Local Smoke Test

Run from `D:\ICLR_2\src`:

```powershell
.\launch_phase1_mock.ps1
```

This uses `MockProver` and synthetic goals only to validate:

- JSON schema;
- failure parser;
- fixed-budget evaluation loop;
- first-failure recovery accounting;
- Rule-FAR controller;
- markdown analysis output.

The mock numbers are not paper evidence. Server-side Lean experiments will keep
the same schema and replace `MockProver` with a Lean/hammer backend.
