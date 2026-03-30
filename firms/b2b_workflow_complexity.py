"""Prompt #03 B2B workflow-complexity modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import workflow_complexity_score


def derive_workflow_complexity(level: str, sector_id: str) -> float:
    return workflow_complexity_score(level, sector_id)
