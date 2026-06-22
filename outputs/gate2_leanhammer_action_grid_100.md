# Gate 2 LeanHammer Action-Grid Pilot

Every action below is evaluated by an actual LeanHammer call with an explicit premise list.

- Goals: 100
- Attempts: 900
- Oracle adaptive success: 80.0%
- Best static action: `expand_200` at 40.0%
- Oracle gap over best static: +40.0 pp

| Action | Goals | Verified | Success | Avg premises | Avg time |
|---|---:|---:|---:|---:|---:|
| `keep` | 100 | 0 | 0.0% | 3.0 | 3.69s |
| `shrink_050` | 100 | 0 | 0.0% | 2.0 | 3.68s |
| `shrink_075` | 100 | 0 | 0.0% | 3.0 | 3.69s |
| `expand_150` | 100 | 20 | 20.0% | 5.0 | 3.68s |
| `expand_200` | 100 | 40 | 40.0% | 6.0 | 3.70s |
| `base_rescue_8` | 100 | 20 | 20.0% | 11.0 | 3.69s |
| `base_rescue_16` | 100 | 20 | 20.0% | 11.0 | 3.69s |
| `second_stage_rescore` | 100 | 20 | 20.0% | 11.0 | 3.69s |
| `stop` | 100 | 0 | 0.0% | 0.0 | 0.00s |

Gate 2 pilot verdict: `pass`.

Caveat: this is a synthetic verified-backend pilot. It validates the action-grid mechanics and oracle-headroom computation, but Mathlib-scale evaluation is still required for a paper claim.
