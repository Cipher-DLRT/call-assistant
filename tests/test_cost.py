import pytest

from app.loop.cost import PRICES, CostMeter


def test_ceiling_and_summary():
    PRICES["fake"] = (1000.0, 2000.0)
    try:
        meter = CostMeter(0.01)
        allowed = []
        for _ in range(4):
            meter.add("gate", "fake", 1, 1)
            allowed.append(meter.allow())

        assert allowed == [True, True, True, False]
        assert meter.allow() is False
        assert meter.summary() == {
            "gate_calls": 4,
            "hint_calls": 0,
            "input_tokens": 4,
            "output_tokens": 4,
            "total_usd": 0.012,
            "ceiling_usd": 0.01,
            "ceiling_hit": True,
        }
        with pytest.raises(AttributeError):
            meter.ceiling_usd = 1.0
        assert meter.allow() is False
    finally:
        del PRICES["fake"]


def test_tracks_each_kind_and_returns_call_cost():
    PRICES["fake"] = (10.0, 20.0)
    try:
        meter = CostMeter(1.0)
        assert meter.add("gate", "fake", 100, 50) == pytest.approx(0.002)
        assert meter.add("hint", "fake", 200, 100) == pytest.approx(0.004)
        assert meter.summary()["gate_calls"] == 1
        assert meter.summary()["hint_calls"] == 1
        assert meter.spent == pytest.approx(0.006)
    finally:
        del PRICES["fake"]


def test_unknown_model_raises():
    meter = CostMeter(0.01)
    with pytest.raises(KeyError):
        meter.add("gate", "does-not-exist", 1, 1)
