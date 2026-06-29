# ADR-002: S&P 500 First

## Status

Accepted

## Context

The MVP needs clean historical data and a simple validation path. Adding VUSA immediately would introduce fund-specific behavior, EUR pricing, currency effects, and European investor considerations.

## Decision

Start with S&P 500 before VUSA.

## Consequences

Using the S&P 500 first keeps the MVP focused on market quality scoring with cleaner historical data. VUSA can be added later as an investor layer after the core scoring engine is validated.

