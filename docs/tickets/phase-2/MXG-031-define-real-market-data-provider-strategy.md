# MXG-031 — Define Real Market Data Provider Strategy

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Real Data Readiness
Type: Product / Data Provider Strategy
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-029 defined the asset analysis and watchlist workflow. MXG-030 defined the asset identity
and symbol resolution contract. The next product and architecture question is how selected
assets should move through a real provider path into normalized Market xG data without falling
back to manual CSV as the current product direction.

## Goal

Define the real market data provider strategy before implementing provider code.

## Scope

- Create `docs/product/real_market_data_provider_strategy.md`.
- Update `docs/product/asset_analysis_workflow.md` with a short provider-strategy reference.
- Update `docs/product/asset_identity_and_symbol_resolution.md` with a short provider-mapping
  reference.
- Define provider direction, provider-symbol strategy, normalization targets, and reliability
  expectations.

## Out of Scope

- Production source-code changes.
- Test changes.
- Provider implementation or a Stooq client.
- Asset search implementation.
- Symbol resolution logic.
- UI implementation.
- Watchlist storage.
- Scheduled refresh.
- CSV import.
- Live data fetching.
- API keys, secrets, or real market data files.
- Scoring, indicator, or aggregation changes.
- External dependency changes.

## Product / Architecture Requirements

- Define a provider-based product flow from asset identity to Market xG result.
- Document Stooq as the first real provider candidate without making it exclusive forever.
- Document that the product must not be hard-coded to VUSA.
- State that manual CSV import is out of current scope.
- Distinguish provider-symbol MVP behavior from the final user-friendly search experience.
- Document non-binding provider-symbol candidates for Apple, Nvidia, ASML, VUSA, Tesla, and an
  S&P 500 or another supported index or instrument example.
- Require provider symbols to be verified during implementation.
- Distinguish product-level asset identity from provider-level provider symbols.
- Define normalized OHLCV targets, recommended metadata, currency rules, reliability behavior,
  and CI testing strategy.

## Acceptance Criteria

- `docs/product/real_market_data_provider_strategy.md` exists.
- The document defines the product flow from user search to provider data to Market xG result.
- The document states Stooq is the first real market data provider candidate.
- The document states Stooq is not a permanent exclusive provider.
- The document states the product must not be hard-coded to VUSA.
- The document states manual CSV import is out of current scope.
- The document does not describe CSV import as part of the current implementation path.
- The document explains provider-symbol MVP versus final user-friendly asset search.
- The document includes non-binding example assets and provider-symbol candidates for Apple,
  Nvidia, ASML, VUSA, Tesla, and S&P 500 or another supported index or instrument.
- The document states provider symbols must be verified during implementation.
- The document does not claim any specific Stooq provider symbol is guaranteed.
- The document explains product-level asset identity versus provider-level `provider_symbol`.
- The document defines the target normalized OHLCV rows and recommended metadata.
- The document documents `adjusted_close` as a future decision without claiming it is
  implemented.
- The document states currency and exchange must be explicit where available.
- The document states no FX conversion is implemented yet.
- The document defines network failure and `needs_user_attention` behavior.
- The document states CI must not depend on live provider calls.
- The document states provider implementation should separate network fetch, response parsing,
  normalization, and validation handoff.
- `docs/product/asset_analysis_workflow.md` references real data provider strategy.
- `docs/product/asset_identity_and_symbol_resolution.md` references provider-specific symbols.
- No production source code is changed.
- No tests are changed.
- No provider implementation, Stooq client, asset search, symbol resolution logic, UI,
  watchlist storage, scheduled refresh, CSV import, or live data fetching is implemented.
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

- This ticket records provider direction and mapping strategy without claiming any live provider
  behavior is already implemented.
- Stooq is documented as the first provider candidate while preserving room for additional
  providers later.
