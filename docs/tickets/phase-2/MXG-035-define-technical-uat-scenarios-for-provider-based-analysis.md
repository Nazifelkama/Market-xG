# MXG-035 — Define Technical UAT Scenarios for Provider-Based Analysis

Status: In Progress
Sprint: Sprint 2
Phase: Phase 2
Epic: Real Data Readiness
Type: QA / UAT Planning
Owner: Codex
Reviewer: QA / PM
Branch: main
PR: TBD
Created: 2026-06-30
Updated: 2026-06-30

## Context

MXG-032 implemented the raw Stooq historical data client and parser. MXG-033 implemented Stooq
historical data normalization into Market xG OHLCV-compatible rows. MXG-034 implemented the
provider-based analysis orchestrator v0.1. The current path can turn already-fetched provider
data into a validated Market xG score and markdown report, but Technical UAT needs to define
how Sponsor / PO / QA decide whether the path is ready for provider-symbol live execution.

## Goal

Define Technical UAT scenarios, acceptance evidence, and go/no-go decision criteria for
provider-based Market xG analysis.

## Scope

- Create `docs/uat/provider_based_analysis_technical_uat.md`.
- Add a short Technical UAT reference to `docs/product/asset_analysis_workflow.md`.
- Create this ticket document under `docs/tickets/phase-2/`.
- Define UAT roles, entry criteria, exit criteria, decision model, deterministic inputs,
  scenarios, critical fail conditions, evidence checklist, limitations, and next milestone.

## Out of Scope

- Production source-code changes.
- Test changes.
- Live provider fetching or provider-symbol CLI.
- Asset search, symbol resolution, UI, watchlist storage, scheduled refresh, persisted status,
  or CSV import.
- Real market data files or screenshots.
- Running Market xG on real assets.
- Scoring, indicator, or aggregation changes.
- External dependency changes.

## Documentation Requirements

- Clearly distinguish Technical UAT from final product UAT.
- Document the current provider-based path from already-fetched `StooqHistoricalResponse` to
  markdown report.
- Define Sponsor / PO, QA, and Engineering roles.
- Define Technical UAT entry and exit criteria.
- Define PASS, CONDITIONAL PASS, and FAIL outcomes.
- Define deterministic Technical UAT inputs that do not require real market data files or live
  Stooq calls.
- Include explicit `UAT-001` through `UAT-010` scenarios.
- Ensure each scenario includes Purpose, Given / When / Then, PO review notes, Expected evidence,
  and Mandatory flag.
- Include `UAT-003` Sideways / mixed market path.
- Mark all ten scenarios as mandatory.
- Include critical fail conditions.
- Include a manual evidence checklist.
- List known limitations and the likely next milestone after Technical UAT.

## Acceptance Criteria

- `docs/uat/provider_based_analysis_technical_uat.md` exists.
- The document clearly distinguishes Technical UAT from final product UAT.
- The document describes the current provider-based analysis path.
- The document defines Technical UAT roles.
- The document defines entry criteria.
- The document defines exit criteria.
- The document defines PASS / CONDITIONAL PASS / FAIL outcomes.
- The document defines deterministic Technical UAT input set.
- The document includes explicit `UAT-001` through `UAT-010` scenarios.
- Each scenario includes Purpose, Given / When / Then, PO review notes, Expected evidence, and
  Mandatory flag.
- `UAT-003` Sideways / mixed market path exists.
- All ten scenarios are mandatory.
- The document includes critical fail conditions.
- The document includes a manual evidence checklist.
- The manual evidence checklist includes Scenario ID, Scenario name, Mandatory? yes/no,
  Pass / Fail, Evidence / notes, Observed score, Observed categories, Observed report
  disclaimer, Failure message where applicable, Reviewer initials, and Review date.
- The document lists known limitations.
- The document defines the likely next milestone after Technical UAT.
- `docs/product/asset_analysis_workflow.md` is updated only with a short useful reference.
- This ticket file exists.
- No production source code is changed.
- No tests are changed.
- No live provider fetching is implemented.
- No provider-symbol CLI is implemented.
- No asset search, symbol resolution, UI, watchlist storage, scheduled refresh, persisted
  status, or CSV import is implemented.
- No real market data files are added.
- No scoring rules, indicator formulas, or aggregation weights are changed.
- No external dependencies are added.

## Check Requirements

- Run `git diff --check`.
- If markdown linting is configured later, run the relevant markdown-lint command.
- Do not run the full test suite unless documentation changes unexpectedly require it.
- Rely on full CI after push or PR for broader repository checks.

## Definition of Done

- Documentation changes are complete within ticket scope.
- Acceptance criteria are satisfied.
- Required lightweight checks pass.
- Global completion expectations continue to follow
  `docs/test_strategy/definition_of_done.md`.

## Review Notes

Pending QA and PM review.

## Decision Log

- Technical UAT is separate from final product UAT.
- Technical UAT validates already-fetched provider data through Market xG analysis/report.
- Live provider execution is not required for Technical UAT.
- Search, symbol resolution, UI, watchlist, scheduling, and persisted status remain future
  product layers.
- Technical UAT can proceed with deterministic provider responses.
- Technical UAT uses a go/no-go decision model before moving to provider-symbol live execution.
