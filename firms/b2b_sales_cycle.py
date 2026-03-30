"""Prompt #03 B2B sales-cycle length modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import sales_cycle_length


def derive_sales_cycle_length(procurement_speed: float, size_band: str, formality: str) -> float:
    return sales_cycle_length(procurement_speed, size_band, formality)
