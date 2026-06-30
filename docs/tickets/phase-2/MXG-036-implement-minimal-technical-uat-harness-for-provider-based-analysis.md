# MXG-036 — Implement Minimal Technical UAT Harness for Provider-Based Analysis

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Real Data Readiness
Type: QA / UAT Harness
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-035 defined the Technical UAT case set from `UAT-001` through `UAT-010`. MXG-034 implemented
provider-based analysis from an already-fetched `StooqHistoricalResponse`. This ticket adds a
minimal deterministic harness that represents those UAT cases without introducing live provider
calls, CLI behavior, file output, or product UI.

## Goal

Create a minimal deterministic Technical UAT harness that can represent and execute `UAT-001`
through `UAT-010` using synthetic provider responses.

## Scope

- Create `src/market_xg/uat/provider_analysis_uat.py`.
- Create `tests/unit/test_provider_analysis_uat.py`.
- Create this ticket document under `docs/tickets/phase-2/`.
- Implement deterministic response builders and a small outcome list for UAT evidence.

## Out of Scope

- Live Stooq calls.
- Stooq fetch-function imports or calls.
- CLI behavior.
- JSON, markdown, or other evidence file output.
- UI, asset search, symbol resolution, watchlist, scheduling, persisted status, or CSV import.
- Real market data files.
- Scoring, indicator, aggregation, or report wording changes.
- External dependency changes.

## Implementation Instructions

- Use Python standard library only.
- Keep the harness small and specific to provider-analysis Technical UAT.
- Use deterministic synthetic `StooqHistoricalResponse` builders.
- Return structured `UATScenarioOutcome` objects instead of printing or writing files.
- Represent `UAT-001` through `UAT-010` as mandatory scenarios.
- Record failed scenario outcomes accurately if current product behavior does not satisfy them.

## Acceptance Criteria

- `provider_analysis_uat.py` exists.
- `UATScenarioOutcome` exists.
- Deterministic builders exist for bullish, weak/downtrend, sideways/mixed, insufficient
  history, and invalid OHLCV responses.
- `run_provider_analysis_uat_scenarios(...)` exists.
- It returns exactly 10 outcomes.
- Scenario IDs are `UAT-001` through `UAT-010`.
- All scenarios are mandatory.
- Happy-path outcomes include observed score and observed categories.
- Expected failure scenarios capture `ProviderAnalysisError` messages as evidence.
- Harness does not print or write files.
- Harness does not call or import Stooq live fetch functions.
- No CLI, export, UI, live fetching, asset search, symbol resolution, watchlist, scheduling,
  persisted status, or CSV import is implemented.
- No real market data files are added.
- No scoring rules, indicator formulas, aggregation weights, or report wording are changed.
- No dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_provider_analysis_uat.py`.
- Run `ruff check src/market_xg/uat/provider_analysis_uat.py tests/unit/test_provider_analysis_uat.py`.
- Run `mypy src/market_xg/uat/provider_analysis_uat.py tests/unit/test_provider_analysis_uat.py`.
- Do not run the full local test suite unless needed.
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

- This is a minimal Technical UAT harness, not a general test framework.
- The harness uses deterministic synthetic provider responses.
- The harness does not perform live provider calls.
- The harness does not write evidence files.
- CLI, JSON export, markdown export, UI, and live provider execution remain out of scope.
- `UAT-001` through `UAT-010` are represented as mandatory.
