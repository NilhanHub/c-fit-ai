"""Prompt #03 red-team audit for weak assumptions and fragile rankings."""

from __future__ import annotations


def run_red_team_audit(results: dict, sensitivity: dict) -> dict:
    top_offer = results["top_opportunities"][0]
    fragile_scenarios = [item["scenario_id"] for item in sensitivity["scenario_deltas"] if item["top10_overlap_vs_mixed_base"] < 6]
    findings = [
        {
            "risk": "pricing_inference",
            "claim_type": "INFERENCE",
            "detail": "Several vendor pages still hide pricing so minimum budget bands remain modeled proxies.",
        },
        {
            "risk": "consumer_weight_sensitivity",
            "claim_type": "INFERENCE",
            "detail": "Consumer rankings move more than SMB-heavy rankings when trust and digital readiness are shocked.",
        },
        {
            "risk": "top_offer_dependency",
            "claim_type": "FACT",
            "detail": f"Current mixed-market leader is {top_offer['offer_id']} and should be challenged with real operator interviews before commercialization claims.",
        },
    ]
    return {"fragile_scenarios": fragile_scenarios, "findings": findings}
