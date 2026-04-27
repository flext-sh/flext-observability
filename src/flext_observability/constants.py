"""Observability constants extending flext-core patterns.

Includes metric types, alert levels, trace statuses, and configuration defaults.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import ClassVar, Final

from flext_core import c


class FlextObservabilityConstants(c):
    """Observability-specific constants extending flext-core patterns.

    Usage:
    ```python
    from flext_observability import FlextObservabilityConstants

    service_name = FlextObservabilityConstants.Observability.DEFAULT_SERVICE_NAME
    metric_type = FlextObservabilityConstants.Observability.MetricType.COUNTER
    ```
    """

    class Observability:
        """Observability domain constants namespace.

        All observability-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        DEFAULT_SERVICE_NAME: Final[str] = "flext-service"
        DEFAULT_LOG_LEVEL: Final[str] = "INFO"
        DEFAULT_METRIC_UNIT: Final[str] = "1"
        DEFAULT_SETTINGS_SERVICE_NAME: Final[str] = "flext-observability"
        DEFAULT_ENVIRONMENT: Final[str] = "development"
        DEFAULT_FLUSH_INTERVAL: Final[int] = 30
        DEFAULT_METRICS_ENABLED: Final[bool] = True
        DEFAULT_TRACES_ENABLED: Final[bool] = True
        DEFAULT_ALERTS_ENABLED: Final[bool] = True

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

        class FunctionArgs:
            """Function argument length constants."""

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

        METRIC_UNIT_COUNT: ClassVar[str] = "count"
        METRIC_UNIT_PERCENT: ClassVar[str] = "percent"
        METRIC_UNIT_BYTES: ClassVar[str] = "bytes"
        METRIC_UNIT_SECONDS: ClassVar[str] = "seconds"
        ALERT_LEVEL_INFO: ClassVar[str] = AlertLevel.INFO.value
        ALERT_LEVEL_WARNING: ClassVar[str] = AlertLevel.WARNING.value
        ALERT_LEVEL_ERROR: ClassVar[str] = AlertLevel.ERROR.value
        ALERT_LEVEL_CRITICAL: ClassVar[str] = AlertLevel.CRITICAL.value
        TRACE_STATUS_STARTED: ClassVar[str] = TraceStatus.STARTED.value
        TRACE_STATUS_RUNNING: ClassVar[str] = TraceStatus.RUNNING.value
        TRACE_STATUS_COMPLETED: ClassVar[str] = TraceStatus.COMPLETED.value
        TRACE_STATUS_FAILED: ClassVar[str] = TraceStatus.FAILED.value
        HEALTH_STATUS_HEALTHY: ClassVar[str] = HealthStatus.HEALTHY.value
        HEALTH_STATUS_DEGRADED: ClassVar[str] = HealthStatus.DEGRADED.value
        HEALTH_STATUS_UNHEALTHY: ClassVar[str] = HealthStatus.UNHEALTHY.value
        LOG_LEVEL_DEBUG: ClassVar[str] = ErrorSeverity.DEBUG.value
        LOG_LEVEL_INFO: ClassVar[str] = ErrorSeverity.INFO.value
        LOG_LEVEL_WARNING: ClassVar[str] = ErrorSeverity.WARNING.value
        LOG_LEVEL_ERROR: ClassVar[str] = ErrorSeverity.ERROR.value
        LOG_LEVEL_CRITICAL: ClassVar[str] = ErrorSeverity.CRITICAL.value
        MAX_METRIC_NAME_LENGTH: ClassVar[int] = 128
        MAX_TRACE_NAME_LENGTH: ClassVar[int] = 256
        MAX_ALERT_MESSAGE_LENGTH: ClassVar[int] = 1024
        MAX_LOG_MESSAGE_LENGTH: ClassVar[int] = 4096


c = FlextObservabilityConstants
__all__: list[str] = ["FlextObservabilityConstants", "c"]
