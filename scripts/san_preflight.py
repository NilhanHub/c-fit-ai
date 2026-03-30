"""Refresh the SAN preflight report."""

from __future__ import annotations

try:
    from scripts.san_shared import SAN_ROOT, git_head_commit, git_status_short, load_bundle, md_bullets, md_table, utc_now_iso, write_json, write_text
except ImportError:  # pragma: no cover - script execution path
    from san_shared import SAN_ROOT, git_head_commit, git_status_short, load_bundle, md_bullets, md_table, utc_now_iso, write_json, write_text


def build_report(bundle: dict) -> dict:
    control = bundle["control"]
    runtime_manifest = bundle["runtime"]
    graph = bundle["graph"]
    scorecard = bundle["scorecard"]
    head_commit = git_head_commit()
    dirty_lines = git_status_short()
    hotspots = [node["id"] for node in graph["nodes"] if node["status"]["hotspot"]]
    split_candidates = [node["id"] for node in graph["nodes"] if node["status"]["splitCandidate"]]
    return {
        "generated_at": utc_now_iso(),
        "active_modes": control["active_modes"],
        "canonical_doctrine_surface": "AGENTS.md",
        "canonical_control_plane_surface": "san/control_plane.json",
        "canonical_durable_state_surface": "san/durable_state.json",
        "competing_authority_surfaces": [],
        "versioned_change_surface": {
            "vcs": "git",
            "head_ref": "HEAD" if head_commit else None,
            "history_present": bool(head_commit),
            "dirty_paths": dirty_lines
        },
        "execution_entrypoints": runtime_manifest["execution_entrypoints"],
        "verification_entrypoints": runtime_manifest["verification_entrypoints"],
        "packaged_capabilities": [
            "scripts/san_sync.py",
            "scripts/san_preflight.py",
            "scripts/san_topology.py",
            "scripts/sanlock.py",
            "scripts/san_verify.py",
            "scripts/run_prompt03_pipeline.py"
        ],
        "conditional_doctrines": control["conditional_doctrines"],
        "topology_graph_exists": True,
        "node_ids": [node["id"] for node in graph["nodes"]],
        "hotspots": hotspots,
        "split_candidates": split_candidates,
        "declared_observed_drift_score": graph["integrity"]["declaredObservedDriftScore"],
        "signs_of_san_drift": [
            "Prompt-era artifacts remain numerous and require historical classification.",
            "Local git exists but remote-forge policy is still unspecified."
        ],
        "signs_of_over_constraint": [],
        "signs_of_under_specification": [
            "Remote-forge and PR workflow are not yet codified.",
            (
                "Baseline SAN checkpoint remains pending until git commit exists."
                if not head_commit
                else "Remote collaboration policy is still unset beyond local git."
            )
        ],
        "current_san_score_summary": scorecard["summary"] if scorecard else "Pending first SANLOCK run."
    }


def render_report_md(report: dict) -> str:
    change_rows = [
        ["vcs", report["versioned_change_surface"]["vcs"]],
        ["head ref", str(report["versioned_change_surface"]["head_ref"])],
        ["history present", str(report["versioned_change_surface"]["history_present"])],
        ["dirty paths", str(len(report["versioned_change_surface"]["dirty_paths"]))],
        ["drift score", str(report["declared_observed_drift_score"])],
    ]
    return f"""# SAN Preflight

## Canonical Surfaces

- doctrine: `{report['canonical_doctrine_surface']}`
- control plane: `{report['canonical_control_plane_surface']}`
- durable state: `{report['canonical_durable_state_surface']}`

## Active Modes

{md_bullets(report['active_modes'])}

## Versioned Change Surface

{md_table(['Item', 'Value'], change_rows)}

## Execution Entrypoints

{md_bullets(report['execution_entrypoints']['simulator'] + report['execution_entrypoints']['jobs_web'] + report['execution_entrypoints']['san'])}

## Verification Entrypoints

{md_bullets(report['verification_entrypoints']['python'] + report['verification_entrypoints']['web'] + report['verification_entrypoints']['san'])}

## Node Topology

- nodes: {", ".join(report['node_ids'])}
- hotspots: {", ".join(report['hotspots']) if report['hotspots'] else 'none'}
- split candidates: {", ".join(report['split_candidates']) if report['split_candidates'] else 'none'}

## SAN Drift

{md_bullets(report['signs_of_san_drift'])}

## Over-Constraint

{md_bullets(report['signs_of_over_constraint'])}

## Under-Specification

{md_bullets(report['signs_of_under_specification'])}

## Current SAN Score Summary

- {report['current_san_score_summary']}
"""


def main() -> int:
    bundle = load_bundle()
    report = build_report(bundle)
    write_json(SAN_ROOT / "preflight_report.json", report)
    write_text(SAN_ROOT / "preflight.md", render_report_md(report))
    print("SAN_PREFLIGHT_REFRESHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
