"""Phase 1 moving average indicators."""

from __future__ import annotations


def simple_moving_average(values: list[float], window: int) -> list[float | None]:
    """Return a same-length list of simple moving average values."""
    _validate_inputs(values, window)

    result: list[float | None] = []
    rolling_sum = 0.0

    for index, value in enumerate(values):
        rolling_sum += value

        if index >= window:
            rolling_sum -= values[index - window]

        if index < window - 1:
            result.append(None)
        else:
            result.append(rolling_sum / window)

    return result


def latest_simple_moving_average(values: list[float], window: int) -> float | None:
    """Return the most recent simple moving average value."""
    averages = simple_moving_average(values, window)
    return averages[-1]


def _validate_inputs(values: list[float], window: int) -> None:
    if window <= 0:
        raise ValueError("window must be greater than 0")
    if not values:
        raise ValueError("values must not be empty")
