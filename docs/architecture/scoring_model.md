# Scoring Model

## Phase 1 System Flow

Phase 1 currently uses this deterministic local flow:

sample CSV -> validation -> indicators -> Trend and Momentum score -> Market xG aggregation
-> markdown report -> integration test

The sample fixture is synthetic/local only. It is not real S&P 500 market data, it is used
for engineering validation only, and it must not be used for financial conclusions or
backtesting.

## Category Weights v0.1

The initial Market xG score will be calculated from weighted category scores.

| Category | Weight |
| --- | ---: |
| Trend and Momentum | 20% |
| Breadth and Participation | 20% |
| Earnings and Fundamental Strength | 15% |
| Macro and Interest Rates | 15% |
| Liquidity and Fund Flows | 10% |
| Sentiment and Volatility | 10% |
| Volume and Accumulation | 5% |
| Valuation | 5% |

## Phase 1 Current Scope

Only the Trend and Momentum category has an implemented score in Phase 1.
Other Market xG categories are configured as future categories only.
Missing categories are reported explicitly and are not assigned fake scores.

## Weighting Philosophy

These weights are v0.1 defaults. They are intended to provide a clear, explainable starting point rather than a final optimized model.

Weights should be tuned later through historical validation. Backtests should examine whether categories and weights improve the relationship between Market xG scores and forward returns, drawdowns, and market state transitions.

## Aggregation Decision

Phase 1 aggregation can reweight available categories.
Reweighting does not create fake category scores.
When only `trend_momentum` is available, Market xG equals the `trend_momentum` score under
reweighting.

## Score Interpretation Limits

The current Market xG score is heuristic, deterministic, and rule-based.
It is not calibrated by backtesting yet.
It should be treated as software and product scaffolding, not investment advice.

The markdown report language reflects the same limits:

- Market xG is probabilistic decision support.
- Market xG is not price prediction.
- The report does not guarantee future returns or outcomes.

## Indicator Output Decision

`IndicatorResult` was introduced as a lightweight future-facing indicator output contract.
Existing Phase 1 indicator functions may still return primitive values.
Existing Phase 1 scorers may still accept primitive `float | None` inputs.
`IndicatorResult` is not fully wired through the Phase 1 pipeline yet.

## Integration Test Decision

MXG-021 proves that implemented Phase 1 modules work together on deterministic fixture data.
It is an integration test, not a production pipeline.
It does not fetch live data.
It does not write reports to disk.

## High-Level Next Direction

At a high level, Volume / Accumulation is a logical next category because the sample fixture
already includes volume.
Real data provider work should remain separate from scoring-category expansion.
