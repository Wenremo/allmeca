import logging
from uuid import uuid4

import structlog


processors = [
    structlog.contextvars.merge_contextvars,
    # structlog.processors.CallsiteParameterAdder(
    #     [
    #         structlog.processors.CallsiteParameter.FUNC_NAME,
    #         structlog.processors.CallsiteParameter.MODULE,
    #     ],
    # ),
    structlog.processors.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.TimeStamper(fmt="iso"),
]

processors.append(structlog.dev.set_exc_info)
processors.append(structlog.dev.ConsoleRenderer())

structlog.configure(
    processors=processors,
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

log = structlog.get_logger()


def log_id():
    return str(uuid4())
