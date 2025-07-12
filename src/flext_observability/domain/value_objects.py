"""Value objects for observability domain - immutable business values.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import field_validator

from flext_core.domain.pydantic_base import DomainValueObject
from flext_core.domain.pydantic_base import Field


class HealthStatus(StrEnum):
    """Health status enumeration for components - specific to observability."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    FAILED = "failed"
    TIMEOUT = "timeout"


class AlertSeverity(StrEnum):
    """Alert severity levels for observability components."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# LogLevel is now imported from flext-core to eliminate duplication


class MetricValue(DomainValueObject):
    """Value object for metric values with validation."""

    value: Decimal = Field(description="The metric value")
    unit: str = Field(description="Unit of measurement")

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: Any) -> Decimal:
        """Validate metric value is numeric and finite.

        Args:
            v: Value to validate.

        Returns:
            Validated Decimal value.

        Raises:
            ValueError: If value is not numeric or not finite.

        """
        if isinstance(v, int | float):
            v = Decimal(str(v))
        if not isinstance(v, Decimal):
            msg = f"Value must be numeric, got {type(v)}"
            raise ValueError(msg)
        if not v.is_finite():
            msg = "Value must be finite"
            raise ValueError(msg)
        return v


class ThresholdValue(DomainValueObject):
    """Value object for alert thresholds."""

    value: Decimal = Field(description="Threshold value")
    operator: str = Field(description="Comparison operator (gt, lt, eq, ge, le)")

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: str) -> str:
        """Validate threshold comparison operator.

        Args:
            v: Operator string to validate.

        Returns:
            Validated operator string.

        Raises:
            ValueError: If operator is not supported.

        """
        valid_operators = {"gt", "lt", "eq", "ge", "le"}
        if v not in valid_operators:
            msg = f"Invalid operator {v}, must be one of {valid_operators}"
            raise ValueError(msg)
        return v

    def compare(self, value: MetricValue) -> bool:
        """Compare metric value against threshold.

        Args:
            value: Metric value to compare.

        Returns:
            True if metric value meets threshold condition.

        """
        ops = {
            "gt": value.value > self.value,
            "lt": value.value < self.value,
            "eq": value.value == self.value,
            "ge": value.value >= self.value,
            "le": value.value <= self.value,
        }
        return ops[self.operator]


class ComponentName(DomainValueObject):
    """Value object for component names."""

    name: str = Field(min_length=1, max_length=100, description="Component name")
    namespace: str = Field(default="default", description="Component namespace")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate component name format.

        Args:
            v: Component name to validate.

        Returns:
            Validated component name.

        Raises:
            ValueError: If name contains invalid characters.

        """
        if not v.replace("-", "").replace("_", "").isalnum():
            msg = "Component name must be alphanumeric with hyphens or underscores"
            raise ValueError(
                msg,
            )
        return v

    @property
    def full_name(self) -> str:
        """Get fully qualified component name.

        Returns:
            Namespace-prefixed component name.

        """
        return f"{self.namespace}.{self.name}"


class TraceId(DomainValueObject):
    """Value object for trace identifiers."""

    trace_id: str = Field(min_length=16, max_length=64, description="Trace identifier")
    span_id: str = Field(min_length=8, max_length=32, description="Span identifier")

    @field_validator("trace_id", "span_id")
    @classmethod
    def validate_hex_string(cls, v: str) -> str:
        """Validate trace and span IDs are valid hex strings.

        Args:
            v: Hex string to validate.

        Returns:
            Validated hex string.

        Raises:
            ValueError: If string is not valid hexadecimal.

        """
        try:
            int(v, 16)
        except ValueError as e:
            msg = f"Invalid hex string: {v}"
            raise ValueError(msg) from e
        return v


class Duration(DomainValueObject):
    """Value object for durations."""

    milliseconds: int = Field(ge=0, description="Duration in milliseconds")

    @property
    def seconds(self) -> float:
        """Get duration in seconds.

        Returns:
            Duration converted to seconds as float.

        """
        return self.milliseconds / 1000.0

    @property
    def microseconds(self) -> int:
        """Get duration in microseconds.

        Returns:
            Duration converted to microseconds as integer.

        """
        return self.milliseconds * 1000

    @classmethod
    def from_seconds(cls, seconds: float) -> Duration:
        """Create Duration from seconds value.

        Args:
            seconds: Duration in seconds.

        Returns:
            Duration instance with converted milliseconds.

        """
        return cls(milliseconds=int(seconds * 1000))
