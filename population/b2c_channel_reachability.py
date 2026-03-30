"""Prompt #03 B2C channel-reachability modeling."""

from __future__ import annotations

from population.prompt03_b2c_core import channel_reachability


DEFAULT_CONSUMER_CHANNELS = ["self_serve_app", "whatsapp_led", "inside_sales", "partner_led"]


def derive_consumer_channel_reachability(
    digital_readiness: float, mobility_score: float, trust_openness: float, channel_modes: list[str] | None = None
) -> dict[str, float]:
    return channel_reachability(channel_modes or DEFAULT_CONSUMER_CHANNELS, digital_readiness, mobility_score, trust_openness)
