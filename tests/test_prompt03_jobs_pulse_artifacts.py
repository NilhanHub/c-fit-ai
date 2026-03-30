from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PROMPT03_FILES = [
    "task_rubric.md",
    "research/market_map.md",
    "research/wedge_matrix.md",
    "research/final_wedge_decision.md",
    "product/product_thesis.md",
    "product/habit_loop.md",
    "product/jtbd.md",
    "product/retention_model.md",
    "ux/ux_blueprint.md",
    "ux/information_architecture.md",
    "ux/user_flows.md",
    "ux/copy_principles.md",
    "stories/story_system_spec.md",
    "stories/story_policy.md",
    "stories/story_ranking.md",
    "trust/fraud_patterns.md",
    "trust/moderation_spec.md",
    "trust/verification_system.md",
    "trust/privacy_rules.md",
    "architecture/system_overview.md",
    "architecture/data_model.md",
    "architecture/api_contracts.md",
    "architecture/background_jobs.md",
    "architecture/analytics_events.md",
    "contracts/job_posting.schema.yaml",
    "contracts/story_item.schema.yaml",
    "contracts/seeker_profile.schema.yaml",
    "contracts/employer_profile.schema.yaml",
    "contracts/alert.schema.yaml",
    "apps/web/package.json",
    "apps/web/index.html",
    "apps/web/src/main.tsx",
    "apps/web/src/App.tsx",
    "apps/web/src/styles.css",
    "demo/demo_script.md",
    "demo/demo_dataset.md",
    "demo/why_this_wins.md",
    "qa/test_report.md",
    "qa/known_gaps.md",
    "qa/morning_decisions.md",
    "HANDOFF/MORNING_BRIEF.md",
    "HANDOFF/BUILD_STATUS.md",
    "HANDOFF/NEXT_72_HOURS.md",
]


def test_prompt03_jobs_pulse_artifacts_exist_and_are_non_empty() -> None:
    missing = []
    empty = []

    for relative_path in REQUIRED_PROMPT03_FILES:
        path = REPO_ROOT / relative_path
        if not path.exists():
            missing.append(relative_path)
        elif path.is_file() and not path.read_text(encoding="utf-8").strip():
            empty.append(relative_path)

    assert not missing, f"Missing Prompt #03 artifacts: {missing}"
    assert not empty, f"Empty Prompt #03 artifacts: {empty}"
