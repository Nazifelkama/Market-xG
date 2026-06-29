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

## Way of Working

The team workflow is documented in [docs/product/way_of_working.md](docs/product/way_of_working.md).
One ticket equals one branch equals one pull request. Work is accepted only after tests, CI,
and review.

Local Checks and Commit Workflow: [docs/product/local_checks_and_commit_workflow.md](docs/product/local_checks_and_commit_workflow.md).
Codex provides a review report before commit. Relevant local checks are used before review,
and full CI checks happen on PR before merge.

Definition of Done: [docs/test_strategy/definition_of_done.md](docs/test_strategy/definition_of_done.md).
Relevant local checks happen before review, full CI is required before merge, and a ticket is
Done only after merge to main.

Roadmap Governance: [docs/product/roadmap_governance.md](docs/product/roadmap_governance.md).
Roadmap changes must be intentional and traceable. Vision, phases, epics, tickets, PRs, and
commits should link together.

Market Data Contract: [docs/architecture/market_data_contract.md](docs/architecture/market_data_contract.md).
Phase 1 local sample OHLCV data must follow this contract before validation, indicators, or
scoring are implemented.

Sample Market Data Fixture: [docs/architecture/sample_market_data.md](docs/architecture/sample_market_data.md).
Phase 1 starts with deterministic local OHLCV sample data for repeatable tests and early
pipeline work.

Real Data Strategy: [docs/architecture/real_data_strategy.md](docs/architecture/real_data_strategy.md).
Synthetic sample data is for engineering tests only and must not be treated as a basis for
financial conclusions or historical backtesting.

Scoring Model: [docs/architecture/scoring_model.md](docs/architecture/scoring_model.md).
Phase 1 currently runs a deterministic local flow:
sample CSV -> validation -> indicators -> Trend and Momentum score -> Market xG aggregation
-> markdown report -> integration test.
Only the Trend and Momentum category is scored today. Missing categories are reported
explicitly and are not assigned fake scores.

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

Phase 1 local scoring MVP. The repository currently supports a deterministic synthetic/local
fixture flow for engineering validation only:
sample OHLCV CSV -> validation -> indicators -> Trend and Momentum score -> weighted Market xG
aggregation -> markdown report -> integration test.

The sample fixture is not real S&P 500 market data. It must not be used for financial
conclusions or backtesting.

Only the Trend and Momentum category has an implemented score in Phase 1. Other configured
Market xG categories remain future categories, are reported as missing, and are not assigned
fake scores.

Phase 1 scoring is heuristic, deterministic, and rule-based. It is not backtested or
calibrated yet, and it should be treated as product scaffolding rather than investment advice.
