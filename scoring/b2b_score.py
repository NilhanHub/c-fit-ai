"""Prompt #02 B2B scoring against synthetic Colombo firm segments."""

from __future__ import annotations

from firms.pain_maps import OFFER_TO_FIRM_PAIN_FIELD
from scoring.b2b_dimensions import B2B_DIMENSION_WEIGHTS, budget_requirement_score, channel_score, level_score, substitute_score
from scoring.engine import score_offer


_PROCUREMENT_STYLE_SCORE = {"owner_led": 72, "manager_led": 60, "committee_led": 42}
_ROI_BONUS = {
    "cost_saving": 82,
    "service_speed": 74,
    "revenue_uplift": 68,
    "risk_reduction": 76,
    "yield_gain": 35,
}


def _clamp(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def _scenario_adjust(segment: dict, scenario: dict) -> dict:
    adjusted = dict(segment)
    for field, delta in scenario.get("b2b_attribute_deltas", {}).items():
        adjusted[field] = _clamp(adjusted[field] + delta)
    share_multiplier = scenario.get("b2b_share_multipliers", {}).get(segment["segment_id"], 1.0)
    adjusted["firm_share"] = round(segment["firm_share"] * share_multiplier, 6)
    return adjusted


def _vertical_penalty(offer: dict, segment_id: str) -> tuple[float, list[str]]:
    blockers: list[str] = []
    multiplier = 1.0

    if offer["problem_domain"] == "healthcare_screening" and segment_id != "b2b_healthcare_admin_clusters":
        multiplier = 0.35
        blockers.append("vertical_mismatch")
    elif offer["problem_domain"] == "education_tutoring" and segment_id != "b2b_education_service_operators":
        multiplier = 0.55
        blockers.append("vertical_mismatch")
    elif offer["offer_id"] == "offer-fasal-farm-advisory":
        multiplier = 0.2
        blockers.append("non_urban_vertical")

    return multiplier, blockers


def score_offer_for_b2b(offer: dict, segments: list[dict], scenario: dict) -> dict:
    if offer["market_side"] == "b2c":
        return {
            "offer_id": offer["offer_id"],
            "scenario_id": scenario["scenario_id"],
            "market": "b2b",
            "aggregate_score": 0.0,
            "scorecards": [],
            "top_segment_id": None,
            "explanation": "B2C-only offer is not scored on the firm-side market.",
        }

    scorecards: list[dict] = []
    weighted_total = 0.0
    weight_total = 0.0
    segment_weights: dict[str, float] = {}
    pain_field = OFFER_TO_FIRM_PAIN_FIELD.get(offer["problem_domain"], "avg_need_document_admin")

    for segment in segments:
        adjusted = _scenario_adjust(segment, scenario)
        blockers: list[str] = []
        vertical_multiplier, vertical_blockers = _vertical_penalty(offer, adjusted["segment_id"])
        blockers.extend(vertical_blockers)
        pain_severity = _clamp(adjusted[pain_field] * vertical_multiplier)
        workflow_roi_clarity = _clamp((pain_severity * 0.65) + (_ROI_BONUS.get(offer["expected_roi_path"], 60) * 0.35))
        ability_to_pay = _clamp(adjusted["avg_ability_to_pay"] - (budget_requirement_score(offer["minimum_budget_band"]) - 35))
        sales_cycle_length = adjusted["avg_decision_speed"]
        owner_buyer_sophistication = _clamp(adjusted["avg_owner_sophistication"] - max(0, level_score(offer["required_digital_maturity"]) - 45) * 0.3)
        digital_maturity = _clamp(adjusted["avg_digital_maturity"] - max(0, level_score(offer["required_digital_maturity"]) - 45) * 0.45)
        integration_burden = _clamp(100 - (level_score(offer["integration_demands"]) * 0.8) + (adjusted["avg_digital_maturity"] * 0.2))
        data_availability = _clamp((adjusted["avg_digital_maturity"] * 0.6) + (adjusted["avg_need_analytics"] * 0.4))
        compliance_risk = _clamp(100 - (level_score(offer["regulatory_sensitivity"]) * 0.7) - (pain_severity * 0.1))
        local_substitution_incumbency = substitute_score(offer["local_substitute_pressure"])
        implementation_complexity = _clamp(100 - (level_score(offer["deployment_friction"]) * 0.65) - (level_score(offer["integration_demands"]) * 0.35))
        urgency = _clamp((pain_severity * 0.6) + (adjusted["avg_need_collections"] * 0.2) + (adjusted["avg_need_customer_support"] * 0.2))
        retention_expansion_potential = _clamp((pain_severity * 0.55) + (_ROI_BONUS.get(offer["expected_roi_path"], 60) * 0.45))
        market_concentration = _clamp(adjusted["firm_share"] * 100)
        channel_reachability = _clamp((channel_score(offer["channel_model"]) * 0.55) + (_PROCUREMENT_STYLE_SCORE[adjusted["dominant_procurement_style"]] * 0.45))

        if ability_to_pay < 35:
            blockers.append("budget_mismatch")
        if digital_maturity < 30 and offer["required_digital_maturity"] == "high":
            blockers.append("maturity_gap")

        scorecard = score_offer(
            offer_id=offer["offer_id"],
            market_segment_id=adjusted["segment_id"],
            scenario_id=scenario["scenario_id"],
            dimension_scores={
                "pain_severity": pain_severity,
                "workflow_roi_clarity": workflow_roi_clarity,
                "ability_to_pay": ability_to_pay,
                "sales_cycle_length": sales_cycle_length,
                "owner_buyer_sophistication": owner_buyer_sophistication,
                "digital_maturity": digital_maturity,
                "integration_burden": integration_burden,
                "data_availability": data_availability,
                "compliance_risk": compliance_risk,
                "local_substitution_incumbency": local_substitution_incumbency,
                "implementation_complexity": implementation_complexity,
                "urgency": urgency,
                "retention_expansion_potential": retention_expansion_potential,
                "market_concentration": market_concentration,
                "channel_reachability": channel_reachability,
            },
            evidence_refs=offer["evidence_refs"] + ["prompt02-b2b-scorer"],
            weights=B2B_DIMENSION_WEIGHTS,
            blockers=blockers,
            rationales={
                "pain_severity": f"{offer['problem_domain']} matched against {pain_field}",
                "ability_to_pay": f"segment ability {adjusted['avg_ability_to_pay']} vs required {offer['minimum_budget_band']}",
                "channel_reachability": f"channel model {offer['channel_model']} into {adjusted['dominant_procurement_style']}",
            },
            simulation_score=adjusted["firm_share"] * 100,
        )
        scorecards.append(scorecard)
        weighted_total += scorecard["final_rank_score"] * adjusted["firm_share"]
        weight_total += adjusted["firm_share"]
        segment_weights[adjusted["segment_id"]] = adjusted["firm_share"]

    top_segment = max(scorecards, key=lambda item: item["final_rank_score"]) if scorecards else None
    aggregate_score = round(weighted_total / weight_total, 2) if weight_total else 0.0
    return {
        "offer_id": offer["offer_id"],
        "scenario_id": scenario["scenario_id"],
        "market": "b2b",
        "aggregate_score": aggregate_score,
        "scorecards": scorecards,
        "top_segment_id": top_segment["market_segment_id"] if top_segment else None,
        "explanation": f"Best firm segment: {top_segment['market_segment_id']}" if top_segment else "No firm scoring",
    }
