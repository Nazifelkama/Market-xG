# Roadmap Governance

## Purpose

This document defines how Market xG roadmap decisions are created, changed, approved, and
converted into work. The roadmap is versioned project memory. Roadmap changes should be
intentional, new ideas are captured before becoming tickets, and not every idea should become
immediate implementation work.

## Roadmap Levels

1. Vision: The long-term product direction and non-goals.
2. Phase: A major delivery period with a clear goal, entry criteria, and exit criteria.
3. Epic: A group of related tickets tied to a business or technical outcome.
4. Ticket: A scoped unit of work with acceptance criteria and test requirements.
5. Pull Request: A reviewed change set that implements one ticket.
6. Commit: A versioned record of approved changes.

## Phase Rules

- Each phase must have a clear goal.
- Each phase must have entry criteria.
- Each phase must have exit criteria.
- Phase 1 cannot start until Phase 0 is accepted.
- Later phases should not be implemented early unless explicitly approved.
- If a later-phase idea appears early, capture it as a future idea, not implementation.

## Epic Rules

- Epics group related tickets.
- Epics should have a business or technical outcome.
- Epics should not be too broad.
- Epics should be traceable to a phase.
- Epics may contain documentation, code, test, and validation work.

## Ticket Rules

- Every meaningful change needs a ticket.
- Tickets must live under `docs/tickets/`.
- Tickets must include scope and out-of-scope.
- Tickets must include acceptance criteria.
- Tickets must include test requirements.
- Tickets must not silently expand scope.
- Ticket IDs must be stable once created.
- One ticket equals one branch equals one pull request.

## Change Control

- Roadmap changes require human approval.
- Major changes should be documented in an ADR.
- Minor clarifications can be made directly in roadmap docs.
- If a change affects scope, phases, scoring philosophy, architecture, or data strategy, create or update an ADR.
- No roadmap change should be hidden inside an unrelated implementation PR.

## Future Ideas Parking Lot

- Ideas that are useful but not ready should go into a parking lot.
- Parking lot items are not commitments.
- Parking lot items can later be promoted into epics or tickets.
- Parking lot should be reviewed during roadmap planning.

## Roadmap Review Cadence

- Review roadmap after each sprint.
- Review roadmap after major backtest findings.
- Review roadmap after data source or architecture changes.
- Review roadmap before starting a new phase.

## Traceability

Work should be traceable across the full delivery chain:

Vision → Phase → Epic → Ticket → PR → Commit

## Done Criteria for Roadmap Changes

A roadmap change is complete when:

- The relevant roadmap document is updated.
- Related tickets are created or updated if needed.
- ADR is created or updated if the decision is significant.
- Tests for required documentation are updated if applicable.
- Review report is provided.
- Relevant local checks pass before review.
- Full CI passes before merge.

