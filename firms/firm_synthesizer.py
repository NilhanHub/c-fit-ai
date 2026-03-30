"""Generate reproducible Colombo B2B samples and buying centers for Prompt #02."""

from __future__ import annotations

import csv
from pathlib import Path
from random import Random

from firms.b2b_ability_to_pay import derive_ability_to_pay
from firms.b2b_admin_burden import derive_admin_burden
from firms.b2b_channel_reachability import derive_b2b_channel_reachability
from firms.b2b_customer_interaction import derive_customer_interaction
from firms.b2b_data_readiness import derive_data_readiness
from firms.b2b_digital_maturity import derive_firm_digital_maturity
from firms.b2b_expansion_potential import derive_expansion_potential
from firms.b2b_owner_sophistication import derive_owner_sophistication
from firms.b2b_payment_cycle_friction import derive_payment_cycle_friction
from firms.b2b_procurement_speed import derive_procurement_speed
from firms.b2b_roi_tolerance import derive_roi_tolerance
from firms.b2b_sales_cycle import derive_sales_cycle_length
from firms.b2b_staff_intensity import derive_staff_intensity
from firms.b2b_substitute_pressure import derive_b2b_substitute_pressure
from firms.b2b_workflow_complexity import derive_workflow_complexity
from firms.firm_archetypes import load_firm_anchors, load_firm_archetypes
from firms.prompt03_b2b_core import (
    Prompt03B2BConfig,
    RETRIEVED_AT_PROMPT03_B2B,
    assign_b2b_segment_v2,
    load_firm_archetypes_v2,
    pain_map_for_firm,
    pick_zone_for_firm,
    summarize_b2b_segments_v2,
)
from firms.segment_taxonomy import assign_firm_segment, summarize_b2b_segments


REPO_ROOT = Path(__file__).resolve().parents[1]
RETRIEVED_AT = "2026-03-16T18:30:00Z"


def _weighted_choice(rng: Random, rows: list[dict]) -> dict:
    return rng.choices(rows, weights=[row["weight"] for row in rows], k=1)[0]


def _adoption_friction(row: dict) -> str:
    if row["digital_maturity"] == "nascent" or row["payment_cycle_friction"] == "high":
        return "high"
    if row["digital_maturity"] == "emerging":
        return "medium"
    return "low"


def _buying_center(firm_id: str, row: dict, firm_index: int) -> dict:
    if row["size_band"] == "micro":
        procurement_style = "owner_led"
        roles = [
            {"role": "economic_buyer", "title": "Owner"},
            {"role": "user_champion", "title": "Frontline operator"},
        ]
        risk_tolerance = "medium"
    elif row["size_band"] == "small":
        procurement_style = "manager_led" if row["formality"] == "formal" else "owner_led"
        roles = [
            {"role": "economic_buyer", "title": "Founder or manager"},
            {"role": "user_champion", "title": "Operations lead"},
            {"role": "approver", "title": "Finance approver"},
        ]
        risk_tolerance = "medium"
    else:
        procurement_style = "committee_led"
        roles = [
            {"role": "economic_buyer", "title": "Business head"},
            {"role": "technical_buyer", "title": "IT or systems lead"},
            {"role": "user_champion", "title": "Operations manager"},
            {"role": "approver", "title": "Finance controller"},
        ]
        risk_tolerance = "low"

    return {
        "buying_center_id": f"bc-{firm_index + 1:06d}",
        "firm_id": firm_id,
        "procurement_style": procurement_style,
        "risk_tolerance": risk_tolerance,
        "decision_roles": roles,
        "claim_type": "INFERENCE",
        "retrieved_at": RETRIEVED_AT,
        "evidence_refs": row["evidence_refs"],
    }


def generate_b2b_market(
    seed: int = 42,
    target_firms: int = 800,
    geography_scope: str = "LK-11",
    firm_sample_size: int | None = None,
) -> dict:
    resolved_firms = firm_sample_size or target_firms
    if resolved_firms <= 0:
        raise ValueError("target_firms must be positive")

    rng = Random(seed)
    archetypes = load_firm_archetypes()
    anchors = load_firm_anchors()
    firms: list[dict] = []
    buying_centers: list[dict] = []

    for index in range(resolved_firms):
        row = _weighted_choice(rng, archetypes)
        firm_id = f"firm-{index + 1:06d}"
        buying_center = _buying_center(firm_id, row, index)
        firm = {
            "firm_id": firm_id,
            "geo_id": geography_scope,
            "sector_code": row["sector_code"],
            "size_band": row["size_band"],
            "formality": row["formality"],
            "digital_maturity": row["digital_maturity"],
            "budget_posture": row["budget_posture"],
            "adoption_friction": _adoption_friction(row),
            "claim_type": "INFERENCE",
            "retrieved_at": RETRIEVED_AT,
            "evidence_refs": row["evidence_refs"],
            "archetype_id": row["archetype_id"],
            "owner_sophistication": row["owner_sophistication"],
            "workflow_complexity": row["workflow_complexity"],
            "customer_interaction_intensity": row["customer_interaction"],
            "staff_intensity": row["staff_intensity"],
            "channel_mix": row["channel_mix"],
            "payment_cycle_friction": row["payment_cycle_friction"],
            "compliance_burden": row["compliance_burden"],
            "decision_speed": row["decision_speed"],
            "ability_to_pay_score": row["ability_to_pay"],
            "pain_scores": {
                "customer_support": row["needs_customer_support"],
                "document_admin": row["needs_document_admin"],
                "sales_marketing": row["needs_sales_marketing"],
                "collections": row["needs_collections"],
                "ops_scheduling": row["needs_ops_scheduling"],
                "hr_internal": row["needs_hr_internal"],
                "analytics": row["needs_analytics"],
                "training": row["needs_training"],
            },
            "procurement_style": buying_center["procurement_style"],
            "market_segment_id": "",
            "assumption_note": row["assumption_note"],
        }
        firm["market_segment_id"] = assign_firm_segment(firm)
        firms.append(firm)
        buying_centers.append(buying_center)

    segment_summaries = summarize_b2b_segments(firms)
    return {
        "metadata": {
            "seed": seed,
            "target_firms": resolved_firms,
            "geography_scope": geography_scope,
            "establishments_anchor": anchors["establishments_total"]["value"],
            "persons_engaged_anchor": anchors["persons_engaged_total"]["value"],
            "claim_type": "FACT",
            "retrieved_at": RETRIEVED_AT,
            "evidence_refs": ["dcs-non-agri-colombo-establishments"],
        },
        "firms": firms,
        "buying_centers": buying_centers,
        "segment_summaries": segment_summaries,
        "segment_summary": segment_summaries,
        "uncertainty_flags": [
            "INFERENCE: sector pain maps are derived from workflow logic rather than Colombo firm interviews",
            "TBD: firm-level revenue bands and procurement timing need later calibration",
        ],
    }


def write_b2b_segment_summary(result: dict, path: Path | None = None) -> Path:
    output_path = path or (REPO_ROOT / "outputs" / "b2b_segment_summary.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(result["segment_summaries"][0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result["segment_summaries"])
    return output_path


def generate_b2b_market_v2(
    seed: int = 42,
    target_firms: int = 1000,
    geography_scope: str = "LK-11",
    firm_sample_size: int | None = None,
) -> dict:
    config = Prompt03B2BConfig(seed=seed, target_firms=firm_sample_size or target_firms, geography_scope=geography_scope)
    rng = Random(config.seed)
    archetypes = load_firm_archetypes_v2()
    firms: list[dict] = []
    buying_centers: list[dict] = []
    for index in range(config.target_firms):
        archetype = rng.choices(archetypes, weights=[row["base_weight"] for row in archetypes], k=1)[0]
        zone = pick_zone_for_firm(rng, archetype)
        digital_maturity = derive_firm_digital_maturity(archetype["digital_maturity"], archetype["size_band"], zone["zone_id"])
        workflow_complexity = derive_workflow_complexity(archetype["workflow_complexity"], archetype["sector_id"])
        owner_sophistication = derive_owner_sophistication(archetype["owner_sophistication"], digital_maturity, archetype["formality"])
        customer_interaction = derive_customer_interaction(archetype["customer_interaction"], archetype["channel_mix"])
        admin_burden = derive_admin_burden(archetype["compliance_burden"], archetype["sector_id"])
        data_readiness = derive_data_readiness(archetype["data_readiness"], digital_maturity, archetype["channel_mix"])
        staff_intensity = derive_staff_intensity(archetype["staff_intensity"])
        payment_cycle = derive_payment_cycle_friction(archetype["payment_cycle_friction"], archetype["formality"], archetype["sector_id"])
        procurement_speed = derive_procurement_speed(archetype["procurement_speed"], archetype["size_band"])
        ability_to_pay = derive_ability_to_pay(float(archetype["ability_to_pay"]), zone["zone_id"], digital_maturity)
        roi_tolerance = derive_roi_tolerance(archetype["roi_tolerance"], owner_sophistication)
        sales_cycle = derive_sales_cycle_length(procurement_speed, archetype["size_band"], archetype["formality"])
        channel_reachability = derive_b2b_channel_reachability(archetype["channel_mix"], owner_sophistication, zone["zone_id"])
        substitute_pressure = derive_b2b_substitute_pressure(archetype["substitute_pressure"], archetype["sector_id"], zone["zone_id"])
        expansion_potential = derive_expansion_potential(ability_to_pay, digital_maturity, customer_interaction, archetype["size_band"])
        pain_scores = pain_map_for_firm(archetype["sector_id"], staff_intensity, customer_interaction, admin_burden)
        firm = {
            "firm_id": f"firm-v2-{index + 1:06d}",
            "geo_id": geography_scope,
            "zone_id": zone["zone_id"],
            "zone_label": zone["zone_label"],
            "sector_id": archetype["sector_id"],
            "size_band": archetype["size_band"],
            "formality": archetype["formality"],
            "claim_type": "INFERENCE",
            "retrieved_at": RETRIEVED_AT_PROMPT03_B2B,
            "evidence_refs": archetype["evidence_refs"],
            "digital_maturity_score": digital_maturity,
            "workflow_complexity_score": workflow_complexity,
            "owner_sophistication_score": owner_sophistication,
            "customer_interaction_score": customer_interaction,
            "admin_burden_score": admin_burden,
            "data_readiness_score": data_readiness,
            "staff_intensity_score": staff_intensity,
            "payment_cycle_friction_score": payment_cycle,
            "procurement_speed_score": procurement_speed,
            "ability_to_pay_score": ability_to_pay,
            "roi_tolerance_score": roi_tolerance,
            "sales_cycle_length_score": sales_cycle,
            "channel_reachability_score": channel_reachability,
            "substitute_pressure_score": substitute_pressure,
            "expansion_potential_score": expansion_potential,
            "pain_scores": pain_scores,
            "channel_mix": archetype["channel_mix"],
            "archetype_id": archetype["archetype_id"],
            "assumption_note": archetype["assumption_note"],
        }
        firm["market_segment_id"] = assign_b2b_segment_v2(firm)
        buying_centers.append(
            {
                "buying_center_id": f"bc-v2-{index + 1:06d}",
                "firm_id": firm["firm_id"],
                "procurement_style": "owner_led" if firm["size_band"] == "micro" else ("committee_led" if firm["size_band"] == "medium" else "manager_led"),
                "risk_tolerance": "medium" if firm["roi_tolerance_score"] >= 58 else "low",
                "decision_roles": [
                    {"role": "economic_buyer", "title": "Owner or business head"},
                    {"role": "user_champion", "title": "Operations lead"},
                    {"role": "approver", "title": "Finance approver"},
                ],
                "claim_type": "INFERENCE",
                "retrieved_at": RETRIEVED_AT_PROMPT03_B2B,
                "evidence_refs": archetype["evidence_refs"],
            }
        )
        firms.append(firm)

    segment_summary = summarize_b2b_segments_v2(firms)
    return {
        "metadata": {
            "seed": seed,
            "target_firms": config.target_firms,
            "geography_scope": geography_scope,
            "claim_type": "INFERENCE",
            "retrieved_at": RETRIEVED_AT_PROMPT03_B2B,
            "evidence_refs": ["dcs-non-agri-colombo-establishments", "dcs-informal-non-agri"],
        },
        "firms": firms,
        "buying_centers": buying_centers,
        "segment_summaries": segment_summary,
        "segment_summary": segment_summary,
        "uncertainty_flags": [
            "INFERENCE: sector and size shares are anchored to official establishment structure but not to firm-level revenue microdata",
            "INFERENCE: owner sophistication and ROI tolerance are modeled commercial proxies, not surveyed truth",
            "TBD: account expansion potential needs calibration with real Colombo SME sales cycles",
        ],
    }


def write_b2b_population_v2(result: dict, path: Path | None = None) -> Path:
    output_path = path or (REPO_ROOT / "outputs" / "b2b_population_v2.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample_rows = [
        {
            "firm_id": row["firm_id"],
            "zone_id": row["zone_id"],
            "sector_id": row["sector_id"],
            "size_band": row["size_band"],
            "market_segment_id": row["market_segment_id"],
            "ability_to_pay_score": row["ability_to_pay_score"],
            "digital_maturity_score": row["digital_maturity_score"],
            "channel_reachability_score": row["channel_reachability_score"],
            "expansion_potential_score": row["expansion_potential_score"],
        }
        for row in result["firms"]
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sample_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sample_rows)
    return output_path
