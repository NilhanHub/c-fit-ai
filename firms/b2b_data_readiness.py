"""Prompt #03 B2B data-availability and integration readiness modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import data_readiness_score


def derive_data_readiness(level: str, digital_maturity: float, channel_mix: str) -> float:
    return data_readiness_score(level, digital_maturity, channel_mix)
