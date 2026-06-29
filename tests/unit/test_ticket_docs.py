from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPRINT_0_TICKETS = [
    "docs/tickets/sprint-0/MXG-001-documentation-foundation.md",
    "docs/tickets/sprint-0/MXG-002-python-repo-skeleton.md",
    "docs/tickets/sprint-0/MXG-003-backlog-and-sprint-plan.md",
    "docs/tickets/sprint-0/MXG-004-ci-pipeline-and-pr-quality-gate.md",
    "docs/tickets/sprint-0/MXG-005-store-executable-tickets.md",
]
REQUIRED_HEADINGS = [
    "Context",
    "Goal",
    "Scope",
    "Acceptance Criteria",
    "Test Requirements",
    "Definition of Done",
]


@pytest.mark.parametrize(
    "path",
    [
        "docs/tickets/README.md",
        "docs/tickets/template.md",
        "docs/tickets/sprint-0",
        *SPRINT_0_TICKETS,
    ],
)
def test_ticket_documentation_paths_exist(path: str) -> None:
    assert (PROJECT_ROOT / path).exists()


@pytest.mark.parametrize("path", SPRINT_0_TICKETS)
def test_sprint_0_ticket_files_contain_required_headings(path: str) -> None:
    content = (PROJECT_ROOT / path).read_text(encoding="utf-8")

    for heading in REQUIRED_HEADINGS:
        assert f"## {heading}" in content

