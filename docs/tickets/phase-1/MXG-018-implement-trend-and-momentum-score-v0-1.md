# MXG-018 — Implement Trend and Momentum Score v0.1

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Scoring Engine
Type: Feature / Category Scoring
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-014, MXG-015, and MXG-016 implemented the first indicator families, and MXG-017 defined a
common indicator result contract. The next step is the first deterministic category score that
uses those indicator outputs without recalculating indicator values inside the scorer.

## Goal

Implement the Phase 1 Trend and Momentum score as a deterministic, rule-based category score.

## Scope

- Add `src/market_xg/scoring/trend_momentum_score.py`.
- Add focused unit tests for scoring rules, validation, and output structure.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Indicator calculation inside the scorer.
- Weighted Market xG aggregation.
- Reports or live data fetching.
- External dependencies such as pandas or numpy.

## Implementation Instructions

- Implement a frozen `TrendMomentumScore` dataclass with validation.
- Implement `calculate_trend_momentum_score(...)` using only passed indicator values.
- Start from a neutral base score of `50` and apply the documented v0.1 rule set.
- Clamp the final score to `0`-`100`.
- Return strengths, weaknesses, and a details dict with source inputs and derived booleans.

## Acceptance Criteria

- `src/market_xg/scoring/trend_momentum_score.py` exists.
- `TrendMomentumScore` dataclass exists.
- `calculate_trend_momentum_score(...)` exists.
- Strong trend case produces score >= 85.
- Weak trend case produces score <= 25.
- Missing optional inputs do not crash scoring.
- All optional indicators missing gives score == 50.
- Equality cases are neutral unless explicitly defined otherwise.
- Score is always between 0 and 100.
- `TrendMomentumScore` validates score bounds.
- Strengths and weaknesses are returned.
- Details dict contains key inputs, derived booleans, `raw_score_before_clamp`, and
  `final_score`.
- Invalid numeric inputs raise `ValueError`.
- No indicator calculation, aggregation, reports, live data fetching, or external
  dependencies are added.
- Scorer does not import or call indicator modules.

## Test Requirements

- Run `pytest tests/unit/test_trend_momentum_score.py`.
- Run `ruff check src/market_xg/scoring/trend_momentum_score.py tests/unit/test_trend_momentum_score.py`.
- Run `mypy src/market_xg/scoring/trend_momentum_score.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Scoring code and tests are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Phase 1 starts this category with explicit rules and transparent explanations instead of a
  learned or optimized model.
- The scorer stays decoupled from indicator calculation so later pipeline assembly can choose
  how indicator values are passed in.
