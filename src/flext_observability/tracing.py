"""FLEXT Observability Tracing Domain Models.

Consolidated tracing models in single class with nested structure.
No helpers, getters, setters, fallbacks or compatibility code.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime

from flext_core import FlextCore
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)


class FlextObservabilityTracing(FlextCore.Models):
    """Consolidated tracing domain models in single class.

    Contains all tracing-related models and configurations as nested classes.
    Follows SOLID principles with no external dependencies or compatibility layers.
    """

    class TraceEntry(FlextCore.Models.Value):
        """Trace entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=False,  # Show input for better error messages
            str_strip_whitespace=True,  # Strip whitespace from strings
            str_to_lower=False,  # Keep original case for strings
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
        tags: FlextCore.Types.StringDict = Field(
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
            self, value: FlextCore.Types.StringDict, _info: object
        ) -> FlextCore.Types.Dict:
            """Serialize tags with trace context."""
            return {
                "tags": value,
                "tag_count": len(value),
                "trace_context": f"{self.service_name}.{self.operation_name}",
            }

    class TraceConfig(BaseModel):
        """Trace configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
            str_strip_whitespace=True,
            str_to_lower=False,
        )

        sampling_rate: float = Field(
            default=1.0,  # Sample all traces by default
            description="Trace sampling rate (0.0 to 1.0)",
        )
        max_spans_per_trace: int = Field(
            default=1000,
            description="Maximum spans per trace",
        )
        service_name: str = Field(description="Service name for traces")
        exporter_endpoint: str | None = Field(
            default=None, description="Trace exporter endpoint"
        )
        enable_auto_instrumentation: bool = Field(
            default=True, description="Enable automatic instrumentation"
        )

        @model_validator(mode="after")
        def validate_trace_config(self) -> Self:
            """Validate trace configuration consistency."""
            if not (0.0 <= self.sampling_rate <= 1.0):
                msg = "Sampling rate must be between 0.0 and 1.0"
                raise ValueError(msg)
            if self.max_spans_per_trace <= 0:
                msg = "Max spans per trace must be positive"
                raise ValueError(msg)
            if not self.service_name or not self.service_name.strip():
                msg = "Service name cannot be empty"
                raise ValueError(msg)
            return self


__all__ = [
    "FlextObservabilityTracing",
]
