"""Prompt #03 B2B procurement-speed modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import procurement_speed_score


def derive_procurement_speed(level: str, size_band: str) -> float:
    return procurement_speed_score(level, size_band)
