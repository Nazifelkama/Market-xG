"""Phase 1 weighted Market xG aggregation."""

from __future__ import annotations

from dataclasses import dataclass


DEFAULT_CATEGORY_WEIGHTS = {
    "trend_momentum": 0.20,
    "breadth_participation": 0.20,
    "earnings_fundamentals": 0.15,
    "macro_rates": 0.15,
    "liquidity_flows": 0.10,
    "sentiment_volatility": 0.10,
    "volume_accumulation": 0.05,
    "valuation": 0.05,
}


@dataclass(frozen=True)
class CategoryScore:
    """A single category score used in Market xG aggregation."""

    name: str
    score: float
    strengths: list[str]
    weaknesses: list[str]

    def __post_init__(self) -> None:
        if self.name.strip() == "":
            raise ValueError("name must not be empty")
        if not 0 <= self.score <= 100:
            raise ValueError("score must be between 0 and 100")
        if not isinstance(self.strengths, list):
            raise ValueError("strengths must be a list")
        if not isinstance(self.weaknesses, list):
            raise ValueError("weaknesses must be a list")


@dataclass(frozen=True)
class MarketXGScore:
    """The aggregated Market xG score."""

    score: float
    category_scores: dict[str, CategoryScore]
    weights_used: dict[str, float]
    missing_categories: list[str]
    details: dict[str, float | int | str | bool | None]

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("score must be between 0 and 100")
        if not self.category_scores:
            raise ValueError("category_scores must not be empty")
        if not self.weights_used:
            raise ValueError("weights_used must not be empty")
        if not isinstance(self.missing_categories, list):
            raise ValueError("missing_categories must be a list")
        if not isinstance(self.details, dict):
            raise ValueError("details must be a dict")


def calculate_market_xg_score(
    category_scores: dict[str, CategoryScore],
    category_weights: dict[str, float] = DEFAULT_CATEGORY_WEIGHTS,
    *,
    reweight_available_categories: bool = True,
) -> MarketXGScore:
    """Aggregate category scores into a weighted Market xG score."""
    if not category_scores:
        raise ValueError("category_scores must not be empty")
    if not category_weights:
        raise ValueError("category_weights must not be empty")

    for category_name, weight in category_weights.items():
        if weight <= 0:
            raise ValueError(f"weight must be greater than 0: {category_name}")

    for category_name, category_score in category_scores.items():
        if category_name not in category_weights:
            raise ValueError(f"unknown category: {category_name}")
        if category_score.name != category_name:
            raise ValueError(f"category score name mismatch: {category_name}")

    missing_categories = [
        category_name
        for category_name in category_weights
        if category_name not in category_scores
    ]
    if not reweight_available_categories and missing_categories:
        raise ValueError("missing categories are not allowed when reweighting is disabled")

    if reweight_available_categories:
        weight_total = sum(category_weights[name] for name in category_scores)
        weights_used = {
            name: category_weights[name] / weight_total for name in category_scores
        }
    else:
        weights_used = {
            name: category_weights[name] for name in category_scores
        }

    raw_score = sum(
        category_scores[name].score * weights_used[name] for name in category_scores
    )
    final_score = min(100.0, max(0.0, raw_score))
    details: dict[str, float | int | str | bool | None] = {
        "raw_score": raw_score,
        "final_score": final_score,
        "reweight_available_categories": reweight_available_categories,
        "available_category_count": len(category_scores),
        "configured_category_count": len(category_weights),
    }

    return MarketXGScore(
        score=final_score,
        category_scores=category_scores,
        weights_used=weights_used,
        missing_categories=missing_categories,
        details=details,
    )
