# Research Methodology

## Operating Principle

- `FACT`: official Sri Lankan sources come first for population, household, digital access, labor, and establishment anchors.
- `INFERENCE`: foreign-offer evidence should come from official vendor pages or named case studies before any directory or aggregator source.

## Desk Research Layer

- Collect high-level structure first:
  - Colombo and urban Sri Lanka population framing
  - household income and expenditure patterns
  - computer and internet access patterns
  - non-agricultural firm and informal-sector structure
  - payment and operational context for AI adoption
- Record every source in `evidence/source_catalog.json`.

## Official-Data Layer

- Priority sources for Prompt #01:
  - Department of Census and Statistics population outputs and census pages
  - HIES 2019 public-use study metadata and documentation
  - Computer Literacy Statistics bulletin
  - informal non-agricultural activity and related establishment reports
  - household economic-crisis survey results
- Use public data for:
  - marginals and anchors
  - segmentation variables
  - realism checks

## Synthetic Population Methodology

- `INFERENCE`: use a hierarchical seeded-IPF approach:
  1. define Colombo household marginals
  2. allocate household archetypes
  3. populate individuals within household constraints
  4. check marginal fit and household consistency
- Required seed inputs:
  - district population anchors
  - household-size distribution
  - age or life-stage proxies
  - income and expenditure bands
  - digital-access proxies
- Calibration status in Prompt #01: seeded, not validated.

## Synthetic Firm / Establishment Methodology

- `INFERENCE`: create firms by sector and size-band strata, then attach buying-center templates by formality and digital maturity.
- Required seed inputs:
  - non-agricultural activity counts or distributions
  - sector mix
  - micro/small/medium proportions
  - formal versus informal behavior proxies
- Prompt #01 output: planning contracts and firm archetype structure, not a production-grade generator.

## Offer Discovery Methodology

- Start with India.
- Target small and mid-sized IT firms with concrete AI offers.
- Reject:
  - generic “AI transformation” messaging
  - pages with no named use case
  - pages without delivery mode, pricing posture, or proof artifact
- Capture:
  - source URL
  - retrieval date
  - offer category
  - public proof points

## Offer Normalization Methodology

- Normalize every candidate into `offer.schema.yaml`.
- Require provenance on every normalized record.
- Preserve both the structured interpretation and the original evidence reference.

## Scoring Methodology

- Score offers separately against B2C and B2B segments.
- Use decomposed dimensions, not one opaque fit score.
- Combine:
  - market pain and severity
  - willingness and ability to pay
  - digital and language reality
  - purchase and channel feasibility
  - support, compliance, and localization burden

## Validation Methodology

- Compare synthetic outputs to public marginals first.
- Compare score assumptions to later pilot observations when available.
- Keep uncertainty visible through:
  - confidence score
  - evidence score
  - explicit `TBD` markers

## Experiment Methodology

- Stage 1: deterministic scoring for the full batch.
- Stage 2: scenario simulation for the top tranche.
- Stage 3: sensitivity analysis and finalist stress tests.
- Track scenario-driven ranking changes instead of relying on one baseline run.

## Bias, Hallucination, And Overfitting Safeguards

- Keep official sources above blog summaries.
- Separate facts from assumptions in both prose and code.
- Do not infer Sri Lanka demand directly from foreign case studies.
- Do not tune weights to “make sense” without recorded evidence.
- Keep the pilot small enough to inspect manually before scaling to 1000 offers.
