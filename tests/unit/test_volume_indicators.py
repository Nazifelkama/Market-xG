from __future__ import annotations

from pathlib import Path

import pytest

from market_xg.data_providers.market_data_validator import load_csv_rows
from market_xg.indicators.volume import (
    average_volume,
    latest_average_volume,
    up_down_volume_summary,
    volume_ratio,
)


def test_average_volume_returns_expected_trailing_averages() -> None:
    assert average_volume([100.0, 200.0, 300.0, 400.0], 2) == [
        None,
        150.0,
        250.0,
        350.0,
    ]


def test_average_volume_returns_none_until_enough_history_exists() -> None:
    assert average_volume([100.0, 200.0, 300.0], 3) == [None, None, 200.0]


def test_average_volume_window_one_returns_each_volume_as_float() -> None:
    assert average_volume([100.0, 200.0, 300.0], 1) == [100.0, 200.0, 300.0]


def test_latest_average_volume_returns_latest_average() -> None:
    assert latest_average_volume([100.0, 200.0, 300.0, 400.0], 2) == 350.0


def test_latest_average_volume_returns_none_when_insufficient_history_exists() -> None:
    assert latest_average_volume([100.0], 2) is None


def test_volume_ratio_returns_expected_ratio() -> None:
    assert volume_ratio(150.0, 100.0) == 1.5


def test_volume_ratio_returns_none_when_average_is_none() -> None:
    assert volume_ratio(150.0, None) is None


def test_volume_ratio_returns_none_when_average_is_zero() -> None:
    assert volume_ratio(150.0, 0.0) is None


def test_volume_ratio_rejects_negative_latest_volume() -> None:
    with pytest.raises(ValueError, match="latest_volume values must be greater than or equal to 0"):
        volume_ratio(-1.0, 100.0)


def test_volume_ratio_rejects_negative_average_volume_value() -> None:
    with pytest.raises(ValueError, match="average_volume_value values must be greater than or equal to 0"):
        volume_ratio(100.0, -1.0)


def test_up_down_volume_summary_returns_expected_totals() -> None:
    summary = up_down_volume_summary(
        close_prices=[100.0, 101.0, 99.0, 99.0],
        volumes=[100.0, 200.0, 300.0, 400.0],
        window=4,
    )

    assert summary["up_volume"] == 200.0
    assert summary["down_volume"] == 300.0
    assert summary["flat_volume"] == 400.0


def test_up_down_volume_summary_returns_expected_ratio() -> None:
    summary = up_down_volume_summary(
        close_prices=[100.0, 101.0, 99.0, 99.0],
        volumes=[100.0, 200.0, 300.0, 400.0],
        window=4,
    )

    assert summary["up_down_volume_ratio"] == pytest.approx(200.0 / 300.0)


def test_up_down_volume_summary_returns_none_values_when_insufficient_history_exists() -> None:
    summary = up_down_volume_summary(
        close_prices=[100.0, 101.0],
        volumes=[100.0, 200.0],
        window=3,
    )

    assert summary == {
        "up_volume": None,
        "down_volume": None,
        "flat_volume": None,
        "up_down_volume_ratio": None,
    }


def test_up_down_volume_summary_handles_down_volume_zero_without_division_error() -> None:
    summary = up_down_volume_summary(
        close_prices=[100.0, 101.0, 102.0],
        volumes=[100.0, 200.0, 300.0],
        window=3,
    )

    assert summary["up_volume"] == 500.0
    assert summary["down_volume"] == 0.0
    assert summary["up_down_volume_ratio"] is None


def test_up_down_volume_summary_rejects_window_one() -> None:
    with pytest.raises(ValueError, match="window must be greater than or equal to 2"):
        up_down_volume_summary([100.0, 101.0], [100.0, 200.0], 1)


def test_empty_volumes_raises_value_error() -> None:
    with pytest.raises(ValueError, match="volumes must not be empty"):
        average_volume([], 2)


def test_empty_close_prices_raises_value_error_where_relevant() -> None:
    with pytest.raises(ValueError, match="close_prices must not be empty"):
        up_down_volume_summary([], [100.0], 2)


def test_invalid_window_raises_value_error() -> None:
    with pytest.raises(ValueError, match="window must be greater than 0"):
        average_volume([100.0], 0)


def test_bool_values_are_rejected_as_numeric_inputs() -> None:
    with pytest.raises(ValueError, match="volume values must be int or float"):
        average_volume([100.0, True], 2)


def test_negative_volume_raises_value_error() -> None:
    with pytest.raises(ValueError, match="volume values must be greater than or equal to 0"):
        average_volume([100.0, -1.0], 2)


def test_negative_close_price_raises_value_error() -> None:
    with pytest.raises(ValueError, match="close_price values must be greater than 0"):
        up_down_volume_summary([100.0, -1.0], [100.0, 200.0], 2)


def test_zero_close_price_raises_value_error() -> None:
    with pytest.raises(ValueError, match="close_price values must be greater than 0"):
        up_down_volume_summary([100.0, 0.0], [100.0, 200.0], 2)


def test_mismatched_close_prices_and_volumes_lengths_raises_value_error() -> None:
    with pytest.raises(ValueError, match="close_prices and volumes must have the same length"):
        up_down_volume_summary([100.0, 101.0], [100.0], 2)


def test_fixture_volume_data_can_calculate_50_day_average_volume() -> None:
    rows = load_csv_rows(Path("tests/fixtures/market_data/sample_sp500_ohlcv.csv"))
    volumes = [float(row["volume"]) for row in rows]

    latest_value = latest_average_volume(volumes, 50)

    assert latest_value is not None


def test_fixture_close_volume_data_can_calculate_20_day_up_down_volume_summary() -> None:
    rows = load_csv_rows(Path("tests/fixtures/market_data/sample_sp500_ohlcv.csv"))
    close_prices = [float(row["close"]) for row in rows]
    volumes = [float(row["volume"]) for row in rows]

    summary = up_down_volume_summary(close_prices, volumes, 20)

    assert summary["up_volume"] is not None
    assert summary["down_volume"] is not None
    assert summary["flat_volume"] is not None
    assert "up_down_volume_ratio" in summary
