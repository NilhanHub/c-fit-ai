"""Build Prompt #03 person records from Colombo household archetypes."""

from __future__ import annotations

from random import Random

from population.b2c_budget_model import derive_budget_headroom
from population.b2c_channel_reachability import derive_consumer_channel_reachability
from population.b2c_conversion_friction import derive_conversion_friction
from population.b2c_device_connectivity import derive_device_connectivity
from population.b2c_digital_readiness import derive_digital_readiness
from population.b2c_language_model import infer_language_preference
from population.b2c_lifestage_triggers import derive_lifestage_triggers
from population.b2c_mobility_model import derive_mobility_access
from population.b2c_need_intensity import derive_need_intensities
from population.b2c_payment_readiness import derive_payment_readiness
from population.b2c_problem_frequency import derive_problem_frequency
from population.b2c_referral_model import derive_referral_potential
from population.b2c_retention_model import derive_retention_potential
from population.b2c_substitutes import derive_substitute_pressure
from population.b2c_trust_model import derive_trust_openness
from population.b2c_urgency import derive_domain_urgency
from population.prompt03_b2c_core import RETRIEVED_AT_PROMPT03, assign_b2c_segment_v2


def _adult_age_band(rng: Random, employment_profile: str) -> str:
    if employment_profile in {"formal_dual_income", "service_plus_side_income"}:
        return rng.choices(["25-34", "35-44", "45-54"], weights=[0.36, 0.42, 0.22], k=1)[0]
    if employment_profile == "informal_precarious":
        return rng.choices(["15-24", "25-34", "35-44", "45-54"], weights=[0.14, 0.42, 0.28, 0.16], k=1)[0]
    return rng.choices(["25-34", "35-44", "45-54", "55-64"], weights=[0.28, 0.32, 0.24, 0.16], k=1)[0]


def _role(adult_index: int, household: dict) -> str:
    if household["archetype_id"] == "female_led_microcommerce" and adult_index == 0:
        return "microbusiness_operator"
    if adult_index == 0:
        return "primary_earner"
    if household["children"] > 0 and adult_index == 1:
        return "parent"
    if household["elders"] > 0 and adult_index == 1:
        return "caregiver"
    return "secondary_earner"


def _employment_status(age_band: str, household: dict, role: str) -> str:
    if age_band == "0-14":
        return "student"
    if age_band == "15-24":
        if "exam" in household["lifestage_focus"] or household["need_education"] >= 80:
            return "student"
        return "entry_worker"
    if role == "microbusiness_operator":
        return "self_employed"
    if household["employment_profile"] == "informal_precarious":
        return "informal_worker"
    if role == "caregiver":
        return "caregiver"
    if household["employment_profile"] == "retirement_plus_support":
        return "retired"
    return "salaried_worker"


def _education_band(age_band: str, education_anchor: str, role: str) -> str:
    if age_band == "0-14":
        return "school"
    if age_band == "15-24":
        return "upper_secondary" if education_anchor == "secondary" else "tertiary_or_diploma"
    if role == "elder":
        return "secondary"
    mapping = {
        "degree_plus": "degree_or_higher",
        "tertiary_track": "tertiary_or_diploma",
        "tertiary_or_diploma": "tertiary_or_diploma",
        "upper_secondary_plus": "upper_secondary",
        "secondary": "secondary",
    }
    return mapping.get(education_anchor, "secondary")


def build_b2c_people_v2(households: list[dict], seed: int) -> list[dict]:
    rng = Random(seed + 303)
    people: list[dict] = []
    for household in households:
        counter = 0
        adults_without_elders = household["adults"] - household["elders"]
        for adult_index in range(adults_without_elders):
            age_band = _adult_age_band(rng, household["employment_profile"])
            role = _role(adult_index, household)
            person = _build_person_record(household, age_band, role, counter, rng)
            people.append(person)
            counter += 1
        for child_index in range(household["children"]):
            age_band = "15-24" if child_index == household["children"] - 1 and household["children"] > 1 else "0-14"
            person = _build_person_record(household, age_band, "student", counter, rng)
            people.append(person)
            counter += 1
        for _elder in range(household["elders"]):
            person = _build_person_record(household, "65+", "elder", counter, rng)
            people.append(person)
            counter += 1
    return people


def _build_person_record(household: dict, age_band: str, role: str, counter: int, rng: Random) -> dict:
    language_preference = infer_language_preference(household["language_profile"], age_band, rng)
    trust_openness = derive_trust_openness(household["trust_skepticism"], household["education_anchor"], household["zone_id"])
    digital_readiness = derive_digital_readiness(
        household["smartphone_access"],
        household["internet_access"],
        household["payment_readiness"],
        household["education_anchor"],
        household["zone_id"],
    )
    device_connectivity = derive_device_connectivity(household["smartphone_access"], household["internet_access"])
    payment_score = derive_payment_readiness(household["payment_readiness"], household["budget_tightness"])
    mobility_score = derive_mobility_access(household["mobility_profile"], household["zone_id"])
    budget_headroom = derive_budget_headroom(
        household["income_band"], household["budget_tightness"], household["zone_id"], household["discretionary_spend"]
    )
    need_scores = derive_need_intensities(household, household["zone_id"])
    if role == "microbusiness_operator":
        need_scores["commerce"] = min(100.0, need_scores["commerce"] + 8)
        need_scores["finance"] = min(100.0, need_scores["finance"] + 8)
    if role in {"parent", "caregiver"}:
        need_scores["family_admin"] = min(100.0, need_scores["family_admin"] + 10)
        need_scores["healthcare"] = min(100.0, need_scores["healthcare"] + 6)
    if age_band == "15-24":
        need_scores["education"] = min(100.0, need_scores["education"] + 8)
        need_scores["jobs"] = min(100.0, need_scores["jobs"] + 6)
    urgency_scores = derive_domain_urgency(need_scores, trust_openness, budget_headroom)
    frequency_scores = derive_problem_frequency(need_scores, mobility_score)
    triggers = derive_lifestage_triggers(household)
    channel_reachability = derive_consumer_channel_reachability(digital_readiness, mobility_score, trust_openness)
    conversion_friction = derive_conversion_friction(digital_readiness, trust_openness, payment_score)
    retention_score = derive_retention_potential(need_scores, frequency_scores, budget_headroom)
    referral_score = derive_referral_potential(digital_readiness, trust_openness, triggers)
    substitute_pressure = derive_substitute_pressure(household["zone_id"], digital_readiness, household["income_band"])

    person = {
        "person_id": f"person-{household['household_id'].split('-')[-1]}-{counter + 1:02d}",
        "household_id": household["household_id"],
        "geo_id": household["geo_id"],
        "zone_id": household["zone_id"],
        "zone_label": household["zone_label"],
        "claim_type": "INFERENCE",
        "retrieved_at": RETRIEVED_AT_PROMPT03,
        "evidence_refs": household["evidence_refs"],
        "age_band": age_band,
        "gender": rng.choices(["female", "male"], weights=[0.51, 0.49], k=1)[0],
        "role_in_household": role,
        "education_band": _education_band(age_band, household["education_anchor"], role),
        "employment_status": _employment_status(age_band, household, role),
        "language_preference": language_preference,
        "budget_headroom_score": budget_headroom,
        "trust_openness_score": trust_openness,
        "digital_readiness_score": digital_readiness,
        "device_connectivity_profile": device_connectivity["profile"],
        "device_connectivity_score": device_connectivity["score"],
        "payment_readiness_score": payment_score,
        "mobility_access_score": mobility_score,
        "need_scores": need_scores,
        "urgency_scores": urgency_scores,
        "frequency_scores": frequency_scores,
        "lifestage_triggers": triggers,
        "channel_reachability": channel_reachability,
        "best_channel_reachability": max(channel_reachability.values()),
        "conversion_friction_score": conversion_friction,
        "retention_potential_score": retention_score,
        "referral_potential_score": referral_score,
        "substitute_pressure": substitute_pressure,
        "income_band": household["income_band"],
        "area_cluster": household["zone_id"],
    }
    person["market_segment_id"] = assign_b2c_segment_v2(person)
    return person
