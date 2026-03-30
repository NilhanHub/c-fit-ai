"""Prompt #03 B2B customer-interaction intensity modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import customer_interaction_score


def derive_customer_interaction(level: str, channel_mix: str) -> float:
    return customer_interaction_score(level, channel_mix)
