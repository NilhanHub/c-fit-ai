"""Prompt #03 B2B within-account expansion-potential modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import expansion_potential_score


def derive_expansion_potential(
    ability_to_pay: float, digital_maturity: float, customer_interaction: float, size_band: str
) -> float:
    return expansion_potential_score(ability_to_pay, digital_maturity, customer_interaction, size_band)
