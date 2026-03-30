"""Prompt #03 B2C conversion-friction modeling."""

from __future__ import annotations

from population.prompt03_b2c_core import conversion_friction_score


def derive_conversion_friction(digital_readiness: float, trust_openness: float, payment_readiness: float) -> float:
    return conversion_friction_score(digital_readiness, trust_openness, payment_readiness)
