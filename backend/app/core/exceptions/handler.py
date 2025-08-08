import logging
from uuid import uuid4

from fastapi import HTTPException, Request
from fastapi.exception_handlers import (
    http_exception_handler as default_http_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse, Response

from ...data.enums import ErrorCode
from ...data.models.responses import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


async def http_exception_handler(
    request: Request, exc: Exception
) -> Response | JSONResponse:
    if not isinstance(exc, HTTPException):
        return await default_http_exception_handler(request, exc)

    error_reference = uuid4().hex
    logger.error(
        "HTTP error | Status: %s | Detail: %s | Ref: %s",
        exc.status_code,
        exc.detail,
        error_reference,
        extra={"error_reference": error_reference},
    )

    error_code = ErrorCode.INTERNAL_SERVER_ERROR
    if exc.status_code == 400:
        error_code = ErrorCode.INVALID_ARGUMENTS
    elif exc.status_code == 404:
        error_code = ErrorCode.RESOURCE_NOT_FOUND

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=error_code.code,
            message=exc.detail or error_code.message,
            error_reference=error_reference,
        ).model_dump(mode="json", exclude_none=True),
    )


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )

    error_reference = uuid4().hex
    errors = [
        ErrorDetail.of(
            field=".".join(map(str, error["loc"][1:])),
            message=error["msg"],
            rejected_value=str(error.get("input"))[:100]
            if error.get("input")
            else None,
        )
        for error in exc.errors()
    ]

    logger.warning(
        "Validation error | Ref: %s | Errors: %d",
        error_reference,
        len(errors),
        extra={"error_reference": error_reference},
    )

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            code=ErrorCode.INVALID_ARGUMENTS.code,
            message=ErrorCode.INVALID_ARGUMENTS.message,
            errors=errors,
            error_reference=error_reference,
        ).model_dump(mode="json", exclude_none=True),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_reference = uuid4().hex
    logger.exception(
        "Unexpected error | Ref: %s | Path: %s",
        error_reference,
        request.url.path,
        exc_info=exc,
        extra={"error_reference": error_reference},
    )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            code=ErrorCode.INTERNAL_SERVER_ERROR.code,
            message=ErrorCode.INTERNAL_SERVER_ERROR.message,
            error_reference=error_reference,
        ).model_dump(mode="json", exclude_none=True),
    )
