from __future__ import annotations

from pathlib import Path

import pytest

from market_xg.scoring.trend_momentum_score import (
    TrendMomentumScore,
    calculate_trend_momentum_score,
)


def test_strong_trend_case_gives_score_at_least_85() -> None:
    result = calculate_trend_momentum_score(
        latest_close=120.0,
        sma_50=110.0,
        sma_200=100.0,
        momentum_1m=5.0,
        momentum_3m=8.0,
        momentum_6m=12.0,
        momentum_12m=20.0,
        drawdown_252d=-2.0,
    )

    assert result.score >= 85


def test_weak_trend_case_gives_score_at_most_25() -> None:
    result = calculate_trend_momentum_score(
        latest_close=80.0,
        sma_50=100.0,
        sma_200=110.0,
        momentum_1m=-2.0,
        momentum_3m=-4.0,
        momentum_6m=-8.0,
        momentum_12m=-12.0,
        drawdown_252d=-25.0,
    )

    assert result.score <= 25


def test_all_optional_indicators_missing_gives_neutral_score() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=None,
        sma_200=None,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert result.score == 50.0
    assert result.strengths == []
    assert result.weaknesses == []


def test_score_is_clamped_to_zero_and_one_hundred() -> None:
    strong_result = calculate_trend_momentum_score(
        latest_close=120.0,
        sma_50=110.0,
        sma_200=100.0,
        momentum_1m=1.0,
        momentum_3m=1.0,
        momentum_6m=1.0,
        momentum_12m=1.0,
        drawdown_252d=-1.0,
    )
    weak_result = calculate_trend_momentum_score(
        latest_close=80.0,
        sma_50=100.0,
        sma_200=110.0,
        momentum_1m=-1.0,
        momentum_3m=-1.0,
        momentum_6m=-1.0,
        momentum_12m=-1.0,
        drawdown_252d=-30.0,
    )

    assert 0 <= strong_result.score <= 100
    assert 0 <= weak_result.score <= 100


def test_trend_momentum_score_rejects_score_below_zero() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        TrendMomentumScore(-1.0, [], [], {})


def test_trend_momentum_score_rejects_score_above_one_hundred() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        TrendMomentumScore(101.0, [], [], {})


def test_latest_close_less_than_or_equal_to_zero_raises_value_error() -> None:
    with pytest.raises(ValueError, match="latest_close must be greater than 0"):
        calculate_trend_momentum_score(
            latest_close=0.0,
            sma_50=None,
            sma_200=None,
            momentum_1m=None,
            momentum_3m=None,
            momentum_6m=None,
            momentum_12m=None,
            drawdown_252d=None,
        )


def test_negative_sma_50_raises_value_error() -> None:
    with pytest.raises(ValueError, match="sma_50 must be greater than 0"):
        calculate_trend_momentum_score(
            latest_close=100.0,
            sma_50=-1.0,
            sma_200=None,
            momentum_1m=None,
            momentum_3m=None,
            momentum_6m=None,
            momentum_12m=None,
            drawdown_252d=None,
        )


def test_negative_sma_200_raises_value_error() -> None:
    with pytest.raises(ValueError, match="sma_200 must be greater than 0"):
        calculate_trend_momentum_score(
            latest_close=100.0,
            sma_50=None,
            sma_200=-1.0,
            momentum_1m=None,
            momentum_3m=None,
            momentum_6m=None,
            momentum_12m=None,
            drawdown_252d=None,
        )


def test_positive_drawdown_raises_value_error() -> None:
    with pytest.raises(
        ValueError, match="drawdown_252d must be less than or equal to 0"
    ):
        calculate_trend_momentum_score(
            latest_close=100.0,
            sma_50=None,
            sma_200=None,
            momentum_1m=None,
            momentum_3m=None,
            momentum_6m=None,
            momentum_12m=None,
            drawdown_252d=1.0,
        )


def test_equality_with_moving_averages_is_neutral() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=100.0,
        sma_200=100.0,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert result.score == 50.0


def test_zero_momentum_is_neutral() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=None,
        sma_200=None,
        momentum_1m=0.0,
        momentum_3m=0.0,
        momentum_6m=0.0,
        momentum_12m=0.0,
        drawdown_252d=None,
    )

    assert result.score == 50.0


def test_positive_momentum_adds_strength() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=None,
        sma_200=None,
        momentum_1m=1.0,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert "positive 1-month momentum" in result.strengths


def test_negative_momentum_adds_weakness() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=None,
        sma_200=None,
        momentum_1m=-1.0,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert "negative 1-month momentum" in result.weaknesses


def test_price_above_moving_averages_adds_strengths() -> None:
    result = calculate_trend_momentum_score(
        latest_close=120.0,
        sma_50=110.0,
        sma_200=100.0,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert "price above 50-day moving average" in result.strengths
    assert "price above 200-day moving average" in result.strengths


def test_price_below_moving_averages_adds_weaknesses() -> None:
    result = calculate_trend_momentum_score(
        latest_close=80.0,
        sma_50=100.0,
        sma_200=110.0,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert "price below 50-day moving average" in result.weaknesses
    assert "price below 200-day moving average" in result.weaknesses


def test_sma_50_above_sma_200_adds_strength() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=110.0,
        sma_200=100.0,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert "50-day moving average above 200-day moving average" in result.strengths


def test_sma_50_below_sma_200_adds_weakness() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=90.0,
        sma_200=100.0,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=None,
    )

    assert "50-day moving average below 200-day moving average" in result.weaknesses


def test_drawdown_close_to_high_adds_strength() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=None,
        sma_200=None,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=-4.0,
    )

    assert "price close to 252-day high" in result.strengths


def test_deep_drawdown_adds_weakness() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=None,
        sma_200=None,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=-25.0,
    )

    assert "deep drawdown from 252-day high" in result.weaknesses


def test_moderate_drawdown_between_minus_twenty_and_minus_five_is_neutral() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=None,
        sma_200=None,
        momentum_1m=None,
        momentum_3m=None,
        momentum_6m=None,
        momentum_12m=None,
        drawdown_252d=-10.0,
    )

    assert result.score == 50.0


def test_details_dict_contains_expected_keys() -> None:
    result = calculate_trend_momentum_score(
        latest_close=100.0,
        sma_50=95.0,
        sma_200=90.0,
        momentum_1m=1.0,
        momentum_3m=2.0,
        momentum_6m=3.0,
        momentum_12m=4.0,
        drawdown_252d=-3.0,
    )

    assert set(result.details.keys()) == {
        "latest_close",
        "sma_50",
        "sma_200",
        "momentum_1m",
        "momentum_3m",
        "momentum_6m",
        "momentum_12m",
        "drawdown_252d",
        "price_above_sma_50",
        "price_above_sma_200",
        "sma_50_above_sma_200",
        "raw_score_before_clamp",
        "final_score",
    }


def test_raw_score_before_clamp_and_final_score_are_present_in_details() -> None:
    result = calculate_trend_momentum_score(
        latest_close=120.0,
        sma_50=110.0,
        sma_200=100.0,
        momentum_1m=5.0,
        momentum_3m=5.0,
        momentum_6m=5.0,
        momentum_12m=5.0,
        drawdown_252d=-2.0,
    )

    assert "raw_score_before_clamp" in result.details
    assert "final_score" in result.details


def test_function_does_not_import_or_call_indicator_modules() -> None:
    source_text = Path(
        "src/market_xg/scoring/trend_momentum_score.py"
    ).read_text(encoding="utf-8")

    forbidden_patterns = (
        "moving_average",
        "momentum.py",
        "drawdown.py",
        "market_xg.indicators.moving_average",
        "market_xg.indicators.momentum",
        "market_xg.indicators.drawdown",
    )

    for pattern in forbidden_patterns:
        assert pattern not in source_text
