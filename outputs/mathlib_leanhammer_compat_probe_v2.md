# Mathlib 4.30 / LeanHammer 4.30 Compatibility Probe

- Verdict: `pass`
- Hammer root: `/workspace/thymic_project/paper/iclr_2/repos/LeanHammer`
- Hammer commit: `3ef50193c9e80f84930f8f400bfd3c097c5e1fd3`
- Hammer toolchain: `leanprover/lean4:v4.30.0`
- Mathlib root: `/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430`
- Mathlib commit: `c5ea00351c28e24afc9f0f84379aa41082b1188f`
- Mathlib toolchain: `leanprover/lean4:v4.30.0`
- Combined Lean version: `Lean (version 4.30.0, x86_64-unknown-linux-gnu, commit d024af099ca4bf2c86f649261ebf59565dc8c622, Release)`

| Probe | Success | Return code | Time |
|---|---:|---:|---:|
| `hammer_lake_lean_path` | true | 0 | 1.24s |
| `mathlib_lake_lean_path` | true | 0 | 1.21s |
| `hammer_only_lake_env` | true | 0 | 3.39s |
| `mathlib_only_lake_env` | true | 0 | 9.40s |
| `combined_lean_version` | true | 0 | 0.07s |
| `combined_import_mathlib_hammer` | true | 0 | 9.74s |

## Readout

- The route-A stack is usable: one Lean 4.30 process can import both `Mathlib` and `Hammer`.
- This removes the immediate Mathlib/LeanHammer compatibility blocker for Mathlib-context smoke tests.

## Output Tails

### hammer_lake_lean_path

```text
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/auto/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/batteries/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/premise-selection/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Qq/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/aesop/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Duper/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/build/lib/lean:/root/.elan/toolchains/leanprover--lean4---v4.30.0/lib/lean

warning: Duper: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Duper' has local changes
warning: aesop: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/aesop' has local changes
warning: Qq: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Qq' has local changes
warning: premise-selection: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/premise-selection' has local changes
warning: batteries: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/batteries' has local changes
warning: auto: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/auto' has local changes
```

### mathlib_lake_lean_path

```text
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/Cli/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/batteries/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/Qq/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/aesop/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/proofwidgets/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/importGraph/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/LeanSearchClient/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/packages/plausible/.lake/build/lib/lean:/workspace/thymic_project/paper/iclr_2/repos/mathlib4_lean430/.lake/build/lib/lean:/root/.elan/toolchains/leanprover--lean4---v4.30.0/lib/lean
```

### hammer_only_lake_env

```text
Hammer.evalHammer : Lean.Elab.Tactic.Tactic

warning: Duper: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Duper' has local changes
warning: aesop: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/aesop' has local changes
warning: Qq: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Qq' has local changes
warning: premise-selection: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/premise-selection' has local changes
warning: batteries: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/batteries' has local changes
warning: auto: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/auto' has local changes
```

### mathlib_only_lake_env

```text
Nat.add_comm (n m : ℕ) : n + m = m + n
```

### combined_lean_version

```text
Lean (version 4.30.0, x86_64-unknown-linux-gnu, commit d024af099ca4bf2c86f649261ebf59565dc8c622, Release)
```

### combined_import_mathlib_hammer

```text
Nat.add_comm (n m : ℕ) : n + m = m + n
Hammer.evalHammer : Lean.Elab.Tactic.Tactic
```
