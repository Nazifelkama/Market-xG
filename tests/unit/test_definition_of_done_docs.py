from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFINITION_OF_DONE = PROJECT_ROOT / "docs/test_strategy/definition_of_done.md"
TICKET_DOC = PROJECT_ROOT / "docs/tickets/sprint-0/MXG-008-definition-of-done.md"


def test_definition_of_done_docs_exist_and_are_referenced() -> None:
    assert DEFINITION_OF_DONE.is_file()
    assert TICKET_DOC.is_file()

    for path in [
        "README.md",
        "docs/product/way_of_working.md",
        "docs/product/local_checks_and_commit_workflow.md",
        "docs/tickets/README.md",
    ]:
        content = (PROJECT_ROOT / path).read_text(encoding="utf-8")
        assert "docs/test_strategy/definition_of_done.md" in content


def test_ticket_template_references_global_quality_gate() -> None:
    content = (PROJECT_ROOT / "docs/tickets/template.md").read_text(encoding="utf-8")

    for expected_text in [
        "Use docs/test_strategy/definition_of_done.md as the global quality gate",
        "Relevant local checks before review",
        "Full CI before merge",
    ]:
        assert expected_text in content


def test_definition_of_done_contains_required_sections_and_rules() -> None:
    content = DEFINITION_OF_DONE.read_text(encoding="utf-8")

    for expected_text in [
        "Global Definition of Done",
        "Documentation Ticket DoD",
        "Code Ticket DoD",
        "Data Ticket DoD",
        "Scoring Ticket DoD",
        "Backtest Ticket DoD",
        "Report / Narrative Ticket DoD",
        "Completion Report DoD",
        "Not Done Examples",
        "No lookahead bias",
        "No unrelated scope",
        "Full CI passes before merge",
        "Relevant local checks pass before review",
    ]:
        assert expected_text in content


@pytest.mark.parametrize(
    "heading",
    [
        "Context",
        "Goal",
        "Scope",
        "Out of Scope",
        "Implementation Instructions",
        "Acceptance Criteria",
        "Test Requirements",
        "Definition of Done",
        "Review Notes",
        "Decision Log",
    ],
)
def test_mxg_008_ticket_file_contains_required_headings(heading: str) -> None:
    content = TICKET_DOC.read_text(encoding="utf-8")

    assert f"## {heading}" in content

