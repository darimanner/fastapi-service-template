from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import health
from src.config.settings import settings
from src.core.db.sessions import engine
from src.core.exceptions.handlers import register_exception_handlers
from src.core.observability.logging import setup_logging
from src.core.observability.middleware import request_context


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    setup_logging(settings.logger.level, debug=settings.logger.debug)
    app = FastAPI(title=settings.app.name, lifespan=lifespan)
    app.middleware("http")(request_context)
    register_exception_handlers(app)
    app.include_router(health.router)
    return app


app = create_app()
