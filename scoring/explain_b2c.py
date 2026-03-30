"""B2C explanation helpers for Prompt #02 rankings."""

from __future__ import annotations


def explain_b2c_result(result: dict) -> dict:
    if not result["scorecards"]:
        return {"headline": "Not scored on B2C", "details": ["Offer is B2B-only."]}

    top_scorecard = max(result["scorecards"], key=lambda item: item["final_rank_score"])
    top_dimensions = sorted(top_scorecard["dimension_scores"].items(), key=lambda item: item[1], reverse=True)[:3]
    return {
        "headline": f"B2C fit centers on {top_scorecard['market_segment_id']}",
        "details": [f"{name}: {value}" for name, value in top_dimensions],
    }
