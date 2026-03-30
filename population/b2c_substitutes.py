"""Prompt #03 local substitute-availability modeling for B2C domains."""

from __future__ import annotations

from population.prompt03_b2c_core import substitute_pressure


def derive_substitute_pressure(zone_id: str, digital_readiness: float, income_band: str) -> dict[str, float]:
    return substitute_pressure(zone_id, digital_readiness, income_band)
