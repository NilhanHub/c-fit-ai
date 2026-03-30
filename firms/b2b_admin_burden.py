"""Prompt #03 B2B admin and compliance burden modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import admin_burden_score


def derive_admin_burden(level: str, sector_id: str) -> float:
    return admin_burden_score(level, sector_id)
