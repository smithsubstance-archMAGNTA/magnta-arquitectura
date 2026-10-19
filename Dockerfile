# Multi-stage Dockerfile for MAGNTA (development & production friendly)

### Builder: prepares wheels to speed up final image
FROM python:3.11-slim as builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /wheels

# Install build deps for building wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /wheels/
RUN pip wheel --no-cache-dir --wheel-dir /wheels/wheels -r requirements.txt

### Final image: lean runtime, install from built wheels
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# minimal runtime deps (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# copy wheels from builder and install
COPY --from=builder /wheels/wheels /wheels
COPY requirements.txt /app/
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# copy source
COPY . /app

# ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh || true

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
