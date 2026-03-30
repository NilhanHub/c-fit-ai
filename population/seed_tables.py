"""Load Prompt #02 Colombo seed tables used by the synthetic B2C model."""

from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = REPO_ROOT / "data" / "seed" / "colombo"

_FLOAT_FIELDS = {"weight", "value", "base_weight"}
_INT_FIELDS = {
    "household_size",
    "adults",
    "children",
    "elders",
    "population_2024",
    "need_jobs",
    "need_education",
    "need_healthcare",
    "need_commerce",
    "need_housing",
    "need_mobility",
    "need_productivity",
    "need_finance",
    "need_family_admin",
}


def _split_refs(raw_value: str) -> list[str]:
    return [item for item in raw_value.split("|") if item]


def _coerce_value(key: str, value: str) -> object:
    if value == "":
        return value
    if key in _INT_FIELDS:
        return int(value)
    if key in _FLOAT_FIELDS or key.endswith("_share"):
        return float(value)
    if key == "evidence_refs":
        return _split_refs(value)
    return value


def load_seed_table(file_name: str) -> list[dict]:
    path = SEED_DIR / file_name
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{key: _coerce_value(key, value) for key, value in row.items()} for row in reader]


def load_population_anchors() -> dict[str, dict]:
    return {row["metric"]: row for row in load_seed_table("population_anchors.csv")}


def load_age_weights() -> list[dict]:
    return load_seed_table("b2c_age_weights.csv")


def load_area_clusters() -> list[dict]:
    return load_seed_table("b2c_area_clusters.csv")


def load_household_archetypes() -> list[dict]:
    return load_seed_table("b2c_household_archetypes.csv")


def load_ds_populations_v2() -> list[dict]:
    return load_seed_table("colombo_ds_population_2024.csv")


def load_zone_map_v1() -> list[dict]:
    return load_seed_table("colombo_zone_map_v1.csv")


def load_household_archetypes_v2() -> list[dict]:
    return load_seed_table("b2c_household_archetypes_v2.csv")


def load_b2b_firm_archetypes_v2() -> list[dict]:
    return load_seed_table("b2b_firm_archetypes_v2.csv")
