"""Prompt #02 reproducibility checks."""

from __future__ import annotations

from experiments.run_rankings import run_all_rankings
from experiments.run_rankings_v2 import run_prompt03_rankings


def run_reproducibility_checks() -> dict:
    first = run_all_rankings(seed=42, b2c_households=900, b2b_firms=450)
    second = run_all_rankings(seed=42, b2c_households=900, b2b_firms=450)
    third = run_all_rankings(seed=43, b2c_households=900, b2b_firms=450)

    first_top = [row["offer_id"] for row in first["base_outputs"]["mixed_market_base"][:5]]
    second_top = [row["offer_id"] for row in second["base_outputs"]["mixed_market_base"][:5]]
    third_top = [row["offer_id"] for row in third["base_outputs"]["mixed_market_base"][:5]]

    return {
        "same_seed_identical": first_top == second_top,
        "different_seed_overlap_top5": len(set(first_top) & set(third_top)),
        "notes": [
            "FACT: same-seed ranking output should be identical.",
            "INFERENCE: different-seed top-5 overlap is a coarse stability proxy, not validation."
        ]
    }


def run_reproducibility_checks_v2() -> dict:
    first = run_prompt03_rankings(seed=42, household_sample_size=900, firm_sample_size=500)
    second = run_prompt03_rankings(seed=42, household_sample_size=900, firm_sample_size=500)
    third = run_prompt03_rankings(seed=43, household_sample_size=900, firm_sample_size=500)

    first_top = [row["offer_id"] for row in first["base_views"]["mixed_market_base"][:5]]
    second_top = [row["offer_id"] for row in second["base_views"]["mixed_market_base"][:5]]
    third_top = [row["offer_id"] for row in third["base_views"]["mixed_market_base"][:5]]
    return {
        "same_seed_identical": first_top == second_top,
        "different_seed_overlap_top5": len(set(first_top) & set(third_top)),
        "notes": [
            "FACT: Prompt #03 same-seed results should be identical.",
            "INFERENCE: Prompt #03 different-seed overlap remains a stability proxy rather than a validation claim.",
        ],
    }
