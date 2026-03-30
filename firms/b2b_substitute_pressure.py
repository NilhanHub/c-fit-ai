"""Prompt #03 B2B local incumbent and substitute-pressure modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import substitute_pressure_score


def derive_b2b_substitute_pressure(level: str, sector_id: str, zone_id: str) -> float:
    return substitute_pressure_score(level, sector_id, zone_id)
