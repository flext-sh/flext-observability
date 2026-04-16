"""Generic FLEXT Observability Models.

 Pydantic models with minimal code using composition and delegation.
Single unified class for all observability entities with SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from hashlib import sha256
from typing import Annotated, ClassVar
from uuid import uuid4

from pydantic import ConfigDict

from flext_core import m
from flext_observability import c, t, u


class FlextObservabilityModels(m):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    class Observability:
        """Observability domain models namespace."""

        class GenericObservabilityEntry(m.DynamicModel):
            """Generic base model for any observability entry using Pydantic."""

            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                frozen=False,
            )

            id: Annotated[
                t.NonEmptyStr,
                m.Field(
                    description="Unique entity identifier",
                ),
            ] = m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique entity identifier",
            )
            name: Annotated[t.NonEmptyStr, m.Field(description="Entity name")]
            type: Annotated[t.NonEmptyStr, m.Field(description="Entity type")]
            timestamp: Annotated[
                datetime,
                m.Field(
                    description="Entry timestamp",
                ),
            ] = m.Field(default_factory=datetime.now, description="Entry timestamp")
            data: Annotated[
                t.ConfigurationMapping,
                m.Field(
                    description="Generic data payload",
                ),
            ] = m.Field(default_factory=dict, description="Generic data payload")
            metadata: Annotated[
                t.ConfigurationMapping,
                m.Field(
                    description="Generic metadata",
                ),
            ] = m.Field(default_factory=dict, description="Generic metadata")

            @u.computed_field()
            @property
            def age_seconds(self) -> float:
                """Computed age in seconds since creation."""
                return (datetime.now(tz=UTC) - self.timestamp).total_seconds()

            @u.computed_field()
            @property
            def data_keys(self) -> t.StrSequence:
                """List of data keys for introspection."""
                return list(self.data.keys()) if self.data else []

            @u.computed_field()
            @property
            def has_data(self) -> bool:
                """Check if entry has any data."""
                return bool(self.data)

        class GenericObservabilityConfig(m.DynamicModel):
            """Generic configuration using Pydantic patterns."""

            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                frozen=False,
            )

            enabled: Annotated[bool, m.Field(description="Enable observability")] = True
            interval_seconds: Annotated[
                t.PositiveFloat,
                m.Field(
                    description="Collection interval",
                ),
            ] = 60.0
            retention_days: Annotated[
                t.PositiveInt,
                m.Field(
                    le=365,
                    description="Retention period",
                ),
            ]
            settings: Annotated[
                t.ConfigurationMapping,
                m.Field(
                    description="Type-specific settings",
                ),
            ] = m.Field(default_factory=dict, description="Type-specific settings")

            @u.computed_field()
            @property
            def interval_minutes(self) -> float:
                """Computed interval in minutes."""
                return self.interval_seconds / 60.0

            @u.computed_field()
            @property
            def retention_hours(self) -> float:
                """Computed retention in hours."""
                return self.retention_days * 24.0

        """Metrics domain models."""

        class MetricEntry(m.Entity):
            """Metric entry model."""

            metric_id: Annotated[
                str,
                m.Field(description="Unique metric entry identifier"),
            ] = m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique metric entry identifier",
            )
            name: Annotated[t.NonEmptyStr, m.Field(description="Metric name")]
            value: Annotated[t.Numeric, m.Field(description="Metric value")]
            unit: Annotated[t.NonEmptyStr, m.Field(description="Measurement unit")]
            source: Annotated[str, m.Field(description="Metric data source")] = (
                "unknown"
            )

        # --- Domain entity models (moved from _core.py FlextObservability) ---

        class Metric(m.Entity):
            """Observability metric entity."""

            id: Annotated[
                str,
                m.Field(description="Unique metric identifier"),
            ] = m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique metric identifier",
            )
            name: Annotated[t.NonEmptyStr, m.Field(description="Metric name")]
            value: Annotated[t.PositiveFloat, m.Field(description="Metric value")]
            unit: Annotated[t.NonEmptyStr, m.Field(description="Measurement unit")]
            metric_type: Annotated[t.NonEmptyStr, m.Field(description="Type of metric")]
            labels: Annotated[
                t.Observability.DomainLabels,
                m.Field(description="Metric labels for categorization"),
            ] = m.Field(
                default_factory=dict, description="Metric labels for categorization"
            )

        class Trace(m.Entity):
            """Distributed trace entity."""

            trace_id: Annotated[
                str,
                m.Field(description="Unique trace identifier"),
            ] = m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique trace identifier",
            )
            name: Annotated[t.NonEmptyStr, m.Field(description="Trace name")]
            attributes: Annotated[
                t.Observability.DomainLabels,
                m.Field(description="Trace attributes"),
            ] = m.Field(default_factory=dict, description="Trace attributes")

        class Alert(m.Entity):
            """Observability alert entity."""

            id: Annotated[
                str,
                m.Field(description="Unique alert identifier"),
            ] = m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique alert identifier",
            )
            title: Annotated[t.NonEmptyStr, m.Field(description="Alert title")]
            message: Annotated[t.NonEmptyStr, m.Field(description="Alert message")]
            severity: Annotated[
                t.NonEmptyStr, m.Field(description="Alert severity level")
            ]
            source: Annotated[t.NonEmptyStr, m.Field(description="Alert source")]
            labels: Annotated[
                t.Observability.DomainLabels,
                m.Field(description="Alert labels for categorization"),
            ] = m.Field(
                default_factory=dict, description="Alert labels for categorization"
            )

        class HealthCheck(m.Entity):
            """Health check entity."""

            id: Annotated[
                str,
                m.Field(description="Unique health check identifier"),
            ] = m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique health check identifier",
            )
            component: Annotated[
                t.NonEmptyStr, m.Field(description="Component being checked")
            ]
            status: Annotated[t.NonEmptyStr, m.Field(description="Health check status")]
            details: Annotated[
                t.Observability.DomainLabels,
                m.Field(description="Health check details"),
            ] = m.Field(default_factory=dict, description="Health check details")

        class LogEntry(m.Entity):
            """Structured log entry entity."""

            id: Annotated[
                str,
                m.Field(description="Unique log entry identifier"),
            ] = m.Field(
                default_factory=lambda: str(uuid4()),
                description="Unique log entry identifier",
            )
            message: Annotated[t.NonEmptyStr, m.Field(description="Log message")]
            level: Annotated[t.NonEmptyStr, m.Field(description="Log level")]
            component: Annotated[t.NonEmptyStr, m.Field(description="Source component")]
            timestamp: Annotated[
                datetime,
                m.Field(description="Log entry timestamp"),
            ] = m.Field(
                default_factory=lambda: datetime.now(tz=UTC),
                description="Log entry timestamp",
            )
            context: Annotated[
                t.Observability.DomainLabels,
                m.Field(description="Log context metadata"),
            ] = m.Field(default_factory=dict, description="Log context metadata")

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
                m.Field(description="HTTP header key-value pairs"),
            ] = m.Field(default_factory=dict, description="HTTP header key-value pairs")

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
                m.Field(description="Propagated baggage key-value pairs"),
            ] = m.Field(
                default_factory=dict, description="Propagated baggage key-value pairs"
            )
            metadata: Annotated[
                t.ConfigurationMapping,
                m.Field(description="Additional context metadata"),
            ] = m.Field(default_factory=dict, description="Additional context metadata")

        # --- Moved from context.py ---
        class BaggageKeyModel(m.Value):
            """Validation model for baggage keys."""

            key: Annotated[t.NonEmptyStr, m.Field(description="Baggage key name")]

        # --- Moved from custom_metrics.py ---
        class MetricTypeInput(m.Value):
            """Validation model for metric type input."""

            metric_type: Annotated[
                c.Observability.MetricType,
                m.Field(description="Type of metric to create"),
            ]

        class CustomMetricDefinition(m.Value):
            """Definition of a custom business metric with type and metadata."""

            name: Annotated[t.NonEmptyStr, m.Field(description="Custom metric name")]
            metric_type: Annotated[
                c.Observability.MetricType,
                m.Field(description="Type of metric"),
            ]
            description: Annotated[
                t.NonEmptyStr, m.Field(description="Human-readable metric description")
            ]
            unit: Annotated[
                str,
                m.Field(
                    min_length=1,
                    description="Measurement unit",
                ),
            ] = "1"
            labels: Annotated[
                t.StrMapping,
                m.Field(description="Metric labels for categorization"),
            ] = m.Field(
                default_factory=dict, description="Metric labels for categorization"
            )

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

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            error_type: Annotated[
                t.NonEmptyStr, m.Field(description="Error classification type")
            ]
            message: Annotated[t.NonEmptyStr, m.Field(description="Error message")]
            severity: Annotated[
                c.Observability.ErrorSeverity,
                m.Field(description="Error severity level"),
            ] = c.Observability.ErrorSeverity.ERROR
            fingerprint: Annotated[
                str, m.Field(description="SHA256 deduplication fingerprint")
            ] = ""
            correlation_id: Annotated[
                str, m.Field(description="Correlation identifier")
            ] = ""

            def calculate_fingerprint(self) -> None:
                """Calculate SHA256 fingerprint from error type and message."""
                self.fingerprint = sha256(
                    f"{self.error_type}:{self.message}".encode(),
                ).hexdigest()

        # --- Moved from health.py ---
        class HealthCheckFactoryKwargs(m.Value):
            """Validation model for health check factory kwargs."""

            metrics: Annotated[
                t.Dict | None,
                m.Field(description="Health check metric values"),
            ] = None
            timestamp: Annotated[
                datetime | None,
                m.Field(description="Health check timestamp"),
            ] = None

        class HealthCheckModel(m.Value):
            """Health check result model."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            component: Annotated[
                t.NonEmptyStr, m.Field(description="Component being checked")
            ]
            status: Annotated[
                str,
                m.Field(
                    min_length=1,
                    description="Health check status",
                ),
            ] = "unknown"
            message: Annotated[str, m.Field(description="Health check message")] = ""
            metrics: Annotated[
                t.Dict,
                m.Field(description="Health check metric values"),
            ] = m.Field(
                default_factory=lambda: t.Dict({}),
                description="Health check metric values",
            )
            timestamp: Annotated[
                datetime,
                m.Field(description="Health check timestamp"),
            ] = m.Field(
                default_factory=datetime.now, description="Health check timestamp"
            )

        # --- Moved from logging_integration.py ---
        class LogContext(m.Value):
            """Trace context for enriching log entries with correlation and span IDs."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            correlation_id: Annotated[
                str | None,
                m.Field(description="Correlation identifier"),
            ] = None
            trace_id: Annotated[
                str | None,
                m.Field(description="Trace identifier"),
            ] = None
            span_id: Annotated[
                str | None,
                m.Field(description="Span identifier"),
            ] = None
            baggage: Annotated[
                str | None,
                m.Field(description="Serialized baggage string"),
            ] = None
            extra: Annotated[
                t.Dict,
                m.Field(description="Additional context data"),
            ] = m.Field(
                default_factory=lambda: t.Dict({}),
                description="Additional context data",
            )

        # --- Moved from performance.py ---
        class PerformanceMetrics(m.Value):
            """Metrics for tracking performance of observability operations."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            operation: Annotated[
                t.NonEmptyStr, m.Field(description="Operation name being measured")
            ]
            start_time: Annotated[
                float,
                m.Field(description="Operation start time in seconds since epoch"),
            ] = m.Field(
                default_factory=time.time,
                description="Operation start time in seconds since epoch",
            )
            end_time: Annotated[
                float, m.Field(description="Operation end time in seconds since epoch")
            ] = 0.0
            duration_ms: Annotated[
                float, m.Field(description="Operation duration in milliseconds")
            ] = 0.0
            memory_used_mb: Annotated[
                float, m.Field(description="Memory used in megabytes")
            ] = 0.0
            cpu_percent: Annotated[
                float, m.Field(description="CPU usage percentage")
            ] = 0.0
            success: Annotated[
                bool, m.Field(description="Whether the operation succeeded")
            ] = True
            error_message: Annotated[
                str, m.Field(description="Error message if operation failed")
            ] = ""

            def calculate_duration(self) -> None:
                """Calculate operation duration in milliseconds from start and end times."""
                if self.end_time <= 0:
                    self.end_time = time.time()
                self.duration_ms = max(0.0, (self.end_time - self.start_time) * 1000.0)


m = FlextObservabilityModels

__all__: list[str] = ["FlextObservabilityModels", "m"]
