"""Normalize externally discovered AI offers into the repo's strict comparable schema."""

from __future__ import annotations

from validation.provenance import require_provenance, slugify


REQUIRED_OFFER_FIELDS = (
    "vendor_name",
    "vendor_country",
    "offer_name",
    "target_segment",
    "problem_category",
    "delivery_mode",
    "pricing_model",
    "language_support",
)


def normalize_offer(raw_offer: dict, source_metadata: dict) -> dict:
    missing = [field for field in REQUIRED_OFFER_FIELDS if field not in raw_offer]
    if missing:
        raise ValueError(f"Missing raw offer fields: {', '.join(missing)}")

    require_provenance(source_metadata, required_fields=("source_url", "claim_type", "retrieved_at", "evidence_refs"))

    normalized = {**raw_offer, **source_metadata}
    normalized["offer_id"] = raw_offer.get(
        "offer_id",
        f"offer-{slugify(raw_offer['vendor_name'])}-{slugify(raw_offer['offer_name'])}",
    )
    normalized.setdefault("proof_points", [])
    normalized.setdefault("assumption_note", "")
    return normalized
