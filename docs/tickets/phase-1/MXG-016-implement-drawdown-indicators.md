# MXG-016 — Implement Drawdown Indicators

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Indicator Engine
Type: Feature / Indicator
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-014 added moving averages and MXG-015 added return-based momentum. Trend and Momentum
scoring also needs drawdown context so the project can measure how far price is below recent
highs.

## Goal

Implement basic rolling-high and drawdown indicators for Phase 1.

## Scope

- Add `src/market_xg/indicators/drawdown.py`.
- Add focused unit tests for rolling-high and drawdown behavior.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Scoring logic.
- Reports or backtesting logic.
- Live market data fetching.
- External dependencies such as pandas or numpy.

## Implementation Instructions

- Implement `rolling_high(values, window)` with same-length output and `None` for insufficient
  history.
- Implement `drawdown_from_rolling_high(values, window)` as percentage drawdown from the
  rolling high.
- Implement `latest_drawdown_from_rolling_high(values, window)` for the latest available
  value.
- Raise `ValueError` for invalid window, empty input, or non-positive values.
- Reuse the committed sample fixture close prices for the integration-like 252-day drawdown
  check.

## Acceptance Criteria

- `src/market_xg/indicators/drawdown.py` exists.
- `ROLLING_DRAWDOWN_WINDOW = 252` exists.
- `rolling_high(values, window)` exists.
- `drawdown_from_rolling_high(values, window)` exists.
- `latest_drawdown_from_rolling_high(values, window)` exists.
- Output length matches input length.
- Insufficient history returns `None`.
- Rolling high is available only when index >= window - 1.
- Rolling high includes current value.
- Drawdown values are percentage-point values, not decimal fractions.
- Drawdown is `0.0` at rolling high.
- Drawdown is negative below rolling high.
- Drawdown values are never positive.
- Window `1` behavior is tested.
- Latest drawdown returns `None` when insufficient history.
- 252-day drawdown can be calculated from sample fixture close prices.
- Invalid window raises `ValueError`.
- Empty values raises `ValueError`.
- Zero or negative values raise `ValueError`.
- No scoring, reports, live data fetching, or external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_drawdown_indicators.py`.
- Run `ruff check src/market_xg/indicators/drawdown.py tests/unit/test_drawdown_indicators.py`.
- Run `mypy src/market_xg/indicators/drawdown.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Indicator code and tests are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- The default rolling drawdown window uses a trading-year-style lookback to align with later
  scoring expectations.
- The sample fixture provides the only integration-like drawdown check until broader pipeline
  tickets exist.
