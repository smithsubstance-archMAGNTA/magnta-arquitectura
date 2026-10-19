from typing import Dict, Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from app.api.websocket_manager import manager
from app.capa_eoo.indicadores import compute_indicators
from app.capa_eoo.motor_diagnostico import diagnose
from app.modelos.esquemas_pydantic import InputSignal
from app.nucleo_mro.inferencia_bayes import estimate_failure_probability

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "project": "MAGNTA"}


@router.get("/metrics")
def metrics() -> dict:
    return {
        "system": "MAGNTA",
        "modules": [
            "EOO",
            "MRO",
            "Kalman",
            "Bayes",
            "WebSocket",
        ],
    }


@router.post("/ingest-signal")
def ingest_signal(signal: InputSignal) -> dict:
    indicators = compute_indicators(signal.payload)
    diagnosis = diagnose(indicators)
    risk = estimate_failure_probability(diagnosis["entropy_score"])
    response = {
        "source": signal.source,
        "timestamp": signal.timestamp,
        "indicators": indicators,
        "diagnosis": diagnosis,
        "failure_probability": risk,
    }
    manager.broadcast({"event": "diagnostic", "payload": response})
    return response


@router.post("/diagnostic")
def diagnostic(signal: InputSignal) -> dict:
    indicators = compute_indicators(signal.payload)
    diagnosis = diagnose(indicators)
    return {
        "source": signal.source,
        "timestamp": signal.timestamp,
        "diagnosis": diagnosis,
        "failure_probability": estimate_failure_probability(diagnosis["entropy_score"]),
    }


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
