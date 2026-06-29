# MXG-025 — Implement Volume / Accumulation Score v0.1

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Volume / Accumulation
Type: Feature / Category Scoring
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-024 added the first reusable volume indicator utilities for Phase 2. The next step is the
second Market xG category score, Volume / Accumulation, using externally calculated inputs
without pulling indicator calculations into the scorer itself.

## Goal

Implement a deterministic, rule-based Volume / Accumulation score for Phase 2.

## Scope

- Add `src/market_xg/scoring/volume_accumulation_score.py`.
- Add focused unit tests for rule behavior, validation, and detail output.
- Add this ticket file under `docs/tickets/phase-2/`.

## Out of Scope

- Volume indicator calculation inside the scorer.
- Market xG aggregation weight changes.
- Phase 1 end-to-end pipeline changes.
- Reports, live data fetching, or external dependencies.

## Implementation Instructions

- Implement a frozen `VolumeAccumulationScore` dataclass with validation.
- Implement `calculate_volume_accumulation_score(...)` using only provided primitive inputs.
- Start from a neutral base score of `50` and apply the documented v0.1 rule set.
- Return strengths, weaknesses, and a details dict with source inputs and derived booleans.
- Keep the scorer independent from `volume.py`.

## Acceptance Criteria

- `src/market_xg/scoring/volume_accumulation_score.py` exists.
- `VolumeAccumulationScore` dataclass exists.
- `calculate_volume_accumulation_score(...)` exists.
- Score is deterministic and rule-based.
- Missing optional inputs do not crash scoring.
- All optional inputs missing gives score == 50.
- Strengths and weaknesses are returned.
- Details dict contains key inputs, derived booleans, raw_score, and final_score.
- Invalid numeric inputs raise `ValueError`.
- `bool` values are rejected as numeric inputs.
- Scorer does not calculate `price_change_20d`.
- Scorer does not import or call volume indicator module.
- No Market xG aggregation weights are modified.
- No pipeline, reports, live data fetching, or external dependencies are added.

## Test Requirements

- Run `pytest tests/unit/test_volume_accumulation_score.py`.
- Run `ruff check src/market_xg/scoring/volume_accumulation_score.py tests/unit/test_volume_accumulation_score.py`.
- Run `mypy src/market_xg/scoring/volume_accumulation_score.py tests/unit/test_volume_accumulation_score.py`.
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

- Phase 2 scoring continues the same pattern as Phase 1 category scorers: deterministic rules,
  explicit detail outputs, and no indicator calculations inside scoring modules.
- Volume / Accumulation scoring stays independent from the aggregation layer so later tickets
  can integrate it deliberately.
