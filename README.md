# C_fit_AI Dual-Node Colombo Workspace

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

- active focus: Install a canonical SAN control plane around both existing product lines.
- SAN score: 3.85/5
- SAN summary: SAN maturity averages 3.85/5 across the current minimum scorecard.

## Not Built Yet

- a remote forge / PR workflow beyond local git
- pilot-calibrated simulator willingness-to-pay curves
- a production Jobs Pulse backend or multi-user deployment layer
- automated export gating for outward-safe sharing

## Verification

```bash
uv run python scripts/san_verify.py
uv run pytest -q
npm --prefix apps/web test
```

## Cold Start

- AGENTS.md
- san/control-plane.md
- san/state/durable-state.md
- san/preflight.md
- san/topology/node-index.md
- san/sanlock.md
