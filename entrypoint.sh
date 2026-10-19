#!/usr/bin/env bash
set -e

: "Ensure DATABASE_URL is set" && :
: ${DATABASE_URL:=sqlite:///./magnta_dev.db}

echo "DATABASE_URL=${DATABASE_URL}"

# Wait for Postgres if used
if echo "$DATABASE_URL" | grep -q "postgresql://"; then
  echo "Waiting for Postgres..."
  host=$(echo "$DATABASE_URL" | sed -n 's|.*@\([^/:]*\).*|\1|p') || true
  host=${host:-db}
  port=5432
  echo "Checking tcp://${host}:${port}"
  for i in {1..60}; do
    if nc -z ${host} ${port}; then
      echo "Postgres is up"
      break
    fi
    echo "Waiting for Postgres... (${i})"
    sleep 1
  done
fi

# Run Alembic migrations if alembic is available
if command -v alembic >/dev/null 2>&1; then
  echo "Running alembic upgrade head"
  alembic upgrade head || echo "Alembic upgrade failed, falling back to create_all"
else
  echo "Alembic not found; will run create_all fallback"
fi

# Fallback migration using create_all
python - <<'PY'
from app.db import migrate
migrate()
PY

# Exec CMD (uvicorn) from Dockerfile
exec "$@"
