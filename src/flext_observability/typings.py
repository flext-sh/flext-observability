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

T = TypeVar("T")


class FlextObservabilityTypes(FlextTypes):
    """Observability-specific type definitions extending t.

    Domain-specific type system for observability and monitoring operations.
    Contains ONLY complex observability-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Observability:
        """Observability-specific project types.

        Adds observability/monitoring-specific project types.
        Follows domain separation principle:
        Observability domain owns monitoring-specific types.
        """

        type ObservabilityProjectType = Literal[
            "library",
            "application",
            "service",
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
        type ObservabilityProjectConfig = dict[
            str, str | int | bool | list[str] | t.Dict
        ]
        type MonitoringConfig = dict[str, str | int | bool | list[str]]
        type MetricsConfig = dict[str, bool | str | dict[str, object]]
        type TracingConfig = dict[str, str | int | bool | list[str] | t.Dict]

    class ObservabilityCore:
        """Core observability types extending t for complex domain operations."""

        type MetricCollection = dict[str, float | int | Decimal | dict[str, object]]
        type MetricAggregation = dict[str, float | dict[str, float | int | Decimal]]
        type MetricThresholds = dict[str, float | int | bool | dict[str, object]]
        type MetricConfiguration = dict[str, bool | str | int | dict[str, object]]
        type TraceConfiguration = dict[str, str | int | bool | dict[str, object]]
        type SpanAttributes = dict[str, t.Scalar | dict[str, object]]
        type TraceContext = dict[str, str | int | dict[str, object]]
        type SpanHierarchy = dict[str, list[dict[str, object]]]
        type AlertConfiguration = dict[str, str | int | bool | dict[str, object]]
        type AlertRules = list[dict[str, str | bool | int | float | dict[str, object]]]
        type AlertChannels = dict[str, str | dict[str, object]]
        type HealthChecks = dict[str, dict[str, float | str | bool]]
        type ComponentStatus = dict[str, str | int | dict[str, object]]
        type SystemMetrics = dict[str, float | int | dict[str, object]]
        type LogConfiguration = dict[str, str | int | bool | dict[str, object]]
        type LogFilters = dict[str, str | list[str] | dict[str, object]]
        type LogProcessing = dict[str, str | dict[str, object] | bool]
        type ServiceRegistry = dict[str, dict[str, str | int | dict[str, object]]]
        type ServiceDiscovery = dict[str, list[dict[str, object]]]
        type ServiceHealth = dict[str, str | dict[str, object]]
        type MetadataDict = dict[str, object]
        type ServicesList = list[tuple[str, t.Dict]]
        type HealthMetricsDict = dict[str, object]
        type MetricDict = dict[str, object]
        type StringList = list[str]


t = FlextObservabilityTypes
__all__ = ["FlextObservabilityTypes", "T", "t"]
