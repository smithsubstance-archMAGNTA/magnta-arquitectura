#!/usr/bin/env bash
set -e

# Simple entrypoint: wait for DB, run migrations (SQLAlchemy create_all) and start server
: "Ensure DATABASE_URL is set" && :
: ${DATABASE_URL:=sqlite:///./magnta_dev.db}

echo "DATABASE_URL=${DATABASE_URL}"

# Wait for Postgres if used
if echo "$DATABASE_URL" | grep -q "postgresql://"; then
  echo "Waiting for Postgres..."
  # parse host and port
  host=$(echo "$DATABASE_URL" | sed -n 's|.*@\([^/:]*\).*|\1|p') || true
  host=${host:-db}
  port=5432
  echo "Checking tcp://${host}:${port}"
  # wait loop
  for i in {1..30}; do
    if nc -z ${host} ${port}; then
      echo "Postgres is up"
      break
    fi
    echo "Waiting for Postgres... (${i})"
    sleep 1
  done
fi

# Run migrations (simple create_all)
echo "Running migrations (create_all)"
python - <<'PY'
from app.db import migrate
migrate()
PY

# Exec CMD (uvicorn) from Dockerfile
exec "$@"
