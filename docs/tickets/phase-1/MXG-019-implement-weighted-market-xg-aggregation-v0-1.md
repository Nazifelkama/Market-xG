# MXG-019 — Implement Weighted Market xG Aggregation v0.1

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Scoring Engine
Type: Feature / Scoring Aggregation
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-018 introduced the first category score, Trend and Momentum. The next step is a small
aggregation layer that can combine available category scores into a top-level Market xG score
without inventing missing category values.

## Goal

Implement weighted Market xG aggregation v0.1 for Phase 1.

## Scope

- Add `src/market_xg/scoring/market_xg_score.py`.
- Add focused unit tests for category validation and aggregation behavior.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- New category scorers.
- Reports or live data fetching.
- Indicator calculation or CSV reading.
- External dependencies such as pandas or numpy.
- Flattening category strengths or weaknesses into top-level Market xG fields.

## Implementation Instructions

- Implement `CategoryScore` and `MarketXGScore` dataclasses with validation.
- Implement `calculate_market_xg_score(...)` using configured category weights.
- Reweight available categories when requested instead of inventing fake missing scores.
- Return aggregation details including raw and final score plus category counts.

## Acceptance Criteria

- `src/market_xg/scoring/market_xg_score.py` exists.
- `DEFAULT_CATEGORY_WEIGHTS` exists.
- `CategoryScore` dataclass exists.
- `MarketXGScore` dataclass exists.
- `calculate_market_xg_score(...)` exists.
- `CategoryScore` validates score bounds and list fields.
- `MarketXGScore` validates score bounds and required collection fields.
- Single available `trend_momentum` category can produce Market xG score.
- Multiple categories aggregate correctly.
- Missing categories are handled explicitly.
- Missing categories are not assigned fake scores.
- Unknown categories raise `ValueError`.
- Invalid weights raise `ValueError`.
- Score is always between 0 and 100.
- `MarketXGScore` does not expose top-level strengths or weaknesses fields.
- No reports, indicator calculation, live data fetching, or external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_market_xg_score.py`.
- Run `ruff check src/market_xg/scoring/market_xg_score.py tests/unit/test_market_xg_score.py`.
- Run `mypy src/market_xg/scoring/market_xg_score.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Aggregation code and tests are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Phase 1 aggregation prefers explicit missing-category handling over invented fallback scores.
- Reweighting available categories allows early partial-system scoring before every category
  scorer exists.
