#!/bin/sh
set -e

echo "==> Ejecutando migraciones de base de datos con Alembic..."
alembic upgrade head

echo "==> Iniciando servidor Uvicorn..."
exec "$@"