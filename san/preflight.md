# SAN Preflight

## Canonical Surfaces

- doctrine: `AGENTS.md`
- control plane: `san/control_plane.json`
- durable state: `san/durable_state.json`

## Active Modes

- MID_BUILD_ALIGNMENT
- LEGACY_RETROFIT
- MAINTENANCE

## Versioned Change Surface

| Item | Value |
| --- | --- |
| vcs | git |
| head commit | 8c8da1db3d5319ea2566a147af727c06e74313e5 |
| dirty paths | 10 |
| drift score | 0.0 |

## Execution Entrypoints

- uv run python scripts/run_prompt03_pipeline.py
- npm --prefix apps/web dev
- npm --prefix apps/web build
- uv run python scripts/san_sync.py
- uv run python scripts/san_preflight.py
- uv run python scripts/san_topology.py
- uv run python scripts/sanlock.py

## Verification Entrypoints

- uv run pytest -q
- npm --prefix apps/web test
- npm --prefix apps/web run typecheck
- uv run python scripts/san_sync.py --check
- uv run python scripts/san_preflight.py
- uv run python scripts/san_topology.py
- uv run python scripts/sanlock.py
- uv run python scripts/san_verify.py

## Node Topology

- nodes: san.repo_os, sim.market_core, sim.research_evidence, jobs.web_app, jobs.product_doctrine, jobs.design_ux, shared.tests_and_scripts
- hotspots: san.repo_os, sim.market_core, sim.research_evidence, jobs.web_app, jobs.product_doctrine, jobs.design_ux, shared.tests_and_scripts
- split candidates: san.repo_os, sim.market_core, sim.research_evidence, jobs.web_app, jobs.product_doctrine, jobs.design_ux, shared.tests_and_scripts

## SAN Drift

- Prompt-era artifacts remain numerous and require historical classification.
- Local git exists but remote-forge policy is still unspecified.

## Over-Constraint

- none

## Under-Specification

- Remote-forge and PR workflow are not yet codified.
- Baseline SAN checkpoint remains pending until git commit exists.

## Current SAN Score Summary

- SAN maturity averages 4.00/5 across the current minimum scorecard.
