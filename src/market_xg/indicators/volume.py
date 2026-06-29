"""Phase 2 volume indicator utilities."""

from __future__ import annotations


def average_volume(volumes: list[float], window: int) -> list[float | None]:
    """Return same-length trailing average volume values."""
    _validate_window(window, minimum=1)
    _validate_numeric_sequence(volumes, name="volumes", allow_zero=True)

    result: list[float | None] = []
    rolling_sum = 0.0

    for index, volume in enumerate(volumes):
        rolling_sum += float(volume)

        if index >= window:
            rolling_sum -= float(volumes[index - window])

        if index < window - 1:
            result.append(None)
        else:
            result.append(rolling_sum / window)

    return result


def latest_average_volume(volumes: list[float], window: int) -> float | None:
    """Return the latest available average volume."""
    averages = average_volume(volumes, window)
    return averages[-1]


def volume_ratio(latest_volume: float, average_volume_value: float | None) -> float | None:
    """Return latest volume divided by average volume when available."""
    _validate_numeric_value(latest_volume, name="latest_volume", allow_zero=True)

    if average_volume_value is None:
        return None

    _validate_numeric_value(
        average_volume_value,
        name="average_volume_value",
        allow_zero=True,
    )
    if float(average_volume_value) == 0.0:
        return None

    return float(latest_volume) / float(average_volume_value)


def up_down_volume_summary(
    close_prices: list[float],
    volumes: list[float],
    window: int,
) -> dict[str, float | None]:
    """Summarize up, down, and flat volume over the latest trailing window."""
    _validate_window(window, minimum=2)
    _validate_numeric_sequence(close_prices, name="close_prices", allow_zero=False)
    _validate_numeric_sequence(volumes, name="volumes", allow_zero=True)

    if len(close_prices) != len(volumes):
        raise ValueError("close_prices and volumes must have the same length")
    if len(close_prices) < window:
        return {
            "up_volume": None,
            "down_volume": None,
            "flat_volume": None,
            "up_down_volume_ratio": None,
        }

    selected_closes = [float(value) for value in close_prices[-window:]]
    selected_volumes = [float(value) for value in volumes[-window:]]

    up_volume = 0.0
    down_volume = 0.0
    flat_volume = 0.0

    for index in range(1, window):
        current_close = selected_closes[index]
        previous_close = selected_closes[index - 1]
        current_volume = selected_volumes[index]

        if current_close > previous_close:
            up_volume += current_volume
        elif current_close < previous_close:
            down_volume += current_volume
        else:
            flat_volume += current_volume

    return {
        "up_volume": up_volume,
        "down_volume": down_volume,
        "flat_volume": flat_volume,
        "up_down_volume_ratio": None if down_volume == 0 else up_volume / down_volume,
    }


def _validate_window(window: int, minimum: int) -> None:
    if window < minimum:
        if minimum == 1:
            raise ValueError("window must be greater than 0")
        raise ValueError(f"window must be greater than or equal to {minimum}")


def _validate_numeric_sequence(
    values: list[float],
    *,
    name: str,
    allow_zero: bool,
) -> None:
    if not values:
        raise ValueError(f"{name} must not be empty")

    for value in values:
        _validate_numeric_value(value, name=name[:-1] if name.endswith("s") else name, allow_zero=allow_zero)


def _validate_numeric_value(value: float, *, name: str, allow_zero: bool) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} values must be int or float")
    numeric_value = float(value)
    if allow_zero:
        if numeric_value < 0:
            raise ValueError(f"{name} values must be greater than or equal to 0")
    else:
        if numeric_value <= 0:
            raise ValueError(f"{name} values must be greater than 0")
