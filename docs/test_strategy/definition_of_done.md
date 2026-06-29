# Definition of Done

A ticket is done when the implementation, tests, and documentation are ready for review and
the project remains safe to extend.

## Required Checks

- Code implemented.
- Unit tests added.
- Integration tests added where relevant.
- Docs updated.
- No silent failures.
- Meaningful errors.
- All acceptance criteria passed.
- pytest passes.
- ruff passes.
- mypy passes.
- No lookahead bias for backtest-related tickets.
- Sample outputs stored or documented where useful.

## Notes

Backtest-related work must explicitly separate scoring-time inputs from future outcome
measurements. Reports must be readable, but correctness of calculations is the priority.

