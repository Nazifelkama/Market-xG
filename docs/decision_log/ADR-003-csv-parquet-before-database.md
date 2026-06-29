# ADR-003: CSV/Parquet Before Database

## Status

Accepted

## Context

The early project needs simple local development, easy inspection of data, and fast iteration on scoring and validation. A database would add operational overhead before the data model and workflows are stable.

## Decision

Use CSV/Parquet before database storage.

## Consequences

CSV and Parquet files keep the MVP simple, local-first, and easy to inspect. This approach may need stronger file organization and validation discipline, but it avoids premature infrastructure complexity.

