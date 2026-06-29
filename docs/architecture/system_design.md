# System Design

## High-Level Flow

Data ingestion
-> Raw data storage
-> Processed data
-> Indicator calculation
-> Category scoring
-> Market xG aggregation
-> Confidence calculation
-> Narrative generation
-> Report generation
-> Backtest validation

## Components

### data_providers

Fetches or loads external market, macro, fundamental, fund flow, sentiment, and price data. The initial implementation should favor simple local files.

### indicators

Calculates reusable market indicators such as moving averages, momentum measures, breadth metrics, volatility measures, and valuation inputs.

### scoring

Normalizes indicators into 0 to 100 scores, calculates category scores, applies weights, and produces the final Market xG score.

### backtesting

Applies historical scores to past data, calculates forward returns and drawdowns, and groups outcomes by score bucket.

### narratives

Turns scores, category movements, and important drivers into concise human-readable explanations.

### reports

Generates markdown reports containing the Market xG score, category scores, confidence score, market state, explanation, and backtest results.

### config

Stores category weights, score thresholds, input paths, reporting settings, and other tunable parameters.

### utils

Contains shared helpers for validation, date handling, file operations, and common calculations.

