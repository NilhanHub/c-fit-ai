"""Combine B2C and B2B scores into scenario-specific offer rankings."""

from __future__ import annotations

from scoring.b2b_score import score_offer_for_b2b
from scoring.b2c_score import score_offer_for_b2c
from scoring.explain_b2b import explain_b2b_result
from scoring.explain_b2c import explain_b2c_result


def _combine_scores(b2c_result: dict, b2b_result: dict, scenario: dict) -> tuple[float, str]:
    market_mode = scenario["market_mode"]
    if market_mode == "b2c":
        return b2c_result["aggregate_score"], "b2c"
    if market_mode == "b2b":
        return b2b_result["aggregate_score"], "b2b"

    b2c_weight = scenario.get("mixed_weights", {}).get("b2c", 0.45)
    b2b_weight = scenario.get("mixed_weights", {}).get("b2b", 0.55)
    return round((b2c_result["aggregate_score"] * b2c_weight) + (b2b_result["aggregate_score"] * b2b_weight), 2), "mixed"


def rank_offers_for_scenario(offers: list[dict], b2c_segments: list[dict], b2b_segments: list[dict], scenario: dict) -> list[dict]:
    ranked: list[dict] = []
    for offer in offers:
        b2c_result = score_offer_for_b2c(offer, b2c_segments, scenario)
        b2b_result = score_offer_for_b2b(offer, b2b_segments, scenario)
        combined_score, market_view = _combine_scores(b2c_result, b2b_result, scenario)
        explanation = {
            "b2c": explain_b2c_result(b2c_result),
            "b2b": explain_b2b_result(b2b_result),
        }
        ranked.append(
            {
                "scenario_id": scenario["scenario_id"],
                "offer_id": offer["offer_id"],
                "vendor_name": offer["vendor_name"],
                "offer_name": offer["offer_name"],
                "market_side": offer["market_side"],
                "problem_domain": offer["problem_domain"],
                "final_score": combined_score,
                "b2c_score": b2c_result["aggregate_score"],
                "b2b_score": b2b_result["aggregate_score"],
                "dominant_market": market_view,
                "top_b2c_segment": b2c_result["top_segment_id"] or "",
                "top_b2b_segment": b2b_result["top_segment_id"] or "",
                "why_it_ranks": " | ".join([explanation["b2c"]["headline"], explanation["b2b"]["headline"]]),
            }
        )

    return sorted(ranked, key=lambda item: (-item["final_score"], item["offer_id"]))
