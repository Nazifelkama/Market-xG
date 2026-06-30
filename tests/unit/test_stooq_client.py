from __future__ import annotations

from email.message import Message
import socket
from urllib import error as urllib_error

import pytest

from market_xg.data_providers import stooq_client
from market_xg.data_providers.stooq_client import (
    EXPECTED_COLUMNS,
    STOOQ_BASE_URL,
    StooqHistoricalResponse,
    StooqNetworkError,
    StooqParseError,
    build_stooq_historical_url,
    fetch_stooq_historical_csv,
    fetch_stooq_historical_data,
    parse_stooq_historical_csv,
)


SAMPLE_CSV = """Date,Open,High,Low,Close,Volume
2026-01-02,100,105,99,104,123456
2026-01-03,104,106,101,102,234567
"""


class MockResponse:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> MockResponse:
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None


def test_build_stooq_historical_url_is_deterministic() -> None:
    url = build_stooq_historical_url("AAPL.US")

    assert url == f"{STOOQ_BASE_URL}?s=aapl.us&i=d"


def test_build_stooq_historical_url_lowercases_only_query_symbol() -> None:
    provider_symbol = "VUSA.NL"

    url = build_stooq_historical_url(provider_symbol)

    assert provider_symbol == "VUSA.NL"
    assert "s=vusa.nl" in url


def test_build_stooq_historical_url_uses_urlencoded_query_parameters() -> None:
    url = build_stooq_historical_url("ABC XYZ")

    assert url == f"{STOOQ_BASE_URL}?s=abc+xyz&i=d"


@pytest.mark.parametrize("provider_symbol", ["", "   "])
def test_build_stooq_historical_url_rejects_blank_provider_symbol(provider_symbol: str) -> None:
    with pytest.raises(ValueError, match="provider_symbol must not be empty"):
        build_stooq_historical_url(provider_symbol)


def test_build_stooq_historical_url_rejects_unsupported_interval() -> None:
    with pytest.raises(ValueError, match="unsupported interval"):
        build_stooq_historical_url("AAPL.US", interval="w")


def test_parse_stooq_historical_csv_parses_valid_csv() -> None:
    response = parse_stooq_historical_csv("AAPL.US", SAMPLE_CSV)

    assert response == StooqHistoricalResponse(
        provider="stooq",
        provider_symbol="AAPL.US",
        interval="d",
        rows=[
            stooq_client.StooqHistoricalRow(
                date="2026-01-02",
                open="100",
                high="105",
                low="99",
                close="104",
                volume="123456",
            ),
            stooq_client.StooqHistoricalRow(
                date="2026-01-03",
                open="104",
                high="106",
                low="101",
                close="102",
                volume="234567",
            ),
        ],
    )


def test_parse_stooq_historical_csv_preserves_raw_string_values() -> None:
    csv_text = """Date,Open,High,Low,Close,Volume
2026-01-02,100.0,105.5,99.1,104.25,00123456
"""

    response = parse_stooq_historical_csv("NVDA.US", csv_text)

    assert response.rows[0].open == "100.0"
    assert response.rows[0].high == "105.5"
    assert response.rows[0].volume == "00123456"


@pytest.mark.parametrize("csv_text", ["", "   "])
def test_parse_stooq_historical_csv_rejects_blank_csv_text(csv_text: str) -> None:
    with pytest.raises(StooqParseError, match="csv_text must not be empty"):
        parse_stooq_historical_csv("AAPL.US", csv_text)


def test_parse_stooq_historical_csv_rejects_unsupported_interval() -> None:
    with pytest.raises(ValueError, match="unsupported interval"):
        parse_stooq_historical_csv("AAPL.US", SAMPLE_CSV, interval="w")


def test_parse_stooq_historical_csv_rejects_missing_required_columns() -> None:
    csv_text = "Date,Open,High,Low,Close\n2026-01-02,100,105,99,104\n"

    with pytest.raises(StooqParseError, match="unexpected CSV columns"):
        parse_stooq_historical_csv("AAPL.US", csv_text)


def test_parse_stooq_historical_csv_rejects_non_csv_error_text() -> None:
    with pytest.raises(StooqParseError, match="unexpected CSV columns"):
        parse_stooq_historical_csv("AAPL.US", "No data available")


def test_parse_stooq_historical_csv_rejects_header_without_rows() -> None:
    csv_text = ",".join(EXPECTED_COLUMNS) + "\n"

    with pytest.raises(StooqParseError, match="no historical data rows found"):
        parse_stooq_historical_csv("AAPL.US", csv_text)


def test_parse_stooq_historical_csv_returns_stooq_provider() -> None:
    response = parse_stooq_historical_csv("AAPL.US", SAMPLE_CSV)

    assert response.provider == "stooq"


def test_parse_stooq_historical_csv_preserves_original_provider_symbol() -> None:
    response = parse_stooq_historical_csv("VUSA.NL", SAMPLE_CSV)

    assert response.provider_symbol == "VUSA.NL"


def test_fetch_stooq_historical_csv_uses_built_url(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(url: str, timeout: float) -> MockResponse:
        captured["url"] = url
        captured["timeout"] = timeout
        return MockResponse(SAMPLE_CSV.encode("utf-8"))

    monkeypatch.setattr(stooq_client.urllib_request, "urlopen", fake_urlopen)

    result = fetch_stooq_historical_csv("AAPL.US", timeout_seconds=3.5)

    assert result == SAMPLE_CSV
    assert captured == {
        "url": f"{STOOQ_BASE_URL}?s=aapl.us&i=d",
        "timeout": 3.5,
    }


def test_fetch_stooq_historical_csv_returns_decoded_utf8_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        stooq_client.urllib_request,
        "urlopen",
        lambda url, timeout: MockResponse(SAMPLE_CSV.encode("utf-8")),
    )

    assert fetch_stooq_historical_csv("NVDA.US") == SAMPLE_CSV


@pytest.mark.parametrize("timeout_seconds", [0.0, -1.0])
def test_fetch_stooq_historical_csv_rejects_non_positive_timeout(
    timeout_seconds: float,
) -> None:
    with pytest.raises(ValueError, match="timeout_seconds must be greater than 0"):
        fetch_stooq_historical_csv("AAPL.US", timeout_seconds=timeout_seconds)


def test_fetch_stooq_historical_csv_raises_network_error_on_http_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(url: str, timeout: float) -> MockResponse:
        raise urllib_error.HTTPError(
            url,
            503,
            "Service Unavailable",
            hdrs=Message(),
            fp=None,
        )

    monkeypatch.setattr(stooq_client.urllib_request, "urlopen", fake_urlopen)

    with pytest.raises(StooqNetworkError, match="HTTP error"):
        fetch_stooq_historical_csv("AAPL.US")


def test_fetch_stooq_historical_csv_raises_network_error_on_url_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(url: str, timeout: float) -> MockResponse:
        raise urllib_error.URLError("host unreachable")

    monkeypatch.setattr(stooq_client.urllib_request, "urlopen", fake_urlopen)

    with pytest.raises(StooqNetworkError, match="network error"):
        fetch_stooq_historical_csv("AAPL.US")


def test_fetch_stooq_historical_csv_raises_network_error_on_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(url: str, timeout: float) -> MockResponse:
        raise urllib_error.URLError(socket.timeout("timed out"))

    monkeypatch.setattr(stooq_client.urllib_request, "urlopen", fake_urlopen)

    with pytest.raises(StooqNetworkError, match="timeout"):
        fetch_stooq_historical_csv("AAPL.US")


def test_fetch_stooq_historical_csv_raises_network_error_on_empty_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        stooq_client.urllib_request,
        "urlopen",
        lambda url, timeout: MockResponse(b""),
    )

    with pytest.raises(StooqNetworkError, match="empty response"):
        fetch_stooq_historical_csv("AAPL.US")


def test_fetch_stooq_historical_csv_raises_network_error_on_decode_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        stooq_client.urllib_request,
        "urlopen",
        lambda url, timeout: MockResponse(b"\xff"),
    )

    with pytest.raises(StooqNetworkError, match="decode"):
        fetch_stooq_historical_csv("AAPL.US")


def test_fetch_stooq_historical_data_calls_fetch_and_parse(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called: dict[str, object] = {}

    def fake_fetch(
        provider_symbol: str,
        *,
        interval: str = "d",
        timeout_seconds: float = 10.0,
    ) -> str:
        called["fetch"] = (provider_symbol, interval, timeout_seconds)
        return SAMPLE_CSV

    def fake_parse(
        provider_symbol: str,
        csv_text: str,
        *,
        interval: str = "d",
    ) -> StooqHistoricalResponse:
        called["parse"] = (provider_symbol, csv_text, interval)
        return StooqHistoricalResponse(
            provider="stooq",
            provider_symbol=provider_symbol,
            interval=interval,
            rows=[],
        )

    monkeypatch.setattr(stooq_client, "fetch_stooq_historical_csv", fake_fetch)
    monkeypatch.setattr(stooq_client, "parse_stooq_historical_csv", fake_parse)

    result = fetch_stooq_historical_data("VUSA.NL", timeout_seconds=7.0)

    assert result.provider_symbol == "VUSA.NL"
    assert called["fetch"] == ("VUSA.NL", "d", 7.0)
    assert called["parse"] == ("VUSA.NL", SAMPLE_CSV, "d")
