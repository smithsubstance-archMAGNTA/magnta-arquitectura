# MAGNTA

Arquitectura Operativa · Modelado de Realidad Operativa · Diagnóstico Institucional

## Visión general

MAGNTA es un sistema de observación, diagnóstico y modelado de la realidad operativa. Su núcleo combina:

- EOO: Esquema de Observación Operativa
- MRO: Modelado de Realidad Operativa
- Entropía Operativa
- Trazabilidad y gobernanza
- Dashboard en tiempo real
- Modelado probabilístico y filtrado de señales

Este repositorio implementa una base inicial para un sistema capaz de:

- validar señales de entrada
- calcular indicadores operativos
- transformar indicadores a una escala de gravedad
- estimar entropía operativa
- filtrar ruido y estimar estado real
- calcular riesgo probabilístico
- exponer resultados mediante REST y WebSockets

## Arquitectura

```text
Señales -> validación -> EOO -> diagnóstico -> MRO -> decisión -> WebSocket -> dashboard
```

## Estructura del proyecto

```text
magnta-arquitectura/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routers.py
│   │   └── websocket_manager.py
│   ├── capa_eoo/
│   │   ├── __init__.py
│   │   ├── indicadores.py
│   │   ├── evaluador_escala.py
│   │   └── motor_diagnostico.py
│   ├── nucleo_mro/
│   │   ├── __init__.py
│   │   ├── filtro_kalman.py
│   │   ├── inferencia_bayes.py
│   │   └── transformadas.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   └── esquemas_pydantic.py
│   └── servicios/
│       └── __init__.py
├── frontend_test/
│   ├── index.html
│   └── js/
│       └── chart_config.js
├── scripts/
│   └── graficador_eoo.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Módulos clave

### EOO
- `capa_eoo/indicadores.py`: calcula indicadores operativos
- `capa_eoo/evaluador_escala.py`: transforma valores a escala tipo Fibonacci
- `capa_eoo/motor_diagnostico.py`: agrega indicadores y calcula entropía y categoría

### MRO
- `nucleo_mro/filtro_kalman.py`: limpieza de ruido y estimación del estado real
- `nucleo_mro/inferencia_bayes.py`: probabilidad estimada de falla o degradación
- `nucleo_mro/transformadas.py`: modelado temporal del sistema

### API
- `app/api/routers.py`: endpoints REST
- `app/api/websocket_manager.py`: transmisión en tiempo real

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Luego visita:
- http://localhost:8000/docs
- http://localhost:8000/health
- http://localhost:8000/websocket para pruebas WebSocket

## Dashboard de prueba

Abre `frontend_test/index.html` en un navegador para ver un mockup del dashboard en tiempo real.

## Siguiente nivel

Se puede extender con:

- persistencia real (Postgres / SQLite)
- modelos de IA para predicción temporal
- autenticación y autorización
- panel de gobernanza institucional
- integración con sensores o datos reales

---

MAGNTA  
Observar · Modelar · Diagnosticar · Decidir
