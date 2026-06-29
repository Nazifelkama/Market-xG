# Sample Market Data

## Purpose

This document defines the deterministic local sample market data fixture used in Phase 1.
The fixture exists to support repeatable tests and early pipeline work before live data,
validation logic, or external integrations are introduced.

## Fixture Location

The committed Phase 1 fixture lives at
`tests/fixtures/market_data/sample_sp500_ohlcv.csv`.

## Relationship to Market Data Contract

The fixture is intentionally shaped to follow
`docs/architecture/market_data_contract.md`.
It is a concrete reference dataset for the OHLCV contract, not a separate schema.

## Data Characteristics

- Synthetic but S&P 500-like daily OHLCV values.
- Deterministic and committed to the repository for stable tests.
- Daily rows with parseable dates sorted ascending.
- Required columns only: `date`, `open`, `high`, `low`, `close`, `volume`.
- No missing required values.
- Positive OHLC values and non-negative volume.
- Intended for Phase 1 local development and test scenarios.

## Usage

- Use this fixture for tests that need valid local OHLCV input.
- Use it as the baseline example when discussing the Phase 1 data contract.
- Keep the file deterministic so future test outcomes stay reproducible.
- Replace or extend it only through a new ticket with explicit review.

## Non-Goals

- This fixture is not live market data.
- This fixture does not prove historical correctness versus external sources.
- This ticket does not add validation code.
- This ticket does not add indicators, scoring, reports, or fetching logic.
