# MXG-005 — Store Executable Tickets

Status: Not Started
Sprint: Sprint 0
Type: Documentation / Test
Owner: Codex
Reviewer: QA / PM

## Context

Market xG uses Agile tickets with V-model style traceability. The repository should store the
actual Codex-ready ticket files so QA and future contributors can compare implementation against
the original instructions.

## Goal

Create a ticket documentation structure and add initial Sprint 0 ticket files.

## Scope

- `docs/tickets/README.md`.
- `docs/tickets/template.md`.
- `docs/tickets/sprint-0/` ticket files.
- Tests verifying ticket documentation exists.

## Out of Scope

- Implementing market logic.
- Changing project behavior.
- Rewriting existing docs.
- Creating Sprint 1 implementation ticket details.

## Implementation Instructions

- Group ticket files by sprint.
- Make tickets Codex-ready, not just summaries.
- Include context, goal, scope, acceptance criteria, test requirements, and definition of done.
- Add tests for required files and headings.

## Acceptance Criteria

- `docs/tickets/README.md` exists.
- `docs/tickets/template.md` exists.
- Sprint 0 ticket files exist.
- Tests verify ticket documentation exists.

## Test Requirements

- Add `tests/unit/test_ticket_docs.py`.
- Verify all Sprint 0 ticket files exist.
- Verify required headings exist in each Sprint 0 ticket file.
- Run pytest, ruff, and mypy.

## Definition of Done

- Ticket documentation structure exists.
- Sprint 0 tickets are readable and concise.
- Ticket doc tests pass.
- All existing tests still pass.

## Notes / Decisions

This ticket makes implementation prompts version-controlled and reviewable.

