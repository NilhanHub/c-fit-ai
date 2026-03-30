from pathlib import Path

from scripts.package_prompt01_evidence import iter_paths


def test_evidence_packaging_excludes_runtime_caches() -> None:
    relative_paths = [path.relative_to(Path.cwd()).as_posix() for path in iter_paths()]

    assert relative_paths, "Expected Prompt #01 evidence packaging to include files"
    assert all("__pycache__" not in path for path in relative_paths)
    assert all(not path.endswith(".pyc") for path in relative_paths)
