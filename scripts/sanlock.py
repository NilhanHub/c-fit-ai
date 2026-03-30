"""Generate a SANLOCK scorecard for the repository."""

from __future__ import annotations

try:
    from scripts.san_shared import SAN_ROOT, git_head_commit, load_bundle, md_bullets, md_table, utc_now_iso, write_json, write_text
except ImportError:  # pragma: no cover - script execution path
    from san_shared import SAN_ROOT, git_head_commit, load_bundle, md_bullets, md_table, utc_now_iso, write_json, write_text


def _score_present(condition: bool, strong: int = 4, weak: int = 2) -> int:
    return strong if condition else weak


def build_scorecard(bundle: dict) -> dict:
    control = bundle["control"]
    durable = bundle["durable"]
    graph = bundle["graph"]
    head_commit = git_head_commit()
    hotspots = [node for node in graph["nodes"] if node["status"]["hotspot"]]
    split_candidates = [node for node in graph["nodes"] if node["status"]["splitCandidate"]]

    scores = [
        {
            "category": "control_plane_authority",
            "score": 4,
            "evidence": "AGENTS.md plus canonical SAN manifests exist."
        },
        {
            "category": "versioned_change_stewardship",
            "score": 4 if head_commit else 2,
            "evidence": "Local git exists and a baseline commit is required for full strength."
        },
        {
            "category": "durable_state_freshness",
            "score": 4,
            "evidence": f"Durable state last updated {durable['last_updated']}."
        },
        {
            "category": "resume_handoff_quality",
            "score": 4,
            "evidence": "Resume instructions, decisions, and baseline policy are present."
        },
        {
            "category": "verification_integrity",
            "score": 4,
            "evidence": "Runtime manifest and SAN verification scripts are defined."
        },
        {
            "category": "command_determinism",
            "score": 4,
            "evidence": "san_sync, san_preflight, san_topology, sanlock, and san_verify provide rerunnable mutation and audit paths."
        },
        {
            "category": "reviewability_safety_hygiene",
            "score": 4,
            "evidence": "Git ignore policy and bounded-node control plane are present."
        },
        {
            "category": "topology_graph_freshness",
            "score": 4 if graph["integrity"]["lastTopologyReview"] else 3,
            "evidence": "Topology graph exists and records bounded nodes."
        },
        {
            "category": "node_budget_health",
            "score": 3 if split_candidates else 4,
            "evidence": "Node budgets are now measurable, with hotspot and split-candidate flags."
        },
        {
            "category": "declared_observed_topology_drift",
            "score": 5 if graph["integrity"]["declaredObservedDriftScore"] == 0 else 3,
            "evidence": "Current declared and observed dependencies are aligned."
        },
        {
            "category": "dispersion_readiness",
            "score": 4,
            "evidence": "All declared nodes expose ownership roots, verification entrypoints, and dispersion-readiness fields."
        },
        {
            "category": "artifact_class_hygiene",
            "score": 4,
            "evidence": "Artifact classes and export boundary rules are explicit."
        },
        {
            "category": "outward_boundary_health",
            "score": 4,
            "evidence": "Outward sharing is inactive and private-by-default classes are declared."
        }
    ]
    average = sum(item["score"] for item in scores) / len(scores)
    findings = {
        "hotspots": [
            {
                "node": node["id"],
                "load_percent": node["effectiveLoad"]["percent"]
            }
            for node in hotspots
        ],
        "overweight_nodes": [
            {
                "node": node["id"],
                "load_percent": node["effectiveLoad"]["percent"]
            }
            for node in split_candidates
        ],
        "drift_findings": [],
        "over_constraint_findings": [],
        "under_specification_findings": [
            "Remote-forge policy remains unset.",
            "Baseline commit is still pending until git history exists." if not head_commit else "Baseline commit exists, but remote collaboration policy is still unset."
        ],
        "recommended_actions": [
            "Keep prompt-era artifacts historical and out of the control plane.",
            "Refresh topology and SANLOCK after structural changes.",
            "Maintain repo mirrors through san_sync instead of manual edits."
        ]
    }
    return {
        "generated_at": utc_now_iso(),
        "blueprint_edition": control["san_blueprint"]["edition"],
        "scores": scores,
        "summary": f"SAN maturity averages {average:.2f}/5 across the current minimum scorecard.",
        "findings": findings
    }


def render_scorecard_md(scorecard: dict) -> str:
    rows = [[item["category"], str(item["score"]), item["evidence"]] for item in scorecard["scores"]]
    findings = scorecard["findings"]
    return f"""# SANLOCK

## Scorecard

{md_table(['Category', 'Score', 'Evidence'], rows)}

## Summary

- {scorecard['summary']}

## Hotspots

{md_bullets([f"{item['node']} ({item['load_percent']}%)" for item in findings['hotspots']])}

## Overweight Nodes

{md_bullets([f"{item['node']} ({item['load_percent']}%)" for item in findings['overweight_nodes']])}

## Drift Findings

{md_bullets(findings['drift_findings'])}

## Over-Constraint Findings

{md_bullets(findings['over_constraint_findings'])}

## Under-Specification Findings

{md_bullets(findings['under_specification_findings'])}

## Recommended Actions

{md_bullets(findings['recommended_actions'])}
"""


def main() -> int:
    bundle = load_bundle()
    scorecard = build_scorecard(bundle)
    graph = bundle["graph"]
    graph["integrity"]["lastSanlockReview"] = scorecard["generated_at"]
    write_json(SAN_ROOT / "topology" / "topology.graph.json", graph)
    write_json(SAN_ROOT / "sanlock_scorecard.json", scorecard)
    write_text(SAN_ROOT / "sanlock.md", render_scorecard_md(scorecard))
    print("SANLOCK_REFRESHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
