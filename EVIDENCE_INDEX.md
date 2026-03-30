# Evidence Index

## Prompt #03 Core Evidence

| Artifact | Path | Purpose |
| --- | --- | --- |
| Prompt #03 manifest | `evidence/prompt03_manifest.json` | machine-readable summary of Prompt #03 outputs |
| Source catalog | `evidence/source_catalog.json` | merged source registry with Prompt #03 snapshots |
| Hash log | `evidence/hash_log.csv` | phase and artifact hash log |
| Run log | `evidence/run_log.md` | Prompt #03 pipeline record |
| Phase evidence | `evidence/phases/PHASE_###/` | phase-by-phase notes, sources, assumptions, and hashes |
| Packaging script | `scripts/package_prompt03_evidence.py` | reproducible creation of `PROMPT#03.zip` |

## Prompt #03 Major Artifacts

| Artifact | Path | Notes |
| --- | --- | --- |
| Continuity audit | `PROMPT03_CONTINUITY_AUDIT.md` | exact Prompt #02 -> Prompt #03 gap and contamination map |
| Commercial target state | `COMMERCIAL_TARGET_STATE.md` | hard gates for commercial usefulness |
| Master plan | `PROMPT03_MASTER_PLAN.md` | sprint plan for source, model, scoring, and handoff work |
| Phase tracker | `PROMPT03_PHASE_TRACKER.md` | 100-phase tracker |
| B2C v2 report | `reports/b2c_model_v2_report.md` | consumer commercial-demand model summary |
| B2B v2 report | `reports/b2b_model_v2_report.md` | firm commercial-demand model summary |
| Offer ontology report | `reports/offer_ontology_v2.md` | v2 offer schema rationale |
| Offer corpus report | `reports/offer_corpus_v2_report.md` | candidate + substitute + benchmark composition |
| Scoring v2 report | `reports/scoring_v2_report.md` | fit and commercial-attractiveness logic |
| Model card | `reports/model_card_v1.md` | scope, evidence, and limits |
| Validation report | `reports/validation_report.md` | reproducibility and sensitivity summary |
| Top opportunities | `outputs/top_opportunities.csv` | mixed-market base short-list |
| Scenario comparison | `outputs/scenario_comparison.csv` | rank movement across scenarios |
| Explainers | `outputs/opportunity_explainers.json` | machine-readable why-this-ranked output |
| Competitor graph | `outputs/offer_competitor_graph.json` | substitute and overlap graph |
| Domain clusters | `outputs/offer_domain_clusters.json` | offer-domain grouping output |
| Executive brief | `HANDOFF/PROMPT03_EXECUTIVE_BRIEF.md` | operator-facing morning brief |

## Claim Register

- `FACT`: source snapshots, repo artifacts, generated outputs, and verification results.
- `INFERENCE`: zone clustering, archetype shares, price bands, trust elasticities, and most commercial weights.
- `TBD`: calibrated willingness to pay, real pilot adoption curves, retention curves, and predictive validity.
