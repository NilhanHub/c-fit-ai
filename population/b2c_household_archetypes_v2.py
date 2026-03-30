"""Load and sample Prompt #03 Colombo household archetypes."""

from __future__ import annotations

from random import Random

from population.prompt03_b2c_core import household_archetypes_v2


def load_b2c_household_archetypes_v2() -> list[dict]:
    return household_archetypes_v2()


def sample_b2c_household_archetype(rng: Random) -> dict:
    rows = household_archetypes_v2()
    return rng.choices(rows, weights=[row["base_weight"] for row in rows], k=1)[0]
