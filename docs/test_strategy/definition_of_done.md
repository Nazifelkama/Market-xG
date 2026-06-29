# Definition of Done

## Purpose

The Definition of Done is the quality gate for accepting Market xG work. Generated code is not
automatically Done. Documentation is not Done just because a file exists. A ticket is Done only
after review, passing checks, and merge to main.

## Global Definition of Done

A ticket is Done only when:

- Scope is implemented exactly as requested.
- Acceptance criteria are satisfied.
- Relevant automated tests are added or updated.
- Relevant local checks pass before review.
- Full CI passes before merge.
- Documentation is updated when behavior, architecture, process, or user-facing output changes.
- No unrelated scope is added.
- No silent failures are introduced.
- Completion report is provided.
- Human review is completed.
- Work is merged to main.
- Ticket status is updated to Done after merge.

## Documentation Ticket DoD

- Required documents are created or updated.
- Links between related docs are added where useful.
- Terminology is consistent with glossary.
- Tests verify important documentation files exist or contain required sections.
- No implementation logic is added.
- Relevant documentation tests pass before review.
- Full CI passes before merge.

## Code Ticket DoD

- Code is implemented inside the correct package/module.
- Public functions have clear names and type hints.
- Unit tests cover normal and edge cases.
- Integration tests are added when workflow behavior changes.
- Errors are meaningful.
- No silent fallback hides invalid data.
- New dependencies are justified.
- Relevant code tests pass before review.
- Full CI passes before merge.

## Data Ticket DoD

- Data source is documented.
- Required columns are validated.
- Missing data handling is explicit.
- Duplicate dates are detected.
- Invalid values are rejected or clearly handled.
- Raw data and processed data responsibilities are clear.
- Data quality tests are added.
- Relevant data tests pass before review.
- Full CI passes before merge.

## Scoring Ticket DoD

- Score output is always between 0 and 100.
- Scoring direction is documented.
- Thresholds are documented.
- Tests cover low, medium, and high score cases.
- Missing inputs lower confidence or raise meaningful errors.
- No category silently receives a fake score.
- Relevant scoring tests pass before review.
- Full CI passes before merge.

## Backtest Ticket DoD

- No lookahead bias.
- Forward return windows are documented.
- Sample size is reported.
- Score buckets are documented.
- Edge cases around incomplete future windows are tested.
- Backtest assumptions are documented.
- Relevant backtest validation tests pass before review.
- Full CI passes before merge.

## Report / Narrative Ticket DoD

- Report includes score, confidence, category scores, strengths, weaknesses, and interpretation where relevant.
- Narrative is consistent with numeric scores.
- Snapshot or content tests are added where useful.
- Report does not claim certainty or exact price prediction.
- Relevant report tests pass before review.
- Full CI passes before merge.

## Completion Report DoD

Codex must provide:

- Ticket ID.
- Changed files.
- Summary of changes.
- Relevant checks run.
- Test results.
- Assumptions or limitations.
- Confirmation no unrelated scope was added.
- Confirmation whether commit was created.
- Confirmation whether branch was pushed.
- Commit hash, if committed.
- PR link, if opened.

## Not Done Examples

- Code works locally but relevant tests were not run.
- Documentation exists but required sections are missing.
- Ticket status was marked Done before merge.
- Report looks good but calculations are untested.
- Backtest uses future data accidentally.
- Score can exceed 100 or fall below 0.
- Codex implemented an improvement outside ticket scope without approval.
- Missing data is silently treated as valid data.

