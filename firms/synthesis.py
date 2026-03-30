"""Planning interface for Colombo-first synthetic firm synthesis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FirmSynthesisConfig:
    geography_scope: str
    target_firms: int
    seed_dataset_refs: list[str]
    sector_focus: list[str]


@dataclass(frozen=True)
class FirmSynthesisPlan:
    geography_scope: str
    target_firms: int
    seed_dataset_refs: list[str]
    sector_focus: list[str]
    method: str
    calibration_status: str
    contracts: list[str]
    notes: list[str]


def build_firms(config: FirmSynthesisConfig) -> FirmSynthesisPlan:
    if config.target_firms <= 0:
        raise ValueError("target_firms must be positive")
    if not config.seed_dataset_refs:
        raise ValueError("seed_dataset_refs must include at least one evidence-backed source")
    if not config.sector_focus:
        raise ValueError("sector_focus must include at least one sector")

    return FirmSynthesisPlan(
        geography_scope=config.geography_scope,
        target_firms=config.target_firms,
        seed_dataset_refs=config.seed_dataset_refs,
        sector_focus=config.sector_focus,
        method="sector_size_seeded_sampler",
        calibration_status="seeded",
        contracts=["firm_entity.schema.yaml", "buying_center.schema.yaml"],
        notes=[
            "FACT: firm and buying-center generation remain separate from offer scoring",
            "TBD: procurement behaviors need later calibration with pilot evidence",
        ],
    )
