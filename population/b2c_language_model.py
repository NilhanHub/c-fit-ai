"""Prompt #03 language-preference modeling for Colombo consumers."""

from __future__ import annotations

from random import Random


def infer_language_preference(language_profile: str, age_band: str, rng: Random) -> str:
    if language_profile == "en_si":
        return rng.choices(["en", "si_en", "si"], weights=[0.42, 0.43, 0.15], k=1)[0]
    if language_profile == "si_en":
        return rng.choices(["si", "si_en", "en"], weights=[0.48, 0.4, 0.12], k=1)[0]
    if language_profile == "si_ta_en":
        weights = [0.33, 0.23, 0.18, 0.16, 0.1]
        if age_band == "15-24":
            weights = [0.28, 0.28, 0.2, 0.14, 0.1]
        return rng.choices(["si_en", "si", "ta_en", "ta", "en"], weights=weights, k=1)[0]
    if language_profile == "si_ta":
        return rng.choices(["si", "ta", "si_en"], weights=[0.6, 0.25, 0.15], k=1)[0]
    return rng.choices(["si", "en"], weights=[0.78, 0.22], k=1)[0]
