"""Prompt #03 B2B sector taxonomy for Colombo commercial demand."""

from __future__ import annotations

from firms.prompt03_b2b_core import SECTOR_LABELS_V2, load_firm_archetypes_v2


def load_b2b_sector_taxonomy_v2() -> list[dict]:
    seen = set()
    rows = []
    for archetype in load_firm_archetypes_v2():
        sector_id = archetype["sector_id"]
        if sector_id in seen:
            continue
        seen.add(sector_id)
        rows.append({"sector_id": sector_id, "sector_label": SECTOR_LABELS_V2[sector_id]})
    return sorted(rows, key=lambda item: item["sector_id"])
