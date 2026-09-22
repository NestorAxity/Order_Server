from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from order_server.config.settings import settings

# Creacion de la conexion (engine)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {},
    echo=settings.DEBUG,
)

# Fabrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base de clases que representan una tabla
class Base(DeclarativeBase):
    pass


# Inyeccion de dependencias (Session per Request)
def get_db() -> Generator[Session, None, None]:
    """Generador que abre una sesión de base de datos por petición HTTP

    y garantiza su cierre automático al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
