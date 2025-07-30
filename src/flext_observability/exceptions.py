"""Observability exception hierarchy using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for observability operations inheriting from flext-core.
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextTimeoutError,
    FlextValidationError,
)


class FlextObservabilityError(FlextError):
    """Base exception for observability operations."""

    def __init__(
        self,
        message: str = "Observability error",
        component: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability error with context."""
        context = kwargs.copy()
        if component is not None:
            context["component"] = component

        super().__init__(message, error_code="OBSERVABILITY_ERROR", context=context)


class FlextObservabilityConfigurationError(FlextConfigurationError):
    """Observability configuration errors."""

    def __init__(
        self,
        message: str = "Observability configuration error",
        config_key: str | None = None,
        component: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability configuration error with context."""
        context = kwargs.copy()
        if config_key is not None:
            context["config_key"] = config_key
        if component is not None:
            context["component"] = component

        super().__init__(f"Observability config: {message}", **context)


class FlextObservabilityValidationError(FlextValidationError):
    """Observability validation errors."""

    def __init__(
        self,
        message: str = "Observability validation failed",
        field: str | None = None,
        value: object = None,
        metric_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability validation error with context."""
        validation_details: dict[str, object] = {}
        if field is not None:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = str(value)[:100]  # Truncate long values

        context = kwargs.copy()
        if metric_name is not None:
            context["metric_name"] = metric_name

        super().__init__(
            f"Observability validation: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextObservabilityConnectionError(FlextConnectionError):
    """Observability connection errors."""

    def __init__(
        self,
        message: str = "Observability connection failed",
        endpoint: str | None = None,
        service_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability connection error with context."""
        context = kwargs.copy()
        if endpoint is not None:
            context["endpoint"] = endpoint
        if service_name is not None:
            context["service_name"] = service_name

        super().__init__(f"Observability connection: {message}", **context)


class FlextObservabilityProcessingError(FlextProcessingError):
    """Observability processing errors."""

    def __init__(
        self,
        message: str = "Observability processing failed",
        operation: str | None = None,
        metric_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability processing error with context."""
        context = kwargs.copy()
        if operation is not None:
            context["operation"] = operation
        if metric_name is not None:
            context["metric_name"] = metric_name

        super().__init__(f"Observability processing: {message}", **context)


class FlextObservabilityTimeoutError(FlextTimeoutError):
    """Observability timeout errors."""

    def __init__(
        self,
        message: str = "Observability operation timed out",
        operation: str | None = None,
        timeout_seconds: float | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability timeout error with context."""
        context = kwargs.copy()
        if operation is not None:
            context["operation"] = operation
        if timeout_seconds is not None:
            context["timeout_seconds"] = timeout_seconds

        super().__init__(f"Observability timeout: {message}", **context)


class FlextObservabilityMetricsError(FlextObservabilityError):
    """Observability metrics-specific errors."""

    def __init__(
        self,
        message: str = "Observability metrics error",
        metric_type: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability metrics error with context."""
        context = kwargs.copy()
        if metric_type is not None:
            context["metric_type"] = metric_type

        super().__init__(
            f"Observability metrics: {message}",
            component="metrics",
            **context,
        )


class FlextObservabilityHealthError(FlextObservabilityError):
    """Observability health check errors."""

    def __init__(
        self,
        message: str = "Observability health check failed",
        check_name: str | None = None,
        service_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability health error with context."""
        context = kwargs.copy()
        if check_name is not None:
            context["check_name"] = check_name
        if service_name is not None:
            context["service_name"] = service_name

        super().__init__(
            f"Observability health: {message}",
            component="health",
            **context,
        )


class FlextObservabilityTracingError(FlextObservabilityError):
    """Observability tracing-specific errors."""

    def __init__(
        self,
        message: str = "Observability tracing error",
        trace_id: str | None = None,
        span_name: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability tracing error with context."""
        context = kwargs.copy()
        if trace_id is not None:
            context["trace_id"] = trace_id
        if span_name is not None:
            context["span_name"] = span_name

        super().__init__(
            f"Observability tracing: {message}",
            component="tracing",
            **context,
        )


class FlextObservabilityLoggingError(FlextObservabilityError):
    """Observability logging-specific errors."""

    def __init__(
        self,
        message: str = "Observability logging error",
        logger_name: str | None = None,
        log_level: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize observability logging error with context."""
        context = kwargs.copy()
        if logger_name is not None:
            context["logger_name"] = logger_name
        if log_level is not None:
            context["log_level"] = log_level

        super().__init__(
            f"Observability logging: {message}",
            component="logging",
            **context,
        )


__all__ = [
    "FlextObservabilityConfigurationError",
    "FlextObservabilityConnectionError",
    "FlextObservabilityError",
    "FlextObservabilityHealthError",
    "FlextObservabilityLoggingError",
    "FlextObservabilityMetricsError",
    "FlextObservabilityProcessingError",
    "FlextObservabilityTimeoutError",
    "FlextObservabilityTracingError",
    "FlextObservabilityValidationError",
]
