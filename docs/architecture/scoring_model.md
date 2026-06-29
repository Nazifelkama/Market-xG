# Scoring Model

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

## Weighting Philosophy

These weights are v0.1 defaults. They are intended to provide a clear, explainable starting point rather than a final optimized model.

Weights should be tuned later through historical validation. Backtests should examine whether categories and weights improve the relationship between Market xG scores and forward returns, drawdowns, and market state transitions.

