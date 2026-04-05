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

from pydantic import ConfigDict, Field, computed_field

from flext_core import FlextModels
from flext_observability import c, t


class FlextObservabilityModels(FlextModels):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    class Observability:
        """Observability domain models namespace."""

        class GenericObservabilityEntry(FlextModels.DynamicModel):
            """Generic base model for any observability entry using Pydantic."""

            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                frozen=False,
            )

            id: Annotated[
                t.NonEmptyStr,
                Field(
                    description="Unique entity identifier",
                ),
            ] = Field(
                default_factory=lambda: str(uuid4()),
                description="Unique entity identifier",
            )
            name: Annotated[t.NonEmptyStr, Field(description="Entity name")]
            type: Annotated[t.NonEmptyStr, Field(description="Entity type")]
            timestamp: Annotated[
                datetime,
                Field(
                    description="Entry timestamp",
                ),
            ] = Field(default_factory=datetime.now, description="Entry timestamp")
            data: Annotated[
                t.ConfigurationMapping,
                Field(
                    description="Generic data payload",
                ),
            ] = Field(default_factory=dict, description="Generic data payload")
            metadata: Annotated[
                t.ConfigurationMapping,
                Field(
                    description="Generic metadata",
                ),
            ] = Field(default_factory=dict, description="Generic metadata")

            @computed_field
            def age_seconds(self) -> float:
                """Computed age in seconds since creation."""
                return (datetime.now(tz=UTC) - self.timestamp).total_seconds()

            @computed_field
            def data_keys(self) -> t.StrSequence:
                """List of data keys for introspection."""
                return list(self.data.keys()) if self.data else []

            @computed_field
            def has_data(self) -> bool:
                """Check if entry has any data."""
                return bool(self.data)

        class GenericObservabilityConfig(FlextModels.DynamicModel):
            """Generic configuration using Pydantic patterns."""

            model_config: ClassVar[ConfigDict] = ConfigDict(
                validate_assignment=True,
                frozen=False,
            )

            enabled: Annotated[
                bool,
                Field(default=True, description="Enable observability"),
            ]
            interval_seconds: Annotated[
                t.PositiveFloat,
                Field(
                    default=60.0,
                    description="Collection interval",
                ),
            ]
            retention_days: Annotated[
                t.PositiveInt,
                Field(
                    le=365,
                    default=30,
                    description="Retention period",
                ),
            ]
            settings: Annotated[
                t.ConfigurationMapping,
                Field(
                    description="Type-specific settings",
                ),
            ] = Field(default_factory=dict, description="Type-specific settings")

            @computed_field
            def interval_minutes(self) -> float:
                """Computed interval in minutes."""
                return self.interval_seconds / 60.0

            @computed_field
            def retention_hours(self) -> float:
                """Computed retention in hours."""
                return self.retention_days * 24.0

        """Metrics domain models."""

        class MetricEntry(FlextModels.Entity):
            """Metric entry model."""

            metric_id: Annotated[
                str,
                Field(description="Unique metric entry identifier"),
            ] = Field(
                default_factory=lambda: str(uuid4()),
                description="Unique metric entry identifier",
            )
            name: Annotated[t.NonEmptyStr, Field(description="Metric name")]
            value: Annotated[t.Numeric, Field(description="Metric value")]
            unit: Annotated[t.NonEmptyStr, Field(description="Measurement unit")]
            source: Annotated[
                str, Field(default="unknown", description="Metric data source")
            ]

        # --- Domain entity models (moved from _core.py FlextObservability) ---

        class Metric(FlextModels.Entity):
            """Observability metric entity."""

            id: Annotated[
                str,
                Field(description="Unique metric identifier"),
            ] = Field(
                default_factory=lambda: str(uuid4()),
                description="Unique metric identifier",
            )
            name: Annotated[t.NonEmptyStr, Field(description="Metric name")]
            value: Annotated[t.PositiveFloat, Field(description="Metric value")]
            unit: Annotated[t.NonEmptyStr, Field(description="Measurement unit")]
            metric_type: Annotated[t.NonEmptyStr, Field(description="Type of metric")]
            labels: Annotated[
                t.Observability.DomainLabels,
                Field(description="Metric labels for categorization"),
            ] = Field(
                default_factory=dict, description="Metric labels for categorization"
            )

        class Trace(FlextModels.Entity):
            """Distributed trace entity."""

            trace_id: Annotated[
                str,
                Field(description="Unique trace identifier"),
            ] = Field(
                default_factory=lambda: str(uuid4()),
                description="Unique trace identifier",
            )
            name: Annotated[t.NonEmptyStr, Field(description="Trace name")]
            attributes: Annotated[
                t.Observability.DomainLabels,
                Field(description="Trace attributes"),
            ] = Field(default_factory=dict, description="Trace attributes")

        class Alert(FlextModels.Entity):
            """Observability alert entity."""

            id: Annotated[
                str,
                Field(description="Unique alert identifier"),
            ] = Field(
                default_factory=lambda: str(uuid4()),
                description="Unique alert identifier",
            )
            title: Annotated[t.NonEmptyStr, Field(description="Alert title")]
            message: Annotated[t.NonEmptyStr, Field(description="Alert message")]
            severity: Annotated[
                t.NonEmptyStr, Field(description="Alert severity level")
            ]
            source: Annotated[t.NonEmptyStr, Field(description="Alert source")]
            labels: Annotated[
                t.Observability.DomainLabels,
                Field(description="Alert labels for categorization"),
            ] = Field(
                default_factory=dict, description="Alert labels for categorization"
            )

        class HealthCheck(FlextModels.Entity):
            """Health check entity."""

            id: Annotated[
                str,
                Field(description="Unique health check identifier"),
            ] = Field(
                default_factory=lambda: str(uuid4()),
                description="Unique health check identifier",
            )
            component: Annotated[
                t.NonEmptyStr, Field(description="Component being checked")
            ]
            status: Annotated[t.NonEmptyStr, Field(description="Health check status")]
            details: Annotated[
                t.Observability.DomainLabels,
                Field(description="Health check details"),
            ] = Field(default_factory=dict, description="Health check details")

        class LogEntry(FlextModels.Entity):
            """Structured log entry entity."""

            id: Annotated[
                str,
                Field(description="Unique log entry identifier"),
            ] = Field(
                default_factory=lambda: str(uuid4()),
                description="Unique log entry identifier",
            )
            message: Annotated[t.NonEmptyStr, Field(description="Log message")]
            level: Annotated[t.NonEmptyStr, Field(description="Log level")]
            component: Annotated[t.NonEmptyStr, Field(description="Source component")]
            timestamp: Annotated[
                datetime,
                Field(description="Log entry timestamp"),
            ] = Field(
                default_factory=lambda: datetime.now(tz=UTC),
                description="Log entry timestamp",
            )
            context: Annotated[
                t.Observability.DomainLabels,
                Field(description="Log context metadata"),
            ] = Field(default_factory=dict, description="Log context metadata")

        class StartTimePayload(FlextModels.Value):
            """Payload for validating HTTP request start time."""

            value: Annotated[
                float,
                Field(ge=0, description="Request start time in seconds since epoch"),
            ]

        class HeadersPayload(FlextModels.Value):
            """Payload for validating HTTP client headers."""

            headers: Annotated[
                t.StrMapping,
                Field(description="HTTP header key-value pairs"),
            ] = Field(default_factory=dict, description="HTTP header key-value pairs")

        # --- Moved from advanced_context.py ---
        class ContextSnapshot(FlextModels.Value):
            """Snapshot of observability context for restoration in async operations."""

            correlation_id: Annotated[
                str, Field(default="", description="Correlation identifier")
            ]
            trace_id: Annotated[str, Field(default="", description="Trace identifier")]
            span_id: Annotated[str, Field(default="", description="Span identifier")]
            baggage: Annotated[
                t.StrMapping,
                Field(description="Propagated baggage key-value pairs"),
            ] = Field(
                default_factory=dict, description="Propagated baggage key-value pairs"
            )
            metadata: Annotated[
                t.ConfigurationMapping,
                Field(description="Additional context metadata"),
            ] = Field(default_factory=dict, description="Additional context metadata")

        # --- Moved from context.py ---
        class BaggageKeyModel(FlextModels.Value):
            """Validation model for baggage keys."""

            key: Annotated[t.NonEmptyStr, Field(description="Baggage key name")]

        # --- Moved from custom_metrics.py ---
        class MetricTypeInput(FlextModels.Value):
            """Validation model for metric type input."""

            metric_type: Annotated[
                c.Observability.MetricType,
                Field(description="Type of metric to create"),
            ]

        class CustomMetricDefinition(FlextModels.Value):
            """Definition of a custom business metric with type and metadata."""

            name: Annotated[t.NonEmptyStr, Field(description="Custom metric name")]
            metric_type: Annotated[
                c.Observability.MetricType,
                Field(description="Type of metric"),
            ]
            description: Annotated[
                t.NonEmptyStr, Field(description="Human-readable metric description")
            ]
            unit: Annotated[
                str,
                Field(
                    default="1",
                    min_length=1,
                    description="Measurement unit",
                ),
            ]
            labels: Annotated[
                t.StrMapping,
                Field(description="Metric labels for categorization"),
            ] = Field(
                default_factory=dict, description="Metric labels for categorization"
            )

        # --- Moved from error_handling.py ---
        class CooldownInput(FlextModels.Value):
            """Validation model for cooldown seconds input."""

            seconds: Annotated[
                t.PositiveFloat, Field(description="Cooldown duration in seconds")
            ]

        class ThresholdInput(FlextModels.Value):
            """Validation model for threshold input."""

            threshold: Annotated[
                t.PositiveInt, Field(description="Error count threshold")
            ]

        class ErrorEvent(FlextModels.Value):
            """Error event with fingerprinting for deduplication and alerting."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            error_type: Annotated[
                t.NonEmptyStr, Field(description="Error classification type")
            ]
            message: Annotated[t.NonEmptyStr, Field(description="Error message")]
            severity: Annotated[
                c.Observability.ErrorSeverity,
                Field(description="Error severity level"),
            ] = c.Observability.ErrorSeverity.ERROR
            fingerprint: Annotated[
                str, Field(default="", description="SHA256 deduplication fingerprint")
            ]
            correlation_id: Annotated[
                str, Field(default="", description="Correlation identifier")
            ]

            def calculate_fingerprint(self) -> None:
                """Calculate SHA256 fingerprint from error type and message."""
                self.fingerprint = sha256(
                    f"{self.error_type}:{self.message}".encode(),
                ).hexdigest()

        # --- Moved from health.py ---
        class HealthCheckFactoryKwargs(FlextModels.Value):
            """Validation model for health check factory kwargs."""

            metrics: Annotated[
                t.Dict | None,
                Field(description="Health check metric values"),
            ] = None
            timestamp: Annotated[
                datetime | None,
                Field(description="Health check timestamp"),
            ] = None

        class HealthCheckModel(FlextModels.Value):
            """Health check result model."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            component: Annotated[
                t.NonEmptyStr, Field(description="Component being checked")
            ]
            status: Annotated[
                str,
                Field(
                    default="unknown",
                    min_length=1,
                    description="Health check status",
                ),
            ]
            message: Annotated[
                str, Field(default="", description="Health check message")
            ]
            metrics: Annotated[
                t.Dict,
                Field(description="Health check metric values"),
            ] = Field(
                default_factory=lambda: t.Dict({}),
                description="Health check metric values",
            )
            timestamp: Annotated[
                datetime,
                Field(description="Health check timestamp"),
            ] = Field(
                default_factory=datetime.now, description="Health check timestamp"
            )

        # --- Moved from logging_integration.py ---
        class LogContext(FlextModels.Value):
            """Trace context for enriching log entries with correlation and span IDs."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            correlation_id: Annotated[
                str | None,
                Field(description="Correlation identifier"),
            ] = None
            trace_id: Annotated[
                str | None,
                Field(description="Trace identifier"),
            ] = None
            span_id: Annotated[
                str | None,
                Field(description="Span identifier"),
            ] = None
            baggage: Annotated[
                str | None,
                Field(description="Serialized baggage string"),
            ] = None
            extra: Annotated[
                t.Dict,
                Field(description="Additional context data"),
            ] = Field(
                default_factory=lambda: t.Dict({}),
                description="Additional context data",
            )

        # --- Moved from performance.py ---
        class PerformanceMetrics(FlextModels.Value):
            """Metrics for tracking performance of observability operations."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            operation: Annotated[
                t.NonEmptyStr, Field(description="Operation name being measured")
            ]
            start_time: Annotated[
                float,
                Field(description="Operation start time in seconds since epoch"),
            ] = Field(
                default_factory=time.time,
                description="Operation start time in seconds since epoch",
            )
            end_time: Annotated[
                float,
                Field(
                    default=0.0, description="Operation end time in seconds since epoch"
                ),
            ]
            duration_ms: Annotated[
                float,
                Field(default=0.0, description="Operation duration in milliseconds"),
            ]
            memory_used_mb: Annotated[
                float,
                Field(default=0.0, description="Memory used in megabytes"),
            ]
            cpu_percent: Annotated[
                float,
                Field(default=0.0, description="CPU usage percentage"),
            ]
            success: Annotated[
                bool,
                Field(default=True, description="Whether the operation succeeded"),
            ]
            error_message: Annotated[
                str,
                Field(default="", description="Error message if operation failed"),
            ]

            def calculate_duration(self) -> None:
                """Calculate operation duration in milliseconds from start and end times."""
                if self.end_time <= 0:
                    self.end_time = time.time()
                self.duration_ms = max(0.0, (self.end_time - self.start_time) * 1000.0)


m = FlextObservabilityModels

__all__ = ["FlextObservabilityModels", "m"]
