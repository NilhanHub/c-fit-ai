"""Prompt #03 B2B ability-to-pay modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import ability_to_pay_score


def derive_ability_to_pay(base_value: float, zone_id: str, digital_maturity: float) -> float:
    return ability_to_pay_score(base_value, zone_id, digital_maturity)
