"""Prompt #03 B2B ROI-tolerance modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import roi_tolerance_score


def derive_roi_tolerance(level: str, owner_sophistication: float) -> float:
    return roi_tolerance_score(level, owner_sophistication)
