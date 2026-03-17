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
from typing import TypeVar

from flext_core import FlextTypes

from flext_observability.constants import c

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

        type ObservabilityProjectType = c.ObservabilityProjectType
        type ObservabilityProjectConfig = dict[
            str, str | int | bool | list[str] | t.Dict
        ]
        type MonitoringConfig = dict[str, str | int | bool | list[str]]
        type MetricsConfig = dict[str, bool | str | dict[str, t.Scalar]]
        type TracingConfig = dict[str, str | int | bool | list[str] | t.Dict]

    class ObservabilityCore:
        """Core observability types extending t for complex domain operations."""

        type MetricCollection = dict[str, float | int | Decimal | dict[str, t.Scalar]]
        type MetricAggregation = dict[str, float | dict[str, float | int | Decimal]]
        type MetricThresholds = dict[str, float | int | bool | dict[str, t.Scalar]]
        type MetricConfiguration = dict[str, bool | str | int | dict[str, t.Scalar]]
        type TraceConfiguration = dict[str, str | int | bool | dict[str, t.Scalar]]
        type SpanAttributes = dict[str, t.Scalar | dict[str, t.Scalar]]
        type TraceContext = dict[str, str | int | dict[str, t.Scalar]]
        type SpanHierarchy = dict[str, list[t.Dict]]
        type AlertConfiguration = dict[str, str | int | bool | dict[str, t.Scalar]]
        type AlertRules = list[
            dict[str, str | bool | int | float | dict[str, t.Scalar]]
        ]
        type AlertChannels = dict[str, str | dict[str, t.Scalar]]
        type HealthChecks = dict[str, dict[str, float | str | bool]]
        type ComponentStatus = dict[str, str | int | dict[str, t.Scalar]]
        type SystemMetrics = dict[str, float | int | dict[str, t.Scalar]]
        type LogConfiguration = dict[str, str | int | bool | dict[str, t.Scalar]]
        type LogFilters = dict[str, str | list[str] | dict[str, t.Scalar]]
        type LogProcessing = dict[str, str | dict[str, t.Scalar] | bool]
        type ServiceRegistry = dict[str, dict[str, str | int | dict[str, t.Scalar]]]
        type ServiceDiscovery = dict[str, list[t.Dict]]
        type ServiceHealth = dict[str, str | dict[str, t.Scalar]]
        type MetadataDict = dict[str, t.Scalar]
        type ServicesList = list[tuple[str, t.Dict]]
        type HealthMetricsDict = dict[str, t.NormalizedValue]
        type MetricDict = dict[str, t.NormalizedValue]
        type StringList = list[str]


t = FlextObservabilityTypes
__all__ = ["FlextObservabilityTypes", "T", "t"]
