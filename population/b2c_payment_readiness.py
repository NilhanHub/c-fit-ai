"""Prompt #03 payment-readiness modeling for Colombo consumers."""

from __future__ import annotations

from population.prompt03_b2c_core import payment_readiness_score


def derive_payment_readiness(payment_readiness: str, budget_tightness: str) -> float:
    return payment_readiness_score(payment_readiness, budget_tightness)
