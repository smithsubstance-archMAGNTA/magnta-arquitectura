import json
from app.capa_eoo.indicadores import compute_indicators


def test_compute_indicators_basic():
    payload = {"a": 1.0, "b": 0.8, "c": 1.2}
    res = compute_indicators(payload)
    assert isinstance(res, list)
    assert len(res) >= 1
    names = [r['name'] for r in res]
    assert 'variabilidad' in names
