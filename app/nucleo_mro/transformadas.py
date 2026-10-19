"""Transformadas y análisis temporal básico."""

from typing import List
import numpy as np


def signal_velocity(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    arr = np.asarray(values, dtype=float)
    return float(np.diff(arr).mean())


def signal_trend(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    arr = np.asarray(values, dtype=float)
    x = np.arange(len(arr), dtype=float)
    slope, _ = np.polyfit(x, arr, 1)
    return float(slope)


def signal_variance(values: List[float]) -> float:
    if not values:
        return 0.0
    arr = np.asarray(values, dtype=float)
    return float(np.var(arr))
