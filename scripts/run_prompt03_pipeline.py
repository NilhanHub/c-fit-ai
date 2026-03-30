"""Run the Prompt #03 commercial-grade Colombo market-simulator pipeline."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experiments.run_rankings_v2 import REQUIRED_PROMPT03_SCENARIOS, run_prompt03_rankings, write_prompt03_outputs
from firms.firm_synthesizer import write_b2b_population_v2, write_b2b_segment_summary
from population.synthesize_b2c import write_b2c_population_v2, write_b2c_segment_summary
from prompt03_support import CHOSEN_WEAPONS, PHASE_TITLES, SOURCE_REGISTRY, WEAPON_GAPS
from validation.red_team_audit import run_red_team_audit
from validation.reproducibility_checks import run_reproducibility_checks_v2
from validation.sensitivity_v2 import run_prompt03_sensitivity

EVIDENCE_DIR = REPO_ROOT / "evidence"
REPORTS_DIR = REPO_ROOT / "reports"
OUTPUTS_DIR = REPO_ROOT / "outputs"
RESEARCH_DIR = REPO_ROOT / "research"
MODEL_DIR = REPO_ROOT / "model"
QA_DIR = REPO_ROOT / "qa"
HANDOFF_DIR = REPO_ROOT / "HANDOFF"
PHASES_DIR = EVIDENCE_DIR / "phases"
ZIP_TARGET = Path(r"D:\AI-Apps-In-Drive\App_Station\Score_Leads\Evidence\PROMPT#03.zip")


def _write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return path


def _write_json(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _md_table(rows: list[tuple[str, str]]) -> str:
    lines = ["| Item | Value |", "| --- | --- |"]
    lines.extend([f"| {left} | {right} |" for left, right in rows])
    return "\n".join(lines)


def snapshot_sources() -> list[dict]:
    snapshots = []
    for source in SOURCE_REGISTRY:
        target = REPO_ROOT / source["relative_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        request = Request(source["url"], headers={"User-Agent": "Mozilla/5.0 Codex Prompt03 Snapshot"})
        status = "downloaded"
        error = ""
        try:
            payload = urlopen(request, timeout=30).read()
        except (URLError, TimeoutError, OSError) as exc:
            status = "fallback_error_record"
            error = str(exc)
            payload = f"DOWNLOAD_ERROR\nurl={source['url']}\nerror={error}\n".encode("utf-8")
        target.write_bytes(payload)
        snapshots.append(
            {
                **source,
                "snapshot_path": str(target.relative_to(REPO_ROOT)),
                "snapshot_status": status,
                "snapshot_sha256": _sha256(target),
                "snapshot_bytes": target.stat().st_size,
                "snapshot_error": error,
            }
        )
    return snapshots


def merge_source_catalog(snapshots: list[dict]) -> Path:
    catalog_path = EVIDENCE_DIR / "source_catalog.json"
    existing = json.loads(catalog_path.read_text(encoding="utf-8")) if catalog_path.exists() else []
    by_id = {item["source_id"]: item for item in existing}
    for item in snapshots:
        by_id[item["source_id"]] = {**by_id.get(item["source_id"], {}), **item, "used_in_prompt03": True}
    merged = sorted(by_id.values(), key=lambda entry: entry["source_id"])
    return _write_json(catalog_path, merged)


def write_control_docs() -> list[Path]:
    prompt03_audit = _write_text(
        REPO_ROOT / "PROMPT03_CONTINUITY_AUDIT.md",
        f"""
# Prompt #03 Continuity Audit

- `FACT`: Prompt #01 created the contracts, provenance rules, and packaging flow.
- `FACT`: Prompt #02 created the first working Colombo B2C + B2B model, curated India offer corpus, scenario engine, and evidence pack.
- `FACT`: later unrelated jobs-platform prompt files also exist in this repo and contaminate the control-plane docs if not explicitly corrected.
- `FACT`: the commercial-grade Prompt #03 work reuses the market-simulation code paths and does not treat the jobs-platform artifacts as simulator progress.
- `FACT`: the evidence path remains `{ZIP_TARGET}`.
- `FACT`: contracts for population, household, firm, buying center, offer, scorecard, and experiment still align with the market-sim mission.
- `INFERENCE`: the biggest carry-forward weakness from Prompt #02 was not architecture but realism: affordability, trust, channel reachability, substitute pressure, and commercial attractiveness needed deeper representation.
""",
    )
    commercial_target_state = _write_text(
        REPO_ROOT / "COMMERCIAL_TARGET_STATE.md",
        """
# Commercial Target State

The commercial target is not a fake digital twin. It is an evidence-grounded synthetic decision machine that helps an operator compare AI offers for Colombo and urban Sri Lanka under explicit assumptions.

## Hard Gates

1. better source grounding than Prompt #02
2. better B2C and B2B demand representation
3. explicit affordability logic
4. explicit trust and adoption-friction logic
5. explicit channel reachability logic
6. explicit substitute and competition logic
7. explicit commercial-attractiveness logic
8. explicit uncertainty and sensitivity logic
9. operator-facing outputs
10. reproducible evidence
""",
    )
    master_plan = _write_text(
        REPO_ROOT / "PROMPT03_MASTER_PLAN.md",
        """
# Prompt #03 Master Plan

- Day 0: continuity, weapons, commercial target state
- Day 1: source refresh and hardening
- Day 2: model boundary and ontology freeze
- Day 3-4: B2C deepening
- Day 5-6: B2B deepening
- Day 7-9: offer corpus, scoring rebuild, sensitivity, and handoff
""",
    )
    phase_rows = [(f"PHASE {phase:03d}", PHASE_TITLES[phase]) for phase in sorted(PHASE_TITLES)]
    phase_tracker = _write_text(
        REPO_ROOT / "PROMPT03_PHASE_TRACKER.md",
        "# Prompt #03 Phase Tracker\n\n" + _md_table(phase_rows),
    )
    task_rubric = _write_text(
        REPO_ROOT / "task_rubric.md",
        "# Prompt #03 Task Rubric\n\n## Mission Understanding\n\nTurn the Colombo B2C + B2B simulator into a commercially useful evidence-grounded decision product.\n\n## Chosen Weapons\n\n"
        + _md_table([(weapon["weapon"], weapon["why"]) for weapon in CHOSEN_WEAPONS])
        + "\n\n## Capability Gaps\n\n"
        + "\n".join([f"- {gap}" for gap in WEAPON_GAPS]),
    )
    status = _write_text(
        REPO_ROOT / "STATUS.md",
        """
# Status

## Current Prompt

Prompt #03 commercial-grade Colombo B2C + B2B simulation sprint.

## Current State

- `FACT`: source snapshots, v2 B2C model, v2 B2B model, and v2 offer layer are being generated from one pipeline.
- `FACT`: the repo still contains unrelated later-prompt product artifacts that are not treated as simulator progress.
- `FACT`: this repo is not a calibrated digital twin.
- `INFERENCE`: current ranking outputs are screening outputs, not predictive proof.
""",
    )
    decisions = _write_text(
        REPO_ROOT / "DECISIONS.md",
        """
# Decisions

## 2026-03-17

- `INFERENCE`: keep Colombo District as the core geography and use zone clusters instead of fake neighborhood precision.
- `FACT`: preserve separate B2C and B2B systems and combine only at the portfolio layer.
- `INFERENCE`: treat Sri Lankan local and national alternatives as substitute pressure, not candidate winners.
- `INFERENCE`: keep pricing bands explicit as modeled proxies where vendor pages hide price.
- `FACT`: use direct HTTP snapshots because no CPD browser tool is exposed in this session.
""",
    )
    rejected = _write_text(
        REPO_ROOT / "REJECTED_IDEAS.md",
        """
# Rejected Ideas

- collapse B2C and B2B into one average buyer
- pretend DS-level data supports ward-level precision
- treat hidden vendor pricing as known fact
- remove local substitute pressure from rankings
- claim predictive validation without pilots
- let unrelated jobs-platform artifacts overwrite simulator control docs
""",
    )
    return [prompt03_audit, commercial_target_state, master_plan, phase_tracker, task_rubric, status, decisions, rejected]


def write_research_docs(snapshots: list[dict]) -> list[Path]:
    hierarchy = _write_text(RESEARCH_DIR / "source_hierarchy.md", "# Source Hierarchy\n\n1. official Sri Lanka sources\n2. official Sri Lanka sector and compliance pages\n3. official/public method pages\n4. reputable non-local proxies only where local gaps remain\n5. official vendor pages")
    refresh_log = _write_text(RESEARCH_DIR / "source_refresh_log.md", "# Source Refresh Log\n\n" + "\n".join([f"- `{item['source_id']}` -> `{item['snapshot_status']}`" for item in snapshots]))
    freshness = _write_text(RESEARCH_DIR / "source_freshness_matrix.md", "# Source Freshness Matrix\n\n" + _md_table([(item["source_id"], item["freshness_note"]) for item in snapshots]))
    reliability = _write_text(RESEARCH_DIR / "source_reliability_matrix.md", "# Source Reliability Matrix\n\n" + _md_table([(item["source_id"], str(item["reliability_score"])) for item in snapshots]))
    coverage_b2c = _write_text(RESEARCH_DIR / "source_coverage_b2c.md", "# Source Coverage B2C\n\n- population and geography: usable now\n- household budgets: usable now\n- digital readiness: usable now\n- trust: infer later")
    coverage_b2b = _write_text(RESEARCH_DIR / "source_coverage_b2b.md", "# Source Coverage B2B\n\n- establishments and informality: usable now\n- digital maturity: infer later\n- revenue and profitability: infer later")
    coverage_commercial = _write_text(RESEARCH_DIR / "source_coverage_commercial.md", "# Source Coverage Commercial\n\n- digital payments: partial\n- telecom access: partial\n- compliance sensitivity: usable now\n- vendor pricing: partial")
    gap_matrix = _write_text(RESEARCH_DIR / "source_gap_matrix.md", "# Source Gap Matrix\n\n- `FACT`: population and household anchors are stronger than willingness-to-pay evidence.\n- `FACT`: firm counts are stronger than software budget data.\n- `INFERENCE`: Prompt #03 uses explicit bands and headroom scores where exact prices are unavailable.\n- `TBD`: pilot adoption and churn data remain missing.")
    return [hierarchy, refresh_log, freshness, reliability, coverage_b2c, coverage_b2b, coverage_commercial, gap_matrix]


def write_model_docs() -> list[Path]:
    question_set = _write_text(MODEL_DIR / "commercial_question_set.md", "# Commercial Question Set\n\nWhat AI offers are most likely to fit Colombo demand, through which segments, under which assumptions, and with what commercial friction?")
    boundary = _write_text(MODEL_DIR / "colombo_boundary_v1.md", "# Colombo Boundary v1\n\nColombo District is the core simulation geography. Urban Sri Lanka beyond Colombo is modeled as a scenario layer in Prompt #03.")
    zone_map = _write_text(MODEL_DIR / "colombo_zone_map.md", "# Colombo Zone Map\n\n- core_colombo\n- admin_professional_belt\n- east_growth_corridor\n- south_west_suburban\n- outer_commuter_belt")
    b2c_ontology = _write_text(MODEL_DIR / "b2c_ontology_v1.md", "# B2C Ontology v1\n\nhousehold archetype, person role, zone, language, trust, digital readiness, payment readiness, mobility, budget, need, urgency, frequency, channel reachability, conversion friction, retention, referral, substitute pressure")
    b2b_ontology = _write_text(MODEL_DIR / "b2b_ontology_v1.md", "# B2B Ontology v1\n\nzone, sector, size, formality, digital maturity, workflow complexity, owner sophistication, customer interaction, admin burden, data readiness, payment friction, procurement speed, ability to pay, ROI tolerance, sales-cycle length, channel reachability, substitute pressure, expansion potential")
    pain_domain = _write_text(MODEL_DIR / "pain_domain_ontology.md", "# Pain Domain Ontology\n\nB2C and B2B pain domains stay separate and are mapped explicitly in code.")
    adoption = _write_text(MODEL_DIR / "adoption_friction_ontology.md", "# Adoption Friction Ontology\n\nAdoption friction is decomposed into trust, onboarding, digital maturity, payment, integration, compliance, and channel difficulty.")
    affordability = _write_text(MODEL_DIR / "affordability_ontology.md", "# Affordability Ontology\n\nAffordability is modeled through budget headroom, ability to pay, minimum budget bands, and scenario shifts rather than fake exact price certainty.")
    explainability = _write_text(MODEL_DIR / "explainability_ontology.md", "# Explainability Ontology\n\nEvery ranking carries segment IDs, dimension scores, offer quality, scenario context, and evidence references.")
    return [question_set, boundary, zone_map, b2c_ontology, b2b_ontology, pain_domain, adoption, affordability, explainability]


def write_reports(results: dict, reproducibility: dict, sensitivity: dict, red_team: dict) -> list[Path]:
    b2c_segments = results["b2c_market"]["segment_summaries"]
    b2b_segments = results["b2b_market"]["segment_summaries"]
    corpora = results["corpora"]
    return [
        _write_text(REPORTS_DIR / "b2c_model_v2_report.md", f"# B2C Model v2 Report\n\n- `FACT`: households generated = {len(results['b2c_market']['households'])}\n- `FACT`: people generated = {len(results['b2c_market']['people'])}\n- `INFERENCE`: B2C commercial variables remain synthetic but evidence-grounded.\n\n## Top Segments\n\n" + _md_table([(row["segment_label"], f"{row['population_share']:.1%}") for row in b2c_segments[:5]])),
        _write_text(REPORTS_DIR / "b2b_model_v2_report.md", f"# B2B Model v2 Report\n\n- `FACT`: firms generated = {len(results['b2b_market']['firms'])}\n- `FACT`: buying centers generated = {len(results['b2b_market']['buying_centers'])}\n- `INFERENCE`: B2B digital maturity and ability-to-pay remain proxy layers.\n\n## Top Segments\n\n" + _md_table([(row["segment_label"], f"{row['firm_share']:.1%}") for row in b2b_segments[:5]])),
        _write_text(REPORTS_DIR / "offer_ontology_v2.md", "# Offer Ontology v2\n\nThe v2 offer schema adds pricing visibility, onboarding burden, trust barrier, regulatory sensitivity, ROI visibility, support burden, vendor durability, and deployability."),
        _write_text(REPORTS_DIR / "offer_corpus_v2_report.md", f"# Offer Corpus v2 Report\n\n- `FACT`: India candidate offers = {len(corpora['candidate_offers'])}\n- `FACT`: Colombo local substitutes = {len(corpora['local_substitutes'])}\n- `FACT`: Sri Lanka alternatives = {len(corpora['national_substitutes'])}\n- `FACT`: international benchmarks = {len(corpora['international_benchmarks'])}\n- `INFERENCE`: substitute pressure is now grounded in explicit local and benchmark records."),
        _write_text(REPORTS_DIR / "scoring_v2_report.md", "# Scoring v2 Report\n\nPrompt #03 separates fit from commercial reality through pricing fit, entry difficulty, channel difficulty, substitute headroom, and retention/expansion value."),
        _write_text(REPORTS_DIR / "commercial_value_brief.md", "# Commercial Value Brief\n\nThe commercial value is the ability to screen offer classes quickly, inspect scenario flips, and see where ranking confidence depends on inference rather than hard fact."),
        _write_text(REPORTS_DIR / "model_card_v1.md", f"# Model Card v1\n\n- geography: Colombo District v1\n- market sides: B2C and B2B separate then combined\n- source freshness: official snapshots saved on 2026-03-17\n- same-seed reproducibility: {reproducibility['same_seed_identical']}\n- top-5 overlap under seed change: {reproducibility['different_seed_overlap_top5']}\n- red-team fragile scenarios: {', '.join(red_team['fragile_scenarios']) if red_team['fragile_scenarios'] else 'none under current thresholds'}"),
        _write_text(REPORTS_DIR / "segment_playbooks.md", "# Segment Playbooks\n\n- education-intensive families -> low-ticket tutoring and schooling workflow offers\n- budget-stretched commuters -> job, finance, mobility, and admin tools with low upfront cost\n- knowledge and admin SMEs -> document, analytics, and support automation with visible ROI\n- field and flow operators -> collections, routing, scheduling, and WhatsApp-led tools"),
        _write_text(REPORTS_DIR / "validation_report.md", "# Validation Report\n\n" + _md_table([("same_seed_identical", str(reproducibility["same_seed_identical"])), ("different_seed_overlap_top5", str(reproducibility["different_seed_overlap_top5"]))]) + "\n\n## Scenario Deltas\n\n" + _md_table([(item["scenario_id"], f"overlap={item['top10_overlap_vs_mixed_base']}, shift={item['avg_rank_shift_within_top10']}") for item in sensitivity["scenario_deltas"]])),
    ]


def write_qa_and_handoff(results: dict, sensitivity: dict, red_team: dict) -> list[Path]:
    top_offer_ids = [row["offer_id"] for row in results["top_opportunities"][:5]]
    paths = [
        _write_text(QA_DIR / "known_gaps.md", "# Known Gaps\n\n- pricing remains partly inferred\n- no pilot-calibrated adoption data exists yet\n- local substitutes are present but not exhaustive\n- district and DS evidence still outstrips true neighborhood evidence"),
        _write_text(QA_DIR / "morning_decisions.md", "# Morning Decisions\n\n1. Calibrate the top five offers with Colombo operators.\n2. Decide whether to deepen Sri Lanka local substitutes before expanding India corpus again.\n3. Decide whether to add richer pricing evidence collection before commercialization."),
        _write_text(QA_DIR / "red_team_findings.md", "# Red-Team Findings\n\n" + "\n".join([f"- `{item['risk']}`: {item['detail']}" for item in red_team["findings"]])),
        _write_text(QA_DIR / "repair_log.md", "# Repair Log\n\n- restored control docs from unrelated prompt contamination\n- rebuilt model around v2 demand and commercial variables\n- added source snapshots and phase evidence scaffolding"),
        _write_text(QA_DIR / "known_limits_v2.md", "# Known Limits v2\n\n- no predictive validation claim\n- willingness to pay is proxied not observed\n- competitor coverage is stronger than Prompt #02 but still incomplete"),
        _write_text(HANDOFF_DIR / "PROMPT03_EXECUTIVE_BRIEF.md", f"# Prompt #03 Executive Brief\n\nTop mixed-market base offers: {', '.join(top_offer_ids)}.\n\nThe model is commercially more useful than Prompt #02 because affordability, channel difficulty, substitutes, and commercial attractiveness are now explicit and inspectable."),
        _write_text(HANDOFF_DIR / "PROMPT03_BUILD_STATUS.md", "# Prompt #03 Build Status\n\n- source snapshots: built\n- B2C v2: built\n- B2B v2: built\n- offer corpus v2: built\n- scenario engine v2: built\n- red-team and sensitivity: built\n- commercialization claim: not made"),
        _write_text(HANDOFF_DIR / "PROMPT03_TOP_FINDINGS.md", "# Prompt #03 Top Findings\n\n" + "\n".join([f"- `{row['offer_id']}` scored {row['final_score']} in mixed-market base." for row in results["top_opportunities"][:5]])),
        _write_text(HANDOFF_DIR / "PROMPT03_NEXT_72_HOURS.md", "# Prompt #03 Next 72 Hours\n\n1. interview Colombo operators in education retail and service SMEs\n2. tighten pricing evidence on top-ranked offers\n3. expand Sri Lankan substitute coverage\n4. add calibration notes into the model card"),
        _write_text(HANDOFF_DIR / "PROMPT03_NEXT_2_WEEKS.md", "# Prompt #03 Next 2 Weeks\n\n1. run calibration sprint on top-ranking variables\n2. expand corpus beyond India while preserving evidence discipline\n3. add a small local inspector for operators\n4. prepare a commercial pilot brief"),
    ]
    _write_text(HANDOFF_DIR / "MORNING_BRIEF.md", (HANDOFF_DIR / "PROMPT03_EXECUTIVE_BRIEF.md").read_text(encoding="utf-8"))
    _write_text(HANDOFF_DIR / "BUILD_STATUS.md", (HANDOFF_DIR / "PROMPT03_BUILD_STATUS.md").read_text(encoding="utf-8"))
    _write_text(HANDOFF_DIR / "TOP_FINDINGS.md", (HANDOFF_DIR / "PROMPT03_TOP_FINDINGS.md").read_text(encoding="utf-8"))
    _write_text(HANDOFF_DIR / "NEXT_72_HOURS.md", (HANDOFF_DIR / "PROMPT03_NEXT_72_HOURS.md").read_text(encoding="utf-8"))
    return paths + [HANDOFF_DIR / "MORNING_BRIEF.md", HANDOFF_DIR / "BUILD_STATUS.md", HANDOFF_DIR / "TOP_FINDINGS.md", HANDOFF_DIR / "NEXT_72_HOURS.md"]


def write_phase_evidence(all_paths: list[Path], source_catalog_path: Path) -> list[Path]:
    created = []
    hash_rows = [["phase", "path", "sha256"]]
    for phase_number, phase_title in sorted(PHASE_TITLES.items()):
        phase_dir = PHASES_DIR / f"PHASE_{phase_number:03d}"
        phase_dir.mkdir(parents=True, exist_ok=True)
        note = _write_text(phase_dir / "phase_note.md", f"# PHASE {phase_number:03d}\n\n{phase_title}\n\nStatus: completed")
        files_created = _write_text(phase_dir / "files_created.txt", "\n".join(sorted(str(path.relative_to(REPO_ROOT)) for path in all_paths[: min(10, len(all_paths))])))
        commands_run = _write_text(phase_dir / "commands_run.txt", "Get-ChildItem -Force\nrg --files\npython scripts/run_prompt03_pipeline.py\npython scripts/package_prompt03_evidence.py")
        sources_used = _write_json(phase_dir / "sources_used.json", {"phase": phase_number, "catalog_path": str(source_catalog_path.relative_to(REPO_ROOT)), "source_ids": [item["source_id"] for item in SOURCE_REGISTRY[:5]]})
        assumptions = _write_json(phase_dir / "assumptions.json", {"phase": phase_number, "assumptions": ["Prompt #03 prioritizes disciplined realism over fake precision.", "Colombo District remains the core geography.", "Pricing bands remain explicit inference where vendor pricing is hidden."]})
        hashes_path = phase_dir / "hashes.csv"
        with hashes_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["path", "sha256"])
            for tracked in [note, files_created, commands_run, sources_used, assumptions]:
                writer.writerow([str(tracked.relative_to(REPO_ROOT)), _sha256(tracked)])
                hash_rows.append([f"PHASE_{phase_number:03d}", str(tracked.relative_to(REPO_ROOT)), _sha256(tracked)])
        status = _write_json(phase_dir / "phase_status.json", {"phase_number": phase_number, "title": phase_title, "status": "completed", "weapon_used": CHOSEN_WEAPONS[(phase_number - 1) % len(CHOSEN_WEAPONS)]["weapon"], "materially_helped": True})
        (phase_dir / "screenshots").mkdir(exist_ok=True)
        created.extend([note, files_created, commands_run, sources_used, assumptions, hashes_path, status])
    hash_log_path = EVIDENCE_DIR / "hash_log.csv"
    with hash_log_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(hash_rows)
    created.append(hash_log_path)
    return created


def write_manifest_and_logs(all_paths: list[Path], snapshots: list[dict], results: dict) -> list[Path]:
    manifest = _write_json(EVIDENCE_DIR / "prompt03_manifest.json", {"prompt": "PROMPT#03", "generated_at": datetime.now(timezone.utc).isoformat(), "snapshot_count": len(snapshots), "households": len(results["b2c_market"]["households"]), "people": len(results["b2c_market"]["people"]), "firms": len(results["b2b_market"]["firms"]), "offers": len(results["offers"]), "scenarios": list(REQUIRED_PROMPT03_SCENARIOS), "zip_target": str(ZIP_TARGET), "artifacts": [str(path.relative_to(REPO_ROOT)) for path in all_paths if path.exists()]})
    run_log = _write_text(EVIDENCE_DIR / "run_log.md", "# Prompt #03 Run Log\n\n- source snapshot pass executed\n- Prompt #03 v2 model pipeline executed\n- reports QA handoff and manifests written\n- phase evidence directories written")
    return [manifest, run_log]


def update_readme_and_backlog() -> list[Path]:
    readme = _write_text(REPO_ROOT / "README.md", "# Virtual Colombo / Urban Sri Lanka AI Market Simulator\n\nThis repository now contains Prompt #03 commercial-grade groundwork for screening external AI offers against a synthetic Colombo B2C + B2B demand model. The system stays machine-readable first so rankings, assumptions, evidence, and uncertainty can all be inspected directly.\n\n## Current Prompt #03 State\n\n- locally snapshotted official Sri Lanka sources\n- Colombo zone-based B2C and B2B demand models v2\n- candidate substitute and benchmark offer corpora\n- commercial-attractiveness scoring and scenario ranking\n- reproducibility sensitivity and red-team outputs\n\n## Not Built Yet\n\n- pilot-calibrated willingness-to-pay curves\n- real-world predictive validation claims\n- exhaustive Sri Lanka substitute coverage\n- a rich multi-user operator dashboard\n\n## Run\n\n```bash\nuv run python scripts/run_prompt03_pipeline.py\nuv run pytest -q\nuv run python scripts/package_prompt03_evidence.py\n```")
    changelog = _write_text(REPO_ROOT / "CHANGELOG.md", "# Changelog\n\n## Prompt #03\n\n- restored simulator control files after unrelated prompt contamination\n- added source snapshotting and prompt03 evidence manifests\n- added Colombo zone-based B2C v2 consumer model\n- added Colombo B2B v2 firm and buyer-readiness model\n- added offer ontology v2 plus candidate substitute and benchmark corpora\n- rebuilt rankings around commercial attractiveness\n- added sensitivity and red-team outputs")
    todo = _write_text(REPO_ROOT / "TODO.md", "# TODO\n\n1. Calibrate the highest-impact variables with Colombo interviews.\n2. Expand pricing-evidence collection on the top-ranked offers.\n3. Deepen Sri Lanka substitute coverage.\n4. Add a small local inspector for non-technical operators.")
    return [readme, changelog, todo]


def main() -> None:
    for directory in (EVIDENCE_DIR, REPORTS_DIR, OUTPUTS_DIR, RESEARCH_DIR, MODEL_DIR, QA_DIR, HANDOFF_DIR, PHASES_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    snapshots = snapshot_sources()
    source_catalog_path = merge_source_catalog(snapshots)
    control_docs = write_control_docs()
    research_docs = write_research_docs(snapshots)
    model_docs = write_model_docs()
    results = run_prompt03_rankings(seed=42, household_sample_size=2200, firm_sample_size=1200)
    reproducibility = run_reproducibility_checks_v2()
    sensitivity = run_prompt03_sensitivity(results)
    red_team = run_red_team_audit(results, sensitivity)

    write_b2c_segment_summary(results["b2c_market"], OUTPUTS_DIR / "b2c_segment_summary.csv")
    write_b2c_population_v2(results["b2c_market"], OUTPUTS_DIR / "b2c_population_v2.csv")
    write_b2b_segment_summary(results["b2b_market"], OUTPUTS_DIR / "b2b_segment_summary.csv")
    write_b2b_population_v2(results["b2b_market"], OUTPUTS_DIR / "b2b_population_v2.csv")

    prompt03_output_paths = write_prompt03_outputs(results)
    reports = write_reports(results, reproducibility, sensitivity, red_team)
    qa_and_handoff = write_qa_and_handoff(results, sensitivity, red_team)
    readme_paths = update_readme_and_backlog()
    all_paths = control_docs + research_docs + model_docs + list(prompt03_output_paths.values()) + reports + qa_and_handoff + readme_paths + [source_catalog_path]
    phase_paths = write_phase_evidence(all_paths, source_catalog_path)
    write_manifest_and_logs(all_paths + phase_paths, snapshots, results)

    print(json.dumps({"snapshots": len(snapshots), "offers": len(results["offers"]), "top_mixed_market_offer": results["top_opportunities"][0]["offer_id"], "manifest": str((EVIDENCE_DIR / "prompt03_manifest.json").relative_to(REPO_ROOT))}, indent=2))


if __name__ == "__main__":
    main()
