# Market xG

Market xG is a probabilistic market quality and continuation engine inspired by football
expected goals. It scores the quality of the current market setup and supports disciplined
market review.

Market xG is not a price prediction tool. It does not forecast exact future prices, provide
guaranteed buy or sell signals, or claim certainty about market outcomes.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Continuous Integration

GitHub Actions runs automated checks on pull requests and pushes to `main`.
The pipeline runs ruff, mypy, and pytest with coverage.

Run the same checks locally with:

```bash
ruff check src tests
mypy src
pytest --cov=market_xg --cov-report=term-missing
```

## Project Structure

```text
docs/                  Product, requirements, architecture, test strategy, and ADRs
src/market_xg/         Python package source
  config/              Configuration placeholders
  data_providers/      Data provider placeholders
  indicators/          Indicator placeholders
  scoring/             Scoring placeholders
  backtesting/         Backtest placeholders
  narratives/          Narrative placeholders
  reports/             Report placeholders
  utils/               Shared utility placeholders
tests/                 Automated tests
  unit/                Unit tests
  integration/         Integration tests
  backtest/            Backtest validation tests
data/                  Local data folders, ignored except .gitkeep files
notebooks/             Exploration notebooks
scripts/               Developer scripts
```

## Current Status

Phase 0 foundation. The repository contains documentation, packaging configuration,
placeholder modules, and automated checks. Market logic is intentionally not implemented yet.
