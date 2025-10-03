"""FLEXT Observability Types Module.

This module provides unified type definitions, aliases, and protocols for the FLEXT observability system.
All type definitions follow the domain separation principle and extend FlextTypes appropriately.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal, Protocol

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

    # =========================================================================
    # OBSERVABILITY PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(CoreFlextTypes.Project):
        """Observability-specific project types extending FlextTypes.Project.

        Adds observability/monitoring-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Observability domain owns monitoring-specific types.
        """

        # Observability-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
            "library",
            "application",
            "service",
            # Observability-specific types
            "monitoring-service",
            "metrics-collector",
            "tracing-service",
            "alerting-system",
            "observability-platform",
            "monitoring-dashboard",
            "metrics-aggregator",
            "trace-collector",
            "health-monitor",
            "log-aggregator",
            "apm-service",
            "monitoring-api",
            "metrics-exporter",
            "alertmanager",
            "observability-gateway",
            "telemetry-service",
        ]

        # Observability-specific project configurations
        type ObservabilityProjectConfig = dict[
            str, str | int | bool | FlextTypes.StringList | object
        ]
        type MonitoringConfig = dict[str, str | int | bool | FlextTypes.StringList]
        type MetricsConfig = dict[str, bool | str | FlextTypes.Dict]
        type TracingConfig = dict[
            str, str | int | bool | FlextTypes.StringList | object
        ]

    # =========================================================================
    # OBSERVABILITY CORE TYPES - Commonly used observability-specific types
    # =========================================================================

    class Core(CoreFlextTypes):
        """Core observability types extending FlextTypes."""

        # Metric types
        type MetricDict = dict[str, float | str | int]
        type MetricFormatDict = dict[str, str | dict[str, float | str | int] | float]
        type MetricValueDict = dict[str, float | int]
        type MetricConfigDict = dict[str, bool | str | FlextTypes.Dict]

        # Tag and metadata types
        type TagsDict = FlextTypes.StringDict
        type MetadataDict = FlextTypes.Dict
        type AttributesDict = FlextTypes.Dict
        type Headers = dict[str, str]  # HTTP headers for observability

        # Trace types
        type TraceContextDict = dict[str, str | None]
        type SpanAttributesDict = FlextTypes.Dict
        type TraceInfoDict = FlextTypes.Dict

        # Health monitoring types
        type HealthMetricsDict = FlextTypes.Dict
        type ComponentHealthDict = FlextTypes.Dict
        type SystemChecksDict = dict[str, dict[str, float | str]]

        # Service and container types
        type ServiceTuple = tuple[str, object]
        type ServicesList = list[ServiceTuple]

        # Storage types for observability services
        type MetricsStore = dict[str, list[MetadataDict]]
        type CountersDict = FlextTypes.FloatDict
        type GaugesDict = FlextTypes.FloatDict
        type HistogramsList = FlextTypes.FloatList
        type HistogramsDict = dict[str, HistogramsList]

        # Trace storage types
        type TracesDict = dict[str, MetadataDict]
        type TraceSpansDict = dict[str, list[MetadataDict]]
        type TraceHierarchyDict = dict[str, FlextTypes.StringList]

        # Health storage types
        type HealthHistoryDict = dict[str, list[MetadataDict]]
        type HealthHistoryList = list[MetadataDict]

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


# Separate protocol classes for backward compatibility and flexibility
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
FlextObservabilityTypesAlias = ObservabilityTypes


__all__ = [
    "AlertLevel",
    "AlertProtocol",
    "E",
    "F",
    "FlextObservabilityTypes",
    "FlextObservabilityTypesAlias",
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
