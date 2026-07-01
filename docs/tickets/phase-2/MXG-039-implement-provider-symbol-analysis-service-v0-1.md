# MXG-039 — Implement Provider-Symbol Analysis Service v0.1

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Real Data Readiness
Type: Feature / Provider Execution
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-07-01
Updated: 2026-07-01

## Context

MXG-032 implemented the Stooq historical data client. MXG-033 implemented Stooq normalization.
MXG-034 implemented provider-based analysis from an already-fetched `StooqHistoricalResponse`.
MXG-037 recorded Technical UAT as passed. MXG-038 defined the provider-symbol live execution
contract.

The next implementation step is a small service that accepts a direct provider symbol and runs the
existing provider-analysis path.

## Goal

Implement provider-symbol analysis service v0.1 that accepts a direct provider symbol, fetches
Stooq historical data, runs Market xG analysis, and returns either a success result or failure
result.

## Scope

- Create `src/market_xg/services/provider_symbol_analysis.py`.
- Create `tests/unit/test_provider_symbol_analysis.py`.
- Create this ticket document under `docs/tickets/phase-2/`.
- Use only the Python standard library and existing Market xG modules.

## Out of Scope

- CLI.
- UI.
- Asset search.
- Symbol resolution.
- Watchlist storage.
- Scheduling.
- Persisted status.
- CSV import.
- Real market data files.
- Scoring rules, indicator formulas, Market xG aggregation weights, or report wording changes.
- Dependency changes.

## Implementation Instructions

- Add `ProviderSymbolAnalysisFailure` as a frozen dataclass.
- Validate `ProviderSymbolAnalysisFailure` fields as non-empty strings.
- Add `ProviderSymbolAnalysisOutcome` as a union of `ProviderAnalysisResult` and
  `ProviderSymbolAnalysisFailure`.
- Add `analyze_provider_symbol(...)`.
- Validate request fields and `timeout_seconds`.
- Return `invalid_request` failure for invalid inputs.
- Support only `provider="stooq"` in v0.1, using case-insensitive provider matching.
- Fetch Stooq data with `fetch_stooq_historical_data(provider_symbol, interval="d",
  timeout_seconds=timeout_seconds)`.
- Run `analyze_stooq_historical_response(...)` on fetched data.
- Return `ProviderAnalysisResult` on success.
- Map Stooq and provider-analysis exceptions to documented failure categories.
- Do not print, write files, or generate timestamps internally.

## Acceptance Criteria

- `provider_symbol_analysis.py` exists.
- `ProviderSymbolAnalysisFailure` exists.
- `analyze_provider_symbol(...)` exists.
- Stooq success path fetches provider data and returns `ProviderAnalysisResult`.
- Failure path returns `ProviderSymbolAnalysisFailure`.
- Unsupported provider maps to `unsupported_provider`.
- Invalid input maps to `invalid_request`.
- `StooqNetworkError` maps to `provider_network_error`.
- `StooqParseError` maps to `provider_parse_error`.
- Other `StooqClientError` maps to `provider_error`.
- `ProviderAnalysisError` maps to `analysis_error`.
- Unexpected errors map to `unknown_error`.
- Tests do not call live Stooq.
- No CLI, UI, asset search, symbol resolution, watchlist, scheduling, persisted status, or CSV
  import is implemented.
- No real market data files are added.
- No scoring, indicator, aggregation, or report wording changes are made.
- No dependencies are added.

## Test Requirements

- Unit tests cover successful Stooq execution.
- Unit tests verify Stooq fetch arguments.
- Unit tests verify case-insensitive Stooq provider matching.
- Unit tests verify success result metadata preservation.
- Unit tests verify invalid request failures.
- Unit tests verify unsupported provider failures.
- Unit tests verify Stooq network, parse, and client error mappings.
- Unit tests verify provider-analysis error mapping.
- Unit tests verify unexpected error mapping.
- Unit tests mock Stooq fetch and must not call live Stooq.

## Definition of Done

- Provider-symbol analysis service is implemented within ticket scope.
- Required unit tests pass.
- Ruff passes for changed Python files.
- Mypy passes for changed Python files.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- This is the first direct provider-symbol analysis service.
- v0.1 supports Stooq only.
- Direct provider-symbol input is an interim step, not final product search.
- Unit tests must mock provider fetch and must not depend on live Stooq.
- Manual live symbol smoke check remains a separate follow-up.
