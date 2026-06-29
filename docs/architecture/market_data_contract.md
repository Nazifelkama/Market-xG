# Market Data Contract

## Purpose

This document defines the OHLCV data shape used by Phase 1 of Market xG. It describes the
minimum local daily market data contract required before validation, indicators, or scoring are
implemented.

## Required Columns

Phase 1 OHLCV data must include these required columns:

- `date`
- `open`
- `high`
- `low`
- `close`
- `volume`

## Column Rules

- `date` must be parseable as a date.
- `date` must be unique.
- Rows must be sorted ascending by `date`.
- `open`, `high`, `low`, and `close` must be numeric.
- `volume` must be numeric and non-negative.
- `high` must be greater than or equal to `low`.
- `open` should be between `low` and `high`.
- `close` should be between `low` and `high`.
- Missing required values are invalid.

## Date Handling

- Phase 1 uses daily market data.
- Dates represent trading days.
- Weekends and market holidays may be absent.
- The data must be sorted ascending before indicator calculation.

## Valid Data Example

| date | open | high | low | close | volume |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2024-01-02 | 4750.20 | 4782.10 | 4738.30 | 4768.40 | 2500000000 |
| 2024-01-03 | 4768.40 | 4775.00 | 4715.20 | 4725.80 | 2600000000 |
| 2024-01-04 | 4725.80 | 4748.60 | 4710.50 | 4739.20 | 2400000000 |

## Invalid Data Examples

| Issue | Example | Reason |
| --- | --- | --- |
| Missing close | `2024-01-02,4750.20,4782.10,4738.30,,2500000000` | Missing required values are invalid. |
| Duplicate date | Two rows with `2024-01-02` | `date` must be unique. |
| Negative volume | `volume = -100` | `volume` must be non-negative. |
| High lower than low | `high = 4700`, `low = 4750` | `high` must be greater than or equal to `low`. |
| Unsorted dates | `2024-01-03` appears before `2024-01-02` | Rows must be sorted ascending by `date`. |

## Phase 1 Constraint

- Phase 1 uses deterministic local sample data only.
- No live data fetching is part of this ticket.
- Validation code will be implemented in a later ticket.

