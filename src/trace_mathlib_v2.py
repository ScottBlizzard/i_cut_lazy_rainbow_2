"""Trace mathlib4 with LeanDojo-v2 for Phase 1 real-goal generation.

Run this in the Python 3.11 LeanDojo-v2 environment on A40:

    conda activate /workspace/thymic_project/paper/iclr2_py311
    source /root/.elan/env
    python trace_mathlib_v2.py --commit <mathlib4-commit>

The script intentionally does not import the repo's main `lean_dojo` package.
LeanDojo-v1 is not compatible with Lean 4.31 tracing; this script uses
`lean_dojo_v2.lean_dojo`.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-url",
        default="https://github.com/leanprover-community/mathlib4",
    )
    parser.add_argument("--repo-path", type=Path, default=None)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--dst-dir", type=Path, default=None)
    parser.add_argument("--summary", type=Path, default=Path("../outputs/mathlib4_trace_v2_summary.json"))
    parser.add_argument("--build-deps", action="store_true")
    args = parser.parse_args()

    start = time.perf_counter()
    from lean_dojo_v2.lean_dojo import LeanGitRepo, trace

    if args.repo_path is not None:
        repo = LeanGitRepo.from_path(args.repo_path)
    else:
        repo = LeanGitRepo(args.repo_url, args.commit)
    traced = trace(repo, dst_dir=args.dst_dir, build_deps=args.build_deps)
    elapsed = time.perf_counter() - start

    n_theorems = 0
    n_tactic_theorems = 0
    for tf in traced.traced_files:
        for thm in tf.get_traced_theorems():
            n_theorems += 1
            if thm.has_tactic_proof():
                n_tactic_theorems += 1

    summary = {
        "repo_url": args.repo_url,
        "commit": repo.commit,
        "lean_version": repo.lean_version,
        "traced_root": str(traced.root_dir),
        "n_files": len(traced.traced_files),
        "n_theorems": n_theorems,
        "n_tactic_theorems": n_tactic_theorems,
        "build_deps": args.build_deps,
        "elapsed_s": elapsed,
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
