"""Prompt #03 B2C fit engine with decomposable commercial scoring."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp
from scoring.channel_acquisition_difficulty import score_channel_acquisition_difficulty
from scoring.commercial_attractiveness import score_commercial_attractiveness
from scoring.engine import score_offer
from scoring.market_entry_difficulty import score_market_entry_difficulty
from scoring.pricing_fit import score_b2c_pricing_fit
from scoring.prompt03_common import B2C_PROBLEM_TO_FIELD, language_fit, level_score, maturity_gap_score, substitute_headroom
from scoring.retention_expansion_value import score_b2c_retention_expansion


B2C_V2_WEIGHTS = {
    "pain_intensity": 1.15,
    "urgency": 1.0,
    "frequency": 0.95,
    "pricing_fit": 1.15,
    "digital_fit": 1.0,
    "trust_fit": 0.95,
    "language_fit": 0.85,
    "channel_fit": 0.9,
    "behavior_change_fit": 0.9,
    "substitute_headroom": 0.75,
    "implementation_fit": 0.9,
    "retention_value": 1.0,
}


def score_offer_for_b2c_v2(offer: dict, segments: list[dict], scenario: dict) -> dict:
    if offer["market_side"] == "b2b":
        return {"aggregate_score": 0.0, "top_segment_id": None, "scorecards": [], "commercial_score": 0.0}

    relevant_domain = B2C_PROBLEM_TO_FIELD.get(offer["problem_domain"], "family_admin")
    weighted_total = 0.0
    weight_sum = 0.0
    top_card = None
    scorecards = []

    for segment in segments:
        pain = clamp(segment[f"avg_need_{relevant_domain}"])
        urgency = clamp(segment[f"avg_urgency_{relevant_domain}"])
        frequency = clamp(segment[f"avg_frequency_{relevant_domain}"])
        pricing_fit = clamp(score_b2c_pricing_fit(segment["avg_budget_headroom"] + scenario.get("budget_shift", 0), offer))
        digital_fit = maturity_gap_score(
            offer["required_digital_maturity"],
            segment["avg_digital_readiness"] + scenario.get("digital_shift", 0),
        )
        trust_fit = clamp(max(
            0.0,
            segment["avg_trust_openness"] + scenario.get("trust_shift", 0) - (level_score(offer["trust_barrier"]) - 28),
        ))
        lang_fit = clamp(language_fit(segment["top_languages"], offer["language_support"]))
        channel_fit = clamp(score_channel_acquisition_difficulty(offer, segment["avg_channel_reachability"], scenario))
        behavior_change_fit = clamp(max(
            0.0,
            100 - ((level_score(offer["implementation_friction"]) * 0.55) + (level_score(offer["onboarding_burden"]) * 0.45)),
        ))
        substitutes = clamp(substitute_headroom(segment[f"avg_substitute_pressure_{relevant_domain}"]))
        implementation_fit = clamp(max(
            0.0,
            100
            - ((level_score(offer["integration_demands"]) * 0.45) + (level_score(offer["implementation_friction"]) * 0.35) - (digital_fit * 0.2)),
        ))
        retention_value = clamp(score_b2c_retention_expansion(
            segment["avg_retention_potential"], segment["avg_referral_potential"], offer
        ))

        scorecard = score_offer(
            offer_id=offer["offer_id"],
            market_segment_id=segment["segment_id"],
            scenario_id=scenario["scenario_id"],
            dimension_scores={
                "pain_intensity": pain,
                "urgency": urgency,
                "frequency": frequency,
                "pricing_fit": pricing_fit,
                "digital_fit": digital_fit,
                "trust_fit": trust_fit,
                "language_fit": lang_fit,
                "channel_fit": channel_fit,
                "behavior_change_fit": behavior_change_fit,
                "substitute_headroom": substitutes,
                "implementation_fit": implementation_fit,
                "retention_value": retention_value,
            },
            evidence_refs=offer["evidence_refs"] + ["prompt03-b2c-fit"],
            weights=B2C_V2_WEIGHTS,
            blockers=["pricing_mismatch"] if pricing_fit < 30 else [],
            simulation_score=segment["population_share"] * 100,
        )
        entry_headroom = score_market_entry_difficulty(offer, scenario)
        commercial_score = score_commercial_attractiveness(
            scorecard["final_rank_score"],
            pricing_fit,
            entry_headroom,
            channel_fit,
            retention_value,
            offer["quality"]["quality_score"],
            scenario,
        )
        scorecard["commercial_score"] = commercial_score
        scorecards.append(scorecard)
        weighted_total += commercial_score * segment["population_share"]
        weight_sum += segment["population_share"]
        if top_card is None or commercial_score > top_card["commercial_score"]:
            top_card = scorecard

    aggregate = round(weighted_total / weight_sum, 2) if weight_sum else 0.0
    return {
        "aggregate_score": aggregate,
        "top_segment_id": top_card["market_segment_id"] if top_card else None,
        "scorecards": scorecards,
        "commercial_score": aggregate,
    }
