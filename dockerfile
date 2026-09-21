# ==========================================
# ETAPA 1: Builder
# ==========================================
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.4.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get purge -y --auto-remove curl && \
    rm -rf /var/lib/apt/lists/*

# Copiamos archivos de dependencias e instalamos
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

# Copiamos el código fuente, archivos de alembic y el entrypoint
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini entrypoint.sh ./

# Aseguramos permisos de ejecución en el script
RUN chmod +x entrypoint.sh

# ==========================================
# ETAPA 2: Runner
# ==========================================
FROM python:3.13-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    DATABASE_URL="sqlite:////app/data/order_app_dev.db"

RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -s /bin/sh appuser

# Crear directorio de datos y asignar permisos
RUN mkdir -p /app/data && chown -R appuser:appgroup /app

# Copiar archivos desde la etapa de builder asignando el propietario correcto
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src
COPY --from=builder --chown=appuser:appgroup /app/alembic /app/alembic
COPY --from=builder --chown=appuser:appgroup /app/alembic.ini /app/alembic.ini
COPY --from=builder --chown=appuser:appgroup /app/entrypoint.sh /app/entrypoint.sh

USER appuser

EXPOSE 8000

# Usamos el script de entrypoint antes del comando principal
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "order_server.main:app", "--host", "0.0.0.0", "--port", "8000"]