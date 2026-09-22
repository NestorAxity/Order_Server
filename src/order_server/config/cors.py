# src/cappython/intermedio/m9_fastapi/config/cors.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from order_server.config.settings import settings


def setup_cors(app: FastAPI) -> None:
    """Aplica la configuración de CORS a la instancia de FastAPI."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
