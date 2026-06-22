# Gate 1 Mathlib-Context LeanHammer Smoke

- Verdict: `pass`
- Hammer root: `/workspace/thymic_project/paper/iclr_2/repos/LeanHammer`
- Mathlib root: `/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430`
- Lean version: `Lean (version 4.30.0, x86_64-unknown-linux-gnu, commit d024af099ca4bf2c86f649261ebf59565dc8c622, Release)`
- Jobs: 8
- Timeout per attempt: 120.0s

| Goal | Variant | Premises | Expected | Verified | Status | Time |
|---|---|---|---:|---:|---|---:|
| `mathlib_nat_add_comm` | `complete` | `Nat.add_comm` | true | true | `proved` | 10.74s |
| `mathlib_nat_add_comm` | `empty` | `` | false | false | `search_fail` | 10.54s |
| `mathlib_nat_add_comm` | `wrong_theorem` | `Nat.mul_comm` | false | false | `search_fail` | 10.48s |
| `mathlib_nat_add_comm` | `extra_noise` | `Nat.add_comm, Nat.mul_comm` | true | true | `proved` | 10.65s |
| `mathlib_nat_mul_comm` | `complete` | `Nat.mul_comm` | true | true | `proved` | 10.53s |
| `mathlib_nat_mul_comm` | `empty` | `` | false | false | `search_fail` | 10.86s |
| `mathlib_nat_mul_comm` | `wrong_theorem` | `Nat.add_comm` | false | false | `search_fail` | 11.25s |
| `mathlib_nat_mul_comm` | `extra_noise` | `Nat.mul_comm, Nat.add_comm` | true | true | `proved` | 10.31s |
| `mathlib_nat_add_assoc` | `complete` | `Nat.add_assoc` | true | true | `proved` | 10.17s |
| `mathlib_nat_add_assoc` | `empty` | `` | false | false | `search_fail` | 10.25s |
| `mathlib_nat_add_assoc` | `wrong_theorem` | `Nat.mul_assoc` | false | false | `search_fail` | 10.02s |
| `mathlib_nat_add_assoc` | `extra_noise` | `Nat.add_assoc, Nat.mul_assoc` | true | true | `proved` | 11.00s |
| `mathlib_nat_mul_assoc` | `complete` | `Nat.mul_assoc` | true | true | `proved` | 10.48s |
| `mathlib_nat_mul_assoc` | `empty` | `` | false | false | `search_fail` | 10.06s |
| `mathlib_nat_mul_assoc` | `wrong_theorem` | `Nat.add_assoc` | false | false | `search_fail` | 10.69s |
| `mathlib_nat_mul_assoc` | `extra_noise` | `Nat.mul_assoc, Nat.add_assoc` | true | true | `proved` | 10.63s |
| `mathlib_nat_gcd_comm` | `complete` | `Nat.gcd_comm` | true | true | `proved` | 10.22s |
| `mathlib_nat_gcd_comm` | `empty` | `` | false | false | `search_fail` | 10.56s |
| `mathlib_nat_gcd_comm` | `wrong_theorem` | `Nat.lcm_comm` | false | false | `search_fail` | 10.08s |
| `mathlib_nat_gcd_comm` | `extra_noise` | `Nat.gcd_comm, Nat.lcm_comm` | true | true | `proved` | 10.00s |
| `mathlib_nat_lcm_comm` | `complete` | `Nat.lcm_comm` | true | true | `proved` | 9.99s |
| `mathlib_nat_lcm_comm` | `empty` | `` | false | false | `search_fail` | 10.90s |
| `mathlib_nat_lcm_comm` | `wrong_theorem` | `Nat.gcd_comm` | false | false | `search_fail` | 10.68s |
| `mathlib_nat_lcm_comm` | `extra_noise` | `Nat.lcm_comm, Nat.gcd_comm` | true | true | `proved` | 10.90s |
| `mathlib_int_add_assoc` | `complete` | `Int.add_assoc` | true | true | `proved` | 10.30s |
| `mathlib_int_add_assoc` | `empty` | `` | false | false | `search_fail` | 10.46s |
| `mathlib_int_add_assoc` | `wrong_theorem` | `Nat.add_assoc` | false | false | `search_fail` | 10.16s |
| `mathlib_int_add_assoc` | `extra_noise` | `Int.add_assoc, Nat.add_assoc` | true | true | `proved` | 10.13s |
| `mathlib_set_subset_trans` | `complete` | `Set.Subset.trans, h_st, h_tu` | true | true | `proved` | 11.01s |
| `mathlib_set_subset_trans` | `missing_trans` | `h_st, h_tu` | false | false | `search_fail` | 10.52s |
| `mathlib_set_subset_trans` | `wrong_theorem` | `Set.Subset.antisymm, h_st, h_tu` | false | false | `search_fail` | 10.09s |
| `mathlib_set_subset_trans` | `extra_noise` | `Set.Subset.trans, h_st, h_tu, Set.Subset.antisymm` | true | true | `proved` | 10.60s |

## Gate Readout

- Gate 1 passes in a Mathlib 4.30 context: explicit premise lists change kernel-verified LeanHammer outcomes.
- The controlled backend has `autoPremises`, `aesopPremises`, and `grindPremises` set to zero, so selector premises are not contributing.

## Expectation Misses

- None.

## Trace Check

### mathlib_nat_add_comm / complete

- user input terms: `[Nat.add_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_add_comm / empty

- user input terms: `[]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_add_comm / wrong_theorem

- user input terms: `[Nat.mul_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_add_comm / extra_noise

- user input terms: `[Nat.add_comm, Nat.mul_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_comm / complete

- user input terms: `[Nat.mul_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_comm / empty

- user input terms: `[]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_comm / wrong_theorem

- user input terms: `[Nat.add_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_comm / extra_noise

- user input terms: `[Nat.mul_comm, Nat.add_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_add_assoc / complete

- user input terms: `[Nat.add_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_add_assoc / empty

- user input terms: `[]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_add_assoc / wrong_theorem

- user input terms: `[Nat.mul_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_add_assoc / extra_noise

- user input terms: `[Nat.add_assoc, Nat.mul_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_assoc / complete

- user input terms: `[Nat.mul_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_assoc / empty

- user input terms: `[]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_assoc / wrong_theorem

- user input terms: `[Nat.add_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_mul_assoc / extra_noise

- user input terms: `[Nat.mul_assoc, Nat.add_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_gcd_comm / complete

- user input terms: `[Nat.gcd_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_gcd_comm / empty

- user input terms: `[]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_gcd_comm / wrong_theorem

- user input terms: `[Nat.lcm_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_gcd_comm / extra_noise

- user input terms: `[Nat.gcd_comm, Nat.lcm_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_lcm_comm / complete

- user input terms: `[Nat.lcm_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_lcm_comm / empty

- user input terms: `[]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_lcm_comm / wrong_theorem

- user input terms: `[Nat.gcd_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_nat_lcm_comm / extra_noise

- user input terms: `[Nat.lcm_comm, Nat.gcd_comm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_int_add_assoc / complete

- user input terms: `[Int.add_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_int_add_assoc / empty

- user input terms: `[]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_int_add_assoc / wrong_theorem

- user input terms: `[Nat.add_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_int_add_assoc / extra_noise

- user input terms: `[Int.add_assoc, Nat.add_assoc]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_set_subset_trans / complete

- user input terms: `[Set.Subset.trans, h_st, h_tu]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_set_subset_trans / missing_trans

- user input terms: `[h_st, h_tu]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_set_subset_trans / wrong_theorem

- user input terms: `[Set.Subset.antisymm, h_st, h_tu]`
- selector premises: `[]`
- selector premises after dedupe: `[]`

### mathlib_set_subset_trans / extra_noise

- user input terms: `[Set.Subset.trans, h_st, h_tu, Set.Subset.antisymm]`
- selector premises: `[]`
- selector premises after dedupe: `[]`
