# Gate 1 LeanHammer Premise-Intervention Smoke

- Hammer root: `/workspace/thymic_project/paper/iclr_2/repos/LeanHammer`
- Timeout per attempt: 60.0s
- Verdict: `pass`

| Goal | Variant | Premises | Expected | Verified | Status | Time |
|---|---|---|---:|---:|---|---:|
| `prop_chain3` | `complete` | `p_A, p_A_to_B, p_B_to_C` | true | true | `proved` | 3.51s |
| `prop_chain3` | `missing_bridge` | `p_A, p_A_to_B` | false | false | `search_fail` | 3.56s |
| `prop_chain3` | `wrong_direction` | `p_A, distractor_AB, p_B_to_C` | false | false | `search_fail` | 3.53s |
| `prop_chain3` | `extra_noise` | `p_A, p_A_to_B, p_B_to_C, distractor_AB` | true | true | `proved` | 3.52s |
| `prop_conjunction` | `complete` | `p_P, p_Q` | true | true | `proved` | 3.51s |
| `prop_conjunction` | `missing_right` | `p_P` | false | false | `search_fail` | 3.58s |
| `prop_conjunction` | `missing_left` | `p_Q` | false | false | `search_fail` | 3.51s |
| `prop_conjunction` | `extra_noise` | `p_P, p_Q, p_Q_to_P` | true | true | `proved` | 3.52s |

## Gate Readout

- Gate 1 passes for the minimal LeanHammer interface: changing the explicit premise list changes verified outcome.
- The smoke uses `hammer [premises]` with selector premise counts set to zero, so the explicit premise intervention is the controlled variable.

## Trace Check

### prop_chain3 / complete

- user input terms: `[p_A, p_A_to_B, p_B_to_C]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### prop_chain3 / missing_bridge

- user input terms: `[p_A, p_A_to_B]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### prop_chain3 / wrong_direction

- user input terms: `[p_A, distractor_AB, p_B_to_C]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### prop_chain3 / extra_noise

- user input terms: `[p_A, p_A_to_B, p_B_to_C, distractor_AB]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### prop_conjunction / complete

- user input terms: `[p_P, p_Q]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### prop_conjunction / missing_right

- user input terms: `[p_P]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### prop_conjunction / missing_left

- user input terms: `[p_Q]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### prop_conjunction / extra_noise

- user input terms: `[p_P, p_Q, p_Q_to_P]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

