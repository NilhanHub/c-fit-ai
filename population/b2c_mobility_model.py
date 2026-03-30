"""Prompt #03 commute and mobility-burden modeling for Colombo consumers."""

from __future__ import annotations

from population.prompt03_b2c_core import mobility_access_score


def derive_mobility_access(mobility_profile: str, zone_id: str) -> float:
    return mobility_access_score(mobility_profile, zone_id)
