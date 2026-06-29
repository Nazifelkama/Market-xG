from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("path", "required_text"),
    [
        ("backlog.md", "MXG-031"),
        ("docs/product/sprint_plan.md", "Sprint 0: Foundation"),
        ("docs/test_strategy/definition_of_done.md", "No silent failures"),
        ("docs/test_strategy/qa_risk_register.md", "QR-001"),
    ],
)
def test_qa_planning_documents_exist(path: str, required_text: str) -> None:
    document = PROJECT_ROOT / path

    assert document.is_file()
    assert required_text in document.read_text(encoding="utf-8")

