"""Dimension weights and helper maps for Prompt #02 B2B scoring."""

from __future__ import annotations


B2B_DIMENSION_WEIGHTS = {
    "pain_severity": 1.25,
    "workflow_roi_clarity": 1.15,
    "ability_to_pay": 1.2,
    "sales_cycle_length": 0.9,
    "owner_buyer_sophistication": 1.0,
    "digital_maturity": 1.0,
    "integration_burden": 0.95,
    "data_availability": 0.9,
    "compliance_risk": 0.9,
    "local_substitution_incumbency": 0.8,
    "implementation_complexity": 0.9,
    "urgency": 1.0,
    "retention_expansion_potential": 1.0,
    "market_concentration": 0.75,
    "channel_reachability": 0.95,
}

_LEVEL_SCORE = {"low": 30, "medium": 60, "high": 85}
_BUDGET_REQUIREMENT = {
    "smb_low": 40,
    "smb_medium": 58,
    "smb_high": 72,
    "enterprise_high": 88,
    "consumer_low": 20,
}
_CHANNEL_SCORE = {
    "inside_sales": 72,
    "enterprise_sales": 45,
    "partner_led": 58,
    "self_serve": 52,
    "api_partner": 40,
}
_SUBSTITUTE_SCORE = {"low": 78, "medium": 55, "high": 35}


def level_score(value: str) -> int:
    return _LEVEL_SCORE[value]


def budget_requirement_score(value: str) -> int:
    return _BUDGET_REQUIREMENT[value]


def channel_score(value: str) -> int:
    return _CHANNEL_SCORE[value]


def substitute_score(value: str) -> int:
    return _SUBSTITUTE_SCORE[value]
