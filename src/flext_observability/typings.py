"""FLEXT Observability Types Module.

This module provides unified type definitions, aliases, and protocols for the FLEXT observability system.
All type definitions follow the domain separation principle and extend FlextCore.Types appropriately.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal, Protocol, TypeVar

from flext_core import FlextCore

# Define T TypeVar for generic programming
T = TypeVar("T")

# Observability-specific type aliases
MetricValue = float | int | Decimal
TagsDict = dict[str, str | int | float] | bool
LogLevel = str  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
AlertLevel = str  # "info", "warning", "error", "critical"
TraceStatus = str  # "started", "running", "completed", "failed"
HealthStatus = str  # "healthy", "degraded", "unhealthy"


class FlextObservabilityTypes(FlextCore.Types):
    """Unified observability types extending FlextCore.Types.

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
    # OBSERVABILITY PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project(FlextCore.Types.Project):
        """Observability-specific project types extending FlextCore.Types.Project.

        Adds observability/monitoring-specific project types while inheriting
        generic types from FlextCore.Types. Follows domain separation principle:
        Observability domain owns monitoring-specific types.
        """

        # Observability-specific project types extending the generic ones
        type ObservabilityProjectType = Literal[
            # Generic types inherited from FlextCore.Types.Project
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
            str, str | int | bool | FlextCore.Types.StringList | object
        ]
        type MonitoringConfig = dict[str, str | int | bool | FlextCore.Types.StringList]
        type MetricsConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type TracingConfig = dict[
            str, str | int | bool | FlextCore.Types.StringList | object
        ]

    # =========================================================================
    # OBSERVABILITY CORE TYPES - Commonly used observability-specific types
    # =========================================================================

    class ObservabilityCore(FlextCore.Types):
        """Core observability types extending FlextCore.Types."""

        # Metric types
        type MetricDict = dict[str, float | str | int]
        type MetricFormatDict = dict[str, str | dict[str, float | str | int] | float]
        type MetricValueDict = dict[str, float | int]
        type MetricConfigDict = dict[str, bool | str | FlextCore.Types.Dict]

        # Tag and metadata types
        type TagsDict = FlextCore.Types.StringDict
        type MetadataDict = FlextCore.Types.Dict
        type AttributesDict = FlextCore.Types.Dict
        type ObservabilityHeaders = dict[str, str]  # HTTP headers for observability

        # Trace types
        type TraceContextDict = dict[str, str | None]
        type SpanAttributesDict = FlextCore.Types.Dict
        type TraceInfoDict = FlextCore.Types.Dict

        # Health monitoring types
        type HealthMetricsDict = FlextCore.Types.Dict
        type ComponentHealthDict = FlextCore.Types.Dict
        type SystemChecksDict = dict[str, dict[str, float | str]]

        # Service and container types
        type ServiceTuple = tuple[str, object]
        type ServicesList = list[ServiceTuple]

        # Storage types for observability services
        type MetricsStore = dict[str, list[MetadataDict]]
        type CountersDict = FlextCore.Types.FloatDict
        type GaugesDict = FlextCore.Types.FloatDict
        type HistogramsList = FlextCore.Types.FloatList
        type HistogramsDict = dict[str, HistogramsList]

        # Trace storage types
        type TracesDict = dict[str, MetadataDict]
        type TraceSpansDict = dict[str, list[MetadataDict]]
        type TraceHierarchyDict = dict[str, FlextCore.Types.StringList]

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

            def span_attributes(self) -> FlextCore.Types.Dict:
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

            def metrics(self) -> FlextCore.Types.Dict:
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

            def context(self) -> FlextCore.Types.Dict:
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


class ObservabilityTypes(FlextCore.Types):
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
    "FlextObservabilityTypes",
    "FlextObservabilityTypesAlias",
    "HealthCheckProtocol",
    "HealthStatus",
    "LogEntryProtocol",
    "LogLevel",
    "MetricProtocol",
    "MetricValue",
    "ObservabilityTypes",
    "T",
    "TagsDict",
    "TraceProtocol",
    "TraceStatus",
]
