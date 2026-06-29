# Way of Working

## Purpose

This document defines how the Market xG team works, reviews, commits, and accepts work. It
keeps product direction, QA expectations, implementation scope, and review decisions traceable
as the project moves from foundation into implementation.

## Roles

### Product Owner / PM

The human owner responsible for product direction, priority, scope decisions, and final
acceptance.

### QA

The human reviewer responsible for acceptance criteria, test thinking, quality risks, and
reviewing whether the delivered work matches the ticket.

### Dev Agent

Codex is the Dev Agent. Codex is responsible for implementation inside ticket scope, running
local checks, reporting results, and calling out assumptions or limitations.

### Architecture / Analysis Partner

ChatGPT is the Architecture / Analysis Partner. ChatGPT supports system design, ticket
refinement, tradeoff analysis, and review preparation.

## Core Rules

- One ticket equals one branch equals one pull request.
- No direct pushes to main.
- No work without a ticket.
- No market logic unless the ticket explicitly asks for it.
- Codex must not silently expand scope.
- Every meaningful change must be traceable to a ticket file under `docs/tickets/`.
- A ticket is not Done just because code was generated.

## Ticket Lifecycle

### Not Started

The ticket exists but work has not begun.

### In Progress

Implementation or documentation work is happening.

### In Review

Work is complete locally and awaiting PR review / CI.

### Done

Work is merged to main after review and passing CI.

Ticket status can move to Done only when the Definition of Done is satisfied. The project-wide
Definition of Done is documented in `docs/test_strategy/definition_of_done.md`.

## Standard Workflow

1. Pick one ticket.
2. Create a branch from latest main.
3. Implement only the ticket scope.
4. Run local checks.
5. Commit changes.
6. Open PR.
7. CI runs.
8. QA/PM reviews.
9. Address feedback.
10. Merge only after approval and green CI.
11. Update ticket status to Done after merge.

## Completion Report

Codex must provide:

- Changed files.
- Summary of changes.
- Commands run.
- Test results.
- Commit hash, if committed.
- PR link, if opened.
- Assumptions or limitations.
- Confirmation that no unrelated scope was added.

## Local Checks and Commit Workflow

Codex provides a review report before commit. Relevant local checks are enough before review
when they match the ticket scope and risk. Full CI checks happen on PR before merge. Codex waits
for human approval before commit/push.

## Scope Control

If Codex sees a useful improvement outside the ticket, it should mention it as a suggestion,
not implement it. New ideas should become new tickets. Implementation tickets should not modify
product philosophy unless explicitly requested.

Roadmap and scope changes should follow roadmap governance. Roadmap governance is documented in
`docs/product/roadmap_governance.md`.

## Phase Discipline

Phase 0 is documentation, traceability, repo foundation, CI, and working agreement. Phase 1 starts only after Phase 0 is accepted. Market logic starts only in Phase 1 tickets.
