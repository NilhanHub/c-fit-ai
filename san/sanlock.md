# SANLOCK

## Scorecard

| Category | Score | Evidence |
| --- | --- | --- |
| control_plane_authority | 4 | AGENTS.md plus canonical SAN manifests exist. |
| versioned_change_stewardship | 2 | Local git exists and a baseline commit is required for full strength. |
| durable_state_freshness | 4 | Durable state last updated 2026-03-30. |
| resume_handoff_quality | 4 | Resume instructions, decisions, and baseline policy are present. |
| verification_integrity | 4 | Runtime manifest and SAN verification scripts are defined. |
| command_determinism | 4 | san_sync, san_preflight, san_topology, sanlock, and san_verify provide rerunnable mutation and audit paths. |
| reviewability_safety_hygiene | 4 | Git ignore policy and bounded-node control plane are present. |
| topology_graph_freshness | 4 | Topology graph exists and records bounded nodes. |
| node_budget_health | 3 | Node budgets are now measurable, with hotspot and split-candidate flags. |
| declared_observed_topology_drift | 5 | Current declared and observed dependencies are aligned. |
| dispersion_readiness | 4 | All declared nodes expose ownership roots, verification entrypoints, and dispersion-readiness fields. |
| artifact_class_hygiene | 4 | Artifact classes and export boundary rules are explicit. |
| outward_boundary_health | 4 | Outward sharing is inactive and private-by-default classes are declared. |

## Summary

- SAN maturity averages 3.85/5 across the current minimum scorecard.

## Hotspots

- san.repo_os (16.12%)
- sim.market_core (14.47%)
- sim.research_evidence (14.42%)
- jobs.web_app (15.03%)
- jobs.product_doctrine (11.09%)
- jobs.design_ux (11.63%)
- shared.tests_and_scripts (17.24%)

## Overweight Nodes

- san.repo_os (16.12%)
- sim.market_core (14.47%)
- sim.research_evidence (14.42%)
- jobs.web_app (15.03%)
- jobs.product_doctrine (11.09%)
- jobs.design_ux (11.63%)
- shared.tests_and_scripts (17.24%)

## Drift Findings

- none

## Over-Constraint Findings

- none

## Under-Specification Findings

- Remote-forge policy remains unset.
- Baseline commit is still pending until git history exists.

## Recommended Actions

- Keep prompt-era artifacts historical and out of the control plane.
- Refresh topology and SANLOCK after structural changes.
- Maintain repo mirrors through san_sync instead of manual edits.
