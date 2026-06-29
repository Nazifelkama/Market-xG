# MXG-013 — Implement Market Data Validation

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Data Foundation
Type: Data / Validation
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-010 defined the OHLCV market data contract, MXG-011 added a deterministic sample fixture,
and MXG-012 documented the limits of that fixture. Before indicators or scoring can use market
data, the repository needs a standard-library validator that enforces the Phase 1 contract.

## Goal

Implement a simple OHLCV validator that reads CSV rows and raises clear validation errors when
the Phase 1 market data contract is violated.

## Scope

- Add `src/market_xg/data_providers/market_data_validator.py`.
- Add focused unit tests for successful and failing validation cases.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Indicators, scoring, reports, or backtesting logic.
- Live market data fetching.
- External dependencies such as pandas or numpy.
- End-to-end Phase 1 system testing beyond fixture validation.

## Implementation Instructions

- Read CSV files with `csv.DictReader` and `pathlib.Path`.
- Validate rows using `datetime.date.fromisoformat` and `decimal.Decimal`.
- Raise `ValueError` with useful keywords for each rule failure.
- Keep the validator reusable for both CSV-loaded rows and rows created directly in tests.

## Acceptance Criteria

- `src/market_xg/data_providers/market_data_validator.py` exists.
- `load_csv_rows(path)` exists.
- `validate_ohlcv_rows(rows)` exists.
- The committed sample fixture passes validation.
- Empty rows fail.
- Missing required columns fail.
- Missing or whitespace-only values fail.
- Invalid dates fail.
- Duplicate dates fail.
- Unsorted dates fail.
- Non-numeric OHLC values fail.
- Non-positive OHLC values fail.
- Non-numeric volume fails.
- Negative volume fails.
- `high` lower than `low` fails.
- `open` outside low-high fails.
- `close` outside low-high fails.
- Tests cover all validation rules.
- No indicators, scoring, reports, live data fetching, or external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_market_data_validator.py`.
- Run `ruff check src/market_xg/data_providers/market_data_validator.py tests/unit/test_market_data_validator.py`.
- Run `mypy src/market_xg/data_providers/market_data_validator.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Validator code and tests are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Validation stays in the standard library to keep Phase 1 lightweight and deterministic.
- The sample fixture is used as the only integration-like check until later pipeline tickets
  introduce broader system behavior.
