# MXG-032 — Implement Stooq Historical Data Client

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

MXG-031 defined the real market data provider strategy and established Stooq as the first real
provider candidate. The next implementation step is a small client boundary that can build
historical download URLs, fetch raw CSV text, and parse provider-specific rows without yet
normalizing them into Market xG OHLCV rows.

## Goal

Implement a small Stooq historical data client that handles URL construction, raw CSV fetching,
and provider-specific CSV parsing for daily historical data.

## Scope

- Create `src/market_xg/data_providers/stooq_client.py`.
- Create `tests/unit/test_stooq_client.py`.
- Create this ticket document under `docs/tickets/phase-2/`.
- Implement raw fetch, parse, and fetch-plus-parse convenience boundaries only.

## Out of Scope

- Market xG OHLCV normalization.
- OHLCV semantic validation.
- Engine execution on Stooq data.
- Asset search or symbol resolution.
- UI, watchlist storage, scheduled refresh, or CSV import.
- Real market data files.
- Scoring, indicator, or aggregation changes.
- External dependency changes.

## Implementation Instructions

- Use Python standard library only.
- Support only daily interval `d` in v0.1.
- Keep provider parsing strict for expected Stooq historical CSV headers.
- Preserve raw string row values in the parser response.
- Keep raw fetch, raw parse, and convenience orchestration as separate functions.
- Ensure unit tests use mocks or monkeypatching and never call live Stooq.

## Acceptance Criteria

- `src/market_xg/data_providers/stooq_client.py` exists.
- `StooqHistoricalRow` dataclass exists.
- `StooqHistoricalResponse` dataclass exists.
- `StooqClientError`, `StooqNetworkError`, and `StooqParseError` exist.
- Only daily interval `d` is supported in v0.1.
- Unsupported intervals raise `ValueError`.
- `build_stooq_historical_url(...)` exists and does not perform network calls.
- `build_stooq_historical_url(...)` lowercases `provider_symbol` only in the URL query.
- `parse_stooq_historical_csv(...)` exists and does not perform network calls.
- `fetch_stooq_historical_csv(...)` exists and performs only raw CSV fetch.
- `fetch_stooq_historical_data(...)` exists as a fetch-plus-parse convenience function.
- The parser preserves raw string values.
- The parser preserves the original `provider_symbol` in `StooqHistoricalResponse`.
- The parser does not normalize into Market xG OHLCV rows.
- The parser does not perform numeric conversion or OHLCV semantic validation.
- The fetcher does not require a specific `Content-Type` in v0.1.
- Unit tests do not call the live Stooq service.
- No asset search, symbol resolution, UI, watchlist storage, scheduled refresh, CSV import, or
  live-provider-dependent CI is implemented.
- No real market data files are added.
- No scoring rules, indicator formulas, or aggregation weights are changed.
- No external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_stooq_client.py`.
- Run `ruff check src/market_xg/data_providers/stooq_client.py tests/unit/test_stooq_client.py`.
- Run `mypy src/market_xg/data_providers/stooq_client.py tests/unit/test_stooq_client.py`.
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

- The first provider boundary is intentionally narrow: URL build, raw fetch, raw parse, and a
  convenience wrapper.
- Normalization and validation remain separate follow-on work so provider behavior can be tested
  independently.
