# Gate 2 Mathlib-Context LeanHammer Action Grid

- Verdict: `pass`
- Hammer root: `/workspace/thymic_project/paper/iclr_2/repos/LeanHammer`
- Mathlib root: `/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430`
- Lean version: `Lean (version 4.30.0, x86_64-unknown-linux-gnu, commit d024af099ca4bf2c86f649261ebf59565dc8c622, Release)`
- Goals: 10
- Attempts: 90
- First failure rate: 100.0%

## Headroom

- Oracle adaptive: 80.0%
- True feedback policy: 80.0%
- Best static: `expand_200` at 40.0%
- Shuffled feedback: 0.0%
- Oracle - best static: 40.0 pp
- True - best static: 40.0 pp
- True - shuffled: 80.0 pp

## Action Success

| Action | Success |
|---|---:|
| `keep` | 0.0% |
| `shrink_050` | 0.0% |
| `shrink_075` | 0.0% |
| `expand_150` | 20.0% |
| `expand_200` | 40.0% |
| `base_rescue_8` | 20.0% |
| `base_rescue_16` | 20.0% |
| `second_stage_rescore` | 20.0% |
| `stop` | 0.0% |

## Gate Readout

- Mathlib-context Gate 2 passes for this theorem-family pilot: oracle adaptive headroom exceeds the 5 pp threshold under verified LeanHammer calls.
- This is still a generated Mathlib-context pilot, not a final traced-corpus result.
