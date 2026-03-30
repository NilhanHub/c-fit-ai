"""Prompt #03 B2B payment-cycle friction modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import payment_cycle_score


def derive_payment_cycle_friction(level: str, formality: str, sector_id: str) -> float:
    return payment_cycle_score(level, formality, sector_id)
