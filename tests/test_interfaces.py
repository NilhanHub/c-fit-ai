from population.synthesis import PopulationSynthesisConfig, build_population
from firms.synthesis import FirmSynthesisConfig, build_firms
from offers.normalize import normalize_offer
from scoring.engine import score_offer
from experiments.runner import run_experiment


def test_population_builder_returns_planning_artifact() -> None:
    plan = build_population(
        PopulationSynthesisConfig(
            geography_scope="LK-11",
            target_households=2500,
            target_individuals=9100,
            seed_dataset_refs=["dcs-census-2024", "hies-2019", "computer-literacy-2023"],
        )
    )

    assert plan.geography_scope == "LK-11"
    assert plan.method == "hierarchical_seeded_ipf"
    assert "population_entity.schema.yaml" in plan.contracts


def test_firm_builder_returns_planning_artifact() -> None:
    plan = build_firms(
        FirmSynthesisConfig(
            geography_scope="LK-11",
            target_firms=1200,
            seed_dataset_refs=["dcs-non-agri-2021", "dcs-industries-2022"],
            sector_focus=["services_bpo", "retail_trade"],
        )
    )

    assert plan.geography_scope == "LK-11"
    assert plan.method == "sector_size_seeded_sampler"
    assert "firm_entity.schema.yaml" in plan.contracts


def test_normalize_offer_requires_provenance_and_emits_offer_id() -> None:
    normalized = normalize_offer(
        raw_offer={
            "vendor_name": "Example AI Pvt Ltd",
            "vendor_country": "IN",
            "offer_name": "AI Support Copilot",
            "target_segment": "b2b_sme",
            "problem_category": "customer_support",
            "delivery_mode": "saas",
            "pricing_model": "subscription",
            "language_support": ["en"],
        },
        source_metadata={
            "source_url": "https://example.com/offer",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "claim_type": "FACT",
            "evidence_refs": ["https://example.com/offer"],
        },
    )

    assert normalized["offer_id"].startswith("offer-example-ai-pvt-ltd")
    assert normalized["claim_type"] == "FACT"


def test_normalize_offer_rejects_missing_evidence() -> None:
    try:
        normalize_offer(
            raw_offer={
                "vendor_name": "Example AI Pvt Ltd",
                "vendor_country": "IN",
                "offer_name": "AI Support Copilot",
                "target_segment": "b2b_sme",
                "problem_category": "customer_support",
                "delivery_mode": "saas",
                "pricing_model": "subscription",
                "language_support": ["en"],
            },
            source_metadata={
                "source_url": "https://example.com/offer",
                "retrieved_at": "2026-03-16T00:00:00Z",
                "claim_type": "FACT",
                "evidence_refs": [],
            },
        )
    except ValueError as error:
        assert "evidence_refs" in str(error)
    else:
        raise AssertionError("Expected normalize_offer to reject missing evidence_refs")


def test_score_offer_is_deterministic_and_monotonic() -> None:
    baseline = score_offer(
        offer_id="offer-0001",
        market_segment_id="colombo-b2b-sme-services",
        scenario_id="baseline",
        dimension_scores={
            "pain_frequency": 50,
            "problem_severity": 50,
            "willingness_to_pay": 50,
            "price_fit": 50,
        },
        evidence_refs=["prompt01"],
    )
    improved = score_offer(
        offer_id="offer-0001",
        market_segment_id="colombo-b2b-sme-services",
        scenario_id="baseline",
        dimension_scores={
            "pain_frequency": 70,
            "problem_severity": 70,
            "willingness_to_pay": 70,
            "price_fit": 70,
        },
        evidence_refs=["prompt01"],
    )

    assert baseline == score_offer(
        offer_id="offer-0001",
        market_segment_id="colombo-b2b-sme-services",
        scenario_id="baseline",
        dimension_scores={
            "pain_frequency": 50,
            "problem_severity": 50,
            "willingness_to_pay": 50,
            "price_fit": 50,
        },
        evidence_refs=["prompt01"],
    )
    assert improved["final_rank_score"] > baseline["final_rank_score"]


def test_run_experiment_selects_top_25_for_pilot_100() -> None:
    scorecards = [
        {
            "offer_id": f"offer-{index:04d}",
            "market_segment_id": "colombo-b2b-sme-services",
            "scenario_id": "baseline",
            "final_rank_score": 100 - index,
            "weighted_score": 100 - index,
            "evidence_score": 80,
            "confidence_score": 60,
            "simulation_score": 0,
            "raw_score": 100 - index,
            "dimension_scores": {"pain_frequency": 50},
            "blockers": [],
            "claim_type": "INFERENCE",
            "retrieved_at": "2026-03-16T00:00:00Z",
            "evidence_refs": ["prompt01"],
        }
        for index in range(100)
    ]

    result = run_experiment(
        experiment_id="pilot-100-baseline",
        offer_batch_id="india-pilot-100",
        market_slice_id="colombo-v0",
        scenario_pack=["baseline", "low_trust"],
        scorecards=scorecards,
        target_scale=100,
        random_seed=42,
        evidence_refs=["prompt01"],
    )

    assert len(result["stage_2_candidates"]) == 25
    assert len(result["stage_3_finalists"]) == 10
    assert result["stage_2_candidates"][0] == "offer-0000"
