# Asset Identity and Symbol Resolution

## Purpose

Asset identity is the canonical representation of the asset the user selected. Symbol
resolution is the process of converting a user search query into one or more candidate asset
identities.

The system must not run Market xG analysis until a precise asset identity is selected. Example
assets in this document are non-binding documentation examples only. This document does not
define a hard-coded asset registry or a hard-coded supported-symbol list.

## Asset Identity Model

### Required Fields

- `symbol`
- `display_name`
- `exchange`
- `currency`
- `asset_type`

### Strongly Recommended Fields

- `data_source`
- `source_symbol`

### Optional Fields

- `isin`
- `country`
- `provider_metadata`

### Field Meanings

- `symbol`: internal symbol used by Market xG for the selected asset.
- `display_name`: human-readable asset name.
- `exchange`: exchange or venue, such as NASDAQ or Euronext Amsterdam.
- `currency`: trading currency, such as USD, EUR, or GBP.
- `asset_type`: equity, ETF, index, fund, crypto, or another supported type.
- `data_source`: source selected for data, such as Yahoo Finance manual CSV or a future
  provider connector.
- `source_symbol`: provider-specific symbol, such as `VUSA.AS` for Yahoo Finance.
- `isin`: optional identifier that can help disambiguate ETFs and funds.
- `country`: optional market or country context.
- `provider_metadata`: optional provider-specific fields.

## Search Result Behavior

A user search may return multiple candidates. In future implementation, search candidates should
be dynamic and may come from a provider, imported metadata, local cache, database, or another
source.

The examples in this document are not the only supported assets. The UI and product should show
enough information for the user to choose correctly. Search results should display:

- `display_name`
- `symbol`
- `exchange`
- `currency`
- `asset_type`
- `data_source` or source availability when known

The system should not auto-select an ambiguous result unless confidence is high and the user can
review it.

## Ambiguity Handling

If a query maps to multiple plausible assets, the product should enter `needs_user_attention`.
For example, if the user searches `VUSA`, the product should show candidates such as:

- `VUSA.AS / Euronext Amsterdam / EUR / ETF`
- `VUSA.L` or other non-Amsterdam listings if available from a provider

The product must not silently choose a different exchange or currency. If the user previously
selected a preferred listing, future UX may prioritize it, but that is future work.

## Non-Binding Example Asset Identities

These examples exist only to demonstrate the asset identity shape. They do not define a
hard-coded asset registry, and they do not imply that Market xG only supports these assets.
Future symbol resolution should return candidates dynamically from a provider, imported
metadata, local cache, database, or another source.

### Apple

- `symbol`: `AAPL`
- `display_name`: `Apple Inc.`
- `exchange`: `NASDAQ`
- `currency`: `USD`
- `asset_type`: `equity`
- `source_symbol`: `AAPL`

### Nvidia

- `symbol`: `NVDA`
- `display_name`: `NVIDIA Corporation`
- `exchange`: `NASDAQ`
- `currency`: `USD`
- `asset_type`: `equity`
- `source_symbol`: `NVDA`

### ASML Amsterdam

- `symbol`: `ASML.AS`
- `display_name`: `ASML Holding N.V.`
- `exchange`: `Euronext Amsterdam`
- `currency`: `EUR`
- `asset_type`: `equity`
- `source_symbol`: `ASML.AS`

### VUSA Amsterdam

- `symbol`: `VUSA.AS`
- `display_name`: `Vanguard S&P 500 UCITS ETF`
- `exchange`: `Euronext Amsterdam`
- `currency`: `EUR`
- `asset_type`: `ETF`
- `source_symbol`: `VUSA.AS`

## VUSA Decision

For the user's intended VUSA use case, the target identity is `VUSA.AS / Euronext Amsterdam /
EUR`. VUSA must not be treated as automatically equivalent to `SPY`, `SPX`, `VOO`, or a
London/GBP listing.

Market xG should analyze the selected tradable instrument or listing, not just the underlying
index idea. If the user searches `VUSA`, the product should show or confirm the listing and
currency before analysis.

## Currency Decision

Currency is part of asset identity. The engine should not silently mix USD, EUR, and GBP series.
No FX conversion is implemented yet.

If a selected asset is EUR-denominated, the input data should also be EUR-denominated unless a
future FX layer explicitly converts it. If imported data currency conflicts with the selected
asset identity, the system should require user attention or fail validation in future
implementation.

## Source Symbol Decision

`source_symbol` may differ by provider. For example, Yahoo Finance may use `VUSA.AS` for
Amsterdam, while future providers may use different formats. The internal asset identity should
preserve the provider-specific `source_symbol` used to fetch or import data.

The product should not assume that one symbol format works across all providers.

## Failure and Attention States

The product should enter `failed` or `needs_user_attention` for scenarios such as:

- no matching asset found
- multiple ambiguous matches
- selected asset has no available data source
- selected asset has unsupported currency
- selected asset has unsupported asset type
- selected asset data source returns incompatible data
- selected asset metadata conflicts with imported data
- selected asset exchange or currency does not match the user's intended listing

## Explicit Non-Goals

- No asset search implementation in this ticket.
- No provider integration in this ticket.
- No live data fetching in this ticket.
- No local CSV adapter in this ticket.
- No watchlist storage in this ticket.
- No UI in this ticket.
- No FX conversion in this ticket.
- No hard-coded asset registry in this ticket.
- No hard-coded supported-symbol list in this ticket.
- No investment advice.
- No guaranteed prediction.
