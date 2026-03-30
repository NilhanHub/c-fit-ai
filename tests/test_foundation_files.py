from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT_FILES = [
    "README.md",
    "AGENT_GUIDE.md",
    "MARKET_MODEL_SPEC.md",
    "RESEARCH_METHODOLOGY.md",
    "SCORING_FRAMEWORK.md",
    "POPULATION_MODEL_PLAN.md",
    "FIRM_MODEL_PLAN.md",
    "OFFER_DISCOVERY_PLAN.md",
    "EXPERIMENT_PLAN.md",
    "TODO.md",
    "CHANGELOG.md",
    "EVIDENCE_INDEX.md",
    "pyproject.toml",
]

REQUIRED_DIRECTORIES = [
    "contracts",
    "data/raw",
    "data/interim",
    "data/processed",
    "data/external_offers",
    "population",
    "firms",
    "offers",
    "scoring",
    "simulation",
    "experiments",
    "validation",
    "scripts",
    "notebooks",
    "evidence",
    "docs",
    "tests",
]


def test_required_files_exist_and_are_non_empty() -> None:
    missing = []
    empty = []

    for relative_path in REQUIRED_ROOT_FILES:
        path = REPO_ROOT / relative_path
        if not path.exists():
            missing.append(relative_path)
        elif not path.read_text(encoding="utf-8").strip():
            empty.append(relative_path)

    assert not missing, f"Missing required files: {missing}"
    assert not empty, f"Required files are empty: {empty}"


def test_required_directories_exist() -> None:
    missing = [
        relative_path
        for relative_path in REQUIRED_DIRECTORIES
        if not (REPO_ROOT / relative_path).exists()
    ]
    assert not missing, f"Missing required directories: {missing}"


def test_readme_describes_current_limitations() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "not built yet" in readme.lower()
    assert "colombo" in readme.lower()
    assert "machine-readable" in readme.lower()
