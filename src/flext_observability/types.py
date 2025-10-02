"""FLEXT Observability Types Module.

This module provides type definitions, aliases, and protocols for the FLEXT observability system.
All type definitions follow the domain separation principle and extend FlextTypes appropriately.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Protocol

# Re-export core types for convenience
from flext_core import E, F, FlextTypes, FlextTypes as CoreFlextTypes, P, R, T, U, V

# Observability-specific type aliases
MetricValue = float | int | Decimal
TagsDict = dict[str, str | int | float] | bool
LogLevel = str  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
AlertLevel = str  # "info", "warning", "error", "critical"
TraceStatus = str  # "started", "running", "completed", "failed"
HealthStatus = str  # "healthy", "degraded", "unhealthy"


# Protocol definitions for observability entities
class MetricProtocol(Protocol):
    """Protocol for metric entities."""

    @property
    def name(self) -> str:
        """The metric name."""

    @property
    def value(self) -> MetricValue:
        """The metric value."""

    @property
    def unit(self) -> str:
        """The metric unit."""

    @property
    def timestamp(self) -> datetime:
        """The metric timestamp."""

    @property
    def tags(self) -> TagsDict:
        """The metric tags."""


class TraceProtocol(Protocol):
    """Protocol for trace entities."""

    @property
    def operation(self) -> str:
        """The trace operation."""

    @property
    def span_id(self) -> str:
        """The span ID."""

    @property
    def trace_id(self) -> str:
        """The trace ID."""

    @property
    def span_attributes(self) -> dict[str, object]:
        """The span attributes."""

    @property
    def duration_ms(self) -> float | None:
        """The duration in milliseconds."""

    @property
    def status(self) -> TraceStatus:
        """The trace status."""

    @property
    def timestamp(self) -> datetime:
        """The trace timestamp."""


class AlertProtocol(Protocol):
    """Protocol for alert entities."""

    @property
    def title(self) -> str:
        """The alert title."""

    @property
    def message(self) -> str:
        """The alert message."""

    @property
    def severity(self) -> AlertLevel:
        """The alert severity."""

    @property
    def status(self) -> str:
        """The alert status."""

    @property
    def tags(self) -> TagsDict:
        """The alert tags."""

    @property
    def timestamp(self) -> datetime:
        """The alert timestamp."""


class HealthCheckProtocol(Protocol):
    """Protocol for health check entities."""

    @property
    def component(self) -> str:
        """The component name."""

    @property
    def status(self) -> HealthStatus:
        """The health status."""

    @property
    def message(self) -> str:
        """The health check message."""

    @property
    def metrics(self) -> dict[str, object]:
        """The health check metrics."""

    @property
    def timestamp(self) -> datetime:
        """The health check timestamp."""


class LogEntryProtocol(Protocol):
    """Protocol for log entry entities."""

    @property
    def message(self) -> str:
        """Log message content."""

    @property
    def level(self) -> LogLevel:
        """Log level for the entry."""

    @property
    def context(self) -> dict[str, object]:
        """Additional context data for the log entry."""

    @property
    def timestamp(self) -> datetime:
        """Timestamp when the log entry was created."""


class ObservabilityTypes(CoreFlextTypes):
    """Observability-specific types extending FlextTypes."""

    # Type aliases
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
