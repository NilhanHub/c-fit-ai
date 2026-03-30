"""Shared helpers for Prompt #03 commercial scoring."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp


LEVEL_SCORE = {"low": 78, "medium": 54, "high": 28}
MATURITY_SCORE = {"low": 32, "medium": 58, "high": 82}
BUDGET_BAND_SCORE = {
    "consumer_low": 18,
    "smb_low": 32,
    "smb_medium": 54,
    "enterprise_high": 82,
}
CHANNEL_MODEL_SCORE = {
    "self_serve": 82,
    "inside_sales": 58,
    "partner_led": 52,
    "enterprise_sales": 32,
}
ROI_VISIBILITY_SCORE = {"low": 36, "medium": 58, "high": 80}

B2C_PROBLEM_TO_FIELD = {
    "education_tutoring": "education",
    "mental_wellbeing": "healthcare",
    "productivity": "productivity",
    "healthcare_access": "healthcare",
    "mobility_logistics": "mobility",
    "customer_support": "family_admin",
    "classifieds_discovery": "commerce",
}

B2B_PROBLEM_TO_FIELD = {
    "customer_support": "customer_support",
    "document_admin": "document_admin",
    "sales_marketing": "sales_marketing",
    "collections": "collections",
    "ops_scheduling": "ops_scheduling",
    "hr_internal": "hr_internal",
    "analytics": "analytics",
    "healthcare_screening": "document_admin",
    "education_tutoring": "training",
    "productivity": "document_admin",
}


def level_score(level: str) -> float:
    return LEVEL_SCORE.get(level, 50)


def maturity_gap_score(required_level: str, available_score: float) -> float:
    required = MATURITY_SCORE.get(required_level, 50)
    return clamp(available_score - max(0.0, required - available_score) * 0.6)


def budget_requirement_score(band: str, minimum_budget_lkr: float) -> float:
    return clamp(BUDGET_BAND_SCORE.get(band, 40) + min(18.0, minimum_budget_lkr / 50000))


def channel_model_score(channel_model: str) -> float:
    return CHANNEL_MODEL_SCORE.get(channel_model, 50)


def language_fit(top_languages: str, supported_languages: list[str]) -> float:
    segment_languages = top_languages.split("|")
    if any(language in supported_languages for language in segment_languages):
        return 84
    if "en" in supported_languages:
        return 48
    return 24


def substitute_headroom(pressure_score: float) -> float:
    return clamp(100 - pressure_score)


def roi_visibility_score(level: str) -> float:
    return ROI_VISIBILITY_SCORE.get(level, 50)
