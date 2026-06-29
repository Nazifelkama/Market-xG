from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE_DOC = PROJECT_ROOT / "docs/product/roadmap_governance.md"
TICKET_DOC = PROJECT_ROOT / "docs/tickets/sprint-0/MXG-009-roadmap-governance.md"


def test_roadmap_governance_docs_exist_and_are_referenced() -> None:
    assert GOVERNANCE_DOC.is_file()
    assert TICKET_DOC.is_file()

    for path in [
        "README.md",
        "docs/product/roadmap.md",
        "docs/tickets/README.md",
    ]:
        content = (PROJECT_ROOT / path).read_text(encoding="utf-8")
        assert "docs/product/roadmap_governance.md" in content

    way_of_working = (PROJECT_ROOT / "docs/product/way_of_working.md").read_text(
        encoding="utf-8"
    )
    assert "roadmap governance" in way_of_working


def test_ticket_template_contains_roadmap_traceability_metadata() -> None:
    content = (PROJECT_ROOT / "docs/tickets/template.md").read_text(encoding="utf-8")

    for expected_text in ["roadmap traceability", "Phase", "Epic"]:
        assert expected_text in content


def test_roadmap_governance_doc_contains_required_sections_and_rules() -> None:
    content = GOVERNANCE_DOC.read_text(encoding="utf-8")

    for expected_text in [
        "Roadmap Levels",
        "Phase Rules",
        "Epic Rules",
        "Ticket Rules",
        "Change Control",
        "Future Ideas Parking Lot",
        "Roadmap Review Cadence",
        "Traceability",
        "Vision → Phase → Epic → Ticket → PR → Commit",
        "Phase 1 cannot start until Phase 0 is accepted",
        "One ticket equals one branch equals one pull request",
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
def test_mxg_009_ticket_file_contains_required_headings(heading: str) -> None:
    content = TICKET_DOC.read_text(encoding="utf-8")

    assert f"## {heading}" in content

