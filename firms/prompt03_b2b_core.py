"""Core Prompt #03 B2B helpers shared across the commercial v2 firm modules."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from random import Random

from population.prompt03_b2c_core import DOMAIN_FIELDS, clamp, load_zone_catalog, zone_distribution
from population.seed_tables import load_b2b_firm_archetypes_v2


RETRIEVED_AT_PROMPT03_B2B = "2026-03-17T03:50:00Z"
SECTOR_LABELS_V2 = {
    "retail_trade": "Retail trade",
    "food_service": "Food service",
    "logistics_services": "Logistics and field service",
    "healthcare_services": "Healthcare services",
    "education_services": "Education services",
    "personal_services": "Personal services",
    "real_estate_services": "Real estate services",
    "professional_services": "Professional services",
    "wholesale_distribution": "Wholesale and distribution",
    "light_manufacturing": "Light manufacturing",
    "tourism_hospitality": "Tourism and hospitality",
    "construction_contractors": "Construction and contracting",
    "finance_admin_smes": "Finance and admin-heavy SMEs",
    "growth_services": "Growth-oriented services",
}

PAIN_FIELDS = (
    "customer_support",
    "document_admin",
    "sales_marketing",
    "collections",
    "ops_scheduling",
    "hr_internal",
    "analytics",
    "training",
)

ZONE_BUSINESS_PREMIUM = {
    "core_colombo": 10,
    "admin_professional_belt": 12,
    "east_growth_corridor": 2,
    "south_west_suburban": 0,
    "outer_commuter_belt": -6,
}

CHANNEL_MIX_SCORE = {
    "offline_first": 28,
    "hybrid": 56,
    "phone_and_field": 48,
    "phone_and_walkin": 46,
    "appointment_led": 58,
    "whatsapp_led": 52,
    "referral_and_digital": 70,
    "ota_and_phone": 60,
    "field_first": 42,
    "digital_first": 80,
}


def _weighted_choice(rng: Random, rows: list[dict], weight_field: str = "base_weight") -> dict:
    return rng.choices(rows, weights=[row[weight_field] for row in rows], k=1)[0]


def load_firm_archetypes_v2() -> list[dict]:
    return load_b2b_firm_archetypes_v2()


def pick_zone_for_firm(rng: Random, archetype: dict) -> dict:
    weights = []
    for zone in zone_distribution():
        weight = zone["weight"]
        if archetype["sector_id"] in {"professional_services", "finance_admin_smes", "growth_services"} and zone["zone_id"] in {
            "core_colombo",
            "admin_professional_belt",
        }:
            weight *= 1.35
        if archetype["sector_id"] in {"construction_contractors", "light_manufacturing", "logistics_services"} and zone["zone_id"] in {
            "east_growth_corridor",
            "outer_commuter_belt",
        }:
            weight *= 1.25
        if archetype["sector_id"] in {"food_service", "retail_trade", "personal_services"} and zone["zone_id"] == "south_west_suburban":
            weight *= 1.15
        weights.append({**zone, "weight": weight})
    return _weighted_choice(rng, weights, weight_field="weight")


def size_class_score(size_band: str) -> float:
    return {"micro": 28, "small": 52, "medium": 74, "large": 86}.get(size_band, 45)


def informality_score(formality: str) -> float:
    return {"informal": 22, "semi_formal": 40, "formal": 72}.get(formality, 45)


def digital_maturity_score(level: str, size_band: str, zone_id: str) -> float:
    base = {"nascent": 26, "emerging": 48, "operational": 70, "advanced": 86}[level]
    return clamp(base + (size_class_score(size_band) * 0.12) + (ZONE_BUSINESS_PREMIUM[zone_id] * 0.6))


def workflow_complexity_score(level: str, sector_id: str) -> float:
    base = {"low": 30, "medium": 56, "high": 78}[level]
    sector_bonus = {
        "healthcare_services": 8,
        "finance_admin_smes": 10,
        "growth_services": 10,
        "construction_contractors": 6,
        "logistics_services": 8,
        "retail_trade": 0,
    }.get(sector_id, 4)
    return clamp(base + sector_bonus)


def owner_sophistication_score(level: str, digital_maturity: float, formality: str) -> float:
    base = {"low": 32, "medium": 58, "high": 80}[level]
    return clamp(base + (digital_maturity * 0.12) + (informality_score(formality) * 0.08))


def customer_interaction_score(level: str, channel_mix: str) -> float:
    base = {"low": 28, "medium": 54, "high": 82}[level]
    return clamp(base + (CHANNEL_MIX_SCORE[channel_mix] * 0.1))


def admin_burden_score(level: str, sector_id: str) -> float:
    base = {"low": 28, "medium": 56, "high": 80}[level]
    sector_bonus = 8 if sector_id in {"healthcare_services", "finance_admin_smes", "professional_services"} else 0
    return clamp(base + sector_bonus)


def data_readiness_score(level: str, digital_maturity: float, channel_mix: str) -> float:
    base = {"low": 24, "medium": 50, "high": 76}[level]
    return clamp(base + (digital_maturity * 0.18) + (CHANNEL_MIX_SCORE[channel_mix] * 0.08))


def staff_intensity_score(level: str) -> float:
    return {"low": 28, "medium": 56, "high": 78}[level]


def payment_cycle_score(level: str, formality: str, sector_id: str) -> float:
    penalty = {"low": 18, "medium": 42, "high": 72}[level]
    if sector_id in {"construction_contractors", "wholesale_distribution"}:
        penalty += 8
    return clamp(penalty - (informality_score(formality) * 0.08))


def procurement_speed_score(level: str, size_band: str) -> float:
    base = {"fast": 78, "medium": 54, "slow": 26}[level]
    return clamp(base - (size_class_score(size_band) * 0.08))


def ability_to_pay_score(base_value: float, zone_id: str, digital_maturity: float) -> float:
    return clamp(base_value + (ZONE_BUSINESS_PREMIUM[zone_id] * 0.8) + (digital_maturity * 0.12))


def roi_tolerance_score(level: str, owner_sophistication: float) -> float:
    base = {"low": 32, "medium": 56, "high": 80}[level]
    return clamp(base + (owner_sophistication * 0.1))


def sales_cycle_length(procurement_speed: float, size_band: str, formality: str) -> float:
    return clamp(100 - procurement_speed + (size_class_score(size_band) * 0.15) + (informality_score(formality) * 0.05))


def channel_reachability_score(channel_mix: str, owner_sophistication: float, zone_id: str) -> float:
    return clamp((CHANNEL_MIX_SCORE[channel_mix] * 0.55) + (owner_sophistication * 0.25) + (ZONE_BUSINESS_PREMIUM[zone_id] + 50) * 0.2)


def substitute_pressure_score(level: str, sector_id: str, zone_id: str) -> float:
    base = {"low": 28, "medium": 52, "high": 74}[level]
    if sector_id in {"retail_trade", "food_service", "personal_services"}:
        base += 8
    return clamp(base + max(0, ZONE_BUSINESS_PREMIUM[zone_id]))


def expansion_potential_score(
    ability_to_pay: float, digital_maturity: float, customer_interaction: float, size_band: str
) -> float:
    return clamp((ability_to_pay * 0.28) + (digital_maturity * 0.28) + (customer_interaction * 0.2) + (size_class_score(size_band) * 0.24))


def pain_map_for_firm(sector_id: str, staff_intensity: float, customer_interaction: float, admin_burden: float) -> dict[str, float]:
    baseline = {
        "customer_support": customer_interaction,
        "document_admin": admin_burden,
        "sales_marketing": 44,
        "collections": 42,
        "ops_scheduling": staff_intensity,
        "hr_internal": staff_intensity * 0.72,
        "analytics": admin_burden * 0.75,
        "training": staff_intensity * 0.65,
    }
    sector_adjustments = {
        "retail_trade": {"sales_marketing": 18, "customer_support": 8, "collections": 6},
        "food_service": {"customer_support": 10, "ops_scheduling": 8, "sales_marketing": 10},
        "logistics_services": {"ops_scheduling": 18, "collections": 10, "analytics": 8},
        "healthcare_services": {"document_admin": 16, "customer_support": 8, "analytics": 8},
        "education_services": {"training": 12, "customer_support": 8, "sales_marketing": 8},
        "personal_services": {"sales_marketing": 12, "customer_support": 10},
        "real_estate_services": {"sales_marketing": 16, "customer_support": 10, "collections": 8},
        "professional_services": {"document_admin": 12, "analytics": 12, "hr_internal": 8},
        "wholesale_distribution": {"collections": 16, "ops_scheduling": 12, "analytics": 8},
        "light_manufacturing": {"ops_scheduling": 16, "document_admin": 8, "training": 8},
        "tourism_hospitality": {"customer_support": 16, "sales_marketing": 10},
        "construction_contractors": {"ops_scheduling": 16, "collections": 12, "document_admin": 8},
        "finance_admin_smes": {"document_admin": 18, "analytics": 16, "hr_internal": 10},
        "growth_services": {"sales_marketing": 10, "analytics": 14, "customer_support": 8},
    }.get(sector_id, {})
    return {field: clamp(baseline[field] + sector_adjustments.get(field, 0)) for field in PAIN_FIELDS}


def assign_b2b_segment_v2(firm: dict) -> str:
    sector = firm["sector_id"]
    size = firm["size_band"]
    if sector in {"retail_trade", "food_service", "personal_services"} and size == "micro":
        return "b2b_frontline_micro_operators"
    if sector in {"retail_trade", "food_service", "tourism_hospitality"}:
        return "b2b_consumer_service_smes"
    if sector in {"logistics_services", "construction_contractors", "wholesale_distribution"}:
        return "b2b_field_and_flow_operators"
    if sector in {"healthcare_services", "education_services"}:
        return "b2b_service_admin_clusters"
    if sector in {"professional_services", "finance_admin_smes", "growth_services"}:
        return "b2b_knowledge_and_admin_smes"
    if sector == "light_manufacturing":
        return "b2b_workshop_manufacturing"
    return "b2b_general_local_smes"


SEGMENT_LABELS_V2 = {
    "b2b_frontline_micro_operators": "Frontline micro operators",
    "b2b_consumer_service_smes": "Consumer-service SMEs",
    "b2b_field_and_flow_operators": "Field and flow operators",
    "b2b_service_admin_clusters": "Service admin clusters",
    "b2b_knowledge_and_admin_smes": "Knowledge and admin SMEs",
    "b2b_workshop_manufacturing": "Workshop manufacturing",
    "b2b_general_local_smes": "General local SMEs",
}


def summarize_b2b_segments_v2(firms: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    total_firms = len(firms)
    for firm in firms:
        grouped[firm["market_segment_id"]].append(firm)

    summaries: list[dict] = []
    for segment_id, rows in grouped.items():
        sector_mix = Counter(row["sector_id"] for row in rows)
        zones = Counter(row["zone_id"] for row in rows)
        summary = {
            "segment_id": segment_id,
            "segment_label": SEGMENT_LABELS_V2[segment_id],
            "firm_count": len(rows),
            "firm_share": round(len(rows) / total_firms, 6),
            "avg_ability_to_pay": round(sum(row["ability_to_pay_score"] for row in rows) / len(rows), 2),
            "avg_digital_maturity": round(sum(row["digital_maturity_score"] for row in rows) / len(rows), 2),
            "avg_workflow_complexity": round(sum(row["workflow_complexity_score"] for row in rows) / len(rows), 2),
            "avg_owner_sophistication": round(sum(row["owner_sophistication_score"] for row in rows) / len(rows), 2),
            "avg_customer_interaction": round(sum(row["customer_interaction_score"] for row in rows) / len(rows), 2),
            "avg_admin_burden": round(sum(row["admin_burden_score"] for row in rows) / len(rows), 2),
            "avg_data_readiness": round(sum(row["data_readiness_score"] for row in rows) / len(rows), 2),
            "avg_payment_cycle_friction": round(sum(row["payment_cycle_friction_score"] for row in rows) / len(rows), 2),
            "avg_procurement_speed": round(sum(row["procurement_speed_score"] for row in rows) / len(rows), 2),
            "avg_roi_tolerance": round(sum(row["roi_tolerance_score"] for row in rows) / len(rows), 2),
            "avg_sales_cycle_length": round(sum(row["sales_cycle_length_score"] for row in rows) / len(rows), 2),
            "avg_channel_reachability": round(sum(row["channel_reachability_score"] for row in rows) / len(rows), 2),
            "avg_substitute_pressure": round(sum(row["substitute_pressure_score"] for row in rows) / len(rows), 2),
            "avg_expansion_potential": round(sum(row["expansion_potential_score"] for row in rows) / len(rows), 2),
            "dominant_sector": sector_mix.most_common(1)[0][0],
            "dominant_zones": "|".join(zone for zone, _ in zones.most_common(2)),
        }
        for field in PAIN_FIELDS:
            summary[f"avg_pain_{field}"] = round(sum(row["pain_scores"][field] for row in rows) / len(rows), 2)
        summaries.append(summary)

    return sorted(summaries, key=lambda item: (-item["firm_share"], item["segment_id"]))


@dataclass(frozen=True)
class Prompt03B2BConfig:
    seed: int
    target_firms: int
    geography_scope: str = "LK-11"
