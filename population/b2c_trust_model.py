"""Prompt #03 trust and skepticism modeling for Colombo consumers."""

from __future__ import annotations

from population.prompt03_b2c_core import trust_openness_score


def derive_trust_openness(trust_skepticism: str, education_anchor: str, zone_id: str) -> float:
    return trust_openness_score(trust_skepticism, education_anchor, zone_id)
