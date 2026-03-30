# Agent Guide

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

- uv run pytest -q
- npm --prefix apps/web test
- npm --prefix apps/web run typecheck
- uv run python scripts/san_sync.py --check
- uv run python scripts/san_preflight.py
- uv run python scripts/san_topology.py
- uv run python scripts/sanlock.py
- uv run python scripts/san_verify.py

## Current Resume Notes

- Read AGENTS.md, then san/control-plane.md, then san/state/durable-state.md.
- Use san/runtime_manifest.json to choose commands instead of guessing.
- Refresh topology and sanlock before broad structural changes.
- Do not hand-edit generated mirrors when san_sync owns them.

## What Not To Break

- Do not collapse the simulator and Jobs Pulse into one blended product truth.
- Do not treat prompt-era docs as canonical authority.
- Do not hand-edit generated mirrors that `san_sync.py` owns.
- Do not bypass topology or SANLOCK refresh after structural changes.
