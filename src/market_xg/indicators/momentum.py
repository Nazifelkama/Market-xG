"""Phase 1 momentum indicators."""

from __future__ import annotations


DEFAULT_MOMENTUM_WINDOWS: dict[str, int] = {
    "1m": 21,
    "3m": 63,
    "6m": 126,
    "12m": 252,
}


def percentage_return(values: list[float], window: int) -> list[float | None]:
    """Return same-length percentage returns for the given lookback window."""
    _validate_inputs(values, window)

    result: list[float | None] = []

    for index, value in enumerate(values):
        if index < window:
            result.append(None)
            continue

        prior_value = values[index - window]
        result.append(((value / prior_value) - 1.0) * 100.0)

    return result


def latest_percentage_return(values: list[float], window: int) -> float | None:
    """Return the latest available percentage return."""
    returns = percentage_return(values, window)
    return returns[-1]


def momentum_summary(values: list[float]) -> dict[str, float | None]:
    """Return the latest 1m, 3m, 6m, and 12m momentum values."""
    return {
        label: latest_percentage_return(values, window)
        for label, window in DEFAULT_MOMENTUM_WINDOWS.items()
    }


def _validate_inputs(values: list[float], window: int) -> None:
    if window <= 0:
        raise ValueError("window must be greater than 0")
    if not values:
        raise ValueError("values must not be empty")
    if any(value <= 0 for value in values):
        raise ValueError("values must be greater than 0")
