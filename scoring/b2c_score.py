"""Prompt #02 B2C scoring against synthetic Colombo consumer segments."""

from __future__ import annotations

from scoring.b2c_dimensions import (
    B2C_DIMENSION_WEIGHTS,
    OFFER_TO_B2C_NEED_FIELD,
    budget_requirement_score,
    device_score,
    level_score,
    market_side_score,
    substitute_score,
)
from scoring.engine import score_offer


_LANGUAGE_SCORES = {"en": 55, "si": 70, "ta": 65, "si_en": 80, "ta_en": 78}
_ROI_BONUS = {"learning_outcome": 75, "wellbeing_outcome": 60, "service_speed": 68, "revenue_uplift": 55}


def _clamp(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def _language_fit(segment: dict, offer: dict) -> float:
    top_languages = segment["top_languages"].split("|")
    scores = [_LANGUAGE_SCORES.get(language, 45) for language in top_languages if language in offer["language_support"]]
    if scores:
        return max(scores)
    if "en" in offer["language_support"]:
        return 45
    return 20


def _scenario_adjust(segment: dict, scenario: dict) -> dict:
    adjusted = dict(segment)
    for field, delta in scenario.get("b2c_attribute_deltas", {}).items():
        adjusted[field] = _clamp(adjusted[field] + delta)
    share_multiplier = scenario.get("b2c_share_multipliers", {}).get(segment["segment_id"], 1.0)
    adjusted["population_share"] = round(segment["population_share"] * share_multiplier, 6)
    return adjusted


def score_offer_for_b2c(offer: dict, segments: list[dict], scenario: dict) -> dict:
    if offer["market_side"] == "b2b":
        return {
            "offer_id": offer["offer_id"],
            "scenario_id": scenario["scenario_id"],
            "market": "b2c",
            "aggregate_score": 0.0,
            "scorecards": [],
            "top_segment_id": None,
            "explanation": "B2B-only offer is not scored on the consumer-side market.",
        }

    scorecards: list[dict] = []
    weight_total = 0.0
    weighted_total = 0.0
    segment_weights: dict[str, float] = {}
    need_field = OFFER_TO_B2C_NEED_FIELD.get(offer["problem_domain"], "avg_need_family_admin")

    for segment in segments:
        adjusted = _scenario_adjust(segment, scenario)
        blockers: list[str] = []
        pain_intensity = adjusted[need_field]
        urgency = _clamp((pain_intensity * 0.65) + (_ROI_BONUS.get(offer["expected_roi_path"], 55) * 0.35))
        frequency = _clamp((adjusted["avg_need_family_admin"] * 0.4) + (pain_intensity * 0.6))
        reachable_channel_fit = _clamp((adjusted["avg_channel_reach_score"] * 0.7) + (device_score(offer["required_device_connectivity"]) * 0.3))
        digital_readiness = _clamp(adjusted["avg_digital_readiness"] - max(0, level_score(offer["required_digital_maturity"]) - 50) * 0.4)
        affordability = _clamp(adjusted["avg_budget_score"] - (budget_requirement_score(offer["minimum_budget_band"]) - 35))
        trust_fit = _clamp(adjusted["avg_trust_openness"] - (level_score(offer["trust_barrier"]) - 35) * 0.55)
        language_fit = _language_fit(adjusted, offer)
        behavior_change_burden = _clamp(100 - (level_score(offer["deployment_friction"]) * 0.45) - (level_score(offer["integration_demands"]) * 0.2))
        local_substitute_saturation = substitute_score(offer["local_substitute_pressure"])
        implementation_friction = _clamp(digital_readiness - (level_score(offer["deployment_friction"]) * 0.25))
        retention_potential = _clamp((pain_intensity * 0.55) + (_ROI_BONUS.get(offer["expected_roi_path"], 55) * 0.45))
        expansion_potential = _clamp((market_side_score(offer["market_side"]) * 0.3) + (adjusted["population_share"] * 100 * 0.7))

        if affordability < 30:
            blockers.append("price_mismatch")
        if digital_readiness < 30:
            blockers.append("digital_mismatch")

        dimension_scores = {
            "pain_intensity": pain_intensity,
            "urgency": urgency,
            "frequency_of_problem": frequency,
            "reachable_channel_fit": reachable_channel_fit,
            "digital_readiness": digital_readiness,
            "affordability": affordability,
            "trust_fit": trust_fit,
            "language_fit": language_fit,
            "behavior_change_burden": behavior_change_burden,
            "local_substitute_saturation": local_substitute_saturation,
            "implementation_friction": implementation_friction,
            "retention_potential": retention_potential,
            "expansion_potential": expansion_potential,
        }

        scorecards.append(
            score_offer(
                offer_id=offer["offer_id"],
                market_segment_id=adjusted["segment_id"],
                scenario_id=scenario["scenario_id"],
                dimension_scores=dimension_scores,
                evidence_refs=offer["evidence_refs"] + ["prompt02-b2c-scorer"],
                weights=B2C_DIMENSION_WEIGHTS,
                blockers=blockers,
                rationales={
                    "pain_intensity": f"{offer['problem_domain']} matched against {need_field}",
                    "affordability": f"segment budget {adjusted['avg_budget_score']} vs required {offer['minimum_budget_band']}",
                    "language_fit": f"segment languages {adjusted['top_languages']}",
                },
                simulation_score=adjusted["population_share"] * 100,
            )
        )
        segment_weights[adjusted["segment_id"]] = adjusted["population_share"]

    for scorecard in scorecards:
        segment_share = segment_weights[scorecard["market_segment_id"]]
        weight_total += segment_share
        weighted_total += scorecard["final_rank_score"] * segment_share

    top_segment = max(scorecards, key=lambda item: item["final_rank_score"]) if scorecards else None
    aggregate_score = round(weighted_total / weight_total, 2) if weight_total else 0.0
    return {
        "offer_id": offer["offer_id"],
        "scenario_id": scenario["scenario_id"],
        "market": "b2c",
        "aggregate_score": aggregate_score,
        "scorecards": scorecards,
        "top_segment_id": top_segment["market_segment_id"] if top_segment else None,
        "explanation": f"Best consumer segment: {top_segment['market_segment_id']}" if top_segment else "No consumer scoring",
    }
