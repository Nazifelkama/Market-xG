# Test Strategy

## Test Layers

### Unit Tests

Validate individual calculations such as indicators, score normalization, category scoring, weighting, and confidence scoring.

### Integration Tests

Validate that data ingestion, indicator calculation, scoring, narrative generation, and report generation work together correctly.

### Data Quality Tests

Validate missing data detection, invalid values, date alignment, duplicate rows, stale data, and unexpected gaps.

### Backtest Validation Tests

Validate forward return calculation, drawdown calculation, score bucket grouping, and prevention of lookahead bias.

### Acceptance Tests

Validate that the system meets documented business, functional, and reporting expectations for each project phase.

## Specific Risks

- Lookahead bias.
- Incorrect moving average windows.
- Incorrect score normalization.
- Missing data treated as valid data.
- Beautiful reports with wrong calculations.

