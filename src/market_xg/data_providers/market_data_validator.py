"""Phase 1 OHLCV market data validation helpers."""

from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import cast


REQUIRED_COLUMNS = ("date", "open", "high", "low", "close", "volume")


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read CSV rows without validating their contents."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return cast(list[dict[str, str]], [dict(row) for row in reader])


def validate_ohlcv_rows(rows: list[dict[str, str]]) -> None:
    """Validate OHLCV rows against the Phase 1 market data contract."""
    if not rows:
        raise ValueError("rows must not be empty")

    seen_dates: set[date] = set()
    previous_date: date | None = None

    for index, row in enumerate(rows, start=1):
        for column in REQUIRED_COLUMNS:
            if column not in row:
                raise ValueError(f"missing required column: {column}")

            raw_value = row.get(column)
            if raw_value is None or raw_value.strip() == "":
                raise ValueError(f"missing value for {column} at row {index}")

        row_date = _parse_date(row["date"], index)
        if row_date in seen_dates:
            raise ValueError(f"duplicate date: {row['date']}")
        if previous_date is not None and row_date < previous_date:
            raise ValueError("dates must be sorted ascending")

        seen_dates.add(row_date)
        previous_date = row_date

        open_price = _parse_decimal(row["open"], "open", index)
        high_price = _parse_decimal(row["high"], "high", index)
        low_price = _parse_decimal(row["low"], "low", index)
        close_price = _parse_decimal(row["close"], "close", index)
        volume = _parse_decimal(row["volume"], "volume", index)

        for value, name in (
            (open_price, "open"),
            (high_price, "high"),
            (low_price, "low"),
            (close_price, "close"),
        ):
            if value <= 0:
                raise ValueError(f"OHLC values must be greater than 0: {name}")

        if volume < 0:
            raise ValueError("volume must be non-negative")
        if high_price < low_price:
            raise ValueError("high must be greater than or equal to low")
        if not low_price <= open_price <= high_price:
            raise ValueError("open must be between low and high")
        if not low_price <= close_price <= high_price:
            raise ValueError("close must be between low and high")


def _parse_date(value: str, row_index: int) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"invalid date at row {row_index}: {value}") from exc


def _parse_decimal(value: str, column: str, row_index: int) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(
            f"invalid numeric value for {column} at row {row_index}: {value}"
        ) from exc
