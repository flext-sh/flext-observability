"""FLEXT Observability Alerting Domain Models.

Consolidated alerting models in single class with nested structure.
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


class FlextObservabilityAlerting(FlextCore.Models):
    """Consolidated alerting domain models in single class.

    Contains all alerting-related models and configurations as nested classes.
    Follows SOLID principles with no external dependencies or compatibility layers.
    """

    class AlertEntry(FlextCore.Models.Value):
        """Alert entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=False,  # Show input for better error messages
            str_strip_whitespace=True,  # Strip whitespace from strings
            str_to_lower=False,  # Keep original case for strings
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
            valid_severities = ["info", "warning", "error", "critical"]
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
                "alert_context": f"{self.source}.{self.name}",
                "severity": self.severity,
            }

    class AlertConfig(BaseModel):
        """Alert configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
            str_strip_whitespace=True,
            str_to_lower=False,
        )

        escalation_timeout_minutes: int = Field(
            default=30,
            description="Alert escalation timeout in minutes",
        )
        max_message_length: int = Field(
            default=1000,
            description="Maximum alert message length",
        )
        enable_auto_escalation: bool = Field(
            default=True, description="Enable automatic alert escalation"
        )
        notification_channels: list[str] = Field(
            default_factory=lambda: ["email"],
            description="Notification channels for alerts",
        )

        @model_validator(mode="after")
        def validate_alert_config(self) -> Self:
            """Validate alert configuration consistency."""
            if self.escalation_timeout_minutes <= 0:
                msg = "Escalation timeout must be positive"
                raise ValueError(msg)
            if self.max_message_length <= 0:
                msg = "Max message length must be positive"
                raise ValueError(msg)
            if not self.notification_channels:
                msg = "At least one notification channel required"
                raise ValueError(msg)
            return self


__all__ = [
    "FlextObservabilityAlerting",
]
