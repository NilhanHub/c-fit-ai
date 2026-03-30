"""Normalize and load the Prompt #03 candidate, substitute, and benchmark corpora."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import jsonschema

from offers.offer_quality_scoring import score_offer_quality


REPO_ROOT = Path(__file__).resolve().parents[1]
CURATED_DIR = REPO_ROOT / "data" / "curated"
OFFER_SCHEMA_V2 = json.loads((REPO_ROOT / "offers" / "offer_schema_v2.json").read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft202012Validator(OFFER_SCHEMA_V2)

CORPUS_PATHS = {
    "candidate_offers": CURATED_DIR / "india_ai_offers_v2.csv",
    "local_substitutes": CURATED_DIR / "colombo_alternatives_v1.csv",
    "national_substitutes": CURATED_DIR / "sri_lanka_alternatives_v1.csv",
    "international_benchmarks": CURATED_DIR / "international_benchmarks_v1.csv",
}


def _split(raw_value: str) -> list[str]:
    return [item.strip() for item in raw_value.split("|") if item.strip()]


def _read_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_offer_record(raw_row: dict) -> dict:
    normalized = {
        "offer_id": raw_row["offer_id"],
        "vendor_name": raw_row["vendor_name"],
        "vendor_country": raw_row["vendor_country"],
        "offer_name": raw_row["offer_name"],
        "source_url": raw_row["source_url"].strip(),
        "source_type": raw_row["source_type"].strip(),
        "claim_type": raw_row["claim_type"],
        "retrieved_at": raw_row["retrieved_at"],
        "evidence_refs": _split(raw_row["evidence_refs"]),
        "offer_kind": raw_row["offer_kind"],
        "market_side": raw_row["market_side"],
        "target_market": raw_row["target_market"],
        "target_user_type": raw_row["target_user_type"],
        "problem_domain": raw_row["problem_domain"],
        "workflow_solved": raw_row["workflow_solved"],
        "input_requirements": _split(raw_row["input_requirements"]),
        "required_device_connectivity": raw_row["required_device_connectivity"],
        "required_digital_maturity": raw_row["required_digital_maturity"],
        "pricing_model": raw_row["pricing_model"],
        "pricing_visibility": raw_row["pricing_visibility"],
        "minimum_budget_band": raw_row["minimum_budget_band"],
        "minimum_budget_lkr": float(raw_row["minimum_budget_lkr"]),
        "implementation_friction": raw_row["implementation_friction"],
        "onboarding_burden": raw_row["onboarding_burden"],
        "trust_barrier": raw_row["trust_barrier"],
        "language_support": _split(raw_row["language_support"]),
        "language_demands": raw_row["language_demands"],
        "integration_demands": raw_row["integration_demands"],
        "regulatory_sensitivity": raw_row["regulatory_sensitivity"],
        "expected_roi_path": raw_row["expected_roi_path"],
        "roi_visibility": raw_row["roi_visibility"],
        "evidence_strength": int(raw_row["evidence_strength"]),
        "channel_model": raw_row["channel_model"],
        "substitute_cluster": raw_row["substitute_cluster"],
        "support_burden": raw_row["support_burden"],
        "vendor_durability": raw_row["vendor_durability"],
        "deployability": raw_row["deployability"],
        "notes": raw_row["notes"],
    }
    VALIDATOR.validate(normalized)
    normalized["quality"] = score_offer_quality(normalized)
    return normalized


def load_prompt03_offer_corpora() -> dict[str, list[dict]]:
    corpora: dict[str, list[dict]] = {}
    for corpus_name, path in CORPUS_PATHS.items():
        corpora[corpus_name] = sorted((normalize_offer_record(row) for row in _read_rows(path)), key=lambda item: item["offer_id"])
    return corpora


def load_prompt03_candidate_offers() -> list[dict]:
    corpora = load_prompt03_offer_corpora()
    return corpora["candidate_offers"]
