# Ticket Documentation

Market xG stores implementation tickets in the repository for traceability. The ticket files
preserve the original intent behind each change, make Codex prompts version-controlled, and
give QA a concrete source to compare against pull request changes.

Each ticket should be Codex-ready. Tickets are not just summaries; they are implementation
instructions with scope, acceptance criteria, test requirements, and definition of done.

Pull requests should reference the relevant ticket file so reviewers can connect the code,
documentation, tests, and decisions back to the planned work.

Ticket status should be updated as work progresses. Keep ticket files grouped by sprint so the
project history remains easy to scan.

## Scope and Status

Tickets are the source of implementation scope. Codex must not implement outside ticket scope.
If a useful idea appears while working, it should be proposed as a follow-up ticket instead of
being added silently.

Ticket status must follow:

- Not Started
- In Progress
- In Review
- Done

A ticket becomes Done only after merge to main. Pull requests should reference the relevant
ticket file so reviewers can trace the implementation back to the original instructions.

## Local Checks and Commit Workflow

Ticket work should follow `docs/product/local_checks_and_commit_workflow.md`. Codex should wait
for approval before commit/push. Local checks may be scoped to the ticket, while full CI remains
the final automated quality gate before merge.

## Definition of Done

Every ticket should be evaluated against `docs/test_strategy/definition_of_done.md`.
Ticket-specific Definition of Done may add stricter requirements. A ticket becomes Done only
after the global Definition of Done is satisfied.

## Roadmap Traceability

Tickets should trace back to a roadmap phase and epic. Roadmap changes follow
`docs/product/roadmap_governance.md`. New ideas should be parked before they become
implementation tickets.

Phase 1 data tickets that depend on OHLCV input should reference
`docs/architecture/market_data_contract.md`.
