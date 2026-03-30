"""Create the Prompt #05 evidence zip in the shared Score_Leads evidence directory."""

from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPO_ROOT = Path(__file__).resolve().parents[1]
ZIP_TARGET = Path(r"D:\AI-Apps-In-Drive\App_Station\Score_Leads\Evidence\PROMPT#05.zip")
MANDATORY_PATHS = [
    "README.md",
    "task_rubric.md",
    "STATUS.md",
    "DECISIONS.md",
    "REJECTED_IDEAS.md",
    "PROMPT05_CONTINUITY_AUDIT.md",
    "PROMPT05_VISUAL_FORENSICS.md",
    "PROMPT05_SURFACE_GAP_MAP.md",
    "research",
    "product",
    "ux",
    "stories",
    "trust",
    "architecture",
    "design",
    "ranking",
    "alerts",
    "employer",
    "mobile",
    "desktop",
    "copy",
    "build",
    "demo",
    "qa",
    "HANDOFF",
    "apps/web",
    "tests",
    "scripts",
    "evidence",
]

EXCLUDED_PATH_MARKERS = {"__pycache__", ".pytest_cache", ".venv", ".benchmarks", "dist", "node_modules"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".pyd"}


def should_include(path: Path) -> bool:
    return not any(part in EXCLUDED_PATH_MARKERS for part in path.parts) and path.suffix not in EXCLUDED_SUFFIXES


def iter_paths() -> list[Path]:
    paths: list[Path] = []
    for relative in MANDATORY_PATHS:
        path = REPO_ROOT / relative
        if path.is_dir():
            paths.extend(
                sorted(candidate for candidate in path.rglob("*") if candidate.is_file() and should_include(candidate))
            )
        elif path.is_file() and should_include(path):
            paths.append(path)
    return paths


def main() -> None:
    ZIP_TARGET.parent.mkdir(parents=True, exist_ok=True)
    file_paths = iter_paths()

    with ZipFile(ZIP_TARGET, "w", ZIP_DEFLATED) as archive:
        for file_path in file_paths:
            archive.write(file_path, file_path.relative_to(REPO_ROOT))

    manifest = {
        "prompt": "PROMPT#05",
        "zip_target": str(ZIP_TARGET),
        "file_count": len(file_paths),
        "files": [str(file_path.relative_to(REPO_ROOT)) for file_path in file_paths],
    }
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
