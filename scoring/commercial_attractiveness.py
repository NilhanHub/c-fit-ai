"""Prompt #03 combined commercial-attractiveness logic."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp


def score_commercial_attractiveness(
    fit_score: float,
    pricing_fit: float,
    entry_headroom: float,
    channel_headroom: float,
    retention_value: float,
    quality_score: float,
    scenario: dict,
) -> float:
    return clamp(
        (fit_score * 0.34)
        + (pricing_fit * 0.16)
        + (entry_headroom * 0.14)
        + (channel_headroom * 0.12)
        + (retention_value * 0.14)
        + (quality_score * 0.1)
        + scenario.get("commercial_shift", 0)
    )
