# Experiment Plan

## Objective

Design an experiment matrix that can eventually test roughly 1000 offers without collapsing into one noisy score run.

## Batch Strategy

- Pilot batch:
  - 100 India-origin offers
- Scale batch:
  - up to 1000 offers after the schema, scoring, and review loop prove stable

## Experiment Stages

1. Deterministic scoring on the full batch.
2. Scenario runs on the top tranche.
3. Sensitivity analysis and finalist stress tests on the leading offers.

## Simulation Runs

- For the 100-offer pilot:
  - top 25 advance to scenario simulation
  - top 10 advance to finalist stress testing
- For the 1000-offer target:
  - top 250 advance to scenario simulation
  - top 50 advance to finalist stress testing

## Scenario Variations

- baseline
- low-trust market
- low-budget market
- high-localization requirement
- payment-friction market
- high-support-burden market

## Sensitivity Analysis

- vary weighting assumptions
- vary confidence penalties
- vary blocker penalties
- vary segment assumptions between B2C and B2B

## Confidence Thresholds

- do not promote offers with thin evidence into top-tier recommendations
- treat low confidence as a visible ranking constraint, not a hidden narrative caveat

## Winner-Selection Rules

- must rank well across more than one plausible scenario
- must not depend on a single fragile assumption
- must have clear pilotability
- must survive a manual review of evidence quality

## Reporting

- produce scenario-by-scenario leaderboards
- show the dimension decomposition for finalists
- show blocker flags and evidence quality beside rank
