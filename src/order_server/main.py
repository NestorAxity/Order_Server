from fastapi import FastAPI

from order_server.config.cors import setup_cors
from order_server.config.database import Base, engine
from order_server.infrastructure.controllers.auth_controller import (
    router as auth_router,
)
from order_server.infrastructure.controllers.health_controller import (
    router as health_router,
)
from order_server.infrastructure.controllers.orders_controller import (
    router as order_router,
)

from .config.settings import settings

# Crea las tablas registradas en Base si no existen
Base.metadata.create_all(bind=engine)

# Inicializacion de la App
app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middlewares
setup_cors(app)

# Controllers
app.include_router(health_router)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(order_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
