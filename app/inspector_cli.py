"""Small CLI inspector for Prompt #03 ranking outputs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "outputs" / "scenario_comparison.csv"


def load_rows() -> list[dict]:
    with SCENARIO_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect Prompt #03 scenario rankings.")
    parser.add_argument("--scenario", default="mixed_market_base", help="Scenario ID to inspect")
    parser.add_argument("--limit", type=int, default=10, help="Maximum rows to print")
    args = parser.parse_args()

    rows = [row for row in load_rows() if row["scenario_id"] == args.scenario][: args.limit]
    for row in rows:
        print(f"{row['rank']:>2}  {row['vendor_name']} / {row['offer_name']}  score={row['final_score']}  market={row['dominant_market']}")


if __name__ == "__main__":
    main()
