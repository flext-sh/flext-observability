"""FLEXT Structured Logging - Advanced Observability Logging Infrastructure.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Advanced structured logging capabilities extending flext-core logging with
observability-specific features including correlation ID management, contextual
metadata binding, and comprehensive observability context propagation across
distributed services in the FLEXT ecosystem.

This module provides enterprise-grade structured logging infrastructure specifically
designed for observability scenarios, supporting correlation tracking, contextual
enrichment, and comprehensive operational visibility across microservices and
data processing pipelines with performance optimization and reliability.

Key Components:
    - FlextStructuredLogger: Advanced structured logger with observability context
    - Correlation ID management with context variable propagation
    - Contextual metadata binding for enriched logging across request lifecycles
    - Observability-specific logging methods with structured data integration
    - Thread-safe context management for concurrent request processing

Architecture:
    Infrastructure layer component providing advanced logging capabilities
    specialized for observability use cases. Extends flext-core logging patterns
    while maintaining compatibility and adding observability-specific features.

Integration:
    - Extends flext-core logging capabilities for observability scenarios
    - Used by FlextLoggingService for comprehensive log management
    - Provides correlation tracking across distributed service calls
    - Supports operational debugging and request tracing infrastructure

Example:
    Advanced structured logging with correlation tracking and context binding:

    >>> from flext_observability.flext_structured import (
    ...     flext_get_structured_logger, flext_set_correlation_id
    ... )
    >>>
    >>> # Set correlation ID for request tracking
    >>> flext_set_correlation_id("req_abc123def456")
    >>>
    >>> # Get structured logger with observability context
    >>> logger = flext_get_structured_logger("user_service")
    >>> bound_logger = logger.flext_bind_observability(
    ...     user_id="12345", operation="user_login"
    ... )
    >>>
    >>> # Log with comprehensive observability context
    >>> bound_logger.flext_observability_info(
    ...     "User authentication successful",
    ...     response_time_ms=245, success_rate=0.98
    ... )

FLEXT Integration:
    Provides advanced structured logging infrastructure across all 33 FLEXT
    ecosystem projects, enabling comprehensive request tracing, operational
    debugging, and observability context propagation throughout the platform.

"""

from __future__ import annotations

from contextvars import ContextVar

from flext_core import FlextResult, get_logger

# ============================================================================
# OBSERVABILITY-SPECIFIC STRUCTURED LOGGING
# ============================================================================

# Context for correlation IDs and observability metadata
_flext_observability_context: ContextVar[dict[str, object] | None] = ContextVar(
    "flext_observability_context",
    default=None,
)


class FlextStructuredLogger:
    """Advanced Structured Logger for Observability Context and Correlation Tracking.

    Enterprise-grade structured logger extending flext-core logging capabilities
    with observability-specific features including correlation ID management,
    contextual metadata binding, and comprehensive request tracing across
    distributed services in the FLEXT ecosystem.

    This logger provides advanced structured logging with automatic context
    propagation, correlation tracking, and observability metadata integration
    designed for enterprise-scale debugging, monitoring, and operational
    visibility across microservices and data processing workflows.

    Responsibilities:
        - Structured logging with observability context integration
        - Correlation ID propagation across distributed service calls
        - Contextual metadata binding for enriched logging
        - Thread-safe context management for concurrent processing
        - Performance-optimized logging with minimal overhead
        - Integration with log aggregation and monitoring systems

    Context Management:
        Utilizes Python's contextvars for thread-safe correlation tracking
        and metadata propagation across async and concurrent execution
        contexts, ensuring consistent observability data across requests.

    Attributes:
        _core_logger: Underlying flext-core logger for actual log output
        _bound_data: Contextual metadata bound to this logger instance

    """

    def __init__(self, name: str) -> None:
        """Initialize with flext-core logger."""
        self._core_logger = get_logger(name)
        self._bound_data: dict[str, object] = {}

    def flext_observability_info(
        self,
        message: str,
        **observability_data: object,
    ) -> FlextResult[None]:
        """Log info with observability context."""
        try:
            context = _flext_observability_context.get() or {}
            all_data = {**context, **self._bound_data, **observability_data}

            if all_data:
                extras = " | ".join(f"{k}={v}" for k, v in all_data.items())
                formatted_message = f"{message} | {extras}"
            else:
                formatted_message = message

            self._core_logger.info(formatted_message)
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Structured logging failed: {e}")

    def flext_observability_error(
        self,
        message: str,
        **observability_data: object,
    ) -> FlextResult[None]:
        """Log error with observability context."""
        try:
            context = _flext_observability_context.get() or {}
            all_data = {**context, **self._bound_data, **observability_data}

            if all_data:
                extras = " | ".join(f"{k}={v}" for k, v in all_data.items())
                formatted_message = f"{message} | {extras}"
            else:
                formatted_message = message

            self._core_logger.error(formatted_message)
            return FlextResult.ok(None)
        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Structured logging failed: {e}")

    def flext_bind_observability(
        self,
        **data: object,
    ) -> FlextStructuredLogger:
        """Bind observability-specific data to logger."""
        new_logger = FlextStructuredLogger(self._core_logger.__class__.__name__)
        new_logger._core_logger = self._core_logger
        new_logger._bound_data = {**self._bound_data, **data}
        return new_logger


def flext_set_correlation_id(correlation_id: str) -> FlextResult[None]:
    """Set correlation ID for observability context."""
    try:
        context = _flext_observability_context.get() or {}.copy()
        context["correlation_id"] = correlation_id
        _flext_observability_context.set(context)
        return FlextResult.ok(None)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to set correlation ID: {e}")


def flext_get_correlation_id() -> FlextResult[str]:
    """Get current correlation ID."""
    try:
        context = _flext_observability_context.get(None)
        # If context is explicitly None, return empty string
        if context is None:
            return FlextResult.ok("")
        correlation_id = context.get("correlation_id", "")
        correlation_id_str = str(correlation_id) if correlation_id else ""
        return FlextResult.ok(correlation_id_str)
    except (ValueError, TypeError, AttributeError) as e:
        return FlextResult.fail(f"Failed to get correlation ID: {e}")


def flext_get_structured_logger(name: str) -> FlextStructuredLogger:
    """Get observability-specific structured logger."""
    return FlextStructuredLogger(name)


__all__ = [
    "FlextStructuredLogger",
    "flext_get_correlation_id",
    "flext_get_structured_logger",
    "flext_set_correlation_id",
]
