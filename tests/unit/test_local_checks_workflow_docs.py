from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DOC = PROJECT_ROOT / "docs/product/local_checks_and_commit_workflow.md"
TICKET_DOC = PROJECT_ROOT / "docs/tickets/sprint-0/MXG-007-local-checks-and-commit-workflow.md"


def test_local_checks_workflow_docs_exist_and_are_referenced() -> None:
    assert WORKFLOW_DOC.is_file()
    assert TICKET_DOC.is_file()

    assert "docs/product/local_checks_and_commit_workflow.md" in (
        PROJECT_ROOT / "README.md"
    ).read_text(encoding="utf-8")
    assert "review report before commit" in (
        PROJECT_ROOT / "docs/product/way_of_working.md"
    ).read_text(encoding="utf-8")
    assert "docs/product/local_checks_and_commit_workflow.md" in (
        PROJECT_ROOT / "docs/tickets/README.md"
    ).read_text(encoding="utf-8")


def test_ticket_template_mentions_local_checks_and_ci() -> None:
    content = (PROJECT_ROOT / "docs/tickets/template.md").read_text(encoding="utf-8")

    assert "Relevant local checks before review" in content
    assert "Full CI before merge" in content


def test_local_checks_workflow_doc_contains_required_sections_and_rules() -> None:
    content = WORKFLOW_DOC.read_text(encoding="utf-8")

    for expected_text in [
        "Codex does not commit immediately after implementation",
        "Relevant Local Checks",
        "Full CI Gate",
        "Review Report Format",
        "Human approval is required before commit/push",
        "Never push directly to main",
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
def test_mxg_007_ticket_file_contains_required_headings(heading: str) -> None:
    content = TICKET_DOC.read_text(encoding="utf-8")

    assert f"## {heading}" in content

