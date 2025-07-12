"""Structured logging implementation using flext-core patterns.

Copyright (c) 2025, client-a. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar
from typing import Any

from flext_core import BaseConfig
from flext_core import LogLevel


class LoggingConfig(BaseConfig):
    """Configuration for logging using flext-core patterns."""

    service_name: str = "flext-observability"
    log_level: LogLevel = LogLevel.INFO
    json_logs: bool = True
    environment: str = "development"
    version: str = "0.7.0"


# Context variables for structured logging
_logging_context: ContextVar[dict[str, Any] | None] = ContextVar("logging_context", default=None)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with flext-core configuration."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def setup_logging(config: LoggingConfig | None = None) -> None:
    """Setup logging configuration."""
    if config is None:
        config = LoggingConfig()

    # Handle LogLevel enum correctly
    log_level = config.log_level
    level_name = log_level.value.upper() if hasattr(log_level, "value") else str(log_level).upper()

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

        def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
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
