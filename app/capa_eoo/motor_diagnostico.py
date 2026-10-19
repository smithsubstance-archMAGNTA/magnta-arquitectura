"""Motor de diagnóstico de entropía operativa."""

from typing import Dict, List
import numpy as np
from scipy.special import expit

from app.capa_eoo.evaluador_escala import batch_map


DEFAULT_WEIGHTS = None


def compute_entropy_score(indicators: List[Dict], weights: Dict[str, float] = None) -> float:
    if not indicators:
        return 0.0

    vals = np.array([item.get("normalized", 0.0) for item in indicators], dtype=float)
    if weights is None:
        score = float(np.mean(vals))
    else:
        names = [item["name"] for item in indicators]
        w = np.array([weights.get(n, 1.0) for n in names], dtype=float)
        score = float(np.dot(vals, w) / np.sum(w)) if np.sum(w) > 0 else float(np.mean(vals))

    # Sigmoide para reforzar extremos y estabilizar la escala
    return float(expit((score - 0.5) * 6.0))


def classify_entropy(score: float) -> str:
    if score < 0.2:
        return "estable"
    if score < 0.45:
        return "vulnerable"
    if score < 0.75:
        return "alerta"
    return "critico"


def diagnose(indicators: List[Dict], weights: Dict[str, float] = None) -> Dict:
    entropy_score = compute_entropy_score(indicators, weights)
    return {
        "entropy_score": entropy_score,
        "category": classify_entropy(entropy_score),
        "indicators": batch_map(indicators),
    }
