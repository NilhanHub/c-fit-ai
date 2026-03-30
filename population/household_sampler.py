"""Generate reproducible Colombo household samples from Prompt #02 seed tables."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from population.seed_tables import load_area_clusters, load_household_archetypes, load_population_anchors


RETRIEVED_AT = "2026-03-16T18:30:00Z"


@dataclass(frozen=True)
class HouseholdSamplerConfig:
    seed: int
    target_households: int
    geography_scope: str = "LK-11"


def _weighted_choice(rng: Random, rows: list[dict]) -> dict:
    return rng.choices(rows, weights=[row["weight"] for row in rows], k=1)[0]


def _smartphone_count_band(archetype: dict) -> str:
    if archetype["smartphone_access"] == "personal" and archetype["household_size"] >= 2:
        return "2+"
    if archetype["smartphone_access"] == "personal":
        return "1"
    if archetype["smartphone_access"] == "shared":
        return "1"
    return "0"


def sample_households(config: HouseholdSamplerConfig) -> dict:
    if config.target_households <= 0:
        raise ValueError("target_households must be positive")

    rng = Random(config.seed)
    archetypes = load_household_archetypes()
    area_clusters = {row["area_cluster"]: row for row in load_area_clusters()}
    anchors = load_population_anchors()
    households: list[dict] = []

    for index in range(config.target_households):
        archetype = _weighted_choice(rng, archetypes)
        area_cluster = area_clusters[archetype["area_cluster"]]
        adults_total = archetype["adults"] + archetype["elders"]
        household = {
            "household_id": f"household-{index + 1:06d}",
            "geo_id": config.geography_scope,
            "claim_type": "INFERENCE",
            "retrieved_at": RETRIEVED_AT,
            "evidence_refs": archetype["evidence_refs"],
            "household_size": archetype["household_size"],
            "composition": {"adults": adults_total, "children": archetype["children"]},
            "economics": {"income_band_lkr_monthly": archetype["income_band"]},
            "digital_context": {
                "smartphone_count_band": _smartphone_count_band(archetype),
                "payment_readiness": archetype["payment_readiness"],
            },
            "archetype_id": archetype["archetype_id"],
            "area_cluster": archetype["area_cluster"],
            "urbanization_proxy": area_cluster["urbanization_proxy"],
            "language_profile": archetype["language_profile"],
            "smartphone_access": archetype["smartphone_access"],
            "internet_access": archetype["internet_access"],
            "mobility_profile": archetype["mobility_profile"],
            "budget_sensitivity": archetype["budget_sensitivity"],
            "trust_sensitivity": archetype["trust_sensitivity"],
            "education_anchor": archetype["education_anchor"],
            "employment_profile": archetype["employment_profile"],
            "elders_count": archetype["elders"],
            "need_domain_scores": {
                "jobs": archetype["need_jobs"],
                "education": archetype["need_education"],
                "healthcare": archetype["need_healthcare"],
                "commerce": archetype["need_commerce"],
                "housing": archetype["need_housing"],
                "mobility": archetype["need_mobility"],
                "productivity": archetype["need_productivity"],
                "finance": archetype["need_finance"],
                "family_admin": archetype["need_family_admin"],
            },
            "assumption_note": archetype["assumption_note"],
        }
        households.append(household)

    return {
        "metadata": {
            "seed": config.seed,
            "target_households": config.target_households,
            "geography_scope": config.geography_scope,
            "population_anchor": anchors["population_total"]["value"],
            "household_anchor": anchors["households_total"]["value"],
            "avg_household_size_anchor": anchors["avg_household_size"]["value"],
            "claim_type": "FACT",
            "retrieved_at": RETRIEVED_AT,
            "evidence_refs": [
                "dcs-census-2024-colombo-population",
                "dcs-census-2024-colombo-households",
                "dcs-hies-2019",
            ],
        },
        "households": households,
        "uncertainty_flags": [
            "INFERENCE: household archetype shares approximate Colombo composition rather than calibrating to full microdata",
            "TBD: household archetypes should later be calibrated against richer district marginals",
        ],
    }
