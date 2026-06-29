# MXG-026 — Add Volume / Accumulation Category to Sample Pipeline

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Volume / Accumulation
Type: Test / Integration
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-021 created the deterministic sample pipeline integration test around the Trend and
Momentum category only. MXG-024 and MXG-025 introduced the first Phase 2 volume primitives and
the Volume / Accumulation scorer, so the sample integration path should now prove both
implemented categories work together.

## Goal

Extend the existing sample pipeline integration test to include the Volume / Accumulation
category.

## Scope

- Update `tests/integration/test_phase_1_sample_pipeline.py`.
- Add this ticket file under `docs/tickets/phase-2/`.

## Out of Scope

- Renaming the integration test file.
- Production pipeline modules, CLI commands, dashboards, or charts.
- Live data fetching or external dependencies.
- Changes to scoring rules, indicator formulas, aggregation weights, or fixture data.
- README or architecture documentation updates.

## Implementation Instructions

- Continue using the deterministic local fixture only.
- Extract both close prices and volumes from validated rows.
- Calculate volume indicators outside the Volume / Accumulation scorer.
- Calculate `price_change_20d` outside the scorer.
- Convert both category scorers into `CategoryScore` objects and aggregate exactly two
  implemented categories.
- Assert presence and range behavior rather than exact final Market xG values.

## Acceptance Criteria

- `tests/integration/test_phase_1_sample_pipeline.py` includes Volume / Accumulation in the
  sample pipeline.
- The integration test file is not renamed.
- Test still uses deterministic local fixture only.
- Test extracts close prices and volumes from validated rows.
- Test calculates volume indicators outside the volume scorer.
- Test calculates `price_change_20d` outside the volume scorer.
- Test calculates Volume / Accumulation score.
- Test converts `VolumeAccumulationScore` into `CategoryScore` with name
  `volume_accumulation`.
- Test aggregates exactly two implemented categories: `trend_momentum` and
  `volume_accumulation`.
- Test verifies `MarketXGScore` contains both implemented categories.
- Test verifies `weights_used` sums to `1.0` using `pytest.approx`.
- Test verifies markdown report includes readable `Volume Accumulation`.
- Test does not assert an exact final Market xG score.
- Test does not fetch live data.
- Test does not write report output to disk.
- Test does not introduce external dependencies.
- Existing scoring rules, indicator formulas, aggregation weights, and fixture data are not
  changed.
- No production source module is created.
- README and architecture documentation are not updated in this ticket.

## Test Requirements

- Run `pytest tests/integration/test_phase_1_sample_pipeline.py`.
- Run `ruff check tests/integration/test_phase_1_sample_pipeline.py`.
- Run `mypy tests/integration/test_phase_1_sample_pipeline.py`.
- Do not run unrelated checks unless scope changes.

## Definition of Done

- Integration test changes and ticket documentation are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant local checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- The sample pipeline remains a composition test, not a production pipeline.
- The integration path now proves the first two implemented categories can coexist without
  changing the broader aggregation or reporting architecture.
