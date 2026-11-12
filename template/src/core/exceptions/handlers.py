from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import structlog

from src.core.exceptions.base import AppError, ValidationFailedError

log = structlog.get_logger()


def problem(request: Request, error: AppError, **extra: object) -> JSONResponse:
    return JSONResponse(
        {
            "type": error.error_type,
            "title": error.title,
            "status": error.status_code,
            "detail": error.detail,
            "instance": request.url.path,
            "request_id": structlog.contextvars.get_contextvars().get("request_id"),
            **extra,
        },
        status_code=error.status_code,
        media_type="application/problem+json",
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    if exc.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        log.error("app.error", error_type=exc.error_type, detail=exc.detail, exc_info=exc)
    else:
        log.warning("app.error", error_type=exc.error_type, detail=exc.detail)
    return problem(request, exc)


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
        for err in exc.errors()
    ]
    return problem(request, ValidationFailedError(), errors=errors)


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error("unexpected.error", exc_info=exc)
    return problem(request, AppError())


def register_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(AppError)(app_error_handler)
    app.exception_handler(RequestValidationError)(validation_error_handler)
    app.exception_handler(Exception)(unexpected_error_handler)
