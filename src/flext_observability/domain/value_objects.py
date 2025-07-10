"""Value objects for observability domain - immutable business values.

REFACTORED: Uses flext-core v0.7.0 types - NO duplication.
All enumerations imported from flext-core.
"""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import Field
from pydantic import field_validator

from flext_core.domain.pydantic_base import DomainValueObject


class HealthStatus(StrEnum):
    """Health status enumeration for components - specific to observability."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    FAILED = "failed"
    TIMEOUT = "timeout"


# LogLevel is now imported from flext-core to eliminate duplication


class MetricValue(DomainValueObject):
    """Value object for metric values with validation."""

    value: Decimal = Field(description="The metric value")
    unit: str = Field(description="Unit of measurement")

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: Any) -> Decimal:
        """Validate metric value is finite and not NaN."""
        if isinstance(v, int | float):
            v = Decimal(str(v))
        if not isinstance(v, Decimal):
            raise ValueError(f"Value must be numeric, got {type(v)}")
        if not v.is_finite():
            raise ValueError("Value must be finite")
        return v


class ThresholdValue(DomainValueObject):
    """Value object for alert thresholds."""

    value: Decimal = Field(description="Threshold value")
    operator: str = Field(description="Comparison operator (gt, lt, eq, ge, le)")

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: str) -> str:
        """Validate threshold operator."""
        valid_operators = {"gt", "lt", "eq", "ge", "le"}
        if v not in valid_operators:
            raise ValueError(f"Invalid operator {v}, must be one of {valid_operators}")
        return v

    def compare(self, value: MetricValue) -> bool:
        """Compare metric value against threshold."""
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
        """Validate component name format."""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError(
                "Component name must be alphanumeric with hyphens or underscores",
            )
        return v

    @property
    def full_name(self) -> str:
        """Get fully qualified component name."""
        return f"{self.namespace}.{self.name}"


class TraceId(DomainValueObject):
    """Value object for trace identifiers."""

    trace_id: str = Field(min_length=16, max_length=64, description="Trace identifier")
    span_id: str = Field(min_length=8, max_length=32, description="Span identifier")

    @field_validator("trace_id", "span_id")
    @classmethod
    def validate_hex_string(cls, v: str) -> str:
        """Validate hex string format."""
        try:
            int(v, 16)
        except ValueError as e:
            raise ValueError(f"Invalid hex string: {v}") from e
        return v


class Duration(DomainValueObject):
    """Value object for durations."""

    milliseconds: int = Field(ge=0, description="Duration in milliseconds")

    @property
    def seconds(self) -> float:
        """Get duration in seconds."""
        return self.milliseconds / 1000.0

    @property
    def microseconds(self) -> int:
        """Get duration in microseconds."""
        return self.milliseconds * 1000

    @classmethod
    def from_seconds(cls, seconds: float) -> Duration:
        """Create duration from seconds."""
        return cls(milliseconds=int(seconds * 1000))
