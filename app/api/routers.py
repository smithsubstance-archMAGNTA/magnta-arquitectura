from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import Dict
import json

from app.api.websocket_manager import manager
from app.capa_eoo.indicadores import compute_indicators
from app.capa_eoo.motor_diagnostico import diagnose
from app.modelos.esquemas_pydantic import InputSignal
from app.nucleo_mro.inferencia_bayes import estimate_failure_probability
from app.db import get_engine, signals

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

    # persist signal into DB (simple insert)
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(signals.insert().values(source=signal.source, timestamp=signal.timestamp, payload=json.dumps(signal.payload)))
    except Exception as e:
        # do not fail ingestion on DB error; report warning
        print('DB insert failed:', e)

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
