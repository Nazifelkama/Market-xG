import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "market_xg",
        "market_xg.config",
        "market_xg.data_providers",
        "market_xg.indicators",
        "market_xg.scoring",
        "market_xg.backtesting",
        "market_xg.narratives",
        "market_xg.reports",
        "market_xg.utils",
    ],
)
def test_placeholder_package_imports(module_name: str) -> None:
    assert importlib.import_module(module_name)

