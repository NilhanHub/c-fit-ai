# Market Model Spec

## Mission

- `FACT`: the repo mission is to evaluate which external AI offers are most likely to work in Sri Lanka using explainable, evidence-backed structures rather than opaque model outputs.
- `INFERENCE`: the best Prompt #01 shape is a modular pipeline with strict contracts and staged experimentation.

## Scope

- In scope now:
  - Colombo District as v0 geography
  - synthetic B2C planning at individual and household levels
  - synthetic B2B planning at firm and buying-center levels
  - external-offer normalization for specific public AI offers
  - transparent scoring and experiment staging
- Out of scope now:
  - nation-wide simulation
  - large-scale scraping
  - causal claims of adoption without pilots
  - full Mesa agent logic beyond scaffold-level reservation

## B2C Model Definition

- Unit layers:
  - individual
  - household
- Mandatory individual attributes:
  - demographic attributes
  - economic band
  - digital access pattern
  - behavioral adoption posture
  - geography link to household
- Mandatory household attributes:
  - composition
  - income and expenditure band
  - device context
  - payment readiness
  - geography

## B2B Model Definition

- Unit layers:
  - firm or establishment
  - buying center
- Mandatory firm attributes:
  - sector
  - size band
  - formality
  - digital maturity
  - budget posture
  - adoption friction
- Mandatory buying-center attributes:
  - roles
  - approval path
  - procurement style
  - risk tolerance

## Rollout Plan

- `FACT`: Colombo-first is the minimum viable scope because it is the most urbanized and data-rich launch target in Sri Lanka.
- `INFERENCE`: broader rollout should move from Colombo District to other highly urbanized districts only after contracts and scoring survive the pilot.

## Offer-Ingestion Pipeline Concept

1. Discover concrete public offers country-by-country.
2. Capture source evidence before normalization.
3. Normalize to `offer.schema.yaml`.
4. Score per segment and scenario.
5. Promote top candidates into simulation runs.

## Scoring Dimensions

- The canonical dimensions are defined in `SCORING_FRAMEWORK.md`.
- Every dimension is stored on a 0-100 higher-is-better scale, including friction dimensions after reverse-coding.

## Validation Philosophy

- `FACT`: official Sri Lankan data sources have priority over private summaries.
- `INFERENCE`: synthetic entities should be calibrated against public marginals before any behavioral claims.
- `TBD`: pilot results, conversion rates, and realized willingness to pay remain unknown until field work exists.

## Limitations And Anti-Delusion Rules

- No black-box “model thinks so” outputs.
- No validation claims without out-of-sample or pilot evidence.
- No average composite buyer that erases household and firm differences.
- No hidden priors embedded in code or Markdown prose.
- No promotion of marketing copy to FACT without supporting public proof.

## Backbone Decision

- `FACT`: Mesa remains the preferred simulation backbone because it is a mature Python ABM framework with agent management and data collection support.
- `INFERENCE`: Prompt #01 should keep Mesa behind the scoring and synthesis boundaries so the repo stays modular and testable.
