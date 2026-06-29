# ADR-001: Rule-Based Scoring First

## Status

Accepted

## Context

Market xG must be explainable, testable, and easy to validate before more advanced modeling is introduced. Early users need to understand why a score changed and which inputs drove the result.

## Decision

Start with rule-based scoring before machine learning.

## Consequences

Rule-based scoring improves explainability, makes debugging easier, and supports clearer QA validation. It may be less adaptive than machine learning at first, but it creates a transparent foundation that can be tested historically before adding model complexity.

