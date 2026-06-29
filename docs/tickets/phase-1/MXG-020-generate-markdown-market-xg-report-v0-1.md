# MXG-020 — Generate Markdown Market xG Report v0.1

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Reporting
Type: Feature / Report
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-018 introduced the first category score and MXG-019 introduced weighted Market xG
aggregation. The next step is a simple markdown report that turns deterministic scoring output
into readable text without recalculating any indicators or scores inside the report module.

## Goal

Generate a deterministic markdown Market xG report v0.1 from an existing `MarketXGScore`.

## Scope

- Add `src/market_xg/reports/markdown_report.py`.
- Add focused unit tests for markdown content and validation behavior.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Dashboards, charts, or end-to-end pipeline tests.
- Indicator or scoring calculation inside the report module.
- Live market data fetching.
- External dependencies such as pandas, numpy, or jinja2.

## Implementation Instructions

- Implement `generate_market_xg_markdown_report(...)` using only the provided inputs.
- Keep the output deterministic and readable.
- Include summary, interpretation, category scores, strengths, weaknesses, missing
  categories, method note, and disclaimer sections.
- Render category names in readable title-case form.

## Acceptance Criteria

- `src/market_xg/reports/markdown_report.py` exists.
- `generate_market_xg_markdown_report(...)` exists.
- Report includes summary, interpretation, category scores, strengths, weaknesses, missing
  categories, method note, and disclaimer.
- Report clearly says `Market xG is not price prediction.`
- Report clearly says `This report does not guarantee future returns or outcomes.`
- Report does not assign fake scores to missing categories.
- Category names are rendered in readable form.
- Strengths and weaknesses include category prefixes.
- Output is deterministic.
- Scores are displayed with one decimal place.
- Invalid inputs raise meaningful errors.
- No dashboard, charts, indicator calculation, scoring calculation, live data fetching, or
  external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_markdown_report.py`.
- Run `ruff check src/market_xg/reports/markdown_report.py tests/unit/test_markdown_report.py`.
- Run `mypy src/market_xg/reports/markdown_report.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Report code and tests are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- The Phase 1 report stays plain markdown so review and testing remain deterministic.
- Missing categories are called out explicitly instead of being hidden behind fallback scores.
