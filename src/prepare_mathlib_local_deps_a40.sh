#!/usr/bin/env bash
set -euo pipefail

source /root/miniconda3/etc/profile.d/conda.sh
conda activate /workspace/thymic_project/paper/iclr2_py311
source /root/.elan/env

ROOT="/workspace/thymic_project/paper/iclr_2"
REPO_DIR="$ROOT/repos/mathlib4_current"
MIRROR_DIR="$ROOT/repos/mathlib_dep_mirrors"
ARCHIVE_DIR="$MIRROR_DIR/_archives"
WORK_DIR="$MIRROR_DIR/_work"
MAP_JSON="$MIRROR_DIR/local_dependency_map.json"

mkdir -p "$MIRROR_DIR" "$ARCHIVE_DIR"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

python - "$REPO_DIR/lake-manifest.json" "$MIRROR_DIR/packages.tsv" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
rows = []
for pkg in manifest["packages"]:
    rows.append((pkg["name"], pkg["url"], pkg["rev"]))
Path(sys.argv[2]).write_text(
    "\n".join("\t".join(row) for row in rows) + "\n",
    encoding="utf-8",
)
PY

while IFS=$'\t' read -r name url rev; do
  [ -n "$name" ] || continue
  path_part="${url#https://github.com/}"
  path_part="${path_part%.git}"
  owner="${path_part%%/*}"
  repo="${path_part#*/}"
  mirror="$MIRROR_DIR/$name"
  archive="$ARCHIVE_DIR/${owner}_${repo}_${rev}.tar.gz"

  if [ ! -d "$mirror/.git" ] || [ "$(cat "$mirror/.original_git_rev" 2>/dev/null || true)" != "$rev" ]; then
    echo "==> preparing $name from $owner/$repo@$rev"
    rm -rf "$mirror" "$WORK_DIR/$name"
    if [ ! -s "$archive" ]; then
      wget \
        --tries=5 \
        --timeout=120 \
        --read-timeout=120 \
        --waitretry=20 \
        -O "$archive" \
        "https://codeload.github.com/${owner}/${repo}/tar.gz/${rev}"
    else
      echo "==> reusing $archive"
    fi
    tar -xzf "$archive" -C "$WORK_DIR"
    top_dir="$(
      python - "$archive" <<'PY'
import sys
import tarfile

with tarfile.open(sys.argv[1], "r:gz") as tar:
    first = tar.next()
    if first is None:
        raise SystemExit("empty archive")
    print(first.name.split("/", 1)[0])
PY
    )"
    mv "$WORK_DIR/$top_dir" "$mirror"
    (
      cd "$mirror"
      git init -q
      git config user.email trace@example.com
      git config user.name trace
      printf "%s\n" "$url" > .original_git_url
      printf "%s\n" "$rev" > .original_git_rev
      git add .
      git commit -q -m "archive $rev"
    )
  else
    echo "==> reusing local mirror $name"
  fi
done < "$MIRROR_DIR/packages.tsv"

python - "$REPO_DIR/lake-manifest.json" "$MIRROR_DIR" "$MAP_JSON" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
mirror_dir = Path(sys.argv[2])
map_path = Path(sys.argv[3])
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
mapping = {}

for pkg in manifest["packages"]:
    name = pkg["name"]
    mirror = (mirror_dir / name).resolve()
    rev = subprocess.check_output(
        ["git", "-C", str(mirror), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    mapping[name] = {
        "original_url": pkg["url"],
        "original_rev": pkg["rev"],
        "local_url": mirror.as_uri(),
        "local_rev": rev,
    }
    pkg["url"] = mirror.as_uri()
    pkg["rev"] = rev
    pkg["inputRev"] = rev

manifest_path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
map_path.write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
PY

(
  cd "$REPO_DIR"
  if [ ! -f lake-manifest.json.original_github_deps ]; then
    git show HEAD:lake-manifest.json > lake-manifest.json.original_github_deps || cp lake-manifest.json lake-manifest.json.original_github_deps
  fi
  git add lake-manifest.json lake-manifest.json.original_github_deps
  git commit -q -m "use local dependency mirrors for trace" || true
  git rev-parse HEAD
)

echo "==> wrote $MAP_JSON"
