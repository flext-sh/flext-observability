"""Unified observability creation utilities following FLEXT patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from flext_core import (
    FlextResult,
    FlextTypes,
)

from flext_observability.services import FlextObservabilityServices


class FlextObservabilityFactories:
    """Unified observability factories following namespace class pattern.

    Single unified class with nested helpers for all observability entity creation.
    Provides consolidated factory operations through nested factory classes.
    """

    class MetricFactory:
        """Nested factory for metric creation operations."""

        @staticmethod
        def create_metric(
            name: str,
            value: float,
            unit: str = "count",
            metadata: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a metric with proper validation and formatting."""
            try:
                # Validate inputs
                if not name or not isinstance(name, str):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Metric name must be a non-empty string"
                    )

                if not isinstance(value, (int, float)):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Metric value must be a number"
                    )

                metric: FlextTypes.Dict = {
                    "name": name.strip(),
                    "value": float(value),
                    "unit": unit,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "metadata": metadata or {},
                }

                return FlextResult[FlextTypes.Dict].ok(metric)
            except Exception as e:
                return FlextResult[FlextTypes.Dict].fail(f"Metric creation failed: {e}")

    class TraceFactory:
        """Nested factory for trace creation operations."""

        @staticmethod
        def create_trace(
            name: str,
            operation: str,
            context: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a trace with proper validation and formatting."""
            try:
                if not name or not isinstance(name, str):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Trace name must be a non-empty string"
                    )

                if not operation or not isinstance(operation, str):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Operation must be a non-empty string"
                    )

                trace_data: FlextTypes.Dict = {
                    "trace_id": str(uuid4()),
                    "span_id": str(uuid4()),
                    "name": name.strip(),
                    "operation": operation.strip(),
                    "start_time": datetime.now(UTC).isoformat(),
                    "context": context or {},
                    "status": "active",
                }

                return FlextResult[FlextTypes.Dict].ok(trace_data)
            except Exception as e:
                return FlextResult[FlextTypes.Dict].fail(f"Trace creation failed: {e}")

    class AlertFactory:
        """Nested factory for alert creation operations."""

        @staticmethod
        def create_alert(
            title: str,
            message: str,
            severity: str = "info",
            source: str = "system",
        ) -> FlextResult[FlextTypes.Dict]:
            """Create an alert with proper validation and formatting."""
            try:
                if not title or not isinstance(title, str):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Alert title must be a non-empty string"
                    )

                if not message or not isinstance(message, str):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Alert message must be a non-empty string"
                    )

                valid_severities = {"critical", "high", "medium", "low", "info"}
                if severity.lower() not in valid_severities:
                    return FlextResult[FlextTypes.Dict].fail(
                        f"Invalid severity '{severity}'. Must be one of: {', '.join(valid_severities)}"
                    )

                alert: FlextTypes.Dict = {
                    "alert_id": str(uuid4()),
                    "title": title.strip(),
                    "message": message.strip(),
                    "severity": severity.lower(),
                    "source": source,
                    "created_at": datetime.now(UTC).isoformat(),
                    "status": "active",
                }

                return FlextResult[FlextTypes.Dict].ok(alert)
            except Exception as e:
                return FlextResult[FlextTypes.Dict].fail(f"Alert creation failed: {e}")

    class HealthCheckFactory:
        """Nested factory for health check creation operations."""

        @staticmethod
        def create_health_check(
            service_name: str,
            status: str = "healthy",
            details: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a health check with proper validation and formatting."""
            try:
                if not service_name or not isinstance(service_name, str):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Service name must be a non-empty string"
                    )

                valid_statuses = {"healthy", "degraded", "unhealthy", "unknown"}
                if status.lower() not in valid_statuses:
                    return FlextResult[FlextTypes.Dict].fail(
                        f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                    )

                health_check: FlextTypes.Dict = {
                    "service_name": service_name.strip(),
                    "status": status.lower(),
                    "details": details or {},
                    "timestamp": datetime.now(UTC).isoformat(),
                    "check_id": str(uuid4()),
                }

                return FlextResult[FlextTypes.Dict].ok(health_check)
            except Exception as e:
                return FlextResult[FlextTypes.Dict].fail(
                    f"Health check creation failed: {e}"
                )

    class LogEntryFactory:
        """Nested factory for log entry creation operations."""

        @staticmethod
        def create_log_entry(
            level: str,
            message: str,
            metadata: FlextTypes.Dict | None = None,
        ) -> FlextResult[FlextTypes.Dict]:
            """Create a structured log entry with proper validation and formatting."""
            try:
                valid_levels = {"debug", "info", "warning", "error", "critical"}
                if level.lower() not in valid_levels:
                    return FlextResult[FlextTypes.Dict].fail(
                        f"Invalid log level '{level}'. Must be one of: {', '.join(valid_levels)}"
                    )

                if not message or not isinstance(message, str):
                    return FlextResult[FlextTypes.Dict].fail(
                        "Log message must be a non-empty string"
                    )

                log_entry: FlextTypes.Dict = {
                    "level": level.lower(),
                    "message": message.strip(),
                    "timestamp": datetime.now(UTC).isoformat(),
                    "correlation_id": str(uuid4()),
                    "metadata": metadata or {},
                }

                return FlextResult[FlextTypes.Dict].ok(log_entry)
            except Exception as e:
                return FlextResult[FlextTypes.Dict].fail(
                    f"Log entry creation failed: {e}"
                )

    class ServiceFactory:
        """Nested factory for service instance creation."""

        @staticmethod
        def get_global_observability_service() -> FlextObservabilityServices:
            """Get the global observability service instance."""
            return FlextObservabilityServices()


# Backward compatibility aliases - maintain ABI stability
def flext_create_metric(
    name: str,
    value: float,
    unit: str = "count",
    metadata: FlextTypes.Dict | None = None,
) -> FlextResult[FlextTypes.Dict]:
    """Create a metric (backward compatibility)."""
    return FlextObservabilityFactories.MetricFactory.create_metric(
        name, value, unit, metadata
    )


def flext_create_trace(
    name: str,
    operation: str,
    context: FlextTypes.Dict | None = None,
) -> FlextResult[FlextTypes.Dict]:
    """Create a trace (backward compatibility)."""
    return FlextObservabilityFactories.TraceFactory.create_trace(
        name, operation, context
    )


def flext_create_alert(
    title: str,
    message: str,
    severity: str = "info",
    source: str = "system",
) -> FlextResult[FlextTypes.Dict]:
    """Create an alert (backward compatibility)."""
    return FlextObservabilityFactories.AlertFactory.create_alert(
        title, message, severity, source
    )


def flext_create_health_check(
    service_name: str,
    status: str = "healthy",
    details: FlextTypes.Dict | None = None,
) -> FlextResult[FlextTypes.Dict]:
    """Create a health check (backward compatibility)."""
    return FlextObservabilityFactories.HealthCheckFactory.create_health_check(
        service_name, status, details
    )


def flext_create_log_entry(
    level: str,
    message: str,
    metadata: FlextTypes.Dict | None = None,
) -> FlextResult[FlextTypes.Dict]:
    """Create a log entry (backward compatibility)."""
    return FlextObservabilityFactories.LogEntryFactory.create_log_entry(
        level, message, metadata
    )


# Global service instance for backward compatibility
def get_global_observability_service() -> FlextObservabilityServices:
    """Get the global observability service instance (backward compatibility)."""
    return FlextObservabilityFactories.ServiceFactory.get_global_observability_service()


__all__ = [
    "FlextObservabilityFactories",
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "get_global_observability_service",
]
