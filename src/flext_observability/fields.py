"""FLEXT Module.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar, cast

from pydantic import Field, field_validator

from flext_observability.constants import ObservabilityConstants

if TYPE_CHECKING:
    from pydantic.fields import FieldInfo


class MetricValueField:
    """Field for metric values with validation."""

    @field_validator("value")
    @classmethod
    def validate_metric_value(cls, v: float) -> float:
        """Validate metric value is numeric."""
        # Convert to float for consistency
        numeric_value = float(v)
        if numeric_value < 0:
            msg = "Metric value cannot be negative"
            raise ValueError(msg)
        return numeric_value


class MetricUnitField:
    """Field for metric units with validation."""

    valid_units: ClassVar[set[str]] = {
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

    @field_validator("unit")
    @classmethod
    def validate_metric_unit(cls, v: str) -> str:
        """Validate metric unit is from allowed set."""
        if v not in cls.valid_units:
            msg = f"Invalid metric unit: {v}. Must be one of {cls.valid_units}"
            raise ValueError(msg)
        return v


class AlertLevelField:
    """Field for alert levels with validation."""

    @field_validator("level")
    @classmethod
    def validate_alert_level(cls, v: str) -> str:
        """Validate alert level is valid."""
        valid_levels = {
            ObservabilityConstants.ALERT_LEVEL_INFO,
            ObservabilityConstants.ALERT_LEVEL_WARNING,
            ObservabilityConstants.ALERT_LEVEL_ERROR,
            ObservabilityConstants.ALERT_LEVEL_CRITICAL,
        }
        if v not in valid_levels:
            msg = f"Invalid alert level: {v}. Must be one of {valid_levels}"
            raise ValueError(msg)
        return v


class TraceStatusField:
    """Field for trace status with validation."""

    @field_validator("status")
    @classmethod
    def validate_trace_status(cls, v: str) -> str:
        """Validate trace status is valid."""
        valid_statuses = {
            ObservabilityConstants.TRACE_STATUS_STARTED,
            ObservabilityConstants.TRACE_STATUS_RUNNING,
            ObservabilityConstants.TRACE_STATUS_COMPLETED,
            ObservabilityConstants.TRACE_STATUS_FAILED,
        }
        if v not in valid_statuses:
            msg = f"Invalid trace status: {v}. Must be one of {valid_statuses}"
            raise ValueError(msg)
        return v


class HealthStatusField:
    """Field for health status with validation."""

    @field_validator("status")
    @classmethod
    def validate_health_status(cls, v: str) -> str:
        """Validate health status is valid."""
        valid_statuses = {
            ObservabilityConstants.HEALTH_STATUS_HEALTHY,
            ObservabilityConstants.HEALTH_STATUS_DEGRADED,
            ObservabilityConstants.HEALTH_STATUS_UNHEALTHY,
        }
        if v not in valid_statuses:
            msg = f"Invalid health status: {v}. Must be one of {valid_statuses}"
            raise ValueError(msg)
        return v


# Convenience field definitions


def _create_metric_name_field() -> FieldInfo:
    """Create metric name field."""
    return cast(
        "FieldInfo",
        Field(min_length=1, max_length=255, description="Metric name"),
    )


def _create_metric_value_field() -> FieldInfo:
    """Create metric value field."""
    return cast("FieldInfo", Field(ge=0.0, description="Metric value (non-negative)"))


def _create_metric_unit_field() -> FieldInfo:
    """Create metric unit field."""
    return cast(
        "FieldInfo",
        Field(
            default=ObservabilityConstants.DEFAULT_METRIC_UNIT,
            description="Metric unit",
        ),
    )


def _create_trace_name_field() -> FieldInfo:
    """Create trace name field."""
    return cast(
        "FieldInfo",
        Field(min_length=1, max_length=255, description="Trace operation name"),
    )


def _create_alert_message_field() -> FieldInfo:
    """Create alert message field."""
    return cast(
        "FieldInfo",
        Field(min_length=1, max_length=1000, description="Alert message"),
    )


def _create_timestamp_field() -> FieldInfo:
    """Create timestamp field."""
    return cast(
        "FieldInfo",
        Field(default_factory=lambda: datetime.now(UTC), description="Timestamp"),
    )


metric_name_field = _create_metric_name_field()
metric_value_field = _create_metric_value_field()
metric_unit_field = _create_metric_unit_field()
trace_name_field = _create_trace_name_field()
alert_message_field = _create_alert_message_field()
timestamp_field = _create_timestamp_field()


__all__ = [
    "AlertLevelField",
    "HealthStatusField",
    "MetricUnitField",
    "MetricValueField",
    "TraceStatusField",
    "alert_message_field",
    "metric_name_field",
    "metric_unit_field",
    "metric_value_field",
    "timestamp_field",
    "trace_name_field",
]
