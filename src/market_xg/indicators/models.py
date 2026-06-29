"""Phase 1 indicator output models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IndicatorResult:
    """A lightweight Phase 1 indicator output contract."""

    name: str
    value: float | None
    available: bool
    reason: str | None = None

    def __post_init__(self) -> None:
        if self.name.strip() == "":
            raise ValueError("name must not be empty")
        if self.available and self.value is None:
            raise ValueError("available indicator must have a value")
        if self.available and self.reason is not None:
            raise ValueError("available indicator must not have a reason")
        if not self.available and self.value is not None:
            raise ValueError("unavailable indicator must not have a value")
        if not self.available and (self.reason is None or self.reason.strip() == ""):
            raise ValueError("unavailable indicator must have a non-empty reason")

    def to_dict(self) -> dict[str, object]:
        """Return a plain dictionary representation."""
        return {
            "name": self.name,
            "value": self.value,
            "available": self.available,
            "reason": self.reason,
        }


def available_indicator(name: str, value: float) -> IndicatorResult:
    """Create an available indicator result."""
    return IndicatorResult(name=name, value=value, available=True)


def unavailable_indicator(name: str, reason: str) -> IndicatorResult:
    """Create an unavailable indicator result."""
    return IndicatorResult(name=name, value=None, available=False, reason=reason)
