"""Planning interface for Colombo-first synthetic population synthesis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PopulationSynthesisConfig:
    geography_scope: str
    target_households: int
    target_individuals: int
    seed_dataset_refs: list[str]


@dataclass(frozen=True)
class PopulationSynthesisPlan:
    geography_scope: str
    target_households: int
    target_individuals: int
    seed_dataset_refs: list[str]
    method: str
    calibration_status: str
    contracts: list[str]
    notes: list[str]


def build_population(config: PopulationSynthesisConfig) -> PopulationSynthesisPlan:
    if config.target_households <= 0 or config.target_individuals <= 0:
        raise ValueError("Population targets must be positive integers")
    if not config.seed_dataset_refs:
        raise ValueError("seed_dataset_refs must include at least one evidence-backed source")

    return PopulationSynthesisPlan(
        geography_scope=config.geography_scope,
        target_households=config.target_households,
        target_individuals=config.target_individuals,
        seed_dataset_refs=config.seed_dataset_refs,
        method="hierarchical_seeded_ipf",
        calibration_status="seeded",
        contracts=["household_entity.schema.yaml", "population_entity.schema.yaml"],
        notes=[
            "FACT: uses explicit seed references instead of hidden priors",
            "INFERENCE: household and individual synthesis logic will be calibrated in later prompts",
        ],
    )
