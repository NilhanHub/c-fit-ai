"""Dimension weights and helper maps for Prompt #02 B2C scoring."""

from __future__ import annotations


B2C_DIMENSION_WEIGHTS = {
    "pain_intensity": 1.25,
    "urgency": 1.1,
    "frequency_of_problem": 1.0,
    "reachable_channel_fit": 1.0,
    "digital_readiness": 1.0,
    "affordability": 1.2,
    "trust_fit": 1.1,
    "language_fit": 1.0,
    "behavior_change_burden": 0.9,
    "local_substitute_saturation": 0.8,
    "implementation_friction": 0.9,
    "retention_potential": 1.0,
    "expansion_potential": 0.8,
}

OFFER_TO_B2C_NEED_FIELD = {
    "education_tutoring": "avg_need_education",
    "mental_wellbeing": "avg_need_healthcare",
    "customer_support": "avg_need_family_admin",
    "sales_marketing": "avg_need_commerce",
    "document_admin": "avg_need_family_admin",
    "finance_bookkeeping": "avg_need_finance",
    "productivity": "avg_need_productivity",
    "housing_search": "avg_need_housing",
    "mobility_logistics": "avg_need_mobility",
}

_BUDGET_REQUIREMENT = {
    "consumer_low": 20,
    "consumer_medium": 45,
    "smb_low": 40,
    "smb_medium": 60,
    "smb_high": 75,
    "enterprise_high": 90,
}
_LEVEL_SCORE = {"low": 35, "medium": 60, "high": 85}
_SUBSTITUTE_SCORE = {"low": 80, "medium": 55, "high": 35}
_DEVICE_SCORE = {
    "smartphone_only": 85,
    "smartphone_or_desktop": 72,
    "desktop_required": 35,
    "cloud_plus_crm": 20,
    "call_center_stack": 10,
}
_MARKET_SIDE_SCORE = {"b2c": 100, "both": 85, "b2b": 0}


def budget_requirement_score(minimum_budget_band: str) -> int:
    return _BUDGET_REQUIREMENT[minimum_budget_band]


def level_score(level: str) -> int:
    return _LEVEL_SCORE[level]


def substitute_score(level: str) -> int:
    return _SUBSTITUTE_SCORE[level]


def device_score(required_device_connectivity: str) -> int:
    return _DEVICE_SCORE[required_device_connectivity]


def market_side_score(market_side: str) -> int:
    return _MARKET_SIDE_SCORE[market_side]
