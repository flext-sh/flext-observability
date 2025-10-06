"""FLEXT Observability Tracing Domain Models.

Provides focused tracing models following the namespace class pattern.
Contains trace entities, configurations, and factory methods for tracing operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Self

from flext_core import FlextModels, FlextResult, FlextTypes
from pydantic import (
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)


class FlextObservabilityTracing(FlextModels):
    """Focused tracing models for observability operations extending FlextModels.

    Provides comprehensive tracing entities, configurations, and operations
    for distributed tracing, span management, and trace correlation within the FLEXT ecosystem.
    """

    # Distributed Tracing Models
    class TraceEntry(FlextModels.Value):
        """Comprehensive trace entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
        )

        trace_id: str = Field(description="Unique trace identifier")
        span_id: str = Field(description="Unique span identifier")
        parent_span_id: str | None = Field(
            default=None, description="Parent span identifier"
        )
        operation_name: str = Field(description="Operation name")
        service_name: str = Field(description="Service name")
        start_time: datetime = Field(
            default_factory=datetime.now, description="Trace start time"
        )
        end_time: datetime | None = Field(default=None, description="Trace end time")
        duration_ms: float | None = Field(
            default=None, description="Duration in milliseconds"
        )
        status: str = Field(default="active", description="Trace status")
        tags: FlextTypes.StringDict = Field(
            default_factory=dict, description="Trace tags"
        )

        @computed_field
        @property
        def trace_key(self) -> str:
            """Computed field for unique trace key."""
            return f"{self.service_name}.{self.operation_name}.{self.span_id}"

        @computed_field
        @property
        def is_root_span(self) -> bool:
            """Computed field indicating if this is a root span."""
            return self.parent_span_id is None

        @computed_field
        @property
        def formatted_duration(self) -> str:
            """Computed field for formatted duration."""
            if self.duration_ms is None:
                return "active"
            return f"{self.duration_ms:.2f}ms"

        @field_validator("operation_name")
        @classmethod
        def validate_operation_name(cls, v: str) -> str:
            """Validate operation name is not empty."""
            if not v or not v.strip():
                msg = "Operation name cannot be empty"
                raise ValueError(msg)
            return v.strip()

        @field_serializer("tags", when_used="json")
        def serialize_tags_with_context(
            self, value: FlextTypes.StringDict, _info: object
        ) -> FlextTypes.Dict:
            """Serialize tags with trace context."""
            return {
                "tags": value,
                "tag_count": len(value),
                "trace_context": {
                    "service": self.service_name,
                    "operation": self.operation_name,
                    "is_root": self.is_root_span,
                },
            }

    class TraceConfig(FlextModels.Configuration):
        """Trace configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
        )

        sampling_rate: float = Field(
            default=0.1,  # 10% sampling
            description="Trace sampling rate (0.0-1.0)",
        )
        max_trace_duration: int = Field(
            default=3600,  # 1 hour
            description="Maximum trace duration in seconds",
        )
        enable_performance_tracing: bool = Field(
            default=True, description="Enable performance tracing"
        )

        @computed_field
        @property
        def sampling_percentage(self) -> float:
            """Computed field for sampling rate as percentage."""
            return self.sampling_rate * 100

        @model_validator(mode="after")
        def validate_trace_config(self) -> Self:
            """Validate trace configuration parameters."""
            if not 0.0 <= self.sampling_rate <= 1.0:
                msg = "Sampling rate must be between 0.0 and 1.0"
                raise ValueError(msg)
            return self

    class FlextTrace(FlextModels.Entity):
        """Distributed Tracing Span Entity for FLEXT Ecosystem.

        Enterprise-grade distributed tracing entity implementing OpenTelemetry-compatible
        span semantics with comprehensive context propagation, timing precision, and
        cross-service correlation.
        """

        trace_id: str = Field(..., description="Trace ID")
        operation: str = Field(..., description="Operation name")
        span_id: str = Field(..., description="Span ID")
        span_attributes: FlextTypes.Dict = Field(
            default_factory=dict,
            description="Span attributes",
        )
        duration_ms: int = Field(default=0, description="Duration in milliseconds")
        status: str = Field(default="pending", description="Trace status")
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

        @field_validator("trace_id")
        @classmethod
        def validate_trace_id(cls, v: str) -> str:
            """Validate trace ID is non-empty for global correlation."""
            if not (v and str(v).strip()):
                msg = "Trace ID cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("operation")
        @classmethod
        def validate_operation_name(cls, v: str) -> str:
            """Validate operation name is meaningful and searchable."""
            if not (v and str(v).strip()):
                msg = "Operation name cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("span_id")
        @classmethod
        def validate_span_id(cls, v: str) -> str:
            """Validate span ID is non-empty for unique identification."""
            if not (v and str(v).strip()):
                msg = "Span ID cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("status")
        @classmethod
        def validate_trace_status(cls, v: str) -> str:
            """Validate trace status is a valid state."""
            valid_statuses = {"pending", "running", "completed", "failed"}
            if v not in valid_statuses:
                msg = f"Invalid trace status: {v}. Must be one of {valid_statuses}"
                raise ValueError(msg)
            return v

        def validate_business_rules(self) -> FlextResult[bool]:
            """Validate distributed tracing business rules."""
            try:
                if not self.trace_id:
                    return FlextResult[bool].fail("Trace ID is required")
                if not self.operation:
                    return FlextResult[bool].fail("Operation name is required")
                if not self.span_id:
                    return FlextResult[bool].fail("Span ID is required")
                if self.status not in {"pending", "running", "completed", "failed"}:
                    return FlextResult[bool].fail(
                        f"Invalid trace status: {self.status}"
                    )
                return FlextResult[bool].ok(True)
            except Exception as e:
                return FlextResult[bool].fail(f"Business rule validation failed: {e}")

    # Factory methods for direct entity creation
    @staticmethod
    def flext_trace(
        trace_id: str,
        operation: str,
        span_id: str,
        status: str = "pending",
        **kwargs: object,
    ) -> FlextResult[FlextObservabilityTracing.FlextTrace]:
        """Create a FlextTrace entity directly."""
        try:
            # Filter kwargs to only include valid FlextTrace parameters
            valid_kwargs: dict[str, object] = {}
            if "span_attributes" in kwargs and isinstance(
                kwargs["span_attributes"], dict
            ):
                valid_kwargs["span_attributes"] = kwargs["span_attributes"]
            if "duration_ms" in kwargs and isinstance(kwargs["duration_ms"], int):
                valid_kwargs["duration_ms"] = kwargs["duration_ms"]
            if "timestamp" in kwargs and isinstance(kwargs["timestamp"], datetime):
                valid_kwargs["timestamp"] = kwargs["timestamp"]

            return FlextResult[FlextObservabilityTracing.FlextTrace].ok(
                FlextObservabilityTracing.FlextTrace(
                    trace_id=trace_id,
                    operation=operation,
                    span_id=span_id,
                    status=status,
                )
            )
        except Exception as e:
            return FlextResult[FlextObservabilityTracing.FlextTrace].fail(
                f"Failed to create trace: {e}"
            )


# Export the focused tracing namespace class
__all__ = [
    "FlextObservabilityTracing",
]
