import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings

from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging

logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    settings = get_settings()
    configure_logging(debug=settings.debug)


    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
    )

    register_exception_handlers(application)


    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
    )

    @application.get("/", tags=["System"])
    def root() -> dict[str, str]:
        return {
            "message": f"{settings.app_name} API",
            "health": f"{settings.api_v1_prefix}/health",
            "docs": "/docs",
            "environment": settings.environment,
        }

    logger.info(
        "Application configured: name=%s version=%s environment=%s",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    return application


app = create_application()
