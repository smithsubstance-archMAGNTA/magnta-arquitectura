# Docker / Deployment guide for MAGNTA

Este documento contiene instrucciones para construir y ejecutar el contenedor de desarrollo de MAGNTA y la matriz de decisión tipo Eisenhower aplicada al trabajo realizado.

## Objetivo del cambio
- Proveer una forma reproducible y localmente consistente de ejecutar MAGNTA usando Docker y Docker Compose.
- Añadir un servicio de base de datos PostgreSQL en `docker-compose` como entorno de desarrollo.

## Comandos rápidos

Construir imagen (opcional, `docker-compose` hace build automáticamente):

    docker build -t magnta:dev .

Levantar servicios con docker-compose:

    docker compose up --build

Detener y borrar contenedores/volúmenes de desarrollo:

    docker compose down -v

Notas:
- El servicio `web` expone el puerto 8000 en el host
- `DATABASE_URL` está configurado en `docker-compose.yml` como: postgresql://magnta:magnta_pass@db:5432/magnta
- En desarrollo el código está montado como volumen para permitir edición en caliente

## Recomendaciones para producción
- Reemplazar el `Dockerfile` por una versión multi-stage optimizada
- No montar el código con `volumes` en producción
- Ejecutar con un servidor de procesos (Gunicorn) y varios workers Uvicorn
- Gestionar secretos (contraseñas, claves) con un vault o variables de entorno seguras
- Usar WSS y certificados cuando expongas WebSockets

## Matriz de Eisenhower aplicada (decisiones y ejecución)

He estructurado las tareas relacionadas con el punto 2 (Docker + Compose) siguiendo la Matriz de Eisenhower (Urgente/Importante):

- CUADRANTE I (Urgente e Importante) — "Hacer ahora" (implementado)
  - Crear Dockerfile de desarrollo simple y reproducible  (hecho)
  - Crear docker-compose.yml con servicio `web` y `db` (Postgres) (hecho)
  - Incluir .dockerignore adecuado (hecho)
  - Documentar comandos básicos para build/up/down (hecho en este archivo)

- CUADRANTE II (Importante pero no Urgente) — "Planificar" (recomendado para siguiente paso)
  - Multi-stage Dockerfile optimizado para producción (separar build/runtime)
  - Integración de migraciones y seeding de datos (scripts de arranque)
  - Healthchecks y probes para el servicio web
  - Configurar uso de un .env y gestión segura de secretos
  - Documentar pasos de despliegue en staging y producción

- CUADRANTE III (Urgente pero no Importante) — "Delegar" (puede delegarse)
  - Montar un runner CI para construir y subir imágenes a un registry (delegable a DevOps)
  - Pruebas de carga con contenedores (simulador) (puede externalizarse o automatizarse)

- CUADRANTE IV (No Urgente, No Importante) — "Eliminar o reducir" (no prioritario)
  - Auditoría profunda de imágenes y scanning hasta que haya pipeline CI/CD
  - Optimización de cada dependencia al nivel de byte (prematuro en esta fase)

Acciones ejecutadas ahora (resumen):
- He implementado los elementos del Cuadrante I y creado los artefactos en el repositorio.
- He documentado los comandos básicos y recomendaciones de producción.

## Qué sigue (sugerencia priorizada)
1. (Q2) Crear Dockerfile multi-stage y preparar imagen de producción
2. (Q2) Añadir healthchecks y entrypoint que aplique migraciones antes del inicio
3. (Q3) Crear pipeline CI que construya y escanee la imagen
4. (Q1/Q2) Configurar persistencia y backup para Postgres en staging

---

Si quieres, procedo a:
- Implementar Dockerfile multi-stage y una imagen de producción optimizada
- Añadir `docker-compose.override.yml` para `dev` vs `prod`
- Crear un `Makefile` con comandos rápidos (`make build`, `make up`, `make down`)

Dime qué deseas que haga ahora y lo implemento.