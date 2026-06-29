# MXG-008 — Definition of Done

Status: In Progress
Sprint: Sprint 0
Type: Documentation / Process
Owner: Codex
Reviewer: QA / PM
Branch: TBD
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

The Market xG project foundation exists. Way of Working has been documented. Local checks and
review-before-commit workflow has been documented. The team now needs a clear Definition of
Done so future tickets cannot be accepted just because code or documentation was generated.

## Goal

Create a project-wide Definition of Done that defines quality gates for documentation, code,
data, scoring, backtest, report/narrative, and completion report work.

## Scope

- Create or update `docs/test_strategy/definition_of_done.md`.
- Create this MXG-008 ticket file.
- Update README, Way of Working, local-check workflow, ticket README, and ticket template.
- Add focused tests for Definition of Done documentation.

## Out of Scope

- Market logic.
- Data ingestion.
- Indicators.
- Scoring.
- Backtesting.
- Reports.
- Dashboard features.
- Future implementation tickets beyond MXG-008.
- Package behavior changes.
- External dependencies.
- Automatic commit.

## Implementation Instructions

- Document the global Definition of Done.
- Document DoD requirements by ticket type.
- Document completion report requirements.
- Document examples of work that is not Done.
- Link the Definition of Done from existing process and ticket documentation.
- Add tests that verify required docs and phrases exist.

## Acceptance Criteria

- `docs/test_strategy/definition_of_done.md` exists.
- `README.md` references `docs/test_strategy/definition_of_done.md`.
- `docs/product/way_of_working.md` mentions Definition of Done.
- `docs/product/local_checks_and_commit_workflow.md` references Definition of Done.
- `docs/tickets/README.md` references `docs/test_strategy/definition_of_done.md`.
- `docs/tickets/template.md` contains "Use docs/test_strategy/definition_of_done.md as the global quality gate".
- `tests/unit/test_definition_of_done_docs.py` exists and passes.
- No market logic is implemented.
- No future implementation tickets are created.

## Test Requirements

- Run `pytest tests/unit/test_definition_of_done_docs.py`.
- Run `ruff check tests/unit/test_definition_of_done_docs.py`.
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

- Definition of Done is the project-wide quality gate.
- Relevant local checks happen before review.
- Full CI is required before merge.
- Ticket status becomes Done only after merge to main.

