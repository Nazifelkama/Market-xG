"""Minimal Technical UAT harness for provider-based analysis."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from market_xg.analysis.provider_analysis import (
    ProviderAnalysisError,
    analyze_stooq_historical_response,
)
from market_xg.data_providers.stooq_client import (
    StooqHistoricalResponse,
    StooqHistoricalRow,
)


ASSET_NAME = "Apple Inc."
REPORT_DATE = "2026-01-01"
REQUIRED_CATEGORIES = ("trend_momentum", "volume_accumulation")
DISCLAIMER_LINES = (
    "Market xG is probabilistic decision support.",
    "Market xG is not price prediction.",
    "This report does not guarantee future returns or outcomes.",
)
RISKY_WORDING = (
    "guaranteed return",
    "guaranteed profit",
    "certain future return",
)


@dataclass(frozen=True)
class UATScenarioOutcome:
    scenario_id: str
    scenario_name: str
    passed: bool
    mandatory: bool
    observed_score: float | None
    observed_categories: tuple[str, ...]
    observed_disclaimer: bool
    failure_message: str | None
    notes: str

    def __post_init__(self) -> None:
        if self.scenario_id.strip() == "":
            raise ValueError("scenario_id must not be empty")
        if self.scenario_name.strip() == "":
            raise ValueError("scenario_name must not be empty")
        if not isinstance(self.observed_categories, tuple):
            raise ValueError("observed_categories must be a tuple")
        if not isinstance(self.notes, str):
            raise ValueError("notes must be a string")
        if not self.passed and _is_blank(self.failure_message) and self.notes.strip() == "":
            raise ValueError("failed outcomes must include failure_message or notes")


def build_bullish_stooq_response(
    provider_symbol: str = "AAPL.US",
    rows: int = 260,
) -> StooqHistoricalResponse:
    return _build_response(provider_symbol=provider_symbol, rows=rows, pattern="bullish")


def build_weak_stooq_response(
    provider_symbol: str = "AAPL.US",
    rows: int = 260,
) -> StooqHistoricalResponse:
    return _build_response(provider_symbol=provider_symbol, rows=rows, pattern="weak")


def build_sideways_stooq_response(
    provider_symbol: str = "AAPL.US",
    rows: int = 260,
) -> StooqHistoricalResponse:
    return _build_response(provider_symbol=provider_symbol, rows=rows, pattern="sideways")


def build_insufficient_history_stooq_response(
    provider_symbol: str = "AAPL.US",
    rows: int = 100,
) -> StooqHistoricalResponse:
    return _build_response(provider_symbol=provider_symbol, rows=rows, pattern="bullish")


def build_invalid_ohlcv_stooq_response(
    provider_symbol: str = "AAPL.US",
    rows: int = 260,
) -> StooqHistoricalResponse:
    response = _build_response(provider_symbol=provider_symbol, rows=rows, pattern="bullish")
    response.rows[0] = StooqHistoricalRow(
        date=response.rows[0].date,
        open="100.00",
        high="98.00",
        low="99.00",
        close="100.00",
        volume="100000",
    )
    return response


def run_provider_analysis_uat_scenarios() -> list[UATScenarioOutcome]:
    """Run the deterministic UAT-001 through UAT-010 scenario set."""
    return [
        _run_happy_path(
            scenario_id="UAT-001",
            scenario_name="Bullish happy path",
            response=build_bullish_stooq_response(),
            require_missing_categories=True,
            notes="Bullish deterministic response should produce score, report, and disclosures.",
        ),
        _run_happy_path(
            scenario_id="UAT-002",
            scenario_name="Weak / downtrend happy path",
            response=build_weak_stooq_response(),
            require_missing_categories=False,
            notes="Weak deterministic response should still produce safe explanatory output.",
        ),
        _run_happy_path(
            scenario_id="UAT-003",
            scenario_name="Sideways / mixed market path",
            response=build_sideways_stooq_response(),
            require_missing_categories=False,
            notes="Sideways deterministic response should produce balanced readable output.",
        ),
        _run_expected_error(
            scenario_id="UAT-004",
            scenario_name="Insufficient history",
            response=build_insufficient_history_stooq_response(),
            expected_terms=("insufficient history", "required rows", "253 rows"),
            asset_name=ASSET_NAME,
            report_date=REPORT_DATE,
            notes="Insufficient history should raise ProviderAnalysisError.",
        ),
        _run_expected_error(
            scenario_id="UAT-005",
            scenario_name="Invalid OHLCV semantics",
            response=build_invalid_ohlcv_stooq_response(),
            expected_terms=("validation", "ohlcv"),
            asset_name=ASSET_NAME,
            report_date=REPORT_DATE,
            notes="Invalid OHLCV semantics should raise ProviderAnalysisError.",
        ),
        _run_invalid_metadata(),
        _run_provider_metadata_preservation(),
        _run_missing_categories_visible(),
        _run_mandatory_disclaimer(),
        UATScenarioOutcome(
            scenario_id="UAT-010",
            scenario_name="No live provider dependency",
            passed=True,
            mandatory=True,
            observed_score=None,
            observed_categories=(),
            observed_disclaimer=False,
            failure_message=None,
            notes=(
                "Harness uses deterministic builders only and does not import or call Stooq "
                "fetch functions."
            ),
        ),
    ]


def _build_response(provider_symbol: str, rows: int, pattern: str) -> StooqHistoricalResponse:
    start_date = date(2025, 1, 1)
    historical_rows: list[StooqHistoricalRow] = []

    for index in range(rows):
        close = _close_for_pattern(index, pattern)
        open_price = close - 0.25
        high = close + 1.0
        low = close - 1.0
        historical_rows.append(
            StooqHistoricalRow(
                date=(start_date + timedelta(days=index)).isoformat(),
                open=f"{open_price:.2f}",
                high=f"{high:.2f}",
                low=f"{low:.2f}",
                close=f"{close:.2f}",
                volume=str(100000 + ((index % 20) * 1000)),
            )
        )

    return StooqHistoricalResponse(
        provider="stooq",
        provider_symbol=provider_symbol,
        interval="d",
        rows=historical_rows,
    )


def _close_for_pattern(index: int, pattern: str) -> float:
    if pattern == "bullish":
        return 100.0 + (index * 0.5)
    if pattern == "weak":
        return 260.0 - (index * 0.4)
    if pattern == "sideways":
        return 150.0 + ((index % 6) - 3) * 0.35
    raise ValueError(f"unknown UAT response pattern: {pattern}")


def _run_happy_path(
    *,
    scenario_id: str,
    scenario_name: str,
    response: StooqHistoricalResponse,
    require_missing_categories: bool,
    notes: str,
) -> UATScenarioOutcome:
    try:
        result = analyze_stooq_historical_response(
            response,
            asset_name=ASSET_NAME,
            report_date=REPORT_DATE,
        )
    except ProviderAnalysisError as exc:
        return _failed_outcome(scenario_id, scenario_name, str(exc), notes)

    observed_categories = _category_names(result)
    checks = [
        _score_in_range(result.market_xg_score.score),
        _has_required_categories(observed_categories),
        result.markdown_report.strip() != "",
        _has_required_disclaimer(result.markdown_report),
    ]
    if require_missing_categories:
        checks.append(_missing_categories_visible(result))

    passed = all(checks)
    failure_message = None if passed else "happy path checks did not all pass"
    return UATScenarioOutcome(
        scenario_id=scenario_id,
        scenario_name=scenario_name,
        passed=passed,
        mandatory=True,
        observed_score=result.market_xg_score.score,
        observed_categories=observed_categories,
        observed_disclaimer=_has_required_disclaimer(result.markdown_report),
        failure_message=failure_message,
        notes=notes,
    )


def _run_expected_error(
    *,
    scenario_id: str,
    scenario_name: str,
    response: StooqHistoricalResponse,
    expected_terms: tuple[str, ...],
    asset_name: str,
    report_date: str,
    notes: str,
) -> UATScenarioOutcome:
    try:
        analyze_stooq_historical_response(
            response,
            asset_name=asset_name,
            report_date=report_date,
        )
    except ProviderAnalysisError as exc:
        message = str(exc)
        passed = any(term in message.lower() for term in expected_terms)
        return UATScenarioOutcome(
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            passed=passed,
            mandatory=True,
            observed_score=None,
            observed_categories=(),
            observed_disclaimer=False,
            failure_message=message,
            notes=notes,
        )

    return _failed_outcome(scenario_id, scenario_name, "expected ProviderAnalysisError", notes)


def _run_invalid_metadata() -> UATScenarioOutcome:
    response = build_bullish_stooq_response()
    messages: list[str] = []

    for asset_name, report_date in (("", REPORT_DATE), (ASSET_NAME, "   ")):
        try:
            analyze_stooq_historical_response(
                response,
                asset_name=asset_name,
                report_date=report_date,
            )
        except ProviderAnalysisError as exc:
            messages.append(str(exc))

    passed = len(messages) == 2 and "asset_name" in messages[0] and "report_date" in messages[1]
    return UATScenarioOutcome(
        scenario_id="UAT-006",
        scenario_name="Invalid request metadata",
        passed=passed,
        mandatory=True,
        observed_score=None,
        observed_categories=(),
        observed_disclaimer=False,
        failure_message=" | ".join(messages) if messages else "expected metadata failures",
        notes="Invalid asset_name and report_date should both raise ProviderAnalysisError.",
    )


def _run_provider_metadata_preservation() -> UATScenarioOutcome:
    result = analyze_stooq_historical_response(
        build_bullish_stooq_response(provider_symbol="AAPL.US"),
        asset_name=ASSET_NAME,
        report_date=REPORT_DATE,
    )
    passed = (
        result.provider == "stooq"
        and result.provider_symbol == "AAPL.US"
        and result.asset_name == ASSET_NAME
    )
    return UATScenarioOutcome(
        scenario_id="UAT-007",
        scenario_name="Provider metadata preservation",
        passed=passed,
        mandatory=True,
        observed_score=result.market_xg_score.score,
        observed_categories=_category_names(result),
        observed_disclaimer=_has_required_disclaimer(result.markdown_report),
        failure_message=None if passed else "provider metadata was not preserved",
        notes="Provider metadata is preserved on ProviderAnalysisResult, not OHLCV rows.",
    )


def _run_missing_categories_visible() -> UATScenarioOutcome:
    result = analyze_stooq_historical_response(
        build_bullish_stooq_response(),
        asset_name=ASSET_NAME,
        report_date=REPORT_DATE,
    )
    observed_categories = _category_names(result)
    passed = (
        _has_required_categories(observed_categories)
        and bool(result.market_xg_score.missing_categories)
        and _missing_categories_visible(result)
    )
    return UATScenarioOutcome(
        scenario_id="UAT-008",
        scenario_name="Missing future categories are visible",
        passed=passed,
        mandatory=True,
        observed_score=result.market_xg_score.score,
        observed_categories=observed_categories,
        observed_disclaimer=_has_required_disclaimer(result.markdown_report),
        failure_message=None if passed else "missing categories were not visible",
        notes="Current v0.1 score discloses missing future categories.",
    )


def _run_mandatory_disclaimer() -> UATScenarioOutcome:
    result = analyze_stooq_historical_response(
        build_bullish_stooq_response(),
        asset_name=ASSET_NAME,
        report_date=REPORT_DATE,
    )
    report_lower = result.markdown_report.lower()
    risky_wording_found = any(term in report_lower for term in RISKY_WORDING)
    passed = _has_required_disclaimer(result.markdown_report) and not risky_wording_found
    return UATScenarioOutcome(
        scenario_id="UAT-009",
        scenario_name="Mandatory disclaimer / safe wording",
        passed=passed,
        mandatory=True,
        observed_score=result.market_xg_score.score,
        observed_categories=_category_names(result),
        observed_disclaimer=_has_required_disclaimer(result.markdown_report),
        failure_message=None if passed else "mandatory disclaimer or safe wording check failed",
        notes="Report must include required disclaimers and avoid obvious guaranteed language.",
    )


def _category_names(result: object) -> tuple[str, ...]:
    market_xg_score = getattr(result, "market_xg_score")
    return tuple(market_xg_score.category_scores.keys())


def _score_in_range(score: float | None) -> bool:
    return score is not None and 0 <= score <= 100


def _has_required_categories(categories: tuple[str, ...]) -> bool:
    return all(category in categories for category in REQUIRED_CATEGORIES)


def _has_required_disclaimer(markdown_report: str) -> bool:
    return all(line in markdown_report for line in DISCLAIMER_LINES)


def _missing_categories_visible(result: object) -> bool:
    market_xg_score = getattr(result, "market_xg_score")
    markdown_report = getattr(result, "markdown_report")
    return bool(market_xg_score.missing_categories) and "## Missing Categories" in markdown_report


def _failed_outcome(
    scenario_id: str,
    scenario_name: str,
    failure_message: str,
    notes: str,
) -> UATScenarioOutcome:
    return UATScenarioOutcome(
        scenario_id=scenario_id,
        scenario_name=scenario_name,
        passed=False,
        mandatory=True,
        observed_score=None,
        observed_categories=(),
        observed_disclaimer=False,
        failure_message=failure_message,
        notes=notes,
    )


def _is_blank(value: str | None) -> bool:
    return value is None or value.strip() == ""
