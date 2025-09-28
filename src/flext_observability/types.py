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
        ...

    @property
    def value(self) -> MetricValue:
        """The metric value."""
        ...

    @property
    def unit(self) -> str:
        """The metric unit."""
        ...

    @property
    def timestamp(self) -> datetime: ...

    @property
    def tags(self) -> TagsDict: ...


class TraceProtocol(Protocol):
    """Protocol for trace entities."""

    @property
    def operation(self) -> str: ...

    @property
    def span_id(self) -> str: ...

    @property
    def trace_id(self) -> str: ...

    @property
    def span_attributes(self) -> dict[str, object]: ...

    @property
    def duration_ms(self) -> float | None: ...

    @property
    def status(self) -> TraceStatus: ...

    @property
    def timestamp(self) -> datetime: ...


class AlertProtocol(Protocol):
    """Protocol for alert entities."""

    @property
    def title(self) -> str: ...

    @property
    def message(self) -> str: ...

    @property
    def severity(self) -> AlertLevel: ...

    @property
    def status(self) -> str: ...

    @property
    def tags(self) -> TagsDict: ...

    @property
    def timestamp(self) -> datetime: ...


class HealthCheckProtocol(Protocol):
    """Protocol for health check entities."""

    @property
    def component(self) -> str: ...

    @property
    def status(self) -> HealthStatus: ...

    @property
    def message(self) -> str: ...

    @property
    def metrics(self) -> dict[str, object]: ...

    @property
    def timestamp(self) -> datetime: ...


class LogEntryProtocol(Protocol):
    """Protocol for log entry entities."""

    @property
    def message(self) -> str: ...

    @property
    def level(self) -> LogLevel: ...

    @property
    def context(self) -> dict[str, object]: ...

    @property
    def timestamp(self) -> datetime: ...


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
