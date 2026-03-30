from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PROMPT05_FILES = [
    "PROMPT05_CONTINUITY_AUDIT.md",
    "PROMPT05_VISUAL_FORENSICS.md",
    "PROMPT05_SURFACE_GAP_MAP.md",
    "design/prompt05_truth_table.md",
    "design/prompt05_scorecard.csv",
    "design/prompt05_ux_thesis.md",
    "design/brand_behavior_principles.md",
    "ux/prompt05_information_architecture.md",
    "ux/mobile_layout_strategy.md",
    "ux/tablet_layout_strategy.md",
    "ux/desktop_layout_strategy.md",
    "ux/zone_priority_map.md",
    "product/prompt05_delta_experience.md",
    "architecture/last_visit_event_model.md",
    "ranking/delta_priority_rules.md",
    "alerts/delta_alert_logic.md",
    "ux/prompt05_onboarding_rebuild.md",
    "design/onboarding_copy_system.md",
    "ux/prompt05_feed_rebuild.md",
    "ux/feed_layout_options.md",
    "ux/final_feed_decision.md",
    "stories/prompt05_story_rebuild.md",
    "stories/story_card_anatomy_v2.md",
    "stories/story_surface_behavior_v2.md",
    "stories/story_priority_v2.md",
    "ux/prompt05_job_surface_rebuild.md",
    "ux/job_card_v2.md",
    "ux/job_detail_v2.md",
    "ux/application_pulse_v2.md",
    "alerts/prompt05_alert_surface_rebuild.md",
    "alerts/saved_search_surface_v2.md",
    "alerts/alerts_surface_v2.md",
    "stories/prompt05_composer_rebuild.md",
    "stories/candidate_story_creation_v2.md",
    "stories/employer_story_creation_v2.md",
    "trust/prompt05_trust_rebuild.md",
    "trust/trust_surface_v2.md",
    "trust/warning_surface_v2.md",
    "trust/report_block_flow_v2.md",
    "employer/prompt05_employer_surface_rebuild.md",
    "employer/employer_profile_v2.md",
    "employer/employer_trust_display_v2.md",
    "design/prompt05_design_system_v2.md",
    "design/component_families_v2.md",
    "design/responsive_rules_v2.md",
    "design/motion_rules_v2.md",
    "mobile/prompt05_mobile_hardening.md",
    "mobile/thumb_zone_map.md",
    "mobile/mobile_action_strategy.md",
    "desktop/prompt05_desktop_rebuild.md",
    "desktop/desktop_density_strategy.md",
    "desktop/right_rail_strategy.md",
    "copy/prompt05_copy_rewrite.md",
    "copy/microcopy_dictionary.md",
    "copy/trust_and_warning_lexicon.md",
    "demo/prompt05_data_realism.md",
    "demo/demo_dataset_v3.md",
    "build/prompt05_build_delta.md",
    "build/prompt05_implemented_vs_mocked.md",
    "qa/prompt05_test_report.md",
    "qa/prompt05_known_gaps.md",
    "qa/before_after_visual_report.md",
    "HANDOFF/PROMPT05_HARD_QUESTIONS.md",
    "HANDOFF/PROMPT05_MORNING_BRIEF.md",
    "HANDOFF/PROMPT05_BUILD_STATUS.md",
    "HANDOFF/PROMPT05_TOP_FINDINGS.md",
    "HANDOFF/PROMPT05_NEXT_72_HOURS.md",
    "HANDOFF/PROMPT05_VISUAL_CHANGELOG.md",
]

REQUIRED_PROMPT05_DIRS = [
    "design",
    "ranking",
    "alerts",
    "employer",
    "mobile",
    "desktop",
    "copy",
    "build",
    "demo/screens/before",
    "demo/screens/after",
]


def test_prompt05_artifacts_exist_and_are_non_empty() -> None:
    missing = []
    empty = []

    for relative_path in REQUIRED_PROMPT05_FILES:
        path = REPO_ROOT / relative_path
        if not path.exists():
            missing.append(relative_path)
        elif path.is_file() and not path.read_text(encoding="utf-8").strip():
            empty.append(relative_path)

    assert not missing, f"Missing Prompt #05 artifacts: {missing}"
    assert not empty, f"Empty Prompt #05 artifacts: {empty}"


def test_prompt05_directories_exist() -> None:
    missing = [
        relative_path
        for relative_path in REQUIRED_PROMPT05_DIRS
        if not (REPO_ROOT / relative_path).exists()
    ]
    assert not missing, f"Missing Prompt #05 directories: {missing}"
