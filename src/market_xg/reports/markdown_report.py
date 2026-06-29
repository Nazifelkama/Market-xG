"""Phase 1 markdown Market xG reporting."""

from __future__ import annotations

from market_xg.scoring.market_xg_score import MarketXGScore


def generate_market_xg_markdown_report(
    *,
    report_date: str,
    asset_name: str,
    market_xg_score: MarketXGScore,
) -> str:
    """Generate a deterministic markdown Market xG report."""
    if report_date.strip() == "":
        raise ValueError("report_date must be a non-empty string")
    if asset_name.strip() == "":
        raise ValueError("asset_name must be a non-empty string")
    if not isinstance(market_xg_score, MarketXGScore):
        raise TypeError("market_xg_score must be a MarketXGScore instance")

    lines = [
        "# Market xG Report",
        "",
        "## Summary",
        f"- Report date: {report_date}",
        f"- Asset name: {asset_name}",
        f"- Market xG score: {market_xg_score.score:.1f} / 100",
        "",
        "## Interpretation",
        _interpretation_text(market_xg_score.score),
        "",
        "## Category Scores",
    ]

    for category_name, category_score in market_xg_score.category_scores.items():
        lines.append(
            f"- {_readable_category_name(category_name)}: {category_score.score:.1f} / 100"
        )

    lines.extend(["", "## Strengths"])
    strength_lines = _category_message_lines(
        market_xg_score=market_xg_score,
        use_strengths=True,
    )
    if strength_lines:
        lines.extend(strength_lines)
    else:
        lines.append("- No clear strengths identified.")

    lines.extend(["", "## Weaknesses"])
    weakness_lines = _category_message_lines(
        market_xg_score=market_xg_score,
        use_strengths=False,
    )
    if weakness_lines:
        lines.extend(weakness_lines)
    else:
        lines.append("- No clear weaknesses identified.")

    lines.extend(["", "## Missing Categories"])
    if market_xg_score.missing_categories:
        for category_name in market_xg_score.missing_categories:
            lines.append(f"- {_readable_category_name(category_name)}")
    else:
        lines.append("- No missing categories.")

    lines.extend(
        [
            "",
            "## Method Note",
            "- This report is generated from available category scores only.",
            "- Missing categories are not assigned fake scores.",
            "",
            "## Disclaimer",
            "- Market xG is probabilistic decision support.",
            "- Market xG is not price prediction.",
            "- This report does not guarantee future returns or outcomes.",
        ]
    )

    return "\n".join(lines)


def _interpretation_text(score: float) -> str:
    if score >= 80:
        return "Strong market quality"
    if score >= 65:
        return "Constructive market quality"
    if score >= 50:
        return "Mixed market quality"
    if score >= 35:
        return "Fragile market quality"
    return "Weak market quality"


def _readable_category_name(category_name: str) -> str:
    return category_name.replace("_", " ").title()


def _category_message_lines(
    *,
    market_xg_score: MarketXGScore,
    use_strengths: bool,
) -> list[str]:
    lines: list[str] = []
    for category_name, category_score in market_xg_score.category_scores.items():
        messages = category_score.strengths if use_strengths else category_score.weaknesses
        readable_name = _readable_category_name(category_name)
        for message in messages:
            lines.append(f"- {readable_name}: {message}")
    return lines
