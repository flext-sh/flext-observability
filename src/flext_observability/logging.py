"""Logging infrastructure for FLEXT Observability.

This module provides the OFFICIAL logging implementation for all FLEXT projects.
Uses flext-core patterns and structured logging with proper observability.
"""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING
from typing import Any

import structlog
from structlog.contextvars import bind_contextvars
from structlog.contextvars import clear_contextvars

from flext_core.config import BaseConfig
from flext_core.domain.types import FlextConstants
from flext_core.domain.types import LogLevel

if TYPE_CHECKING:
    from structlog.typing import Processor


class LoggingConfig(BaseConfig):
    """Configuration for logging using flext-core patterns."""

    service_name: str = "flext-observability"
    log_level: LogLevel = LogLevel.INFO
    json_logs: bool = True
    environment: str = "development"
    version: str = FlextConstants.FRAMEWORK_VERSION
    include_correlation_id: bool = True
    include_trace_info: bool = True


def setup_logging(
    service_name: str = "flext-observability",
    log_level: str = "INFO",
    json_logs: bool = True,
    environment: str = "development",
    version: str = "0.7.0",
) -> None:
    """Setup structured logging configuration.

    Args:
        service_name: Name of the service for log context
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Whether to output logs in JSON format
        environment: Environment name (development, staging, production)
        version: Service version
    """
    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # Configure structlog processors
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # Add JSON or console formatting based on configuration
    if json_logs:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Bind global context
    bind_contextvars(
        service=service_name,
        environment=environment,
        version=version,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured structured logger
    """
    return structlog.get_logger(name)


def bind_context(**kwargs: Any) -> None:
    """Bind additional context to all logs in current context.

    Args:
        **kwargs: Key-value pairs to bind to logging context
    """
    bind_contextvars(**kwargs)


def clear_context() -> None:
    """Clear all context variables."""
    clear_contextvars()


def with_context(**kwargs: Any) -> Any:
    """Decorator to bind context to a function's logging.

    Args:
        **kwargs: Key-value pairs to bind to logging context

    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **func_kwargs):
            bind_context(**kwargs)
            try:
                return func(*args, **func_kwargs)
            finally:
                clear_context()
        return wrapper
    return decorator


# Default logger for the module
logger = get_logger(__name__)
