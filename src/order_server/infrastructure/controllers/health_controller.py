from fastapi import APIRouter

from order_server.config.settings import settings

router = APIRouter(tags=["Healt Check"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint para verificación de disponibilidad de la API."""
    return {"status": "ok", "app": settings.APP_NAME}
