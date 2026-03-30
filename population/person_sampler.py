"""Generate person-level records from sampled Colombo households."""

from __future__ import annotations

from random import Random

from population.segment_taxonomy import assign_b2c_segment


RETRIEVED_AT = "2026-03-16T18:30:00Z"
_GENDER_WEIGHTS = {"female": 0.51, "male": 0.49}


def _weighted_choice(rng: Random, pairs: list[tuple[str, float]]) -> str:
    values = [item[0] for item in pairs]
    weights = [item[1] for item in pairs]
    return rng.choices(values, weights=weights, k=1)[0]


def _adult_age_band(rng: Random, profile: str) -> str:
    if profile == "professional_dual":
        return _weighted_choice(rng, [("25-34", 0.35), ("35-44", 0.4), ("45-54", 0.2), ("55-64", 0.05)])
    if profile == "informal_precarious":
        return _weighted_choice(rng, [("15-24", 0.15), ("25-34", 0.4), ("35-44", 0.25), ("45-54", 0.15), ("55-64", 0.05)])
    return _weighted_choice(rng, [("25-34", 0.32), ("35-44", 0.3), ("45-54", 0.2), ("55-64", 0.12), ("15-24", 0.06)])


def _assign_role(adult_index: int, household: dict) -> str:
    if household["archetype_id"] == "female_led_microcommerce" and adult_index == 0:
        return "microbusiness_operator"
    if adult_index == 0:
        return "primary_earner"
    if household["elders_count"] > 0 and adult_index == 1:
        return "caregiver"
    if household["composition"]["children"] > 0 and adult_index == 1:
        return "parent"
    return "secondary_earner"


def _education_band(age_band: str, anchor: str, role: str) -> str:
    if age_band == "0-14":
        return "school"
    if age_band == "15-24":
        return "upper_secondary" if "lower_secondary" in anchor else "tertiary_or_diploma"
    if role == "elder":
        return "secondary"
    return {
        "degree_plus": "degree_or_higher",
        "tertiary_track": "tertiary_or_diploma",
        "tertiary_or_diploma": "tertiary_or_diploma",
        "upper_secondary_plus": "upper_secondary",
        "secondary": "secondary",
        "lower_secondary": "lower_secondary",
        "mixed": "upper_secondary",
    }.get(anchor, "secondary")


def _employment_status(age_band: str, profile: str, role: str) -> str:
    if age_band == "0-14":
        return "child"
    if age_band == "15-24":
        return "student" if "student" in profile or role == "student" else "entry_level_worker"
    if role == "elder":
        return "retired"
    if role == "caregiver":
        return "caregiver"
    if role == "microbusiness_operator":
        return "self_employed"
    if profile == "informal_precarious":
        return "informal_worker"
    if profile == "mixed_wage":
        return "underemployed"
    return "salaried_worker"


def _adoption_posture(smartphone_access: str, internet_access: str, trust_sensitivity: str) -> str:
    if smartphone_access == "personal" and internet_access == "fixed_and_mobile" and trust_sensitivity == "low":
        return "early_adopter"
    if smartphone_access == "personal":
        return "early_majority"
    if trust_sensitivity == "high":
        return "late_majority"
    return "early_majority"


def _language_preference(language_profile: str, rng: Random) -> str:
    if language_profile == "si_en":
        return _weighted_choice(rng, [("si", 0.55), ("si_en", 0.45)])
    if language_profile == "si_ta_en":
        return _weighted_choice(rng, [("si_en", 0.45), ("ta_en", 0.25), ("si", 0.2), ("ta", 0.1)])
    if language_profile == "si_ta":
        return _weighted_choice(rng, [("si", 0.6), ("ta", 0.25), ("si_en", 0.15)])
    if language_profile == "en_si":
        return _weighted_choice(rng, [("en", 0.4), ("si_en", 0.45), ("si", 0.15)])
    return language_profile


def _adjust_needs(base_needs: dict, role: str, age_band: str) -> dict:
    needs = dict(base_needs)
    if role == "microbusiness_operator":
        needs["commerce"] = min(100, needs["commerce"] + 10)
        needs["finance"] = min(100, needs["finance"] + 8)
        needs["productivity"] = min(100, needs["productivity"] + 8)
    if role in {"parent", "caregiver"}:
        needs["family_admin"] = min(100, needs["family_admin"] + 8)
        needs["healthcare"] = min(100, needs["healthcare"] + 6)
    if age_band == "15-24":
        needs["education"] = min(100, needs["education"] + 10)
        needs["jobs"] = min(100, needs["jobs"] + 8)
    if role == "elder":
        needs["healthcare"] = min(100, needs["healthcare"] + 10)
        needs["mobility"] = max(0, needs["mobility"] - 10)
    return needs


def sample_people(households: list[dict], seed: int) -> list[dict]:
    rng = Random(seed + 101)
    people: list[dict] = []

    for household in households:
        person_counter = 0

        for adult_index in range(household["composition"]["adults"] - household["elders_count"]):
            age_band = _adult_age_band(rng, household["employment_profile"])
            role = _assign_role(adult_index, household)
            person = {
                "person_id": f"person-{household['household_id'].split('-')[-1]}-{person_counter + 1:02d}",
                "household_id": household["household_id"],
                "geo_id": household["geo_id"],
                "claim_type": "INFERENCE",
                "retrieved_at": RETRIEVED_AT,
                "evidence_refs": household["evidence_refs"],
                "demographics": {
                    "age_band": age_band,
                    "gender": _weighted_choice(rng, list(_GENDER_WEIGHTS.items())),
                },
                "economics": {"income_band_lkr_monthly": household["economics"]["income_band_lkr_monthly"]},
                "digital": {
                    "smartphone_access": household["smartphone_access"],
                    "internet_access": household["internet_access"],
                },
                "behavioral": {
                    "adoption_posture": _adoption_posture(
                        household["smartphone_access"], household["internet_access"], household["trust_sensitivity"]
                    )
                },
                "role_in_household": role,
                "education_band": _education_band(age_band, household["education_anchor"], role),
                "employment_status": _employment_status(age_band, household["employment_profile"], role),
                "language_preference": _language_preference(household["language_profile"], rng),
                "payment_readiness": household["digital_context"]["payment_readiness"],
                "mobility_profile": household["mobility_profile"],
                "budget_sensitivity": household["budget_sensitivity"],
                "trust_sensitivity": household["trust_sensitivity"],
                "area_cluster": household["area_cluster"],
                "need_domain_scores": _adjust_needs(household["need_domain_scores"], role, age_band),
            }
            person["market_segment_id"] = assign_b2c_segment(person)
            people.append(person)
            person_counter += 1

        for child_index in range(household["composition"]["children"]):
            age_band = "15-24" if child_index == household["composition"]["children"] - 1 and household["composition"]["children"] > 1 else "0-14"
            role = "student"
            person = {
                "person_id": f"person-{household['household_id'].split('-')[-1]}-{person_counter + 1:02d}",
                "household_id": household["household_id"],
                "geo_id": household["geo_id"],
                "claim_type": "INFERENCE",
                "retrieved_at": RETRIEVED_AT,
                "evidence_refs": household["evidence_refs"],
                "demographics": {
                    "age_band": age_band,
                    "gender": _weighted_choice(rng, list(_GENDER_WEIGHTS.items())),
                },
                "economics": {"income_band_lkr_monthly": household["economics"]["income_band_lkr_monthly"]},
                "digital": {
                    "smartphone_access": "shared" if age_band == "0-14" else household["smartphone_access"],
                    "internet_access": household["internet_access"],
                },
                "behavioral": {
                    "adoption_posture": _adoption_posture(
                        "shared" if age_band == "0-14" else household["smartphone_access"],
                        household["internet_access"],
                        household["trust_sensitivity"],
                    )
                },
                "role_in_household": role,
                "education_band": _education_band(age_band, household["education_anchor"], role),
                "employment_status": _employment_status(age_band, household["employment_profile"], role),
                "language_preference": _language_preference(household["language_profile"], rng),
                "payment_readiness": household["digital_context"]["payment_readiness"],
                "mobility_profile": household["mobility_profile"],
                "budget_sensitivity": household["budget_sensitivity"],
                "trust_sensitivity": household["trust_sensitivity"],
                "area_cluster": household["area_cluster"],
                "need_domain_scores": _adjust_needs(household["need_domain_scores"], role, age_band),
            }
            person["market_segment_id"] = assign_b2c_segment(person)
            people.append(person)
            person_counter += 1

        for _elder_index in range(household["elders_count"]):
            role = "elder"
            person = {
                "person_id": f"person-{household['household_id'].split('-')[-1]}-{person_counter + 1:02d}",
                "household_id": household["household_id"],
                "geo_id": household["geo_id"],
                "claim_type": "INFERENCE",
                "retrieved_at": RETRIEVED_AT,
                "evidence_refs": household["evidence_refs"],
                "demographics": {"age_band": "65+", "gender": _weighted_choice(rng, list(_GENDER_WEIGHTS.items()))},
                "economics": {"income_band_lkr_monthly": household["economics"]["income_band_lkr_monthly"]},
                "digital": {"smartphone_access": "shared", "internet_access": household["internet_access"]},
                "behavioral": {"adoption_posture": "late_majority"},
                "role_in_household": role,
                "education_band": _education_band("65+", household["education_anchor"], role),
                "employment_status": "retired",
                "language_preference": _language_preference(household["language_profile"], rng),
                "payment_readiness": household["digital_context"]["payment_readiness"],
                "mobility_profile": household["mobility_profile"],
                "budget_sensitivity": household["budget_sensitivity"],
                "trust_sensitivity": household["trust_sensitivity"],
                "area_cluster": household["area_cluster"],
                "need_domain_scores": _adjust_needs(household["need_domain_scores"], role, "65+"),
            }
            person["market_segment_id"] = assign_b2c_segment(person)
            people.append(person)
            person_counter += 1

    return people
