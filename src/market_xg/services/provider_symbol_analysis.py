"""Provider-symbol Market xG analysis service."""

from __future__ import annotations

from dataclasses import dataclass

from market_xg.analysis.provider_analysis import (
    ProviderAnalysisError,
    ProviderAnalysisResult,
    analyze_stooq_historical_response,
)
from market_xg.data_providers.stooq_client import (
    StooqClientError,
    StooqNetworkError,
    StooqParseError,
    fetch_stooq_historical_data,
)


@dataclass(frozen=True)
class ProviderSymbolAnalysisFailure:
    provider: str
    provider_symbol: str
    asset_name: str
    report_date: str
    failure_category: str
    message: str

    def __post_init__(self) -> None:
        for field_name in (
            "provider",
            "provider_symbol",
            "asset_name",
            "report_date",
            "failure_category",
            "message",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or value.strip() == "":
                raise ValueError(f"{field_name} must be a non-empty string")


ProviderSymbolAnalysisOutcome = ProviderAnalysisResult | ProviderSymbolAnalysisFailure


def analyze_provider_symbol(
    *,
    provider: str,
    provider_symbol: str,
    asset_name: str,
    report_date: str,
    timeout_seconds: float = 10.0,
) -> ProviderSymbolAnalysisOutcome:
    """Analyze a direct provider symbol and return a success result or failure result."""
    invalid_message = _invalid_request_message(
        provider=provider,
        provider_symbol=provider_symbol,
        asset_name=asset_name,
        report_date=report_date,
        timeout_seconds=timeout_seconds,
    )
    if invalid_message is not None:
        return _failure(
            provider=provider,
            provider_symbol=provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            failure_category="invalid_request",
            message=invalid_message,
        )

    if provider.strip().lower() != "stooq":
        return _failure(
            provider=provider,
            provider_symbol=provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            failure_category="unsupported_provider",
            message="provider-symbol analysis v0.1 supports only the stooq provider",
        )

    try:
        response = fetch_stooq_historical_data(
            provider_symbol,
            interval="d",
            timeout_seconds=timeout_seconds,
        )
        return analyze_stooq_historical_response(
            response,
            asset_name=asset_name,
            report_date=report_date,
        )
    except StooqNetworkError as exc:
        return _failure(
            provider=provider,
            provider_symbol=provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            failure_category="provider_network_error",
            message=str(exc),
        )
    except StooqParseError as exc:
        return _failure(
            provider=provider,
            provider_symbol=provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            failure_category="provider_parse_error",
            message=str(exc),
        )
    except StooqClientError as exc:
        return _failure(
            provider=provider,
            provider_symbol=provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            failure_category="provider_error",
            message=str(exc),
        )
    except ProviderAnalysisError as exc:
        return _failure(
            provider=provider,
            provider_symbol=provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            failure_category="analysis_error",
            message=str(exc),
        )
    except Exception as exc:
        return _failure(
            provider=provider,
            provider_symbol=provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            failure_category="unknown_error",
            message=str(exc) or "unexpected provider-symbol analysis error",
        )


def _invalid_request_message(
    *,
    provider: str,
    provider_symbol: str,
    asset_name: str,
    report_date: str,
    timeout_seconds: float,
) -> str | None:
    if not _is_non_empty_string(provider):
        return "provider must be a non-empty string"
    if not _is_non_empty_string(provider_symbol):
        return "provider_symbol must be a non-empty string"
    if not _is_non_empty_string(asset_name):
        return "asset_name must be a non-empty string"
    if not _is_non_empty_string(report_date):
        return "report_date must be a non-empty string"
    if timeout_seconds <= 0:
        return "timeout_seconds must be greater than 0"
    return None


def _is_non_empty_string(value: str) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _failure(
    *,
    provider: str,
    provider_symbol: str,
    asset_name: str,
    report_date: str,
    failure_category: str,
    message: str,
) -> ProviderSymbolAnalysisFailure:
    return ProviderSymbolAnalysisFailure(
        provider=_failure_field_value(provider),
        provider_symbol=_failure_field_value(provider_symbol),
        asset_name=_failure_field_value(asset_name),
        report_date=_failure_field_value(report_date),
        failure_category=failure_category,
        message=message,
    )


def _failure_field_value(value: str) -> str:
    if isinstance(value, str) and value.strip() != "":
        return value
    return "invalid"
