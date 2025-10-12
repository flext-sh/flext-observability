"""FLEXT Observability Alerting Domain Models.

Provides focused alerting models following the namespace class pattern.
Contains alert entities, configurations, and factory methods for alerting operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Self

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


class FlextObservabilityAlerting(FlextCore.Models):
    """Focused alerting models for observability operations extending FlextCore.Models.

    Provides comprehensive alert entities, configurations, and operations
    for alert management, escalation, and notification within the FLEXT ecosystem.
    """

    # Alert Management Models
    class AlertEntry(FlextCore.Models.Value):
        """Comprehensive alert entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
        )

        alert_id: str = Field(description="Unique alert identifier")
        name: str = Field(description="Alert name")
        severity: str = Field(description="Alert severity level")
        message: str = Field(description="Alert message")
        source: str = Field(description="Alert source")
        created_at: datetime = Field(
            default_factory=datetime.now, description="Alert creation time"
        )
        resolved_at: datetime | None = Field(
            default=None, description="Alert resolution time"
        )
        status: str = Field(default="active", description="Alert status")
        metadata: FlextCore.Types.StringDict = Field(
            default_factory=dict, description="Alert metadata"
        )

        @computed_field
        @property
        def alert_key(self) -> str:
            """Computed field for unique alert key."""
            return f"{self.source}.{self.name}.{self.severity}"

        @computed_field
        @property
        def is_resolved(self) -> bool:
            """Computed field indicating if alert is resolved."""
            return self.resolved_at is not None

        @computed_field
        @property
        def duration_minutes(self) -> float | None:
            """Computed field for alert duration in minutes."""
            if self.resolved_at is None:
                return None
            delta = self.resolved_at - self.created_at
            return delta.total_seconds() / 60

        @field_validator("severity")
        @classmethod
        def validate_severity(cls, v: str) -> str:
            """Validate severity is one of the valid levels."""
            valid_severities = ["critical", "warning", "info", "low"]
            if v.lower() not in valid_severities:
                msg = f"Severity must be one of: {valid_severities}"
                raise ValueError(msg)
            return v.lower()

        @field_serializer("metadata", when_used="json")
        def serialize_metadata_with_alert_context(
            self, value: FlextCore.Types.StringDict, _info: object
        ) -> FlextCore.Types.Dict:
            """Serialize metadata with alert context."""
            return {
                "metadata": value,
                "alert_context": {
                    "severity": self.severity,
                    "source": self.source,
                    "status": self.status,
                    "is_resolved": self.is_resolved,
                },
            }

    class AlertConfig(BaseModel):
        """Alert configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
        )

        escalation_delay: int = Field(
            default=300,  # 5 minutes
            description="Escalation delay in seconds",
        )
        max_escalation_level: int = Field(
            default=3,
            description="Maximum escalation level",
        )
        enable_notifications: bool = Field(
            default=True, description="Enable alert notifications"
        )
        notification_channels: FlextCore.Types.StringList = Field(
            default_factory=list, description="Notification channels"
        )

        @computed_field
        @property
        def escalation_delay_minutes(self) -> float:
            """Computed field for escalation delay in minutes."""
            return self.escalation_delay / 60

        @model_validator(mode="after")
        def validate_alert_config(self) -> Self:
            """Validate alert configuration parameters."""
            if self.escalation_delay <= 0:
                msg = "Escalation delay must be positive"
                raise ValueError(msg)
            if self.max_escalation_level <= 0:
                msg = "Max escalation level must be positive"
                raise ValueError(msg)
            return self

    class FlextAlert(FlextCore.Models.Entity):
        """Alert Management Entity for FLEXT Ecosystem Monitoring.

        Enterprise-grade alert entity implementing comprehensive alerting semantics
        with severity classification, lifecycle management, and rich contextual
        information.
        """

        title: str = Field(..., description="Alert title")
        message: str = Field(..., description="Alert message")
        severity: str = Field(default="low", description="Alert severity")
        status: str = Field(default="active", description="Alert status")
        tags: FlextCore.Types.Dict = Field(
            default_factory=dict, description="Alert tags"
        )
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

        @field_validator("title")
        @classmethod
        def validate_alert_title(cls, v: str) -> str:
            """Validate alert title is non-empty and descriptive."""
            if not (v and str(v).strip()):
                msg = "Alert title cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("message")
        @classmethod
        def validate_alert_message(cls, v: str) -> str:
            """Validate alert message provides sufficient detail."""
            if not (v and str(v).strip()):
                msg = "Alert message cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("severity")
        @classmethod
        def validate_alert_severity(cls, v: str) -> str:
            """Validate alert severity is a valid classification level."""
            valid_severities = {"low", "medium", "high", "critical", "emergency"}
            if v not in valid_severities:
                msg = f"Invalid alert severity: {v}. Must be one of {valid_severities}"
                raise ValueError(msg)
            return v

        @field_validator("status")
        @classmethod
        def validate_alert_status(cls, v: str) -> str:
            """Validate alert status is a valid state."""
            valid_statuses = {"active", "acknowledged", "resolved", "suppressed"}
            if v not in valid_statuses:
                msg = f"Invalid alert status: {v}. Must be one of {valid_statuses}"
                raise ValueError(msg)
            return v

        def validate_business_rules(self) -> FlextCore.Result[bool]:
            """Validate alert management business rules."""
            try:
                if not self.title:
                    return FlextCore.Result[bool].fail("Alert title is required")
                if not self.message:
                    return FlextCore.Result[bool].fail("Alert message is required")
                if self.severity not in {
                    "low",
                    "medium",
                    "high",
                    "critical",
                    "emergency",
                }:
                    return FlextCore.Result[bool].fail(
                        f"Invalid alert severity: {self.severity}"
                    )
                if self.status not in {
                    "active",
                    "acknowledged",
                    "resolved",
                    "suppressed",
                }:
                    return FlextCore.Result[bool].fail(
                        f"Invalid alert status: {self.status}"
                    )
                return FlextCore.Result[bool].ok(True)
            except Exception as e:
                return FlextCore.Result[bool].fail(
                    f"Business rule validation failed: {e}"
                )

    # Factory methods for direct entity creation
    @staticmethod
    def flext_alert(
        title: str,
        message: str,
        severity: str = "info",
        **kwargs: object,
    ) -> FlextCore.Result[FlextObservabilityAlerting.FlextAlert]:
        """Create a FlextAlert entity directly."""
        try:
            # Filter kwargs to only include valid FlextAlert parameters
            valid_kwargs: FlextCore.Types.Dict = {}
            if "status" in kwargs and isinstance(kwargs["status"], str):
                valid_kwargs["status"] = kwargs["status"]
            if "tags" in kwargs and isinstance(kwargs["tags"], dict):
                valid_kwargs["tags"] = kwargs["tags"]
            if "timestamp" in kwargs and isinstance(kwargs["timestamp"], datetime):
                valid_kwargs["timestamp"] = kwargs["timestamp"]

            return FlextCore.Result[FlextObservabilityAlerting.FlextAlert].ok(
                FlextObservabilityAlerting.FlextAlert(
                    title=title,
                    message=message,
                    severity=severity,
                )
            )
        except Exception as e:
            return FlextCore.Result[FlextObservabilityAlerting.FlextAlert].fail(
                f"Failed to create alert: {e}"
            )


# Export the focused alerting namespace class
__all__ = [
    "FlextObservabilityAlerting",
]
