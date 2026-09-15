"""Generic FLEXT Observability Models.

 Pydantic models with minimal code using composition and delegation.
Single unified class for all observability entities with SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time
from datetime import datetime
from hashlib import sha256
from types import MappingProxyType
from typing import Annotated, Self
from uuid import uuid4

from flext_cli import m as _m

from flext_core import t

from ._models import FlextObservabilityModelsBase
from .constants import FlextObservabilityConstants as _c


class FlextObservabilityModels(_m, FlextObservabilityModelsBase):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    class Observability:
        """Observability domain models namespace."""

        """Metrics domain models."""

        class MetricEntry(_m.Entity):
            """Metric entry model."""

            metric_id: Annotated[
                str,
                _m.Field(
                    default_factory=lambda: str(uuid4()),
                    description="Unique metric entry identifier",
                ),
            ]
            name: Annotated[t.NonEmptyStr, _m.Field(description="Metric name")]
            value: Annotated[t.Numeric, _m.Field(description="Metric value")]
            unit: Annotated[t.NonEmptyStr, _m.Field(description="Measurement unit")]
            source: Annotated[str, _m.Field(description="Metric data source")] = (
                "unknown"
            )

        class _EntityWithId(_m.Entity):
            """Base for domain entities with auto-generated unique ID."""

            id: Annotated[
                str,
                _m.Field(
                    default_factory=lambda: str(uuid4()),
                    description="Unique entity identifier",
                ),
            ]

        # --- Domain entity models (moved from _core.py FlextObservability) ---

        class Metric(_EntityWithId):
            """Observability metric entity."""

            name: Annotated[t.NonEmptyStr, _m.Field(description="Metric name")]
            value: Annotated[t.PositiveFloat, _m.Field(description="Metric value")]
            unit: Annotated[t.NonEmptyStr, _m.Field(description="Measurement unit")]
            metric_type: Annotated[
                t.NonEmptyStr, _m.Field(description="Type of metric")
            ]
            labels: Annotated[
                t.ScalarMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Metric labels for categorization",
                ),
            ]

        class Trace(_m.Entity):
            """Distributed trace entity."""

            trace_id: Annotated[
                str,
                _m.Field(
                    default_factory=lambda: str(uuid4()),
                    description="Unique trace identifier",
                ),
            ]
            name: Annotated[t.NonEmptyStr, _m.Field(description="Trace name")]
            attributes: Annotated[
                t.ScalarMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Trace attributes",
                ),
            ]

        class Alert(_EntityWithId):
            """Observability alert entity."""

            title: Annotated[t.NonEmptyStr, _m.Field(description="Alert title")]
            message: Annotated[t.NonEmptyStr, _m.Field(description="Alert message")]
            severity: Annotated[
                t.NonEmptyStr, _m.Field(description="Alert severity level")
            ]
            source: Annotated[t.NonEmptyStr, _m.Field(description="Alert source")]
            labels: Annotated[
                t.ScalarMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Alert labels for categorization",
                ),
            ]

        class HealthCheck(_EntityWithId):
            """Health check entity."""

            component: Annotated[
                t.NonEmptyStr, _m.Field(description="Component being checked")
            ]
            status: Annotated[
                t.NonEmptyStr, _m.Field(description="Health check status")
            ]
            details: Annotated[
                t.ScalarMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Health check details",
                ),
            ]

        class LogEntry(_EntityWithId):
            """Structured log entry entity."""

            message: Annotated[t.NonEmptyStr, _m.Field(description="Log message")]
            level: Annotated[t.NonEmptyStr, _m.Field(description="Log level")]
            component: Annotated[
                t.NonEmptyStr, _m.Field(description="Source component")
            ]
            timestamp: Annotated[
                datetime,
                _m.Field(
                    default_factory=datetime.now, description="Log entry timestamp"
                ),
            ]
            context: Annotated[
                t.ScalarMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Log context metadata",
                ),
            ]

        class StartTimePayload(_m.Value):
            """Payload for validating HTTP request start time."""

            value: Annotated[
                float,
                _m.Field(ge=0, description="Request start time in seconds since epoch"),
            ]

        class HeadersPayload(_m.Value):
            """Payload for validating HTTP client headers."""

            headers: Annotated[
                t.StrMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="HTTP header key-value pairs",
                ),
            ]

        # --- Moved from advanced_context.py ---
        class ContextSnapshot(_m.Value):
            """Snapshot of observability context for restoration in async operations."""

            correlation_id: Annotated[
                str, _m.Field(description="Correlation identifier")
            ] = ""
            trace_id: Annotated[str, _m.Field(description="Trace identifier")] = ""
            span_id: Annotated[str, _m.Field(description="Span identifier")] = ""
            baggage: Annotated[
                t.StrMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Propagated baggage key-value pairs",
                ),
            ]
            metadata: Annotated[
                t.ConfigurationMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Additional context metadata",
                ),
            ]

        # --- Moved from context.py ---
        class BaggageKeyModel(_m.Value):
            """Validation model for baggage keys."""

            key: Annotated[t.NonEmptyStr, _m.Field(description="Baggage key name")]

        # --- Moved from custom_metrics.py ---
        class MetricTypeInput(_m.Value):
            """Validation model for metric type input."""

            metric_type: Annotated[
                _c.Observability.MetricType,
                _m.Field(description="Type of metric to create"),
            ]

        class CustomMetricDefinition(_m.Value):
            """Definition of a custom business metric with type and metadata."""

            name: Annotated[t.NonEmptyStr, _m.Field(description="Custom metric name")]
            metric_type: Annotated[
                _c.Observability.MetricType, _m.Field(description="Type of metric")
            ]
            description: Annotated[
                t.NonEmptyStr, _m.Field(description="Human-readable metric description")
            ]
            unit: Annotated[
                str, _m.Field(min_length=1, description="Measurement unit")
            ] = "1"
            labels: Annotated[
                t.StrMapping,
                _m.Field(
                    default_factory=lambda: MappingProxyType({}),
                    description="Metric labels for categorization",
                ),
            ]

        # --- Moved from error_handling.py ---
        class CooldownInput(_m.Value):
            """Validation model for cooldown seconds input."""

            seconds: Annotated[
                t.PositiveFloat, _m.Field(description="Cooldown duration in seconds")
            ]

        class ThresholdInput(_m.Value):
            """Validation model for threshold input."""

            threshold: Annotated[
                t.PositiveInt, _m.Field(description="Error count threshold")
            ]

        class ErrorEvent(_m.Value):
            """Error event with fingerprinting for deduplication and alerting."""

            error_type: Annotated[
                t.NonEmptyStr, _m.Field(description="Error classification type")
            ]
            message: Annotated[t.NonEmptyStr, _m.Field(description="Error message")]
            severity: Annotated[
                _c.Observability.ErrorSeverity,
                _m.Field(description="Error severity level"),
            ] = _c.Observability.ErrorSeverity.ERROR
            fingerprint: Annotated[
                str, _m.Field(description="SHA256 deduplication fingerprint")
            ] = ""
            correlation_id: Annotated[
                str, _m.Field(description="Correlation identifier")
            ] = ""

            def calculate_fingerprint(self) -> Self:
                """Calculate SHA256 fingerprint from error type and message.

                Returns:
                    Self: A new instance with the fingerprint populated.

                """
                return self.model_copy(
                    update={
                        "fingerprint": sha256(
                            f"{self.error_type}:{self.message}".encode()
                        ).hexdigest()
                    }
                )

        # --- Moved from health.py ---

        # --- Moved from logging_integration.py ---
        class LogContext(_m.Value):
            """Trace context for enriching log entries with correlation and span IDs."""

            correlation_id: Annotated[
                str | None, _m.Field(description="Correlation identifier")
            ] = None
            trace_id: Annotated[
                str | None, _m.Field(description="Trace identifier")
            ] = None
            span_id: Annotated[str | None, _m.Field(description="Span identifier")] = (
                None
            )
            baggage: Annotated[
                str | None, _m.Field(description="Serialized baggage string")
            ] = None
            extra: Annotated[
                _m.Dict, _m.Field(description="Additional context data")
            ] = _m.Field(default_factory=lambda: _m.Dict({}))

        # --- Moved from performance.py ---
        class PerformanceMetrics(_m.Value):
            """Metrics for tracking performance of observability operations."""

            operation: Annotated[
                t.NonEmptyStr, _m.Field(description="Operation name being measured")
            ]
            start_time: Annotated[
                float,
                _m.Field(description="Operation start time in seconds since epoch"),
            ] = _m.Field(default_factory=time.time)
            end_time: Annotated[
                float, _m.Field(description="Operation end time in seconds since epoch")
            ] = 0.0
            duration_ms: Annotated[
                float, _m.Field(description="Operation duration in milliseconds")
            ] = 0.0
            memory_used_mb: Annotated[
                float, _m.Field(description="Memory used in megabytes")
            ] = 0.0
            cpu_percent: Annotated[
                float, _m.Field(description="CPU usage percentage")
            ] = 0.0
            success: Annotated[
                bool, _m.Field(description="Whether the operation succeeded")
            ] = True
            error_message: Annotated[
                str, _m.Field(description="Error message if operation failed")
            ] = ""

            def calculate_duration(self) -> Self:
                """Calculate operation duration in milliseconds from start and end times.

                Returns:
                    Self: A new instance with end_time and duration_ms populated.

                """
                end_time = self.end_time
                if end_time <= 0:
                    end_time = time.time()
                duration_ms = max(0.0, (end_time - self.start_time) * 1000.0)
                return self.model_copy(
                    update={"end_time": end_time, "duration_ms": duration_ms}
                )


m = FlextObservabilityModels

__all__: list[str] = ["FlextObservabilityModels", "m"]
