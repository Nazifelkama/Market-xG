"""Normalize parsed Stooq historical rows into Market xG OHLCV rows."""

from __future__ import annotations

from market_xg.data_providers.market_data_validator import validate_ohlcv_rows
from market_xg.data_providers.stooq_client import StooqHistoricalResponse


class StooqNormalizationError(ValueError):
    """Raised when Stooq provider rows cannot be normalized safely."""


def normalize_stooq_historical_response(
    response: StooqHistoricalResponse,
    *,
    validate: bool = True,
) -> list[dict[str, str]]:
    """Normalize Stooq historical response rows into pure OHLCV dictionaries."""
    if not isinstance(response, StooqHistoricalResponse):
        raise TypeError("response must be a StooqHistoricalResponse")
    if not response.rows:
        raise StooqNormalizationError("response.rows must not be empty")

    normalized_rows: list[dict[str, str]] = []
    for index, row in enumerate(response.rows, start=1):
        normalized_row = {
            "date": _normalize_field(row.date, "date", index),
            "open": _normalize_field(row.open, "open", index),
            "high": _normalize_field(row.high, "high", index),
            "low": _normalize_field(row.low, "low", index),
            "close": _normalize_field(row.close, "close", index),
            "volume": _normalize_field(row.volume, "volume", index),
        }
        normalized_rows.append(normalized_row)

    if validate:
        try:
            validate_ohlcv_rows(normalized_rows)
        except ValueError as exc:
            raise StooqNormalizationError(
                f"normalized Stooq rows failed OHLCV validation: {exc}"
            ) from exc

    return normalized_rows


def normalize_and_validate_stooq_historical_response(
    response: StooqHistoricalResponse,
) -> list[dict[str, str]]:
    """Normalize Stooq historical rows and apply OHLCV semantic validation."""
    return normalize_stooq_historical_response(response, validate=True)


def _normalize_field(value: str | None, field_name: str, row_index: int) -> str:
    if value is None:
        raise StooqNormalizationError(f"missing value for {field_name} at row {row_index}")

    normalized_value = value.strip()
    if normalized_value == "":
        raise StooqNormalizationError(f"missing value for {field_name} at row {row_index}")

    return normalized_value
