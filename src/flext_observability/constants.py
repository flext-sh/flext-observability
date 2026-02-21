"""Observability constants extending flext-core patterns.

Includes metric types, alert levels, trace statuses, and configuration defaults.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_core import c


class FlextObservabilityConstants(c):
    """Observability-specific constants extending flext-core patterns.

    Usage:
    ```python
    from flext_observability.constants import FlextObservabilityConstants

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

            DEFAULT_METRICS_NAMESPACE: Final[str] = "flext"
            DEFAULT_SERVICE_NAME: Final[str] = "flext-service"
            DEFAULT_LOG_LEVEL: Final[str] = "INFO"
            DEFAULT_METRIC_UNIT: Final[str] = "count"
            DEFAULT_TRACE_TIMEOUT: Final[float] = 30.0
            DEFAULT_HEALTH_CHECK_INTERVAL: Final[float] = 60.0
            DEFAULT_METRICS_EXPORT_INTERVAL_SECONDS: Final[int] = 60
            DEFAULT_TRACING_SAMPLING_RATE: Final[float] = 1.0
            DEFAULT_MAX_SPAN_ATTRIBUTES: Final[int] = 128
            DEFAULT_MONITORING_ENDPOINT: Final[str] = "http://localhost:9090"

        # =============================================================================
        # STRENUM CLASSES - Single source of truth for string enumerations
        # =============================================================================

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

        class HealthStatus(StrEnum):
            """Health check status enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use HealthStatus.HEALTHY.value
                or HealthStatus.HEALTHY directly - no base strings needed.
            """

            HEALTHY = "healthy"
            DEGRADED = "degraded"
            UNHEALTHY = "unhealthy"

        class Storage:
            """Storage limits for metrics service."""

            MAX_METRICS_STORE_SIZE: Final[int] = 1000
            METRICS_STORE_CLEANUP_SIZE: Final[int] = 500

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

        class SamplingDecision(StrEnum):
            """Sampling decision enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use SamplingDecision.SAMPLED.value
                or SamplingDecision.SAMPLED directly - no base strings needed.
            """

            SAMPLED = "sampled"
            NOT_SAMPLED = "not_sampled"

        class ErrorSeverity(StrEnum):
            """Error severity enumeration.

            DRY Pattern:
                StrEnum is the single source of truth. Use ErrorSeverity.INFO.value
                or ErrorSeverity.INFO directly - no base strings needed.
            """

            INFO = "info"
            WARNING = "warning"
            ERROR = "error"
            CRITICAL = "critical"

        # =============================================================================
        # LITERAL TYPES - Type-safe string literals (PEP 695)
        # =============================================================================
        # All Literal types reference StrEnum members - NO string duplication!

        class Literals:
            """Type-safe string literals for observability (Python 3.13+ best practices).

            These type aliases provide strict type checking for common string values
            used throughout the flext-observability codebase.
            All Literal types reference StrEnum members to avoid string duplication (DRY principle).
            Using PEP 695 type statement for better type checking and IDE support.
            """

            # Metric type literal - references MetricType StrEnum members
            type MetricTypeLiteral = Literal[
                FlextObservabilityConstants.Observability.MetricType.COUNTER,
                FlextObservabilityConstants.Observability.MetricType.GAUGE,
                FlextObservabilityConstants.Observability.MetricType.HISTOGRAM,
                FlextObservabilityConstants.Observability.MetricType.SUMMARY,
            ]

            # Alert level literal - references AlertLevel StrEnum members
            type AlertLevelLiteral = Literal[
                FlextObservabilityConstants.Observability.AlertLevel.INFO,
                FlextObservabilityConstants.Observability.AlertLevel.WARNING,
                FlextObservabilityConstants.Observability.AlertLevel.ERROR,
                FlextObservabilityConstants.Observability.AlertLevel.CRITICAL,
            ]

            # Trace status literal - references TraceStatus StrEnum members
            type TraceStatusLiteral = Literal[
                FlextObservabilityConstants.Observability.TraceStatus.STARTED,
                FlextObservabilityConstants.Observability.TraceStatus.RUNNING,
                FlextObservabilityConstants.Observability.TraceStatus.COMPLETED,
                FlextObservabilityConstants.Observability.TraceStatus.FAILED,
            ]

            # Health status literal - references HealthStatus StrEnum members
            type HealthStatusLiteral = Literal[
                FlextObservabilityConstants.Observability.HealthStatus.HEALTHY,
                FlextObservabilityConstants.Observability.HealthStatus.DEGRADED,
                FlextObservabilityConstants.Observability.HealthStatus.UNHEALTHY,
            ]

            # Service literal - references Service StrEnum members
            type ServiceLiteral = Literal[
                FlextObservabilityConstants.Observability.Service.METRICS,
                FlextObservabilityConstants.Observability.Service.TRACING,
                FlextObservabilityConstants.Observability.Service.ALERTS,
                FlextObservabilityConstants.Observability.Service.HEALTH,
                FlextObservabilityConstants.Observability.Service.LOGGING,
            ]

        class FunctionArgs:
            """Function argument length constants."""

            NO_ARGS: Final[int] = 0  # No arguments
            ONE_ARG: Final[int] = 1  # One argument
            TWO_ARGS: Final[int] = 2  # Two arguments


c = FlextObservabilityConstants
ErrorSeverity = FlextObservabilityConstants.Observability.ErrorSeverity
MetricType = FlextObservabilityConstants.Observability.MetricType

__all__ = [
    "ErrorSeverity",
    "FlextObservabilityConstants",
    "MetricType",
    "c",
]
