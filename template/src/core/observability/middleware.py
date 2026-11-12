import time
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint
import structlog

from src.core.exceptions.handlers import unexpected_error_handler

log = structlog.get_logger()


async def request_context(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id, method=request.method, path=request.url.path
    )
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        response = await unexpected_error_handler(request, exc)
    response.headers["X-Request-ID"] = request_id
    log.info(
        "request.completed",
        status=response.status_code,
        duration_ms=round((time.perf_counter() - started) * 1000, 1),
    )
    return response
