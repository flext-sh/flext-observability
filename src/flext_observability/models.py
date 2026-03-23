"""Generic FLEXT Observability Models.

 Pydantic models with minimal code using composition and delegation.
Single unified class for all observability entities with SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from hashlib import sha256
from typing import Annotated, ClassVar
from uuid import uuid4

from flext_core import FlextModels, t
from pydantic import ConfigDict, Field, computed_field

# Deferred import to avoid circular dependency - used inside Observability nested classes
from flext_observability import FlextObservabilityConstants as _c

# Domain scalar type alias used in model fields
_DomainLabels = Mapping[str, t.Scalar]


class FlextObservabilityModels(FlextModels):
    """Generic observability models with Pydantic patterns.

    Single class providing generic base models using composition and delegation.
    Zero domain-specific logic - pure generic foundation with minimal code.
    """

    class GenericObservabilityEntry(FlextModels.Value):
        """Generic base model for any observability entry using Pydantic."""

        model_config: ClassVar[ConfigDict] = ConfigDict(
            validate_assignment=True,
            extra="allow",
            frozen=False,
            str_strip_whitespace=True,
        )

        id: Annotated[
            t.NonEmptyStr,
            Field(
                default_factory=lambda: str(uuid4()),
                description="Unique entity identifier",
            ),
        ]
        name: Annotated[t.NonEmptyStr, Field(description="Entity name")]
        type: Annotated[t.NonEmptyStr, Field(description="Entity type")]
        timestamp: Annotated[
            datetime,
            Field(
                default_factory=datetime.now,
                description="Entry timestamp",
            ),
        ]
        data: Annotated[
            Mapping[str, t.Scalar],
            Field(
                default_factory=dict,
                description="Generic data payload",
            ),
        ]
        metadata: Annotated[
            Mapping[str, t.Scalar],
            Field(
                default_factory=dict,
                description="Generic metadata",
            ),
        ]

        @computed_field
        def age_seconds(self) -> float:
            """Computed age in seconds since creation."""
            return (datetime.now(tz=UTC) - self.timestamp).total_seconds()

        @computed_field
        def data_keys(self) -> Sequence[str]:
            """List of data keys for introspection."""
            return list(self.data.keys()) if self.data else []

        @computed_field
        def has_data(self) -> bool:
            """Check if entry has any data."""
            return bool(self.data)

    class GenericObservabilityConfig(FlextModels.Value):
        """Generic configuration using Pydantic patterns."""

        model_config: ClassVar[ConfigDict] = ConfigDict(
            validate_assignment=True,
            extra="allow",
            frozen=False,
            str_strip_whitespace=True,
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
            int,
            Field(
                ge=1,
                le=365,
                default=30,
                description="Retention period",
            ),
        ]
        settings: Annotated[
            Mapping[str, t.Scalar],
            Field(
                default_factory=dict,
                description="Type-specific settings",
            ),
        ]

        @computed_field
        def interval_minutes(self) -> float:
            """Computed interval in minutes."""
            return self.interval_seconds / 60.0

        @computed_field
        def retention_hours(self) -> float:
            """Computed retention in hours."""
            return self.retention_days * 24.0

    class Observability:
        """Metrics domain models."""

        class MetricEntry(FlextModels.Entity):
            """Metric entry model."""

            metric_id: Annotated[str, Field(default_factory=lambda: str(uuid4()))]
            name: Annotated[str, Field(min_length=1)]
            value: t.Numeric
            unit: str
            source: Annotated[str, Field(default="unknown")]

        # --- Domain entity models (moved from _core.py FlextObservability) ---

        class Metric(FlextModels.Entity):
            """Observability metric entity."""

            id: Annotated[str, Field(default_factory=lambda: str(uuid4()))]
            name: str
            value: float
            unit: str
            metric_type: str
            labels: Annotated[_DomainLabels, Field(default_factory=dict)]

        class Trace(FlextModels.Entity):
            """Distributed trace entity."""

            trace_id: Annotated[str, Field(default_factory=lambda: str(uuid4()))]
            name: str
            attributes: Annotated[_DomainLabels, Field(default_factory=dict)]

        class Alert(FlextModels.Entity):
            """Observability alert entity."""

            id: Annotated[str, Field(default_factory=lambda: str(uuid4()))]
            title: str
            message: str
            severity: str
            source: str
            labels: Annotated[_DomainLabels, Field(default_factory=dict)]

        class HealthCheck(FlextModels.Entity):
            """Health check entity."""

            id: Annotated[str, Field(default_factory=lambda: str(uuid4()))]
            component: str
            status: str
            details: Annotated[_DomainLabels, Field(default_factory=dict)]

        class LogEntry(FlextModels.Entity):
            """Structured log entry entity."""

            id: Annotated[str, Field(default_factory=lambda: str(uuid4()))]
            message: str
            level: str
            component: str
            timestamp: Annotated[
                datetime,
                Field(default_factory=lambda: datetime.now(tz=UTC)),
            ]
            context: Annotated[_DomainLabels, Field(default_factory=dict)]

        class _StartTimePayload(FlextModels.Value):
            """Payload for validating HTTP request start time."""

            value: Annotated[float, Field(ge=0)]

        class _HeadersPayload(FlextModels.Value):
            """Payload for validating HTTP client headers."""

            headers: Annotated[Mapping[str, str], Field(default_factory=dict)]

        # --- Moved from advanced_context.py ---
        class ContextSnapshot(FlextModels.Value):
            """Snapshot of observability context for restoration in async operations."""

            correlation_id: Annotated[str, Field(default="")]
            trace_id: Annotated[str, Field(default="")]
            span_id: Annotated[str, Field(default="")]
            baggage: Annotated[Mapping[str, str], Field(default_factory=dict)]
            metadata: Annotated[Mapping[str, t.Scalar], Field(default_factory=dict)]

        # --- Moved from context.py ---
        class BaggageKeyModel(FlextModels.Value):
            """Validation model for baggage keys."""

            key: Annotated[str, Field(min_length=1)]

        # --- Moved from custom_metrics.py ---
        class MetricTypeInput(FlextModels.Value):
            """Validation model for metric type input."""

            metric_type: _c.Observability.MetricType

        class CustomMetricDefinition(FlextModels.Value):
            """Definition of a custom business metric with type and metadata."""

            name: Annotated[str, Field(min_length=1)]
            metric_type: _c.Observability.MetricType
            description: Annotated[str, Field(min_length=1)]
            unit: Annotated[str, Field(default="1", min_length=1)]
            labels: Annotated[Mapping[str, str], Field(default_factory=dict)]

        # --- Moved from error_handling.py ---
        class CooldownInput(FlextModels.Value):
            """Validation model for cooldown seconds input."""

            seconds: Annotated[float, Field(gt=0)]

        class ThresholdInput(FlextModels.Value):
            """Validation model for threshold input."""

            threshold: Annotated[int, Field(ge=1)]

        class ErrorEvent(FlextModels.Value):
            """Error event with fingerprinting for deduplication and alerting."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            error_type: Annotated[str, Field(min_length=1)]
            message: Annotated[str, Field(min_length=1)]
            severity: _c.Observability.ErrorSeverity = (
                _c.Observability.ErrorSeverity.ERROR
            )
            fingerprint: str = ""
            correlation_id: str = ""

            def calculate_fingerprint(self) -> None:
                """Calculate SHA256 fingerprint from error type and message."""
                self.fingerprint = sha256(
                    f"{self.error_type}:{self.message}".encode(),
                ).hexdigest()

        # --- Moved from health.py ---
        class HealthCheckFactoryKwargs(FlextModels.Value):
            """Validation model for health check factory kwargs."""

            metrics: t.Dict | None = None
            timestamp: datetime | None = None

        class HealthCheckModel(FlextModels.Value):
            """Health check result model."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            component: Annotated[str, Field(min_length=1)]
            status: Annotated[str, Field(default="unknown", min_length=1)]
            message: Annotated[str, Field(default="")]
            metrics: Annotated[t.Dict, Field(default_factory=lambda: t.Dict({}))]
            timestamp: Annotated[datetime, Field(default_factory=datetime.now)]

        # --- Moved from logging_integration.py ---
        class LogContext(FlextModels.Value):
            """Trace context for enriching log entries with correlation and span IDs."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            correlation_id: str | None = None
            trace_id: str | None = None
            span_id: str | None = None
            baggage: str | None = None
            extra: Annotated[t.Dict, Field(default_factory=lambda: t.Dict({}))]

        # --- Moved from performance.py ---
        class PerformanceMetrics(FlextModels.Value):
            """Metrics for tracking performance of observability operations."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=False)

            operation: Annotated[str, Field(min_length=1)]
            start_time: Annotated[float, Field(default_factory=time.time)]
            end_time: float = 0.0
            duration_ms: float = 0.0
            memory_used_mb: float = 0.0
            cpu_percent: float = 0.0
            success: bool = True
            error_message: str = ""

            def calculate_duration(self) -> None:
                """Calculate operation duration in milliseconds from start and end times."""
                if self.end_time <= 0:
                    self.end_time = time.time()
                self.duration_ms = max(0.0, (self.end_time - self.start_time) * 1000.0)


m = FlextObservabilityModels

__all__ = ["FlextObservabilityModels", "m"]
