"""Prompt #03 B2C referral and virality potential modeling."""

from __future__ import annotations

from population.prompt03_b2c_core import referral_potential


def derive_referral_potential(digital_readiness: float, trust_openness: float, top_triggers: list[str]) -> float:
    return referral_potential(digital_readiness, trust_openness, top_triggers)
