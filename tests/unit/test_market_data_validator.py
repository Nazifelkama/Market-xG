from __future__ import annotations

from pathlib import Path

import pytest

from market_xg.data_providers.market_data_validator import (
    REQUIRED_COLUMNS,
    load_csv_rows,
    validate_ohlcv_rows,
)


def valid_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2024-01-02",
            "open": "100",
            "high": "105",
            "low": "99",
            "close": "104",
            "volume": "1000000",
        },
        {
            "date": "2024-01-03",
            "open": "104",
            "high": "106",
            "low": "103",
            "close": "105",
            "volume": "1100000",
        },
    ]


def test_sample_fixture_passes_validation() -> None:
    rows = load_csv_rows(Path("tests/fixtures/market_data/sample_sp500_ohlcv.csv"))

    validate_ohlcv_rows(rows)


def test_empty_rows_fail() -> None:
    with pytest.raises(ValueError, match="rows must not be empty"):
        validate_ohlcv_rows([])


def test_missing_required_column_fails() -> None:
    rows = valid_rows()
    del rows[0]["close"]

    with pytest.raises(ValueError, match="missing required column"):
        validate_ohlcv_rows(rows)


def test_missing_value_fails() -> None:
    rows = valid_rows()
    rows[0]["close"] = ""

    with pytest.raises(ValueError, match="missing value"):
        validate_ohlcv_rows(rows)


def test_whitespace_value_fails() -> None:
    rows = valid_rows()
    rows[0]["close"] = "   "

    with pytest.raises(ValueError, match="missing value"):
        validate_ohlcv_rows(rows)


def test_invalid_date_fails() -> None:
    rows = valid_rows()
    rows[0]["date"] = "2024/01/02"

    with pytest.raises(ValueError, match="invalid date"):
        validate_ohlcv_rows(rows)


def test_duplicate_date_fails() -> None:
    rows = valid_rows()
    rows[1]["date"] = rows[0]["date"]

    with pytest.raises(ValueError, match="duplicate date"):
        validate_ohlcv_rows(rows)


def test_unsorted_dates_fail() -> None:
    rows = valid_rows()
    rows[0]["date"] = "2024-01-03"
    rows[1]["date"] = "2024-01-02"

    with pytest.raises(ValueError, match="dates must be sorted ascending"):
        validate_ohlcv_rows(rows)


def test_non_numeric_ohlc_fails() -> None:
    rows = valid_rows()
    rows[0]["open"] = "abc"

    with pytest.raises(ValueError, match="invalid numeric value"):
        validate_ohlcv_rows(rows)


def test_non_positive_ohlc_fails() -> None:
    rows = valid_rows()
    rows[0]["open"] = "0"

    with pytest.raises(ValueError, match="OHLC values must be greater than 0"):
        validate_ohlcv_rows(rows)


def test_non_numeric_volume_fails() -> None:
    rows = valid_rows()
    rows[0]["volume"] = "many"

    with pytest.raises(ValueError, match="invalid numeric value"):
        validate_ohlcv_rows(rows)


def test_negative_volume_fails() -> None:
    rows = valid_rows()
    rows[0]["volume"] = "-1"

    with pytest.raises(ValueError, match="volume must be non-negative"):
        validate_ohlcv_rows(rows)


def test_high_lower_than_low_fails() -> None:
    rows = valid_rows()
    rows[0]["high"] = "98"
    rows[0]["low"] = "99"

    with pytest.raises(ValueError, match="high must be greater than or equal to low"):
        validate_ohlcv_rows(rows)


def test_open_below_low_fails() -> None:
    rows = valid_rows()
    rows[0]["open"] = "98"

    with pytest.raises(ValueError, match="open must be between low and high"):
        validate_ohlcv_rows(rows)


def test_open_above_high_fails() -> None:
    rows = valid_rows()
    rows[0]["open"] = "106"

    with pytest.raises(ValueError, match="open must be between low and high"):
        validate_ohlcv_rows(rows)


def test_close_below_low_fails() -> None:
    rows = valid_rows()
    rows[0]["close"] = "98"

    with pytest.raises(ValueError, match="close must be between low and high"):
        validate_ohlcv_rows(rows)


def test_close_above_high_fails() -> None:
    rows = valid_rows()
    rows[0]["close"] = "106"

    with pytest.raises(ValueError, match="close must be between low and high"):
        validate_ohlcv_rows(rows)


def test_load_csv_rows_returns_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        ",".join(REQUIRED_COLUMNS) + "\n"
        "2024-01-02,100,105,99,104,1000000\n"
        "2024-01-03,104,106,103,105,1100000\n",
        encoding="utf-8",
    )

    rows = load_csv_rows(csv_path)

    assert len(rows) == 2
    assert rows[0]["date"] == "2024-01-02"
    assert rows[1]["volume"] == "1100000"
