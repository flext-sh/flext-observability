"""FLEXT Observability Fields - Unified field validation and definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations
from flext_observability import c

from datetime import UTC, datetime
from typing import ClassVar

from pydantic import Field, field_validator

from flext_observability import t


class FlextObservabilityFields:
    """Unified observability fields class with validation logic.

    Single unified class containing all field validation and definition logic
    for observability entities. Follows FLEXT namespace class pattern.
    """

    METRIC_VALID_UNITS: ClassVar[set[str]] = {
        "count",
        "percent",
        "bytes",
        "seconds",
        "milliseconds",
        "requests",
        "errors",
        "connections",
        "memory",
        "cpu",
    }
    ALERT_VALID_LEVELS: ClassVar[set[str]] = {
        c.Observability.AlertLevel.INFO,
        c.Observability.AlertLevel.WARNING,
        c.Observability.AlertLevel.ERROR,
        c.Observability.AlertLevel.CRITICAL,
    }
    TRACE_VALID_STATUSES: ClassVar[set[str]] = {
        c.Observability.TraceStatus.STARTED,
        c.Observability.TraceStatus.RUNNING,
        c.Observability.TraceStatus.COMPLETED,
        c.Observability.TraceStatus.FAILED,
    }
    HEALTH_VALID_STATUSES: ClassVar[set[str]] = {
        c.Observability.HealthStatus.HEALTHY,
        c.Observability.HealthStatus.DEGRADED,
        c.Observability.HealthStatus.UNHEALTHY,
    }

    class MetricFields:
        """Nested class for metric field validation."""

        @field_validator("unit")
        @classmethod
        def validate_metric_unit(cls, v: str) -> str:
            """Validate metric unit is from allowed set."""
            if v not in FlextObservabilityFields.METRIC_VALID_UNITS:
                msg = f"Invalid metric unit: {v}. Must be one of {FlextObservabilityFields.METRIC_VALID_UNITS}"
                raise ValueError(msg)
            return v

        @field_validator("value")
        @classmethod
        def validate_metric_value(cls, v: float) -> float:
            """Validate metric value is numeric and non-negative."""
            numeric_value = float(v)
            if numeric_value < 0:
                msg = "Metric value cannot be negative"
                raise ValueError(msg)
            return numeric_value

    @classmethod
    def create_alert_message_field(cls) -> t.Scalar:
        """Create alert message field."""
        return Field(min_length=1, max_length=1000, description="Alert message")

    @classmethod
    def create_metric_name_field(cls) -> t.Scalar:
        """Create metric name field."""
        return Field(min_length=1, max_length=255, description="Metric name")

    @classmethod
    def create_metric_unit_field(cls) -> t.Scalar:
        """Create metric unit field."""
        return Field(
            default=c.Observability.Defaults.DEFAULT_METRIC_UNIT,
            description="Metric unit",
        )

    @classmethod
    def create_metric_value_field(cls) -> t.Scalar:
        """Create metric value field."""
        return Field(ge=0.0, description="Metric value (non-negative)")

    @classmethod
    def create_timestamp_field(cls) -> t.Scalar:
        """Create timestamp field."""
        return Field(default_factory=lambda: datetime.now(UTC), description="Timestamp")

    @classmethod
    def create_trace_name_field(cls) -> t.Scalar:
        """Create trace name field."""
        return Field(min_length=1, max_length=255, description="Trace operation name")


__all__ = ["FlextObservabilityFields"]
