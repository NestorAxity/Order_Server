from fastapi import FastAPI

from order_server.config.cors import setup_cors

from .config.settings import settings

# Inicializacion de la App
app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middlewares
setup_cors(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
