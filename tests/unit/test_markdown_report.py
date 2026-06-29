from __future__ import annotations

import pytest

from market_xg.reports.markdown_report import generate_market_xg_markdown_report
from market_xg.scoring.market_xg_score import CategoryScore, MarketXGScore


def test_report_includes_title() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "# Market xG Report" in report


def test_report_includes_report_date() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "2026-06-29" in report


def test_report_includes_asset_name() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "S&P 500" in report


def test_report_includes_market_xg_score_with_one_decimal_place() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "74.0 / 100" in report


def test_report_includes_required_sections() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    for section in (
        "## Interpretation",
        "## Category Scores",
        "## Strengths",
        "## Weaknesses",
        "## Missing Categories",
        "## Method Note",
        "## Disclaimer",
    ):
        assert section in report


def test_report_includes_exact_disclaimer_sentences() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "Market xG is probabilistic decision support." in report
    assert "Market xG is not price prediction." in report
    assert "This report does not guarantee future returns or outcomes." in report


def test_report_renders_readable_category_name() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "Trend Momentum: 80.0 / 100" in report


def test_report_lists_category_strengths_with_prefix() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "- Trend Momentum: price above 200-day moving average" in report


def test_report_lists_category_weaknesses_with_prefix() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "- Trend Momentum: moderate drawdown from recent high" in report


def test_report_shows_fallback_text_when_no_strengths_exist() -> None:
    market_xg_score = MarketXGScore(
        score=50.0,
        category_scores={"trend_momentum": CategoryScore("trend_momentum", 50.0, [], [])},
        weights_used={"trend_momentum": 1.0},
        missing_categories=[],
        details=_details(50.0),
    )

    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=market_xg_score,
    )

    assert "- No clear strengths identified." in report


def test_report_shows_fallback_text_when_no_weaknesses_exist() -> None:
    market_xg_score = MarketXGScore(
        score=75.0,
        category_scores={
            "trend_momentum": CategoryScore(
                "trend_momentum",
                75.0,
                ["price above 200-day moving average"],
                [],
            )
        },
        weights_used={"trend_momentum": 1.0},
        missing_categories=[],
        details=_details(75.0),
    )

    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=market_xg_score,
    )

    assert "- No clear weaknesses identified." in report


def test_report_shows_readable_missing_categories() -> None:
    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=_sample_market_xg_score(),
    )

    assert "- Breadth Participation" in report
    assert "- Macro Rates" in report


def test_report_shows_fallback_text_when_no_missing_categories_exist() -> None:
    market_xg_score = MarketXGScore(
        score=74.0,
        category_scores={"trend_momentum": CategoryScore("trend_momentum", 74.0, [], [])},
        weights_used={"trend_momentum": 1.0},
        missing_categories=[],
        details=_details(74.0),
    )

    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=market_xg_score,
    )

    assert "- No missing categories." in report


@pytest.mark.parametrize(
    ("score", "expected_text"),
    [
        (80.0, "Strong market quality"),
        (65.0, "Constructive market quality"),
        (50.0, "Mixed market quality"),
        (35.0, "Fragile market quality"),
        (34.9, "Weak market quality"),
    ],
)
def test_report_interpretation_bands(score: float, expected_text: str) -> None:
    market_xg_score = MarketXGScore(
        score=score,
        category_scores={"trend_momentum": CategoryScore("trend_momentum", score, [], [])},
        weights_used={"trend_momentum": 1.0},
        missing_categories=[],
        details=_details(score),
    )

    report = generate_market_xg_markdown_report(
        report_date="2026-06-29",
        asset_name="S&P 500",
        market_xg_score=market_xg_score,
    )

    assert expected_text in report


def test_empty_report_date_raises_value_error() -> None:
    with pytest.raises(ValueError, match="report_date must be a non-empty string"):
        generate_market_xg_markdown_report(
            report_date="",
            asset_name="S&P 500",
            market_xg_score=_sample_market_xg_score(),
        )


def test_whitespace_only_report_date_raises_value_error() -> None:
    with pytest.raises(ValueError, match="report_date must be a non-empty string"):
        generate_market_xg_markdown_report(
            report_date="   ",
            asset_name="S&P 500",
            market_xg_score=_sample_market_xg_score(),
        )


def test_empty_asset_name_raises_value_error() -> None:
    with pytest.raises(ValueError, match="asset_name must be a non-empty string"):
        generate_market_xg_markdown_report(
            report_date="2026-06-29",
            asset_name="",
            market_xg_score=_sample_market_xg_score(),
        )


def test_whitespace_only_asset_name_raises_value_error() -> None:
    with pytest.raises(ValueError, match="asset_name must be a non-empty string"):
        generate_market_xg_markdown_report(
            report_date="2026-06-29",
            asset_name="   ",
            market_xg_score=_sample_market_xg_score(),
        )


def test_wrong_market_xg_score_type_raises_type_error() -> None:
    with pytest.raises(TypeError, match="market_xg_score must be a MarketXGScore instance"):
        generate_market_xg_markdown_report(
            report_date="2026-06-29",
            asset_name="S&P 500",
            market_xg_score="not a score",  # type: ignore[arg-type]
        )


def _sample_market_xg_score() -> MarketXGScore:
    return MarketXGScore(
        score=74.0,
        category_scores={
            "trend_momentum": CategoryScore(
                name="trend_momentum",
                score=80.0,
                strengths=["price above 200-day moving average"],
                weaknesses=["moderate drawdown from recent high"],
            ),
            "sentiment_volatility": CategoryScore(
                name="sentiment_volatility",
                score=62.0,
                strengths=["volatility remains contained"],
                weaknesses=[],
            ),
        },
        weights_used={
            "trend_momentum": 0.6666666666666666,
            "sentiment_volatility": 0.3333333333333333,
        },
        missing_categories=["breadth_participation", "macro_rates"],
        details=_details(74.0),
    )


def _details(score: float) -> dict[str, float | int | str | bool | None]:
    return {
        "raw_score": score,
        "final_score": score,
        "reweight_available_categories": True,
        "available_category_count": 1,
        "configured_category_count": 8,
    }
