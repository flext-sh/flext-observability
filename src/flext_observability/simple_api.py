"""FLEXT Observability Simple API - Easy-to-use factory functions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simple factory functions for creating observability objects without complex setup.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from flext_core import FlextEntityId

from flext_observability.domain.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)


def create_flext_metric(
    name: str,
    value: float | Decimal,
    unit: str = "",
    tags: dict[str, str] | None = None,
    timestamp: datetime | None = None,
) -> FlextMetric:
    """Create a metric with simple parameters.

    Args:
        name: Name of the metric
        value: Numeric value of the metric
        unit: Unit of measurement
        tags: Optional tags for the metric
        timestamp: Optional timestamp, defaults to now

    Returns:
        FlextMetric instance

    """
    return FlextMetric(
        entity_id=FlextEntityId.generate(),
        name=name,
        value=Decimal(str(value)),
        unit=unit,
        tags=tags or {},
        timestamp=timestamp or datetime.now(),
    )


def create_flext_log_entry(
    message: str,
    level: str = "info",
    context: dict[str, Any] | None = None,
    timestamp: datetime | None = None,
) -> FlextLogEntry:
    """Create a log entry with simple parameters.

    Args:
        message: Log message
        level: Log level (debug, info, warning, error, critical)
        context: Optional context data
        timestamp: Optional timestamp, defaults to now

    Returns:
        FlextLogEntry instance

    """
    return FlextLogEntry(
        entity_id=FlextEntityId.generate(),
        level=level,
        message=message,
        context=context or {},
        timestamp=timestamp or datetime.now(),
    )


def create_flext_trace(
    trace_id: str,
    operation: str,
    span_id: str = "",
    duration_ms: int = 0,
    status: str = "pending",
    timestamp: datetime | None = None,
) -> FlextTrace:
    """Create a trace with simple parameters.

    Args:
        trace_id: Unique trace identifier
        operation: Operation being traced
        span_id: Optional span identifier
        duration_ms: Duration in milliseconds
        status: Trace status
        timestamp: Optional timestamp, defaults to now

    Returns:
        FlextTrace instance

    """
    return FlextTrace(
        entity_id=FlextEntityId.generate(),
        trace_id=trace_id,
        span_id=span_id or f"{trace_id}-span",
        operation=operation,
        duration_ms=duration_ms,
        status=status,
        timestamp=timestamp or datetime.now(),
    )


def create_flext_alert(
    title: str,
    message: str,
    severity: str = "low",
    status: str = "active",
    timestamp: datetime | None = None,
) -> FlextAlert:
    """Create an alert with simple parameters.

    Args:
        title: Alert title
        message: Alert message
        severity: Alert severity (low, medium, high, critical)
        status: Alert status (active, acknowledged, resolved)
        timestamp: Optional timestamp, defaults to now

    Returns:
        FlextAlert instance

    """
    return FlextAlert(
        entity_id=FlextEntityId.generate(),
        title=title,
        message=message,
        severity=severity,
        status=status,
        timestamp=timestamp or datetime.now(),
    )


def create_flext_health_check(
    component: str,
    status: str = "unknown",
    message: str = "",
    timestamp: datetime | None = None,
) -> FlextHealthCheck:
    """Create a health check with simple parameters.

    Args:
        component: Component being checked
        status: Health status (healthy, unhealthy, unknown, degraded)
        message: Optional health message
        timestamp: Optional timestamp, defaults to now

    Returns:
        FlextHealthCheck instance

    """
    return FlextHealthCheck(
        entity_id=FlextEntityId.generate(),
        component=component,
        status=status,
        message=message,
        timestamp=timestamp or datetime.now(),
    )
