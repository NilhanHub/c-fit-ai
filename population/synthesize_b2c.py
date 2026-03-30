"""Run the Prompt #02 B2C synthesis pipeline for Colombo District."""

from __future__ import annotations

import csv
from pathlib import Path
from random import Random

from population.b2c_household_archetypes_v2 import sample_b2c_household_archetype
from population.b2c_person_archetypes_v2 import build_b2c_people_v2
from population.household_sampler import HouseholdSamplerConfig, sample_households
from population.person_sampler import sample_people
from population.prompt03_b2c_core import (
    Prompt03B2CConfig,
    RETRIEVED_AT_PROMPT03,
    pick_zone_for_archetype,
    summarize_b2c_segments_v2,
)
from population.segment_taxonomy import summarize_b2c_segments


REPO_ROOT = Path(__file__).resolve().parents[1]


def generate_b2c_market(
    seed: int = 42,
    target_households: int = 1500,
    geography_scope: str = "LK-11",
    household_sample_size: int | None = None,
) -> dict:
    resolved_households = household_sample_size or target_households
    sampled = sample_households(
        HouseholdSamplerConfig(seed=seed, target_households=resolved_households, geography_scope=geography_scope)
    )
    households = sampled["households"]
    people = sample_people(households, seed=seed)
    segment_summaries = summarize_b2c_segments(people)
    return {
        "metadata": sampled["metadata"],
        "households": households,
        "people": people,
        "segment_summaries": segment_summaries,
        "segment_summary": segment_summaries,
        "uncertainty_flags": sampled["uncertainty_flags"]
        + [
            "INFERENCE: person-level roles, language preference, and need intensities are archetype-derived rather than directly observed",
            "TBD: segment shares should later be calibrated against survey microdata and pilot data",
        ],
    }


def write_b2c_segment_summary(result: dict, path: Path | None = None) -> Path:
    output_path = path or (REPO_ROOT / "outputs" / "b2c_segment_summary.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(result["segment_summaries"][0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result["segment_summaries"])
    return output_path


def generate_b2c_market_v2(
    seed: int = 42,
    target_households: int = 2000,
    geography_scope: str = "LK-11",
    household_sample_size: int | None = None,
) -> dict:
    config = Prompt03B2CConfig(seed=seed, target_households=household_sample_size or target_households, geography_scope=geography_scope)
    rng = Random(config.seed)
    households: list[dict] = []
    for index in range(config.target_households):
        archetype = sample_b2c_household_archetype(rng)
        zone = pick_zone_for_archetype(rng, archetype)
        household = {
            "household_id": f"household-v2-{index + 1:06d}",
            "geo_id": geography_scope,
            "zone_id": zone["zone_id"],
            "zone_label": zone["zone_label"],
            "claim_type": "INFERENCE",
            "retrieved_at": RETRIEVED_AT_PROMPT03,
            "evidence_refs": archetype["evidence_refs"],
            "archetype_id": archetype["archetype_id"],
            "household_size": archetype["household_size"],
            "adults": archetype["adults"],
            "children": archetype["children"],
            "elders": archetype["elders"],
            "income_band": archetype["income_band"],
            "education_anchor": archetype["education_anchor"],
            "employment_profile": archetype["employment_profile"],
            "language_profile": archetype["language_profile"],
            "smartphone_access": archetype["smartphone_access"],
            "internet_access": archetype["internet_access"],
            "payment_readiness": archetype["payment_readiness"],
            "mobility_profile": archetype["mobility_profile"],
            "budget_tightness": archetype["budget_tightness"],
            "trust_skepticism": archetype["trust_skepticism"],
            "discretionary_spend": archetype["discretionary_spend"],
            "lifestage_focus": archetype["lifestage_focus"],
            "need_jobs": archetype["need_jobs"],
            "need_education": archetype["need_education"],
            "need_healthcare": archetype["need_healthcare"],
            "need_commerce": archetype["need_commerce"],
            "need_housing": archetype["need_housing"],
            "need_mobility": archetype["need_mobility"],
            "need_productivity": archetype["need_productivity"],
            "need_finance": archetype["need_finance"],
            "need_family_admin": archetype["need_family_admin"],
            "assumption_note": archetype["assumption_note"],
        }
        households.append(household)

    people = build_b2c_people_v2(households, seed)
    segment_summary = summarize_b2c_segments_v2(people)
    return {
        "metadata": {
            "seed": seed,
            "target_households": config.target_households,
            "geography_scope": geography_scope,
            "claim_type": "INFERENCE",
            "retrieved_at": RETRIEVED_AT_PROMPT03,
            "evidence_refs": ["dcs-cph-2024-basic-population-ds", "dcs-hies-2019", "dcs-computer-literacy-2025-h1"],
        },
        "households": households,
        "people": people,
        "segment_summaries": segment_summary,
        "segment_summary": segment_summary,
        "uncertainty_flags": [
            "INFERENCE: zone clustering collapses DS divisions into five commercial simulation zones rather than claiming ward-level precision",
            "INFERENCE: household archetype shares are structured from official anchors plus explicit commercial heuristics",
            "TBD: willingness-to-pay and trust elasticities still need calibration against Colombo user interviews or pilots",
        ],
    }


def write_b2c_population_v2(result: dict, path: Path | None = None) -> Path:
    output_path = path or (REPO_ROOT / "outputs" / "b2c_population_v2.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample_rows = []
    for row in result["people"]:
        sample_rows.append(
            {
                "person_id": row["person_id"],
                "household_id": row["household_id"],
                "zone_id": row["zone_id"],
                "market_segment_id": row["market_segment_id"],
                "age_band": row["age_band"],
                "employment_status": row["employment_status"],
                "language_preference": row["language_preference"],
                "budget_headroom_score": row["budget_headroom_score"],
                "trust_openness_score": row["trust_openness_score"],
                "digital_readiness_score": row["digital_readiness_score"],
                "best_channel_reachability": row["best_channel_reachability"],
                "retention_potential_score": row["retention_potential_score"],
            }
        )
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sample_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sample_rows)
    return output_path
