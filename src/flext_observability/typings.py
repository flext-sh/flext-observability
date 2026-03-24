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
            t.Scalar | Sequence[str] | t.Dict,
        ]
        type MonitoringConfig = Mapping[str, t.Scalar | Sequence[str]]
        type MetricsConfig = Mapping[str, bool | str | t.ScalarMapping]
        type TracingConfig = Mapping[str, t.Scalar | Sequence[str] | t.Dict]

        type MetricCollection = Mapping[str, float | int | Decimal | t.ScalarMapping]
        type MetricAggregation = Mapping[
            str, float | Mapping[str, float | int | Decimal]
        ]
        type MetricThresholds = Mapping[str, float | int | bool | t.ScalarMapping]
        type MetricConfiguration = Mapping[str, bool | str | int | t.ScalarMapping]
        type TraceConfiguration = Mapping[str, t.Scalar | t.ScalarMapping]
        type SpanAttributes = Mapping[str, t.Scalar | t.ScalarMapping]
        type TraceContext = Mapping[str, str | int | t.ScalarMapping]
        type SpanHierarchy = Mapping[str, Sequence[t.Dict]]
        type AlertConfiguration = Mapping[str, t.Scalar | t.ScalarMapping]
        type AlertRules = Sequence[
            Mapping[str, str | bool | int | float | t.ScalarMapping]
        ]
        type AlertChannels = Mapping[str, str | t.ScalarMapping]
        type HealthChecks = Mapping[str, Mapping[str, float | str | bool]]
        type ComponentStatus = Mapping[str, str | int | t.ScalarMapping]
        type SystemMetrics = Mapping[str, float | int | t.ScalarMapping]
        type LogConfiguration = Mapping[str, t.Scalar | t.ScalarMapping]
        type LogFilters = Mapping[str, str | Sequence[str] | t.ScalarMapping]
        type LogProcessing = Mapping[str, str | t.ScalarMapping | bool]
        type ServiceRegistry = Mapping[str, Mapping[str, str | int | t.ScalarMapping]]
        type ServiceDiscovery = Mapping[str, Sequence[t.Dict]]
        type ServiceHealth = Mapping[str, str | t.ScalarMapping]
        type MetadataDict = Mapping[str, t.Scalar]
        type ServicesList = Sequence[tuple[str, t.Dict]]
        type HealthMetricsDict = t.ContainerMapping
        type MetricDict = t.ContainerMapping
        type StringList = Sequence[str]


t = FlextObservabilityTypes

__all__ = ["FlextObservabilityTypes", "t"]
