# Local Checks and Commit Workflow

## Purpose

This document defines what Codex should do after implementing a ticket but before committing or
pushing. It keeps review fast while preserving human QA control over what becomes part of the
project history.

## Core Rule

Codex does not commit immediately after implementation.

Codex must first provide a review report and wait for human approval.

## Standard Flow

1. Implement only the ticket scope.
2. Run relevant local checks.
3. Provide a review report.
4. Wait for approval.
5. Commit only after approval.
6. Push the ticket branch after commit, if requested.
7. Never push directly to main.
8. Full checks run in CI before merge.

## Relevant Local Checks

Local checks should match the type and risk of the change.

For documentation-only tickets:

- Run the specific doc-related pytest file, if one exists.
- Run ruff only on changed Python test files, if Python tests were changed.
- Do not run mypy unless `src` Python files changed.
- Do not run the full test suite unless the documentation change is broad or touches many tests.

For Python/code tickets:

- Run relevant unit tests.
- Run relevant integration tests if workflow behavior changed.
- Run ruff on changed Python files.
- Run mypy only on affected `src` modules or full `src` if easier.
- Run broader tests if shared/core logic changed.

For backtest/scoring/data tickets:

- Run relevant unit tests.
- Run relevant integration tests.
- Run data validation or backtest validation tests if available.
- Be stricter because mistakes can create false confidence.

## Full CI Gate

Full checks are expected on PR through CI. A PR cannot be merged until CI is green.

Local checks are for fast feedback. CI is the final automated quality gate.

## Review Report Format

Codex must provide:

- Ticket ID.
- Changed files.
- Summary of changes.
- Relevant checks run.
- Test results.
- Assumptions or limitations.
- Confirmation no unrelated scope was added.
- Confirmation whether commit was created.
- Confirmation whether branch was pushed.

## Approval Rule

Human approval is required before commit/push.

Approval can be written as "approved, commit and push". If changes are requested, Codex updates
the same ticket work and provides a new report. Codex should not start another ticket while
waiting for approval.

## Commit Rule

Commit message must include the ticket ID. Commit only files related to the approved ticket.
Do not combine unrelated tickets in one commit after this workflow is adopted.

