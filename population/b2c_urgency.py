"""Prompt #03 urgency modeling for Colombo consumer demand domains."""

from __future__ import annotations

from population.prompt03_b2c_core import urgency_from_need


def derive_domain_urgency(need_scores: dict[str, float], trust_openness: float, budget_headroom: float) -> dict[str, float]:
    return urgency_from_need(need_scores, trust_openness, budget_headroom)
