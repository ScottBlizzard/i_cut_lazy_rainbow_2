# Gate 2 LeanHammer Action-Grid Pilot

Every action below is evaluated by an actual LeanHammer call with an explicit premise list.

- Goals: 10
- Attempts: 90
- Oracle adaptive success: 80.0%
- Best static action: `expand_200` at 40.0%
- Oracle gap over best static: +40.0 pp

| Action | Goals | Verified | Success | Avg premises | Avg time |
|---|---:|---:|---:|---:|---:|
| `keep` | 10 | 0 | 0.0% | 3.0 | 3.61s |
| `shrink_050` | 10 | 0 | 0.0% | 2.0 | 3.60s |
| `shrink_075` | 10 | 0 | 0.0% | 3.0 | 3.60s |
| `expand_150` | 10 | 2 | 20.0% | 5.0 | 3.61s |
| `expand_200` | 10 | 4 | 40.0% | 6.0 | 3.62s |
| `base_rescue_8` | 10 | 2 | 20.0% | 11.0 | 3.59s |
| `base_rescue_16` | 10 | 2 | 20.0% | 11.0 | 3.62s |
| `second_stage_rescore` | 10 | 2 | 20.0% | 11.0 | 3.64s |
| `stop` | 10 | 0 | 0.0% | 0.0 | 0.00s |

Gate 2 pilot verdict: `pass`.

Caveat: this is a synthetic verified-backend pilot. It validates the action-grid mechanics and oracle-headroom computation, but Mathlib-scale evaluation is still required for a paper claim.
