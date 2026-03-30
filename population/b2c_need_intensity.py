"""Prompt #03 need-intensity modeling for Colombo consumer domains."""

from __future__ import annotations

from population.prompt03_b2c_core import need_intensity_map


def derive_need_intensities(archetype: dict, zone_id: str) -> dict[str, float]:
    return need_intensity_map(archetype, zone_id)
