import logging
import sys

import structlog
from structlog.typing import EventDict, FilteringBoundLogger, Processor, WrappedLogger

# A lazy proxy: it picks up the config from setup_logging on first use.
log: FilteringBoundLogger = structlog.get_logger()

SECRET_PARTS = ("password", "token", "secret", "authorization", "api_key", "cookie")


def mask_secrets(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    for key in event_dict:
        if any(part in key.lower() for part in SECRET_PARTS):
            event_dict[key] = "***"
    return event_dict


def setup_logging(level: str, *, debug: bool) -> None:
    shared: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        mask_secrets,
    ]
    renderers: list[Processor] = (
        [structlog.dev.ConsoleRenderer()]
        if debug
        else [structlog.processors.format_exc_info, structlog.processors.JSONRenderer()]
    )
    structlog.configure(
        processors=[*shared, *renderers],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                *renderers,
            ],
        )
    )
    # Root stays at WARNING: INFO would make SQLAlchemy log every statement.
    logging.basicConfig(handlers=[handler], level=logging.WARNING, force=True)
    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("uvicorn").propagate = True
    logging.getLogger("uvicorn.access").disabled = True
