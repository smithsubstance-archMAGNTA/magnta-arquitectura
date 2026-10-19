"""Mapa de indicadores a escala tipo Fibonacci."""

import bisect

FIB_SCALE = [0, 1, 2, 3, 5, 8, 13, 21]
THRESHOLDS = [i / (len(FIB_SCALE) - 1) for i in range(len(FIB_SCALE))]


def map_to_fib(normalized_value: float) -> int:
    value = max(0.0, min(1.0, float(normalized_value)))
    idx = bisect.bisect_right(THRESHOLDS, value) - 1
    idx = max(0, min(len(FIB_SCALE) - 1, idx))
    return FIB_SCALE[idx]


def batch_map(indicators: list) -> list:
    mapped = []
    for item in indicators:
        copied = item.copy()
        copied["fib_scale"] = map_to_fib(item.get("normalized", 0.0))
        mapped.append(copied)
    return mapped
