import json
import subprocess
import sys
from pathlib import Path

from scripts.san_preflight import build_report
from scripts.san_verify import build_command_plan


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SAN_FILES = [
    "AGENTS.md",
    "san/control_plane.json",
    "san/durable_state.json",
    "san/runtime_manifest.json",
    "san/artifact_classes.json",
    "san/topology/topology.graph.json",
    "san/sanlock_scorecard.json",
    "san/control-plane.md",
    "san/state/durable-state.md",
    "san/preflight.md",
    "san/sanlock.md",
    "san/topology/node-index.md",
    "san/state/authority-map.md",
    "san/state/export-boundary.md",
    "san/state/recurring-failures.md",
    "scripts/san_sync.py",
    "scripts/san_preflight.py",
    "scripts/san_topology.py",
    "scripts/sanlock.py",
    "scripts/san_verify.py",
]


def test_san_core_files_exist() -> None:
    missing = [path for path in REQUIRED_SAN_FILES if not (REPO_ROOT / path).exists()]
    assert not missing, f"Missing SAN files: {missing}"


def test_runtime_manifest_declares_dual_node_repo() -> None:
    manifest = json.loads((REPO_ROOT / "san" / "runtime_manifest.json").read_text(encoding="utf-8"))

    assert manifest["repo_shape"] == "dual-node"
    assert "uv run pytest -q" in manifest["verification_entrypoints"]["python"]
    assert "npm --prefix apps/web test" in manifest["verification_entrypoints"]["web"]
    assert "npm --prefix apps/web run typecheck" in manifest["verification_entrypoints"]["web"]
    assert "san/control-plane.md" in manifest["cold_start_sequence"]


def test_topology_graph_covers_both_product_lines() -> None:
    graph = json.loads(
        (REPO_ROOT / "san" / "topology" / "topology.graph.json").read_text(encoding="utf-8")
    )
    node_ids = {node["id"] for node in graph["nodes"]}

    assert graph["authoritative"] is True
    assert {
        "san.repo_os",
        "sim.market_core",
        "sim.research_evidence",
        "jobs.web_app",
        "jobs.product_doctrine",
        "jobs.design_ux",
        "shared.tests_and_scripts",
    }.issubset(node_ids)


def test_san_sync_check_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "san_sync.py"), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout


def test_san_preflight_and_sanlock_run() -> None:
    for script_name in ("san_preflight.py", "san_topology.py", "sanlock.py"):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / script_name)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"{script_name} failed: {result.stderr or result.stdout}"


def test_san_verify_uses_windows_safe_npm_invocation() -> None:
    commands = build_command_plan()
    npm_commands = [command for command in commands if "apps/web" in " ".join(command)]

    assert npm_commands
    assert any(command[0].lower().endswith("npm.cmd") for command in npm_commands)
    assert any(command[-1] == "test" for command in npm_commands)
    assert all("--runInBand" not in command for command in npm_commands)


def test_preflight_tracks_live_git_baseline_state() -> None:
    report = build_report({
        "control": json.loads((REPO_ROOT / "san" / "control_plane.json").read_text(encoding="utf-8")),
        "runtime": json.loads((REPO_ROOT / "san" / "runtime_manifest.json").read_text(encoding="utf-8")),
        "graph": json.loads((REPO_ROOT / "san" / "topology" / "topology.graph.json").read_text(encoding="utf-8")),
        "scorecard": json.loads((REPO_ROOT / "san" / "sanlock_scorecard.json").read_text(encoding="utf-8")),
    })

    head_commit = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    assert head_commit
    assert report["versioned_change_surface"]["head_ref"] == "HEAD"
    assert report["versioned_change_surface"]["history_present"] is True
    assert not any(
        "pending until git commit exists" in item.lower()
        for item in report["signs_of_under_specification"]
    )
