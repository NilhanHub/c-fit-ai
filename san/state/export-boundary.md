# Export Boundary

## Artifact Classes

| Class | Default Exposure | Description |
| --- | --- | --- |
| doctrine | internal_authoritative | Instruction and governance surfaces that define how agents should operate in this repo. |
| durable_state | internal_authoritative | Repo-local memory used for resuming work across stateless sessions. |
| runtime_manifest | internal_authoritative | Canonical execution and verification entrypoints. |
| topology_truth | internal_authoritative | Machine-readable bounded-node graph and node-budget data. |
| verification_evidence | internal_private | Proof artifacts, scorecards, preflight checks, and runtime verification outputs. |
| product_truth | internal_shareable | Product-facing source truth for either the simulator or Jobs Pulse node. |
| outward_narrative | shareable_after_review | Human-readable mirrors or summaries that explain current repo state. |
| historical_prompt_artifact | internal_private | Prompt-era artifacts retained for auditability and historical context. |

## Boundary Rules

- outward sharing active: `False`
- private by default: doctrine, durable_state, runtime_manifest, topology_truth, verification_evidence, historical_prompt_artifact
- review required: outward_narrative, product_truth

## Notes

- Outward sharing is currently inactive.
- Prompt-era evidence and internal doctrine are not automatically outward-safe.
