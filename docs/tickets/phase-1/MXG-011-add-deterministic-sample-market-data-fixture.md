# MXG-011 — Add Deterministic Sample Market Data Fixture

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Data Foundation
Type: Test Data
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

Phase 1 needs a stable local OHLCV fixture before validation, indicators, or scoring work
begins. The repository already defines the market data contract, so this ticket adds a
deterministic sample file and supporting documentation that future implementation tickets can
reuse.

## Goal

Create a committed local sample S&P 500-style OHLCV fixture plus documentation and tests that
prove the fixture follows the documented Phase 1 contract.

## Scope

- Add `tests/fixtures/market_data/sample_sp500_ohlcv.csv`.
- Add `docs/architecture/sample_market_data.md`.
- Add `tests/unit/test_sample_market_data_fixture.py`.
- Add this ticket document under `docs/tickets/phase-1/`.
- Update references in existing docs where useful.

## Out of Scope

- Validation code for market data.
- Sample data loading utilities.
- Indicator, scoring, reporting, or backtesting logic.
- Live market data fetching.
- Extra columns such as symbol, currency, adjusted close, or source metadata.

## Implementation Instructions

- Commit a deterministic CSV fixture with only the Phase 1 OHLCV columns.
- Keep the rows sorted ascending by date and free of missing values.
- Document how the fixture relates to the market data contract.
- Add focused tests that verify the file shape, numeric rules, and document links.
- Use only relevant local checks before review.

## Acceptance Criteria

- `docs/architecture/sample_market_data.md` exists.
- `tests/fixtures/market_data/sample_sp500_ohlcv.csv` exists.
- The fixture contains the required OHLCV columns only.
- The fixture contains at least 260 rows.
- Dates are parseable, unique, and sorted ascending.
- OHLC values are numeric and positive.
- Volume is numeric and non-negative.
- `high` is greater than or equal to `low`.
- `open` and `close` are within the daily low-high range.
- `docs/tickets/phase-1/MXG-011-add-deterministic-sample-market-data-fixture.md` exists.
- No validation code is implemented.
- No market logic is implemented.

## Test Requirements

- Run `pytest tests/unit/test_sample_market_data_fixture.py`.
- Run `ruff check tests/unit/test_sample_market_data_fixture.py`.
- Do not run unrelated checks unless the scope changes.

## Definition of Done

- The fixture, docs, and tests are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global quality expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Phase 1 uses deterministic local sample data before any live data integration.
- The fixture keeps only the contract columns to avoid premature schema expansion.
