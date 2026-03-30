# Authority Map

| Path | Authority | Artifact Class | Notes |
| --- | --- | --- | --- |
| AGENTS.md | canonical | doctrine | Root doctrine entrypoint. |
| san/control_plane.json | canonical | doctrine | Write-authoritative control-plane source truth. |
| san/durable_state.json | canonical | durable_state | Write-authoritative durable-state source truth. |
| san/runtime_manifest.json | canonical | runtime_manifest | Execution and verification truth. |
| san/artifact_classes.json | canonical | doctrine | Artifact exposure and class policy. |
| san/topology/topology.graph.json | canonical | topology_truth | Machine-readable node graph. |
| san/sanlock_scorecard.json | canonical | verification_evidence | Current SAN scorecard. |
| san/references/** | local_overlay | doctrine | Vendored SAN reference pack for cold-start bootability. |
| san/references/import_manifest.json | generated | verification_evidence | Reference import provenance and hashes. |
| san/control-plane.md | mirrored | outward_narrative | Human mirror of the control plane. |
| san/state/durable-state.md | mirrored | outward_narrative | Human mirror of durable state. |
| san/state/authority-map.md | mirrored | outward_narrative | Surface classification mirror. |
| san/state/export-boundary.md | mirrored | outward_narrative | Artifact exposure mirror. |
| san/state/recurring-failures.md | mirrored | outward_narrative | Recurring-failure memory mirror. |
| san/topology/node-index.md | generated | outward_narrative | Human-readable topology view. |
| san/preflight.md | generated | verification_evidence | Latest SAN preflight findings. |
| san/sanlock.md | generated | verification_evidence | Latest SANLOCK findings. |
| README.md | generated | outward_narrative | Repo overview mirror. |
| AGENT_GUIDE.md | generated | outward_narrative | Cold-start operating guide mirror. |
| STATUS.md | generated | outward_narrative | Current status mirror. |
| DECISIONS.md | generated | outward_narrative | Decision log mirror. |
| task_rubric.md | generated | outward_narrative | Task rubric mirror. |
| PROMPT02_* | historical | historical_prompt_artifact | Historical prompt-era artifacts. |
| PROMPT03_* | historical | historical_prompt_artifact | Historical prompt-era artifacts. |
| PROMPT05_* | historical | historical_prompt_artifact | Historical prompt-era artifacts. |
| HANDOFF/** | historical | historical_prompt_artifact | Historical handoff surfaces retained for evidence. |
| evidence/prompt*.json | historical | historical_prompt_artifact | Prompt-era evidence manifests remain retained, not canonical. |
