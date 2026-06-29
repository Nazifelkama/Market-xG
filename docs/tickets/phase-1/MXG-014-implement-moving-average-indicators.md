# MXG-014 — Implement Moving Average Indicators

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

MXG-013 introduced Phase 1 market data validation, which clears the path for the first
indicator work. Moving averages come first because upcoming trend and momentum tickets will
depend on them as basic building blocks.

## Goal

Implement simple moving average helpers for Phase 1 using only the Python standard library.

## Scope

- Add `src/market_xg/indicators/moving_average.py`.
- Add focused unit tests for SMA behavior and sample fixture usage.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Momentum indicators.
- Drawdown indicators.
- Scoring, reports, or backtesting logic.
- Live market data fetching.
- External dependencies such as pandas or numpy.

## Implementation Instructions

- Implement `simple_moving_average(values, window)` with same-length output.
- Return `None` where there is insufficient history for the window.
- Implement `latest_simple_moving_average(values, window)` for the latest available value.
- Raise `ValueError` for invalid window or empty input values.
- Reuse the committed sample fixture close prices for integration-like SMA checks.

## Acceptance Criteria

- `src/market_xg/indicators/moving_average.py` exists.
- `simple_moving_average(values, window)` exists.
- `latest_simple_moving_average(values, window)` exists.
- SMA output length matches input length.
- Insufficient history returns `None`.
- Latest SMA returns `None` when insufficient history.
- 50-day SMA can be calculated from sample fixture close prices.
- 200-day SMA can be calculated from sample fixture close prices.
- Invalid window raises `ValueError`.
- Empty values raises `ValueError`.
- No momentum, drawdown, scoring, reports, live data fetching, or external dependencies are
  added.

## Test Requirements

- Run `pytest tests/unit/test_moving_average_indicators.py`.
- Run `ruff check src/market_xg/indicators/moving_average.py tests/unit/test_moving_average_indicators.py`.
- Run `mypy src/market_xg/indicators/moving_average.py`.
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

- The first indicator implementation stays intentionally small so later tickets can build on a
  stable SMA baseline.
- The sample fixture provides the only integration-like check here until broader pipeline
  tickets exist.
