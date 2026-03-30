"""Prompt #03 B2B owner or manager sophistication modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import owner_sophistication_score


def derive_owner_sophistication(level: str, digital_maturity: float, formality: str) -> float:
    return owner_sophistication_score(level, digital_maturity, formality)
