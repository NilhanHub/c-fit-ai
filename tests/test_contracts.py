from pathlib import Path

import jsonschema
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = REPO_ROOT / "contracts"


def load_schema(name: str) -> dict:
    return yaml.safe_load((CONTRACT_DIR / name).read_text(encoding="utf-8"))


def validate(schema_name: str, payload: dict) -> None:
    jsonschema.Draft202012Validator(load_schema(schema_name)).validate(payload)


def test_contract_schemas_validate_minimal_examples() -> None:
    validate(
        "population_entity.schema.yaml",
        {
            "person_id": "person-0001",
            "household_id": "household-0001",
            "geo_id": "LK-11",
            "claim_type": "INFERENCE",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "evidence_refs": ["dcs-hies-2019"],
            "demographics": {"age_band": "25-34", "gender": "female"},
            "economics": {"income_band_lkr_monthly": "100000-149999"},
            "digital": {"smartphone_access": "shared", "internet_access": "mobile_only"},
            "behavioral": {"adoption_posture": "early_majority"},
        },
    )
    validate(
        "household_entity.schema.yaml",
        {
            "household_id": "household-0001",
            "geo_id": "LK-11",
            "claim_type": "INFERENCE",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "evidence_refs": ["dcs-hies-2019"],
            "household_size": 4,
            "composition": {"adults": 2, "children": 2},
            "economics": {"income_band_lkr_monthly": "100000-149999"},
            "digital_context": {"smartphone_count_band": "2+", "payment_readiness": "mixed"},
        },
    )
    validate(
        "firm_entity.schema.yaml",
        {
            "firm_id": "firm-0001",
            "geo_id": "LK-11",
            "sector_code": "services_bpo",
            "size_band": "small",
            "formality": "formal",
            "digital_maturity": "emerging",
            "budget_posture": "targeted",
            "adoption_friction": "medium",
            "claim_type": "INFERENCE",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "evidence_refs": ["dcs-non-agri-2021"],
        },
    )
    validate(
        "buying_center.schema.yaml",
        {
            "buying_center_id": "bc-0001",
            "firm_id": "firm-0001",
            "procurement_style": "owner_led",
            "risk_tolerance": "medium",
            "decision_roles": [
                {"role": "economic_buyer", "title": "Founder"},
                {"role": "user_champion", "title": "Operations Lead"},
            ],
            "claim_type": "INFERENCE",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "evidence_refs": ["prompt01-spec"],
        },
    )
    validate(
        "offer.schema.yaml",
        {
            "offer_id": "offer-0001",
            "vendor_name": "Example AI Pvt Ltd",
            "vendor_country": "IN",
            "offer_name": "AI Support Copilot",
            "target_segment": "b2b_sme",
            "problem_category": "customer_support",
            "delivery_mode": "saas",
            "pricing_model": "subscription",
            "language_support": ["en"],
            "evidence_refs": ["https://example.com/offer"],
            "claim_type": "FACT",
            "source_url": "https://example.com/offer",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "proof_points": [{"type": "case_study", "summary": "Named BFSI deployment"}],
        },
    )
    validate(
        "scorecard.schema.yaml",
        {
            "offer_id": "offer-0001",
            "market_segment_id": "colombo-b2b-sme-services",
            "scenario_id": "baseline",
            "dimension_scores": {
                "pain_frequency": 70,
                "problem_severity": 65,
                "willingness_to_pay": 55,
                "price_fit": 60,
                "trust_barrier": 40,
                "language_friction": 50,
                "smartphone_fit": 75,
                "payment_friction": 45,
                "workflow_fit": 68,
                "repeat_usage_potential": 74,
                "switching_cost": 58,
                "sme_purchase_plausibility": 62,
                "enterprise_purchase_plausibility": 54,
                "sales_cycle_friction": 49,
                "channel_feasibility": 61,
                "pilotability": 77,
                "regulatory_compliance_friction": 52,
                "support_burden": 46,
                "explainability": 71,
                "localization_effort": 57,
            },
            "raw_score": 60.45,
            "weighted_score": 61.1,
            "confidence_score": 58.0,
            "evidence_score": 80.0,
            "simulation_score": 50.0,
            "final_rank_score": 61.0,
            "blockers": [],
            "claim_type": "INFERENCE",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "evidence_refs": ["prompt01-scoring-framework"],
        },
    )
    validate(
        "experiment.schema.yaml",
        {
            "experiment_id": "pilot-100-baseline",
            "offer_batch_id": "india-pilot-100",
            "scenario_pack": ["baseline", "low_trust", "payment_friction"],
            "random_seed": 42,
            "market_slice_id": "colombo-v0",
            "selection_rule": "top25_then_top10",
            "claim_type": "INFERENCE",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "evidence_refs": ["prompt01-experiment-plan"],
        },
    )


def test_offer_schema_rejects_invalid_claim_type() -> None:
    schema = load_schema("offer.schema.yaml")
    payload = {
        "offer_id": "offer-0002",
        "vendor_name": "Example AI Pvt Ltd",
        "vendor_country": "IN",
        "offer_name": "AI Support Copilot",
        "target_segment": "b2b_sme",
        "problem_category": "customer_support",
        "delivery_mode": "saas",
        "pricing_model": "subscription",
        "language_support": ["en"],
        "evidence_refs": ["https://example.com/offer"],
        "claim_type": "UNPROVEN",
        "source_url": "https://example.com/offer",
        "retrieved_at": "2026-03-16T00:00:00Z",
    }

    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: error.path)
    assert errors, "Expected invalid claim_type to be rejected"


def test_scorecard_schema_requires_provenance() -> None:
    schema = load_schema("scorecard.schema.yaml")
    payload = {
        "offer_id": "offer-0001",
        "market_segment_id": "colombo-b2c-mobile-workers",
        "scenario_id": "baseline",
        "dimension_scores": {"pain_frequency": 70},
        "raw_score": 70,
        "weighted_score": 70,
        "confidence_score": 50,
        "evidence_score": 50,
        "simulation_score": 0,
        "final_rank_score": 55,
        "blockers": [],
        "claim_type": "INFERENCE",
        "retrieved_at": "2026-03-16T00:00:00Z",
    }

    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: error.path)
    assert errors, "Expected missing evidence_refs to be rejected"
