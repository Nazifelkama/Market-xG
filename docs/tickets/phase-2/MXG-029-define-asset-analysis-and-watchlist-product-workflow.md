# MXG-029 — Define Asset Analysis and Watchlist Product Workflow

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Product Workflow
Type: Product / Workflow Contract
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

The Market xG engine currently has a tested calculation core, but the product workflow around
asset search, asset selection, watchlist behavior, and result display is not yet defined. Before
building UI, provider integrations, or orchestration layers, the product workflow contract needs
to be documented clearly.

## Goal

Define the user-facing workflow contract for one-time asset analysis and future watchlist
tracking while keeping the current ticket strictly documentation-only.

## Scope

- Create `docs/product/asset_analysis_workflow.md`.
- Document the Analyze now workflow.
- Document the Track asset workflow.
- Define asset identity requirements, analysis statuses, result expectations, and watchlist
  contract concepts.

## Out of Scope

- Production source-code changes.
- Test changes.
- UI implementation.
- Asset search implementation.
- Symbol resolution implementation.
- Watchlist storage implementation.
- Background jobs or scheduled refresh implementation.
- CSV adapter or live data-provider implementation.
- Scoring, indicator, or aggregation changes.
- External dependency changes.

## Product Requirements

- Define Market xG as probabilistic decision support rather than guaranteed prediction.
- Document Analyze now and Track asset as the two core user actions.
- Require explicit asset identity through symbol, display name, exchange, currency, asset type,
  and source when known.
- Define the analysis status model and the high-level product flow around the existing engine.
- Define the future watchlist item concept and completed-result display requirements.
- Document safe prediction wording and future indicator-quality expectations.
- State explicit non-goals for UI, search, live data, storage, refresh, and backtesting.

## Acceptance Criteria

- `docs/product/asset_analysis_workflow.md` exists.
- The document defines Analyze now and Track asset workflows.
- The document explains that users search for assets and select a specific symbol, exchange, and
  currency.
- The document includes examples for AAPL, VUSA.AS, ASML.AS, and NVDA.
- The document explains why asset identity matters, especially for `VUSA.AS / Euronext
  Amsterdam / EUR`.
- The document defines the analysis status model.
- The document defines the high-level analysis flow.
- The document defines the future watchlist item concept.
- The document defines result display requirements.
- The document documents safe prediction wording.
- The document explains that indicator quality, independence, and calibration drive Market xG
  usefulness.
- The document clearly states no UI, asset search, live data fetching, watchlist storage,
  scheduled refresh, or backtesting is implemented yet.
- No production source code is changed.
- No tests are changed.
- No data providers, CSV adapters, UI, watchlist storage, jobs, or scheduled refresh are
  implemented.
- No scoring rules, indicator formulas, or aggregation weights are changed.
- No external dependencies are added.

## Test / Check Requirements

- Run `git diff --check`.
- If markdown linting is configured later, run the relevant markdown-lint command.
- Rely on full CI after push or PR for broader repository checks.

## Definition of Done

- Documentation changes are complete within ticket scope.
- Acceptance criteria are satisfied.
- Required local documentation checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- This ticket defines the product workflow around the existing engine without claiming that the
  surrounding product layers already exist.
- Asset identity is treated as a first-class contract to avoid silently analyzing the wrong
  listing or currency.
