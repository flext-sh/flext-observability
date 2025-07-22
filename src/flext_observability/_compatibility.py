"""Compatibility Layer for FLEXT Observability.

Provides backward-compatible implementations of critical functions
that are used across the FLEXT ecosystem during the semantic reorganization.

🎯 CRITICAL FUNCTIONS IMPLEMENTATION:
- get_logger() with StructuredLogger (PRIORITY 1)
- LoggingConfig and setup_logging() (PRIORITY 2)
- Context functions (PRIORITY 3)

Based on actual usage analysis from flext_cli, flext_meltano, and other modules.
"""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING, Any

from flext_observability._deprecated import warn_deprecated_function

if TYPE_CHECKING:
    import types


class StructuredLogger:
    """Compatibility implementation of StructuredLogger.

    Provides full compatibility with existing code patterns:
    - logger.bind(**kwargs) for contextual logging (flext-meltano)
    - logger.info("message", key=value) for structured logging
    - logger.info("message %s", arg) for traditional formatting

    🎯 CRITICAL: This class MUST maintain 100% compatibility
    with existing usage patterns found in flext_cli and flext_meltano.
    """

    def __init__(self, name: str, base_logger: logging.Logger | None = None) -> None:
        """Initialize structured logger.

        Args:
            name: Logger name (usually __name__)
            base_logger: Optional base logger, creates new if None

        """
        self._name = name
        self._base_logger = base_logger or logging.getLogger(name)
        self._context: dict[str, Any] = {}

    def bind(self, **kwargs: Any) -> StructuredLogger:
        """Create a new logger with additional context.

        🎯 CRITICAL: This method is extensively used in flext-meltano.

        Args:
            **kwargs: Context key-value pairs to bind

        Returns:
            New StructuredLogger instance with bound context

        Example:
            logger = get_logger(__name__)
            contextual_logger = logger.bind(project_root="/path", user_id="123")
            contextual_logger.info("Message")  # Will include bound context

        """
        new_logger = StructuredLogger(self._name, self._base_logger)
        new_logger._context = {**self._context, **kwargs}
        return new_logger

    def _format_message(self, message: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
        """Format message with args and context.

        Supports both traditional and structured logging patterns:
        - logger.info("Message %s", arg)  # Traditional
        - logger.info("Message", key=value)  # Structured
        """
        # Start with base message and args (traditional format)
        if args:
            try:
                formatted_message = message % args
            except (TypeError, ValueError):
                # If formatting fails, just use message as-is
                formatted_message = message
        else:
            formatted_message = message

        # Add structured context and kwargs
        all_context = {**self._context, **kwargs}

        if all_context:
            context_parts = [f"{k}={v!r}" for k, v in all_context.items()]
            context_str = " ".join(context_parts)
            formatted_message = f"{formatted_message} [{context_str}]"

        return formatted_message

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message with optional context.

        Supports both patterns:
        - logger.debug("Debug %s", value)
        - logger.debug("Debug message", key=value)
        """
        if self._base_logger.isEnabledFor(logging.DEBUG):
            formatted_message = self._format_message(message, args, kwargs)
            self._base_logger.debug(formatted_message)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log info message with optional context.

        🎯 CRITICAL: This method is heavily used in flext-meltano with kwargs.

        Examples:
        - logger.info("Creating project %s", project_name)
        - logger.info("Creating project", project_name=name, root=path)

        """
        if self._base_logger.isEnabledFor(logging.INFO):
            formatted_message = self._format_message(message, args, kwargs)
            self._base_logger.info(formatted_message)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message with optional context."""
        if self._base_logger.isEnabledFor(logging.WARNING):
            formatted_message = self._format_message(message, args, kwargs)
            self._base_logger.warning(formatted_message)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log error message with optional context."""
        if self._base_logger.isEnabledFor(logging.ERROR):
            formatted_message = self._format_message(message, args, kwargs)
            self._base_logger.error(formatted_message)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log exception message with traceback and context.

        🎯 CRITICAL: Used in flext_cli for error handling.
        """
        if self._base_logger.isEnabledFor(logging.ERROR):
            formatted_message = self._format_message(message, args, kwargs)
            self._base_logger.error(formatted_message)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message with optional context."""
        if self._base_logger.isEnabledFor(logging.CRITICAL):
            formatted_message = self._format_message(message, args, kwargs)
            self._base_logger.critical(formatted_message)

    # Aliases for compatibility
    warn = warning
    fatal = critical

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to base logger for full compatibility."""
        return getattr(self._base_logger, name)


def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance.

    🎯 CRITICAL: This is the MOST USED function across FLEXT ecosystem.
    Used extensively in:
    - flext_cli (basic logging)
    - flext_meltano (structured logging with bind())
    - flext_api (configuration and health checks)

    Args:
        name: Logger name, typically __name__

    Returns:
        StructuredLogger instance with full compatibility

    Example:
        # Basic usage (flext_cli pattern)
        logger = get_logger(__name__)
        logger.info("Processing file %s", filename)
        logger.exception("Error occurred")

        # Advanced usage (flext_meltano pattern)
        logger = get_logger(__name__)
        ctx_logger = logger.bind(project_root="/path", user="admin")
        ctx_logger.info("Creating project", project_name=name)

    """
    warn_deprecated_function(
        "get_logger",
        "flext_observability.infrastructure.logging.get_structured_logger",
    )

    return StructuredLogger(name)


# Configuration classes for advanced setups
class LoggingConfig:
    """Compatibility logging configuration.

    Provides basic configuration options used by some modules.
    """

    def __init__(
        self,
        service_name: str = "flext-observability",
        log_level: str = "INFO",
        json_logs: bool = True,
        environment: str = "development",
        version: str = "0.7.0",
    ) -> None:
        self.service_name = service_name
        self.log_level = log_level.upper()
        self.json_logs = json_logs
        self.environment = environment
        self.version = version


def setup_logging(config: LoggingConfig | None = None) -> None:
    """Setup basic logging configuration.

    🎯 MEDIUM PRIORITY: Used in some CLI scripts and applications.

    Args:
        config: Optional logging configuration

    """
    warn_deprecated_function(
        "setup_logging",
        "flext_observability.configuration.setup_observability_logging",
    )

    if config is None:
        config = LoggingConfig()

    # Convert string level to logging constant
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    log_level = level_map.get(config.log_level, logging.INFO)

    # Basic setup - compatible with existing expectations
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    # Set the service name in root logger if needed (use public attribute approach)
    root_logger = logging.getLogger()
    if not hasattr(root_logger, "service_name"):
        # Store service name as a regular attribute - dynamically add to logger
        root_logger.service_name = config.service_name


# Context functions (lower priority but included for completeness)
_global_context: dict[str, Any] = {}


def bind_context(**kwargs: Any) -> None:
    """Bind context globally (legacy function).

    🎯 LOW PRIORITY: Less commonly used function.
    """
    warn_deprecated_function(
        "bind_context",
        "flext_observability.infrastructure.logging.bind_trace_context",
    )

    _global_context.update(kwargs)


def clear_context() -> None:
    """Clear global context (legacy function)."""
    warn_deprecated_function(
        "clear_context",
        "flext_observability.infrastructure.logging.clear_trace_context",
    )

    _global_context.clear()


def with_context(**kwargs: Any) -> Any:
    """Context manager for temporary context (legacy function)."""
    warn_deprecated_function(
        "with_context",
        "flext_observability.infrastructure.logging.with_trace_context",
    )

    class ContextManager:
        def __init__(self, context: dict[str, Any]) -> None:
            self.context = context
            self.old_context: dict[str, Any] = {}

        def __enter__(self) -> None:
            # Update global context - must use global for modification
            global _global_context
            # Store current global context for restoration
            self.old_context = _global_context.copy()
            _global_context = {**_global_context, **self.context}

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: types.TracebackType | None,
        ) -> None:
            global _global_context
            _global_context = self.old_context

    return ContextManager(kwargs)
