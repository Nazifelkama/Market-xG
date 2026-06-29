# MXG-027 — Phase 2 Documentation Alignment for Volume Category

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Documentation
Type: Documentation / Alignment
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-024 implemented volume indicator utilities, MXG-025 implemented the Volume / Accumulation
category score, and MXG-026 added that category to the sample integration pipeline. The
documentation should now reflect the current two-category Phase 2 state without implying live
data support, backtesting, or direct accumulation/distribution labeling.

## Goal

Align the Phase 2 documentation with the currently implemented Volume / Accumulation category
work.

## Scope

- Update `README.md`.
- Update `docs/architecture/scoring_model.md`.
- Add this ticket file under `docs/tickets/phase-2/`.

## Out of Scope

- Production source-code changes.
- Test changes.
- Changes to scoring rules, indicator formulas, aggregation weights, or fixture data.
- Live data fetching, external dependencies, or new features.
- Detailed future tickets, dates, milestones, or implementation plans.

## Documentation Updates

- State clearly that the implemented category scores are Trend / Momentum and Volume /
  Accumulation.
- Describe the updated deterministic sample pipeline with both category scores.
- Summarize the current Volume / Accumulation implementation at a high level.
- State clearly that remaining categories are still missing or future categories.
- State clearly that missing categories are not assigned fake scores.
- Reaffirm that data is still synthetic/local only and scoring remains heuristic and not
  backtested.
- Keep future direction high level only.

## Acceptance Criteria

- Only allowed documentation or ticket files are changed.
- Documentation accurately states that Trend / Momentum and Volume / Accumulation are
  implemented category scores.
- Documentation accurately describes the updated sample pipeline with volume indicators and
  Volume / Accumulation score.
- Documentation clearly states remaining categories are still missing or future categories.
- Documentation clearly states missing categories are not assigned fake scores.
- Documentation clearly states Volume / Accumulation does not directly infer
  accumulation/distribution labels from indicators.
- Documentation clearly states fixture data is synthetic/local and not for financial
  conclusions.
- Documentation clearly states scoring is heuristic and not backtested/calibrated.
- Documentation clearly states Market xG is not price prediction.
- Documentation does not claim live data, backtesting, production pipeline, dashboard, or real
  investment decision support exists.
- Suggested future direction is documented only at a high level.
- No production source code is changed.
- No tests are changed.
- No scoring rules, indicator formulas, fixture data, live data fetching, or external
  dependencies are added.
- No executable examples or new usage snippets are added.
- No detailed future tickets, dates, milestones, or implementation plans are created.

## Test / Check Requirements

- Run `git diff --check`.
- Run any existing markdown-specific lint only if it is already configured.
- Do not run the full test suite unless documentation changes require it.

## Definition of Done

- Documentation changes are complete within ticket scope.
- Acceptance criteria are satisfied.
- Relevant lightweight checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- The documentation should describe the implemented two-category Phase 2 state directly rather
  than hinting at unsupported live-data or calibrated behavior.
- Volume / Accumulation is described as a rule-based score built on deterministic indicator
  inputs, not as direct accumulation/distribution labeling.
