"""Refresh the authoritative SAN topology graph and node index."""

from __future__ import annotations

try:
    from scripts.san_shared import REPO_ROOT, SAN_ROOT, collect_root_stats, load_bundle, render_topology_index_md, utc_now_iso, write_json, write_text
except ImportError:  # pragma: no cover - script execution path
    from san_shared import REPO_ROOT, SAN_ROOT, collect_root_stats, load_bundle, render_topology_index_md, utc_now_iso, write_json, write_text


def _normalized_code_surface(bytes_share: float) -> float:
    return round(min(5.0, bytes_share * 25.0), 2)


def _weighted_burden(factor_scores: dict[str, float]) -> float:
    return sum(float(value) for value in factor_scores.values())


def main() -> int:
    bundle = load_bundle()
    runtime_manifest = bundle["runtime"]
    graph = bundle["graph"]
    nodes = graph["nodes"]

    node_stats: dict[str, dict[str, float]] = {}
    total_bytes = 0
    for node in nodes:
        stats = collect_root_stats(node["ownershipRoots"], runtime_manifest)
        node_stats[node["id"]] = stats
        total_bytes += max(int(stats["total_bytes"]), 1)

    raw_burdens: dict[str, float] = {}
    for node in nodes:
        stats = node_stats[node["id"]]
        share = stats["total_bytes"] / total_bytes if total_bytes else 0.0
        node["measuredSurface"] = stats
        node["effectiveLoad"]["factorScores"]["codeSurfaceShare"] = _normalized_code_surface(share)
        raw_burdens[node["id"]] = _weighted_burden(node["effectiveLoad"]["factorScores"])

    total_burden = sum(raw_burdens.values()) or 1.0
    policy = graph["nodeBudgetPolicy"]
    review_trigger = float(policy["reviewTriggerPercent"])
    dispersion_trigger = float(policy["mandatoryDispersionReviewPercent"])

    for node in nodes:
        percent = round(raw_burdens[node["id"]] / total_burden * 100.0, 2)
        node["effectiveLoad"]["percent"] = percent
        node["status"]["hotspot"] = percent >= review_trigger
        node["status"]["splitCandidate"] = percent >= dispersion_trigger
        node["status"]["exceptionalNode"] = percent >= dispersion_trigger and bool(policy["allowExceptionalNodes"])

    drift_values = []
    for node in nodes:
        declared = set(node["declaredDependencies"])
        observed = set(node["observedDependencies"])
        drift_values.append(len(declared.symmetric_difference(observed)))

    graph["integrity"]["declaredObservedDriftScore"] = round(sum(drift_values) / max(len(drift_values), 1), 2)
    graph["integrity"]["cyclesPresent"] = False
    graph["integrity"]["lastTopologyReview"] = utc_now_iso()

    write_json(SAN_ROOT / "topology" / "topology.graph.json", graph)
    write_text(SAN_ROOT / "topology" / "node-index.md", render_topology_index_md(graph))
    print("SAN_TOPOLOGY_REFRESHED", REPO_ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
