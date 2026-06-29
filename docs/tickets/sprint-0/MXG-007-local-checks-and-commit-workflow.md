# MXG-007 — Local Checks and Review-Before-Commit Workflow

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

The Market xG project foundation is committed and Way of Working documentation exists. Before
creating the Definition of Done, the team needs a practical local-check and commit workflow.
Codex should implement ticket work, run relevant checks, provide a review report, and wait for
human approval before committing or pushing.

## Goal

Document the local-check and review-before-commit workflow so delivery remains fast while QA and
PM retain control over commits and pushes.

## Scope

- Create `docs/product/local_checks_and_commit_workflow.md`.
- Create this MXG-007 ticket file.
- Update README, Way of Working, ticket README, and ticket template.
- Add focused tests for local-check workflow documentation.

## Out of Scope

- Market logic.
- Data ingestion.
- Indicators.
- Scoring.
- Backtesting.
- Reports.
- Dashboard features.
- Future implementation tickets.
- Package behavior changes.
- External dependencies.
- Automatic commit.

## Implementation Instructions

- Document that Codex does not commit immediately after implementation.
- Document relevant local checks by ticket type.
- Document that full CI remains the final automated quality gate before merge.
- Document the required review report format.
- Document that human approval is required before commit/push.
- Add tests that verify the required docs and phrases exist.

## Acceptance Criteria

- `docs/product/local_checks_and_commit_workflow.md` exists.
- `README.md` references `docs/product/local_checks_and_commit_workflow.md`.
- `docs/product/way_of_working.md` references review report before commit.
- `docs/tickets/README.md` references `docs/product/local_checks_and_commit_workflow.md`.
- `docs/tickets/template.md` contains "Relevant local checks before review".
- `docs/tickets/template.md` contains "Full CI before merge".
- `tests/unit/test_local_checks_workflow_docs.py` exists and passes.
- No market logic is implemented.
- No future implementation tickets are created.

## Test Requirements

- Run `pytest tests/unit/test_local_checks_workflow_docs.py`.
- Run `ruff check tests/unit/test_local_checks_workflow_docs.py`.
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

- Local checks are scoped to ticket risk.
- Full CI remains the final automated quality gate before merge.
- Codex waits for human approval before commit/push.

