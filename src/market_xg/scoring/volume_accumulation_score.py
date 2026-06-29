"""Phase 2 Volume / Accumulation scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VolumeAccumulationScore:
    """Deterministic Phase 2 Volume / Accumulation score output."""

    score: float
    strengths: list[str]
    weaknesses: list[str]
    details: dict[str, float | int | bool | str | None]

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("score must be between 0 and 100")
        if not isinstance(self.strengths, list):
            raise ValueError("strengths must be a list")
        if not isinstance(self.weaknesses, list):
            raise ValueError("weaknesses must be a list")
        if not isinstance(self.details, dict):
            raise ValueError("details must be a dict")


def calculate_volume_accumulation_score(
    *,
    price_change_20d: float | None,
    latest_volume_ratio_50d: float | None,
    up_down_volume_ratio_20d: float | None,
) -> VolumeAccumulationScore:
    """Calculate the Phase 2 Volume / Accumulation score."""
    _validate_optional_number(
        price_change_20d,
        name="price_change_20d",
        minimum=None,
    )
    _validate_optional_number(
        latest_volume_ratio_50d,
        name="latest_volume_ratio_50d",
        minimum=0.0,
    )
    _validate_optional_number(
        up_down_volume_ratio_20d,
        name="up_down_volume_ratio_20d",
        minimum=0.0,
    )

    raw_score = 50.0
    strengths: list[str] = []
    weaknesses: list[str] = []

    if price_change_20d is not None and latest_volume_ratio_50d is not None:
        if price_change_20d > 0 and latest_volume_ratio_50d >= 1.10:
            raw_score += 15
            strengths.append("rising price confirmed by above-average volume")
        elif price_change_20d > 0 and latest_volume_ratio_50d < 0.80:
            raw_score -= 10
            weaknesses.append("rising price on weak volume")
        elif price_change_20d < 0 and latest_volume_ratio_50d >= 1.20:
            raw_score -= 15
            weaknesses.append("falling price on heavy volume")
        elif price_change_20d < 0 and latest_volume_ratio_50d < 0.80:
            raw_score += 5
            strengths.append("falling price on light volume")

    if up_down_volume_ratio_20d is not None:
        if up_down_volume_ratio_20d > 1.20:
            raw_score += 15
            strengths.append("up-day volume exceeds down-day volume")
        elif up_down_volume_ratio_20d < 0.80:
            raw_score -= 15
            weaknesses.append("down-day volume exceeds up-day volume")

    details: dict[str, float | int | bool | str | None] = {
        "price_change_20d": price_change_20d,
        "latest_volume_ratio_50d": latest_volume_ratio_50d,
        "up_down_volume_ratio_20d": up_down_volume_ratio_20d,
        "price_rising_20d": None if price_change_20d is None else price_change_20d > 0,
        "price_falling_20d": None if price_change_20d is None else price_change_20d < 0,
        "above_average_volume_50d": (
            None
            if latest_volume_ratio_50d is None
            else latest_volume_ratio_50d >= 1.10
        ),
        "weak_volume_50d": (
            None if latest_volume_ratio_50d is None else latest_volume_ratio_50d < 0.80
        ),
        "heavy_volume_50d": (
            None
            if latest_volume_ratio_50d is None
            else latest_volume_ratio_50d >= 1.20
        ),
        "up_volume_dominant_20d": (
            None
            if up_down_volume_ratio_20d is None
            else up_down_volume_ratio_20d > 1.20
        ),
        "down_volume_dominant_20d": (
            None
            if up_down_volume_ratio_20d is None
            else up_down_volume_ratio_20d < 0.80
        ),
        "raw_score": raw_score,
        "final_score": raw_score,
    }

    return VolumeAccumulationScore(
        score=raw_score,
        strengths=strengths,
        weaknesses=weaknesses,
        details=details,
    )


def _validate_optional_number(
    value: float | None,
    *,
    name: str,
    minimum: float | None,
) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be int or float")
    if minimum is not None and float(value) < minimum:
        if minimum == 0.0:
            raise ValueError(f"{name} must be greater than or equal to 0")
        raise ValueError(f"{name} must be greater than or equal to {minimum}")
