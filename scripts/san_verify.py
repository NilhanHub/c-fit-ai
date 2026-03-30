"""Run the canonical SAN verification path."""

from __future__ import annotations

import shutil
import subprocess
import sys

try:
    from scripts.san_shared import REPO_ROOT, load_bundle
except ImportError:  # pragma: no cover - script execution path
    from san_shared import REPO_ROOT, load_bundle


def build_command_plan() -> list[list[str]]:
    npm_executable = shutil.which("npm.cmd") or shutil.which("npm") or "npm.cmd"
    return [
        [sys.executable, str(REPO_ROOT / "scripts" / "san_topology.py")],
        [sys.executable, str(REPO_ROOT / "scripts" / "sanlock.py")],
        [sys.executable, str(REPO_ROOT / "scripts" / "san_preflight.py")],
        [sys.executable, str(REPO_ROOT / "scripts" / "san_sync.py")],
        ["uv", "run", "pytest", "-q"],
        [npm_executable, "--prefix", "apps/web", "test"],
        [npm_executable, "--prefix", "apps/web", "run", "typecheck"],
        [sys.executable, str(REPO_ROOT / "scripts" / "san_sync.py"), "--check"],
    ]


def main() -> int:
    bundle = load_bundle()
    for command in build_command_plan():
        print("RUN", " ".join(command))
        result = subprocess.run(command, cwd=REPO_ROOT, check=False)
        if result.returncode != 0:
            return result.returncode
    print("SAN_VERIFY_PASSED", bundle["runtime"]["repo_shape"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
