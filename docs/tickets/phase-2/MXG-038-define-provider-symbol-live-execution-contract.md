# MXG-038 — Define Provider-Symbol Live Execution Contract

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Real Data Readiness
Type: Product / Execution Contract
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-032 implemented the raw Stooq historical data client and parser. MXG-033 implemented Stooq
normalization into Market xG OHLCV-compatible rows. MXG-034 implemented provider-based analysis
from an already-fetched `StooqHistoricalResponse`. MXG-035 defined Technical UAT scenarios,
MXG-036 implemented the deterministic UAT harness, and MXG-037 recorded a passing Technical UAT
result.

The next milestone is to move from already-fetched provider responses toward direct
provider-symbol based live execution.

## Goal

Define the product and engineering contract for provider-symbol based live execution before any
live execution implementation begins.

## Scope

- Create `docs/product/provider_symbol_live_execution_contract.md`.
- Create this ticket document under `docs/tickets/phase-2/`.
- Optionally add short references from related product or UAT documentation.

## Out of Scope

- Production source-code changes.
- Test changes.
- Provider-symbol live execution implementation.
- Live Stooq calls or real provider symbol verification.
- CLI, UI, asset search, symbol resolution, watchlist storage, scheduling, persisted analysis
  status, or CSV import.
- Real market data files.
- Scoring rules, indicator formulas, Market xG aggregation weights, or report wording changes.
- Dependency changes.

## Documentation Requirements

- Explain provider-symbol execution as an interim technical and product milestone.
- Define the current already-fetched provider-analysis path.
- Define the next intended direct provider-symbol path.
- Define required and future provider-symbol input fields.
- Define successful output expectations.
- Define failure categories and status guidance.
- Define intended status flow.
- Define CI and live-provider boundaries.
- Clarify that provider symbols are candidates until verified.
- Explain the relationship between provider-level symbols and product-level asset identity.
- Preserve product trust and safety wording expectations.
- Document known limitations and the likely next implementation step.

## Acceptance Criteria

- `docs/product/provider_symbol_live_execution_contract.md` exists.
- Document defines provider-symbol input contract.
- Document defines successful output contract.
- Document defines failure categories.
- Document maps failures to `failed` or `needs_user_attention` guidance.
- Document defines intended status flow.
- Document states CI must not depend on live provider calls.
- Document states manual live verification is separate from CI.
- Document states provider symbols are candidates until verified.
- Document states no specific symbol is guaranteed by this ticket.
- Document states provider-symbol execution is interim and not final product search.
- Document explains relationship between `provider_symbol` and asset identity.
- Document preserves safe product wording and missing-category transparency.
- Known limitations are documented.
- Next implementation step is documented.
- This ticket file exists.
- No production source code is changed.
- No tests are changed.
- No live provider fetching or provider-symbol execution is implemented.
- No provider symbol verification is performed.
- No CLI, UI, asset search, symbol resolution, watchlist, scheduling, persisted status, or CSV
  import is implemented.
- No real market data files are added.
- No scoring rules, indicator formulas, aggregation weights, or report wording are changed.
- No dependencies are added.

## Check Requirements

- Run `git diff --check`.
- If markdown linting is configured later, run the relevant markdown-lint command.
- Do not run the full local test suite unless needed.

## Definition of Done

- Provider-symbol live execution contract is documented within ticket scope.
- Acceptance criteria are satisfied.
- Required checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Provider-symbol live execution is an interim milestone, not the final user experience.
- Final product target remains user-friendly asset search and selected asset identity.
- v0.1 provider-symbol execution is expected to use Stooq first.
- Direct provider symbols must not become a hard-coded `VUSA`-only path.
- CI must not depend on live provider calls.
- Real provider symbol verification remains separate from this contract.
- Persisted status is not implemented in this ticket.
