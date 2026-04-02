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
from flext_observability import FlextObservabilityConstants as c


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

        type ObservabilityProjectType = c.Observability.ObservabilityProjectType
        type ObservabilityProjectConfig = Mapping[
            str,
            FlextTypes.Scalar | FlextTypes.StrSequence | FlextTypes.Dict,
        ]
        type MonitoringConfig = Mapping[str, FlextTypes.Scalar | FlextTypes.StrSequence]
        type MetricsConfig = Mapping[str, bool | str | FlextTypes.ScalarMapping]
        type TracingConfig = Mapping[
            str,
            FlextTypes.Scalar | FlextTypes.StrSequence | FlextTypes.Dict,
        ]

        type MetricCollection = Mapping[
            str,
            float | int | Decimal | FlextTypes.ScalarMapping,
        ]
        type MetricAggregation = Mapping[
            str,
            float | Mapping[str, float | int | Decimal],
        ]
        type MetricThresholds = Mapping[
            str,
            float | int | bool | FlextTypes.ScalarMapping,
        ]
        type MetricConfiguration = Mapping[
            str,
            bool | str | int | FlextTypes.ScalarMapping,
        ]
        type TraceConfiguration = Mapping[
            str,
            FlextTypes.Scalar | FlextTypes.ScalarMapping,
        ]
        type SpanAttributes = Mapping[str, FlextTypes.Scalar | FlextTypes.ScalarMapping]
        type TraceContext = Mapping[str, str | int | FlextTypes.ScalarMapping]
        type SpanHierarchy = Mapping[str, Sequence[FlextTypes.Dict]]
        type AlertConfiguration = Mapping[
            str,
            FlextTypes.Scalar | FlextTypes.ScalarMapping,
        ]
        type AlertRules = Sequence[
            Mapping[str, str | bool | t.Numeric | FlextTypes.ScalarMapping]
        ]
        type AlertChannels = Mapping[str, str | FlextTypes.ScalarMapping]
        type HealthChecks = Mapping[str, Mapping[str, float | str | bool]]
        type ComponentStatus = Mapping[str, str | int | FlextTypes.ScalarMapping]
        type SystemMetrics = Mapping[str, float | int | FlextTypes.ScalarMapping]
        type LogConfiguration = Mapping[
            str,
            FlextTypes.Scalar | FlextTypes.ScalarMapping,
        ]
        type LogFilters = Mapping[
            str,
            str | FlextTypes.StrSequence | FlextTypes.ScalarMapping,
        ]
        type LogProcessing = Mapping[str, str | FlextTypes.ScalarMapping | bool]
        type ServiceRegistry = Mapping[
            str,
            Mapping[str, str | int | FlextTypes.ScalarMapping],
        ]
        type ServiceDiscovery = Mapping[str, Sequence[FlextTypes.Dict]]
        type ServiceHealth = Mapping[str, str | FlextTypes.ScalarMapping]
        type MetadataDict = FlextTypes.ConfigurationMapping
        type ServicesList = Sequence[tuple[str, FlextTypes.Dict]]
        type HealthMetricsDict = FlextTypes.ContainerMapping
        type MetricDict = FlextTypes.ContainerMapping
        type StringList = FlextTypes.StrSequence


t = FlextObservabilityTypes

__all__ = ["FlextObservabilityTypes", "t"]
