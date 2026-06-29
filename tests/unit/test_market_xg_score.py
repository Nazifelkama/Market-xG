from __future__ import annotations

from dataclasses import fields

import pytest

from market_xg.scoring.market_xg_score import (
    CategoryScore,
    MarketXGScore,
    calculate_market_xg_score,
)


def test_category_score_valid_creation() -> None:
    score = CategoryScore(
        name="trend_momentum",
        score=80.0,
        strengths=["trend strong"],
        weaknesses=[],
    )

    assert score.name == "trend_momentum"
    assert score.score == 80.0


def test_category_score_rejects_score_below_zero() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        CategoryScore("trend_momentum", -1.0, [], [])


def test_category_score_rejects_score_above_one_hundred() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        CategoryScore("trend_momentum", 101.0, [], [])


def test_category_score_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="name must not be empty"):
        CategoryScore("", 50.0, [], [])


def test_category_score_rejects_whitespace_only_name() -> None:
    with pytest.raises(ValueError, match="name must not be empty"):
        CategoryScore("   ", 50.0, [], [])


def test_category_score_rejects_non_list_strengths() -> None:
    with pytest.raises(ValueError, match="strengths must be a list"):
        CategoryScore("trend_momentum", 50.0, "bad", [])


def test_category_score_rejects_non_list_weaknesses() -> None:
    with pytest.raises(ValueError, match="weaknesses must be a list"):
        CategoryScore("trend_momentum", 50.0, [], "bad")


def test_market_xg_score_rejects_score_below_zero() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        MarketXGScore(-1.0, {"trend_momentum": _trend_score(50.0)}, {"trend_momentum": 1.0}, [], {})


def test_market_xg_score_rejects_score_above_one_hundred() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        MarketXGScore(101.0, {"trend_momentum": _trend_score(50.0)}, {"trend_momentum": 1.0}, [], {})


def test_empty_category_scores_raises_value_error() -> None:
    with pytest.raises(ValueError, match="category_scores must not be empty"):
        calculate_market_xg_score({})


def test_empty_category_weights_raises_value_error() -> None:
    with pytest.raises(ValueError, match="category_weights must not be empty"):
        calculate_market_xg_score({"trend_momentum": _trend_score(80.0)}, {})


def test_unknown_category_name_raises_value_error() -> None:
    with pytest.raises(ValueError, match="unknown category"):
        calculate_market_xg_score({"unknown": CategoryScore("unknown", 80.0, [], [])})


def test_invalid_zero_weight_raises_value_error() -> None:
    weights = {"trend_momentum": 0.0}

    with pytest.raises(ValueError, match="weight must be greater than 0"):
        calculate_market_xg_score({"trend_momentum": _trend_score(80.0)}, weights)


def test_invalid_negative_weight_raises_value_error() -> None:
    weights = {"trend_momentum": -0.1}

    with pytest.raises(ValueError, match="weight must be greater than 0"):
        calculate_market_xg_score({"trend_momentum": _trend_score(80.0)}, weights)


def test_single_trend_momentum_category_with_reweighting_returns_same_score() -> None:
    result = calculate_market_xg_score({"trend_momentum": _trend_score(80.0)})

    assert result.score == 80.0


def test_multiple_categories_aggregate_correctly() -> None:
    category_scores = {
        "trend_momentum": _trend_score(80.0),
        "macro_rates": CategoryScore("macro_rates", 60.0, [], []),
    }
    category_weights = {
        "trend_momentum": 0.20,
        "macro_rates": 0.15,
    }

    result = calculate_market_xg_score(category_scores, category_weights)

    expected = 80.0 * (0.20 / 0.35) + 60.0 * (0.15 / 0.35)
    assert result.score == pytest.approx(expected)


def test_missing_categories_are_listed_when_reweighting() -> None:
    result = calculate_market_xg_score({"trend_momentum": _trend_score(80.0)})

    assert "breadth_participation" in result.missing_categories
    assert "valuation" in result.missing_categories


def test_missing_categories_raise_value_error_when_reweighting_disabled() -> None:
    with pytest.raises(ValueError, match="missing categories"):
        calculate_market_xg_score(
            {"trend_momentum": _trend_score(80.0)},
            reweight_available_categories=False,
        )


def test_no_fake_scores_are_created_for_missing_categories() -> None:
    result = calculate_market_xg_score({"trend_momentum": _trend_score(80.0)})

    assert set(result.category_scores.keys()) == {"trend_momentum"}


def test_weights_used_sum_to_one_when_reweighting() -> None:
    category_scores = {
        "trend_momentum": _trend_score(80.0),
        "macro_rates": CategoryScore("macro_rates", 60.0, [], []),
    }

    result = calculate_market_xg_score(category_scores)

    assert sum(result.weights_used.values()) == pytest.approx(1.0)


def test_details_contains_expected_keys() -> None:
    result = calculate_market_xg_score({"trend_momentum": _trend_score(80.0)})

    assert set(result.details.keys()) == {
        "raw_score",
        "final_score",
        "reweight_available_categories",
        "available_category_count",
        "configured_category_count",
    }


def test_raw_score_and_final_score_are_present_in_details() -> None:
    result = calculate_market_xg_score({"trend_momentum": _trend_score(80.0)})

    assert "raw_score" in result.details
    assert "final_score" in result.details


def test_market_xg_score_does_not_expose_top_level_strengths_or_weaknesses_fields() -> None:
    field_names = {field.name for field in fields(MarketXGScore)}

    assert "strengths" not in field_names
    assert "weaknesses" not in field_names


def _trend_score(score: float) -> CategoryScore:
    return CategoryScore(
        name="trend_momentum",
        score=score,
        strengths=["trend strong"] if score > 50 else [],
        weaknesses=["trend weak"] if score < 50 else [],
    )
