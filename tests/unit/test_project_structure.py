from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "folder",
    [
        "docs/product",
        "docs/requirements",
        "docs/architecture",
        "docs/test_strategy",
        "docs/decision_log",
        "src/market_xg",
        "src/market_xg/config",
        "src/market_xg/data_providers",
        "src/market_xg/indicators",
        "src/market_xg/scoring",
        "src/market_xg/backtesting",
        "src/market_xg/narratives",
        "src/market_xg/reports",
        "src/market_xg/utils",
        "tests/unit",
        "tests/integration",
        "tests/backtest",
        "data/raw",
        "data/processed",
        "data/backtest",
    ],
)
def test_required_folder_exists(folder: str) -> None:
    assert (PROJECT_ROOT / folder).is_dir()

