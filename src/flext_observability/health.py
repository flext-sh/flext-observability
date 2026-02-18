"""FLEXT Observability Health Domain Models.

Provides focused health monitoring models following the namespace class pattern.
Contains health check entities, configurations, and factory methods for health operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from flext_core import m
from flext_observability.models import m
from flext_core.models import m
from __future__ import annotations

from datetime import UTC, datetime
from typing import Self

from flext_core import FlextModels, FlextResult, FlextTypes as t
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)


class FlextObservabilityHealth(FlextModels):
    """Focused health monitoring models for observability operations extending FlextModels.

    Provides complete health check entities, configurations, and operations
    for service health monitoring, status tracking, and health validation within the FLEXT ecosystem.
    """

    # Health Monitoring Models
    class HealthCheckEntry(m.Value):
        """Complete health check entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=False,  # Show input for better error messages
            str_strip_whitespace=True,  # Strip whitespace from strings
            str_to_lower=False,  # Keep original case for strings
        )

        check_id: str = Field(description="Unique health check identifier")
        name: str = Field(description="Health check name")
        status: str = Field(description="Health check status")
        component: str = Field(description="Component being checked")
        timestamp: datetime = Field(
            default_factory=datetime.now,
            description="Check timestamp",
        )
        response_time_ms: float | None = Field(
            default=None,
            description="Response time in milliseconds",
        )
        details: dict[str, t.GeneralValueType] = Field(
            default_factory=dict,
            description="Health check details",
        )

        @computed_field
        def health_key(self) -> str:
            """Computed field for unique health check key."""
            return f"{self.component}.{self.name}"

        @computed_field
        def is_healthy(self) -> bool:
            """Computed field indicating if component is healthy."""
            return self.status.lower() == "healthy"

        @computed_field
        def formatted_response_time(self) -> str:
            """Computed field for formatted response time."""
            if self.response_time_ms is None:
                return "unknown"
            return f"{self.response_time_ms:.2f}ms"

        @field_validator("status")
        @classmethod
        def validate_status(cls, v: str) -> str:
            """Validate health check status is one of the valid statuses."""
            valid_statuses = ["healthy", "degraded", "unhealthy", "unknown"]
            if v.lower() not in valid_statuses:
                msg = f"Status must be one of: {valid_statuses}"
                raise ValueError(msg)
            return v.lower()

        @field_serializer("details", when_used="json")
        def serialize_details_with_health_context(
            self,
            value: dict[str, t.GeneralValueType],
            _info: object,
        ) -> dict[str, dict[str, t.GeneralValueType] | dict[str, str | bool]]:
            """Serialize details with health check context."""
            return {
                "details": value,
                "health_context": {
                    "component": self.component,
                    "status": self.status,
                    "is_healthy": self.is_healthy,
                    "response_time": self.formatted_response_time,
                },
            }

    class HealthConfig(BaseModel):
        """Health monitoring configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
            str_strip_whitespace=True,
            str_to_lower=False,
        )

        check_interval: int = Field(
            default=30,  # 30 seconds
            description="Health check interval in seconds",
        )
        timeout: int = Field(
            default=10,  # 10 seconds
            description="Health check timeout in seconds",
        )
        failure_threshold: int = Field(
            default=3,
            description="Failure threshold for unhealthy status",
        )
        enable_auto_recovery: bool = Field(
            default=True,
            description="Enable automatic recovery",
        )

        @computed_field
        def check_interval_minutes(self) -> float:
            """Computed field for check interval in minutes."""
            return self.check_interval / 60

        @model_validator(mode="after")
        def validate_health_config(self) -> Self:
            """Validate health configuration parameters."""
            if self.check_interval <= 0:
                msg = "Check interval must be positive"
                raise ValueError(msg)
            if self.timeout <= 0:
                msg = "Timeout must be positive"
                raise ValueError(msg)
            if self.failure_threshold <= 0:
                msg = "Failure threshold must be positive"
                raise ValueError(msg)
            return self

    class FlextHealthCheck(FlextModels.Entity):
        """Health Monitoring Entity for FLEXT Ecosystem Components.

        health check entity implementing complete service health
        semantics with status classification, diagnostic metrics, and dependency validation.
        """

        component: str = Field(..., min_length=1, description="Component name")
        status: str = Field(
            default="unknown",
            pattern="^(healthy|degraded|unhealthy|unknown)$",
            description="Health status",
        )
        message: str = Field(default="", description="Health check message")
        metrics: dict[str, t.GeneralValueType] = Field(
            default_factory=dict,
            description="Health metrics",
        )
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

        def validate_business_rules(self) -> FlextResult[bool]:
            """Validate health monitoring business rules."""
            try:
                if not self.component:
                    return FlextResult[bool].fail("Component name is required")
                if self.status not in {"healthy", "degraded", "unhealthy", "unknown"}:
                    return FlextResult[bool].fail(
                        f"Invalid health status: {self.status}",
                    )
                return FlextResult[bool].ok(value=True)
            except Exception as e:
                return FlextResult[bool].fail(f"Business rule validation failed: {e}")

    # Factory methods for direct entity creation
    @staticmethod
    def flext_health_check(
        component: str,
        status: str = "unknown",
        message: str = "",
        **kwargs: object,
    ) -> FlextResult[FlextObservabilityHealth.FlextHealthCheck]:
        """Create a FlextHealthCheck entity directly."""
        try:
            # Filter kwargs to only include valid FlextHealthCheck parameters
            valid_kwargs: dict[str, t.GeneralValueType] = {}
            if "metrics" in kwargs and isinstance(kwargs["metrics"], dict):
                valid_kwargs["metrics"] = kwargs["metrics"]
            if "timestamp" in kwargs and isinstance(kwargs["timestamp"], datetime):
                valid_kwargs["timestamp"] = kwargs["timestamp"]

            return FlextResult[FlextObservabilityHealth.FlextHealthCheck].ok(
                FlextObservabilityHealth.FlextHealthCheck(
                    component=component,
                    status=status,
                    message=message,
                ),
            )
        except Exception as e:
            return FlextResult[FlextObservabilityHealth.FlextHealthCheck].fail(
                f"Failed to create health check: {e}",
            )


# Export the focused health namespace class
__all__ = [
    "FlextObservabilityHealth",
]
