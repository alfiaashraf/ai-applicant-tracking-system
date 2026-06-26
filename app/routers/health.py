from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    response_description="Service availability and version.",
)
async def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", version=settings.app_version)
