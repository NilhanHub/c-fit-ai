"""Prompt #03 budget-tightness and discretionary-spend modeling for Colombo consumers."""

from __future__ import annotations

from population.prompt03_b2c_core import budget_headroom_score


def derive_budget_headroom(income_band: str, budget_tightness: str, zone_id: str, discretionary_spend: str) -> float:
    return budget_headroom_score(income_band, budget_tightness, zone_id, discretionary_spend)
