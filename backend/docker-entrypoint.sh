#!/bin/bash

echo "⌛ Waiting for PostgreSQL to be ready..."
until pg_isready -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  sleep 2
done

echo "✅ PostgreSQL is up. Running migrations..."

alembic upgrade head

echo "🚀 Starting FastAPI app..."
exec uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
