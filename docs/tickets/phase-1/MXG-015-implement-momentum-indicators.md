# MXG-015 — Implement Momentum Indicators

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

MXG-014 added moving average indicators as the first Phase 1 indicator family. Trend and
Momentum scoring also needs return-based momentum signals, so the next step is a small set of
standard-library momentum helpers that work with the validated local OHLCV fixture.

## Goal

Implement basic percentage-return momentum indicators for Phase 1.

## Scope

- Add `src/market_xg/indicators/momentum.py`.
- Add focused unit tests for return calculations, validation behavior, and sample fixture use.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Drawdown indicators.
- Scoring, reports, or backtesting logic.
- Live market data fetching.
- External dependencies such as pandas or numpy.

## Implementation Instructions

- Implement `percentage_return(values, window)` with same-length output and `None` for
  insufficient history.
- Implement `latest_percentage_return(values, window)` for the latest available value.
- Implement `momentum_summary(values)` using the default 1m, 3m, 6m, and 12m windows.
- Raise `ValueError` for invalid window, empty input, or non-positive values.
- Reuse the committed sample fixture close prices for integration-like momentum checks.

## Acceptance Criteria

- `src/market_xg/indicators/momentum.py` exists.
- `percentage_return(values, window)` exists.
- `latest_percentage_return(values, window)` exists.
- `momentum_summary(values)` exists.
- Output length matches input length.
- Insufficient history returns `None`.
- A return is available only when index >= window.
- Returns are percentage-point values, not decimal fractions.
- Latest return returns `None` when insufficient history.
- `momentum_summary` returns exactly `1m`, `3m`, `6m`, `12m`.
- 1m, 3m, 6m, and 12m momentum can be calculated from sample fixture close prices.
- Invalid window raises `ValueError`.
- Empty values raises `ValueError`.
- Zero or negative values raise `ValueError`.
- No drawdown, scoring, reports, live data fetching, or external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_momentum_indicators.py`.
- Run `ruff check src/market_xg/indicators/momentum.py tests/unit/test_momentum_indicators.py`.
- Run `mypy src/market_xg/indicators/momentum.py`.
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

- Default windows use trading-day-style lookbacks so later scoring work can reference stable
  labels and durations.
- The sample fixture provides the only integration-like momentum check until broader pipeline
  tickets exist.
