"""Prompt #03 B2B staff-intensity and labor-pain modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import staff_intensity_score


def derive_staff_intensity(level: str) -> float:
    return staff_intensity_score(level)
