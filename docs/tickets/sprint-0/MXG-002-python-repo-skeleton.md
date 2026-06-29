# MXG-002 — Python Repo Skeleton

Status: Not Started
Sprint: Sprint 0
Type: Repo
Owner: Codex
Reviewer: QA / PM

## Context

Market xG needs a simple Python repository foundation before real scoring work begins. The
project uses a `src` layout with package name `market_xg`.

## Goal

Create the initial Python package skeleton, packaging configuration, ignored local artifacts,
and placeholder automated checks.

## Scope

- `src/market_xg` package structure.
- `tests` structure.
- `data` directories.
- `pyproject.toml`.
- `README.md`.
- `.gitignore`.
- pytest configuration.
- ruff configuration.
- mypy configuration.
- Placeholder tests.

## Out of Scope

- Market logic.
- Market data fetching.
- Indicator calculations.
- pandas or numpy dependencies.

## Implementation Instructions

- Use setuptools and `src` layout.
- Add placeholder package modules only.
- Add tests for required folders, imports, and a fake pipeline step.
- Keep the repo local-first and simple.

## Acceptance Criteria

- Project can be installed with `pip install -e ".[dev]"`.
- pytest passes.
- `ruff check src tests` passes.
- `mypy src` passes.
- Required folders exist.
- Required modules can be imported.

## Test Requirements

- Run pytest.
- Run ruff.
- Run mypy.
- Run `scripts/run_tests.sh`.

## Definition of Done

- Repo skeleton is present.
- Automated checks pass.
- No market logic is implemented.
- Acceptance criteria are satisfied.

## Notes / Decisions

This ticket provides the foundation for future implementation tickets without introducing model
behavior.

