from pydantic import BaseModel, Field
from typing import Dict, Any


class InputSignal(BaseModel):
    source: str = Field(..., description="Identificador de la fuente/sensor")
    timestamp: float = Field(..., description="Epoch timestamp en segundos")
    payload: Dict[str, float] = Field(..., description="Mapa de mediciones (clave -> valor)")


class IndicatorResult(BaseModel):
    name: str
    value: float
    normalized: float
    meta: Dict[str, Any] = {}
