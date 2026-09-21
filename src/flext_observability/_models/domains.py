"""Observability domain models owned by the private models family."""

from __future__ import annotations

import time
from datetime import datetime
from hashlib import sha256
from types import MappingProxyType
from typing import Annotated, Self
from uuid import uuid4

from flext_cli import m

from flext_core import t
from flext_observability import c


class FlextObservabilityModelsDomains:
    """Observability domain models namespace."""

    """Observability domain models namespace."""

    """Metrics domain models."""

    class MetricEntry(m.Entity):
        """Metric entry model."""

        metric_id: Annotated[
            str,
            m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique metric entry identifier",
            ),
        ]
        name: Annotated[t.NonEmptyStr, m.Field(description="Metric name")]
        value: Annotated[t.Numeric, m.Field(description="Metric value")]
        unit: Annotated[t.NonEmptyStr, m.Field(description="Measurement unit")]
        source: Annotated[str, m.Field(description="Metric data source")] = "unknown"

    class _EntityWithId(m.Entity):
        """Base for domain entities with auto-generated unique ID."""

        id: Annotated[
            str,
            m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique entity identifier",
            ),
        ]

    # --- Domain entity models (moved from _core.py FlextObservability) ---

    class Metric(_EntityWithId):
        """Observability metric entity."""

        name: Annotated[t.NonEmptyStr, m.Field(description="Metric name")]
        value: Annotated[t.PositiveFloat, m.Field(description="Metric value")]
        unit: Annotated[t.NonEmptyStr, m.Field(description="Measurement unit")]
        metric_type: Annotated[t.NonEmptyStr, m.Field(description="Type of metric")]
        labels: Annotated[
            t.ScalarMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
                description="Metric labels for categorization",
            ),
        ]

    class Trace(m.Entity):
        """Distributed trace entity."""

        trace_id: Annotated[
            str,
            m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique trace identifier",
            ),
        ]
        name: Annotated[t.NonEmptyStr, m.Field(description="Trace name")]
        attributes: Annotated[
            t.ScalarMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
                description="Trace attributes",
            ),
        ]

    class Alert(_EntityWithId):
        """Observability alert entity."""

        title: Annotated[t.NonEmptyStr, m.Field(description="Alert title")]
        message: Annotated[t.NonEmptyStr, m.Field(description="Alert message")]
        severity: Annotated[t.NonEmptyStr, m.Field(description="Alert severity level")]
        source: Annotated[t.NonEmptyStr, m.Field(description="Alert source")]
        labels: Annotated[
            t.ScalarMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
                description="Alert labels for categorization",
            ),
        ]

    class HealthCheck(_EntityWithId):
        """Health check entity."""

        component: Annotated[
            t.NonEmptyStr, m.Field(description="Component being checked")
        ]
        status: Annotated[t.NonEmptyStr, m.Field(description="Health check status")]
        details: Annotated[
            t.ScalarMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
                description="Health check details",
            ),
        ]

    class LogEntry(_EntityWithId):
        """Structured log entry entity."""

        message: Annotated[t.NonEmptyStr, m.Field(description="Log message")]
        level: Annotated[t.NonEmptyStr, m.Field(description="Log level")]
        component: Annotated[t.NonEmptyStr, m.Field(description="Source component")]
        timestamp: Annotated[
            datetime,
            m.Field(default_factory=datetime.now, description="Log entry timestamp"),
        ]
        context: Annotated[
            t.ScalarMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
                description="Log context metadata",
            ),
        ]

    class StartTimePayload(m.Value):
        """Payload for validating HTTP request start time."""

        value: Annotated[
            float,
            m.Field(ge=0, description="Request start time in seconds since epoch"),
        ]

    class HeadersPayload(m.Value):
        """Payload for validating HTTP client headers."""

        headers: Annotated[
            t.StrMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, str]({}),
                description="HTTP header key-value pairs",
            ),
        ]

    # --- Moved from advanced_context.py ---
    class ContextSnapshot(m.Value):
        """Snapshot of observability context for restoration in async operations."""

        correlation_id: Annotated[
            str, m.Field(description="Correlation identifier")
        ] = ""
        trace_id: Annotated[str, m.Field(description="Trace identifier")] = ""
        span_id: Annotated[str, m.Field(description="Span identifier")] = ""
        baggage: Annotated[
            t.StrMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, str]({}),
                description="Propagated baggage key-value pairs",
            ),
        ]
        metadata: Annotated[
            t.ConfigurationMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
                description="Additional context metadata",
            ),
        ]

    # --- Moved from context.py ---
    class BaggageKeyModel(m.Value):
        """Validation model for baggage keys."""

        key: Annotated[t.NonEmptyStr, m.Field(description="Baggage key name")]

    # --- Moved from custom_metrics.py ---
    class MetricTypeInput(m.Value):
        """Validation model for metric type input."""

        metric_type: Annotated[
            c.Observability.MetricType, m.Field(description="Type of metric to create")
        ]

    class CustomMetricDefinition(m.Value):
        """Definition of a custom business metric with type and metadata."""

        name: Annotated[t.NonEmptyStr, m.Field(description="Custom metric name")]
        metric_type: Annotated[
            c.Observability.MetricType, m.Field(description="Type of metric")
        ]
        description: Annotated[
            t.NonEmptyStr, m.Field(description="Human-readable metric description")
        ]
        unit: Annotated[str, m.Field(min_length=1, description="Measurement unit")] = (
            "1"
        )
        labels: Annotated[
            t.StrMapping,
            m.Field(
                default_factory=lambda: MappingProxyType[str, str]({}),
                description="Metric labels for categorization",
            ),
        ]

    # --- Moved from error_handling.py ---
    class CooldownInput(m.Value):
        """Validation model for cooldown seconds input."""

        seconds: Annotated[
            t.PositiveFloat, m.Field(description="Cooldown duration in seconds")
        ]

    class ThresholdInput(m.Value):
        """Validation model for threshold input."""

        threshold: Annotated[
            t.PositiveInt, m.Field(description="Error count threshold")
        ]

    class ErrorEvent(m.Value):
        """Error event with fingerprinting for deduplication and alerting."""

        error_type: Annotated[
            t.NonEmptyStr, m.Field(description="Error classification type")
        ]
        message: Annotated[t.NonEmptyStr, m.Field(description="Error message")]
        severity: Annotated[
            c.Observability.ErrorSeverity, m.Field(description="Error severity level")
        ] = c.Observability.ErrorSeverity.ERROR
        fingerprint: Annotated[
            str, m.Field(description="SHA256 deduplication fingerprint")
        ] = ""
        correlation_id: Annotated[
            str, m.Field(description="Correlation identifier")
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
    class LogContext(m.Value):
        """Trace context for enriching log entries with correlation and span IDs."""

        correlation_id: Annotated[
            str | None, m.Field(description="Correlation identifier")
        ] = None
        trace_id: Annotated[str | None, m.Field(description="Trace identifier")] = None
        span_id: Annotated[str | None, m.Field(description="Span identifier")] = None
        baggage: Annotated[
            str | None, m.Field(description="Serialized baggage string")
        ] = None
        extra: Annotated[m.Dict, m.Field(description="Additional context data")] = (
            m.Field(default_factory=lambda: m.Dict({}))
        )

    # --- Moved from performance.py ---
    class PerformanceMetrics(m.Value):
        """Metrics for tracking performance of observability operations."""

        operation: Annotated[
            t.NonEmptyStr, m.Field(description="Operation name being measured")
        ]
        start_time: Annotated[
            float, m.Field(description="Operation start time in seconds since epoch")
        ] = m.Field(default_factory=time.time)
        end_time: Annotated[
            float, m.Field(description="Operation end time in seconds since epoch")
        ] = 0.0
        duration_ms: Annotated[
            float, m.Field(description="Operation duration in milliseconds")
        ] = 0.0
        memory_used_mb: Annotated[
            float, m.Field(description="Memory used in megabytes")
        ] = 0.0
        cpu_percent: Annotated[float, m.Field(description="CPU usage percentage")] = 0.0
        success: Annotated[
            bool, m.Field(description="Whether the operation succeeded")
        ] = True
        error_message: Annotated[
            str, m.Field(description="Error message if operation failed")
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


__all__: list[str] = ["FlextObservabilityModelsDomains"]
