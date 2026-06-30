# Asset Analysis Workflow

## Product Purpose

Market xG lets a user analyze market quality for a selected asset and optionally track that
asset over time in a watchlist. The product is probabilistic decision support, not guaranteed
price prediction, and it should avoid language that promises future returns or certain outcomes.

## Core User Actions

### Analyze Now

1. The user searches for an asset.
2. The user selects the correct asset result.
3. The system runs one Market xG analysis for that selected asset.
4. The system shows processing status while analysis runs.
5. When ready, the system shows the Market xG score, interpretation, category scores,
   strengths, weaknesses, missing categories, and the generated report.

### Track Asset

1. The user searches for an asset.
2. The user selects the correct asset result.
3. The system adds the asset to a watchlist.
4. The system stores the selected asset identity.
5. The system can later refresh or re-run analysis for that asset.

Scheduled refresh is future work and must not be described as already implemented.

## Example Target Assets

These examples are for product workflow design only. No provider integration is implemented in
this ticket.

- Apple Inc. / AAPL / NASDAQ / USD / equity
- Vanguard S&P 500 UCITS ETF / VUSA.AS / Euronext Amsterdam / EUR / ETF
- ASML Holding / ASML.AS / Euronext Amsterdam / EUR / equity
- Nvidia / NVDA / NASDAQ / USD / equity

## Asset Identity Requirement

The user must not search only by display name. The selected asset should resolve to an explicit
identity with:

- `symbol`
- `display_name`
- `exchange`
- `currency`
- `asset_type`
- `source`, when known

This matters because the same display name can refer to different listings. For example,
`VUSA.AS` on Euronext Amsterdam in EUR is not the same as a London listing or a USD/GBP-priced
listing. The engine should never silently analyze the wrong listing or wrong currency.

## Analysis Status Model

- `idle`: no analysis is running and the system is waiting for user input.
- `resolving_asset`: the system is matching the user search to a specific tradable asset.
- `waiting_for_data`: the system needs a local CSV upload or provider data before processing.
- `fetching_data`: the system is loading market data from the chosen source.
- `validating_data`: the system is checking whether the OHLCV input matches the required contract.
- `calculating_indicators`: the system is deriving indicator outputs from validated input data.
- `scoring`: the system is producing category scores and the aggregate Market xG score.
- `generating_report`: the system is building the final user-facing report output.
- `ready`: the analysis completed successfully and the result is available to view.
- `failed`: the system hit an unrecoverable error and could not finish the analysis.
- `needs_user_attention`: the system cannot continue until the user chooses a symbol, uploads
  data, or fixes an input problem.

## High-Level Analysis Flow

`User search -> asset selection -> data source selection or data availability check -> data
loading -> validation -> indicator calculation -> category scoring -> Market xG aggregation ->
report generation -> result display`

The existing engine begins only after valid OHLCV data is available. Asset search, symbol
resolution, data-provider access, and watchlist persistence are future layers around the
existing engine.

## Asset Identity Reference

Asset analysis must start from a selected asset identity. Symbol resolution happens before data
loading. If symbol resolution is ambiguous, analysis should not proceed automatically.

The selected asset identity should travel through the analysis and watchlist workflow so result
displays can show symbol, exchange, currency, and source consistently. See
`docs/product/asset_identity_and_symbol_resolution.md`.

## Real Data Provider Reference

Real data provider strategy is the intended data path for asset analysis. Manual CSV import is
out of current scope. Provider fetching happens after asset identity is selected and before
validation and indicator calculation. See
`docs/product/real_market_data_provider_strategy.md`.

## Watchlist Item Concept

This is a future product contract only. No storage or scheduling is implemented in this ticket.

- `asset_identity`
- `status`
- `last_analysis_at`
- `last_market_xg_score`
- `last_interpretation`
- `missing_categories`
- `last_error`
- `next_refresh_at`

## Result Display Requirements

A completed result should show:

- asset display name
- symbol
- exchange
- currency
- Market xG score
- interpretation
- category scores
- strengths
- weaknesses
- missing categories
- data source
- analysis timestamp
- disclaimer / limitation text

## Prediction Wording Decision

Users may think of the output as a market-quality forecast or directional support, but product
language should avoid promising exact price prediction.

Preferred language:

- Analyze Market Quality
- Run Market xG
- Market quality outlook
- Probabilistic decision support

Avoid language:

- Guaranteed prediction
- Guaranteed return
- Exact future price target

## Indicator Quality Decision

The usefulness of Market xG depends on the quality, independence, and calibration of its
indicators and category scores. More indicators are not automatically better. Future indicator
work should prioritize independent market-quality dimensions over duplicate technical signals.

Important future market-quality dimensions may include:

- trend
- momentum
- volume
- breadth
- volatility / sentiment
- macro / rates
- valuation
- earnings / fundamentals
- liquidity / flows

Backtesting and calibration are future work and must not be described as already implemented.

## Explicit Non-Goals

- No UI implemented yet.
- No asset search implemented yet.
- No live data fetching implemented yet.
- No watchlist storage implemented yet.
- No scheduled refresh implemented yet.
- No backtesting implemented yet.
- No investment advice.
- No guaranteed prediction.
