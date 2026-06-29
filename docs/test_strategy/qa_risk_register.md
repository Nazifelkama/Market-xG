# QA Risk Register

| Risk ID | Risk | Impact | Mitigation | Test Coverage |
| --- | --- | --- | --- | --- |
| QR-001 | Lookahead bias | Backtests overstate score quality and create false confidence. | Separate scoring inputs from future outcomes and validate date joins. | Backtest validation tests with intentional future leakage fixtures. |
| QR-002 | Incorrect moving average window | Trend signals become inaccurate or shifted. | Use deterministic fixtures with known expected moving averages. | Unit tests for window sizes, warmup periods, and date alignment. |
| QR-003 | Missing market data treated as valid data | Scores appear valid when input quality is poor. | Fail clearly on missing required data and lower confidence when partial data is allowed. | Data quality tests for missing columns, gaps, stale dates, and null values. |
| QR-004 | VIX sentiment scoring inverted incorrectly | High volatility could be scored as healthy by mistake. | Document score direction and test normal, elevated, and extreme VIX regimes. | Unit tests for VIX scoring thresholds and directionality. |
| QR-005 | Weighted score outside 0-100 | Final Market xG score becomes invalid or misleading. | Validate category score bounds and weight totals before aggregation. | Unit tests for bounds, weight sums, missing categories, and invalid inputs. |
| QR-006 | Beautiful report but incorrect calculations | Users trust polished output with wrong underlying math. | Treat reports as views over tested calculations, not calculation sources. | Integration tests comparing report content to known score fixtures. |
| QR-007 | Historical data source changes format | Ingestion breaks silently or misreads columns. | Validate schemas and fail with meaningful errors on unexpected formats. | Data provider tests for schema changes, renamed columns, and bad date formats. |
| QR-008 | Overfitting during later ML phase | Adaptive weighting may look good historically but fail out of sample. | Keep rule-based baseline, use holdout periods, and document validation limits. | Future ML validation tests with train/test splits and baseline comparisons. |

