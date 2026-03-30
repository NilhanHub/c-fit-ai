# Decisions

## 2026-03-30

- `INFERENCE`: Preserve a dual-node repo shape instead of choosing a single canonical product line.
- why: Both the simulator and Jobs Pulse contain real working code, tests, and artifacts.

## 2026-03-30

- `FACT`: Canonical repo-OS truth now lives in SAN JSON manifests, not prompt-era docs.
- why: The blueprint requires singular control-plane authority.

## 2026-03-30

- `INFERENCE`: Generated repo mirrors are acceptable as long as they remain subordinate to the canonical SAN manifests.
- why: Equivalent manifestations are allowed when authority stays singular.

## 2026-03-30

- `FACT`: The canonical web test command is `npm --prefix apps/web test`, not a Jest-style `--runInBand` variant.
- why: The repo uses Vitest, and live verification showed the Jest flag is invalid in this web node.
