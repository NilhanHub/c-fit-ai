"""Stage deterministic scoring, simulation candidates, and finalist stress tests."""

from __future__ import annotations

from validation.provenance import DEFAULT_RETRIEVED_AT, require_provenance


def _stage_counts(target_scale: int) -> tuple[int, int]:
    if target_scale <= 100:
        return 25, 10
    if target_scale >= 1000:
        return 250, 50
    stage_2 = max(25, round(target_scale * 0.25))
    stage_3 = max(10, round(target_scale * 0.1))
    return stage_2, stage_3


def run_experiment(
    *,
    experiment_id: str,
    offer_batch_id: str,
    market_slice_id: str,
    scenario_pack: list[str],
    scorecards: list[dict],
    target_scale: int,
    random_seed: int,
    evidence_refs: list[str],
    claim_type: str = "INFERENCE",
    retrieved_at: str = DEFAULT_RETRIEVED_AT,
) -> dict:
    if not scenario_pack:
        raise ValueError("scenario_pack must include at least one scenario")
    if not scorecards:
        raise ValueError("scorecards must include at least one ranked scorecard")

    ranked = sorted(
        scorecards,
        key=lambda item: (item["final_rank_score"], item["weighted_score"], item["offer_id"]),
        reverse=True,
    )
    stage_2_count, stage_3_count = _stage_counts(target_scale)
    stage_2_candidates = [item["offer_id"] for item in ranked[:stage_2_count]]
    stage_3_finalists = [item["offer_id"] for item in ranked[:stage_3_count]]

    result = {
        "experiment_id": experiment_id,
        "offer_batch_id": offer_batch_id,
        "market_slice_id": market_slice_id,
        "scenario_pack": scenario_pack,
        "random_seed": random_seed,
        "selection_rule": f"top{stage_2_count}_then_top{stage_3_count}",
        "stage_1_population": len(scorecards),
        "stage_2_candidates": stage_2_candidates,
        "stage_3_finalists": stage_3_finalists,
        "claim_type": claim_type,
        "retrieved_at": retrieved_at,
        "evidence_refs": evidence_refs,
    }
    require_provenance(result)
    return result
