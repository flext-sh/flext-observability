"""FLEXT Observability Types - Domain-specific observability type definitions.

This module provides observability-specific type definitions extending t.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends t properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from decimal import Decimal
from typing import Literal, TypeVar

from flext_core import FlextTypes

# Define T TypeVar for generic programming
T = TypeVar("T")


class FlextObservabilityTypes(FlextTypes):
    """Observability-specific type definitions extending t.

    Domain-specific type system for observability and monitoring operations.
    Contains ONLY complex observability-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # OBSERVABILITY PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project:
        """Observability-specific project types.

        Adds observability/monitoring-specific project types.
        Follows domain separation principle:
        Observability domain owns monitoring-specific types.
        """

        # Observability-specific project types extending the generic ones
        type ObservabilityProjectType = Literal[
            # Generic types inherited from t
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
            str,
            str | int | bool | list[str] | object,
        ]
        type MonitoringConfig = dict[str, str | int | bool | list[str]]
        type MetricsConfig = dict[
            str, bool | str | dict[str, FlextTypes.GeneralValueType]
        ]
        type TracingConfig = dict[str, str | int | bool | list[str] | object]

    # =========================================================================
    # OBSERVABILITY CORE TYPES - Commonly used observability-specific types
    # =========================================================================

    # =========================================================================
    # OBSERVABILITY CORE TYPES - Domain-specific core types
    # =========================================================================

    class ObservabilityCore:
        """Core observability types extending t for complex domain operations."""

        # Metric collection and processing types
        type MetricCollection = dict[
            str,
            float | int | Decimal | dict[str, FlextTypes.JsonValue],
        ]
        type MetricAggregation = dict[str, float | dict[str, float | int | Decimal]]
        type MetricThresholds = dict[
            str, float | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type MetricConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.GeneralValueType]
        ]

        # Tracing and span types
        type TraceConfiguration = dict[
            str,
            str | int | bool | dict[str, FlextTypes.JsonValue],
        ]
        type SpanAttributes = dict[
            str, str | int | float | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type TraceContext = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type SpanHierarchy = dict[str, list[dict[str, FlextTypes.JsonValue]]]

        # Alerting and notification types
        type AlertConfiguration = dict[
            str,
            str | int | bool | dict[str, FlextTypes.JsonValue],
        ]
        type AlertRules = list[
            dict[str, str | bool | int | float | dict[str, FlextTypes.GeneralValueType]]
        ]
        type AlertChannels = dict[str, str | dict[str, FlextTypes.GeneralValueType]]

        # Health monitoring types
        type HealthChecks = dict[str, dict[str, float | str | bool]]
        type ComponentStatus = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type SystemMetrics = dict[str, float | int | dict[str, FlextTypes.JsonValue]]

        # Log aggregation types
        type LogConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.GeneralValueType]
        ]
        type LogFilters = dict[str, str | list[str] | dict[str, FlextTypes.JsonValue]]
        type LogProcessing = dict[str, str | dict[str, FlextTypes.JsonValue] | bool]

        # Service discovery types
        type ServiceRegistry = dict[
            str, dict[str, str | int | dict[str, FlextTypes.GeneralValueType]]
        ]
        type ServiceDiscovery = dict[str, list[dict[str, FlextTypes.JsonValue]]]
        type ServiceHealth = dict[str, str | dict[str, FlextTypes.JsonValue]]

        # Additional core types for monitoring
        type MetadataDict = dict[str, FlextTypes.GeneralValueType]
        type ServicesList = list[tuple[str, object]]
        type HealthMetricsDict = dict[str, FlextTypes.GeneralValueType]
        type MetricDict = dict[str, FlextTypes.GeneralValueType]
        type StringList = list[str]

    # Note: All protocol definitions are centralized in protocols.py
    # Use p.Observability.* for protocols (MetricsProtocol, TracingProtocol, etc.)
    # This follows FLEXT SOLID principles - protocols in protocols.py, types in typings.py

    class Observability:
        """Observability types namespace for cross-project access.

        Provides organized access to all Observability types for other FLEXT projects.
        Usage: Other projects can reference `t.Observability.Core.*`, `t.Observability.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.

        Examples:
            from flext_observability.typings import t
            metrics: t.Observability.Core.MetricCollection = ...
            config: t.Observability.Project.ObservabilityProjectConfig = ...

        Note: Namespace composition via inheritance - no aliases needed.
        Access parent namespaces directly through inheritance.

        """


# Alias for simplified usage
t = FlextObservabilityTypes

# Namespace composition via class inheritance
# Observability namespace provides access to nested classes through inheritance
# Access patterns:
# - t.Observability.* for Observability-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)

__all__ = [
    "FlextObservabilityTypes",
    "T",
    "t",
]
