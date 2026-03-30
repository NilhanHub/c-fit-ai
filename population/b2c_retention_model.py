"""Prompt #03 B2C retention-likelihood modeling."""

from __future__ import annotations

from population.prompt03_b2c_core import retention_potential


def derive_retention_potential(
    need_scores: dict[str, float], frequency_scores: dict[str, float], budget_headroom: float
) -> float:
    return retention_potential(need_scores, frequency_scores, budget_headroom)
