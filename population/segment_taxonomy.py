"""Prompt #02 B2C segment taxonomy and summary helpers."""

from __future__ import annotations

from collections import Counter, defaultdict


SEGMENT_LABELS = {
    "b2c_youth_upskilling_seekers": "Youth upskilling seekers",
    "b2c_mobile_income_strivers": "Mobile income strivers",
    "b2c_microcommerce_household_operators": "Microcommerce household operators",
    "b2c_care_navigation_households": "Care navigation households",
    "b2c_family_admin_coordinators": "Family admin coordinators",
    "b2c_affluent_productivity_seekers": "Affluent productivity seekers",
    "b2c_housing_commute_optimizers": "Housing and commute optimizers",
    "b2c_everyday_digital_convenience": "Everyday digital convenience",
}

_BUDGET_SCORE = {"very_high": 15, "high": 30, "medium": 55, "low": 80}
_DIGITAL_SCORE = {
    ("shared", "mobile_only"): 45,
    ("personal", "mobile_only"): 65,
    ("shared", "fixed_and_mobile"): 70,
    ("personal", "fixed_and_mobile"): 88,
}
_PAYMENT_SCORE = {"cash_only": 20, "mixed": 55, "digital_ready": 85}
_TRUST_SENSITIVITY = {"high": 75, "medium": 55, "low": 30}
_MOBILITY_SCORE = {
    "bus_and_walk": 45,
    "bus_commuter": 52,
    "local_radius": 58,
    "caregiver_bound": 30,
    "transit_heavy": 78,
    "commute_heavy": 68,
    "car_and_transit": 72,
}


def assign_b2c_segment(person: dict) -> str:
    needs = person["need_domain_scores"]
    age_band = person["demographics"]["age_band"]
    role = person["role_in_household"]
    income_band = person["economics"]["income_band_lkr_monthly"]

    if age_band == "15-24" and max(needs["education"], needs["jobs"]) >= 70:
        return "b2c_youth_upskilling_seekers"
    if needs["jobs"] >= 80 or person["employment_status"] in {"underemployed", "informal_worker"}:
        return "b2c_mobile_income_strivers"
    if needs["commerce"] >= 75 or role == "microbusiness_operator":
        return "b2c_microcommerce_household_operators"
    if needs["healthcare"] >= 80 or role in {"caregiver", "elder"}:
        return "b2c_care_navigation_households"
    if needs["family_admin"] >= 70 and role in {"parent", "caregiver"}:
        return "b2c_family_admin_coordinators"
    if needs["productivity"] >= 75 and income_band in {"150000-249999", "250000_plus"}:
        return "b2c_affluent_productivity_seekers"
    if needs["housing"] >= 70 or needs["mobility"] >= 70:
        return "b2c_housing_commute_optimizers"
    return "b2c_everyday_digital_convenience"


def summarize_b2c_segments(people: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for person in people:
        grouped[person["market_segment_id"]].append(person)

    total_people = len(people)
    summaries: list[dict] = []
    for segment_id, rows in grouped.items():
        language_counts = Counter(person["language_preference"] for person in rows)
        summary = {
            "segment_id": segment_id,
            "segment_label": SEGMENT_LABELS[segment_id],
            "population_count": len(rows),
            "population_share": round(len(rows) / total_people, 4),
            "avg_budget_score": round(sum(_BUDGET_SCORE[person["budget_sensitivity"]] for person in rows) / len(rows), 2),
            "avg_digital_readiness": round(
                sum(_DIGITAL_SCORE[(person["digital"]["smartphone_access"], person["digital"]["internet_access"])] for person in rows)
                / len(rows),
                2,
            ),
            "avg_payment_readiness": round(
                sum(_PAYMENT_SCORE[person["payment_readiness"]] for person in rows) / len(rows), 2
            ),
            "avg_trust_openness": round(
                100 - (sum(_TRUST_SENSITIVITY[person["trust_sensitivity"]] for person in rows) / len(rows)),
                2,
            ),
            "avg_channel_reach_score": round(
                sum(_MOBILITY_SCORE[person["mobility_profile"]] for person in rows) / len(rows),
                2,
            ),
            "avg_need_jobs": round(sum(person["need_domain_scores"]["jobs"] for person in rows) / len(rows), 2),
            "avg_need_education": round(sum(person["need_domain_scores"]["education"] for person in rows) / len(rows), 2),
            "avg_need_healthcare": round(sum(person["need_domain_scores"]["healthcare"] for person in rows) / len(rows), 2),
            "avg_need_commerce": round(sum(person["need_domain_scores"]["commerce"] for person in rows) / len(rows), 2),
            "avg_need_housing": round(sum(person["need_domain_scores"]["housing"] for person in rows) / len(rows), 2),
            "avg_need_mobility": round(sum(person["need_domain_scores"]["mobility"] for person in rows) / len(rows), 2),
            "avg_need_productivity": round(sum(person["need_domain_scores"]["productivity"] for person in rows) / len(rows), 2),
            "avg_need_finance": round(sum(person["need_domain_scores"]["finance"] for person in rows) / len(rows), 2),
            "avg_need_family_admin": round(sum(person["need_domain_scores"]["family_admin"] for person in rows) / len(rows), 2),
            "top_languages": "|".join(language for language, _count in language_counts.most_common(2)),
            "evidence_refs": "dcs-hies-2019|dcs-computer-literacy-2023|prompt02-b2c-model",
        }
        summaries.append(summary)

    return sorted(summaries, key=lambda item: (-item["population_share"], item["segment_id"]))
