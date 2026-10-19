from fastapi import FastAPI
from app.api.routers import router

app = FastAPI(
    title="MAGNTA",
    description="Arquitectura Operativa, EOO, MRO y diagnóstico de entropía operativa",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {
        "project": "MAGNTA",
        "status": "online",
        "description": "Arquitectura Operativa y Modelado de Realidad Operativa",
    }
