"""FLEXT Observability Types - Domain-specific observability type definitions.

This module provides observability-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal, Protocol, TypeVar

from flext_core import FlextTypes

# Define T TypeVar for generic programming
T = TypeVar("T")


class FlextObservabilityTypes(FlextTypes):
    """Observability-specific type definitions extending FlextTypes.

    Domain-specific type system for observability and monitoring operations.
    Contains ONLY complex observability-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # OBSERVABILITY PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Observability-specific project types extending FlextTypes.Project.

        Adds observability/monitoring-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Observability domain owns monitoring-specific types.
        """

        # Observability-specific project types extending the generic ones
        type ObservabilityProjectType = Literal[
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

    # =========================================================================
    # OBSERVABILITY CORE TYPES - Domain-specific core types
    # =========================================================================

    class ObservabilityCore:
        """Core observability types extending FlextTypes for complex domain operations."""

        # Metric collection and processing types
        type MetricCollection = dict[
            str, float | int | Decimal | dict[str, FlextTypes.JsonValue]
        ]
        type MetricAggregation = dict[str, float | dict[str, float | int | Decimal]]
        type MetricThresholds = dict[str, float | int | bool | FlextTypes.Dict]
        type MetricConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.ConfigValue]
        ]

        # Tracing and span types
        type TraceConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.JsonValue]
        ]
        type SpanAttributes = dict[str, str | int | float | bool | FlextTypes.Dict]
        type TraceContext = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type SpanHierarchy = dict[str, list[dict[str, FlextTypes.JsonValue]]]

        # Alerting and notification types
        type AlertConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.JsonValue]
        ]
        type AlertRules = list[dict[str, str | bool | int | float | FlextTypes.Dict]]
        type AlertChannels = dict[str, str | dict[str, FlextTypes.ConfigValue]]

        # Health monitoring types
        type HealthChecks = dict[str, dict[str, float | str | bool]]
        type ComponentStatus = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type SystemMetrics = dict[str, float | int | dict[str, FlextTypes.JsonValue]]

        # Log aggregation types
        type LogConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type LogFilters = dict[str, str | list[str] | dict[str, FlextTypes.JsonValue]]
        type LogProcessing = dict[str, str | dict[str, FlextTypes.JsonValue] | bool]

        # Service discovery types
        type ServiceRegistry = dict[str, dict[str, str | int | FlextTypes.Dict]]
        type ServiceDiscovery = dict[str, list[dict[str, FlextTypes.JsonValue]]]
        type ServiceHealth = dict[str, str | dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # OBSERVABILITY PROTOCOLS - Protocol definitions for observability interfaces
    # =========================================================================

    class Protocols:
        """Protocol definitions for observability interfaces and contracts."""

        class MetricProtocol(Protocol):
            """Protocol for metric collection and reporting."""

            def name(self) -> str:
                """Get metric name."""
                ...

            def value(self) -> float | int | Decimal:
                """Get metric value."""
                ...

            def unit(self) -> str:
                """Get metric unit."""
                ...

            def timestamp(self) -> datetime:
                """Get metric timestamp."""
                ...

            def tags(self) -> dict[str, str | int | float]:
                """Get metric tags."""
                ...

        class TraceProtocol(Protocol):
            """Protocol for distributed tracing."""

            def operation(self) -> str:
                """Get operation name."""
                ...

            def span_id(self) -> str:
                """Get span ID."""
                ...

            def trace_id(self) -> str:
                """Get trace ID."""
                ...

            def span_attributes(self) -> FlextTypes.Dict:
                """Get span attributes."""
                ...

            def duration_ms(self) -> float | None:
                """Get duration in milliseconds."""
                ...

            def status(self) -> str:
                """Get trace status."""
                ...

            def timestamp(self) -> datetime:
                """Get trace timestamp."""
                ...

        class AlertProtocol(Protocol):
            """Protocol for alerting and notifications."""

            def title(self) -> str:
                """Get alert title."""
                ...

            def message(self) -> str:
                """Get alert message."""
                ...

            def severity(self) -> str:
                """Get alert severity."""
                ...

            def status(self) -> str:
                """Get alert status."""
                ...

            def tags(self) -> dict[str, str | int | float]:
                """Get alert tags."""
                ...

            def timestamp(self) -> datetime:
                """Get alert timestamp."""
                ...

        class HealthCheckProtocol(Protocol):
            """Protocol for health monitoring."""

            def component(self) -> str:
                """Get component name."""
                ...

            def status(self) -> str:
                """Get health status."""
                ...

            def message(self) -> str:
                """Get health message."""
                ...

            def metrics(self) -> FlextTypes.Dict:
                """Get health metrics."""
                ...

            def timestamp(self) -> datetime:
                """Get health check timestamp."""
                ...

        class LogEntryProtocol(Protocol):
            """Protocol for log aggregation."""

            def message(self) -> str:
                """Get log message."""
                ...

            def level(self) -> str:
                """Get log level."""
                ...

            def context(self) -> FlextTypes.Dict:
                """Get log context."""
                ...

            def timestamp(self) -> datetime:
                """Get log timestamp."""
                ...


# =============================================================================
# PUBLIC API EXPORTS - FlextObservabilityTypes and related types
# =============================================================================

__all__ = [
    "FlextObservabilityTypes",
    "T",
]
