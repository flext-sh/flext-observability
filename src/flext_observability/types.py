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
                raise NotImplementedError

            def value(self) -> MetricValue:
                raise NotImplementedError

            def unit(self) -> str:
                raise NotImplementedError

            def timestamp(self) -> datetime:
                raise NotImplementedError

            def tags(self) -> TagsDict:
                raise NotImplementedError

        class TraceProtocol:
            """Abstract base for trace entities."""

            def operation(self) -> str:
                raise NotImplementedError

            def span_id(self) -> str:
                raise NotImplementedError

            def trace_id(self) -> str:
                raise NotImplementedError

            def span_attributes(self) -> FlextTypes.Dict:
                raise NotImplementedError

            def duration_ms(self) -> float | None:
                raise NotImplementedError

            def status(self) -> TraceStatus:
                raise NotImplementedError

            def timestamp(self) -> datetime:
                raise NotImplementedError

        class AlertProtocol:
            """Abstract base for alert entities."""

            def title(self) -> str:
                raise NotImplementedError

            def message(self) -> str:
                raise NotImplementedError

            def severity(self) -> AlertLevel:
                raise NotImplementedError

            def status(self) -> str:
                raise NotImplementedError

            def tags(self) -> TagsDict:
                raise NotImplementedError

            def timestamp(self) -> datetime:
                raise NotImplementedError

        class HealthCheckProtocol:
            """Abstract base for health check entities."""

            def component(self) -> str:
                raise NotImplementedError

            def status(self) -> HealthStatus:
                raise NotImplementedError

            def message(self) -> str:
                raise NotImplementedError

            def metrics(self) -> FlextTypes.Dict:
                raise NotImplementedError

            def timestamp(self) -> datetime:
                raise NotImplementedError

        class LogEntryProtocol:
            """Abstract base for log entry entities."""

            def message(self) -> str:
                raise NotImplementedError

            def level(self) -> LogLevel:
                raise NotImplementedError

            def context(self) -> FlextTypes.Dict:
                raise NotImplementedError

            def timestamp(self) -> datetime:
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
