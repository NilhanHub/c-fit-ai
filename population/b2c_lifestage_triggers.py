"""Prompt #03 life-stage trigger modeling for Colombo consumers."""

from __future__ import annotations

from population.prompt03_b2c_core import lifestage_trigger_list


def derive_lifestage_triggers(archetype: dict) -> list[str]:
    return lifestage_trigger_list(archetype)
