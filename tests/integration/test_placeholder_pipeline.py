from typing import TypedDict


class PlaceholderPipelineState(TypedDict):
    asset: str
    placeholder_score: int


def test_placeholder_pipeline_step() -> None:
    pipeline_state: PlaceholderPipelineState = {
        "asset": "S&P 500",
        "placeholder_score": 50,
    }

    assert pipeline_state["asset"] == "S&P 500"
    assert 0 <= pipeline_state["placeholder_score"] <= 100
