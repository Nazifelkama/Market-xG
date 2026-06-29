"""Phase 1 Trend and Momentum scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrendMomentumScore:
    """Deterministic Phase 1 Trend and Momentum score output."""

    score: float
    strengths: list[str]
    weaknesses: list[str]
    details: dict[str, float | bool | str | None]

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("score must be between 0 and 100")
        if not isinstance(self.strengths, list):
            raise ValueError("strengths must be a list")
        if not isinstance(self.weaknesses, list):
            raise ValueError("weaknesses must be a list")
        if not isinstance(self.details, dict):
            raise ValueError("details must be a dict")


def calculate_trend_momentum_score(
    latest_close: float,
    sma_50: float | None,
    sma_200: float | None,
    momentum_1m: float | None,
    momentum_3m: float | None,
    momentum_6m: float | None,
    momentum_12m: float | None,
    drawdown_252d: float | None,
) -> TrendMomentumScore:
    """Calculate the Phase 1 Trend and Momentum score."""
    _validate_inputs(
        latest_close=latest_close,
        sma_50=sma_50,
        sma_200=sma_200,
        drawdown_252d=drawdown_252d,
    )

    raw_score = 50.0
    strengths: list[str] = []
    weaknesses: list[str] = []

    if sma_50 is not None:
        if latest_close > sma_50:
            raw_score += 10
            strengths.append("price above 50-day moving average")
        elif latest_close < sma_50:
            raw_score -= 10
            weaknesses.append("price below 50-day moving average")

    if sma_200 is not None:
        if latest_close > sma_200:
            raw_score += 15
            strengths.append("price above 200-day moving average")
        elif latest_close < sma_200:
            raw_score -= 15
            weaknesses.append("price below 200-day moving average")

    if sma_50 is not None and sma_200 is not None:
        if sma_50 > sma_200:
            raw_score += 10
            strengths.append("50-day moving average above 200-day moving average")
        elif sma_50 < sma_200:
            raw_score -= 10
            weaknesses.append("50-day moving average below 200-day moving average")

    raw_score = _apply_momentum_rule(
        raw_score, momentum_1m, "1-month", strengths, weaknesses
    )
    raw_score = _apply_momentum_rule(
        raw_score, momentum_3m, "3-month", strengths, weaknesses
    )
    raw_score = _apply_momentum_rule(
        raw_score, momentum_6m, "6-month", strengths, weaknesses
    )
    raw_score = _apply_momentum_rule(
        raw_score, momentum_12m, "12-month", strengths, weaknesses
    )

    if drawdown_252d is not None:
        if drawdown_252d >= -5:
            raw_score += 5
            strengths.append("price close to 252-day high")
        elif drawdown_252d <= -20:
            raw_score -= 10
            weaknesses.append("deep drawdown from 252-day high")

    final_score = min(100.0, max(0.0, raw_score))
    details: dict[str, float | bool | str | None] = {
        "latest_close": latest_close,
        "sma_50": sma_50,
        "sma_200": sma_200,
        "momentum_1m": momentum_1m,
        "momentum_3m": momentum_3m,
        "momentum_6m": momentum_6m,
        "momentum_12m": momentum_12m,
        "drawdown_252d": drawdown_252d,
        "price_above_sma_50": None if sma_50 is None else latest_close > sma_50,
        "price_above_sma_200": None if sma_200 is None else latest_close > sma_200,
        "sma_50_above_sma_200": (
            None if sma_50 is None or sma_200 is None else sma_50 > sma_200
        ),
        "raw_score_before_clamp": raw_score,
        "final_score": final_score,
    }

    return TrendMomentumScore(
        score=final_score,
        strengths=strengths,
        weaknesses=weaknesses,
        details=details,
    )


def _apply_momentum_rule(
    raw_score: float,
    momentum_value: float | None,
    label: str,
    strengths: list[str],
    weaknesses: list[str],
) -> float:
    if momentum_value is None:
        return raw_score
    if momentum_value > 0:
        strengths.append(f"positive {label} momentum")
        return raw_score + 5
    if momentum_value < 0:
        weaknesses.append(f"negative {label} momentum")
        return raw_score - 5
    return raw_score


def _validate_inputs(
    latest_close: float,
    sma_50: float | None,
    sma_200: float | None,
    drawdown_252d: float | None,
) -> None:
    if latest_close <= 0:
        raise ValueError("latest_close must be greater than 0")
    if sma_50 is not None and sma_50 <= 0:
        raise ValueError("sma_50 must be greater than 0")
    if sma_200 is not None and sma_200 <= 0:
        raise ValueError("sma_200 must be greater than 0")
    if drawdown_252d is not None and drawdown_252d > 0:
        raise ValueError("drawdown_252d must be less than or equal to 0")
