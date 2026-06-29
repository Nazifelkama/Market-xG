# MXG-021 — Implement Phase 1 End-to-End Sample Pipeline Test

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: System Validation
Type: Test / Integration
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-013 through MXG-020 established the Phase 1 building blocks: fixture validation,
indicators, category scoring, weighted aggregation, and markdown reporting. Before moving
further, the repository needs one clear deterministic integration test that proves those
modules work together on the committed local sample fixture.

## Goal

Create a happy-path Phase 1 end-to-end sample pipeline test using the deterministic OHLCV
fixture only.

## Scope

- Add `tests/integration/test_phase_1_sample_pipeline.py`.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Production pipeline modules or CLI commands.
- Dashboards, charts, or live data fetching.
- Changes to indicator formulas or scoring rules.
- External dependencies such as pandas or numpy.
- Duplicate unit-test edge-case coverage.

## Implementation Instructions

- Load and validate the committed sample fixture.
- Extract close prices and assert the fixture has enough rows for 252-day calculations.
- Calculate SMA, momentum, and drawdown values using existing modules.
- Convert the Trend and Momentum score into a `CategoryScore` named `trend_momentum`.
- Aggregate to Market xG and generate a deterministic markdown report.
- Assert presence and range conditions rather than a brittle exact final score.

## Acceptance Criteria

- `tests/integration/test_phase_1_sample_pipeline.py` exists.
- Test uses deterministic local fixture only.
- Test validates fixture data.
- Test asserts fixture has enough rows for 252-day calculations.
- Test calculates indicators from fixture close prices.
- Test maps momentum values explicitly into `calculate_trend_momentum_score(...)`.
- Test converts `TrendMomentumScore` into `CategoryScore` with name `trend_momentum`.
- Test calculates Market xG aggregate score.
- Test generates markdown report.
- Test verifies report contains key deterministic text.
- Test does not assert an exact final Market xG score.
- Test does not fetch live data.
- Test does not write generated report output to disk.
- Test does not introduce external dependencies.
- Existing scoring rules and indicator formulas are not changed.
- No production source module is created.

## Test Requirements

- Run `pytest tests/integration/test_phase_1_sample_pipeline.py`.
- Run `ruff check tests/integration/test_phase_1_sample_pipeline.py`.
- Run `mypy tests/integration/test_phase_1_sample_pipeline.py`.
- Add only the minimum package files if import issues require them.

## Definition of Done

- Integration test and ticket documentation are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- The first end-to-end test stays intentionally narrow and deterministic so it validates
  module composition without creating a production pipeline abstraction too early.
- The test favors presence and range assertions over exact final scores to reduce brittleness
  while keeping the system behavior meaningful.
