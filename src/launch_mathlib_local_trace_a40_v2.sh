#!/usr/bin/env bash
set -euo pipefail

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2_py311
source /root/.elan/env
unset GITHUB_ACCESS_TOKEN

ROOT="/workspace/thymic_project/paper/iclr_2"
REPO_DIR="$ROOT/repos/mathlib4_current"
COMMIT="${1:-014c1563dc2c952488b6acfd3fac97ee588f0c6d}"
LOG="$ROOT/outputs/log_mathlib4_local_trace_v2_current.txt"
SUMMARY="$ROOT/outputs/mathlib4_local_trace_v2_current_summary.json"
ARCHIVE="$ROOT/repos/mathlib4_${COMMIT}.tar.gz"

mkdir -p "$ROOT/repos" "$ROOT/outputs"

{
  echo "==> target commit: $COMMIT"
  echo "==> repo dir: $REPO_DIR"

  if [ ! -d "$REPO_DIR/.git" ]; then
    rm -rf "$REPO_DIR"
    cloned=0
    if [ "${FORCE_ARCHIVE:-0}" != "1" ]; then
      for attempt in 1 2; do
        echo "==> git clone attempt $attempt"
        if timeout 120 git clone --depth 1 --single-branch https://github.com/leanprover-community/mathlib4.git "$REPO_DIR"; then
          cloned=1
          break
        fi
        rm -rf "$REPO_DIR"
        sleep $((attempt * 20))
      done
    else
      echo "==> FORCE_ARCHIVE=1; skipping git clone"
    fi
    if [ "$cloned" -eq 0 ]; then
      echo "==> git clone failed; falling back to GitHub codeload archive"
      rm -rf "$REPO_DIR" "$ROOT/repos/mathlib4-${COMMIT}"
      if [ ! -s "$ARCHIVE" ]; then
        wget \
          --tries=5 \
          --timeout=120 \
          --read-timeout=120 \
          --waitretry=20 \
          -O "$ARCHIVE" \
          "https://codeload.github.com/leanprover-community/mathlib4/tar.gz/${COMMIT}"
      else
        echo "==> reusing archive $ARCHIVE"
      fi
      tar -tzf "$ARCHIVE" > "$ROOT/repos/mathlib4_archive_files.txt"
      top_dir="$(head -n 1 "$ROOT/repos/mathlib4_archive_files.txt" | cut -d/ -f1)"
      tar -xzf "$ARCHIVE" -C "$ROOT/repos"
      mv "$ROOT/repos/$top_dir" "$REPO_DIR"
      cd "$REPO_DIR"
      git init -q
      git config user.email trace@example.com
      git config user.name trace
      git add .
      git commit -q -m "archive ${COMMIT}"
      echo "$COMMIT" > .original_mathlib4_commit
      git add .original_mathlib4_commit
      git commit -q -m "record original mathlib4 commit"
    fi
  else
    echo "==> reusing existing repo"
    cd "$REPO_DIR"
    git fetch --depth 1 origin master || true
  fi

  cd "$REPO_DIR"
  if git cat-file -e "$COMMIT^{commit}" 2>/dev/null; then
    git checkout "$COMMIT"
  else
    echo "==> original commit object not present in local repo; using local archive commit"
  fi
  git rev-parse HEAD

  cd "$ROOT/src"
  python trace_mathlib_v2.py \
    --repo-path "$REPO_DIR" \
    --summary "$SUMMARY"
} > "$LOG" 2>&1
