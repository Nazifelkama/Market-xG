from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_DOC = PROJECT_ROOT / "docs/architecture/market_data_contract.md"
TICKET_DOC = PROJECT_ROOT / "docs/tickets/phase-1/MXG-010-define-market-data-contract.md"


def test_market_data_contract_docs_exist() -> None:
    assert CONTRACT_DOC.is_file()
    assert TICKET_DOC.is_file()


def test_market_data_contract_contains_required_content() -> None:
    content = CONTRACT_DOC.read_text(encoding="utf-8")

    for expected_text in [
        "Market Data Contract",
        "Required Columns",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "Valid Data Example",
        "Invalid Data Examples",
        "Phase 1 uses deterministic local sample data only",
    ]:
        assert expected_text in content


@pytest.mark.parametrize(
    "heading",
    [
        "Context",
        "Goal",
        "Scope",
        "Out of Scope",
        "Acceptance Criteria",
        "Test Requirements",
        "Definition of Done",
    ],
)
def test_mxg_010_ticket_file_contains_required_headings(heading: str) -> None:
    content = TICKET_DOC.read_text(encoding="utf-8")

    assert f"## {heading}" in content

