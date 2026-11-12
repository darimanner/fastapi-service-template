import structlog
from structlog.typing import EventDict, Processor, WrappedLogger

SECRET_KEYS = frozenset({"password", "token", "secret", "authorization"})


def mask_secrets(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    for key in SECRET_KEYS & event_dict.keys():
        event_dict[key] = "***"
    return event_dict


def setup_logging(level: str, *, debug: bool) -> None:
    renderers: list[Processor] = (
        [structlog.dev.ConsoleRenderer()]
        if debug
        else [structlog.processors.format_exc_info, structlog.processors.JSONRenderer()]
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            mask_secrets,
            *renderers,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )
