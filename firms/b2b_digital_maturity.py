"""Prompt #03 B2B digital-maturity modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import digital_maturity_score


def derive_firm_digital_maturity(level: str, size_band: str, zone_id: str) -> float:
    return digital_maturity_score(level, size_band, zone_id)
