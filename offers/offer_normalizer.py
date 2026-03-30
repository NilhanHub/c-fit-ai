"""Load and normalize the Prompt #02 curated India AI offer corpus."""

from __future__ import annotations

import csv
from pathlib import Path

from offers.normalize import normalize_offer


REPO_ROOT = Path(__file__).resolve().parents[1]
CURATED_OFFERS_PATH = REPO_ROOT / "data" / "curated" / "india_ai_offers_v1.csv"


def _split_pipe_list(raw_value: str) -> list[str]:
    return [item.strip() for item in raw_value.split("|") if item.strip()]


def normalize_curated_offer(raw_row: dict) -> dict:
    normalized = normalize_offer(
        raw_offer={
            "offer_id": raw_row["offer_id"],
            "vendor_name": raw_row["vendor_name"].strip(),
            "vendor_country": raw_row["vendor_country"],
            "offer_name": raw_row["offer_name"].strip(),
            "target_segment": raw_row["target_segment"],
            "problem_category": raw_row["problem_domain"],
            "delivery_mode": "hybrid" if raw_row["implementation_motion"] == "integration_project" else "saas",
            "pricing_model": raw_row["pricing_model"],
            "language_support": _split_pipe_list(raw_row["language_support"]),
        },
        source_metadata={
            "source_url": raw_row["source_url"],
            "source_type": raw_row["source_type"],
            "retrieved_at": raw_row["retrieved_at"],
            "claim_type": raw_row["claim_type"],
            "evidence_refs": _split_pipe_list(raw_row["evidence_refs"]),
            "assumption_note": raw_row["notes"],
        },
    )
    normalized.update(
        {
            "target_user_type": raw_row["target_user_type"],
            "problem_domain": raw_row["problem_domain"],
            "workflow_solved": raw_row["workflow_solved"],
            "input_requirements": _split_pipe_list(raw_row["input_requirements"]),
            "required_device_connectivity": raw_row["required_device_connectivity"],
            "required_digital_maturity": raw_row["required_digital_maturity"],
            "minimum_budget_band": raw_row["minimum_budget_band"],
            "deployment_friction": raw_row["deployment_friction"],
            "trust_barrier": raw_row["trust_barrier"],
            "language_demands": raw_row["language_demands"],
            "integration_demands": raw_row["integration_demands"],
            "regulatory_sensitivity": raw_row["regulatory_sensitivity"],
            "expected_roi_path": raw_row["expected_roi_path"],
            "evidence_strength": int(raw_row["evidence_strength"]),
            "market_side": raw_row["market_side"],
            "channel_model": raw_row["channel_model"],
            "local_substitute_pressure": raw_row["local_substitute_pressure"],
            "implementation_motion": raw_row["implementation_motion"],
            "notes": raw_row["notes"],
        }
    )
    return normalized


def load_curated_offer_corpus(path: Path | None = None) -> list[dict]:
    source_path = path or CURATED_OFFERS_PATH
    with source_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return sorted((normalize_curated_offer(row) for row in rows), key=lambda item: item["offer_id"])
