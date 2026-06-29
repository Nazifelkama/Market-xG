"""Phase 1 drawdown indicators."""

from __future__ import annotations


ROLLING_DRAWDOWN_WINDOW = 252


def rolling_high(values: list[float], window: int) -> list[float | None]:
    """Return same-length rolling highs for the given trailing window."""
    _validate_inputs(values, window)

    result: list[float | None] = []

    for index in range(len(values)):
        if index < window - 1:
            result.append(None)
            continue

        result.append(max(values[index - window + 1 : index + 1]))

    return result


def drawdown_from_rolling_high(values: list[float], window: int) -> list[float | None]:
    """Return same-length percentage drawdown values from the rolling high."""
    highs = rolling_high(values, window)
    result: list[float | None] = []

    for value, high in zip(values, highs):
        if high is None:
            result.append(None)
        else:
            result.append(((value / high) - 1.0) * 100.0)

    return result


def latest_drawdown_from_rolling_high(values: list[float], window: int) -> float | None:
    """Return the latest available drawdown value."""
    drawdowns = drawdown_from_rolling_high(values, window)
    return drawdowns[-1]


def _validate_inputs(values: list[float], window: int) -> None:
    if window <= 0:
        raise ValueError("window must be greater than 0")
    if not values:
        raise ValueError("values must not be empty")
    if any(value <= 0 for value in values):
        raise ValueError("values must be greater than 0")
