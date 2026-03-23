"""Observability constants extending flext-core patterns.

Includes metric types, alert levels, trace statuses, and configuration defaults.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import ClassVar, Final, Literal

from flext_core import FlextConstants


class FlextObservabilityConstants(FlextConstants):
    """Observability-specific constants extending flext-core patterns.

    Usage:
    ```python
    from flext_observability import FlextObservabilityConstants

    namespace = (
        FlextObservabilityConstants.Observability.Defaults.DEFAULT_METRICS_NAMESPACE
    )
    metric_type = FlextObservabilityConstants.Observability.MetricType.COUNTER
    ```
    """

    class Observability:
        """Observability domain constants namespace.

        All observability-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        class Defaults:
            """Configuration defaults."""

            DEFAULT_SERVICE_NAME: Final[str] = "flext-service"
            DEFAULT_LOG_LEVEL: Final[str] = "INFO"
            DEFAULT_METRIC_UNIT: Final[str] = "1"

        @unique
        class MetricType(StrEnum):
            """Metric type enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use MetricType.COUNTER.value
                or MetricType.COUNTER directly - no base strings needed.
            """

            COUNTER = "counter"
            GAUGE = "gauge"
            HISTOGRAM = "histogram"
            SUMMARY = "summary"

        @unique
        class AlertLevel(StrEnum):
            """Alert level enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use AlertLevel.INFO.value
                or AlertLevel.INFO directly - no base strings needed.
            """

            INFO = "info"
            WARNING = "warning"
            ERROR = "error"
            CRITICAL = "critical"

        @unique
        class TraceStatus(StrEnum):
            """Trace status enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use TraceStatus.STARTED.value
                or TraceStatus.STARTED directly - no base strings needed.
            """

            STARTED = "started"
            RUNNING = "running"
            COMPLETED = "completed"
            FAILED = "failed"
            UNSET = "unset"
            OK = "ok"
            ERROR = "error"

        @unique
        class HealthStatus(StrEnum):
            """Health check status enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use HealthStatus.HEALTHY.value
                or HealthStatus.HEALTHY directly - no base strings needed.
            """

            HEALTHY = "healthy"
            DEGRADED = "degraded"
            UNHEALTHY = "unhealthy"

        @unique
        class AlertSeverity(StrEnum):
            """Alert severity enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use AlertSeverity.INFO.value
                or AlertSeverity.INFO directly - no base strings needed.
            """

            INFO = "info"
            WARNING = "warning"
            ERROR = "error"
            CRITICAL = "critical"

        @unique
        class AlertStatus(StrEnum):
            """Alert status enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use AlertStatus.FIRING.value
                or AlertStatus.FIRING directly - no base strings needed.
            """

            FIRING = "firing"
            RESOLVED = "resolved"

        class Storage:
            """Storage limits for metrics service."""

        @unique
        class Service(StrEnum):
            """Service name enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use Service.METRICS.value
                or Service.METRICS directly - no base strings needed.
            """

            METRICS = "metrics"
            TRACING = "tracing"
            ALERTS = "alerts"
            HEALTH = "health"
            LOGGING = "logging"

        @unique
        class SamplingDecision(StrEnum):
            """Sampling decision enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use SamplingDecision.SAMPLED.value
                or SamplingDecision.SAMPLED directly - no base strings needed.
            """

            SAMPLED = "sampled"
            NOT_SAMPLED = "not_sampled"

        @unique
        class ErrorSeverity(StrEnum):
            """Error severity enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use ErrorSeverity.INFO.value
                or ErrorSeverity.INFO directly - no base strings needed.
            """

            DEBUG = "debug"
            INFO = "info"
            WARNING = "warning"
            ERROR = "error"
            CRITICAL = "critical"

        class Literals:
            """Type-safe string literals for observability (Python 3.13+ best practices).

            These type aliases provide strict type checking for common string values
            used throughout the flext-observability codebase.
            All Literal types reference StrEnum members to avoid string duplication (DRY principle).
            Using PEP 695 type statement for better type checking and IDE support.
            """

            type MetricTypeLiteral = Literal[
                FlextObservabilityConstants.Observability.MetricType.COUNTER,
                FlextObservabilityConstants.Observability.MetricType.GAUGE,
                FlextObservabilityConstants.Observability.MetricType.HISTOGRAM,
                FlextObservabilityConstants.Observability.MetricType.SUMMARY,
            ]
            type AlertLevelLiteral = Literal[
                FlextObservabilityConstants.Observability.AlertLevel.INFO,
                FlextObservabilityConstants.Observability.AlertLevel.WARNING,
                FlextObservabilityConstants.Observability.AlertLevel.ERROR,
                FlextObservabilityConstants.Observability.AlertLevel.CRITICAL,
            ]
            type TraceStatusLiteral = Literal[
                FlextObservabilityConstants.Observability.TraceStatus.STARTED,
                FlextObservabilityConstants.Observability.TraceStatus.RUNNING,
                FlextObservabilityConstants.Observability.TraceStatus.COMPLETED,
                FlextObservabilityConstants.Observability.TraceStatus.FAILED,
            ]
            type HealthStatusLiteral = Literal[
                FlextObservabilityConstants.Observability.HealthStatus.HEALTHY,
                FlextObservabilityConstants.Observability.HealthStatus.DEGRADED,
                FlextObservabilityConstants.Observability.HealthStatus.UNHEALTHY,
            ]
            type ServiceLiteral = Literal[
                FlextObservabilityConstants.Observability.Service.METRICS,
                FlextObservabilityConstants.Observability.Service.TRACING,
                FlextObservabilityConstants.Observability.Service.ALERTS,
                FlextObservabilityConstants.Observability.Service.HEALTH,
                FlextObservabilityConstants.Observability.Service.LOGGING,
            ]

        class FunctionArgs:
            """Function argument length constants."""

    METRIC_UNIT_COUNT: ClassVar[str] = "count"
    METRIC_UNIT_PERCENT: ClassVar[str] = "percent"
    METRIC_UNIT_BYTES: ClassVar[str] = "bytes"
    METRIC_UNIT_SECONDS: ClassVar[str] = "seconds"
    ALERT_LEVEL_INFO: ClassVar[str] = "info"
    ALERT_LEVEL_WARNING: ClassVar[str] = "warning"
    ALERT_LEVEL_ERROR: ClassVar[str] = "error"
    ALERT_LEVEL_CRITICAL: ClassVar[str] = "critical"
    TRACE_STATUS_STARTED: ClassVar[str] = "started"
    TRACE_STATUS_RUNNING: ClassVar[str] = "running"
    TRACE_STATUS_COMPLETED: ClassVar[str] = "completed"
    TRACE_STATUS_FAILED: ClassVar[str] = "failed"
    HEALTH_STATUS_HEALTHY: ClassVar[str] = "healthy"
    HEALTH_STATUS_DEGRADED: ClassVar[str] = "degraded"
    HEALTH_STATUS_UNHEALTHY: ClassVar[str] = "unhealthy"
    LOG_LEVEL_DEBUG: ClassVar[str] = "debug"
    LOG_LEVEL_INFO: ClassVar[str] = "info"
    LOG_LEVEL_WARNING: ClassVar[str] = "warning"
    LOG_LEVEL_ERROR: ClassVar[str] = "error"
    LOG_LEVEL_CRITICAL: ClassVar[str] = "critical"
    MAX_METRIC_NAME_LENGTH: ClassVar[int] = 128
    MAX_TRACE_NAME_LENGTH: ClassVar[int] = 256
    MAX_ALERT_MESSAGE_LENGTH: ClassVar[int] = 1024
    MAX_LOG_MESSAGE_LENGTH: ClassVar[int] = 4096
    DEFAULT_SERVICE_NAME: ClassVar[str] = "flext-observability"
    DEFAULT_ENVIRONMENT: ClassVar[str] = "development"

    @unique
    class ObservabilityProjectType(StrEnum):
        """Project-type identifiers for observability packages."""

        MONITORING_SERVICE = "monitoring-service"
        METRICS_COLLECTOR = "metrics-collector"
        TRACING_SERVICE = "tracing-service"
        ALERTING_SYSTEM = "alerting-system"
        OBSERVABILITY_PLATFORM = "observability-platform"
        MONITORING_DASHBOARD = "monitoring-dashboard"
        METRICS_AGGREGATOR = "metrics-aggregator"
        TRACE_COLLECTOR = "trace-collector"
        HEALTH_MONITOR = "health-monitor"
        LOG_AGGREGATOR = "log-aggregator"
        APM_SERVICE = "apm-service"
        MONITORING_API = "monitoring-api"
        METRICS_EXPORTER = "metrics-exporter"
        ALERTMANAGER = "alertmanager"
        OBSERVABILITY_GATEWAY = "observability-gateway"
        TELEMETRY_SERVICE = "telemetry-service"


c = FlextObservabilityConstants
__all__ = ["FlextObservabilityConstants", "c"]
