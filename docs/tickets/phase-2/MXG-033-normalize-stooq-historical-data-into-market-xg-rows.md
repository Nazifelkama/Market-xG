# MXG-033 — Normalize Stooq Historical Data into Market xG Rows

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Real Data Readiness
Type: Feature / Data Provider
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-032 implemented the raw Stooq historical data client and intentionally stopped at raw fetch
and provider-specific parsing. The next step is to bridge parsed provider rows into the existing
Market xG OHLCV contract and reuse the existing semantic validator.

## Goal

Normalize parsed Stooq historical data into Market xG OHLCV-compatible rows and validate them
using the existing market data validator.

## Scope

- Create `src/market_xg/data_providers/stooq_normalizer.py`.
- Create `tests/unit/test_stooq_normalizer.py`.
- Create this ticket document under `docs/tickets/phase-2/`.
- Implement pure OHLCV normalization plus validator handoff.

## Out of Scope

- Live network calls or Stooq fetching.
- Asset search or symbol resolution.
- UI, watchlist storage, scheduled refresh, or CSV import.
- Engine execution or report generation from Stooq data.
- Provider metadata on normalized rows.
- `adjusted_close`.
- Real market data files.
- Scoring, indicator, or aggregation changes.
- External dependency changes.

## Implementation Instructions

- Use Python standard library only.
- Accept only `StooqHistoricalResponse` inputs.
- Normalize rows into pure OHLCV dictionaries with string values.
- Strip whitespace during normalization.
- Reuse `validate_ohlcv_rows(...)` as the semantic validation boundary when `validate=True`.
- Keep provider metadata out of normalized OHLCV rows in this ticket.

## Acceptance Criteria

- `src/market_xg/data_providers/stooq_normalizer.py` exists.
- `StooqNormalizationError` exists.
- `normalize_stooq_historical_response(...)` exists.
- `normalize_and_validate_stooq_historical_response(...)` exists.
- Wrong response type raises `TypeError`.
- Stooq rows normalize into Market xG OHLCV-compatible rows.
- Normalized rows contain exactly `date`, `open`, `high`, `low`, `close`, `volume`.
- Values are preserved as stripped strings.
- Numeric conversion is not performed in the normalizer.
- Provider metadata and `adjusted_close` are not added in this ticket.
- Existing `validate_ohlcv_rows(...)` is used when `validate=True`.
- Validation errors are wrapped as `StooqNormalizationError`.
- Unit tests do not call live Stooq service.
- No live fetching, asset search, symbol resolution, UI, watchlist storage, scheduled refresh,
  CSV import, engine pipeline execution, or report generation is implemented.
- No real market data files are added.
- No scoring rules, indicator formulas, or aggregation weights are changed.
- No external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_stooq_normalizer.py`.
- Run `ruff check src/market_xg/data_providers/stooq_normalizer.py tests/unit/test_stooq_normalizer.py`.
- Run `mypy src/market_xg/data_providers/stooq_normalizer.py tests/unit/test_stooq_normalizer.py`.
- Rely on full CI after push or PR for broader repository checks.

## Definition of Done

- Implementation stays within ticket scope.
- Relevant unit, lint, and type checks pass.
- Acceptance criteria are satisfied.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Stooq normalization returns pure OHLCV rows only.
- Provider metadata is intentionally kept out of normalized OHLCV rows in this ticket.
- Future orchestration and result layers must preserve provider metadata separately.
- Existing `validate_ohlcv_rows(...)` remains the semantic validation boundary.
