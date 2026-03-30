# Scoring Framework

## Canonical Dimensions

Every dimension is scored from 0 to 100 on a higher-is-better scale. Friction and barrier concepts are reverse-coded before storage so the scorecard remains directionally consistent.

| Dimension | Meaning |
| --- | --- |
| pain_frequency | How often the underlying problem appears in the target segment |
| problem_severity | How costly or harmful the problem is when it appears |
| willingness_to_pay | Likelihood the target segment will allocate money to solve it |
| price_fit | How well the offer's pricing posture fits local budget reality |
| trust_barrier | Residual trust friction after reverse-coding |
| language_friction | Residual language fit after reverse-coding |
| smartphone_fit | Compatibility with mobile-first usage patterns |
| payment_friction | Residual payment friction after reverse-coding |
| workflow_fit | Compatibility with the target workflow and process reality |
| repeat_usage_potential | Likelihood of recurring usage rather than one-off usage |
| switching_cost | Advantage created by existing switching dynamics after reverse-coding |
| SME_purchase_plausibility | Probability an SME can realistically buy and deploy it |
| enterprise_purchase_plausibility | Probability a larger enterprise can realistically buy and deploy it |
| sales_cycle_friction | Residual sales-cycle friction after reverse-coding |
| channel_feasibility | Realistic route-to-market fit in Sri Lanka |
| pilotability | Ease of running a low-risk initial pilot |
| regulatory_compliance_friction | Residual regulatory or compliance friction after reverse-coding |
| support_burden | Residual support burden after reverse-coding |
| explainability | Ease of explaining the offer's value and outputs locally |
| localization_effort | Residual localization effort after reverse-coding |

## Derived Scores

- `raw_score`
  - arithmetic mean of available dimension scores
- `weighted_score`
  - weighted mean using the default weights in `scoring/engine.py`
- `confidence_score`
  - current proxy for dimension coverage and model completeness
- `evidence_score`
  - current proxy for evidence specificity and provenance coverage
- `simulation_score`
  - scenario-run uplift or penalty, reserved for later Mesa-based execution
- `final_rank_score`
  - current ranking composite:

```text
final_rank_score =
  0.50 * weighted_score
  + 0.15 * raw_score
  + 0.15 * confidence_score
  + 0.10 * evidence_score
  + 0.10 * simulation_score
  - blocker_penalty
```

## Weighting Notes

- `FACT`: Prompt #01 ships a transparent default weighting table in code.
- `INFERENCE`: those weights are provisional and designed for explainability, not validation.
- `TBD`: real calibration from pilots or expert elicitation.

## Blockers

- Blockers are explicit non-score flags such as:
  - unsupported language requirement
  - impossible payment route
  - regulatory mismatch
  - unacceptably high localization burden
- Blockers apply a bounded penalty instead of hiding the issue inside a dimension score.

## Decision Rules

- Use deterministic scorecards to rank all offers first.
- Promote top-ranked offers to simulation only after passing provenance and blocker checks.
- Never interpret a high `final_rank_score` as proof of adoption; it is a prioritization signal for deeper testing.
