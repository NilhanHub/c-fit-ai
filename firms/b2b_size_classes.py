"""Prompt #03 B2B size-class modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import size_class_score


def derive_size_class_score(size_band: str) -> float:
    return size_class_score(size_band)
