"""Prompt #03 digital-readiness modeling for Colombo consumers."""

from __future__ import annotations

from population.prompt03_b2c_core import digital_readiness_score


def derive_digital_readiness(
    smartphone_access: str, internet_access: str, payment_readiness: str, education_anchor: str, zone_id: str
) -> float:
    return digital_readiness_score(smartphone_access, internet_access, payment_readiness, education_anchor, zone_id)
