"""FLEXT Observability Types Module.

This module provides type definitions, aliases, and protocols for the FLEXT observability system.
All type definitions follow the domain separation principle and extend FlextTypes appropriately.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

# Re-export core types for convenience
from flext_core import E, F, FlextTypes, FlextTypes as CoreFlextTypes, P, R, T, U, V

# Observability-specific type aliases
MetricValue = float | int | Decimal
TagsDict = dict[str, str | int | float] | bool
LogLevel = str  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
AlertLevel = str  # "info", "warning", "error", "critical"
TraceStatus = str  # "started", "running", "completed", "failed"
HealthStatus = str  # "healthy", "degraded", "unhealthy"


class FlextObservabilityTypes(CoreFlextTypes):
    """Unified observability types extending FlextTypes.

    Single class containing all observability type definitions,
    protocols, and aliases following unified class pattern.
    """

    # Type aliases
    MetricValue = MetricValue
    TagsDict = TagsDict
    LogLevel = LogLevel
    AlertLevel = AlertLevel
    TraceStatus = TraceStatus
    HealthStatus = HealthStatus

    class Protocols:
        """Nested class for all observability protocols."""

        class MetricProtocol:
            """Abstract base for metric entities."""

            def name(self) -> str:
                """Get metric name."""
                raise NotImplementedError

            def value(self) -> MetricValue:
                """Get metric value."""
                raise NotImplementedError

            def unit(self) -> str:
                """Get metric unit."""
                raise NotImplementedError

            def timestamp(self) -> datetime:
                """Get metric timestamp."""
                raise NotImplementedError

            def tags(self) -> TagsDict:
                """Get metric tags."""
                raise NotImplementedError

        class TraceProtocol:
            """Abstract base for trace entities."""

            def operation(self) -> str:
                """Get operation name."""
                raise NotImplementedError

            def span_id(self) -> str:
                """Get span ID."""
                raise NotImplementedError

            def trace_id(self) -> str:
                """Get trace ID."""
                raise NotImplementedError

            def span_attributes(self) -> FlextTypes.Dict:
                """Get span attributes."""
                raise NotImplementedError

            def duration_ms(self) -> float | None:
                """Get duration in milliseconds."""
                raise NotImplementedError

            def status(self) -> TraceStatus:
                """Get trace status."""
                raise NotImplementedError

            def timestamp(self) -> datetime:
                """Get trace timestamp."""
                raise NotImplementedError

        class AlertProtocol:
            """Abstract base for alert entities."""

            def title(self) -> str:
                """Get alert title."""
                raise NotImplementedError

            def message(self) -> str:
                """Get alert message."""
                raise NotImplementedError

            def severity(self) -> AlertLevel:
                """Get alert severity."""
                raise NotImplementedError

            def status(self) -> str:
                """Get alert status."""
                raise NotImplementedError

            def tags(self) -> TagsDict:
                """Get alert tags."""
                raise NotImplementedError

            def timestamp(self) -> datetime:
                """Get alert timestamp."""
                raise NotImplementedError

        class HealthCheckProtocol:
            """Abstract base for health check entities."""

            def component(self) -> str:
                """Get component name."""
                raise NotImplementedError

            def status(self) -> HealthStatus:
                """Get health status."""
                raise NotImplementedError

            def message(self) -> str:
                """Get health message."""
                raise NotImplementedError

            def metrics(self) -> FlextTypes.Dict:
                """Get health metrics."""
                raise NotImplementedError

            def timestamp(self) -> datetime:
                """Get health check timestamp."""
                raise NotImplementedError

        class LogEntryProtocol:
            """Abstract base for log entry entities."""

            def message(self) -> str:
                """Get log message."""
                raise NotImplementedError

            def level(self) -> LogLevel:
                """Get log level."""
                raise NotImplementedError

            def context(self) -> FlextTypes.Dict:
                """Get log context."""
                raise NotImplementedError

            def timestamp(self) -> datetime:
                """Get log timestamp."""
                raise NotImplementedError


__all__ = [
    "AlertLevel",
    "E",
    "F",
    "FlextObservabilityTypes",
    "FlextTypes",
    "HealthStatus",
    "LogLevel",
    "MetricValue",
    "P",
    "R",
    "T",
    "TagsDict",
    "TraceStatus",
    "U",
    "V",
]
