from __future__ import annotations

from datetime import date, timedelta
import inspect
from typing import cast

import pytest

from market_xg.analysis import provider_analysis
from market_xg.analysis.provider_analysis import (
    ProviderAnalysisError,
    ProviderAnalysisResult,
    analyze_stooq_historical_response,
)
from market_xg.data_providers import stooq_client
from market_xg.data_providers.stooq_client import (
    StooqHistoricalResponse,
    StooqHistoricalRow,
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


def test_analyze_stooq_historical_response_returns_result() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert isinstance(result, ProviderAnalysisResult)


def test_result_preserves_provider_fields() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert result.provider == "stooq"
    assert result.provider_symbol == "AAPL.US"


def test_result_preserves_asset_name_and_report_date() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert result.asset_name == "Apple Inc."
    assert result.report_date == "2026-06-30"


def test_market_xg_score_is_between_zero_and_one_hundred() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert 0 <= result.market_xg_score.score <= 100


def test_market_xg_score_contains_two_implemented_categories() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert "trend_momentum" in result.market_xg_score.category_scores
    assert "volume_accumulation" in result.market_xg_score.category_scores


def test_market_xg_weights_sum_to_one() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert sum(result.market_xg_score.weights_used.values()) == pytest.approx(1.0)


def test_markdown_report_contains_expected_content() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert "# Market xG Report" in result.markdown_report
    assert "Apple Inc." in result.markdown_report
    assert "Trend Momentum" in result.markdown_report
    assert "Volume Accumulation" in result.markdown_report
    assert "Market xG is not price prediction." in result.markdown_report


def test_details_include_expected_keys() -> None:
    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert {
        "row_count",
        "latest_close",
        "latest_volume",
        "sma_50",
        "sma_200",
        "drawdown_252d",
        "avg_volume_50",
        "latest_volume_ratio_50d",
        "price_change_20d",
        "up_down_volume_ratio_20d",
        "implemented_category_count",
        "provider",
    } <= set(result.details.keys())


def test_fewer_than_required_rows_raises_provider_analysis_error() -> None:
    with pytest.raises(ProviderAnalysisError, match="at least 253 rows"):
        analyze_stooq_historical_response(
            build_response(row_count=252),
            asset_name="Apple Inc.",
            report_date="2026-06-30",
        )


@pytest.mark.parametrize("asset_name", ["", "   "])
def test_invalid_asset_name_raises_provider_analysis_error(asset_name: str) -> None:
    with pytest.raises(ProviderAnalysisError, match="asset_name must be a non-empty string"):
        analyze_stooq_historical_response(
            build_response(),
            asset_name=asset_name,
            report_date="2026-06-30",
        )


@pytest.mark.parametrize("report_date", ["", "   "])
def test_invalid_report_date_raises_provider_analysis_error(report_date: str) -> None:
    with pytest.raises(ProviderAnalysisError, match="report_date must be a non-empty string"):
        analyze_stooq_historical_response(
            build_response(),
            asset_name="Apple Inc.",
            report_date=report_date,
        )


def test_wrong_response_type_raises_provider_analysis_error() -> None:
    with pytest.raises(ProviderAnalysisError, match="StooqHistoricalResponse"):
        analyze_stooq_historical_response(
            cast(StooqHistoricalResponse, object()),
            asset_name="Apple Inc.",
            report_date="2026-06-30",
        )


def test_normalization_failure_is_wrapped_as_provider_analysis_error() -> None:
    response = build_response()
    response.rows[0] = StooqHistoricalRow(
        date="2026-01-01",
        open="",
        high="101.00",
        low="98.00",
        close="100.00",
        volume="100000",
    )

    with pytest.raises(ProviderAnalysisError, match="failed to normalize and validate"):
        analyze_stooq_historical_response(
            response,
            asset_name="Apple Inc.",
            report_date="2026-06-30",
        )


def test_no_live_stooq_network_function_is_called(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        stooq_client,
        "fetch_stooq_historical_csv",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network fetch called")),
    )
    monkeypatch.setattr(
        stooq_client,
        "fetch_stooq_historical_data",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network fetch called")),
    )

    result = analyze_stooq_historical_response(
        build_response(),
        asset_name="Apple Inc.",
        report_date="2026-06-30",
    )

    assert result.provider == "stooq"


def test_provider_analysis_does_not_import_fetch_functions() -> None:
    source = inspect.getsource(provider_analysis)

    assert "fetch_stooq_historical_csv" not in source
    assert "fetch_stooq_historical_data" not in source
