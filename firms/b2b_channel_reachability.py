"""Prompt #03 B2B channel-reachability modeling."""

from __future__ import annotations

from firms.prompt03_b2b_core import channel_reachability_score


def derive_b2b_channel_reachability(channel_mix: str, owner_sophistication: float, zone_id: str) -> float:
    return channel_reachability_score(channel_mix, owner_sophistication, zone_id)
