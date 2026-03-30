"""Quality scoring for Prompt #03 offer records."""

from __future__ import annotations


SOURCE_TYPE_SCORES = {
    "vendor_official": 62,
    "benchmark_official": 64,
}

VISIBILITY_SCORES = {"high_visibility": 80, "medium_visibility": 58, "low_visibility": 34}
LEVEL_SCORES = {"low": 80, "medium": 58, "high": 34}
DURABILITY_SCORES = {"low": 30, "medium": 56, "high": 78}


def score_offer_quality(offer: dict) -> dict:
    source_score = SOURCE_TYPE_SCORES.get(offer["source_type"], 45)
    pricing_score = VISIBILITY_SCORES.get(offer["pricing_visibility"], 40)
    roi_score = VISIBILITY_SCORES.get(offer["roi_visibility"], 40)
    deployability_score = {"plug_and_play": 82, "assisted_setup": 62, "integration_project": 36}[offer["deployability"]]
    trust_penalty = 100 - LEVEL_SCORES.get(offer["trust_barrier"], 50)
    support_score = LEVEL_SCORES.get(offer["support_burden"], 50)
    durability_score = DURABILITY_SCORES.get(offer["vendor_durability"], 50)
    quality_score = round(
        (offer["evidence_strength"] * 0.3)
        + (source_score * 0.15)
        + (pricing_score * 0.1)
        + (roi_score * 0.1)
        + (deployability_score * 0.1)
        + (support_score * 0.1)
        + (durability_score * 0.1)
        + (trust_penalty * 0.05),
        2,
    )
    return {
        "quality_score": quality_score,
        "source_score": source_score,
        "pricing_score": pricing_score,
        "roi_score": roi_score,
        "deployability_score": deployability_score,
        "support_score": support_score,
        "durability_score": durability_score,
    }
