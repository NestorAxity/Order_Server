import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context  # type: ignore[attr-defined]

# 1. Permitir que Alembic encuentre los paquetes dentro de src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

# 2. Importar tus modelos y tu configuración
# NOTA: Ajusta las importaciones a los nombres reales de tus módulos
from order_server.config.database import (
    Base,  # O donde definiste Base = declarative_base()
)

# Uvicacion de tu DATABASE_URL
from order_server.config.settings import settings

# Configuración de Alembic (.ini)
config = context.config

# Inyectar tu DATABASE_URL dinámica en la configuración de Alembic
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Vincular los metadatos de SQLAlchemy para --autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
