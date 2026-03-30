"""Prompt #03 frequency-of-problem modeling for Colombo consumer demand domains."""

from __future__ import annotations

from population.prompt03_b2c_core import frequency_from_need


def derive_problem_frequency(need_scores: dict[str, float], mobility_score: float) -> dict[str, float]:
    return frequency_from_need(need_scores, mobility_score)
