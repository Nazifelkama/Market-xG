from __future__ import annotations

from pathlib import Path

import pytest

from market_xg.data_providers.market_data_validator import load_csv_rows
from market_xg.indicators.moving_average import (
    latest_simple_moving_average,
    simple_moving_average,
)


def test_simple_moving_average_calculates_expected_values() -> None:
    values = [10.0, 20.0, 30.0, 40.0, 50.0]

    averages = simple_moving_average(values, 3)

    assert averages == [None, None, 20.0, 30.0, 40.0]


def test_output_length_equals_input_length() -> None:
    values = [10.0, 20.0, 30.0, 40.0]

    averages = simple_moving_average(values, 2)

    assert len(averages) == len(values)


def test_insufficient_history_returns_none() -> None:
    values = [10.0, 20.0, 30.0]

    averages = simple_moving_average(values, 3)

    assert averages[0] is None
    assert averages[1] is None


def test_latest_simple_moving_average_returns_latest_sma() -> None:
    values = [10.0, 20.0, 30.0, 40.0, 50.0]

    assert latest_simple_moving_average(values, 3) == 40.0


def test_latest_simple_moving_average_returns_none_when_insufficient_history() -> None:
    assert latest_simple_moving_average([10.0, 20.0], 3) is None


def test_window_of_one_returns_original_values_as_floats() -> None:
    values = [10.0, 20.5, 30.25]

    assert simple_moving_average(values, 1) == [10.0, 20.5, 30.25]


def test_invalid_window_zero_raises_value_error() -> None:
    with pytest.raises(ValueError, match="window must be greater than 0"):
        simple_moving_average([10.0], 0)


def test_invalid_negative_window_raises_value_error() -> None:
    with pytest.raises(ValueError, match="window must be greater than 0"):
        simple_moving_average([10.0], -1)


def test_empty_values_raise_value_error() -> None:
    with pytest.raises(ValueError, match="values must not be empty"):
        simple_moving_average([], 3)


def test_sample_fixture_close_prices_can_produce_50_day_sma() -> None:
    close_prices = _fixture_close_prices()

    latest_sma = latest_simple_moving_average(close_prices, 50)

    assert latest_sma is not None


def test_sample_fixture_close_prices_can_produce_200_day_sma() -> None:
    close_prices = _fixture_close_prices()

    latest_sma = latest_simple_moving_average(close_prices, 200)

    assert latest_sma is not None


def _fixture_close_prices() -> list[float]:
    rows = load_csv_rows(Path("tests/fixtures/market_data/sample_sp500_ohlcv.csv"))
    return [float(row["close"]) for row in rows]
