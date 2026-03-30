"""Prompt #02 ranking sensitivity analysis."""

from __future__ import annotations

from experiments.run_rankings import run_all_rankings


def run_sensitivity_analysis(results: dict | None = None) -> dict:
    ranking_results = results or run_all_rankings(seed=42, b2c_households=1200, b2b_firms=600)
    base = ranking_results["base_outputs"]["mixed_market_base"]
    base_ranks = {row["offer_id"]: index + 1 for index, row in enumerate(base)}

    scenario_deltas: list[dict] = []
    for scenario in ranking_results["scenario_results"]:
        top_10 = scenario["top_10"]
        overlap = len({row["offer_id"] for row in top_10} & {row["offer_id"] for row in base[:10]})
        movers = []
        for row in top_10:
            if row["offer_id"] in base_ranks:
                movers.append(abs(base_ranks[row["offer_id"]] - (top_10.index(row) + 1)))
        scenario_deltas.append(
            {
                "scenario_id": scenario["scenario_id"],
                "top10_overlap_vs_mixed_base": overlap,
                "avg_rank_shift_within_top10": round(sum(movers) / len(movers), 2) if movers else 0.0
            }
        )

    return {
        "scenario_deltas": scenario_deltas,
        "notes": [
            "INFERENCE: overlap and average rank shift indicate robustness, not predictive truth.",
            "TBD: future sensitivity work should vary weights continuously rather than via named scenarios only."
        ]
    }
