"""Structured logging implementation using flext-core patterns.

Copyright (c) 2025, client-a. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

from flext_core import BaseConfig, LogLevel

if TYPE_CHECKING:
    import types


class LoggingConfig(BaseConfig):
    """Configuration for logging using flext-core patterns."""

    service_name: str = "flext-infrastructure.monitoring.flext-observability"
    log_level: LogLevel = LogLevel.INFO
    json_logs: bool = True
    environment: str = "development"
    version: str = "0.7.0"


# Context variables for structured logging
_logging_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "logging_context",
    default=None,
)


class StructuredLogger:
    """Structured logger wrapper that accepts keyword arguments."""

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger
        self._bound_context: dict[str, Any] = {}

    def _format_message(self, message: str, **kwargs: Any) -> str:
        """Format message with structured data."""
        # Merge bound context with current kwargs
        all_context = {**getattr(self, "_bound_context", {}), **kwargs}
        if all_context:
            extras = " ".join(f"{k}={v}" for k, v in all_context.items())
            return f"{message} [{extras}]"
        return message

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message with structured data."""
        # Support % formatting for performance and linting compliance
        formatted_message = message % args if args else message
        self._logger.debug(self._format_message(formatted_message, **kwargs))

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log info message with structured data."""
        # Support % formatting for performance and linting compliance
        formatted_message = message % args if args else message
        self._logger.info(self._format_message(formatted_message, **kwargs))

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message with structured data."""
        # Support % formatting for performance and linting compliance
        formatted_message = message % args if args else message
        self._logger.warning(self._format_message(formatted_message, **kwargs))

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log error message with structured data."""
        # Support % formatting for performance and linting compliance
        formatted_message = message % args if args else message
        self._logger.error(self._format_message(formatted_message, **kwargs))

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log exception message with structured data."""
        # Support % formatting for performance and linting compliance
        formatted_message = message % args if args else message
        self._logger.error(self._format_message(formatted_message, **kwargs))

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message with structured data."""
        # Support % formatting for performance and linting compliance
        formatted_message = message % args if args else message
        self._logger.critical(self._format_message(formatted_message, **kwargs))

    def bind(self, **kwargs: Any) -> StructuredLogger:
        """Create a new logger with bound context (for compatibility)."""
        # Create a new logger instance with bound context
        new_logger = StructuredLogger(self._logger)
        new_logger._bound_context = {**getattr(self, "_bound_context", {}), **kwargs}
        return new_logger


def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger with flext-core configuration."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return StructuredLogger(logger)


def setup_logging(config: LoggingConfig | None = None) -> None:
    """Setup logging configuration."""
    if config is None:
        config = LoggingConfig()

    # Handle LogLevel enum correctly
    log_level = config.log_level
    level_name = (
        log_level.value.upper()
        if hasattr(log_level, "value")
        else str(log_level).upper()
    )

    logging.basicConfig(
        level=getattr(logging, level_name),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def bind_context(**kwargs: Any) -> None:
    """Bind context variables for structured logging."""
    current = _logging_context.get() or {}
    current.update(kwargs)
    _logging_context.set(current)


def clear_context() -> None:
    """Clear logging context."""
    _logging_context.set({})


def with_context(**kwargs: Any) -> Any:
    """Context manager for temporary logging context."""

    class ContextManager:
        def __enter__(self) -> Any:
            self.old_context = _logging_context.get() or {}
            new_context = self.old_context.copy()
            new_context.update(kwargs)
            _logging_context.set(new_context)
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: types.TracebackType | None,
        ) -> None:
            _logging_context.set(self.old_context)

    return ContextManager()


__all__ = [
    "LoggingConfig",
    "bind_context",
    "clear_context",
    "get_logger",
    "setup_logging",
    "with_context",
]
