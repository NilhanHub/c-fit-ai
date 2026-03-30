from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PROMPT02_FILES = [
    "PROMPT02_CONTINUITY_AUDIT.md",
    "task_rubric.md",
    "STATUS.md",
    "DECISIONS.md",
    "REJECTED_IDEAS.md",
    "research/source_hierarchy.md",
    "research/source_gap_matrix.md",
    "research/source_reliability.md",
    "model/model_boundary.md",
    "model/question_definition.md",
    "model/non_goals.md",
    "population/seed_tables.py",
    "population/household_sampler.py",
    "population/person_sampler.py",
    "population/segment_taxonomy.py",
    "population/synthesize_b2c.py",
    "firms/segment_taxonomy.py",
    "firms/firm_archetypes.py",
    "firms/firm_synthesizer.py",
    "firms/pain_maps.py",
    "offers/offer_schema.json",
    "offers/offer_normalizer.py",
    "scoring/b2c_dimensions.py",
    "scoring/b2c_score.py",
    "scoring/explain_b2c.py",
    "scoring/b2b_dimensions.py",
    "scoring/b2b_score.py",
    "scoring/explain_b2b.py",
    "scoring/portfolio_ranker.py",
    "experiments/scenario_definitions.py",
    "experiments/run_rankings.py",
    "validation/reproducibility_checks.py",
    "validation/sensitivity.py",
    "validation/model_limits.md",
    "reports/b2c_model_report.md",
    "reports/b2b_model_report.md",
    "reports/offer_corpus_report.md",
    "reports/b2c_scoring_framework.md",
    "reports/b2b_scoring_framework.md",
    "reports/ranking_report.md",
    "reports/validation_report.md",
    "outputs/b2c_segment_summary.csv",
    "outputs/b2b_segment_summary.csv",
    "outputs/top_offers_base.csv",
    "outputs/top_offers_by_scenario.csv",
    "data/curated/india_ai_offers_v1.csv",
    "qa/test_report.md",
    "qa/known_gaps.md",
    "qa/morning_decisions.md",
    "HANDOFF/MORNING_BRIEF.md",
    "HANDOFF/BUILD_STATUS.md",
    "HANDOFF/TOP_FINDINGS.md",
    "HANDOFF/NEXT_72_HOURS.md",
    "evidence/prompt02_manifest.json",
    "evidence/hash_log.csv",
    "evidence/run_log.md",
]


def test_prompt02_artifacts_exist_and_are_non_empty() -> None:
    missing = []
    empty = []

    for relative_path in REQUIRED_PROMPT02_FILES:
        path = REPO_ROOT / relative_path
        if not path.exists():
            missing.append(relative_path)
        elif path.is_file() and not path.read_text(encoding="utf-8").strip():
            empty.append(relative_path)

    assert not missing, f"Missing Prompt #02 artifacts: {missing}"
    assert not empty, f"Empty Prompt #02 artifacts: {empty}"
