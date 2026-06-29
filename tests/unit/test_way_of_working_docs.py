from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_way_of_working_document_exists() -> None:
    assert (PROJECT_ROOT / "docs/product/way_of_working.md").is_file()


def test_readme_mentions_way_of_working() -> None:
    content = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert "Way of Working" in content


def test_ticket_readme_documents_status_lifecycle() -> None:
    content = (PROJECT_ROOT / "docs/tickets/README.md").read_text(encoding="utf-8")

    for expected_text in ["Not Started", "In Progress", "In Review", "Done"]:
        assert expected_text in content


def test_ticket_template_contains_review_metadata_and_sections() -> None:
    content = (PROJECT_ROOT / "docs/tickets/template.md").read_text(encoding="utf-8")

    for expected_text in ["Branch", "PR", "Review Notes", "Decision Log"]:
        assert expected_text in content


def test_way_of_working_contains_core_rules_and_phase_discipline() -> None:
    content = (PROJECT_ROOT / "docs/product/way_of_working.md").read_text(encoding="utf-8")

    for expected_text in [
        "One ticket equals one branch equals one pull request",
        "No direct pushes to main",
        "A ticket is not Done just because code was generated",
        "Phase 1 starts only after Phase 0 is accepted",
    ]:
        assert expected_text in content

