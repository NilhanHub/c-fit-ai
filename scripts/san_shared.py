"""Shared helpers for the repo-local SAN control plane."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SAN_ROOT = REPO_ROOT / "san"


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def git_head_commit() -> str | None:
    return git_output("rev-parse", "--verify", "HEAD")


def git_status_short() -> list[str]:
    output = git_output("status", "--short")
    if not output:
        return []
    return [line for line in output.splitlines() if line.strip()]


def load_bundle() -> dict[str, Any]:
    bundle = {
        "control": read_json(SAN_ROOT / "control_plane.json"),
        "durable": read_json(SAN_ROOT / "durable_state.json"),
        "runtime": read_json(SAN_ROOT / "runtime_manifest.json"),
        "artifacts": read_json(SAN_ROOT / "artifact_classes.json"),
        "graph": read_json(SAN_ROOT / "topology" / "topology.graph.json"),
    }
    scorecard_path = SAN_ROOT / "sanlock_scorecard.json"
    bundle["scorecard"] = read_json(scorecard_path) if scorecard_path.exists() else None
    return bundle


def _is_ignored(path: Path, runtime_manifest: dict[str, Any]) -> bool:
    ignored_parts = set(runtime_manifest["ignore_path_parts"])
    ignored_suffixes = tuple(runtime_manifest["ignored_suffixes"])
    return any(part in ignored_parts for part in path.parts) or path.name.endswith(ignored_suffixes)


def iter_owned_files(roots: list[str], runtime_manifest: dict[str, Any]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        path = REPO_ROOT / root
        if not path.exists():
            continue
        if path.is_file():
            if not _is_ignored(path.relative_to(REPO_ROOT), runtime_manifest):
                seen.add(path)
            continue
        for child in path.rglob("*"):
            if child.is_file():
                rel = child.relative_to(REPO_ROOT)
                if not _is_ignored(rel, runtime_manifest):
                    seen.add(child)
    files.extend(sorted(seen))
    return files


def collect_root_stats(roots: list[str], runtime_manifest: dict[str, Any]) -> dict[str, Any]:
    files = iter_owned_files(roots, runtime_manifest)
    return {
        "file_count": len(files),
        "total_bytes": sum(file.stat().st_size for file in files),
        "sample_paths": [file.relative_to(REPO_ROOT).as_posix() for file in files[:10]],
    }


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def md_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- none"


def render_control_plane_md(control: dict[str, Any]) -> str:
    canonical_rows = [
        [name.replace("_", " "), path]
        for name, path in control["canonical_surfaces"].items()
    ]
    product_lines = [
        f"`{product['id']}`: {product['name']} - {product['summary']}"
        for product in control["products"]
    ]
    return f"""# SAN Control Plane

## Repo Shape

- repo id: `{control['repo_id']}`
- repo shape: `{control['repo_shape']}`
- active modes: {", ".join(control['active_modes'])}

## Canonical Surfaces

{md_table(["Surface", "Path"], canonical_rows)}

## Product Nodes

{md_bullets(product_lines)}

## Active Work

- headline: {control['active_work']['headline']}
- status: `{control['active_work']['current_status']}`
- focus: {control['active_work']['bounded_focus']}

## Authority Rules

{md_bullets(control['authority_rules'])}
"""


def render_durable_state_md(durable: dict[str, Any]) -> str:
    decision_lines = [
        f"`{item['type']}` {item['date']}: {item['statement']} Why: {item['why']}"
        for item in durable["decisions"]
    ]
    unresolved = [
        f"`{item['severity']}`: {item['item']}"
        for item in durable["unresolved"]
    ]
    return f"""# SAN Durable State

## Current Focus

- {durable['current_focus']}

## Active Now

{md_bullets(durable['active_now'])}

## Next

{md_bullets(durable['next'])}

## Blocked

{md_bullets(durable['blocked'])}

## Decisions

{md_bullets(decision_lines)}

## Unresolved

{md_bullets(unresolved)}

## Resume

{md_bullets(durable['resume_instructions'])}

## Baseline Checkpoint

- status: `{durable['baseline_checkpoint']['status']}`
- policy: {durable['baseline_checkpoint']['policy']}
- recorded commit: `{durable['baseline_checkpoint']['recorded_commit']}`
"""


def render_authority_map_md(control: dict[str, Any]) -> str:
    rows = [
        [item["path"], item["authority"], item["artifact_class"], item["notes"]]
        for item in control["surface_classifications"]
    ]
    return "# Authority Map\n\n" + md_table(["Path", "Authority", "Artifact Class", "Notes"], rows)


def render_export_boundary_md(artifacts: dict[str, Any]) -> str:
    class_rows = [
        [item["id"], item["default_exposure"], item["description"]]
        for item in artifacts["classes"]
    ]
    boundary = artifacts["export_boundary"]
    return f"""# Export Boundary

## Artifact Classes

{md_table(["Class", "Default Exposure", "Description"], class_rows)}

## Boundary Rules

- outward sharing active: `{boundary['outward_sharing_active']}`
- private by default: {", ".join(boundary['private_by_default_classes'])}
- review required: {", ".join(boundary['review_required_for_export'])}

## Notes

{md_bullets(boundary['notes'])}
"""


def render_recurring_failures_md(durable: dict[str, Any]) -> str:
    rows = [
        [
            item["id"],
            str(item["occurrences"]),
            item["status"],
            item["pattern"],
        ]
        for item in durable["recurring_failures"]
    ]
    return "# Recurring Failures\n\n" + md_table(["Failure", "Occurrences", "Status", "Pattern"], rows)


def render_topology_index_md(graph: dict[str, Any]) -> str:
    node_rows = []
    for node in graph["nodes"]:
        node_rows.append(
            [
                node["id"],
                node["role"],
                f"{node['effectiveLoad']['percent']:.2f}",
                ", ".join(node["ownershipRoots"][:4]) + (" ..." if len(node["ownershipRoots"]) > 4 else ""),
                ", ".join(node["verificationEntrypoints"][:2]),
            ]
        )
    return "# Topology Index\n\n" + md_table(
        ["Node", "Role", "Load %", "Owned Roots", "Verification"],
        node_rows,
    )


def _score_summary(scorecard: dict[str, Any] | None) -> tuple[str, str]:
    if not scorecard:
        return ("pending", "No SANLOCK scorecard has been generated yet.")
    scores = [item["score"] for item in scorecard["scores"]]
    average = sum(scores) / len(scores)
    return (f"{average:.2f}/5", scorecard["summary"])


def render_readme(
    control: dict[str, Any],
    durable: dict[str, Any],
    runtime_manifest: dict[str, Any],
    scorecard: dict[str, Any] | None,
) -> str:
    san_score, san_summary = _score_summary(scorecard)
    verification_commands = [
        "uv run python scripts/san_verify.py",
        runtime_manifest["verification_entrypoints"]["python"][0],
        runtime_manifest["verification_entrypoints"]["web"][0],
    ]
    return f"""# C_fit_AI Dual-Node Colombo Workspace

This repository is a machine-readable dual-node workspace for Colombo product work. It keeps both the Colombo AI market simulator and the Colombo Jobs Pulse web product inside one SAN Repo OS so cold-start agents can discover authority, recover state, verify reality, and leave diffable progress.

## Live Product Lines

- `score-leads-market-simulator`: evidence-grounded Colombo / urban Sri Lanka B2C + B2B screening model.
- `colombo-jobs-pulse-web`: jobs operating system focused on freshness, trust, urgency, and repeat checking.

## Canonical SAN Entry Points

- doctrine: `AGENTS.md`
- control plane: `san/control-plane.md`
- durable state: `san/state/durable-state.md`
- topology: `san/topology/node-index.md`
- SANLOCK: `san/sanlock.md`

## Current State

- active focus: {durable['current_focus']}
- SAN score: {san_score}
- SAN summary: {san_summary}

## Not Built Yet

- a remote forge / PR workflow beyond local git
- pilot-calibrated simulator willingness-to-pay curves
- a production Jobs Pulse backend or multi-user deployment layer
- automated export gating for outward-safe sharing

## Verification

```bash
{verification_commands[0]}
{verification_commands[1]}
{verification_commands[2]}
```

## Cold Start

{md_bullets(runtime_manifest['cold_start_sequence'])}
"""


def render_agent_guide(
    control: dict[str, Any],
    durable: dict[str, Any],
    runtime_manifest: dict[str, Any],
) -> str:
    return f"""# Agent Guide

## How To Enter

1. Read `AGENTS.md`.
2. Read `san/control-plane.md`.
3. Read `san/state/durable-state.md`.
4. Read `san/preflight.md` and `san/topology/node-index.md`.
5. Use `san/runtime_manifest.json` instead of guessing commands.

## What To Read First By Node

- simulator code: `population/`, `firms/`, `offers/`, `scoring/`, `experiments/`
- simulator evidence: `research/`, `reports/`, `outputs/`, root simulator spec docs
- jobs web app: `apps/web/src/`
- jobs doctrine and UX: `product/`, `architecture/`, `design/`, `ux/`, `stories/`, `trust/`
- repo OS: `AGENTS.md`, `san/*.json`, `scripts/san_*.py`

## Canonical Verification Commands

{md_bullets(runtime_manifest['verification_entrypoints']['python'] + runtime_manifest['verification_entrypoints']['web'] + runtime_manifest['verification_entrypoints']['san'])}

## Current Resume Notes

{md_bullets(durable['resume_instructions'])}

## What Not To Break

- Do not collapse the simulator and Jobs Pulse into one blended product truth.
- Do not treat prompt-era docs as canonical authority.
- Do not hand-edit generated mirrors that `san_sync.py` owns.
- Do not bypass topology or SANLOCK refresh after structural changes.
"""


def render_status_md(durable: dict[str, Any], scorecard: dict[str, Any] | None) -> str:
    san_score, san_summary = _score_summary(scorecard)
    return f"""# Status

## Current Focus

- `{durable['current_focus']}`

## Current State

- `FACT`: the repo now has one intended canonical doctrine path through `AGENTS.md` and the SAN manifests.
- `FACT`: both the simulator and Jobs Pulse remain live bounded nodes.
- `FACT`: prompt-era artifacts are retained as historical evidence rather than control-plane truth.
- `INFERENCE`: SAN maturity is currently `{san_score}`.
- `INFERENCE`: {san_summary}
"""


def render_decisions_md(durable: dict[str, Any]) -> str:
    lines = ["# Decisions", ""]
    for item in durable["decisions"]:
        lines.append(f"## {item['date']}")
        lines.append("")
        lines.append(f"- `{item['type']}`: {item['statement']}")
        lines.append(f"- why: {item['why']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_task_rubric_md(control: dict[str, Any], durable: dict[str, Any]) -> str:
    weapon_rows = [[item["weapon"], item["why"]] for item in control["chosen_weapons"]]
    gaps = [
        "No project-local copy of using-superpowers exists, so the global skill is used for gateway routing.",
        "Prompt-era artifacts remain numerous, so historical classification is required to avoid shadow authority.",
        "Remote-forge policy is still unset because the repo only has local git right now."
    ]
    return f"""# SAN Retrofit Task Rubric

## Mission Understanding

- Retrofit `D:/AI/C_fit_AI` into a dual-node SAN Repo OS without deleting either product line.

## Chosen Weapons

{md_table(["Weapon", "Why"], weapon_rows)}

## Capability Gaps

{md_bullets(gaps)}

## Active Repo Focus

{md_bullets(durable['active_now'])}
"""


def generate_mirrors(bundle: dict[str, Any]) -> dict[Path, str]:
    control = bundle["control"]
    durable = bundle["durable"]
    runtime_manifest = bundle["runtime"]
    artifacts = bundle["artifacts"]
    graph = bundle["graph"]
    scorecard = bundle["scorecard"]
    return {
        SAN_ROOT / "control-plane.md": render_control_plane_md(control),
        SAN_ROOT / "state" / "durable-state.md": render_durable_state_md(durable),
        SAN_ROOT / "state" / "authority-map.md": render_authority_map_md(control),
        SAN_ROOT / "state" / "export-boundary.md": render_export_boundary_md(artifacts),
        SAN_ROOT / "state" / "recurring-failures.md": render_recurring_failures_md(durable),
        SAN_ROOT / "topology" / "node-index.md": render_topology_index_md(graph),
        REPO_ROOT / "README.md": render_readme(control, durable, runtime_manifest, scorecard),
        REPO_ROOT / "AGENT_GUIDE.md": render_agent_guide(control, durable, runtime_manifest),
        REPO_ROOT / "STATUS.md": render_status_md(durable, scorecard),
        REPO_ROOT / "DECISIONS.md": render_decisions_md(durable),
        REPO_ROOT / "task_rubric.md": render_task_rubric_md(control, durable),
    }
