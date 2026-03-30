from experiments.run_rankings import REQUIRED_SCENARIOS, run_all_rankings
from firms.firm_synthesizer import generate_b2b_market
from offers.offer_normalizer import load_curated_offer_corpus
from population.synthesize_b2c import generate_b2c_market


def test_b2c_generation_is_reproducible() -> None:
    first = generate_b2c_market(seed=7, household_sample_size=120)
    second = generate_b2c_market(seed=7, household_sample_size=120)

    assert first["households"] == second["households"]
    assert first["segment_summary"] == second["segment_summary"]
    assert len(first["households"]) == 120
    assert first["people"], "Expected synthetic people to be generated"


def test_b2b_generation_is_reproducible() -> None:
    first = generate_b2b_market(seed=13, firm_sample_size=150)
    second = generate_b2b_market(seed=13, firm_sample_size=150)

    assert first["firms"] == second["firms"]
    assert first["segment_summary"] == second["segment_summary"]
    assert len(first["firms"]) == 150


def test_curated_offer_corpus_has_b2c_and_b2b_coverage() -> None:
    corpus = load_curated_offer_corpus()

    assert len(corpus) >= 12
    market_sides = {offer["market_side"] for offer in corpus}
    assert "b2c" in market_sides or "hybrid" in market_sides
    assert "b2b" in market_sides or "hybrid" in market_sides


def test_rankings_cover_required_scenarios() -> None:
    ranking_bundle = run_all_rankings(seed=42, household_sample_size=160, firm_sample_size=120)

    assert set(ranking_bundle["scenario_rankings"]) == set(REQUIRED_SCENARIOS)
    assert ranking_bundle["base_ranking"], "Expected at least one base ranking row"
    assert ranking_bundle["scenario_rankings"]["mixed_market_base"], "Expected mixed-market leaderboard"
