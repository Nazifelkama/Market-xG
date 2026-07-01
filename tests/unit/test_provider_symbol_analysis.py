from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pytest

from market_xg.analysis.provider_analysis import (
    ProviderAnalysisError,
    ProviderAnalysisResult,
)
from market_xg.data_providers.stooq_client import (
    StooqClientError,
    StooqHistoricalResponse,
    StooqHistoricalRow,
    StooqNetworkError,
    StooqParseError,
)
from market_xg.services import provider_symbol_analysis
from market_xg.services.provider_symbol_analysis import (
    ProviderSymbolAnalysisFailure,
    analyze_provider_symbol,
)


def build_response(row_count: int = 260) -> StooqHistoricalResponse:
    rows: list[StooqHistoricalRow] = []
    start_date = date(2025, 1, 1)
    for index in range(row_count):
        base_close = 100.0 + index
        row_date = start_date + timedelta(days=index)
        rows.append(
            StooqHistoricalRow(
                date=row_date.isoformat(),
                open=f"{base_close - 1:.2f}",
                high=f"{base_close + 1:.2f}",
                low=f"{base_close - 2:.2f}",
                close=f"{base_close:.2f}",
                volume=str(100000 + (index * 1000)),
            )
        )
    return StooqHistoricalResponse(
        provider="stooq",
        provider_symbol="AAPL.US",
        interval="d",
        rows=rows,
    )


def test_successful_stooq_path_returns_provider_analysis_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        provider_symbol_analysis,
        "fetch_stooq_historical_data",
        lambda *args, **kwargs: build_response(),
    )

    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderAnalysisResult)


def test_fetch_function_is_called_with_expected_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_fetch(
        provider_symbol: str,
        *,
        interval: str,
        timeout_seconds: float,
    ) -> StooqHistoricalResponse:
        captured["provider_symbol"] = provider_symbol
        captured["interval"] = interval
        captured["timeout_seconds"] = timeout_seconds
        return build_response()

    monkeypatch.setattr(provider_symbol_analysis, "fetch_stooq_historical_data", fake_fetch)

    analyze_provider_symbol(
        provider="stooq",
        provider_symbol="NVDA.US",
        asset_name="Nvidia",
        report_date="2026-06-30",
        timeout_seconds=2.5,
    )

    assert captured == {
        "provider_symbol": "NVDA.US",
        "interval": "d",
        "timeout_seconds": 2.5,
    }


def test_provider_matching_is_case_insensitive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        provider_symbol_analysis,
        "fetch_stooq_historical_data",
        lambda *args, **kwargs: build_response(),
    )

    result = analyze_provider_symbol(
        provider="StOoQ",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderAnalysisResult)


def test_result_preserves_provider_symbol_asset_name_and_report_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        provider_symbol_analysis,
        "fetch_stooq_historical_data",
        lambda *args, **kwargs: build_response(),
    )

    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderAnalysisResult)
    assert result.provider_symbol == "AAPL.US"
    assert result.asset_name == "Apple Inc."
    assert result.report_date == "2026-06-30"


def test_unsupported_provider_returns_failure() -> None:
    result = analyze_provider_symbol(
        provider="other",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.failure_category == "unsupported_provider"


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("provider", ""),
        ("provider", "   "),
        ("provider_symbol", ""),
        ("provider_symbol", "   "),
        ("asset_name", ""),
        ("asset_name", "   "),
        ("report_date", ""),
        ("report_date", "   "),
    ],
)
def test_empty_request_fields_return_invalid_request(
    field_name: str,
    invalid_value: str,
) -> None:
    provider = invalid_value if field_name == "provider" else "stooq"
    provider_symbol = invalid_value if field_name == "provider_symbol" else "AAPL.US"
    asset_name = invalid_value if field_name == "asset_name" else "Apple Inc."
    report_date = invalid_value if field_name == "report_date" else "2026-06-30"

    result = analyze_provider_symbol(
        provider=provider,
        provider_symbol=provider_symbol,
        asset_name=asset_name,
        report_date=report_date,
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.failure_category == "invalid_request"
    assert field_name in result.message


def test_non_positive_timeout_returns_invalid_request() -> None:
    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
        timeout_seconds=0,
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.failure_category == "invalid_request"
    assert "timeout_seconds" in result.message


@pytest.mark.parametrize(
    ("exception", "failure_category"),
    [
        (StooqNetworkError("network down"), "provider_network_error"),
        (StooqParseError("bad csv"), "provider_parse_error"),
        (StooqClientError("client problem"), "provider_error"),
    ],
)
def test_stooq_client_errors_map_to_failure_categories(
    monkeypatch: pytest.MonkeyPatch,
    exception: StooqClientError,
    failure_category: str,
) -> None:
    def fake_fetch(*args: object, **kwargs: object) -> StooqHistoricalResponse:
        raise exception

    monkeypatch.setattr(provider_symbol_analysis, "fetch_stooq_historical_data", fake_fetch)

    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.failure_category == failure_category


def test_provider_analysis_error_maps_to_analysis_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        provider_symbol_analysis,
        "fetch_stooq_historical_data",
        lambda *args, **kwargs: build_response(row_count=252),
    )

    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.failure_category == "analysis_error"


def test_provider_analysis_error_from_orchestrator_maps_to_analysis_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_analyze(*args: object, **kwargs: object) -> ProviderAnalysisResult:
        raise ProviderAnalysisError("analysis failed")

    monkeypatch.setattr(
        provider_symbol_analysis,
        "fetch_stooq_historical_data",
        lambda *args, **kwargs: build_response(),
    )
    monkeypatch.setattr(provider_symbol_analysis, "analyze_stooq_historical_response", fake_analyze)

    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.failure_category == "analysis_error"


def test_unexpected_exception_maps_to_unknown_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(*args: object, **kwargs: object) -> StooqHistoricalResponse:
        raise RuntimeError("surprise")

    monkeypatch.setattr(provider_symbol_analysis, "fetch_stooq_historical_data", fake_fetch)

    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.failure_category == "unknown_error"


def test_failure_result_preserves_request_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(*args: object, **kwargs: object) -> StooqHistoricalResponse:
        raise StooqNetworkError("network down")

    monkeypatch.setattr(provider_symbol_analysis, "fetch_stooq_historical_data", fake_fetch)

    result = analyze_provider_symbol(
        provider="Stooq",
        provider_symbol="NVDA.US",
        asset_name="Nvidia",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderSymbolAnalysisFailure)
    assert result.provider == "Stooq"
    assert result.provider_symbol == "NVDA.US"
    assert result.asset_name == "Nvidia"
    assert result.report_date == "2026-06-30"


def test_failure_dataclass_rejects_empty_fields() -> None:
    with pytest.raises(ValueError, match="message must be a non-empty string"):
        ProviderSymbolAnalysisFailure(
            provider="stooq",
            provider_symbol="AAPL.US",
            asset_name="Apple Inc.",
            report_date="2026-06-30",
            failure_category="invalid_request",
            message="",
        )


def test_no_live_stooq_call_is_made(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(*args: object, **kwargs: object) -> StooqHistoricalResponse:
        return build_response()

    monkeypatch.setattr(provider_symbol_analysis, "fetch_stooq_historical_data", fake_fetch)

    result = analyze_provider_symbol(
        provider="stooq",
        provider_symbol="AAPL.US",
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderAnalysisResult)
