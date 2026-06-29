# MXG-024 — Implement Volume Indicators

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Volume / Accumulation
Type: Feature / Indicator
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

Phase 1 established the tested Market xG skeleton with validation, indicators, scoring,
aggregation, reporting, and a deterministic integration test. Phase 2 starts by adding the
next independent market-quality foundation: volume indicator utilities for future Volume /
Accumulation work.

## Goal

Implement deterministic volume indicator utilities using only the Python standard library.

## Scope

- Add `src/market_xg/indicators/volume.py`.
- Add focused unit tests for volume averages, ratios, and up/down volume summaries.
- Add this ticket file under `docs/tickets/phase-2/`.

## Out of Scope

- Volume / Accumulation scoring.
- Market xG aggregation weight changes.
- Phase 1 end-to-end pipeline changes.
- Changes to existing trend, momentum, drawdown, or moving-average indicators.
- Live data fetching or external dependencies.

## Implementation Instructions

- Implement `average_volume(...)` and `latest_average_volume(...)` with trailing-window
  behavior and `None` for insufficient history.
- Implement `volume_ratio(...)` with safe `None` handling and division-by-zero protection.
- Implement `up_down_volume_summary(...)` for the latest trailing window only.
- Reject invalid numeric inputs explicitly, including `bool` values.
- Keep the functions deterministic and free of scoring labels.

## Acceptance Criteria

- `src/market_xg/indicators/volume.py` exists.
- `average_volume(...)` exists.
- `latest_average_volume(...)` exists.
- `volume_ratio(...)` exists.
- `up_down_volume_summary(...)` exists.
- Volume indicators are deterministic.
- `average_volume` supports `window=1`.
- `up_down_volume_summary` requires `window >= 2`.
- Invalid inputs raise `ValueError` with meaningful messages.
- `bool` values are rejected as numeric inputs.
- Insufficient history returns `None` values instead of crashing.
- Existing fixture volume data is covered by tests.
- No accumulation or distribution labels are inferred.
- No Volume / Accumulation score is implemented.
- Market xG aggregation weights are not modified.
- Phase 1 end-to-end pipeline is not modified.
- Existing indicator formulas and scoring rules are not changed.
- No live data fetching or external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_volume_indicators.py`.
- Run `ruff check src/market_xg/indicators/volume.py tests/unit/test_volume_indicators.py`.
- Run `mypy src/market_xg/indicators/volume.py tests/unit/test_volume_indicators.py`.
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

- Phase 2 starts with reusable volume primitives before any Volume / Accumulation scoring is
  introduced.
- Volume utilities stay descriptive and deterministic rather than inferring higher-level market
  labels.
