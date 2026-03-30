# Prompt #02 Continuity Audit

## Scope

This audit compares the Prompt #01 foundation to the Prompt #02 overnight mission: build a real v0 Colombo B2C+B2B decision model rather than a documentation-first scaffold.

## Repo Continuity Check

- `FACT`: the Prompt #01 root docs, contracts, provenance utilities, scaffold interfaces, tests, and evidence packaging flow exist in `D:\AI\C_fit_AI`.
- `FACT`: Prompt #01 explicitly deferred the core modeling work: synthetic population generation, synthetic firm generation, live offer corpus ingestion, calibrated scoring weights, and any meaningful simulation runtime.
- `FACT`: the evidence path rule still points to `D:\AI-Apps-In-Drive\App_Station\Score_Leads\Evidence\PROMPT#02.zip`.
- `FACT`: the contract family for population, household, firm, buying center, offer, scorecard, and experiment still aligns with the Prompt #02 mission.
- `FACT`: the app/repo naming remains consistent with `Score_Leads`.

## What Already Exists From Prompt #01

### Solid

- root project docs and operating guide
- baseline contracts in `contracts/`
- provenance enforcement in `validation/provenance.py`
- explainable score aggregation in `scoring/engine.py`
- experiment staging in `experiments/runner.py`
- evidence catalog and packaging for Prompt #01
- baseline tests for contracts and interfaces

### Partial

- `population/synthesis.py` and `firms/synthesis.py` are planning interfaces only
- `offers/normalize.py` normalizes a single record but does not load a real corpus
- Prompt #01 docs define methods and principles but do not generate a runnable market
- source registry exists, but Prompt #02 needs broader source hierarchy and reliability treatment

### Missing For Prompt #02

- B2C seed-table ingestion and household/person synthesis
- B2C segment taxonomy and summary outputs
- B2B firm archetypes, buying-center synthesis, and summary outputs
- normalized India-first offer corpus
- B2C-specific scoring logic
- B2B-specific scoring logic
- scenario definitions and multi-scenario portfolio ranking
- validation routines for reproducibility and sensitivity
- Prompt #02 reports, handoff pack, and evidence zip

## Gap Map: Prompt #01 -> Prompt #02

| Area | Prompt #01 State | Prompt #02 Requirement | Gap Severity |
| --- | --- | --- | --- |
| Source system | baseline source catalog | ranked source hierarchy + gaps + reliability | high |
| B2C model | plan only | runnable synthetic sample + segment summary | critical |
| B2B model | plan only | runnable firm sample + buying centers + summary | critical |
| Offer corpus | no live corpus | curated India-first normalized offers | critical |
| Scoring | generic score combiner | B2C and B2B explainable dimension engines | critical |
| Ranking | experiment staging only | scenario portfolio outputs and top-offer tables | critical |
| Validation | baseline tests only | reproducibility, sensitivity, sanity checks | high |
| Evidence | Prompt #01 manifest only | Prompt #02 manifest, hash log, run log, archive | high |

## Contract Alignment Check

- `FACT`: existing contracts are still directionally correct for Prompt #02.
- `INFERENCE`: Prompt #02 can ship tonight without fully expanding every contract field if generated outputs preserve provenance and remain structurally mappable into the canonical schemas.
- `TBD`: richer contract enforcement for segment summaries, richer offer metadata, and uncertainty artifacts may need contract upgrades in Prompt #03.

## Main Build Implication

Prompt #02 should keep the Prompt #01 architecture intact and fill in the first working data -> synthesis -> scoring -> ranking path, rather than replacing the foundation with a second unrelated stack.
