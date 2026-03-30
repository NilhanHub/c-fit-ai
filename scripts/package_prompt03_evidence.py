"""Create the Prompt #03 evidence zip in the shared Score_Leads evidence directory."""

from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPO_ROOT = Path(__file__).resolve().parents[1]
ZIP_TARGET = Path(r"D:\AI-Apps-In-Drive\App_Station\Score_Leads\Evidence\PROMPT#03.zip")
MANDATORY_PATHS = [
    "README.md",
    "PROMPT03_CONTINUITY_AUDIT.md",
    "COMMERCIAL_TARGET_STATE.md",
    "PROMPT03_MASTER_PLAN.md",
    "PROMPT03_PHASE_TRACKER.md",
    "task_rubric.md",
    "STATUS.md",
    "DECISIONS.md",
    "REJECTED_IDEAS.md",
    "research",
    "model",
    "contracts",
    "data/seed",
    "data/curated",
    "data/snapshots",
    "population",
    "firms",
    "offers",
    "scoring",
    "experiments",
    "validation",
    "outputs",
    "reports",
    "qa",
    "HANDOFF",
    "scripts",
    "tests",
    "evidence",
]

EXCLUDED_PATH_MARKERS = {"__pycache__", ".pytest_cache", ".venv", ".benchmarks", "node_modules", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".pyd"}


def should_include(path: Path) -> bool:
    return not any(part in EXCLUDED_PATH_MARKERS for part in path.parts) and path.suffix not in EXCLUDED_SUFFIXES


def iter_paths() -> list[Path]:
    paths: list[Path] = []
    for relative in MANDATORY_PATHS:
        path = REPO_ROOT / relative
        if path.is_dir():
            paths.extend(sorted(candidate for candidate in path.rglob("*") if candidate.is_file() and should_include(candidate)))
        elif path.is_file() and should_include(path):
            paths.append(path)
    return paths


def main() -> None:
    ZIP_TARGET.parent.mkdir(parents=True, exist_ok=True)
    file_paths = iter_paths()
    with ZipFile(ZIP_TARGET, "w", ZIP_DEFLATED) as archive:
        for file_path in file_paths:
            archive.write(file_path, file_path.relative_to(REPO_ROOT))
    print(json.dumps({"prompt": "PROMPT#03", "zip_target": str(ZIP_TARGET), "file_count": len(file_paths)}))


if __name__ == "__main__":
    main()
