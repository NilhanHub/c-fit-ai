from experiments.run_rankings_v2 import REQUIRED_PROMPT03_SCENARIOS, run_prompt03_rankings
from firms.firm_synthesizer import generate_b2b_market_v2
from offers.offer_normalizer_v2 import load_prompt03_offer_corpora
from population.synthesize_b2c import generate_b2c_market_v2
from validation.sensitivity_v2 import run_prompt03_sensitivity


def test_b2c_v2_generation_is_reproducible() -> None:
    first = generate_b2c_market_v2(seed=17, household_sample_size=180)
    second = generate_b2c_market_v2(seed=17, household_sample_size=180)

    assert first["households"] == second["households"]
    assert first["segment_summary"] == second["segment_summary"]
    assert len(first["households"]) == 180
    assert first["people"], "Expected B2C population v2 people to be generated"


def test_b2b_v2_generation_is_reproducible() -> None:
    first = generate_b2b_market_v2(seed=19, firm_sample_size=140)
    second = generate_b2b_market_v2(seed=19, firm_sample_size=140)

    assert first["firms"] == second["firms"]
    assert first["segment_summary"] == second["segment_summary"]
    assert len(first["firms"]) == 140


def test_prompt03_offer_corpora_cover_candidates_and_substitutes() -> None:
    corpora = load_prompt03_offer_corpora()

    assert len(corpora["candidate_offers"]) >= 18
    assert len(corpora["local_substitutes"]) >= 4
    assert len(corpora["international_benchmarks"]) >= 4
    assert any(offer["market_side"] in {"b2c", "both"} for offer in corpora["candidate_offers"])
    assert any(offer["market_side"] in {"b2b", "both"} for offer in corpora["candidate_offers"])


def test_prompt03_rankings_cover_required_views() -> None:
    bundle = run_prompt03_rankings(seed=41, household_sample_size=220, firm_sample_size=160)

    assert set(bundle["scenario_rankings"]) == set(REQUIRED_PROMPT03_SCENARIOS)
    assert bundle["top_opportunities"], "Expected top opportunities output"
    assert bundle["base_views"]["mixed_market_base"], "Expected mixed-market base ranking"
    assert bundle["competitor_graph"]["nodes"], "Expected competitor graph nodes"


def test_prompt03_sensitivity_reports_rank_movement() -> None:
    bundle = run_prompt03_rankings(seed=29, household_sample_size=200, firm_sample_size=150)
    sensitivity = run_prompt03_sensitivity(bundle)

    assert sensitivity["scenario_deltas"], "Expected scenario deltas"
    assert sensitivity["weight_shocks"], "Expected weight shock results"
    assert any(delta["top10_overlap_vs_mixed_base"] < 10 for delta in sensitivity["scenario_deltas"])
