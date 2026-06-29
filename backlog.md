# Market xG Backlog

## Epic 1: Product Documentation

### MXG-001: Create product vision document

- Ticket ID: MXG-001
- Title: Create product vision document
- Goal: Define Market xG as decision support, not exact price prediction.
- Acceptance Criteria: Vision document exists and covers outputs, non-goals, and the football xG analogy.
- Test Notes: Review document for clear scope and non-deterministic language.
- Status: Not Started

### MXG-002: Create glossary

- Ticket ID: MXG-002
- Title: Create glossary
- Goal: Define core terms used across product, architecture, scoring, and testing.
- Acceptance Criteria: Glossary includes Market xG, category scores, confidence, regime, backtest, and lookahead bias.
- Test Notes: Review terminology for consistency with requirements and architecture docs.
- Status: Not Started

### MXG-003: Create roadmap

- Ticket ID: MXG-003
- Title: Create roadmap
- Goal: Define project phases from foundation through adaptive weighting.
- Acceptance Criteria: Roadmap exists and identifies Phase 0 through Phase 6.
- Test Notes: Review phase order against architecture and current implementation scope.
- Status: Not Started

## Epic 2: Architecture Foundation

### MXG-004: Create system design document

- Ticket ID: MXG-004
- Title: Create system design document
- Goal: Document the high-level data, scoring, reporting, and backtesting flow.
- Acceptance Criteria: System design describes data_providers, indicators, scoring, backtesting, narratives, reports, config, and utils.
- Test Notes: Review component boundaries for simple local-first execution.
- Status: Not Started

### MXG-005: Create scoring model document

- Ticket ID: MXG-005
- Title: Create scoring model document
- Goal: Document initial category weights and the v0.1 scoring philosophy.
- Acceptance Criteria: Scoring model includes all initial category weights and states that weights require historical validation.
- Test Notes: Check that weights add to 100% and avoid implying certainty.
- Status: Not Started

### MXG-006: Create ADRs for major early decisions

- Ticket ID: MXG-006
- Title: Create ADRs for major early decisions
- Goal: Record early decisions that shape the MVP.
- Acceptance Criteria: ADRs exist for rule-based scoring first, S&P 500 first, and CSV/Parquet before database.
- Test Notes: Review ADRs for context, decision, and consequences.
- Status: Not Started

## Epic 3: Repository Foundation

### MXG-007: Create Python project skeleton

- Ticket ID: MXG-007
- Title: Create Python project skeleton
- Goal: Create the src-layout Python package and placeholder modules.
- Acceptance Criteria: Package directories exist under src/market_xg and can be imported.
- Test Notes: Run structure and import tests.
- Status: Not Started

### MXG-008: Configure pytest, ruff, and mypy

- Ticket ID: MXG-008
- Title: Configure pytest, ruff, and mypy
- Goal: Add automated checks for tests, linting, and type checking.
- Acceptance Criteria: pyproject.toml configures pytest, ruff, mypy, and dev dependencies.
- Test Notes: Run pytest, ruff check src tests, and mypy src.
- Status: Not Started

### MXG-009: Add initial project structure tests

- Ticket ID: MXG-009
- Title: Add initial project structure tests
- Goal: Protect the expected documentation, source, test, and data folder layout.
- Acceptance Criteria: Tests fail if required foundation folders are missing.
- Test Notes: Run pytest and inspect folder coverage.
- Status: Not Started

### MXG-010: Add import tests

- Ticket ID: MXG-010
- Title: Add import tests
- Goal: Verify placeholder package modules are importable.
- Acceptance Criteria: Tests import market_xg and all initial component packages.
- Test Notes: Run pytest with src on pythonpath.
- Status: Not Started

## Epic 4: Data Ingestion

### MXG-011: Ingest S&P 500 daily OHLCV data

- Ticket ID: MXG-011
- Title: Ingest S&P 500 daily OHLCV data
- Goal: Load daily S&P 500 open, high, low, close, and volume data for the MVP.
- Acceptance Criteria: Raw S&P 500 data can be loaded locally with expected columns and dates.
- Test Notes: Add data quality tests for required columns, date order, duplicates, and missing values.
- Status: Not Started

### MXG-012: Ingest VIX daily data

- Ticket ID: MXG-012
- Title: Ingest VIX daily data
- Goal: Load daily VIX data for sentiment and volatility scoring.
- Acceptance Criteria: VIX input aligns by date with S&P 500 price data.
- Test Notes: Add tests for missing VIX values, date alignment, and numeric validity.
- Status: Not Started

### MXG-013: Ingest US 10Y yield data

- Ticket ID: MXG-013
- Title: Ingest US 10Y yield data
- Goal: Load US 10Y yield data for macro and interest rate scoring.
- Acceptance Criteria: Yield data loads locally and aligns with market data dates.
- Test Notes: Add tests for stale values, missing dates, and invalid yield ranges.
- Status: Not Started

### MXG-014: Validate raw market data

- Ticket ID: MXG-014
- Title: Validate raw market data
- Goal: Prevent invalid raw inputs from entering the scoring pipeline.
- Acceptance Criteria: Validation detects missing columns, invalid values, duplicate dates, and unexpected gaps.
- Test Notes: Add fixtures covering valid data and each failure mode.
- Status: Not Started

## Epic 5: Indicator Engine

### MXG-015: Calculate moving averages

- Ticket ID: MXG-015
- Title: Calculate moving averages
- Goal: Calculate deterministic moving averages for price trend analysis.
- Acceptance Criteria: Moving average outputs use correct windows and align to available historical dates only.
- Test Notes: Add unit tests with small known input series and expected outputs.
- Status: Not Started

### MXG-016: Calculate momentum indicators

- Ticket ID: MXG-016
- Title: Calculate momentum indicators
- Goal: Calculate simple momentum measures for trend and continuation quality.
- Acceptance Criteria: Momentum outputs are reproducible and handle insufficient history explicitly.
- Test Notes: Add unit tests for positive, negative, flat, and insufficient-history cases.
- Status: Not Started

### MXG-017: Calculate rolling drawdown

- Ticket ID: MXG-017
- Title: Calculate rolling drawdown
- Goal: Calculate rolling drawdown for historical risk context.
- Acceptance Criteria: Drawdown calculations use past and current values only.
- Test Notes: Add tests for peak, trough, recovery, and flat series cases.
- Status: Not Started

### MXG-018: Validate indicator outputs

- Ticket ID: MXG-018
- Title: Validate indicator outputs
- Goal: Detect invalid or suspicious indicator outputs before scoring.
- Acceptance Criteria: Validation catches missing indicator values, invalid ranges, and date misalignment.
- Test Notes: Add data quality tests for invalid indicator fixtures.
- Status: Not Started

## Epic 6: Scoring Engine

### MXG-019: Implement normalized score function

- Ticket ID: MXG-019
- Title: Implement normalized score function
- Goal: Convert indicator values into bounded 0-100 scores.
- Acceptance Criteria: Normalization clamps or rejects invalid scores according to documented behavior.
- Test Notes: Add unit tests for lower bound, upper bound, midpoint, and invalid inputs.
- Status: Not Started

### MXG-020: Implement Trend and Momentum score v0.1

- Ticket ID: MXG-020
- Title: Implement Trend and Momentum score v0.1
- Goal: Create the first rule-based trend and momentum category score.
- Acceptance Criteria: Category score returns 0-100 and explains its input drivers.
- Test Notes: Add unit tests for bullish, neutral, bearish, and missing-input cases.
- Status: Not Started

### MXG-021: Implement Sentiment and Volatility score v0.1

- Ticket ID: MXG-021
- Title: Implement Sentiment and Volatility score v0.1
- Goal: Create a rule-based sentiment and volatility category score using VIX.
- Acceptance Criteria: Score direction is documented and high VIX is not accidentally scored as low risk.
- Test Notes: Add tests for normal, elevated, and extreme VIX regimes.
- Status: Not Started

### MXG-022: Implement Macro and Interest Rates score v0.1

- Ticket ID: MXG-022
- Title: Implement Macro and Interest Rates score v0.1
- Goal: Create a rule-based macro score using US 10Y yield behavior.
- Acceptance Criteria: Macro score returns 0-100 and handles missing yield data explicitly.
- Test Notes: Add tests for rising, falling, stable, and missing yield inputs.
- Status: Not Started

### MXG-023: Implement weighted Market xG aggregation

- Ticket ID: MXG-023
- Title: Implement weighted Market xG aggregation
- Goal: Combine category scores into a final bounded Market xG score.
- Acceptance Criteria: Aggregation applies documented weights and returns a 0-100 score.
- Test Notes: Add tests for weight sums, missing categories, and bounds.
- Status: Not Started

### MXG-024: Implement confidence score v0.1

- Ticket ID: MXG-024
- Title: Implement confidence score v0.1
- Goal: Estimate trust in the score based on data completeness and input agreement.
- Acceptance Criteria: Confidence score returns 0-100 and drops when required data is missing.
- Test Notes: Add tests for complete, partial, conflicting, and invalid input states.
- Status: Not Started

## Epic 7: Narrative and Reports

### MXG-025: Generate category explanations

- Ticket ID: MXG-025
- Title: Generate category explanations
- Goal: Explain category score drivers in human-readable language.
- Acceptance Criteria: Explanations mention key drivers without implying certainty.
- Test Notes: Add unit tests for expected explanation fragments.
- Status: Not Started

### MXG-026: Generate daily markdown report

- Ticket ID: MXG-026
- Title: Generate daily markdown report
- Goal: Produce a daily markdown report with score, categories, confidence, and narrative.
- Acceptance Criteria: Report includes Market xG score, category scores, confidence score, market state, and explanation.
- Test Notes: Add integration tests for required report sections.
- Status: Not Started

### MXG-027: Add report snapshot tests

- Ticket ID: MXG-027
- Title: Add report snapshot tests
- Goal: Protect report structure from accidental regressions.
- Acceptance Criteria: Snapshot tests cover representative report output.
- Test Notes: Store or document sample output and compare stable sections.
- Status: Not Started

## Epic 8: Backtesting

### MXG-028: Calculate forward returns

- Ticket ID: MXG-028
- Title: Calculate forward returns
- Goal: Calculate future returns for historical score validation.
- Acceptance Criteria: Forward returns are calculated only after score dates and never used in scoring inputs.
- Test Notes: Add tests that detect off-by-one and lookahead bias.
- Status: Not Started

### MXG-029: Create score bucket analysis

- Ticket ID: MXG-029
- Title: Create score bucket analysis
- Goal: Group historical outcomes by Market xG score bucket.
- Acceptance Criteria: Buckets summarize forward returns and drawdowns by score range.
- Test Notes: Add tests for bucket boundaries, empty buckets, and aggregate calculations.
- Status: Not Started

### MXG-030: Detect lookahead bias risks

- Ticket ID: MXG-030
- Title: Detect lookahead bias risks
- Goal: Add safeguards against using future data in historical validation.
- Acceptance Criteria: Backtest validation flags future-dated inputs and improper joins.
- Test Notes: Add negative tests that intentionally include future leakage.
- Status: Not Started

### MXG-031: Generate backtest summary report

- Ticket ID: MXG-031
- Title: Generate backtest summary report
- Goal: Produce a concise report summarizing score bucket behavior and validation limits.
- Acceptance Criteria: Report includes bucket results, sample periods, limitations, and caveats.
- Test Notes: Add integration tests for required sections and no deterministic claims.
- Status: Not Started

