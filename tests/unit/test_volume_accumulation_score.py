from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from market_xg.scoring.volume_accumulation_score import (
    VolumeAccumulationScore,
    calculate_volume_accumulation_score,
)


def test_volume_accumulation_score_valid_creation() -> None:
    result = VolumeAccumulationScore(50.0, [], [], {"raw_score": 50.0})

    assert result.score == 50.0


def test_volume_accumulation_score_rejects_score_below_zero() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        VolumeAccumulationScore(-1.0, [], [], {})


def test_volume_accumulation_score_rejects_score_above_one_hundred() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        VolumeAccumulationScore(101.0, [], [], {})


def test_all_optional_inputs_missing_gives_neutral_score() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 50.0
    assert result.strengths == []
    assert result.weaknesses == []


def test_rising_price_with_above_average_volume_adds_strength() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=1.10,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 65.0
    assert "rising price confirmed by above-average volume" in result.strengths


def test_rising_price_on_weak_volume_adds_weakness() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=0.79,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 40.0
    assert "rising price on weak volume" in result.weaknesses


def test_falling_price_on_heavy_volume_adds_weakness() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=-5.0,
        latest_volume_ratio_50d=1.20,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 35.0
    assert "falling price on heavy volume" in result.weaknesses


def test_falling_price_on_light_volume_adds_strength() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=-5.0,
        latest_volume_ratio_50d=0.79,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 55.0
    assert "falling price on light volume" in result.strengths


def test_flat_price_gives_no_price_volume_confirmation_score_change() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=0.0,
        latest_volume_ratio_50d=1.50,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 50.0


def test_latest_volume_ratio_point_eight_zero_is_neutral_for_weak_volume_rules() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=0.80,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 50.0


def test_latest_volume_ratio_point_one_zero_confirms_rising_price() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=1.10,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 65.0


def test_latest_volume_ratio_point_two_zero_confirms_falling_heavy_volume() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=-5.0,
        latest_volume_ratio_50d=1.20,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 35.0


def test_up_down_volume_ratio_above_one_point_two_adds_strength() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=1.21,
    )

    assert result.score == 65.0
    assert "up-day volume exceeds down-day volume" in result.strengths


def test_up_down_volume_ratio_below_zero_point_eight_adds_weakness() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=0.79,
    )

    assert result.score == 35.0
    assert "down-day volume exceeds up-day volume" in result.weaknesses


def test_up_down_volume_ratio_exactly_one_point_two_is_neutral() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=1.20,
    )

    assert result.score == 50.0


def test_up_down_volume_ratio_exactly_zero_point_eight_is_neutral() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=0.80,
    )

    assert result.score == 50.0


def test_up_down_volume_ratio_between_band_is_neutral() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=1.00,
    )

    assert result.score == 50.0


def test_missing_price_change_skips_volume_confirmation() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=1.50,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 50.0


def test_missing_latest_volume_ratio_skips_volume_confirmation() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 50.0


def test_missing_up_down_volume_ratio_skips_participation_rule() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=1.10,
        up_down_volume_ratio_20d=None,
    )

    assert result.score == 65.0


def test_negative_latest_volume_ratio_raises_value_error() -> None:
    with pytest.raises(ValueError, match="latest_volume_ratio_50d must be greater than or equal to 0"):
        calculate_volume_accumulation_score(
            price_change_20d=5.0,
            latest_volume_ratio_50d=-0.1,
            up_down_volume_ratio_20d=None,
        )


def test_negative_up_down_volume_ratio_raises_value_error() -> None:
    with pytest.raises(ValueError, match="up_down_volume_ratio_20d must be greater than or equal to 0"):
        calculate_volume_accumulation_score(
            price_change_20d=5.0,
            latest_volume_ratio_50d=1.0,
            up_down_volume_ratio_20d=-0.1,
        )


def test_bool_values_are_rejected_as_numeric_inputs() -> None:
    with pytest.raises(ValueError, match="price_change_20d must be int or float"):
        calculate_volume_accumulation_score(
            price_change_20d=cast(float | None, True),
            latest_volume_ratio_50d=None,
            up_down_volume_ratio_20d=None,
        )


def test_details_dict_contains_expected_keys() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=1.10,
        up_down_volume_ratio_20d=1.21,
    )

    assert set(result.details.keys()) == {
        "price_change_20d",
        "latest_volume_ratio_50d",
        "up_down_volume_ratio_20d",
        "price_rising_20d",
        "price_falling_20d",
        "above_average_volume_50d",
        "weak_volume_50d",
        "heavy_volume_50d",
        "up_volume_dominant_20d",
        "down_volume_dominant_20d",
        "raw_score",
        "final_score",
    }


def test_boolean_details_are_none_when_required_inputs_are_missing() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=None,
        latest_volume_ratio_50d=None,
        up_down_volume_ratio_20d=None,
    )

    assert result.details["price_rising_20d"] is None
    assert result.details["price_falling_20d"] is None
    assert result.details["above_average_volume_50d"] is None
    assert result.details["weak_volume_50d"] is None
    assert result.details["heavy_volume_50d"] is None
    assert result.details["up_volume_dominant_20d"] is None
    assert result.details["down_volume_dominant_20d"] is None


def test_raw_score_and_final_score_are_present_in_details() -> None:
    result = calculate_volume_accumulation_score(
        price_change_20d=5.0,
        latest_volume_ratio_50d=1.10,
        up_down_volume_ratio_20d=1.21,
    )

    assert result.details["raw_score"] == 80.0
    assert result.details["final_score"] == 80.0


def test_scorer_does_not_import_or_call_volume_indicator_module() -> None:
    source_text = Path(
        "src/market_xg/scoring/volume_accumulation_score.py"
    ).read_text(encoding="utf-8")

    forbidden_patterns = (
        "market_xg.indicators.volume",
        "from market_xg.indicators import volume",
        "import volume",
    )

    for pattern in forbidden_patterns:
        assert pattern not in source_text
