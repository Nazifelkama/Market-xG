# MXG-028 — Update GitHub Actions for Node 24 Compatibility

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: CI / Quality
Type: Maintenance / CI
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

The GitHub Actions workflow is currently green, but GitHub warns that some official actions
target Node.js 20 and are being forced onto the Node.js 24 runtime. The workflow should be
updated to use Node 24-compatible action versions without changing CI behavior.

## Goal

Update the GitHub Actions workflow to Node 24-compatible official action versions while
preserving the existing CI behavior.

## Scope

- Update `.github/workflows/ci.yml`.
- Add this ticket file under `docs/tickets/phase-2/`.
- Run the same local quality checks used by the workflow.

## Out of Scope

- Production source-code changes.
- Test changes.
- Scoring rule, indicator formula, or fixture changes.
- Workflow rename, trigger changes, job-name changes, runner changes, or Python-version
  changes.
- New jobs, new tools, self-hosted runners, or external dependencies.

## Implementation Instructions

- Update only the official GitHub Actions versions needed for Node 24 compatibility.
- Preserve workflow name, triggers, job names, runner OS, Python version, install command, and
  CI commands.
- Re-run the same local checks used by CI after the workflow update.

## Acceptance Criteria

- `.github/workflows/ci.yml` uses Node 24-compatible versions for affected GitHub Actions.
- `actions/checkout` is updated from `v4` to `v5` if present.
- `actions/setup-python` is updated from `v5` to `v6` if present.
- Existing CI behavior is preserved.
- Workflow name, triggers, job names, runner OS, Python version, dependency installation
  commands, and CI commands are not changed.
- No self-hosted runner configuration is added.
- No production source code is changed.
- No tests are changed.
- No scoring rules, indicator formulas, or fixture data are changed.
- No new jobs, tools, or dependencies are added.
- Local `pytest`, `ruff`, and `mypy` pass, or any inability to run them is clearly reported.
- After push, GitHub Actions should remain green and the Node 20 deprecation warning should be
  resolved.

## Test / Check Requirements

- Run `pytest`.
- Run `ruff check .`.
- Run `mypy src tests`.
- Verify the GitHub Actions run after push.

## Definition of Done

- Workflow updates are complete within ticket scope.
- Relevant local checks pass.
- Acceptance criteria are satisfied.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- This ticket updates only the minimum official action versions needed to address the Node 20
  deprecation warning.
- CI behavior is intentionally preserved so the workflow change remains operationally narrow.
