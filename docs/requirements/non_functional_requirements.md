# Non-Functional Requirements

## Explainability

Scores shall be traceable to their input indicators, category scores, weights, and narrative explanations.

## Reproducibility

Given the same input data and configuration, the system shall produce the same outputs.

## Testability

Core calculations, score normalization, data validation, and report generation shall be testable with deterministic fixtures.

## Maintainability

The system shall use simple module boundaries, clear configuration, and readable logic so future categories and indicators can be added safely.

## No Silent Failures

Missing, invalid, stale, or inconsistent data shall be surfaced clearly instead of being treated as valid.

## Simple Local-First Execution

The MVP shall run locally with simple file-based inputs and outputs before adding infrastructure complexity.

## Data Quality Checks

The system shall validate input completeness, date alignment, numeric ranges, and unexpected missing values before producing scores.

