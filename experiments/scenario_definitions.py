"""Prompt #02 scenario definitions for Colombo and urban Sri Lanka ranking runs."""

from __future__ import annotations


SCENARIOS = {
    "colombo_b2c_base": {
        "scenario_id": "colombo_b2c_base",
        "market_mode": "b2c",
        "description": "Consumer-side Colombo District base case.",
        "b2c_attribute_deltas": {},
        "b2c_share_multipliers": {},
    },
    "colombo_b2b_base": {
        "scenario_id": "colombo_b2b_base",
        "market_mode": "b2b",
        "description": "Firm-side Colombo District base case.",
        "b2b_attribute_deltas": {},
        "b2b_share_multipliers": {},
    },
    "mixed_market_base": {
        "scenario_id": "mixed_market_base",
        "market_mode": "mixed",
        "description": "Combined Colombo consumer and firm view.",
        "mixed_weights": {"b2c": 0.4, "b2b": 0.6},
    },
    "budget_sensitive_market": {
        "scenario_id": "budget_sensitive_market",
        "market_mode": "mixed",
        "description": "Households and firms are more price constrained.",
        "mixed_weights": {"b2c": 0.45, "b2b": 0.55},
        "b2c_attribute_deltas": {"avg_budget_score": -18},
        "b2b_attribute_deltas": {"avg_ability_to_pay": -15},
    },
    "low_digital_readiness_market": {
        "scenario_id": "low_digital_readiness_market",
        "market_mode": "mixed",
        "description": "Digital comfort and device readiness soften outside the base.",
        "mixed_weights": {"b2c": 0.45, "b2b": 0.55},
        "b2c_attribute_deltas": {"avg_digital_readiness": -18, "avg_channel_reach_score": -10},
        "b2b_attribute_deltas": {"avg_digital_maturity": -15},
    },
    "trust_friction_heavy_market": {
        "scenario_id": "trust_friction_heavy_market",
        "market_mode": "mixed",
        "description": "Trust barriers are heavier for both consumers and firms.",
        "mixed_weights": {"b2c": 0.45, "b2b": 0.55},
        "b2c_attribute_deltas": {"avg_trust_openness": -18},
        "b2b_attribute_deltas": {"avg_owner_sophistication": -10},
    },
    "smb_heavy_market": {
        "scenario_id": "smb_heavy_market",
        "market_mode": "b2b",
        "description": "SMB-heavy mix boosts retail, logistics, and consumer-service firms.",
        "b2b_share_multipliers": {
            "b2b_smb_retail_operators": 1.2,
            "b2b_consumer_service_frontdesks": 1.15,
            "b2b_field_ops_and_logistics": 1.15,
            "b2b_formal_growth_smes": 0.85
        }
    },
    "youth_heavy_consumer_market": {
        "scenario_id": "youth_heavy_consumer_market",
        "market_mode": "b2c",
        "description": "Youth and upskilling pressure are stronger than the base mix.",
        "b2c_share_multipliers": {
            "b2c_youth_upskilling_seekers": 1.35,
            "b2c_affluent_productivity_seekers": 0.9
        },
        "b2c_attribute_deltas": {"avg_need_education": 8, "avg_need_jobs": 6}
    },
    "urban_sri_lanka_expansion": {
        "scenario_id": "urban_sri_lanka_expansion",
        "market_mode": "mixed",
        "description": "Expansion beyond Colombo with lower budgets and more uneven readiness.",
        "mixed_weights": {"b2c": 0.45, "b2b": 0.55},
        "b2c_attribute_deltas": {"avg_budget_score": -12, "avg_digital_readiness": -10, "avg_channel_reach_score": -8},
        "b2b_attribute_deltas": {"avg_ability_to_pay": -10, "avg_digital_maturity": -8, "avg_decision_speed": -8}
    }
}
