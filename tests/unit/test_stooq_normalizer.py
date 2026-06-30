from __future__ import annotations

import pytest

from market_xg.data_providers.stooq_client import (
    StooqHistoricalResponse,
    StooqHistoricalRow,
)
from market_xg.data_providers.stooq_normalizer import (
    StooqNormalizationError,
    normalize_and_validate_stooq_historical_response,
    normalize_stooq_historical_response,
)


def valid_response() -> StooqHistoricalResponse:
    return StooqHistoricalResponse(
        provider="stooq",
        provider_symbol="AAPL.US",
        interval="d",
        rows=[
            StooqHistoricalRow(
                date="2026-01-02",
                open="100",
                high="105",
                low="99",
                close="104",
                volume="123456",
            ),
            StooqHistoricalRow(
                date="2026-01-03",
                open="104",
                high="106",
                low="101",
                close="102",
                volume="234567",
            ),
        ],
    )


def test_valid_response_normalizes_into_market_xg_rows() -> None:
    rows = normalize_stooq_historical_response(valid_response())

    assert rows == [
        {
            "date": "2026-01-02",
            "open": "100",
            "high": "105",
            "low": "99",
            "close": "104",
            "volume": "123456",
        },
        {
            "date": "2026-01-03",
            "open": "104",
            "high": "106",
            "low": "101",
            "close": "102",
            "volume": "234567",
        },
    ]


def test_normalized_rows_have_exact_ohlcv_keys() -> None:
    rows = normalize_stooq_historical_response(valid_response())

    assert tuple(rows[0].keys()) == ("date", "open", "high", "low", "close", "volume")


def test_values_are_preserved_as_stripped_strings() -> None:
    response = StooqHistoricalResponse(
        provider="stooq",
        provider_symbol="AAPL.US",
        interval="d",
        rows=[
            StooqHistoricalRow(
                date=" 2026-01-02 ",
                open=" 100.0 ",
                high=" 105.50 ",
                low=" 99 ",
                close=" 104.25 ",
                volume=" 00123456 ",
            )
        ],
    )

    rows = normalize_stooq_historical_response(response, validate=False)

    assert rows == [
        {
            "date": "2026-01-02",
            "open": "100.0",
            "high": "105.50",
            "low": "99",
            "close": "104.25",
            "volume": "00123456",
        }
    ]
    assert isinstance(rows[0]["open"], str)


def test_numeric_values_are_not_converted_to_floats() -> None:
    rows = normalize_stooq_historical_response(valid_response(), validate=False)

    assert rows[0]["open"] == "100"
    assert not isinstance(rows[0]["open"], float)


def test_input_response_is_not_mutated() -> None:
    response = valid_response()
    original_row = response.rows[0]

    normalize_stooq_historical_response(response, validate=False)

    assert response.rows[0] == original_row
    assert response.rows[0].open == "100"


def test_wrong_response_type_raises_type_error() -> None:
    with pytest.raises(TypeError, match="StooqHistoricalResponse"):
        normalize_stooq_historical_response(object())  # type: ignore[arg-type]


def test_empty_response_rows_raise_normalization_error() -> None:
    response = StooqHistoricalResponse(
        provider="stooq",
        provider_symbol="AAPL.US",
        interval="d",
        rows=[],
    )

    with pytest.raises(StooqNormalizationError, match="response.rows must not be empty"):
        normalize_stooq_historical_response(response)


def test_whitespace_only_field_raises_normalization_error() -> None:
    response = valid_response()
    response.rows[0] = StooqHistoricalRow(
        date="2026-01-02",
        open="   ",
        high="105",
        low="99",
        close="104",
        volume="123456",
    )

    with pytest.raises(StooqNormalizationError, match="missing value for open at row 1"):
        normalize_stooq_historical_response(response, validate=False)


def test_validate_true_calls_existing_semantic_validation_and_accepts_valid_rows() -> None:
    rows = normalize_stooq_historical_response(valid_response(), validate=True)

    assert len(rows) == 2


def test_validate_true_wraps_validation_failures_as_normalization_error() -> None:
    response = StooqHistoricalResponse(
        provider="stooq",
        provider_symbol="AAPL.US",
        interval="d",
        rows=[
            StooqHistoricalRow(
                date="2026-01-02",
                open="100",
                high="98",
                low="99",
                close="104",
                volume="123456",
            )
        ],
    )

    with pytest.raises(StooqNormalizationError, match="failed OHLCV validation"):
        normalize_stooq_historical_response(response, validate=True)


def test_validate_false_skips_semantic_validation() -> None:
    response = StooqHistoricalResponse(
        provider="stooq",
        provider_symbol="AAPL.US",
        interval="d",
        rows=[
            StooqHistoricalRow(
                date="2026-01-02",
                open="100",
                high="98",
                low="99",
                close="104",
                volume="123456",
            )
        ],
    )

    rows = normalize_stooq_historical_response(response, validate=False)

    assert rows[0]["high"] == "98"


def test_normalize_and_validate_wrapper_returns_valid_rows() -> None:
    rows = normalize_and_validate_stooq_historical_response(valid_response())

    assert rows[1]["date"] == "2026-01-03"


def test_no_live_stooq_service_is_called() -> None:
    response = valid_response()

    rows = normalize_stooq_historical_response(response, validate=False)

    assert rows[0]["close"] == "104"
