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

from collections.abc import Mapping, Sequence
from decimal import Decimal

from flext_core import FlextTypes

from flext_observability import c


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
        type ObservabilityProjectConfig = Mapping[
            str,
            str | int | bool | Sequence[str] | t.Dict,
        ]
        type MonitoringConfig = Mapping[str, str | int | bool | Sequence[str]]
        type MetricsConfig = Mapping[str, bool | str | Mapping[str, t.Scalar]]
        type TracingConfig = Mapping[str, str | int | bool | Sequence[str] | t.Dict]

        type MetricCollection = Mapping[
            str, float | int | Decimal | Mapping[str, t.Scalar]
        ]
        type MetricAggregation = Mapping[
            str, float | Mapping[str, float | int | Decimal]
        ]
        type MetricThresholds = Mapping[
            str, float | int | bool | Mapping[str, t.Scalar]
        ]
        type MetricConfiguration = Mapping[
            str, bool | str | int | Mapping[str, t.Scalar]
        ]
        type TraceConfiguration = Mapping[
            str, str | int | bool | Mapping[str, t.Scalar]
        ]
        type SpanAttributes = Mapping[str, t.Scalar | Mapping[str, t.Scalar]]
        type TraceContext = Mapping[str, str | int | Mapping[str, t.Scalar]]
        type SpanHierarchy = Mapping[str, Sequence[t.Dict]]
        type AlertConfiguration = Mapping[
            str, str | int | bool | Mapping[str, t.Scalar]
        ]
        type AlertRules = Sequence[
            Mapping[str, str | bool | int | float | Mapping[str, t.Scalar]]
        ]
        type AlertChannels = Mapping[str, str | Mapping[str, t.Scalar]]
        type HealthChecks = Mapping[str, Mapping[str, float | str | bool]]
        type ComponentStatus = Mapping[str, str | int | Mapping[str, t.Scalar]]
        type SystemMetrics = Mapping[str, float | int | Mapping[str, t.Scalar]]
        type LogConfiguration = Mapping[str, str | int | bool | Mapping[str, t.Scalar]]
        type LogFilters = Mapping[str, str | Sequence[str] | Mapping[str, t.Scalar]]
        type LogProcessing = Mapping[str, str | Mapping[str, t.Scalar] | bool]
        type ServiceRegistry = Mapping[
            str, Mapping[str, str | int | Mapping[str, t.Scalar]]
        ]
        type ServiceDiscovery = Mapping[str, Sequence[t.Dict]]
        type ServiceHealth = Mapping[str, str | Mapping[str, t.Scalar]]
        type MetadataDict = Mapping[str, t.Scalar]
        type ServicesList = Sequence[tuple[str, t.Dict]]
        type HealthMetricsDict = Mapping[str, t.NormalizedValue]
        type MetricDict = Mapping[str, t.NormalizedValue]
        type StringList = Sequence[str]


t = FlextObservabilityTypes

__all__ = ["FlextObservabilityTypes", "t"]
