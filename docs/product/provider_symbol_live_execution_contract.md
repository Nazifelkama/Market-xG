# Provider-Symbol Live Execution Contract

## Purpose

Technical UAT validated the already-fetched provider-analysis path. The next step is direct
provider-symbol based live execution, where a caller supplies a provider-specific symbol such as
`AAPL.US`, `NVDA.US`, or another provider symbol and receives a Market xG result.

This contract defines how direct provider symbols will be handled before full user-friendly asset
search and symbol resolution exist.

Provider-symbol execution is an interim technical and product milestone. It is not the final
product experience. The final product goal remains user-friendly asset search, selected asset
identity, and explicit symbol resolution before analysis.

## Current Position

The completed provider-analysis path is:

`Already-fetched StooqHistoricalResponse -> Stooq normalization -> OHLCV validation -> indicator
calculation -> Trend / Momentum score -> Volume / Accumulation score -> Market xG aggregation ->
markdown report`

The next intended provider-symbol path is:

`provider_symbol input -> live provider fetch -> provider parser -> provider-based analysis
orchestrator -> ProviderAnalysisResult -> markdown report`

## Provider-Symbol Input Contract

Provider-symbol live execution v0.1 should accept these required fields:

- `provider`
- `provider_symbol`
- `asset_name`
- `report_date`

Optional or future fields:

- `selected_asset_identity`
- `exchange`
- `currency`
- `requested_start_date`
- `requested_end_date`
- `interval`
- `user_notes`

Input rules:

- `provider` must be explicit.
- v0.1 provider is expected to be `stooq`.
- `provider_symbol` must be explicit and non-empty.
- `asset_name` must be explicit and non-empty.
- `report_date` must be supplied by the caller for deterministic behavior.
- `interval` v0.1 is daily only.
- The analysis core must not generate current timestamps internally.
- Direct `provider_symbol` input is accepted as an interim milestone only.

## Output Contract

A successful provider-symbol execution should return:

- `provider`
- `provider_symbol`
- `asset_name`
- `report_date`
- Market xG score
- implemented category scores
- missing categories
- markdown report
- key details or diagnostics

The output should preserve `provider` and `provider_symbol`. It should not hide missing future
categories. The markdown report should continue to include safe disclaimer wording.

## Failure Contract

Provider-symbol execution should fail explicitly instead of silently producing misleading output.

| Failure category | Meaning | Status guidance | Example user-facing message |
| --- | --- | --- | --- |
| `invalid_request` | Required request fields are missing or malformed. | `needs_user_attention` | The analysis request is missing required information. |
| `unsupported_provider` | The requested provider is not supported by v0.1. | `failed` or `needs_user_attention`, depending on product context | This data provider is not supported yet. |
| `invalid_provider_symbol` | The provider symbol is empty, malformed, or not usable for the selected provider. | `needs_user_attention` | Check the provider symbol and try again. |
| `provider_network_error` | The provider request could not complete because of network or provider availability. | `failed` | Market data could not be fetched right now. |
| `provider_parse_error` | The provider response could not be parsed into the expected raw response shape. | `failed` | Market data was returned in an unexpected format. |
| `provider_no_data` | The provider returned no usable rows for the requested symbol and date range. | `needs_user_attention` or `failed` | No market data was found for this provider symbol. |
| `provider_data_validation_error` | Normalized OHLCV rows failed the Market xG data contract. | `failed` | Market data failed validation and cannot be analyzed. |
| `insufficient_history` | Valid data exists, but there are too few rows for the implemented indicators. | `needs_user_attention` | There is not enough historical data to calculate Market xG. |
| `analysis_error` | Indicator, scoring, aggregation, or report generation failed. | `failed` | Market xG analysis could not be completed. |
| `unknown_error` | An unexpected error occurred. | `failed` | An unexpected error occurred while running Market xG. |

## Status Mapping

The intended status flow is:

`idle -> fetching_data -> validating_data -> calculating_indicators -> scoring ->
generating_report -> ready`

Failure statuses:

- `failed`
- `needs_user_attention`

Persisted status storage is not implemented yet. This contract only defines intended status
behavior. MXG-039 may return a success result or failure object, but should not implement full
persisted status unless separately scoped.

## Live Execution and CI Boundary

- Provider-symbol live execution may perform live network calls when explicitly invoked.
- Unit tests and CI must not depend on live provider calls.
- Tests should mock provider fetch responses.
- Manual live verification must be separate from CI.
- Real provider symbol verification should be recorded separately.

## Provider Symbol Verification

Candidate symbols such as `AAPL.US`, `NVDA.US`, `ASML.NL`, or `VUSA.NL` must be treated as
candidates until verified. This contract does not claim that any provider symbol is guaranteed.

Symbol verification belongs to manual live verification or provider coverage documentation. Direct
provider-symbol execution must not become a hard-coded `VUSA`-only path.

## Relationship to Asset Identity

`provider_symbol` is provider-level. Asset identity is product-level. Full asset search and symbol
resolution are future product layers.

Direct provider-symbol execution must still preserve enough metadata to later map a result back to
selected asset identity. In v0.1, `asset_name` is caller-provided.

## Product Trust and Safety Wording

Provider-symbol live execution must not present Market xG as guaranteed price prediction. Reports
must retain safe disclaimer wording. Missing categories must remain visible.

Failures should be explicit rather than silently producing misleading output.

## Known Limitations

- No full user-friendly search yet.
- No symbol resolution yet.
- No UI yet.
- No watchlist or scheduled refresh yet.
- No persisted status yet.
- No provider fallback yet.
- No real symbol verification in this ticket.
- Only two Market xG categories are currently implemented.
- No backtesting or calibration yet.
- No FX conversion.
- No `adjusted_close` decision implemented.

## Next Implementation Step

The next likely ticket is MXG-039: Implement Provider-Symbol Analysis Service v0.1.

MXG-039 should use mocked tests and no live-provider-dependent CI. Manual live Stooq verification
should remain a separate follow-up.
