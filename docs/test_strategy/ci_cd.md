# CI/CD

## Purpose

The CI pipeline protects the Market xG foundation by running automated quality checks before
changes are merged. It helps keep the project testable, reproducible, and ready for the first
real scoring implementation tickets.

## When It Runs

The GitHub Actions workflow runs on:

- Pull requests targeting `main`.
- Pushes to `main`.
- Manual `workflow_dispatch` runs.

## What It Checks

The `quality-checks` job runs on Ubuntu with Python 3.11 and verifies:

- `ruff check src tests`
- `mypy src`
- `pytest --cov=market_xg --cov-report=term-missing`

The CI must fail if linting, type checking, or tests fail.

## Local Checks

Run the same checks locally before opening or updating a pull request:

```bash
pip install -e ".[dev]"
ruff check src tests
mypy src
pytest --cov=market_xg --cov-report=term-missing
```

## Branch Protection Recommendation

- Protect the `main` branch.
- Require a pull request before merge.
- Require status check: `quality-checks`.
- Require conversation resolution before merge.
- Do not allow force pushes to `main`.
- Do not allow direct pushes to `main`.

