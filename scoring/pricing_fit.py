"""Prompt #03 pricing-fit and affordability logic."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp
from scoring.prompt03_common import budget_requirement_score


def score_b2c_pricing_fit(avg_budget_headroom: float, offer: dict) -> float:
    requirement = budget_requirement_score(offer["minimum_budget_band"], offer["minimum_budget_lkr"])
    return clamp(avg_budget_headroom - (requirement - 28))


def score_b2b_pricing_fit(avg_ability_to_pay: float, offer: dict) -> float:
    requirement = budget_requirement_score(offer["minimum_budget_band"], offer["minimum_budget_lkr"])
    return clamp(avg_ability_to_pay - (requirement - 36))
