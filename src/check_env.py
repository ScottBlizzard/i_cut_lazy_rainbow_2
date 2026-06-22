"""Phase 0 environment check for local/server runs."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
from importlib import metadata


def version_cmd(cmd: list[str]) -> str:
    exe = shutil.which(cmd[0])
    if exe is None:
        return "MISSING"
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=60)
        return out.strip().splitlines()[0]
    except Exception as exc:
        return f"ERROR: {exc}"


def module_version(name: str) -> str:
    spec = importlib.util.find_spec(name)
    if spec is None:
        return "MISSING"
    package_name = {
        "sentence_transformers": "sentence-transformers",
        "sklearn": "scikit-learn",
        "faiss": "faiss-cpu",
        "lean_dojo": "lean-dojo",
    }.get(name, name)
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return "present"


def main() -> None:
    elan_bin = Path.home() / ".elan" / "bin"
    if elan_bin.exists():
        os.environ["PATH"] = f"{elan_bin}:{os.environ.get('PATH', '')}"
    print("python:", sys.version.replace("\n", " "))
    print("lean:", version_cmd(["lean", "--version"]))
    print("lake:", version_cmd(["lake", "--version"]))
    print("git:", version_cmd(["git", "--version"]))
    for mod in ["torch", "transformers", "sentence_transformers", "sklearn", "faiss", "lean_dojo"]:
        print(f"{mod}:", module_version(mod))


if __name__ == "__main__":
    main()
