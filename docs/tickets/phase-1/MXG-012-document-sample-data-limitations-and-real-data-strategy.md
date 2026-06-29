# MXG-012 — Document Sample Data Limitations and Real Data Strategy

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Data Foundation
Type: Documentation / Data Strategy
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-011 introduced a deterministic synthetic OHLCV sample fixture for engineering work. The
repository now needs explicit documentation that this fixture is not real market history and
must not be used for financial conclusions or historical backtesting.

## Goal

Document the limits of the synthetic Phase 1 sample data and define the high-level strategy
for introducing real market data later.

## Scope

- Add `docs/architecture/real_data_strategy.md`.
- Update sample data documentation to state the fixture is synthetic and limited.
- Update architecture or README references where useful for traceability.
- Add focused tests that verify the new documentation exists and contains the required
  statements.

## Out of Scope

- Live market data fetching.
- External provider selection or implementation.
- Validation, indicators, scoring, reports, or backtesting code.
- Changes to the sample CSV beyond documentation consistency needs.

## Implementation Instructions

- Document that Phase 1 uses synthetic deterministic sample data only.
- State clearly that the fixture is for engineering tests, not financial conclusions or
  historical backtesting.
- Describe how future real data should be researched and introduced through later tickets.
- Keep tests local and documentation-focused.

## Acceptance Criteria

- `docs/architecture/real_data_strategy.md` exists.
- `docs/architecture/sample_market_data.md` clearly says the fixture is synthetic.
- `docs/architecture/sample_market_data.md` clearly says the fixture is not for financial
  conclusions or backtesting.
- `README.md` references `docs/architecture/real_data_strategy.md`.
- `docs/tickets/phase-1/MXG-012-document-sample-data-limitations-and-real-data-strategy.md`
  exists.
- No live data fetching is added.
- No market logic is implemented.

## Test Requirements

- Run `pytest tests/unit/test_real_data_strategy_docs.py`.
- Run `ruff check tests/unit/test_real_data_strategy_docs.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Documentation changes are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- The synthetic Phase 1 fixture remains intentionally narrow so later provider decisions can
  be made with explicit ticketed scope.
- Real data behavior will be researched before implementation instead of being implied by test
  fixtures.
