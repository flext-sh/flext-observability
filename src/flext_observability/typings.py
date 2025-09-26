"""FLEXT Module.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal, Protocol

from flext_core import E, F, FlextTypes as CoreFlextTypes, P, R, T, U, V

# Observability-specific type aliases
MetricValue = float | int | Decimal
TagsDict = dict[str, str | int | float] | bool
LogLevel = str  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
AlertLevel = str  # "info", "warning", "error", "critical"
TraceStatus = str  # "started", "running", "completed", "failed"
HealthStatus = str  # "healthy", "degraded", "unhealthy"


class FlextObservabilityTypes(CoreFlextTypes):
    """Observability-specific types extending FlextTypes."""

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
            str, CoreFlextTypes.Core.ConfigValue | object
        ]
        type MonitoringConfig = dict[str, str | int | bool | list[str]]
        type MetricsConfig = dict[str, bool | str | dict[str, object]]
        type TracingConfig = dict[str, CoreFlextTypes.Core.ConfigValue | object]

    # =========================================================================
    # OBSERVABILITY CORE TYPES - Commonly used observability-specific types
    # =========================================================================

    class Core(CoreFlextTypes.Core):
        """Core observability types extending FlextTypes.Core."""

        # Metric types
        type MetricDict = dict[str, float]
        type MetricFormatDict = dict[str, str]
        type MetricValueDict = dict[str, float | int]
        type MetricConfigDict = dict[str, bool | str | dict[str, object]]

        # Tag and metadata types
        type TagsDict = dict[str, str]
        type MetadataDict = dict[str, object]
        type AttributesDict = dict[str, object]

        # Trace types
        type TraceContextDict = dict[str, str]
        type SpanAttributesDict = dict[str, object]
        type TraceInfoDict = dict[str, object]

        # Health monitoring types
        type HealthMetricsDict = dict[str, object]
        type ComponentHealthDict = dict[str, object]
        type SystemChecksDict = dict[str, dict[str, float | str]]

        # Service and container types
        type ServiceTuple = tuple[str, object]
        type ServicesList = list[ServiceTuple]

        # Storage types for observability services
        type MetricsStore = dict[str, list[CoreFlextTypes.Core.Dict]]
        type CountersDict = dict[str, float]
        type GaugesDict = dict[str, float]
        type HistogramsList = list[float]
        type HistogramsDict = dict[str, HistogramsList]

        # Trace storage types
        type TracesDict = dict[str, CoreFlextTypes.Core.Dict]
        type TraceSpansDict = dict[str, list[CoreFlextTypes.Core.Dict]]
        type TraceHierarchyDict = dict[str, CoreFlextTypes.Core.StringList]

        # Health storage types
        type HealthHistoryDict = dict[str, list[CoreFlextTypes.Core.Dict]]
        type HealthHistoryList = list[CoreFlextTypes.Core.Dict]


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
