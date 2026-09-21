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

# Copiamos archivos de dependencias e instalamos (se guarda en caché)
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

# Copiamos el código fuente
COPY src ./src

# ==========================================
# ETAPA 2: Runner
# ==========================================
FROM python:3.13-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"\
    DATABASE_URL="sqlite:////app/data/order_app_dev.db"

RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -s /bin/sh appuser

# Crear el directorio de datos y asignar permisos al usuario no-root
RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

USER appuser

EXPOSE 8000

CMD ["uvicorn", "order_server.main:app", "--host", "0.0.0.0", "--port", "8000"]