from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
import structlog

from src.core.exceptions.base import AppError, ValidationFailedError

log = structlog.get_logger()


def problem(
    request: Request, status: int, title: str, detail: str, **extra: object
) -> JSONResponse:
    return JSONResponse(
        {
            "type": title.lower().replace(" ", "-"),
            "title": title,
            "status": status,
            "detail": detail,
            "instance": request.url.path,
            "request_id": structlog.contextvars.get_contextvars().get("request_id"),
            **extra,
        },
        status_code=status,
        media_type="application/problem+json",
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    if exc.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        log.error("app.error", title=exc.title, detail=exc.detail, exc_info=exc)
    else:
        log.warning("app.error", title=exc.title, detail=exc.detail)
    return problem(request, exc.status_code, exc.title, exc.detail)


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    response = problem(
        request, exc.status_code, HTTPStatus(exc.status_code).phrase, exc.detail
    )
    response.headers.update(exc.headers or {})
    return response


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error = ValidationFailedError()
    errors = [
        {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
        for err in exc.errors()
    ]
    return problem(request, error.status_code, error.title, error.detail, errors=errors)


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error("unexpected.error", exc_info=exc)
    error = AppError()
    return problem(request, error.status_code, error.title, error.detail)


def register_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(AppError)(app_error_handler)
    app.exception_handler(HTTPException)(http_error_handler)
    app.exception_handler(RequestValidationError)(validation_error_handler)
