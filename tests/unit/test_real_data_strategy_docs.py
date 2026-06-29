from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_DATA_STRATEGY_PATH = REPO_ROOT / "docs" / "architecture" / "real_data_strategy.md"
SAMPLE_MARKET_DATA_PATH = REPO_ROOT / "docs" / "architecture" / "sample_market_data.md"
TICKET_PATH = (
    REPO_ROOT
    / "docs"
    / "tickets"
    / "phase-1"
    / "MXG-012-document-sample-data-limitations-and-real-data-strategy.md"
)


def test_real_data_strategy_doc_exists() -> None:
    assert REAL_DATA_STRATEGY_PATH.exists()


def test_sample_market_data_doc_contains_limitations() -> None:
    sample_text = SAMPLE_MARKET_DATA_PATH.read_text(encoding="utf-8").lower()

    assert "synthetic" in sample_text
    assert "not for financial conclusions" in sample_text
    assert "not for backtesting" in sample_text


def test_real_data_strategy_doc_contains_required_statements() -> None:
    strategy_text = REAL_DATA_STRATEGY_PATH.read_text(encoding="utf-8")

    for expected_text in (
        "synthetic deterministic sample data",
        "must not be used for financial conclusions",
        "must not be used for historical backtesting",
        "Real data providers will be introduced later",
        "Phase 1 tests must not depend on live network calls",
        "adjusted close",
    ):
        assert expected_text in strategy_text


def test_ticket_file_exists_with_required_headings() -> None:
    assert TICKET_PATH.exists()

    ticket_text = TICKET_PATH.read_text(encoding="utf-8")
    for heading in (
        "## Context",
        "## Goal",
        "## Scope",
        "## Out of Scope",
        "## Acceptance Criteria",
        "## Test Requirements",
        "## Definition of Done",
    ):
        assert heading in ticket_text
