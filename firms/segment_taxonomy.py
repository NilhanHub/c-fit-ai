"""Prompt #02 B2B segment taxonomy and summary helpers."""

from __future__ import annotations

from collections import Counter, defaultdict


SEGMENT_LABELS = {
    "b2b_smb_retail_operators": "SMB retail operators",
    "b2b_consumer_service_frontdesks": "Consumer service front desks",
    "b2b_field_ops_and_logistics": "Field ops and logistics",
    "b2b_healthcare_admin_clusters": "Healthcare admin clusters",
    "b2b_education_service_operators": "Education service operators",
    "b2b_knowledge_service_backoffices": "Knowledge service back offices",
    "b2b_workshop_manufacturing_operators": "Workshop manufacturing operators",
    "b2b_formal_growth_smes": "Formal growth SMEs",
}

_DIGITAL_SCORE = {"nascent": 30, "emerging": 52, "operational": 72, "advanced": 90}
_DECISION_SPEED_SCORE = {"fast": 80, "medium": 55, "slow": 30}
_SOPHISTICATION_SCORE = {"medium": 55, "high": 78, "low": 35}


def assign_firm_segment(firm: dict) -> str:
    sector = firm["sector_code"]
    if sector == "retail_trade":
        return "b2b_smb_retail_operators"
    if sector in {"food_service", "tourism_hospitality", "real_estate_services"}:
        return "b2b_consumer_service_frontdesks"
    if sector in {"logistics_services", "wholesale_distribution"}:
        return "b2b_field_ops_and_logistics"
    if sector == "healthcare_services":
        return "b2b_healthcare_admin_clusters"
    if sector == "education_services":
        return "b2b_education_service_operators"
    if sector == "professional_services":
        return "b2b_knowledge_service_backoffices"
    if sector == "light_manufacturing":
        return "b2b_workshop_manufacturing_operators"
    return "b2b_formal_growth_smes"


def summarize_b2b_segments(firms: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for firm in firms:
        grouped[firm["market_segment_id"]].append(firm)

    total_firms = len(firms)
    summaries: list[dict] = []
    for segment_id, rows in grouped.items():
        procurement_styles = Counter(firm["procurement_style"] for firm in rows)
        summary = {
            "segment_id": segment_id,
            "segment_label": SEGMENT_LABELS[segment_id],
            "firm_count": len(rows),
            "firm_share": round(len(rows) / total_firms, 4),
            "avg_ability_to_pay": round(sum(firm["ability_to_pay_score"] for firm in rows) / len(rows), 2),
            "avg_digital_maturity": round(sum(_DIGITAL_SCORE[firm["digital_maturity"]] for firm in rows) / len(rows), 2),
            "avg_owner_sophistication": round(sum(_SOPHISTICATION_SCORE[firm["owner_sophistication"]] for firm in rows) / len(rows), 2),
            "avg_decision_speed": round(sum(_DECISION_SPEED_SCORE[firm["decision_speed"]] for firm in rows) / len(rows), 2),
            "avg_need_customer_support": round(sum(firm["pain_scores"]["customer_support"] for firm in rows) / len(rows), 2),
            "avg_need_document_admin": round(sum(firm["pain_scores"]["document_admin"] for firm in rows) / len(rows), 2),
            "avg_need_sales_marketing": round(sum(firm["pain_scores"]["sales_marketing"] for firm in rows) / len(rows), 2),
            "avg_need_collections": round(sum(firm["pain_scores"]["collections"] for firm in rows) / len(rows), 2),
            "avg_need_ops_scheduling": round(sum(firm["pain_scores"]["ops_scheduling"] for firm in rows) / len(rows), 2),
            "avg_need_hr_internal": round(sum(firm["pain_scores"]["hr_internal"] for firm in rows) / len(rows), 2),
            "avg_need_analytics": round(sum(firm["pain_scores"]["analytics"] for firm in rows) / len(rows), 2),
            "avg_need_training": round(sum(firm["pain_scores"]["training"] for firm in rows) / len(rows), 2),
            "dominant_procurement_style": procurement_styles.most_common(1)[0][0],
            "evidence_refs": "dcs-non-agri-colombo-establishments|prompt02-b2b-model",
        }
        summaries.append(summary)

    return sorted(summaries, key=lambda item: (-item["firm_share"], item["segment_id"]))
