"""Prompt #03 retention and expansion value logic."""

from __future__ import annotations

from population.prompt03_b2c_core import clamp
from scoring.prompt03_common import roi_visibility_score


def score_b2c_retention_expansion(retention_score: float, referral_score: float, offer: dict) -> float:
    return clamp((retention_score * 0.48) + (referral_score * 0.22) + (roi_visibility_score(offer["roi_visibility"]) * 0.3))


def score_b2b_retention_expansion(retention_score: float, expansion_score: float, offer: dict) -> float:
    return clamp((retention_score * 0.42) + (expansion_score * 0.33) + (roi_visibility_score(offer["roi_visibility"]) * 0.25))
