from __future__ import annotations

from pathlib import Path

import pytest

from market_xg.data_providers.market_data_validator import (
    load_csv_rows,
    validate_ohlcv_rows,
)
from market_xg.indicators.drawdown import latest_drawdown_from_rolling_high
from market_xg.indicators.momentum import momentum_summary
from market_xg.indicators.moving_average import latest_simple_moving_average
from market_xg.indicators.volume import (
    latest_average_volume,
    up_down_volume_summary,
    volume_ratio,
)
from market_xg.reports.markdown_report import generate_market_xg_markdown_report
from market_xg.scoring.market_xg_score import CategoryScore, calculate_market_xg_score
from market_xg.scoring.trend_momentum_score import calculate_trend_momentum_score
from market_xg.scoring.volume_accumulation_score import (
    calculate_volume_accumulation_score,
)


def test_phase_1_sample_pipeline_happy_path() -> None:
    rows = load_csv_rows(Path("tests/fixtures/market_data/sample_sp500_ohlcv.csv"))
    validate_ohlcv_rows(rows)

    close_prices = [float(row["close"]) for row in rows]
    volumes = [float(row["volume"]) for row in rows]

    assert close_prices
    assert volumes
    assert len(volumes) == len(close_prices)
    assert len(close_prices) >= 252

    sma_50 = latest_simple_moving_average(close_prices, 50)
    sma_200 = latest_simple_moving_average(close_prices, 200)
    momentum = momentum_summary(close_prices)
    drawdown_252d = latest_drawdown_from_rolling_high(close_prices, 252)
    avg_volume_50 = latest_average_volume(volumes, 50)
    latest_volume_ratio_50d = volume_ratio(volumes[-1], avg_volume_50)
    up_down_summary_20d = up_down_volume_summary(close_prices, volumes, 20)
    price_change_20d = ((close_prices[-1] / close_prices[-21]) - 1) * 100

    assert sma_50 is not None
    assert sma_200 is not None
    assert list(momentum.keys()) == ["1m", "3m", "6m", "12m"]
    assert drawdown_252d is not None
    assert avg_volume_50 is not None
    assert latest_volume_ratio_50d is not None
    assert "up_down_volume_ratio" in up_down_summary_20d

    trend_score = calculate_trend_momentum_score(
        latest_close=close_prices[-1],
        sma_50=sma_50,
        sma_200=sma_200,
        momentum_1m=momentum["1m"],
        momentum_3m=momentum["3m"],
        momentum_6m=momentum["6m"],
        momentum_12m=momentum["12m"],
        drawdown_252d=drawdown_252d,
    )

    assert 0 <= trend_score.score <= 100

    volume_score = calculate_volume_accumulation_score(
        price_change_20d=price_change_20d,
        latest_volume_ratio_50d=latest_volume_ratio_50d,
        up_down_volume_ratio_20d=up_down_summary_20d["up_down_volume_ratio"],
    )

    assert 0 <= volume_score.score <= 100

    market_xg_score = calculate_market_xg_score(
        {
            "trend_momentum": CategoryScore(
                name="trend_momentum",
                score=trend_score.score,
                strengths=trend_score.strengths,
                weaknesses=trend_score.weaknesses,
            ),
            "volume_accumulation": CategoryScore(
                name="volume_accumulation",
                score=volume_score.score,
                strengths=volume_score.strengths,
                weaknesses=volume_score.weaknesses,
            ),
        }
    )

    assert 0 <= market_xg_score.score <= 100
    assert "trend_momentum" in market_xg_score.category_scores
    assert "volume_accumulation" in market_xg_score.category_scores
    assert len(market_xg_score.category_scores) == 2
    assert "trend_momentum" in market_xg_score.weights_used
    assert "volume_accumulation" in market_xg_score.weights_used
    assert sum(market_xg_score.weights_used.values()) == pytest.approx(1.0)
    assert market_xg_score.missing_categories

    report = generate_market_xg_markdown_report(
        report_date="2026-01-01",
        asset_name="Synthetic S&P 500 Sample",
        market_xg_score=market_xg_score,
    )

    assert "# Market xG Report" in report
    assert "Synthetic S&P 500 Sample" in report
    assert "Trend Momentum" in report
    assert "Volume Accumulation" in report
    assert "Market xG is not price prediction." in report
    assert "Missing categories are not assigned fake scores." in report
