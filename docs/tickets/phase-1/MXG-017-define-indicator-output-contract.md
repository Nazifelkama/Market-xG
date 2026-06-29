# MXG-017 — Define Indicator Output Contract

Status: In Progress
Sprint: Sprint 1
Phase: Phase 1
Epic: Indicator Engine
Type: Design / Indicator Contract
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-29
Updated: 2026-06-29

## Context

MXG-014, MXG-015, and MXG-016 introduced the first indicator calculation helpers for moving
average, momentum, and drawdown. Before scoring starts, the repository needs a small common
output contract so indicator availability and values can be consumed in a consistent way.

## Goal

Define a lightweight Phase 1 indicator output model with explicit availability semantics.

## Scope

- Add `src/market_xg/indicators/models.py`.
- Add focused unit tests for valid and invalid indicator result combinations.
- Add this ticket file under `docs/tickets/phase-1/`.

## Out of Scope

- Refactoring existing indicator calculation functions.
- Scoring or reporting logic.
- Live market data fetching.
- External dependencies such as pandas, numpy, or pydantic.
- Extra fields such as `as_of_date`, `metadata`, `category`, or `source`.

## Implementation Instructions

- Implement a frozen `IndicatorResult` dataclass with `name`, `value`, `available`, and
  `reason`.
- Enforce valid available/unavailable combinations in `__post_init__`.
- Add helper constructors for available and unavailable indicators.
- Provide `to_dict()` with exactly `name`, `value`, `available`, and `reason`.

## Acceptance Criteria

- `src/market_xg/indicators/models.py` exists.
- `IndicatorResult` dataclass exists.
- `available_indicator` helper exists.
- `unavailable_indicator` helper exists.
- `to_dict` exists and returns exactly `name`, `value`, `available`, `reason`.
- Invalid `IndicatorResult` combinations raise `ValueError`.
- Negative values are allowed for available indicators.
- `IndicatorResult` is immutable.
- Existing indicator calculation functions are not refactored.
- Tests cover valid and invalid cases.
- No scoring, reports, live data fetching, or external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_indicator_models.py`.
- Run `ruff check src/market_xg/indicators/models.py tests/unit/test_indicator_models.py`.
- Run `mypy src/market_xg/indicators/models.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Contract code and tests are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- The Phase 1 contract keeps availability explicit instead of overloading `None` alone.
- The initial model stays intentionally small so later tickets can add broader reporting or
  scoring context only when needed.
