# Mathlib / LeanHammer Compatibility Probe

- Hammer root: `/workspace/thymic_project/paper/iclr_2/repos/LeanHammer`
- Mathlib root: `/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current`
- Lean 4.30: `/root/.elan/toolchains/leanprover--lean4---v4.30.0/bin/lean`
- Lean 4.31: `/root/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean`

| Probe | Success | Return code | Time |
|---|---:|---:|---:|
| `hammer_only_lake_env` | false | 1 | 4.10s |
| `mathlib_only_lake_env` | false | 1 | 5.15s |
| `combined_with_lean31` | false | 1 | 0.29s |
| `combined_with_lean30` | false | 1 | 0.28s |

## Verdict

- Combined Mathlib + LeanHammer import does not currently work in this environment.
- This blocks Mathlib-scale verified LeanHammer experiments until we use a compatible Mathlib/LeanHammer pair or patch LeanHammer for the current Mathlib toolchain.

## Output Tails

### hammer_only_lake_env

```text
/workspace/thymic_project/paper/iclr_2/outputs/mathlib_leanhammer_compat_probe_files/HammerOnly.lean:1:0: error: unknown module prefix 'Duper'

No directory 'Duper' or file 'Duper.olean' in the search path entries:
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/auto/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/batteries/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/premise-selection/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Qq/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/aesop/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Duper/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/build/lib/lean
/root/.elan/toolchains/leanprover--lean4---v4.30.0/lib/lean
/root/.elan/toolchains/leanprover--lean4---v4.30.0/lib/lean

info: Duper: cloning https://github.com/leanprover-community/duper.git
info: Duper: checking out revision '3e56459ec9cc7a1b2f6465f5a4208564f9d9d9c3'
warning: aesop: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/aesop' has local changes
warning: Qq: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Qq' has local changes
warning: premise-selection: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/premise-selection' has local changes
warning: batteries: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/batteries' has local changes
warning: auto: repository '/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/auto' has local changes
```

### mathlib_only_lake_env

```text
/workspace/thymic_project/paper/iclr_2/outputs/mathlib_leanhammer_compat_probe_files/MathlibOnly.lean:1:0: error: unknown module prefix 'Mathlib'

No directory 'Mathlib' or file 'Mathlib.olean' in the search path entries:
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/Cli/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/batteries/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/Qq/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/aesop/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/proofwidgets/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/importGraph/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/LeanSearchClient/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/packages/plausible/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/mathlib4_current/.lake/build/lib/lean
/root/.elan/toolchains/leanprover--lean4---v4.31.0/lib/lean
/root/.elan/toolchains/leanprover--lean4---v4.31.0/lib/lean

info: plausible: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/plausible
info: plausible: checking out revision '41783c75501a955e153a9a08bf018f8f61cb41a8'
info: LeanSearchClient: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/LeanSearchClient
info: LeanSearchClient: checking out revision '857a70579c135b9af82c4a23b36f1f9aa825626c'
info: importGraph: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/importGraph
info: importGraph: checking out revision 'fd3f8a0727635c1fbfd821d1981ff2e55729072c'
info: proofwidgets: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/proofwidgets
info: proofwidgets: checking out revision '11dc89eaffec1673c78c28032fc1864dc1ec8e95'
info: aesop: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/aesop
info: aesop: checking out revision '4e9929b7f7b2b22da5e02f34a68257fccf61adf0'
info: Qq: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/Qq
info: Qq: checking out revision '1f12f19bd017580ff24a3ce675dbfcd9aefce3c3'
info: batteries: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/batteries
info: batteries: checking out revision '11fc13e35b03ec392c85ec4bccf9a0ac6e3ea09f'
info: Cli: cloning file:///workspace/thymic_project/paper/iclr_2/repos/mathlib_dep_mirrors/Cli
info: Cli: checking out revision '448e08ce0f242270750b7f1d1167f6fb5d50dacb'
```

### combined_with_lean31

```text
/workspace/thymic_project/paper/iclr_2/outputs/mathlib_leanhammer_compat_probe_files/Combined.lean:1:0: error: unknown module prefix 'Mathlib'

No directory 'Mathlib' or file 'Mathlib.olean' in the search path entries:
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Qq/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/aesop/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/auto/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/batteries/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/premise-selection/.lake/build/lib/lean
/root/.elan/toolchains/leanprover--lean4---v4.31.0/lib/lean
```

### combined_with_lean30

```text
/workspace/thymic_project/paper/iclr_2/outputs/mathlib_leanhammer_compat_probe_files/Combined.lean:1:0: error: unknown module prefix 'Mathlib'

No directory 'Mathlib' or file 'Mathlib.olean' in the search path entries:
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/Qq/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/aesop/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/auto/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/batteries/.lake/build/lib/lean
/workspace/thymic_project/paper/iclr_2/repos/LeanHammer/.lake/packages/premise-selection/.lake/build/lib/lean
/root/.elan/toolchains/leanprover--lean4---v4.30.0/lib/lean
```
