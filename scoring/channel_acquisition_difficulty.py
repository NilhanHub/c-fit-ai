"""Prompt #03 channel-acquisition difficulty logic."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp
from scoring.prompt03_common import channel_model_score


def score_channel_acquisition_difficulty(offer: dict, reachability_score: float, scenario: dict) -> float:
    return clamp((reachability_score * 0.55) + (channel_model_score(offer["channel_model"]) * 0.45) + scenario.get("channel_shift", 0))
