from __future__ import annotations

import inspect

import pytest

from market_xg.analysis.provider_analysis import ProviderAnalysisError
from market_xg.data_providers import stooq_client
from market_xg.data_providers.stooq_client import StooqHistoricalResponse
from market_xg.uat import provider_analysis_uat
from market_xg.uat.provider_analysis_uat import (
    UATScenarioOutcome,
    build_bullish_stooq_response,
    build_insufficient_history_stooq_response,
    build_invalid_ohlcv_stooq_response,
    build_sideways_stooq_response,
    build_weak_stooq_response,
    run_provider_analysis_uat_scenarios,
)


def test_builders_return_stooq_historical_response() -> None:
    builders = (
        build_bullish_stooq_response,
        build_weak_stooq_response,
        build_sideways_stooq_response,
        build_insufficient_history_stooq_response,
        build_invalid_ohlcv_stooq_response,
    )

    for builder in builders:
        assert isinstance(builder(), StooqHistoricalResponse)


def test_bullish_builder_creates_generally_rising_closes() -> None:
    response = build_bullish_stooq_response()

    assert float(response.rows[-1].close) > float(response.rows[0].close)


def test_weak_builder_creates_generally_falling_closes() -> None:
    response = build_weak_stooq_response()

    assert float(response.rows[-1].close) < float(response.rows[0].close)


def test_sideways_builder_creates_mostly_mixed_sideways_closes() -> None:
    response = build_sideways_stooq_response()
    closes = [float(row.close) for row in response.rows]

    assert max(closes) - min(closes) < 3.0
    assert len(set(closes[:12])) > 2


def test_insufficient_builder_creates_fewer_than_required_rows() -> None:
    response = build_insufficient_history_stooq_response()

    assert len(response.rows) < 253


def test_invalid_ohlcv_builder_fails_provider_analysis() -> None:
    response = build_invalid_ohlcv_stooq_response()

    with pytest.raises(ProviderAnalysisError):
        provider_analysis_uat.analyze_stooq_historical_response(
            response,
            asset_name="Apple Inc.",
            report_date="2026-01-01",
        )


def test_run_provider_analysis_uat_scenarios_returns_ten_outcomes() -> None:
    outcomes = run_provider_analysis_uat_scenarios()

    assert len(outcomes) == 10
    assert all(isinstance(outcome, UATScenarioOutcome) for outcome in outcomes)


def test_scenario_ids_are_exactly_uat_001_through_uat_010() -> None:
    outcomes = run_provider_analysis_uat_scenarios()

    assert [outcome.scenario_id for outcome in outcomes] == [
        "UAT-001",
        "UAT-002",
        "UAT-003",
        "UAT-004",
        "UAT-005",
        "UAT-006",
        "UAT-007",
        "UAT-008",
        "UAT-009",
        "UAT-010",
    ]


def test_all_outcomes_are_mandatory() -> None:
    outcomes = run_provider_analysis_uat_scenarios()

    assert all(outcome.mandatory for outcome in outcomes)


def test_each_outcome_has_scenario_name_and_notes() -> None:
    outcomes = run_provider_analysis_uat_scenarios()

    assert all(outcome.scenario_name for outcome in outcomes)
    assert all(outcome.notes for outcome in outcomes)


def test_happy_path_outcomes_include_observed_score() -> None:
    outcomes = run_provider_analysis_uat_scenarios()

    for outcome in outcomes[:3]:
        assert outcome.observed_score is not None


def test_happy_path_categories_include_implemented_categories() -> None:
    outcomes = run_provider_analysis_uat_scenarios()

    for outcome in outcomes[:3]:
        assert "trend_momentum" in outcome.observed_categories
        assert "volume_accumulation" in outcome.observed_categories


def test_uat_004_records_expected_provider_analysis_error_evidence() -> None:
    outcome = run_provider_analysis_uat_scenarios()[3]

    assert outcome.scenario_id == "UAT-004"
    assert outcome.passed
    assert outcome.failure_message is not None
    assert "253 rows" in outcome.failure_message


def test_uat_005_records_expected_provider_analysis_error_evidence() -> None:
    outcome = run_provider_analysis_uat_scenarios()[4]

    assert outcome.scenario_id == "UAT-005"
    assert outcome.passed
    assert outcome.failure_message is not None
    assert "validation" in outcome.failure_message.lower()


def test_uat_006_records_invalid_metadata_evidence() -> None:
    outcome = run_provider_analysis_uat_scenarios()[5]

    assert outcome.scenario_id == "UAT-006"
    assert outcome.passed
    assert outcome.failure_message is not None
    assert "asset_name" in outcome.failure_message
    assert "report_date" in outcome.failure_message


def test_provider_analysis_uat_does_not_import_fetch_functions() -> None:
    source = inspect.getsource(provider_analysis_uat)

    assert "fetch_stooq_historical_csv" not in source
    assert "fetch_stooq_historical_data" not in source


def test_no_live_network_function_is_called(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        stooq_client,
        "fetch_stooq_historical_csv",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network called")),
    )
    monkeypatch.setattr(
        stooq_client,
        "fetch_stooq_historical_data",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network called")),
    )

    outcomes = run_provider_analysis_uat_scenarios()

    assert len(outcomes) == 10
