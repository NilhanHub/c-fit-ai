"""Transparent score aggregation for Colombo market-fit evaluation."""

from __future__ import annotations

from statistics import fmean

from validation.provenance import DEFAULT_RETRIEVED_AT, require_provenance


DEFAULT_DIMENSION_WEIGHTS = {
    "pain_frequency": 1.0,
    "problem_severity": 1.0,
    "willingness_to_pay": 1.0,
    "price_fit": 1.0,
    "trust_barrier": 0.9,
    "language_friction": 0.9,
    "smartphone_fit": 0.8,
    "payment_friction": 0.8,
    "workflow_fit": 1.0,
    "repeat_usage_potential": 0.9,
    "switching_cost": 0.7,
    "sme_purchase_plausibility": 0.9,
    "enterprise_purchase_plausibility": 0.7,
    "sales_cycle_friction": 0.8,
    "channel_feasibility": 0.8,
    "pilotability": 0.8,
    "regulatory_compliance_friction": 0.7,
    "support_burden": 0.7,
    "explainability": 0.8,
    "localization_effort": 0.8,
}


def _resolve_weight(dimension: str, custom_weights: dict[str, float] | None) -> float:
    if custom_weights and dimension in custom_weights:
        return custom_weights[dimension]
    return DEFAULT_DIMENSION_WEIGHTS.get(dimension, 1.0)


def score_offer(
    *,
    offer_id: str,
    market_segment_id: str,
    scenario_id: str,
    dimension_scores: dict[str, float],
    evidence_refs: list[str],
    weights: dict[str, float] | None = None,
    blockers: list[str] | None = None,
    rationales: dict[str, str] | None = None,
    simulation_score: float = 0.0,
    claim_type: str = "INFERENCE",
    retrieved_at: str = DEFAULT_RETRIEVED_AT,
) -> dict:
    if not dimension_scores:
        raise ValueError("dimension_scores must include at least one dimension")

    for name, value in dimension_scores.items():
        if not 0 <= value <= 100:
            raise ValueError(f"Dimension '{name}' must be between 0 and 100")

    resolved_blockers = blockers or []
    raw_score = round(fmean(dimension_scores.values()), 2)
    total_weight = sum(_resolve_weight(dimension, weights) for dimension in dimension_scores)
    weighted_score = round(
        sum(score * _resolve_weight(dimension, weights) for dimension, score in dimension_scores.items()) / total_weight,
        2,
    )
    coverage_ratio = min(1.0, len(dimension_scores) / len(DEFAULT_DIMENSION_WEIGHTS))
    confidence_score = round(40 + (60 * coverage_ratio), 2)
    evidence_score = min(100.0, round(55 + (5 * len(evidence_refs)), 2))
    blocker_penalty = min(25.0, 5.0 * len(resolved_blockers))
    final_rank_score = round(
        (weighted_score * 0.5)
        + (raw_score * 0.15)
        + (confidence_score * 0.15)
        + (evidence_score * 0.1)
        + (simulation_score * 0.1)
        - blocker_penalty,
        2,
    )

    scorecard = {
        "offer_id": offer_id,
        "market_segment_id": market_segment_id,
        "scenario_id": scenario_id,
        "dimension_scores": dimension_scores,
        "raw_score": raw_score,
        "weighted_score": weighted_score,
        "confidence_score": confidence_score,
        "evidence_score": evidence_score,
        "simulation_score": round(simulation_score, 2),
        "final_rank_score": max(final_rank_score, 0.0),
        "blockers": resolved_blockers,
        "rationales": rationales or {},
        "claim_type": claim_type,
        "retrieved_at": retrieved_at,
        "evidence_refs": evidence_refs,
    }
    require_provenance(scorecard)
    return scorecard
