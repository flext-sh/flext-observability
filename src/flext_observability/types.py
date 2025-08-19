"""Type definitions for observability domain.

Extends flext-core types with observability-specific type aliases and protocols.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Protocol

from flext_core.typings import E, F, FlextTypes as CoreFlextTypes, P, R, T, U, V

# Observability-specific type aliases
MetricValue = float | int | Decimal
TagsDict = dict[str, str | int | float | bool]
LogLevel = str  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
AlertLevel = str  # "info", "warning", "error", "critical"
TraceStatus = str  # "started", "running", "completed", "failed"
HealthStatus = str  # "healthy", "degraded", "unhealthy"


class MetricProtocol(Protocol):
    """Protocol for metric entities."""

    name: str
    value: MetricValue
    unit: str
    timestamp: datetime
    tags: TagsDict


class TraceProtocol(Protocol):
    """Protocol for trace entities."""

    operation_name: str
    service_name: str
    span_id: str
    trace_id: str
    start_time: datetime
    end_time: datetime | None
    status: TraceStatus


class AlertProtocol(Protocol):
    """Protocol for alert entities."""

    message: str
    level: AlertLevel
    service: str
    timestamp: datetime
    resolved: bool


class HealthCheckProtocol(Protocol):
    """Protocol for health check entities."""

    service_name: str
    status: HealthStatus
    timestamp: datetime
    details: TagsDict


class LogEntryProtocol(Protocol):
    """Protocol for log entry entities."""

    message: str
    level: LogLevel
    service: str
    timestamp: datetime
    correlation_id: str | None


class ObservabilityTypes(CoreFlextTypes):
    """Observability domain-specific types extending flext-core."""

    # Value types
    MetricValue = MetricValue
    TagsDict = TagsDict
    LogLevel = LogLevel
    AlertLevel = AlertLevel
    TraceStatus = TraceStatus
    HealthStatus = HealthStatus

    # Protocols
    MetricProtocol = MetricProtocol
    TraceProtocol = TraceProtocol
    AlertProtocol = AlertProtocol
    HealthCheckProtocol = HealthCheckProtocol
    LogEntryProtocol = LogEntryProtocol


# Alias for backwards compatibility
FlextTypes = ObservabilityTypes


__all__ = [
    "AlertLevel",
    "AlertProtocol",
    "E",
    "F",
    "FlextTypes",
    "HealthCheckProtocol",
    "HealthStatus",
    "LogEntryProtocol",
    "LogLevel",
    "MetricProtocol",
    "MetricValue",
    "ObservabilityTypes",
    "P",
    "R",
    "T",
    "TagsDict",
    "TraceProtocol",
    "TraceStatus",
    "U",
    "V",
]
