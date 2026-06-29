from __future__ import annotations

from pathlib import Path

import pytest

from market_xg.data_providers.market_data_validator import load_csv_rows
from market_xg.indicators.drawdown import (
    ROLLING_DRAWDOWN_WINDOW,
    drawdown_from_rolling_high,
    latest_drawdown_from_rolling_high,
    rolling_high,
)


def test_rolling_high_calculates_expected_values() -> None:
    values = [100.0, 110.0, 105.0, 120.0, 108.0]

    highs = rolling_high(values, 3)

    assert highs == [None, None, 110.0, 120.0, 120.0]


def test_drawdown_from_rolling_high_calculates_expected_values() -> None:
    values = [100.0, 110.0, 105.0, 120.0, 108.0]

    drawdowns = drawdown_from_rolling_high(values, 3)

    assert drawdowns[0] is None
    assert drawdowns[1] is None
    assert drawdowns[2] == pytest.approx(-4.545454545454541)
    assert drawdowns[3] == pytest.approx(0.0)
    assert drawdowns[4] == pytest.approx(-10.0)


def test_output_length_equals_input_length() -> None:
    values = [100.0, 110.0, 105.0, 120.0]

    highs = rolling_high(values, 2)
    drawdowns = drawdown_from_rolling_high(values, 2)

    assert len(highs) == len(values)
    assert len(drawdowns) == len(values)


def test_insufficient_history_returns_none() -> None:
    values = [100.0, 110.0, 105.0]

    highs = rolling_high(values, 3)
    drawdowns = drawdown_from_rolling_high(values, 3)

    assert highs[0] is None
    assert highs[1] is None
    assert drawdowns[0] is None
    assert drawdowns[1] is None


def test_rolling_high_is_available_only_when_index_is_greater_than_or_equal_to_window_minus_one() -> None:
    values = [100.0, 110.0, 105.0, 120.0]

    highs = rolling_high(values, 3)

    assert highs[0] is None
    assert highs[1] is None
    assert highs[2] == 110.0
    assert highs[3] == 120.0


def test_drawdown_is_zero_at_rolling_high() -> None:
    values = [100.0, 110.0, 120.0]

    drawdowns = drawdown_from_rolling_high(values, 2)

    assert drawdowns[1] == pytest.approx(0.0)
    assert drawdowns[2] == pytest.approx(0.0)


def test_drawdown_is_negative_below_rolling_high() -> None:
    values = [100.0, 110.0, 105.0]

    drawdowns = drawdown_from_rolling_high(values, 2)

    assert drawdowns[2] is not None
    assert drawdowns[2] < 0


def test_non_none_drawdown_values_are_never_positive() -> None:
    values = [100.0, 110.0, 105.0, 120.0, 108.0]

    drawdowns = drawdown_from_rolling_high(values, 3)

    non_none_values = [value for value in drawdowns if value is not None]
    assert all(value <= 0 for value in non_none_values)


def test_window_one_returns_original_values_as_rolling_highs() -> None:
    values = [100.0, 110.0, 105.0]

    highs = rolling_high(values, 1)

    assert highs == [100.0, 110.0, 105.0]


def test_window_one_returns_zero_drawdown_for_every_value() -> None:
    values = [100.0, 110.0, 105.0]

    drawdowns = drawdown_from_rolling_high(values, 1)

    assert drawdowns == [0.0, 0.0, 0.0]


def test_latest_drawdown_from_rolling_high_returns_latest_drawdown() -> None:
    values = [100.0, 110.0, 105.0, 120.0, 108.0]

    latest_drawdown = latest_drawdown_from_rolling_high(values, 3)

    assert latest_drawdown == pytest.approx(-10.0)


def test_latest_drawdown_from_rolling_high_returns_none_when_insufficient_history() -> None:
    assert latest_drawdown_from_rolling_high([100.0, 110.0], 3) is None


def test_invalid_window_zero_raises_value_error() -> None:
    with pytest.raises(ValueError, match="window must be greater than 0"):
        rolling_high([100.0], 0)


def test_invalid_negative_window_raises_value_error() -> None:
    with pytest.raises(ValueError, match="window must be greater than 0"):
        rolling_high([100.0], -1)


def test_empty_values_raise_value_error() -> None:
    with pytest.raises(ValueError, match="values must not be empty"):
        rolling_high([], 3)


def test_zero_value_raises_value_error() -> None:
    with pytest.raises(ValueError, match="values must be greater than 0"):
        rolling_high([100.0, 0.0, 110.0], 2)


def test_negative_value_raises_value_error() -> None:
    with pytest.raises(ValueError, match="values must be greater than 0"):
        rolling_high([100.0, -5.0, 110.0], 2)


def test_sample_fixture_close_prices_can_produce_252_day_drawdown() -> None:
    close_prices = _fixture_close_prices()

    latest_drawdown = latest_drawdown_from_rolling_high(
        close_prices, ROLLING_DRAWDOWN_WINDOW
    )

    assert latest_drawdown is not None
    assert latest_drawdown <= 0


def _fixture_close_prices() -> list[float]:
    rows = load_csv_rows(Path("tests/fixtures/market_data/sample_sp500_ohlcv.csv"))
    return [float(row["close"]) for row in rows]
