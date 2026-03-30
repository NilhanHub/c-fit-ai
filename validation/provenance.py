"""Utilities that enforce the repo's FACT / INFERENCE / TBD provenance doctrine."""

from __future__ import annotations

from typing import Iterable


ALLOWED_CLAIM_TYPES = {"FACT", "INFERENCE", "TBD"}
REQUIRED_PROVENANCE_FIELDS = ("claim_type", "retrieved_at", "evidence_refs")
DEFAULT_RETRIEVED_AT = "1970-01-01T00:00:00Z"


def require_provenance(payload: dict, required_fields: Iterable[str] = REQUIRED_PROVENANCE_FIELDS) -> dict:
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise ValueError(f"Missing provenance fields: {', '.join(missing)}")

    claim_type = payload["claim_type"]
    if claim_type not in ALLOWED_CLAIM_TYPES:
        raise ValueError(f"claim_type must be one of {sorted(ALLOWED_CLAIM_TYPES)}")

    evidence_refs = payload["evidence_refs"]
    if not isinstance(evidence_refs, list) or not evidence_refs or not all(
        isinstance(item, str) and item.strip() for item in evidence_refs
    ):
        raise ValueError("evidence_refs must contain at least one non-empty string")

    return payload


def slugify(value: str) -> str:
    normalized = "".join(character.lower() if character.isalnum() else "-" for character in value)
    compact = "-".join(fragment for fragment in normalized.split("-") if fragment)
    return compact or "unknown"
