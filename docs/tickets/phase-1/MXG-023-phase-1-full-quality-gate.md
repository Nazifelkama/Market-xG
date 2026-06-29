# MXG-023 — Phase 1 Full Quality Gate

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Quality
Type: Quality / Release Gate
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-022 aligned the Phase 1 documentation and decision logs. The repository now has the full
Phase 1 local stack in place, including deterministic fixture validation, indicators, scoring,
aggregation, reporting, and an integration test. Before closing Phase 1, the full local
quality gate should pass cleanly.

## Goal

Run the full local quality gate for Phase 1 and fix only failures that are directly required
to make the repository pass cleanly.

## Scope

- Add this ticket file under `docs/tickets/phase-1/`.
- Run the full configured test, lint, and type-check commands.
- Apply only minimal fixes that are directly justified by failing checks.

## Out of Scope

- New features, indicators, scoring categories, or reports.
- Scoring-rule or indicator-formula changes unless a failing check proves a real bug.
- Fixture changes unless a failing check proves the fixture is invalid.
- Refactors for preference, module renames, or package reorganization.
- Live data fetching, external dependencies, CLI, dashboard, charts, or production pipeline
  work.

## Quality Gate Commands

- `pytest`
- `ruff check .`
- `mypy src tests`

## Fix Policy

- Fix only failures found by `pytest`, `ruff`, or `mypy`.
- Keep fixes minimal and directly tied to specific failing checks.
- Do not modify passing code or tests for preference.
- If failures are broad or ambiguous, report them instead of making sweeping changes.

## Acceptance Criteria

- Full `pytest` passes, or any failure is clearly reported without broad unrelated changes.
- Full `ruff check .` passes, or any failure is clearly reported without broad unrelated
  changes.
- Full `mypy src tests` passes, or any failure is clearly reported without broad unrelated
  changes.
- This MXG-023 ticket file exists.
- If all checks pass, only the MXG-023 ticket file is changed.
- Any non-ticket-file fixes are minimal and directly tied to quality gate failures.
- No new features are added.
- No new indicators or scoring categories are added.
- No scoring rules or indicator formulas are changed unless required by a proven check
  failure.
- No fixture data is changed unless required by a proven check failure.
- No module, function, class, or file renames or package reorganization are done.
- No live data fetching or external dependencies are added.
- No CLI, dashboard, charts, production pipeline, or report files are created.

## Test / Check Requirements

- Run `pytest`.
- Run `ruff check .`.
- Run `mypy src tests`.
- Record any fixes and the failing checks that justified them.

## Definition of Done

- The full local quality gate has been executed.
- Any required fixes are complete and minimal.
- Acceptance criteria are satisfied.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Phase 1 should close on a clean repository state rather than relying only on incremental
  ticket-level checks.
- Quality-gate fixes, if any, should stay tightly scoped to proven failures.
