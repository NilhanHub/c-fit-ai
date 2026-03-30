"""Prompt #03 ranking runner, competitor graph builder, and output helpers."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from experiments.scenario_pack_v2 import PROMPT03_SCENARIOS
from firms.firm_synthesizer import generate_b2b_market_v2
from offers.offer_normalizer_v2 import load_prompt03_offer_corpora
from population.synthesize_b2c import generate_b2c_market_v2
from scoring.b2b_fit_v2 import score_offer_for_b2b_v2
from scoring.b2c_fit_v2 import score_offer_for_b2c_v2


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PROMPT03_SCENARIOS = tuple(PROMPT03_SCENARIOS.keys())


def _combine_scores(b2c_result: dict, b2b_result: dict, scenario: dict) -> tuple[float, str]:
    market_mode = scenario["market_mode"]
    if market_mode == "b2c":
        return b2c_result["commercial_score"], "b2c"
    if market_mode == "b2b":
        return b2b_result["commercial_score"], "b2b"
    weights = scenario.get("mixed_weights", {"b2c": 0.45, "b2b": 0.55})
    return round((b2c_result["commercial_score"] * weights["b2c"]) + (b2b_result["commercial_score"] * weights["b2b"]), 2), "mixed"


def build_competitor_graph(corpora: dict[str, list[dict]]) -> dict:
    all_rows = []
    for corpus_name, rows in corpora.items():
        for row in rows:
            all_rows.append({**row, "corpus_name": corpus_name})
    nodes = [
        {
            "id": row["offer_id"],
            "label": row["offer_name"],
            "vendor": row["vendor_name"],
            "offer_kind": row["offer_kind"],
            "problem_domain": row["problem_domain"],
            "substitute_cluster": row["substitute_cluster"],
        }
        for row in all_rows
    ]
    edges = []
    for index, left in enumerate(all_rows):
        for right in all_rows[index + 1 :]:
            reasons = []
            if left["problem_domain"] == right["problem_domain"]:
                reasons.append("same_problem_domain")
            if left["substitute_cluster"] == right["substitute_cluster"]:
                reasons.append("same_substitute_cluster")
            if left["market_side"] == right["market_side"]:
                reasons.append("same_market_side")
            if reasons:
                edges.append({"source": left["offer_id"], "target": right["offer_id"], "reasons": reasons[:2]})
    domain_clusters = defaultdict(list)
    for row in all_rows:
        domain_clusters[row["problem_domain"]].append(row["offer_id"])
    return {"nodes": nodes, "edges": edges, "domain_clusters": domain_clusters}


def run_prompt03_rankings(
    seed: int = 42,
    household_sample_size: int = 2200,
    firm_sample_size: int = 1200,
) -> dict:
    b2c_market = generate_b2c_market_v2(seed=seed, household_sample_size=household_sample_size)
    b2b_market = generate_b2b_market_v2(seed=seed, firm_sample_size=firm_sample_size)
    corpora = load_prompt03_offer_corpora()
    offers = corpora["candidate_offers"]
    competitor_graph = build_competitor_graph(corpora)
    scenario_results = []
    for scenario_id in REQUIRED_PROMPT03_SCENARIOS:
        scenario = PROMPT03_SCENARIOS[scenario_id]
        rows = []
        for offer in offers:
            b2c_result = score_offer_for_b2c_v2(offer, b2c_market["segment_summaries"], scenario)
            b2b_result = score_offer_for_b2b_v2(offer, b2b_market["segment_summaries"], scenario)
            final_score, dominant_market = _combine_scores(b2c_result, b2b_result, scenario)
            rows.append(
                {
                    "scenario_id": scenario_id,
                    "offer_id": offer["offer_id"],
                    "vendor_name": offer["vendor_name"],
                    "offer_name": offer["offer_name"],
                    "problem_domain": offer["problem_domain"],
                    "market_side": offer["market_side"],
                    "offer_kind": offer["offer_kind"],
                    "final_score": final_score,
                    "b2c_score": b2c_result["commercial_score"],
                    "b2b_score": b2b_result["commercial_score"],
                    "dominant_market": dominant_market,
                    "top_b2c_segment": b2c_result["top_segment_id"] or "",
                    "top_b2b_segment": b2b_result["top_segment_id"] or "",
                    "quality_score": offer["quality"]["quality_score"],
                }
            )
        ranked = sorted(rows, key=lambda item: (-item["final_score"], item["offer_id"]))
        active_ranked = [row for row in ranked if row["final_score"] > 0]
        scenario_results.append(
            {
                "scenario_id": scenario_id,
                "description": scenario["description"],
                "rankings": ranked,
                "top_10": active_ranked[:10],
                "top_25": active_ranked[:25],
            }
        )

    base_views = {
        "colombo_b2c_base": next(item["top_10"] for item in scenario_results if item["scenario_id"] == "colombo_b2c_base"),
        "colombo_b2b_base": next(item["top_10"] for item in scenario_results if item["scenario_id"] == "colombo_b2b_base"),
        "mixed_market_base": next(item["top_10"] for item in scenario_results if item["scenario_id"] == "mixed_market_base"),
    }
    scenario_rankings = {item["scenario_id"]: item["rankings"] for item in scenario_results}
    return {
        "b2c_market": b2c_market,
        "b2b_market": b2b_market,
        "corpora": corpora,
        "offers": offers,
        "scenario_results": scenario_results,
        "scenario_rankings": scenario_rankings,
        "base_views": base_views,
        "top_opportunities": base_views["mixed_market_base"],
        "top_segments": build_top_segments(b2c_market["segment_summaries"], b2b_market["segment_summaries"]),
        "opportunity_explainers": build_opportunity_explainers(base_views["mixed_market_base"], scenario_results),
        "competitor_graph": {"nodes": competitor_graph["nodes"], "edges": competitor_graph["edges"]},
        "offer_domain_clusters": {key: value for key, value in competitor_graph["domain_clusters"].items()},
    }


def build_top_segments(b2c_segments: list[dict], b2b_segments: list[dict]) -> list[dict]:
    rows = []
    for segment in b2c_segments[:5]:
        rows.append(
            {
                "market": "b2c",
                "segment_id": segment["segment_id"],
                "segment_label": segment["segment_label"],
                "share": segment["population_share"],
                "commercial_readiness": round(
                    (segment["avg_budget_headroom"] * 0.25)
                    + (segment["avg_digital_readiness"] * 0.25)
                    + (segment["avg_channel_reachability"] * 0.25)
                    + (segment["avg_retention_potential"] * 0.25),
                    2,
                ),
            }
        )
    for segment in b2b_segments[:5]:
        rows.append(
            {
                "market": "b2b",
                "segment_id": segment["segment_id"],
                "segment_label": segment["segment_label"],
                "share": segment["firm_share"],
                "commercial_readiness": round(
                    (segment["avg_ability_to_pay"] * 0.25)
                    + (segment["avg_digital_maturity"] * 0.25)
                    + (segment["avg_channel_reachability"] * 0.25)
                    + (segment["avg_expansion_potential"] * 0.25),
                    2,
                ),
            }
        )
    return sorted(rows, key=lambda item: (-item["commercial_readiness"], item["segment_id"]))


def build_opportunity_explainers(base_rows: list[dict], scenario_results: list[dict]) -> dict:
    lookup = {row["offer_id"]: row for row in base_rows}
    scenario_presence = Counter(offer["offer_id"] for scenario in scenario_results for offer in scenario["top_10"])
    explainers = {}
    for offer_id, row in lookup.items():
        explainers[offer_id] = {
            "offer_name": row["offer_name"],
            "vendor_name": row["vendor_name"],
            "base_score": row["final_score"],
            "dominant_market": row["dominant_market"],
            "top_b2c_segment": row["top_b2c_segment"],
            "top_b2b_segment": row["top_b2b_segment"],
            "top10_scenario_count": scenario_presence[offer_id],
            "why": [
                f"{row['problem_domain']} aligns with a high-need Colombo segment",
                f"{row['dominant_market']} demand currently drives the score",
                f"quality score {row['quality_score']} supports the ranking",
            ],
        }
    return explainers


def write_prompt03_outputs(results: dict) -> dict[str, Path]:
    outputs_dir = REPO_ROOT / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    top_opportunities_path = outputs_dir / "top_opportunities.csv"
    with top_opportunities_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results["top_opportunities"][0].keys()))
        writer.writeheader()
        writer.writerows(results["top_opportunities"])
    paths["top_opportunities"] = top_opportunities_path

    top_offers_base_path = outputs_dir / "top_offers_base.csv"
    base_rows = []
    for scenario_id, rows in results["base_views"].items():
        for rank, row in enumerate(rows, start=1):
            base_rows.append({"scenario_id": scenario_id, "rank": rank, **row})
    with top_offers_base_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(base_rows[0].keys()))
        writer.writeheader()
        writer.writerows(base_rows)
    paths["top_offers_base"] = top_offers_base_path

    top_segments_path = outputs_dir / "top_segments.csv"
    with top_segments_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results["top_segments"][0].keys()))
        writer.writeheader()
        writer.writerows(results["top_segments"])
    paths["top_segments"] = top_segments_path

    scenario_comparison_path = outputs_dir / "scenario_comparison.csv"
    scenario_rows = []
    for scenario in results["scenario_results"]:
        for rank, row in enumerate(scenario["top_10"], start=1):
            scenario_rows.append({"scenario_id": scenario["scenario_id"], "rank": rank, **row})
    with scenario_comparison_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scenario_rows[0].keys()))
        writer.writeheader()
        writer.writerows(scenario_rows)
    paths["scenario_comparison"] = scenario_comparison_path

    top_offers_by_scenario_path = outputs_dir / "top_offers_by_scenario.csv"
    with top_offers_by_scenario_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scenario_rows[0].keys()))
        writer.writeheader()
        writer.writerows(scenario_rows)
    paths["top_offers_by_scenario"] = top_offers_by_scenario_path

    explainers_path = outputs_dir / "opportunity_explainers.json"
    explainers_path.write_text(json.dumps(results["opportunity_explainers"], indent=2), encoding="utf-8")
    paths["opportunity_explainers"] = explainers_path

    competitor_graph_path = outputs_dir / "offer_competitor_graph.json"
    competitor_graph_path.write_text(json.dumps(results["competitor_graph"], indent=2), encoding="utf-8")
    paths["offer_competitor_graph"] = competitor_graph_path

    domain_clusters_path = outputs_dir / "offer_domain_clusters.json"
    domain_clusters_path.write_text(json.dumps(results["offer_domain_clusters"], indent=2), encoding="utf-8")
    paths["offer_domain_clusters"] = domain_clusters_path

    return paths
