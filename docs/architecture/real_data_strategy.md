# Real Data Strategy

## Purpose

This document defines how Market xG should treat synthetic sample data in Phase 1 and how
real market data should be introduced later without weakening determinism, traceability, or
test reliability.

## Phase 1 Position

- Phase 1 uses synthetic deterministic sample data only.
- The committed sample fixture exists for deterministic engineering tests.
- The sample fixture must not be used for financial conclusions.
- The sample fixture must not be used for historical backtesting.
- Phase 1 tests must not depend on live network calls.

## Why the Synthetic Fixture Exists

- Early tickets need stable local input before provider research and ingestion work begin.
- Deterministic fixtures keep tests reproducible across machines and CI runs.
- The fixture supports engineering validation of file shape, contracts, and pipeline wiring.
- The fixture is intentionally limited and does not represent real market history.

## Real Data Introduction Strategy

- Real data providers will be introduced later.
- Candidate real data sources should be researched before implementation.
- Provider choice should consider licensing, reliability, historical coverage, and update
  behavior.
- Provider integration should arrive through explicit future tickets, not ad hoc expansion of
  sample-data work.

## Testing Strategy for Future Providers

- Real data provider tests should use fixtures or mocks, not live network calls.
- Integration boundaries should be validated with committed sample responses where possible.
- Network-dependent checks, if ever added later, should be isolated from the default test
  suite.

## Future Real Data Considerations

Future real data may require:

- adjusted close
- source
- symbol
- currency
- timezone
- data quality rules

These fields and rules are intentionally out of scope for the synthetic Phase 1 fixture and
should be introduced only when the corresponding ingestion and validation tickets begin.
