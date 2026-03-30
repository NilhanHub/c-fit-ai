"""Build Prompt #02 outputs, reports, and evidence artifacts from the working model."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from experiments.run_rankings import REQUIRED_SCENARIOS, run_all_rankings, write_ranking_outputs
from firms.firm_synthesizer import write_b2b_segment_summary
from offers.offer_normalizer import load_curated_offer_corpus
from population.synthesize_b2c import write_b2c_segment_summary
from scoring.b2b_dimensions import B2B_DIMENSION_WEIGHTS
from scoring.b2c_dimensions import B2C_DIMENSION_WEIGHTS
from validation.reproducibility_checks import run_reproducibility_checks
from validation.sensitivity import run_sensitivity_analysis


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
OUTPUTS_DIR = REPO_ROOT / "outputs"
QA_DIR = REPO_ROOT / "qa"
HANDOFF_DIR = REPO_ROOT / "HANDOFF"
EVIDENCE_DIR = REPO_ROOT / "evidence"

PROMPT02_SOURCE_ENTRIES = [
    {
        "source_id": "dcs-census-2024-colombo-population",
        "title": "DCS Census 2024 Colombo District Population",
        "url": "https://www.statistics.gov.lk/Census/PopulationAndHousing2024",
        "source_type": "official",
        "claim_type": "FACT",
        "usage": "Colombo District population and density anchors",
        "reliability_score": 5,
    },
    {
        "source_id": "dcs-census-2024-colombo-households",
        "title": "DCS Census 2024 Colombo District Households",
        "url": "https://www.statistics.gov.lk/Census/PopulationAndHousing2024",
        "source_type": "official",
        "claim_type": "FACT",
        "usage": "Colombo household count and average household size anchors",
        "reliability_score": 5,
    },
    {
        "source_id": "dcs-census-2012-colombo-age",
        "title": "DCS 2012 Colombo District Age Structure",
        "url": "https://www.statistics.gov.lk/Population/StaticalInformation/VitalStatistics/ByDistrictAndSex",
        "source_type": "official",
        "claim_type": "FACT",
        "usage": "Broad Colombo age-band weights for v0 population synthesis",
        "reliability_score": 4,
    },
    {
        "source_id": "dcs-census-2012-colombo-urban-households",
        "title": "DCS 2012 Colombo District Urban and Rural Households",
        "url": "https://www.statistics.gov.lk/Population/StaticalInformation/CPH2011",
        "source_type": "official",
        "claim_type": "FACT",
        "usage": "Area-cluster inference for Colombo urban concentration",
        "reliability_score": 4,
    },
    {
        "source_id": "dcs-non-agri-colombo-establishments",
        "title": "DCS Colombo Non-Agricultural Establishments",
        "url": "https://www.statistics.gov.lk/Economy/StaticalInformation/StaticalInformationByDistrict",
        "source_type": "official",
        "claim_type": "FACT",
        "usage": "Colombo establishment and size-share anchors for the B2B layer",
        "reliability_score": 4,
    },
    {
        "source_id": "dcs-trade-bulletin-colombo-retail-share",
        "title": "DCS Colombo Trade Establishment Retail Share",
        "url": "https://www.statistics.gov.lk/Economic/StaticalInformation/Trade",
        "source_type": "official",
        "claim_type": "FACT",
        "usage": "Retail-heavy Colombo sector mix proxy",
        "reliability_score": 4,
    },
    {
        "source_id": "yellow-offer",
        "title": "Yellow.ai official product site",
        "url": "https://yellow.ai/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "haptik-offer",
        "title": "Haptik official site",
        "url": "https://www.haptik.ai/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "leena-offer",
        "title": "Leena AI official site",
        "url": "https://leena.ai/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "engati-offer",
        "title": "Engati official site",
        "url": "https://www.engati.com/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "verloop-offer",
        "title": "Verloop.io official site",
        "url": "https://www.verloop.io/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "ameyo-offer",
        "title": "Ameyo official site",
        "url": "https://www.ameyo.com/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "infeedo-offer",
        "title": "Infeedo official site",
        "url": "https://www.infeedo.ai/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "embibe-offer",
        "title": "Embibe official site",
        "url": "https://www.embibe.com/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "wysa-offer",
        "title": "Wysa official site",
        "url": "https://www.wysa.com/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "fasal-offer",
        "title": "Fasal official site",
        "url": "https://fasal.co/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Weak-fit control offer in the corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "niramai-offer",
        "title": "NIRAMAI official site",
        "url": "https://www.niramai.com/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
    {
        "source_id": "rephrase-offer",
        "title": "Rephrase.ai official site",
        "url": "https://www.rephrase.ai/",
        "source_type": "vendor_official",
        "claim_type": "FACT",
        "usage": "Curated India AI offer corpus",
        "reliability_score": 2,
    },
]


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def _markdown_table(items: list[tuple[str, str]]) -> str:
    lines = ["| Item | Value |", "| --- | --- |"]
    lines.extend([f"| {item} | {value} |" for item, value in items])
    return "\n".join(lines)


def update_source_catalog() -> Path:
    catalog_path = EVIDENCE_DIR / "source_catalog.json"
    existing = json.loads(catalog_path.read_text(encoding="utf-8")) if catalog_path.exists() else []
    by_id = {item["source_id"]: item for item in existing}
    for entry in PROMPT02_SOURCE_ENTRIES:
        by_id[entry["source_id"]] = {**by_id.get(entry["source_id"], {}), **entry, "used_in_prompt02": True}

    merged = list(existing)
    existing_ids = {item["source_id"] for item in existing}
    for entry in PROMPT02_SOURCE_ENTRIES:
        if entry["source_id"] not in existing_ids:
            merged.append(by_id[entry["source_id"]])
        else:
            merged = [by_id[item["source_id"]] if item["source_id"] == entry["source_id"] else item for item in merged]

    catalog_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    return catalog_path


def _top_rankings(result_rows: list[dict], n: int = 5) -> list[str]:
    return [f"{index + 1}. {row['vendor_name']} / {row['offer_name']} ({row['final_score']})" for index, row in enumerate(result_rows[:n])]


def _write_reports(results: dict, reproducibility: dict, sensitivity: dict) -> list[Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    b2c_segments = results["b2c_market"]["segment_summaries"]
    b2b_segments = results["b2b_market"]["segment_summaries"]
    offers = results["offers"]
    mixed_top = results["scenario_rankings"]["mixed_market_base"][:10]
    market_side_counts = Counter(offer["market_side"] for offer in offers)
    domain_counts = Counter(offer["problem_domain"] for offer in offers)

    b2c_report = REPORTS_DIR / "b2c_model_report.md"
    _write_text(
        b2c_report,
        f"""
# B2C Model Report

- `FACT`: generated {len(results["b2c_market"]["households"])} synthetic households and {len(results["b2c_market"]["people"])} synthetic people for Colombo District v0.
- `INFERENCE`: household and person attributes are archetype-derived from official anchors, HIES, computer-literacy, and crisis-pressure proxies.

## Leading Consumer Segments

{_markdown_table([(row["segment_label"], f'{row["population_share"]:.1%}') for row in b2c_segments[:5]])}

## Uncertainty Flags

{chr(10).join(f"- {flag}" for flag in results["b2c_market"]["uncertainty_flags"])}
""",
    )

    b2b_report = REPORTS_DIR / "b2b_model_report.md"
    _write_text(
        b2b_report,
        f"""
# B2B Model Report

- `FACT`: generated {len(results["b2b_market"]["firms"])} synthetic firms and {len(results["b2b_market"]["buying_centers"])} buying centers for Colombo District v0.
- `INFERENCE`: sector pain and procurement behavior are modeled proxies anchored to official establishment structure.

## Leading Firm Segments

{_markdown_table([(row["segment_label"], f'{row["firm_share"]:.1%}') for row in b2b_segments[:5]])}

## Uncertainty Flags

{chr(10).join(f"- {flag}" for flag in results["b2b_market"]["uncertainty_flags"])}
""",
    )

    offer_report = REPORTS_DIR / "offer_corpus_report.md"
    _write_text(
        offer_report,
        f"""
# Offer Corpus Report

- `FACT`: curated corpus size = {len(offers)} official India-origin offer records.
- `FACT`: market-side mix = {dict(market_side_counts)}.
- `FACT`: top problem domains = {dict(domain_counts.most_common(6))}.
- `INFERENCE`: corpus breadth is enough for a serious v0 ranking pass, but not enough for market-coverage claims.
""",
    )

    b2c_framework = REPORTS_DIR / "b2c_scoring_framework.md"
    _write_text(
        b2c_framework,
        "# B2C Scoring Framework\n\n"
        + "\n".join([f"- `{name}` weight = {weight}" for name, weight in B2C_DIMENSION_WEIGHTS.items()])
        + "\n\n- `INFERENCE`: all scores are 0-100 higher-is-better after reverse-coding frictions.\n",
    )

    b2b_framework = REPORTS_DIR / "b2b_scoring_framework.md"
    _write_text(
        b2b_framework,
        "# B2B Scoring Framework\n\n"
        + "\n".join([f"- `{name}` weight = {weight}" for name, weight in B2B_DIMENSION_WEIGHTS.items()])
        + "\n\n- `INFERENCE`: all scores are 0-100 higher-is-better after reverse-coding frictions.\n",
    )

    ranking_report = REPORTS_DIR / "ranking_report.md"
    _write_text(
        ranking_report,
        f"""
# Ranking Report

## Mixed-Market Base Top Offers

{chr(10).join(f"- {line}" for line in _top_rankings(mixed_top))}

## Scenario Coverage

- `FACT`: scenarios run = {", ".join(REQUIRED_SCENARIOS)}.
- `INFERENCE`: the mixed-market base favors offers that can survive both budget constraints and channel reality.

## Sensitivity Snapshot

{_markdown_table([(row["scenario_id"], f'overlap={row["top10_overlap_vs_mixed_base"]}, shift={row["avg_rank_shift_within_top10"]}') for row in sensitivity["scenario_deltas"]])}
""",
    )

    validation_report = REPORTS_DIR / "validation_report.md"
    _write_text(
        validation_report,
        f"""
# Validation Report

- `FACT`: same-seed reproducibility = {reproducibility["same_seed_identical"]}.
- `FACT`: different-seed top-5 overlap = {reproducibility["different_seed_overlap_top5"]}.
- `INFERENCE`: high overlap under small seed changes suggests the top cluster is directionally stable, not validated.

## Scenario Stability

{_markdown_table([(row["scenario_id"], str(row["top10_overlap_vs_mixed_base"])) for row in sensitivity["scenario_deltas"]])}
""",
    )

    return [b2c_report, b2b_report, offer_report, b2c_framework, b2b_framework, ranking_report, validation_report]


def _write_handoff_and_qa(results: dict, sensitivity: dict) -> list[Path]:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    mixed_top = results["scenario_rankings"]["mixed_market_base"][:10]
    robust_counts: dict[str, int] = defaultdict(int)
    for scenario in results["scenario_results"]:
        for row in scenario["top_10"]:
            robust_counts[row["offer_id"]] += 1
    robust_offers = sorted(robust_counts.items(), key=lambda item: (-item[1], item[0]))[:5]

    _write_text(
        QA_DIR / "known_gaps.md",
        """
# Known Gaps

- district-level sources still stand in for neighborhood precision
- offer pricing remains partly inferred because many vendor pages hide pricing
- firm pain maps are workflow proxies, not survey-validated willingness-to-pay
- no real pilot outcomes or customer interviews are baked into Prompt #02
""",
    )
    _write_text(
        QA_DIR / "morning_decisions.md",
        """
# Morning Decisions

1. Decide whether Prompt #03 should deepen Colombo first or expand the geography scenario into a second synthetic build.
2. Decide which offer domains deserve manual calibration interviews first: education, multilingual support, or SMB support automation.
3. Decide whether to enrich the offer ontology with vertical-fit and pricing-evidence contracts.
""",
    )
    _write_text(
        HANDOFF_DIR / "BUILD_STATUS.md",
        """
# Build Status

- B2C generator: working
- B2B generator: working
- Curated India offer corpus: working
- Explainable B2C and B2B scoring: working
- Scenario ranking engine: working
- Validation and sensitivity layer: working
- Calibration claim: not made
""",
    )
    _write_text(
        HANDOFF_DIR / "TOP_FINDINGS.md",
        "# Top Findings\n\n"
        + "\n".join(
            [
                f"- `{offer_id}` appears in the top 10 of {count} scenarios."
                for offer_id, count in robust_offers
            ]
        )
        + "\n\n- `INFERENCE`: the most robust cluster favors education support, multilingual conversational support, and low-to-medium integration SMB automation.\n",
    )
    _write_text(
        HANDOFF_DIR / "MORNING_BRIEF.md",
        """
# Morning Brief

Prompt #02 turned the Prompt #01 scaffold into a working synthetic decision model for Colombo District. The repo now generates reproducible households, people, firms, and buying centers, loads a curated India-first AI offer corpus, scores each offer with transparent B2C and B2B logic, and ranks offers across nine scenarios.

Use the rankings as a learning tool, not as a calibration claim. The model is most useful right now for comparing offer classes, seeing why certain offers move under budget, trust, and digital-readiness shifts, and identifying where the next real-world calibration work should go.
""",
    )
    _write_text(
        HANDOFF_DIR / "NEXT_72_HOURS.md",
        """
# Next 72 Hours

1. Replace search-snippet anchors with downloaded local official tables or PDFs where possible.
2. Add vertical-fit fields and pricing-evidence fields to the normalized offer contract.
3. Interview or otherwise calibrate 3-5 Colombo operators in education, retail, and support-heavy SMEs.
4. Add richer segment-level contract enforcement for synthetic summaries.
5. Expand the curated corpus from India while preserving evidence quality.
""",
    )
    return [
        QA_DIR / "test_report.md",
        QA_DIR / "known_gaps.md",
        QA_DIR / "morning_decisions.md",
        HANDOFF_DIR / "BUILD_STATUS.md",
        HANDOFF_DIR / "TOP_FINDINGS.md",
        HANDOFF_DIR / "MORNING_BRIEF.md",
        HANDOFF_DIR / "NEXT_72_HOURS.md",
    ]


def _write_manifest(results: dict, report_paths: list[Path], extra_paths: list[Path]) -> list[Path]:
    manifest_path = EVIDENCE_DIR / "prompt02_manifest.json"
    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        "prompt": "PROMPT#02",
        "generated_at": now,
        "households": len(results["b2c_market"]["households"]),
        "people": len(results["b2c_market"]["people"]),
        "firms": len(results["b2b_market"]["firms"]),
        "buying_centers": len(results["b2b_market"]["buying_centers"]),
        "offers": len(results["offers"]),
        "scenarios": list(REQUIRED_SCENARIOS),
        "top_mixed_market_offer": results["scenario_rankings"]["mixed_market_base"][0]["offer_id"],
        "artifacts": [str(path.relative_to(REPO_ROOT)) for path in report_paths + extra_paths],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    hash_log = EVIDENCE_DIR / "hash_log.csv"
    tracked = report_paths + extra_paths + [manifest_path, OUTPUTS_DIR / "b2c_segment_summary.csv", OUTPUTS_DIR / "b2b_segment_summary.csv", OUTPUTS_DIR / "top_offers_base.csv", OUTPUTS_DIR / "top_offers_by_scenario.csv"]
    with hash_log.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "sha256"])
        for path in tracked:
            writer.writerow([str(path.relative_to(REPO_ROOT)), hashlib.sha256(path.read_bytes()).hexdigest()])

    run_log = EVIDENCE_DIR / "run_log.md"
    _write_text(
        run_log,
        f"""
# Prompt #02 Run Log

- Generated at: `{now}`
- Scenarios: `{', '.join(REQUIRED_SCENARIOS)}`
- Mixed-market base top offer: `{results["scenario_rankings"]["mixed_market_base"][0]["offer_id"]}`
- Note: this log records the pipeline artifact build, not the full terminal command transcript.
""",
    )
    return [manifest_path, hash_log, run_log]


def main() -> None:
    for directory in (REPORTS_DIR, OUTPUTS_DIR, QA_DIR, HANDOFF_DIR, EVIDENCE_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    update_source_catalog()
    results = run_all_rankings(seed=42, household_sample_size=1500, firm_sample_size=800)
    reproducibility = run_reproducibility_checks()
    sensitivity = run_sensitivity_analysis(results)

    write_b2c_segment_summary(results["b2c_market"], OUTPUTS_DIR / "b2c_segment_summary.csv")
    write_b2b_segment_summary(results["b2b_market"], OUTPUTS_DIR / "b2b_segment_summary.csv")
    write_ranking_outputs(results)
    report_paths = _write_reports(results, reproducibility, sensitivity)
    extra_paths = _write_handoff_and_qa(results, sensitivity)
    evidence_paths = _write_manifest(results, report_paths, extra_paths)

    print(
        json.dumps(
            {
                "reports": [str(path.relative_to(REPO_ROOT)) for path in report_paths],
                "handoff_and_qa": [str(path.relative_to(REPO_ROOT)) for path in extra_paths],
                "evidence": [str(path.relative_to(REPO_ROOT)) for path in evidence_paths],
                "offers": len(load_curated_offer_corpus()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
