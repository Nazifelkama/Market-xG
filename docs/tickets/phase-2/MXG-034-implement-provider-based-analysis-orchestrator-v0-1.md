# MXG-034 — Implement Provider-Based Analysis Orchestrator v0.1

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Real Data Readiness
Type: Feature / Analysis Orchestration
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-032 implemented the raw Stooq historical data client and parser. MXG-033 implemented
Stooq historical data normalization into Market xG OHLCV-compatible rows. The next step is an
in-memory orchestration layer that accepts already-fetched provider data and runs the currently
implemented Market xG pipeline through scoring and report generation.

## Goal

Implement a deterministic provider-based analysis orchestrator v0.1 that runs Market xG from a
`StooqHistoricalResponse` without performing live network calls.

## Scope

- Create `src/market_xg/analysis/provider_analysis.py`.
- Create `tests/unit/test_provider_analysis.py`.
- Create this ticket document under `docs/tickets/phase-2/`.
- Implement normalization, validation, indicator calculation, scoring, aggregation, and report
  generation for already-fetched provider data.

## Out of Scope

- Live Stooq network calls.
- Asset search or symbol resolution.
- UI, watchlist storage, scheduled refresh, or persisted analysis status.
- CSV import.
- Engine report file writing.
- Real market data files.
- Scoring, indicator, or aggregation changes.
- External dependency changes.

## Implementation Instructions

- Use Python standard library only.
- Accept only `StooqHistoricalResponse` input.
- Normalize and validate provider data before indicator calculation.
- Require at least 253 rows of history.
- Aggregate exactly the two implemented categories: `trend_momentum` and
  `volume_accumulation`.
- Preserve provider metadata in `ProviderAnalysisResult`, not in normalized OHLCV rows.
- Use the caller-provided `report_date`; do not generate current timestamps internally.

## Acceptance Criteria

- `src/market_xg/analysis/provider_analysis.py` exists.
- `ProviderAnalysisError` exists.
- `ProviderAnalysisResult` dataclass exists.
- `analyze_stooq_historical_response(...)` exists.
- The function accepts `StooqHistoricalResponse` and returns `ProviderAnalysisResult`.
- The function normalizes and validates Stooq rows using the existing normalizer and validator
  path.
- The function requires at least 253 rows.
- The function calculates Trend / Momentum score.
- The function calculates Volume / Accumulation score.
- The function aggregates exactly two implemented categories: `trend_momentum` and
  `volume_accumulation`.
- The function generates a markdown report.
- The function does not generate current timestamps internally.
- The result preserves `provider` and `provider_symbol`.
- The result preserves `asset_name` and `report_date`.
- Details include `row_count`, `latest_close`, `latest_volume`, and key indicator inputs.
- Fewer than 253 rows raises `ProviderAnalysisError`.
- Unit tests do not call live Stooq service.
- Stooq network fetch functions are not called or imported by the orchestrator.
- No persisted analysis status, live fetching, asset search, symbol resolution, UI, watchlist
  storage, scheduled refresh, CSV import, or report file writing is implemented.
- No real market data files are added.
- No scoring rules, indicator formulas, or aggregation weights are changed.
- No external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_provider_analysis.py`.
- Run `ruff check src/market_xg/analysis/provider_analysis.py tests/unit/test_provider_analysis.py`.
- Run `mypy src/market_xg/analysis/provider_analysis.py tests/unit/test_provider_analysis.py`.
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

- This orchestrator accepts already-fetched provider data.
- This orchestrator does not perform live network calls.
- This orchestrator returns a successful result or raises `ProviderAnalysisError`.
- Persisted analysis status is a future product layer, not implemented here.
- Provider metadata is preserved in `ProviderAnalysisResult`, not in normalized OHLCV rows.
- The orchestrator currently aggregates exactly two implemented categories:
  `trend_momentum` and `volume_accumulation`.
- Asset search, symbol resolution, watchlist, scheduling, and UI remain future layers.
