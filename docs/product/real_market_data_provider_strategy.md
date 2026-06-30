# Real Market Data Provider Strategy

## Purpose

Market xG needs a real market data provider path so users can analyze real assets without
manually importing CSV files. Provider integration should support the product workflow from a
selected asset identity to a final Market xG result.

This document defines strategy only. It does not implement provider code.

## Product Flow

`User search -> candidate asset identities -> user selects asset identity -> provider symbol is
resolved -> provider fetches historical market data -> data is normalized into Market xG rows ->
data is validated -> indicators are calculated -> category scores are calculated -> Market xG is
aggregated -> report or result is displayed`

MXG-030 owns the asset identity and symbol resolution contract. This document focuses on the
provider data path after or alongside asset identity selection.

## Provider Direction

- Stooq is the first real market data provider candidate.
- Stooq should be treated as a provider candidate, not as a permanent exclusive provider.
- Provider architecture should allow additional providers later.
- The product should not be hard-coded to one provider forever.
- The product should not be hard-coded to VUSA.

## CSV Decision

- Manual CSV import is out of current scope.
- Current product direction prioritizes provider-based real market data.
- CSV import should not be described as part of the current implementation path.

## Asset Coverage Strategy

The product goal is to support any asset that can be resolved and fetched by the provider layer.
Examples include:

- Apple / US equity
- Nvidia / US equity
- ASML / Netherlands or another supported listing
- VUSA / Netherlands or another supported ETF listing
- Tesla / US equity
- S&P 500 or another supported index or instrument if provider data is available

These examples are non-binding and must not become a hard-coded supported-symbol list. If a
provider cannot resolve or fetch a selected asset, the product should enter
`needs_user_attention` or `failed`.

## Provider-Symbol MVP Versus Product Search

Product target:

- user-friendly search such as `Apple`, `VUSA`, `ASML`, or `Nvidia`
- candidate assets shown when a query is ambiguous

Possible technical MVP:

- start with direct provider symbols if provider search is not implemented yet
- provider-symbol entry is a technical stepping stone, not the final product experience
- direct provider symbols must still map to explicit asset identity metadata before analysis

## Stooq Symbol Candidates and Assumptions

Stooq uses provider-specific symbol formats. Candidate provider symbols may include:

- `AAPL.US` for Apple, if supported by Stooq
- `NVDA.US` for Nvidia, if supported by Stooq
- `ASML.NL` or another provider-specific symbol for ASML Netherlands, depending on Stooq coverage
- `VUSA.NL` or another provider-specific symbol for VUSA Netherlands or EUR, depending on Stooq
  coverage

These are provider-symbol candidates only. Provider symbols must be verified during
implementation. This document does not claim that `VUSA.NL`, `ASML.NL`, `AAPL.US`, `NVDA.US`, or
any specific Stooq symbol is guaranteed until verified by provider implementation.

## Asset Identity and Provider Mapping

Selected asset identity is product-level. Provider symbol is provider-level. A selected asset
may have different provider symbols across providers.

The provider layer must preserve:

- selected asset identity
- provider name
- provider symbol
- exchange, currency, and source metadata when available

The engine should not silently analyze data that conflicts with the selected asset identity.

## Real Data Normalization Target

Provider data should normalize into existing Market xG OHLCV-compatible rows:

- `date`
- `open`
- `high`
- `low`
- `close`
- `volume`

Recommended metadata:

- `symbol`
- `provider_symbol`
- `display_name`
- `exchange`
- `currency`
- `source`
- `fetched_at`

Adjusted close decision:

- `adjusted_close` may be available from some providers
- the existing engine currently uses `close`
- future work may decide whether `adjusted_close` should be used for return and momentum
  calculations
- this document does not claim that `adjusted_close` is already wired into the engine

## Currency and Exchange Handling

- Currency and exchange must be explicit where available.
- The engine must not silently mix USD, EUR, or GBP series.
- No FX conversion is implemented yet.
- If provider metadata conflicts with selected asset identity, the product should enter `failed`
  or `needs_user_attention`.

## Network and Reliability Strategy

- Provider calls can fail.
- Provider data can be missing, delayed, malformed, or incomplete.
- Network failures should map to `failed`.
- Missing provider symbol or ambiguous provider mapping should map to `needs_user_attention`.
- Malformed provider data should map to `failed`.
- Conflicting exchange or currency metadata should map to `failed` or `needs_user_attention`.
- The user should receive a clear failure reason.

## CI and Testing Strategy

- CI must not depend on live provider calls.
- Unit tests should use mocked provider responses or deterministic fixtures.
- Integration tests involving live provider calls should be optional or manual unless a stable
  mocked or cached strategy exists.
- Provider implementation should separate network fetch from data normalization so normalization
  can be tested deterministically.
- Provider implementation should separate:
  - raw network fetch
  - raw response parsing
  - normalization into Market xG rows
  - validation handoff

## Data Freshness

- Provider results should expose or preserve `fetched_at`.
- Future product UI should show `last_analysis_at` and data source or freshness.
- Market xG should not pretend stale data is current.
- No scheduling or automatic refresh is implemented yet.

## Explicit Non-Goals

- No provider implementation in this ticket.
- No live data fetching in this ticket.
- No CSV import in current scope.
- No UI.
- No watchlist storage.
- No scheduled refresh.
- No backtesting.
- No FX conversion.
- No investment advice.
- No guaranteed prediction.
