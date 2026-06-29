from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_ci_workflow_exists_and_contains_quality_checks() -> None:
    workflow = PROJECT_ROOT / ".github/workflows/ci.yml"

    assert workflow.is_file()

    content = workflow.read_text(encoding="utf-8")
    for expected_text in [
        "Market xG CI",
        "quality-checks",
        "ruff check src tests",
        "mypy src",
        "pytest --cov=market_xg --cov-report=term-missing",
    ]:
        assert expected_text in content


def test_ci_cd_documentation_exists() -> None:
    assert (PROJECT_ROOT / "docs/test_strategy/ci_cd.md").is_file()

