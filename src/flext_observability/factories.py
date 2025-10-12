"""Simplified observability creation utilities following FLEXT patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from flext_core import FlextCore

# Simplified factory functions - inline validation logic, no unnecessary nested classes


def flext_create_metric(
    name: str,
    value: float,
    unit: str = "count",
    metadata: FlextCore.Types.Dict | None = None,
) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Create a metric with inline validation."""
    try:
        if not name or not isinstance(name, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Metric name must be a non-empty string"
            )

        if not isinstance(value, (int, float)):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Metric value must be a number"
            )

        metric: FlextCore.Types.Dict = {
            "name": name.strip(),
            "value": float(value),
            "unit": unit,
            "timestamp": datetime.now(UTC).isoformat(),
            "metadata": metadata or {},
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(metric)
    except Exception as e:
        return FlextCore.Result[FlextCore.Types.Dict].fail(
            f"Metric creation failed: {e}"
        )


def flext_create_trace(
    name: str,
    operation: str,
    context: FlextCore.Types.Dict | None = None,
) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Create a trace with inline validation."""
    try:
        if not name or not isinstance(name, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Trace name must be a non-empty string"
            )

        if not operation or not isinstance(operation, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Operation must be a non-empty string"
            )

        trace_data: FlextCore.Types.Dict = {
            "trace_id": str(uuid4()),
            "span_id": str(uuid4()),
            "name": name.strip(),
            "operation": operation.strip(),
            "start_time": datetime.now(UTC).isoformat(),
            "context": context or {},
            "status": "active",
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(trace_data)
    except Exception as e:
        return FlextCore.Result[FlextCore.Types.Dict].fail(
            f"Trace creation failed: {e}"
        )


def flext_create_alert(
    title: str,
    message: str,
    severity: str = "info",
    source: str = "system",
) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Create an alert with inline validation."""
    try:
        if not title or not isinstance(title, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Alert title must be a non-empty string"
            )

        if not message or not isinstance(message, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Alert message must be a non-empty string"
            )

        valid_severities = {"info", "warning", "error", "critical"}
        if severity not in valid_severities:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Invalid severity '{severity}'. Must be one of: {', '.join(valid_severities)}"
            )

        alert: FlextCore.Types.Dict = {
            "alert_id": str(uuid4()),
            "title": title.strip(),
            "message": message.strip(),
            "severity": severity,
            "source": source,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "active",
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(alert)
    except Exception as e:
        return FlextCore.Result[FlextCore.Types.Dict].fail(
            f"Alert creation failed: {e}"
        )


def flext_create_health_check(
    service_name: str,
    status: str = "healthy",
    details: FlextCore.Types.Dict | None = None,
) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Create a health check with inline validation."""
    try:
        if not service_name or not isinstance(service_name, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Service name must be a non-empty string"
            )

        valid_statuses = {"healthy", "degraded", "unhealthy"}
        if status not in valid_statuses:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
            )

        health_check: FlextCore.Types.Dict = {
            "service_name": service_name.strip(),
            "status": status,
            "timestamp": datetime.now(UTC).isoformat(),
            "details": details or {},
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(health_check)
    except Exception as e:
        return FlextCore.Result[FlextCore.Types.Dict].fail(
            f"Health check creation failed: {e}"
        )


def flext_create_log_entry(
    message: str,
    level: str = "INFO",
    service: str = "unknown",
    correlation_id: str | None = None,
) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Create a log entry with inline validation."""
    try:
        if not message or not isinstance(message, str):
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Log message must be a non-empty string"
            )

        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level.upper() not in valid_levels:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Invalid log level '{level}'. Must be one of: {', '.join(valid_levels)}"
            )

        log_entry: FlextCore.Types.Dict = {
            "message": message.strip(),
            "level": level.upper(),
            "service": service,
            "timestamp": datetime.now(UTC).isoformat(),
            "correlation_id": correlation_id or str(uuid4()),
        }

        return FlextCore.Result[FlextCore.Types.Dict].ok(log_entry)
    except Exception as e:
        return FlextCore.Result[FlextCore.Types.Dict].fail(
            f"Log entry creation failed: {e}"
        )


__all__ = [
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
]
