import logging
logger = logging.getLogger(__name__)

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AIProviderConfigurationError,
    AIProviderError,
    AppException,
    DocumentContentTooLargeError,
    DocumentEncodingError,
    DocumentParsingError,
    DocumentTextUnavailableError,
    DocumentTooLargeError,
    DocumentValidationError,
    EmptyDocumentError,
    EncryptedDocumentError,
    InvalidOperationError,
    ResourceConflictError,
    ResourceNotFoundError,
    UnsupportedDocumentTypeError,
)

def create_error_response(
    *,
    status_code: int,
    error_code: str,
    message: str,
    details: Any = None,
) -> JSONResponse:
    content: dict[str, Any] = {
        "error": {
            "code": error_code,
            "message": message,
        }
    }

    if details is not None:
        content["error"]["details"] = details

    return JSONResponse(
        status_code=status_code,
        content=content,
    )


async def app_exception_handler(
    request: Request,
    exception: AppException,
) -> JSONResponse:
    del request

    status_code = 400

    if isinstance(exception, ResourceNotFoundError):
        status_code = 404

    elif isinstance(exception, ResourceConflictError):
        status_code = 409

    elif isinstance(
        exception,
        (
            InvalidOperationError,
            DocumentParsingError,
            DocumentEncodingError,
            DocumentTextUnavailableError,
            EncryptedDocumentError,
        ),
    ):
        status_code = 422

    elif isinstance(
        exception,
        (
            DocumentTooLargeError,
            DocumentContentTooLargeError,
        ),
    ):
        status_code = 413

    elif isinstance(
        exception,
        (
            DocumentValidationError,
            EmptyDocumentError,
            UnsupportedDocumentTypeError,
        ),
    ):
        status_code = 400

    elif isinstance(exception, AIProviderConfigurationError):
        status_code = 503

    elif isinstance(exception, AIProviderError):
        status_code = 502

    return create_error_response(
        status_code=status_code,
        error_code=exception.error_code,
        message=exception.message,
    )

async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    return create_error_response(
        status_code=422,
        error_code="validation_error",
        message="The request contains invalid data.",
        details=exception.errors(),
    )


async def unexpected_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    logger.exception(
        "Unexpected error while processing %s %s",
        request.method,
        request.url.path,
        exc_info=exception,
    )

    return create_error_response(
        status_code=500,
        error_code="internal_server_error",
        message="An unexpected error occurred.",
    )

def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    application.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    application.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )