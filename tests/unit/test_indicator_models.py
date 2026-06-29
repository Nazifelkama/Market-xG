from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from market_xg.indicators.models import (
    IndicatorResult,
    available_indicator,
    unavailable_indicator,
)


def test_available_indicator_result_can_be_created() -> None:
    result = IndicatorResult(name="sma_50", value=100.0, available=True)

    assert result.name == "sma_50"
    assert result.value == 100.0
    assert result.available is True
    assert result.reason is None


def test_unavailable_indicator_result_can_be_created() -> None:
    result = IndicatorResult(
        name="sma_200", value=None, available=False, reason="insufficient history"
    )

    assert result.name == "sma_200"
    assert result.value is None
    assert result.available is False
    assert result.reason == "insufficient history"


def test_empty_name_raises_value_error() -> None:
    with pytest.raises(ValueError, match="name must not be empty"):
        IndicatorResult(name="", value=1.0, available=True)


def test_whitespace_only_name_raises_value_error() -> None:
    with pytest.raises(ValueError, match="name must not be empty"):
        IndicatorResult(name="   ", value=1.0, available=True)


def test_available_true_with_value_none_raises_value_error() -> None:
    with pytest.raises(ValueError, match="available indicator must have a value"):
        IndicatorResult(name="mom_1m", value=None, available=True)


def test_available_true_with_reason_set_raises_value_error() -> None:
    with pytest.raises(
        ValueError, match="available indicator must not have a reason"
    ):
        IndicatorResult(name="mom_1m", value=1.0, available=True, reason="unexpected")


def test_available_false_with_value_set_raises_value_error() -> None:
    with pytest.raises(
        ValueError, match="unavailable indicator must not have a value"
    ):
        IndicatorResult(
            name="dd_252", value=0.0, available=False, reason="missing history"
        )


def test_available_false_with_reason_none_raises_value_error() -> None:
    with pytest.raises(
        ValueError, match="unavailable indicator must have a non-empty reason"
    ):
        IndicatorResult(name="dd_252", value=None, available=False, reason=None)


def test_available_false_with_empty_reason_raises_value_error() -> None:
    with pytest.raises(
        ValueError, match="unavailable indicator must have a non-empty reason"
    ):
        IndicatorResult(name="dd_252", value=None, available=False, reason="")


def test_negative_value_is_allowed_when_available() -> None:
    result = IndicatorResult(name="drawdown_252", value=-10.0, available=True)

    assert result.value == -10.0


def test_helper_available_indicator_creates_expected_result() -> None:
    result = available_indicator("sma_50", 123.4)

    assert result == IndicatorResult(name="sma_50", value=123.4, available=True)


def test_helper_unavailable_indicator_creates_expected_result() -> None:
    result = unavailable_indicator("sma_200", "insufficient history")

    assert result == IndicatorResult(
        name="sma_200",
        value=None,
        available=False,
        reason="insufficient history",
    )


def test_to_dict_returns_exact_expected_keys() -> None:
    result = available_indicator("mom_1m", 5.0)

    payload = result.to_dict()

    assert list(payload.keys()) == ["name", "value", "available", "reason"]


def test_to_dict_preserves_none_reason_for_available_indicator() -> None:
    payload = available_indicator("mom_1m", 5.0).to_dict()

    assert payload["reason"] is None


def test_to_dict_preserves_none_value_for_unavailable_indicator() -> None:
    payload = unavailable_indicator("mom_12m", "insufficient history").to_dict()

    assert payload["value"] is None


def test_dataclass_is_frozen_and_immutable() -> None:
    result = available_indicator("sma_50", 123.4)

    with pytest.raises(FrozenInstanceError):
        setattr(result, "name", "sma_200")
