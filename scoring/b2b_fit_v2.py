"""Prompt #03 B2B fit engine with decomposable commercial scoring."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp
from scoring.channel_acquisition_difficulty import score_channel_acquisition_difficulty
from scoring.commercial_attractiveness import score_commercial_attractiveness
from scoring.engine import score_offer
from scoring.market_entry_difficulty import score_market_entry_difficulty
from scoring.pricing_fit import score_b2b_pricing_fit
from scoring.prompt03_common import B2B_PROBLEM_TO_FIELD, level_score, maturity_gap_score, substitute_headroom
from scoring.retention_expansion_value import score_b2b_retention_expansion


B2B_V2_WEIGHTS = {
    "pain_severity": 1.15,
    "urgency": 1.0,
    "workflow_roi_clarity": 1.0,
    "pricing_fit": 1.1,
    "digital_fit": 0.95,
    "data_fit": 0.9,
    "owner_fit": 0.85,
    "integration_fit": 0.9,
    "compliance_fit": 0.85,
    "procurement_fit": 0.85,
    "sales_cycle_fit": 0.85,
    "channel_fit": 0.9,
    "substitute_headroom": 0.8,
    "retention_expansion": 1.05,
}


def score_offer_for_b2b_v2(offer: dict, segments: list[dict], scenario: dict) -> dict:
    if offer["market_side"] == "b2c":
        return {"aggregate_score": 0.0, "top_segment_id": None, "scorecards": [], "commercial_score": 0.0}

    relevant_domain = B2B_PROBLEM_TO_FIELD.get(offer["problem_domain"], "document_admin")
    weighted_total = 0.0
    weight_sum = 0.0
    top_card = None
    scorecards = []

    for segment in segments:
        pain = clamp(segment[f"avg_pain_{relevant_domain}"])
        urgency = clamp(max(pain, segment["avg_admin_burden"]))
        workflow_roi = clamp((pain * 0.6) + (segment["avg_workflow_complexity"] * 0.15) + 20)
        pricing_fit = clamp(score_b2b_pricing_fit(segment["avg_ability_to_pay"] + scenario.get("budget_shift", 0), offer))
        digital_fit = maturity_gap_score(
            offer["required_digital_maturity"], segment["avg_digital_maturity"] + scenario.get("digital_shift", 0)
        )
        data_fit = clamp(max(0.0, segment["avg_data_readiness"] - (level_score(offer["integration_demands"]) - 28)))
        owner_fit = clamp(max(0.0, segment["avg_owner_sophistication"] - (level_score(offer["onboarding_burden"]) - 24)))
        integration_fit = clamp(max(
            0.0,
            100
            - ((level_score(offer["integration_demands"]) * 0.55) + (level_score(offer["implementation_friction"]) * 0.45) - (segment["avg_data_readiness"] * 0.2)),
        ))
        compliance_fit = clamp(max(
            0.0, 100 - (level_score(offer["regulatory_sensitivity"]) * 0.7) + (segment["avg_admin_burden"] * 0.1)
        ))
        procurement_fit = clamp(segment["avg_procurement_speed"])
        sales_cycle_fit = clamp(max(0.0, 100 - segment["avg_sales_cycle_length"]))
        channel_fit = clamp(score_channel_acquisition_difficulty(offer, segment["avg_channel_reachability"], scenario))
        substitutes = clamp(substitute_headroom(segment["avg_substitute_pressure"]))
        retention_expansion = clamp(score_b2b_retention_expansion(
            max(segment["avg_pain_customer_support"], segment["avg_pain_document_admin"]),
            segment["avg_expansion_potential"],
            offer,
        ))

        blockers = []
        if pricing_fit < 34:
            blockers.append("pricing_mismatch")
        if offer["problem_domain"] == "healthcare_screening" and segment["segment_id"] not in {"b2b_service_admin_clusters"}:
            blockers.append("vertical_mismatch")
        scorecard = score_offer(
            offer_id=offer["offer_id"],
            market_segment_id=segment["segment_id"],
            scenario_id=scenario["scenario_id"],
            dimension_scores={
                "pain_severity": pain,
                "urgency": urgency,
                "workflow_roi_clarity": workflow_roi,
                "pricing_fit": pricing_fit,
                "digital_fit": digital_fit,
                "data_fit": data_fit,
                "owner_fit": owner_fit,
                "integration_fit": integration_fit,
                "compliance_fit": compliance_fit,
                "procurement_fit": procurement_fit,
                "sales_cycle_fit": sales_cycle_fit,
                "channel_fit": channel_fit,
                "substitute_headroom": substitutes,
                "retention_expansion": retention_expansion,
            },
            evidence_refs=offer["evidence_refs"] + ["prompt03-b2b-fit"],
            weights=B2B_V2_WEIGHTS,
            blockers=blockers,
            simulation_score=segment["firm_share"] * 100,
        )
        entry_headroom = score_market_entry_difficulty(offer, scenario)
        commercial_score = score_commercial_attractiveness(
            scorecard["final_rank_score"],
            pricing_fit,
            entry_headroom,
            channel_fit,
            retention_expansion,
            offer["quality"]["quality_score"],
            scenario,
        )
        scorecard["commercial_score"] = commercial_score
        scorecards.append(scorecard)
        weighted_total += commercial_score * segment["firm_share"]
        weight_sum += segment["firm_share"]
        if top_card is None or commercial_score > top_card["commercial_score"]:
            top_card = scorecard

    aggregate = round(weighted_total / weight_sum, 2) if weight_sum else 0.0
    return {
        "aggregate_score": aggregate,
        "top_segment_id": top_card["market_segment_id"] if top_card else None,
        "scorecards": scorecards,
        "commercial_score": aggregate,
    }
