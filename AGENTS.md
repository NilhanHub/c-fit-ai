# C_fit_AI SAN Doctrine

This repository operates as a dual-node Stateless-Agent-Native workspace.

## Canonical Order

1. `AGENTS.md` is the canonical doctrine entrypoint.
2. `san/control_plane.json` is the write-authoritative control-plane manifest.
3. `san/durable_state.json` is the write-authoritative durable-state manifest.
4. `san/runtime_manifest.json` is the canonical runtime and verification manifest.
5. `san/topology/topology.graph.json` is the canonical bounded-node graph.
6. Human-readable mirrors are generated from canonical SAN manifests and must not become competing truth surfaces.

## Repo Shape

- `sim.market_core` + `sim.research_evidence`: the Colombo / urban Sri Lanka AI market simulator.
- `jobs.web_app` + `jobs.product_doctrine` + `jobs.design_ux`: the Colombo Jobs Pulse product slice.
- `san.repo_os`: the repo operating system layer that governs both.

Neither product line may silently overwrite the other. Treat them as separate bounded nodes under one control plane.

## Cold Start

1. Read `san/control-plane.md`.
2. Read `san/state/durable-state.md`.
3. Read `san/preflight.md`.
4. Read `san/topology/node-index.md`.
5. Read `san/sanlock.md`.
6. Use `san/runtime_manifest.json` for execution and verification entrypoints.

## Mutation Rules

- Canonical SAN manifests are the only write-authoritative repo-OS surfaces.
- Update mirrors through `uv run python scripts/san_sync.py`, not by manual drift.
- Refresh topology through `uv run python scripts/san_topology.py`.
- Refresh the SAN scorecard through `uv run python scripts/sanlock.py`.
- Refresh the SAN preflight report through `uv run python scripts/san_preflight.py`.
- Use `uv run python scripts/san_verify.py` for full repo verification.

## Safety Rules

- Preserve both product lines.
- Keep prompt-era artifacts as historical evidence, not operational truth.
- No hidden weights, no hidden randomization, no silent authority drift.
- Prefer deterministic mutation paths when a change spans coupled surfaces.
