"""Load Colombo firm archetypes for Prompt #02."""

from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = REPO_ROOT / "data" / "seed" / "colombo"

_FLOAT_FIELDS = {"weight"}
_INT_FIELDS = {
    "ability_to_pay",
    "needs_customer_support",
    "needs_document_admin",
    "needs_sales_marketing",
    "needs_collections",
    "needs_ops_scheduling",
    "needs_hr_internal",
    "needs_analytics",
    "needs_training",
}


def _split_refs(raw_value: str) -> list[str]:
    return [item for item in raw_value.split("|") if item]


def _coerce_value(key: str, value: str) -> object:
    if key in _INT_FIELDS:
        return int(value)
    if key in _FLOAT_FIELDS or key.endswith("_share"):
        return float(value)
    if key == "evidence_refs":
        return _split_refs(value)
    return value


def _load_csv_rows(file_name: str) -> list[dict]:
    with (SEED_DIR / file_name).open("r", encoding="utf-8", newline="") as handle:
        return [{key: _coerce_value(key, value) for key, value in row.items()} for row in csv.DictReader(handle)]


def load_firm_archetypes() -> list[dict]:
    return _load_csv_rows("b2b_firm_archetypes.csv")


def load_firm_anchors() -> dict[str, dict]:
    return {row["metric"]: row for row in _load_csv_rows("firm_anchors.csv")}
