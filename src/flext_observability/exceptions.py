"""FLEXT Observability domain-specific exceptions.

This module provides observability-specific exceptions using the modern FlextErrorMixin
pattern from flext-core. All exceptions follow Pydantic v2 error handling patterns and
support structured error context for comprehensive observability error reporting.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import Enum

from flext_core import FlextError
from flext_core.exceptions import FlextErrorMixin


class FlextObservabilityErrorCodes(Enum):
    """Error codes for observability domain operations."""

    # Metrics errors
    INVALID_METRIC_NAME = "INVALID_METRIC_NAME"
    INVALID_METRIC_VALUE = "INVALID_METRIC_VALUE"
    METRIC_COLLECTION_FAILED = "METRIC_COLLECTION_FAILED"
    METRIC_EXPORT_FAILED = "METRIC_EXPORT_FAILED"

    # Tracing errors
    INVALID_TRACE_NAME = "INVALID_TRACE_NAME"
    TRACE_CONTEXT_INVALID = "TRACE_CONTEXT_INVALID"
    TRACE_EXPORT_FAILED = "TRACE_EXPORT_FAILED"
    SPAN_CREATION_FAILED = "SPAN_CREATION_FAILED"

    # Alert errors
    INVALID_ALERT_SEVERITY = "INVALID_ALERT_SEVERITY"
    ALERT_ROUTING_FAILED = "ALERT_ROUTING_FAILED"
    ALERT_THRESHOLD_INVALID = "ALERT_THRESHOLD_INVALID"

    # Health check errors
    HEALTH_CHECK_FAILED = "HEALTH_CHECK_FAILED"
    HEALTH_DEPENDENCY_TIMEOUT = "HEALTH_DEPENDENCY_TIMEOUT"
    HEALTH_VALIDATION_FAILED = "HEALTH_VALIDATION_FAILED"

    # Logging errors
    LOG_FORMATTING_FAILED = "LOG_FORMATTING_FAILED"
    LOG_EXPORT_FAILED = "LOG_EXPORT_FAILED"
    CORRELATION_ID_INVALID = "CORRELATION_ID_INVALID"

    # Platform errors
    OBSERVABILITY_PLATFORM_INIT_FAILED = "OBSERVABILITY_PLATFORM_INIT_FAILED"
    SERVICE_REGISTRATION_FAILED = "SERVICE_REGISTRATION_FAILED"
    TELEMETRY_EXPORT_FAILED = "TELEMETRY_EXPORT_FAILED"


# Base observability exception using FlextErrorMixin pattern
class FlextObservabilityError(FlextErrorMixin, FlextError):
    """Base exception for all observability domain errors."""


# Metrics domain exceptions
class FlextObservabilityMetricsError(FlextObservabilityError):
    """Base exception for metrics-related errors."""


class FlextObservabilityInvalidMetricError(FlextObservabilityMetricsError):
    """Raised when metric validation fails."""


class FlextObservabilityMetricCollectionError(FlextObservabilityMetricsError):
    """Raised when metric collection fails."""


class FlextObservabilityMetricExportError(FlextObservabilityMetricsError):
    """Raised when metric export to external systems fails."""


# Tracing domain exceptions
class FlextObservabilityTracingError(FlextObservabilityError):
    """Base exception for tracing-related errors."""


class FlextObservabilityInvalidTraceError(FlextObservabilityTracingError):
    """Raised when trace validation fails."""


class FlextObservabilityTraceExportError(FlextObservabilityTracingError):
    """Raised when trace export to external systems fails."""


class FlextObservabilitySpanError(FlextObservabilityTracingError):
    """Raised when span operations fail."""


# Alert domain exceptions
class FlextObservabilityAlertError(FlextObservabilityError):
    """Base exception for alert-related errors."""


class FlextObservabilityInvalidAlertError(FlextObservabilityAlertError):
    """Raised when alert validation fails."""


class FlextObservabilityAlertRoutingError(FlextObservabilityAlertError):
    """Raised when alert routing fails."""


# Health check domain exceptions
class FlextObservabilityHealthError(FlextObservabilityError):
    """Base exception for health check-related errors."""


class FlextObservabilityHealthCheckError(FlextObservabilityHealthError):
    """Raised when health checks fail."""


class FlextObservabilityHealthTimeoutError(FlextObservabilityHealthError):
    """Raised when health check dependencies timeout."""


# Logging domain exceptions
class FlextObservabilityLoggingError(FlextObservabilityError):
    """Base exception for logging-related errors."""


class FlextObservabilityLogFormattingError(FlextObservabilityLoggingError):
    """Raised when log formatting fails."""


class FlextObservabilityCorrelationError(FlextObservabilityLoggingError):
    """Raised when correlation ID handling fails."""


# Platform domain exceptions
class FlextObservabilityPlatformError(FlextObservabilityError):
    """Base exception for platform-related errors."""


class FlextObservabilityInitializationError(FlextObservabilityPlatformError):
    """Raised when observability platform initialization fails."""


class FlextObservabilityServiceError(FlextObservabilityPlatformError):
    """Raised when observability service registration or operation fails."""


class FlextObservabilityTelemetryError(FlextObservabilityPlatformError):
    """Raised when telemetry export operations fail."""


# Factory class for creating observability exceptions with proper context
class FlextObservabilityExceptionFactory:
    """Factory for creating observability exceptions with structured context."""

    @classmethod
    def invalid_metric(
        cls,
        metric_name: str,
        *,
        reason: str,
        value: object | None = None,
        unit: str | None = None,
    ) -> FlextObservabilityInvalidMetricError:
        """Create invalid metric exception with metric context."""
        context = {"metric_name": metric_name, "reason": reason}
        if value is not None:
            context["value"] = str(value)
        if unit is not None:
            context["unit"] = unit

        return FlextObservabilityInvalidMetricError(
            f"Invalid metric '{metric_name}': {reason}",
            code=FlextObservabilityErrorCodes.INVALID_METRIC_NAME,
            context=context,
        )

    @classmethod
    def metric_collection_failed(
        cls,
        metric_name: str,
        *,
        error: str,
        collector: str | None = None,
    ) -> FlextObservabilityMetricCollectionError:
        """Create metric collection failure exception."""
        context = {"metric_name": metric_name, "error": error}
        if collector:
            context["collector"] = collector

        return FlextObservabilityMetricCollectionError(
            f"Metric collection failed for '{metric_name}': {error}",
            code=FlextObservabilityErrorCodes.METRIC_COLLECTION_FAILED,
            context=context,
        )

    @classmethod
    def invalid_trace(
        cls,
        trace_name: str,
        *,
        reason: str,
        operation: str | None = None,
    ) -> FlextObservabilityInvalidTraceError:
        """Create invalid trace exception with trace context."""
        context = {"trace_name": trace_name, "reason": reason}
        if operation:
            context["operation"] = operation

        return FlextObservabilityInvalidTraceError(
            f"Invalid trace '{trace_name}': {reason}",
            code=FlextObservabilityErrorCodes.INVALID_TRACE_NAME,
            context=context,
        )

    @classmethod
    def trace_export_failed(
        cls,
        trace_name: str,
        *,
        error: str,
        exporter: str | None = None,
    ) -> FlextObservabilityTraceExportError:
        """Create trace export failure exception."""
        context = {"trace_name": trace_name, "error": error}
        if exporter:
            context["exporter"] = exporter

        return FlextObservabilityTraceExportError(
            f"Trace export failed for '{trace_name}': {error}",
            code=FlextObservabilityErrorCodes.TRACE_EXPORT_FAILED,
            context=context,
        )

    @classmethod
    def invalid_alert(
        cls,
        alert_name: str,
        *,
        reason: str,
        severity: str | None = None,
    ) -> FlextObservabilityInvalidAlertError:
        """Create invalid alert exception with alert context."""
        context = {"alert_name": alert_name, "reason": reason}
        if severity:
            context["severity"] = severity

        return FlextObservabilityInvalidAlertError(
            f"Invalid alert '{alert_name}': {reason}",
            code=FlextObservabilityErrorCodes.INVALID_ALERT_SEVERITY,
            context=context,
        )

    @classmethod
    def health_check_failed(
        cls,
        check_name: str,
        *,
        error: str,
        dependency: str | None = None,
        timeout_seconds: int | None = None,
    ) -> FlextObservabilityHealthCheckError:
        """Create health check failure exception."""
        context = {"check_name": check_name, "error": error}
        if dependency:
            context["dependency"] = dependency
        if timeout_seconds:
            context["timeout_seconds"] = timeout_seconds

        return FlextObservabilityHealthCheckError(
            f"Health check failed for '{check_name}': {error}",
            code=FlextObservabilityErrorCodes.HEALTH_CHECK_FAILED,
            context=context,
        )

    @classmethod
    def platform_initialization_failed(
        cls,
        component: str,
        *,
        error: str,
        service: str | None = None,
    ) -> FlextObservabilityInitializationError:
        """Create platform initialization failure exception."""
        context = {"component": component, "error": error}
        if service:
            context["service"] = service

        return FlextObservabilityInitializationError(
            f"Observability platform initialization failed for '{component}': {error}",
            code=FlextObservabilityErrorCodes.OBSERVABILITY_PLATFORM_INIT_FAILED,
            context=context,
        )


__all__ = [
    # Alert exceptions
    "FlextObservabilityAlertError",
    "FlextObservabilityAlertRoutingError",
    "FlextObservabilityCorrelationError",
    # Base exceptions
    "FlextObservabilityError",
    # Error codes
    "FlextObservabilityErrorCodes",
    # Factory
    "FlextObservabilityExceptionFactory",
    "FlextObservabilityHealthCheckError",
    # Health check exceptions
    "FlextObservabilityHealthError",
    "FlextObservabilityHealthTimeoutError",
    "FlextObservabilityInitializationError",
    "FlextObservabilityInvalidAlertError",
    "FlextObservabilityInvalidMetricError",
    "FlextObservabilityInvalidTraceError",
    "FlextObservabilityLogFormattingError",
    # Logging exceptions
    "FlextObservabilityLoggingError",
    "FlextObservabilityMetricCollectionError",
    "FlextObservabilityMetricExportError",
    # Metrics exceptions
    "FlextObservabilityMetricsError",
    # Platform exceptions
    "FlextObservabilityPlatformError",
    "FlextObservabilityServiceError",
    "FlextObservabilitySpanError",
    "FlextObservabilityTelemetryError",
    "FlextObservabilityTraceExportError",
    # Tracing exceptions
    "FlextObservabilityTracingError",
]
