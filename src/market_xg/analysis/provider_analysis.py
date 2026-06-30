"""Provider-based Market xG analysis orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from market_xg.data_providers.stooq_client import StooqHistoricalResponse
from market_xg.data_providers.stooq_normalizer import (
    normalize_and_validate_stooq_historical_response,
)
from market_xg.indicators.drawdown import latest_drawdown_from_rolling_high
from market_xg.indicators.momentum import momentum_summary
from market_xg.indicators.moving_average import latest_simple_moving_average
from market_xg.indicators.volume import (
    latest_average_volume,
    up_down_volume_summary,
    volume_ratio,
)
from market_xg.reports.markdown_report import generate_market_xg_markdown_report
from market_xg.scoring.market_xg_score import (
    CategoryScore,
    MarketXGScore,
    calculate_market_xg_score,
)
from market_xg.scoring.trend_momentum_score import calculate_trend_momentum_score
from market_xg.scoring.volume_accumulation_score import (
    calculate_volume_accumulation_score,
)


MINIMUM_HISTORY_ROWS = 253


class ProviderAnalysisError(ValueError):
    """Raised when provider-based analysis cannot be completed safely."""


@dataclass(frozen=True)
class ProviderAnalysisResult:
    provider: str
    provider_symbol: str
    asset_name: str
    report_date: str
    market_xg_score: MarketXGScore
    markdown_report: str
    details: dict[str, float | int | bool | str | None]

    def __post_init__(self) -> None:
        for field_name in ("provider", "provider_symbol", "asset_name", "report_date"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or value.strip() == "":
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.market_xg_score, MarketXGScore):
            raise ValueError("market_xg_score must be a MarketXGScore instance")
        if not isinstance(self.markdown_report, str) or self.markdown_report.strip() == "":
            raise ValueError("markdown_report must be a non-empty string")
        if not isinstance(self.details, dict):
            raise ValueError("details must be a dict")


def analyze_stooq_historical_response(
    response: StooqHistoricalResponse,
    *,
    asset_name: str,
    report_date: str,
) -> ProviderAnalysisResult:
    """Run deterministic Market xG analysis on an already-fetched Stooq response."""
    if not isinstance(response, StooqHistoricalResponse):
        raise ProviderAnalysisError("response must be a StooqHistoricalResponse")
    if not isinstance(asset_name, str) or asset_name.strip() == "":
        raise ProviderAnalysisError("asset_name must be a non-empty string")
    if not isinstance(report_date, str) or report_date.strip() == "":
        raise ProviderAnalysisError("report_date must be a non-empty string")

    try:
        normalized_rows = normalize_and_validate_stooq_historical_response(response)
    except Exception as exc:
        raise ProviderAnalysisError(
            f"failed to normalize and validate provider data: {exc}"
        ) from exc

    row_count = len(normalized_rows)
    if row_count < MINIMUM_HISTORY_ROWS:
        raise ProviderAnalysisError(
            f"at least {MINIMUM_HISTORY_ROWS} rows are required for provider analysis"
        )

    try:
        close_prices = [float(row["close"]) for row in normalized_rows]
        volumes = [float(row["volume"]) for row in normalized_rows]
        latest_close = close_prices[-1]
        latest_volume = volumes[-1]

        sma_50 = latest_simple_moving_average(close_prices, 50)
        sma_200 = latest_simple_moving_average(close_prices, 200)
        momentum = momentum_summary(close_prices)
        drawdown_252d = latest_drawdown_from_rolling_high(close_prices, 252)

        trend_momentum_score = calculate_trend_momentum_score(
            latest_close=latest_close,
            sma_50=sma_50,
            sma_200=sma_200,
            momentum_1m=momentum["1m"],
            momentum_3m=momentum["3m"],
            momentum_6m=momentum["6m"],
            momentum_12m=momentum["12m"],
            drawdown_252d=drawdown_252d,
        )

        avg_volume_50 = latest_average_volume(volumes, 50)
        latest_volume_ratio_50d = volume_ratio(latest_volume, avg_volume_50)
        up_down_summary_20d = up_down_volume_summary(close_prices, volumes, 20)
        price_change_20d = ((close_prices[-1] / close_prices[-21]) - 1.0) * 100.0
        up_down_volume_ratio_20d = up_down_summary_20d["up_down_volume_ratio"]

        volume_accumulation_score = calculate_volume_accumulation_score(
            price_change_20d=price_change_20d,
            latest_volume_ratio_50d=latest_volume_ratio_50d,
            up_down_volume_ratio_20d=up_down_volume_ratio_20d,
        )

        category_scores = {
            "trend_momentum": CategoryScore(
                name="trend_momentum",
                score=trend_momentum_score.score,
                strengths=trend_momentum_score.strengths,
                weaknesses=trend_momentum_score.weaknesses,
            ),
            "volume_accumulation": CategoryScore(
                name="volume_accumulation",
                score=volume_accumulation_score.score,
                strengths=volume_accumulation_score.strengths,
                weaknesses=volume_accumulation_score.weaknesses,
            ),
        }
        market_xg_score = calculate_market_xg_score(category_scores)
        markdown_report = generate_market_xg_markdown_report(
            report_date=report_date,
            asset_name=asset_name,
            market_xg_score=market_xg_score,
        )
    except Exception as exc:
        raise ProviderAnalysisError(f"failed to analyze provider data: {exc}") from exc

    details: dict[str, float | int | bool | str | None] = {
        "row_count": row_count,
        "latest_close": latest_close,
        "latest_volume": latest_volume,
        "sma_50": sma_50,
        "sma_200": sma_200,
        "drawdown_252d": drawdown_252d,
        "avg_volume_50": avg_volume_50,
        "latest_volume_ratio_50d": latest_volume_ratio_50d,
        "price_change_20d": price_change_20d,
        "up_down_volume_ratio_20d": up_down_volume_ratio_20d,
        "implemented_category_count": len(category_scores),
        "provider": response.provider,
    }

    try:
        return ProviderAnalysisResult(
            provider=response.provider,
            provider_symbol=response.provider_symbol,
            asset_name=asset_name,
            report_date=report_date,
            market_xg_score=market_xg_score,
            markdown_report=markdown_report,
            details=details,
        )
    except ValueError as exc:
        raise ProviderAnalysisError(f"invalid provider analysis result: {exc}") from exc
