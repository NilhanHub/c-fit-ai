"""Prompt #03 market-entry difficulty logic."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp
from scoring.prompt03_common import channel_model_score, level_score


def score_market_entry_difficulty(offer: dict, scenario: dict) -> float:
    difficulty = (
        level_score(offer["implementation_friction"]) * 0.28
        + level_score(offer["onboarding_burden"]) * 0.22
        + level_score(offer["trust_barrier"]) * 0.2
        + level_score(offer["regulatory_sensitivity"]) * 0.15
        + (100 - channel_model_score(offer["channel_model"])) * 0.15
    )
    shock = scenario.get("entry_difficulty_shift", 0)
    return clamp(100 - difficulty + shock)
