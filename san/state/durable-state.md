# SAN Durable State

## Current Focus

- Install a canonical SAN control plane around both existing product lines.

## Active Now

- Treat the repo as one workspace with two live product nodes.
- Make SAN manifests the only write-authoritative repo-OS surfaces.
- Keep prompt-era artifacts as historical evidence, not shadow authority.
- Establish the first intentional git checkpoint on main.

## Next

- Refresh SAN mirrors from canonical manifests after any repo-OS change.
- Run topology, sanlock, and preflight after major structure changes.
- Keep Python and web verification green before publishing repo-OS changes.

## Blocked

- none

## Decisions

- `INFERENCE` 2026-03-30: Preserve a dual-node repo shape instead of choosing a single canonical product line. Why: Both the simulator and Jobs Pulse contain real working code, tests, and artifacts.
- `FACT` 2026-03-30: Canonical repo-OS truth now lives in SAN JSON manifests, not prompt-era docs. Why: The blueprint requires singular control-plane authority.
- `INFERENCE` 2026-03-30: Generated repo mirrors are acceptable as long as they remain subordinate to the canonical SAN manifests. Why: Equivalent manifestations are allowed when authority stays singular.
- `FACT` 2026-03-30: The canonical web test command is `npm --prefix apps/web test`, not a Jest-style `--runInBand` variant. Why: The repo uses Vitest, and live verification showed the Jest flag is invalid in this web node.
- `FACT` 2026-03-30: Git baseline commit `8c8da1db3d5319ea2566a147af727c06e74313e5` established the first SAN-aligned checkpoint on `main`. Why: Versioned change stewardship is a constitutional SAN requirement, and the repo previously had no commit history.

## Unresolved

- `medium`: Long-term remote forge policy is still unset because the repo has only local git today.
- `low`: Future physical relocation of prompt-era historical artifacts is optional and not required for the initial SAN retrofit.

## Resume

- Read AGENTS.md, then san/control-plane.md, then san/state/durable-state.md.
- Use san/runtime_manifest.json to choose commands instead of guessing.
- Refresh topology and sanlock before broad structural changes.
- Do not hand-edit generated mirrors when san_sync owns them.

## Baseline Checkpoint

- status: `recorded_git_commit`
- policy: The first commit on main containing the SAN control-plane files is the initial SAN-aligned checkpoint.
- recorded commit: `8c8da1db3d5319ea2566a147af727c06e74313e5`
