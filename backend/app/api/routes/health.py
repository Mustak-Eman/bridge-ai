from fastapi import APIRouter

from app.core.config import get_settings
from app.core.exceptions import AppException

router = APIRouter()


@router.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    settings = get_settings()

    return {
        "status": "healthy",
        "service": "bridge-ai-api",
        "version": settings.app_version,
        "environment": settings.environment,
    }

@router.get("/test-error", include_in_schema=False)
def test_error() -> None:
    raise AppException(
        message="This is a test application error.",
        status_code=400,
        error_code="test_error",
    )