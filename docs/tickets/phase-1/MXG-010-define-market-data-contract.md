# MXG-010 — Define Market Data Contract

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Data Foundation
Type: Documentation / Data Contract
Owner: Codex
Reviewer: QA / PM
Branch: TBD
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

Market xG Phase 1 will use deterministic local sample market data first. Before adding fixtures,
validation, indicators, or scoring, the project needs a clear OHLCV data contract.

## Goal

Define the Phase 1 market data contract for daily OHLCV data.

## Scope

- Create `docs/architecture/market_data_contract.md`.
- Create this MXG-010 ticket file under `docs/tickets/phase-1/`.
- Add focused tests that verify the contract and ticket documentation exist.
- Add relevant references from project documentation.

## Out of Scope

- Data validation code.
- Sample CSV data.
- Indicators.
- Scoring.
- Reports.
- Live market data fetching.
- External dependencies.
- Automatic commit.

## Implementation Instructions

- Document the required OHLCV columns.
- Document column-level rules.
- Document date handling for daily trading data.
- Add valid and invalid data examples.
- State that Phase 1 uses deterministic local sample data only.
- State that validation code will be implemented later.

## Acceptance Criteria

- `docs/architecture/market_data_contract.md` exists.
- Required OHLCV columns are documented.
- Column rules are documented.
- Valid and invalid examples are documented.
- `docs/tickets/phase-1/MXG-010-define-market-data-contract.md` exists.
- `README.md` references `docs/architecture/market_data_contract.md` if README has a docs section.
- No validation code is implemented.
- No market logic is implemented.

## Test Requirements

- Run `pytest tests/unit/test_market_data_contract_docs.py`.
- Run `ruff check tests/unit/test_market_data_contract_docs.py`.
- Do not run mypy unless `src` Python files are changed.
- Do not run the full test suite unless needed.

## Definition of Done

- Documentation created or updated.
- Relevant local checks pass.
- Review report provided.
- No automatic commit before approval.
- No unrelated scope added.

## Review Notes

Awaiting QA / PM review after relevant local checks pass.

## Decision Log

- Phase 1 starts with deterministic local sample data only.
- Live market data fetching is explicitly excluded from this ticket.
- Validation code is deferred to a later ticket.

