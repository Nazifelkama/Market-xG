# MXG-004 — CI Pipeline and PR Quality Gate

Status: Not Started
Sprint: Sprint 0
Type: CI
Owner: Codex
Reviewer: QA / PM

## Context

Market xG uses pytest, ruff, and mypy. Pull requests and pushes to `main` need an automated
quality gate before implementation work expands.

## Goal

Add a simple GitHub Actions CI workflow and supporting CI/CD documentation.

## Scope

- `.github/workflows/ci.yml`.
- `docs/test_strategy/ci_cd.md`.
- README CI section.
- Tests for CI docs.

## Out of Scope

- Deployment automation.
- Release automation.
- Poetry, uv, tox, or nox.
- Market logic.

## Implementation Instructions

- Use GitHub Actions with Python 3.11 on `ubuntu-latest`.
- Use one stable job named `quality-checks`.
- Run ruff, mypy, and pytest with coverage.
- Document branch protection recommendations.

## Acceptance Criteria

- CI workflow exists.
- CI runs on `pull_request` to `main`.
- CI runs on `push` to `main`.
- CI can be triggered manually with `workflow_dispatch`.
- CI runs ruff, mypy, and pytest with coverage.
- CI job is named `quality-checks`.

## Test Requirements

- Add tests verifying CI workflow and CI/CD docs exist.
- Verify workflow contains required commands.
- Run pytest, ruff, and mypy locally.

## Definition of Done

- CI workflow is committed-ready.
- CI documentation exists.
- Local checks pass.
- Acceptance criteria are satisfied.

## Notes / Decisions

The workflow is intentionally simple so `quality-checks` can later become a required status
check.

