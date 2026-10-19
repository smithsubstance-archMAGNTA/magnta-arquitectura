from typing import Dict, List
import numpy as np


# Indicadores básicos. Se pueden extender con fórmulas más reales según el dominio.
def _variabilidad(payload):
    vals = np.array(list(payload.values()), dtype=float)
    return float(np.std(vals))


def _desviacion_media(payload):
    vals = np.array(list(payload.values()), dtype=float)
    return float(np.mean(np.abs(vals - np.mean(vals))))


def _saturacion(payload):
    vals = np.array(list(payload.values()), dtype=float)
    if len(vals) == 0:
        return 0.0
    max_value = np.max(vals)
    if max_value == 0:
        return 0.0
    return float(np.sum(vals > 0.9 * max_value) / len(vals))


def _latencia_aparente(payload):
    return float(payload.get("latency", 0.0))


def _anomalies_rate(payload):
    vals = np.array(list(payload.values()), dtype=float)
    if len(vals) == 0:
        return 0.0
    return float(np.sum(np.isnan(vals) | (vals < 0)) / len(vals))


INDICATORS = {
    "variabilidad": _variabilidad,
    "desviacion_media": _desviacion_media,
    "saturacion": _saturacion,
    "latencia_aparente": _latencia_aparente,
    "anomalies_rate": _anomalies_rate,
}


def compute_indicators(payload: Dict[str, float]) -> List[Dict]:
    raw_values = {}
    for name, fn in INDICATORS.items():
        try:
            raw_values[name] = float(fn(payload))
        except Exception:
            raw_values[name] = 0.0

    arr = np.array(list(raw_values.values()), dtype=float)
    if len(arr) == 0:
        return []

    p1, p99 = np.percentile(arr, [1, 99]) if len(arr) > 1 else (0.0, 1.0)
    denom = p99 - p1 if (p99 - p1) != 0 else 1.0

    results = []
    for name, raw in raw_values.items():
        normalized = (raw - p1) / denom
        normalized = float(np.clip(normalized, 0.0, 1.0))
        results.append({
            "name": name,
            "value": float(raw),
            "normalized": normalized,
            "meta": {},
        })
    return results
