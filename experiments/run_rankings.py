"""Run Prompt #02 scenario rankings for the Colombo v0 market model."""

from __future__ import annotations

import csv
from pathlib import Path

from experiments.scenario_definitions import SCENARIOS
from firms.firm_synthesizer import generate_b2b_market
from offers.offer_normalizer import load_curated_offer_corpus
from population.synthesize_b2c import generate_b2c_market
from scoring.portfolio_ranker import rank_offers_for_scenario


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SCENARIOS = tuple(SCENARIOS.keys())


def run_all_rankings(
    seed: int = 42,
    b2c_households: int = 1500,
    b2b_firms: int = 800,
    household_sample_size: int | None = None,
    firm_sample_size: int | None = None,
) -> dict:
    resolved_households = household_sample_size or b2c_households
    resolved_firms = firm_sample_size or b2b_firms
    b2c_market = generate_b2c_market(seed=seed, target_households=resolved_households)
    b2b_market = generate_b2b_market(seed=seed, target_firms=resolved_firms)
    offers = load_curated_offer_corpus()

    scenario_results: list[dict] = []
    for scenario_id in REQUIRED_SCENARIOS:
        scenario = SCENARIOS[scenario_id]
        rankings = rank_offers_for_scenario(offers, b2c_market["segment_summaries"], b2b_market["segment_summaries"], scenario)
        scenario_results.append(
            {
                "scenario_id": scenario_id,
                "description": scenario["description"],
                "rankings": rankings,
                "top_10": rankings[:10],
                "top_25": rankings[:25],
            }
        )

    base_outputs = {
        "colombo_b2c_base": scenario_results[0]["top_10"],
        "colombo_b2b_base": scenario_results[1]["top_10"],
        "mixed_market_base": scenario_results[2]["top_10"],
    }
    scenario_rankings = {result["scenario_id"]: result["rankings"] for result in scenario_results}
    return {
        "offers": offers,
        "b2c_market": b2c_market,
        "b2b_market": b2b_market,
        "scenario_results": scenario_results,
        "scenario_rankings": scenario_rankings,
        "base_outputs": base_outputs,
        "base_ranking": base_outputs["mixed_market_base"],
    }


def write_ranking_outputs(results: dict) -> tuple[Path, Path]:
    outputs_dir = REPO_ROOT / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    base_path = outputs_dir / "top_offers_base.csv"
    scenario_path = outputs_dir / "top_offers_by_scenario.csv"

    base_rows = []
    for scenario_id, rankings in results["base_outputs"].items():
        for rank, row in enumerate(rankings, start=1):
            base_rows.append({"scenario_id": scenario_id, "rank": rank, **row})

    scenario_rows = []
    for scenario in results["scenario_results"]:
        for rank, row in enumerate(scenario["top_25"], start=1):
            scenario_rows.append({"rank": rank, **row})

    if base_rows:
        with base_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(base_rows[0].keys()))
            writer.writeheader()
            writer.writerows(base_rows)

    if scenario_rows:
        with scenario_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(scenario_rows[0].keys()))
            writer.writeheader()
            writer.writerows(scenario_rows)

    return base_path, scenario_path
