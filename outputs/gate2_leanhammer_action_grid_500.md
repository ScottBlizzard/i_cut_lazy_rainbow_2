# Gate 2 LeanHammer Action-Grid Pilot

Every action below is evaluated by an actual LeanHammer call with an explicit premise list.

- Goals: 500
- Attempts: 4500
- Oracle adaptive success: 80.0%
- Best static action: `expand_200` at 40.0%
- Oracle gap over best static: +40.0 pp

| Action | Goals | Verified | Success | Avg premises | Avg time |
|---|---:|---:|---:|---:|---:|
| `keep` | 500 | 0 | 0.0% | 3.0 | 3.87s |
| `shrink_050` | 500 | 0 | 0.0% | 2.0 | 3.87s |
| `shrink_075` | 500 | 0 | 0.0% | 3.0 | 3.87s |
| `expand_150` | 500 | 100 | 20.0% | 5.0 | 3.88s |
| `expand_200` | 500 | 200 | 40.0% | 6.0 | 3.88s |
| `base_rescue_8` | 500 | 100 | 20.0% | 11.0 | 3.88s |
| `base_rescue_16` | 500 | 100 | 20.0% | 11.0 | 3.88s |
| `second_stage_rescore` | 500 | 100 | 20.0% | 11.0 | 3.88s |
| `stop` | 500 | 0 | 0.0% | 0.0 | 0.00s |

Gate 2 pilot verdict: `pass`.

Caveat: this is a synthetic verified-backend pilot. It validates the action-grid mechanics and oracle-headroom computation, but Mathlib-scale evaluation is still required for a paper claim.
