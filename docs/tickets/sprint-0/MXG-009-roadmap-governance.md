# MXG-009 — Roadmap Governance

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

Market xG now has project foundation, executable tickets, Way of Working, local checks and
review-before-commit workflow, and Definition of Done. Before creating the big implementation
roadmap, the project needs governance rules for how roadmap, phases, epics, and tickets are
created and changed.

## Goal

Create roadmap governance documentation that defines how roadmap phases, epics, tickets,
approvals, future ideas, and traceability work.

## Scope

- Create `docs/product/roadmap_governance.md`.
- Create this MXG-009 ticket file.
- Update README, roadmap, Way of Working, ticket README, and ticket template.
- Add focused tests for roadmap governance documentation.

## Out of Scope

- Market logic.
- Data ingestion.
- Indicators.
- Scoring.
- Backtesting.
- Reports.
- Dashboard features.
- Full implementation roadmap.
- Future implementation tickets beyond MXG-009.
- Package behavior changes.
- External dependencies.
- Automatic commit.

## Implementation Instructions

- Document roadmap levels from vision to commit.
- Document phase, epic, and ticket rules.
- Document change control and future ideas parking lot.
- Document review cadence and traceability.
- Link roadmap governance from relevant project and ticket documentation.
- Add tests that verify required docs and phrases exist.

## Acceptance Criteria

- `docs/product/roadmap_governance.md` exists.
- `README.md` references `docs/product/roadmap_governance.md`.
- `docs/product/roadmap.md` references `docs/product/roadmap_governance.md`.
- `docs/product/way_of_working.md` references roadmap governance.
- `docs/tickets/README.md` references roadmap governance.
- `docs/tickets/template.md` mentions roadmap traceability.
- `tests/unit/test_roadmap_governance_docs.py` exists and passes.
- No market logic is implemented.
- No future implementation tickets are created.

## Test Requirements

- Run `pytest tests/unit/test_roadmap_governance_docs.py`.
- Run `ruff check tests/unit/test_roadmap_governance_docs.py`.
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

- Roadmap changes require human approval.
- Major roadmap decisions should be captured in ADRs.
- Later-phase ideas should be parked instead of implemented early.

