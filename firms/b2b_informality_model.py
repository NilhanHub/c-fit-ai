"""Prompt #03 B2B informality and semi-formality modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import informality_score


def derive_informality_score(formality: str) -> float:
    return informality_score(formality)
