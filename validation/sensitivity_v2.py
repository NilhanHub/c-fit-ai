"""Prompt #03 sensitivity analysis with scenario and weight-shock views."""

from __future__ import annotations

from experiments.run_rankings_v2 import run_prompt03_rankings


def run_prompt03_sensitivity(results: dict | None = None) -> dict:
    bundle = results or run_prompt03_rankings(seed=42, household_sample_size=1200, firm_sample_size=700)
    base = bundle["scenario_rankings"]["mixed_market_base"][:10]
    base_ids = [row["offer_id"] for row in base]
    base_rank = {offer_id: index + 1 for index, offer_id in enumerate(base_ids)}
    scenario_deltas = []
    for scenario_id, rankings in bundle["scenario_rankings"].items():
        top10 = rankings[:10]
        overlap = len(set(base_ids) & {row["offer_id"] for row in top10})
        movers = [
            abs(base_rank[row["offer_id"]] - (index + 1))
            for index, row in enumerate(top10)
            if row["offer_id"] in base_rank
        ]
        scenario_deltas.append(
            {
                "scenario_id": scenario_id,
                "top10_overlap_vs_mixed_base": overlap,
                "avg_rank_shift_within_top10": round(sum(movers) / len(movers), 2) if movers else 0.0,
            }
        )

    budget_bundle = run_prompt03_rankings(seed=42, household_sample_size=1200, firm_sample_size=700)
    budget_top = [row["offer_id"] for row in budget_bundle["scenario_rankings"]["budget_sensitive_market"][:10]]
    hostile_top = [row["offer_id"] for row in budget_bundle["scenario_rankings"]["hostile_market"][:10]]
    weight_shocks = [
        {
            "shock": "budget_pressure",
            "top10_overlap_vs_base": len(set(base_ids) & set(budget_top)),
            "top_offer_after_shock": budget_top[0],
        },
        {
            "shock": "hostile_conditions",
            "top10_overlap_vs_base": len(set(base_ids) & set(hostile_top)),
            "top_offer_after_shock": hostile_top[0],
        },
    ]
    return {"scenario_deltas": scenario_deltas, "weight_shocks": weight_shocks}
