# MXG-030 — Define Asset Identity and Symbol Resolution Contract

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Product Workflow
Type: Product / Asset Contract
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-029 defined the asset analysis and watchlist workflow, but that workflow depends on
resolving a user query into a precise asset identity before analysis or tracking can proceed.
This is especially important for assets with multiple listings, exchanges, or currencies such
as VUSA.

## Goal

Define the asset identity and symbol resolution contract so Market xG does not silently analyze
the wrong listing, exchange, or currency.

## Scope

- Create `docs/product/asset_identity_and_symbol_resolution.md`.
- Update `docs/product/asset_analysis_workflow.md` with a short reference to asset identity.
- Define the intended asset identity model, ambiguity rules, example identities, and failure
  states.

## Out of Scope

- Production source-code changes.
- Test changes.
- Asset search implementation.
- Symbol resolution logic.
- Provider lookup.
- UI implementation.
- Watchlist storage.
- CSV import adapters.
- Live data fetching.
- Hard-coded asset registries or supported-symbol lists.
- Scoring, indicator, or aggregation changes.
- External dependency changes.

## Product Requirements

- Define asset identity as the canonical representation of a selected asset.
- Define symbol resolution as the process that converts a search query into candidate asset
  identities.
- Require explicit identity fields including symbol, display name, exchange, currency, and asset
  type.
- Document strongly recommended and optional fields for provider-specific and market metadata.
- Explain dynamic future search behavior and ambiguity handling.
- Include non-binding examples for AAPL, NVDA, ASML.AS, and VUSA.AS.
- Document the intended VUSA Amsterdam identity and the no-silent-substitution rule.
- Document currency handling, source-symbol handling, and failure or user-attention scenarios.

## Acceptance Criteria

- `docs/product/asset_identity_and_symbol_resolution.md` exists.
- The document defines asset identity and symbol resolution.
- The document defines required, strongly recommended, and optional asset identity fields.
- The document explains search-result behavior and ambiguity handling.
- The document states search results are expected to be dynamic in future implementation, not
  hard-coded.
- The document includes non-binding examples for `AAPL`, `NVDA`, `ASML.AS`, and `VUSA.AS`.
- The document states example assets are documentation examples only.
- The document does not define a hard-coded asset registry or supported-symbol list.
- The document does not imply Market xG only supports `AAPL`, `NVDA`, `ASML.AS`, or `VUSA.AS`.
- The document explicitly states the intended VUSA identity is `VUSA.AS / Euronext Amsterdam /
  EUR`.
- The document states VUSA must not be silently treated as `SPY`, `SPX`, `VOO`, or a
  London/GBP listing.
- The document states currency is part of asset identity.
- The document states no FX conversion is implemented yet.
- The document explains `source_symbol` and provider-specific symbol formats.
- The document defines failure and `needs_user_attention` scenarios.
- `docs/product/asset_analysis_workflow.md` references asset identity before data loading.
- No production source code is changed.
- No tests are changed.
- No asset search, symbol resolution, provider integration, CSV adapter, live data fetching, UI,
  watchlist storage, or FX conversion is implemented.
- No hard-coded asset registry or supported-symbol list is implemented.
- No real market data files are added.
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

- This ticket keeps the product contract explicit while avoiding implementation claims for
  search, provider lookup, or storage.
- Asset identity is treated as a first-class contract to prevent silent listing, exchange, or
  currency mistakes.
