"""Core Prompt #03 B2C helpers shared across the commercial v2 population modules."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from random import Random

from population.seed_tables import load_ds_populations_v2, load_household_archetypes_v2, load_zone_map_v1


RETRIEVED_AT_PROMPT03 = "2026-03-17T03:45:00Z"
DOMAIN_FIELDS = (
    "jobs",
    "education",
    "healthcare",
    "commerce",
    "housing",
    "mobility",
    "productivity",
    "finance",
    "family_admin",
)

INCOME_MIDPOINTS = {
    "50000-74999": 62500,
    "75000-99999": 87500,
    "100000-149999": 125000,
    "150000-249999": 200000,
    "250000_plus": 275000,
}

EDUCATION_SCORES = {
    "secondary": 38,
    "upper_secondary": 52,
    "upper_secondary_plus": 58,
    "tertiary_or_diploma": 68,
    "tertiary_track": 64,
    "degree_plus": 82,
}

EMPLOYMENT_PREMIUM = {
    "formal_dual_income": 20,
    "mixed_wage": 8,
    "informal_precarious": -12,
    "self_employed_micro": -6,
    "retirement_plus_support": -16,
    "service_single_income": 0,
    "service_plus_side_income": 6,
}

ZONE_INCOME_PREMIUM = {
    "core_colombo": 10,
    "admin_professional_belt": 14,
    "east_growth_corridor": 0,
    "south_west_suburban": -2,
    "outer_commuter_belt": -8,
}

ZONE_REACHABILITY = {
    "core_colombo": 80,
    "admin_professional_belt": 72,
    "east_growth_corridor": 63,
    "south_west_suburban": 66,
    "outer_commuter_belt": 54,
}

ZONE_SUBSTITUTE_PRESSURE = {
    "core_colombo": 72,
    "admin_professional_belt": 66,
    "east_growth_corridor": 56,
    "south_west_suburban": 62,
    "outer_commuter_belt": 44,
}


def _weighted_choice(rng: Random, rows: list[dict], weight_field: str = "weight") -> dict:
    return rng.choices(rows, weights=[row[weight_field] for row in rows], k=1)[0]


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return round(max(low, min(high, value)), 2)


def load_zone_catalog() -> list[dict]:
    ds_rows = load_ds_populations_v2()
    zone_map = load_zone_map_v1()
    ds_by_name = {row["ds_division"]: row for row in ds_rows}
    totals: dict[str, int] = defaultdict(int)
    zone_rows: list[dict] = []
    for mapping in zone_map:
        population = ds_by_name[mapping["ds_division"]]["population_2024"]
        totals[mapping["zone_id"]] += population
        zone_rows.append({**mapping, "population_2024": population})

    district_total = sum(row["population_2024"] for row in zone_rows)
    summary: list[dict] = []
    for zone_id, population in totals.items():
        representative = next(row for row in zone_rows if row["zone_id"] == zone_id)
        summary.append(
            {
                "zone_id": zone_id,
                "zone_label": representative["zone_label"],
                "zone_type": representative["zone_type"],
                "population_2024": population,
                "population_share": round(population / district_total, 6),
                "commuter_role": representative["commuter_role"],
                "evidence_refs": representative["evidence_refs"],
            }
        )
    return sorted(summary, key=lambda item: (-item["population_share"], item["zone_id"]))


def zone_lookup() -> dict[str, dict]:
    return {row["zone_id"]: row for row in load_zone_catalog()}


def zone_distribution() -> list[dict]:
    return [
        {"zone_id": row["zone_id"], "weight": row["population_share"], "zone_label": row["zone_label"]}
        for row in load_zone_catalog()
    ]


def household_archetypes_v2() -> list[dict]:
    return load_household_archetypes_v2()


def pick_zone_for_archetype(rng: Random, archetype: dict) -> dict:
    candidates = [item for item in zone_distribution() if item["zone_id"] in archetype["preferred_zones"].split("|")]
    if not candidates:
        candidates = zone_distribution()
    return _weighted_choice(rng, candidates)


def budget_headroom_score(income_band: str, budget_tightness: str, zone_id: str, discretionary_spend: str) -> float:
    base = {
        "very_high": 20,
        "high": 36,
        "medium": 58,
        "low": 82,
    }[budget_tightness]
    discretionary = {"very_low": -10, "low": -4, "medium": 4, "high": 12}[discretionary_spend]
    income_boost = (INCOME_MIDPOINTS[income_band] / 4000) / 10
    return clamp(base + discretionary + income_boost + (ZONE_INCOME_PREMIUM[zone_id] * 0.25))


def trust_openness_score(trust_skepticism: str, education_anchor: str, zone_id: str) -> float:
    skepticism_penalty = {"high": 36, "medium": 20, "low": 8}[trust_skepticism]
    education_bonus = EDUCATION_SCORES[education_anchor] * 0.25
    return clamp(100 - skepticism_penalty + education_bonus + (ZONE_REACHABILITY[zone_id] * 0.08))


def digital_readiness_score(
    smartphone_access: str, internet_access: str, payment_readiness: str, education_anchor: str, zone_id: str
) -> float:
    device_score = 30 if smartphone_access == "shared" else 55
    internet_score = 22 if internet_access == "mobile_only" else 38
    payment_bonus = {"cash_only": 4, "mixed": 12, "digital_ready": 20}[payment_readiness]
    return clamp(device_score + internet_score + payment_bonus + (EDUCATION_SCORES[education_anchor] * 0.18) + (ZONE_REACHABILITY[zone_id] * 0.08))


def device_connectivity_profile(smartphone_access: str, internet_access: str) -> dict[str, float | str]:
    if smartphone_access == "personal" and internet_access == "fixed_and_mobile":
        return {"profile": "always_on", "score": 88}
    if smartphone_access == "personal":
        return {"profile": "mobile_primary", "score": 68}
    if internet_access == "fixed_and_mobile":
        return {"profile": "shared_fixed_access", "score": 56}
    return {"profile": "shared_mobile_constraint", "score": 42}


def payment_readiness_score(payment_readiness: str, budget_tightness: str) -> float:
    base = {"cash_only": 28, "mixed": 56, "digital_ready": 82}[payment_readiness]
    budget_penalty = {"very_high": 8, "high": 4, "medium": 0, "low": -2}[budget_tightness]
    return clamp(base - budget_penalty)


def mobility_access_score(mobility_profile: str, zone_id: str) -> float:
    base = {
        "car_and_transit": 82,
        "transit_heavy": 72,
        "bus_commuter": 58,
        "commute_heavy": 48,
        "local_radius": 62,
        "bus_and_walk": 44,
        "caregiver_bound": 30,
    }[mobility_profile]
    return clamp(base + (ZONE_REACHABILITY[zone_id] * 0.15))


def lifestage_trigger_list(archetype: dict) -> list[str]:
    focus = archetype["lifestage_focus"]
    trigger_map = {
        "career_progression": ["career_switch", "upskilling", "productivity_upgrade"],
        "schooling_and_bills": ["school_admin", "budget_pressure", "commute_coordination"],
        "income_stability": ["job_search", "collections", "family_budgeting"],
        "microbusiness_growth": ["lead_generation", "collections", "inventory_tracking"],
        "exam_and_upskilling": ["exam_preparation", "career_search", "peer_learning"],
        "care_and_admin": ["medical_admin", "care_coordination", "household_support"],
        "productivity_and_services": ["workflow_optimization", "service_discovery", "premium_support"],
        "rent_and_job_switch": ["rental_search", "job_search", "mobility_planning"],
        "commute_and_bills": ["route_planning", "bill_management", "income_support"],
        "education_and_family_admin": ["tutoring", "family_coordination", "education_financing"],
    }
    return trigger_map.get(focus, ["family_admin"])


def need_intensity_map(archetype: dict, zone_id: str) -> dict[str, float]:
    zone_adjust = {
        "core_colombo": {"housing": 8, "productivity": 8, "commerce": 4},
        "admin_professional_belt": {"education": 6, "productivity": 8, "finance": 4},
        "east_growth_corridor": {"jobs": 5, "mobility": 6, "commerce": 4},
        "south_west_suburban": {"family_admin": 5, "mobility": 4, "healthcare": 4},
        "outer_commuter_belt": {"jobs": 7, "mobility": 10, "finance": 6},
    }[zone_id]
    scores = {}
    for domain in DOMAIN_FIELDS:
        scores[domain] = clamp(archetype[f"need_{domain}"] + zone_adjust.get(domain, 0))
    return scores


def urgency_from_need(need_scores: dict[str, float], trust_openness: float, budget_headroom: float) -> dict[str, float]:
    urgency = {}
    for domain, score in need_scores.items():
        modifier = 0.0
        if domain in {"jobs", "finance", "housing"}:
            modifier += max(0.0, 58 - budget_headroom) * 0.2
        if domain in {"healthcare", "family_admin"}:
            modifier += max(0.0, 62 - trust_openness) * 0.08
        urgency[domain] = clamp((score * 0.72) + modifier + 10)
    return urgency


def frequency_from_need(need_scores: dict[str, float], mobility_score: float) -> dict[str, float]:
    frequency = {}
    for domain, score in need_scores.items():
        modifier = 0.0
        if domain in {"mobility", "family_admin", "finance"}:
            modifier += max(0.0, 60 - mobility_score) * 0.2
        frequency[domain] = clamp((score * 0.62) + modifier + 16)
    return frequency


def channel_reachability(channel_modes: list[str], digital_readiness: float, mobility_score: float, trust_openness: float) -> dict[str, float]:
    catalog = {
        "self_serve_app": clamp((digital_readiness * 0.6) + (trust_openness * 0.25) + 10),
        "inside_sales": clamp((digital_readiness * 0.35) + (trust_openness * 0.25) + (mobility_score * 0.2) + 15),
        "whatsapp_led": clamp((digital_readiness * 0.52) + (trust_openness * 0.22) + 12),
        "field_sales": clamp((mobility_score * 0.55) + (trust_openness * 0.15) + 18),
        "partner_led": clamp((trust_openness * 0.35) + (mobility_score * 0.25) + 22),
    }
    return {mode: catalog[mode] for mode in channel_modes if mode in catalog}


def conversion_friction_score(digital_readiness: float, trust_openness: float, payment_readiness: float) -> float:
    return clamp(100 - ((digital_readiness * 0.35) + (trust_openness * 0.35) + (payment_readiness * 0.3)))


def retention_potential(need_scores: dict[str, float], frequency_scores: dict[str, float], budget_headroom: float) -> float:
    top_need = max(need_scores.values())
    top_frequency = max(frequency_scores.values())
    return clamp((top_need * 0.42) + (top_frequency * 0.38) + (budget_headroom * 0.2))


def referral_potential(digital_readiness: float, trust_openness: float, top_triggers: list[str]) -> float:
    trigger_bonus = 10 if {"exam_preparation", "career_search", "lead_generation"} & set(top_triggers) else 4
    return clamp((digital_readiness * 0.45) + (trust_openness * 0.35) + trigger_bonus)


def substitute_pressure(zone_id: str, digital_readiness: float, income_band: str) -> dict[str, float]:
    base = ZONE_SUBSTITUTE_PRESSURE[zone_id]
    income_adjust = min(10.0, INCOME_MIDPOINTS[income_band] / 30000)
    return {domain: clamp(base + income_adjust + (digital_readiness * 0.1)) for domain in DOMAIN_FIELDS}


def assign_b2c_segment_v2(person: dict) -> str:
    needs = person["need_scores"]
    triggers = set(person["lifestage_triggers"])
    if person["age_band"] == "15-24" and max(needs["education"], needs["jobs"]) >= 74:
        return "b2c_youth_upskilling_renters"
    if "lead_generation" in triggers or needs["commerce"] >= 76:
        return "b2c_microcommerce_strivers"
    if person["budget_headroom_score"] <= 36 and needs["mobility"] >= 58:
        return "b2c_budget_stretched_commuters"
    if person["role_in_household"] in {"caregiver", "elder"} or needs["healthcare"] >= 82:
        return "b2c_care_navigation_households"
    if person["budget_headroom_score"] >= 72 and needs["productivity"] >= 70:
        return "b2c_affluent_service_optimizers"
    if person["zone_id"] == "outer_commuter_belt" and needs["jobs"] >= 70:
        return "b2c_outer_belt_income_makers"
    if needs["education"] >= 72 and needs["family_admin"] >= 66:
        return "b2c_education_intensive_families"
    return "b2c_everyday_utility_seekers"


SEGMENT_LABELS_V2 = {
    "b2c_youth_upskilling_renters": "Youth upskilling renters",
    "b2c_microcommerce_strivers": "Microcommerce strivers",
    "b2c_budget_stretched_commuters": "Budget-stretched commuters",
    "b2c_care_navigation_households": "Care navigation households",
    "b2c_affluent_service_optimizers": "Affluent service optimizers",
    "b2c_outer_belt_income_makers": "Outer-belt income makers",
    "b2c_education_intensive_families": "Education-intensive families",
    "b2c_everyday_utility_seekers": "Everyday utility seekers",
}


def summarize_b2c_segments_v2(people: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    total_people = len(people)
    for person in people:
        grouped[person["market_segment_id"]].append(person)

    summaries: list[dict] = []
    for segment_id, rows in grouped.items():
        languages = Counter(row["language_preference"] for row in rows)
        zones = Counter(row["zone_id"] for row in rows)
        top_triggers = Counter(trigger for row in rows for trigger in row["lifestage_triggers"])
        summary = {
            "segment_id": segment_id,
            "segment_label": SEGMENT_LABELS_V2[segment_id],
            "population_count": len(rows),
            "population_share": round(len(rows) / total_people, 6),
            "avg_budget_headroom": round(sum(row["budget_headroom_score"] for row in rows) / len(rows), 2),
            "avg_trust_openness": round(sum(row["trust_openness_score"] for row in rows) / len(rows), 2),
            "avg_digital_readiness": round(sum(row["digital_readiness_score"] for row in rows) / len(rows), 2),
            "avg_device_connectivity": round(sum(row["device_connectivity_score"] for row in rows) / len(rows), 2),
            "avg_payment_readiness": round(sum(row["payment_readiness_score"] for row in rows) / len(rows), 2),
            "avg_mobility_access": round(sum(row["mobility_access_score"] for row in rows) / len(rows), 2),
            "avg_channel_reachability": round(sum(row["best_channel_reachability"] for row in rows) / len(rows), 2),
            "avg_conversion_friction": round(sum(row["conversion_friction_score"] for row in rows) / len(rows), 2),
            "avg_retention_potential": round(sum(row["retention_potential_score"] for row in rows) / len(rows), 2),
            "avg_referral_potential": round(sum(row["referral_potential_score"] for row in rows) / len(rows), 2),
            "top_languages": "|".join(language for language, _ in languages.most_common(3)),
            "dominant_zones": "|".join(zone for zone, _ in zones.most_common(2)),
            "top_triggers": "|".join(trigger for trigger, _ in top_triggers.most_common(3)),
        }
        for domain in DOMAIN_FIELDS:
            summary[f"avg_need_{domain}"] = round(sum(row["need_scores"][domain] for row in rows) / len(rows), 2)
            summary[f"avg_urgency_{domain}"] = round(sum(row["urgency_scores"][domain] for row in rows) / len(rows), 2)
            summary[f"avg_frequency_{domain}"] = round(sum(row["frequency_scores"][domain] for row in rows) / len(rows), 2)
            summary[f"avg_substitute_pressure_{domain}"] = round(
                sum(row["substitute_pressure"][domain] for row in rows) / len(rows), 2
            )
        summaries.append(summary)

    return sorted(summaries, key=lambda item: (-item["population_share"], item["segment_id"]))


@dataclass(frozen=True)
class Prompt03B2CConfig:
    seed: int
    target_households: int
    geography_scope: str = "LK-11"
