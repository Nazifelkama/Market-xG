# Provider-Based Analysis Technical UAT Results

## Purpose

This document records the Technical UAT execution result for provider-based Market xG analysis.
It gives Sponsor / PO / QA a reviewable evidence record before moving to provider-symbol live
execution.

## UAT Scope

This Technical UAT covers:

`Already-fetched StooqHistoricalResponse -> Stooq normalization -> OHLCV validation -> indicator
calculation -> Trend / Momentum score -> Volume / Accumulation score -> Market xG aggregation ->
markdown report`

This Technical UAT does not cover:

- live provider-symbol execution
- asset search
- symbol resolution
- UI
- watchlist
- scheduling
- persisted analysis status
- real market data verification
- backtesting / calibration

## Execution Method

- UAT was executed using the MXG-036 deterministic Technical UAT harness.
- The harness uses synthetic `StooqHistoricalResponse` inputs.
- No live Stooq calls were used.
- No external market data files were used.
- The UAT harness was not changed in this ticket.
- The results were recorded from actual harness execution.

Commands used:

```bash
.venv/bin/pytest tests/unit/test_provider_analysis_uat.py
.venv/bin/python - <<'PY'
from market_xg.uat.provider_analysis_uat import run_provider_analysis_uat_scenarios
outcomes = run_provider_analysis_uat_scenarios()
passed = sum(o.passed for o in outcomes)
print(f"mandatory={sum(o.mandatory for o in outcomes)} passed={passed} failed={len(outcomes)-passed}")
for outcome in outcomes:
    score = "" if outcome.observed_score is None else f"{outcome.observed_score:.1f}"
    categories = ", ".join(outcome.observed_categories)
    failure = outcome.failure_message or ""
    print("|".join([
        outcome.scenario_id,
        outcome.scenario_name,
        str(outcome.mandatory),
        "PASS" if outcome.passed else "FAIL",
        score,
        categories,
        str(outcome.observed_disclaimer),
        failure,
        outcome.notes,
    ]))
PY
```

## Execution Summary

- Recorded date: 2026-06-30
- UAT case set: UAT-001 through UAT-010
- Mandatory scenarios: 10
- Passed scenarios: 10
- Failed scenarios: 0
- Overall result: PASS
- Data source: deterministic synthetic provider responses
- Live provider calls: no
- External market data files: no

## Scenario Results

| Scenario ID | Scenario name | Mandatory | Result | Observed score | Observed categories | Failure message | Evidence / notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UAT-001 | Bullish happy path | Yes | PASS | 90.0 | trend_momentum, volume_accumulation |  | Score/report produced from bullish deterministic response; disclaimer and missing categories were visible. |
| UAT-002 | Weak/downtrend happy path | Yes | PASS | 7.0 | trend_momentum, volume_accumulation |  | Score/report produced from weak deterministic response; safe explanatory output remained available. |
| UAT-003 | Sideways / mixed market path | Yes | PASS | 21.0 | trend_momentum, volume_accumulation |  | Score/report produced from sideways deterministic response; output remained structured and readable. |
| UAT-004 | Insufficient history | Yes | PASS |  |  | at least 253 rows are required for provider analysis | Expected `ProviderAnalysisError` was raised for insufficient history. |
| UAT-005 | Invalid OHLCV semantics | Yes | PASS |  |  | failed to normalize and validate provider data: normalized Stooq rows failed OHLCV validation: high must be greater than or equal to low | Expected `ProviderAnalysisError` was raised for invalid OHLCV semantics. |
| UAT-006 | Invalid request metadata | Yes | PASS |  |  | asset_name must be a non-empty string / report_date must be a non-empty string | Expected `ProviderAnalysisError` was raised for invalid `asset_name` and `report_date`. |
| UAT-007 | Provider metadata preservation | Yes | PASS | 90.0 | trend_momentum, volume_accumulation |  | `provider`, `provider_symbol`, and `asset_name` were preserved at result level. |
| UAT-008 | Missing future categories are visible | Yes | PASS | 90.0 | trend_momentum, volume_accumulation |  | Implemented categories were present and missing future categories remained visible. |
| UAT-009 | Mandatory disclaimer / safe wording | Yes | PASS | 90.0 | trend_momentum, volume_accumulation |  | Required disclaimer wording was present and obvious guaranteed-return wording was absent. |
| UAT-010 | No live provider dependency | Yes | PASS |  |  |  | Harness used deterministic builders only and did not import or call Stooq fetch functions. |

## Product / PO Review Notes

- The provider-based analysis path is understandable enough for Technical UAT review.
- The generated report includes safe disclaimer wording.
- Missing future categories remain visible.
- Provider metadata is preserved at `ProviderAnalysisResult` level.
- Invalid or insufficient data fails clearly with `ProviderAnalysisError`.
- This is not final product UAT.

## Go / No-Go Decision

Technical UAT decision: PASS

Decision: proceed to provider-symbol live execution planning / implementation.

Rationale:

- All 10 mandatory scenarios passed.
- No failed mandatory scenarios were observed.
- Results were based on actual deterministic harness execution.
- No live Stooq dependency or external market data file dependency was introduced.

## Known Limitations

- No live provider-symbol execution yet.
- No real Stooq symbol verification yet.
- No user-friendly asset search yet.
- No symbol resolution yet.
- No UI yet.
- No watchlist or scheduled refresh yet.
- No persisted analysis status yet.
- Only two Market xG categories are implemented.
- No backtesting / calibration yet.
- No FX conversion.
- No `adjusted_close` decision implemented.
- Not investment advice.
- Not guaranteed prediction.

## Next Milestone

Because Technical UAT result is PASS, likely next steps are:

- Define provider-symbol live execution contract.
- Implement provider-symbol analysis service v0.1.
- Manually verify selected Stooq provider symbols outside CI.
