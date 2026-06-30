"""Stooq historical CSV client and parsing helpers."""

from __future__ import annotations

import csv
import io
import socket
from dataclasses import dataclass
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request


STOOQ_BASE_URL = "https://stooq.com/q/d/l/"
SUPPORTED_INTERVAL = "d"
EXPECTED_COLUMNS = ("Date", "Open", "High", "Low", "Close", "Volume")


@dataclass(frozen=True)
class StooqHistoricalRow:
    date: str
    open: str
    high: str
    low: str
    close: str
    volume: str


@dataclass(frozen=True)
class StooqHistoricalResponse:
    provider: str
    provider_symbol: str
    interval: str
    rows: list[StooqHistoricalRow]


class StooqClientError(Exception):
    """Base exception for Stooq client failures."""


class StooqNetworkError(StooqClientError):
    """Raised when Stooq network or decoding operations fail."""


class StooqParseError(StooqClientError):
    """Raised when Stooq CSV text cannot be parsed as expected."""


def build_stooq_historical_url(
    provider_symbol: str,
    *,
    interval: str = SUPPORTED_INTERVAL,
) -> str:
    """Build the Stooq historical daily CSV URL for a provider symbol."""
    normalized_symbol = _require_provider_symbol(provider_symbol)
    _require_supported_interval(interval)

    query = urllib_parse.urlencode({"s": normalized_symbol.lower(), "i": interval})
    return f"{STOOQ_BASE_URL}?{query}"


def parse_stooq_historical_csv(
    provider_symbol: str,
    csv_text: str,
    *,
    interval: str = SUPPORTED_INTERVAL,
) -> StooqHistoricalResponse:
    """Parse raw Stooq CSV text into provider-specific response rows."""
    normalized_symbol = _require_provider_symbol(provider_symbol)
    _require_supported_interval(interval)

    if csv_text.strip() == "":
        raise StooqParseError("csv_text must not be empty")

    reader = csv.DictReader(io.StringIO(csv_text))
    fieldnames = reader.fieldnames
    if fieldnames is None:
        raise StooqParseError("missing required columns: Date, Open, High, Low, Close, Volume")
    if tuple(fieldnames) != EXPECTED_COLUMNS:
        raise StooqParseError(
            "unexpected CSV columns: expected Date, Open, High, Low, Close, Volume"
        )

    rows = [
        StooqHistoricalRow(
            date=row["Date"],
            open=row["Open"],
            high=row["High"],
            low=row["Low"],
            close=row["Close"],
            volume=row["Volume"],
        )
        for row in reader
    ]
    if not rows:
        raise StooqParseError("no historical data rows found")

    return StooqHistoricalResponse(
        provider="stooq",
        provider_symbol=normalized_symbol,
        interval=interval,
        rows=rows,
    )


def fetch_stooq_historical_csv(
    provider_symbol: str,
    *,
    interval: str = SUPPORTED_INTERVAL,
    timeout_seconds: float = 10.0,
) -> str:
    """Fetch raw UTF-8 CSV text from Stooq."""
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than 0")

    url = build_stooq_historical_url(provider_symbol, interval=interval)

    try:
        with urllib_request.urlopen(url, timeout=timeout_seconds) as response:
            payload = response.read()
    except urllib_error.HTTPError as exc:
        raise StooqNetworkError(
            f"HTTP error while fetching Stooq historical CSV: {exc.code}"
        ) from exc
    except urllib_error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.timeout):
            raise StooqNetworkError("timeout while fetching Stooq historical CSV") from exc
        raise StooqNetworkError(
            f"network error while fetching Stooq historical CSV: {reason}"
        ) from exc
    except TimeoutError as exc:
        raise StooqNetworkError("timeout while fetching Stooq historical CSV") from exc

    if payload == b"":
        raise StooqNetworkError("received empty response from Stooq historical CSV endpoint")

    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StooqNetworkError("failed to decode Stooq historical CSV as UTF-8") from exc

    if text.strip() == "":
        raise StooqNetworkError("received empty response from Stooq historical CSV endpoint")

    return text


def fetch_stooq_historical_data(
    provider_symbol: str,
    *,
    interval: str = SUPPORTED_INTERVAL,
    timeout_seconds: float = 10.0,
) -> StooqHistoricalResponse:
    """Fetch and parse Stooq historical daily CSV data."""
    csv_text = fetch_stooq_historical_csv(
        provider_symbol,
        interval=interval,
        timeout_seconds=timeout_seconds,
    )
    return parse_stooq_historical_csv(
        provider_symbol,
        csv_text,
        interval=interval,
    )


def _require_provider_symbol(provider_symbol: str) -> str:
    if provider_symbol.strip() == "":
        raise ValueError("provider_symbol must not be empty")
    return provider_symbol


def _require_supported_interval(interval: str) -> None:
    if interval != SUPPORTED_INTERVAL:
        raise ValueError("unsupported interval: only daily interval 'd' is supported")
