def test_placeholder_pipeline_step() -> None:
    pipeline_state = {
        "asset": "S&P 500",
        "placeholder_score": 50,
    }

    assert pipeline_state["asset"] == "S&P 500"
    assert 0 <= pipeline_state["placeholder_score"] <= 100

