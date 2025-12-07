"""FLEXT Observability Fields - Unified field validation and definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import ClassVar

from pydantic import Field, field_validator

from flext_observability.constants import FlextObservabilityConstants


class FlextObservabilityFields:
    """Unified observability fields class with validation logic.

    Single unified class containing all field validation and definition logic
    for observability entities. Follows FLEXT namespace class pattern.
    """

    # Metric field validation constants
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

    # Alert field validation constants
    ALERT_VALID_LEVELS: ClassVar[set[str]] = {
        FlextObservabilityConstants.Observability.AlertLevel.INFO,
        FlextObservabilityConstants.Observability.AlertLevel.WARNING,
        FlextObservabilityConstants.Observability.AlertLevel.ERROR,
        FlextObservabilityConstants.Observability.AlertLevel.CRITICAL,
    }

    # Trace field validation constants
    TRACE_VALID_STATUSES: ClassVar[set[str]] = {
        FlextObservabilityConstants.Observability.TraceStatus.STARTED,
        FlextObservabilityConstants.Observability.TraceStatus.RUNNING,
        FlextObservabilityConstants.Observability.TraceStatus.COMPLETED,
        FlextObservabilityConstants.Observability.TraceStatus.FAILED,
    }

    # Health field validation constants
    HEALTH_VALID_STATUSES: ClassVar[set[str]] = {
        FlextObservabilityConstants.Observability.HealthStatus.HEALTHY,
        FlextObservabilityConstants.Observability.HealthStatus.DEGRADED,
        FlextObservabilityConstants.Observability.HealthStatus.UNHEALTHY,
    }

    class MetricFields:
        """Nested class for metric field validation."""

        @field_validator("value")
        @classmethod
        def validate_metric_value(cls, v: float) -> float:
            """Validate metric value is numeric and non-negative."""
            # Convert to float for consistency
            numeric_value = float(v)
            if numeric_value < 0:
                msg = "Metric value cannot be negative"
                raise ValueError(msg)
            return numeric_value

        @field_validator("unit")
        @classmethod
        def validate_metric_unit(cls, v: str) -> str:
            """Validate metric unit is from allowed set."""
            if v not in FlextObservabilityFields.METRIC_VALID_UNITS:
                msg = f"Invalid metric unit: {v}. Must be one of {FlextObservabilityFields.METRIC_VALID_UNITS}"
                raise ValueError(msg)
            return v

    # Convenience field definitions as class methods

    @classmethod
    def create_metric_name_field(cls) -> object:
        """Create metric name field."""
        return Field(min_length=1, max_length=255, description="Metric name")

    @classmethod
    def create_metric_value_field(cls) -> object:
        """Create metric value field."""
        return Field(ge=0.0, description="Metric value (non-negative)")

    @classmethod
    def create_metric_unit_field(cls) -> object:
        """Create metric unit field."""
        return Field(
            default=FlextObservabilityConstants.Observability.Defaults.DEFAULT_METRIC_UNIT,
            description="Metric unit",
        )

    @classmethod
    def create_trace_name_field(cls) -> object:
        """Create trace name field."""
        return Field(min_length=1, max_length=255, description="Trace operation name")

    @classmethod
    def create_alert_message_field(cls) -> object:
        """Create alert message field."""
        return Field(min_length=1, max_length=1000, description="Alert message")

    @classmethod
    def create_timestamp_field(cls) -> object:
        """Create timestamp field."""
        return Field(default_factory=lambda: datetime.now(UTC), description="Timestamp")


# Removed unused backward compatibility classes and field instances
# All field functionality is now available through FlextObservabilityFields


__all__ = [
    "FlextObservabilityFields",
]
