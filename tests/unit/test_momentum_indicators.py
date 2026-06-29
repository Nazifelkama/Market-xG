from __future__ import annotations

from pathlib import Path

import pytest

from market_xg.data_providers.market_data_validator import load_csv_rows
from market_xg.indicators.momentum import (
    DEFAULT_MOMENTUM_WINDOWS,
    latest_percentage_return,
    momentum_summary,
    percentage_return,
)


def test_percentage_return_calculates_expected_values() -> None:
    values = [100.0, 110.0, 121.0]

    returns = percentage_return(values, 1)

    assert returns[0] is None
    assert returns[1] == pytest.approx(10.0)
    assert returns[2] == pytest.approx(10.0)


def test_output_length_equals_input_length() -> None:
    values = [100.0, 110.0, 121.0, 133.1]

    returns = percentage_return(values, 2)

    assert len(returns) == len(values)


def test_insufficient_history_returns_none() -> None:
    values = [100.0, 110.0, 121.0]

    returns = percentage_return(values, 2)

    assert returns[0] is None
    assert returns[1] is None


def test_return_is_available_only_when_index_is_greater_than_or_equal_to_window() -> None:
    values = [100.0, 110.0, 121.0, 133.1]

    returns = percentage_return(values, 2)

    assert returns[0] is None
    assert returns[1] is None
    assert returns[2] == pytest.approx(21.0)
    assert returns[3] == pytest.approx(21.0)


def test_latest_percentage_return_returns_latest_value() -> None:
    values = [100.0, 110.0, 121.0]

    latest_return = latest_percentage_return(values, 1)

    assert latest_return == pytest.approx(10.0)


def test_latest_percentage_return_returns_none_when_insufficient_history() -> None:
    assert latest_percentage_return([100.0, 110.0], 3) is None


def test_momentum_summary_returns_exact_expected_keys() -> None:
    values = [float(index) for index in range(1, 400)]

    summary = momentum_summary(values)

    assert list(summary.keys()) == ["1m", "3m", "6m", "12m"]


def test_momentum_summary_uses_default_windows() -> None:
    values = [float(index) for index in range(1, 400)]

    summary = momentum_summary(values)

    for label, window in DEFAULT_MOMENTUM_WINDOWS.items():
        assert summary[label] == latest_percentage_return(values, window)


def test_invalid_window_zero_raises_value_error() -> None:
    with pytest.raises(ValueError, match="window must be greater than 0"):
        percentage_return([100.0], 0)


def test_invalid_negative_window_raises_value_error() -> None:
    with pytest.raises(ValueError, match="window must be greater than 0"):
        percentage_return([100.0], -1)


def test_empty_values_raise_value_error() -> None:
    with pytest.raises(ValueError, match="values must not be empty"):
        percentage_return([], 1)


def test_zero_value_raises_value_error() -> None:
    with pytest.raises(ValueError, match="values must be greater than 0"):
        percentage_return([100.0, 0.0, 110.0], 1)


def test_negative_value_raises_value_error() -> None:
    with pytest.raises(ValueError, match="values must be greater than 0"):
        percentage_return([100.0, -5.0, 110.0], 1)


def test_sample_fixture_close_prices_can_produce_all_default_momentum_values() -> None:
    close_prices = _fixture_close_prices()

    summary = momentum_summary(close_prices)

    assert summary["1m"] is not None
    assert summary["3m"] is not None
    assert summary["6m"] is not None
    assert summary["12m"] is not None


def _fixture_close_prices() -> list[float]:
    rows = load_csv_rows(Path("tests/fixtures/market_data/sample_sp500_ohlcv.csv"))
    return [float(row["close"]) for row in rows]
