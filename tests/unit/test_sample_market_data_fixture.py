from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "market_data" / "sample_sp500_ohlcv.csv"
)
DOC_PATH = REPO_ROOT / "docs" / "architecture" / "sample_market_data.md"
TICKET_PATH = (
    REPO_ROOT
    / "docs"
    / "tickets"
    / "phase-1"
    / "MXG-011-add-deterministic-sample-market-data-fixture.md"
)
EXPECTED_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def _read_rows() -> list[dict[str, str]]:
    with FIXTURE_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def _to_decimal(value: str) -> Decimal:
    return Decimal(value)


def test_market_data_fixture_exists_with_expected_columns() -> None:
    assert FIXTURE_PATH.exists()

    with FIXTURE_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)

    assert header == EXPECTED_COLUMNS


def test_market_data_fixture_has_minimum_rows_and_sorted_unique_dates() -> None:
    rows = _read_rows()
    assert len(rows) >= 260

    parsed_dates = [date.fromisoformat(row["date"]) for row in rows]

    assert parsed_dates == sorted(parsed_dates)
    assert len(parsed_dates) == len(set(parsed_dates))


def test_market_data_fixture_values_follow_contract_rules() -> None:
    rows = _read_rows()

    for row in rows:
        assert list(row.keys()) == EXPECTED_COLUMNS
        assert all(row[column] != "" for column in EXPECTED_COLUMNS)

        date.fromisoformat(row["date"])
        open_price = _to_decimal(row["open"])
        high_price = _to_decimal(row["high"])
        low_price = _to_decimal(row["low"])
        close_price = _to_decimal(row["close"])
        volume = _to_decimal(row["volume"])

        assert open_price > 0
        assert high_price > 0
        assert low_price > 0
        assert close_price > 0
        assert volume >= 0
        assert high_price >= low_price
        assert low_price <= open_price <= high_price
        assert low_price <= close_price <= high_price


def test_sample_market_data_docs_exist_and_reference_contract() -> None:
    assert DOC_PATH.exists()
    assert TICKET_PATH.exists()

    doc_text = DOC_PATH.read_text(encoding="utf-8")
    assert "# Sample Market Data" in doc_text
    assert "tests/fixtures/market_data/sample_sp500_ohlcv.csv" in doc_text
    assert "docs/architecture/market_data_contract.md" in doc_text
    assert "deterministic" in doc_text.lower()


def test_ticket_file_contains_required_sections() -> None:
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
