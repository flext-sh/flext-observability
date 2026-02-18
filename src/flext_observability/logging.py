"""FLEXT Observability Logging Domain Models.

Provides focused logging models following the namespace class pattern.
Contains log entities, configurations, and factory methods for logging operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal, Self

from flext_core import FlextModels, FlextResult, FlextTypes as t, m
from flext_core.models import m
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from flext_observability.models import m


class FlextObservabilityLogging(FlextModels):
    """Focused logging models for observability operations extending FlextModels.

    Provides complete logging entities, configurations, and operations
    for structured logging, log management, and log analysis within the FLEXT ecosystem.
    """

    # Log Management Models
    class LogEntry(m.Value):
        """Complete log entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=False,  # Show input for better error messages
            str_strip_whitespace=True,  # Strip whitespace from strings
            str_to_lower=False,  # Keep original case for strings
        )

        log_id: str = Field(description="Unique log identifier")
        level: Literal["debug", "info", "warning", "error", "critical"] = Field(
            default="info",
            description="Log level",
        )
        message: str = Field(description="Log message")
        logger_name: str = Field(description="Logger name")
        timestamp: datetime = Field(
            default_factory=datetime.now,
            description="Log timestamp",
        )
        source: str = Field(description="Log source")
        context: dict[str, t.GeneralValueType] = Field(
            default_factory=dict,
            description="Log context",
        )

        @computed_field
        def log_key(self) -> str:
            """Computed field for unique log key."""
            return f"{self.source}.{self.logger_name}.{self.level}"

        @computed_field
        def is_error_level(self) -> bool:
            """Computed field indicating if log is error level or higher."""
            error_levels = ["error", "critical"]
            return self.level.lower() in error_levels

        @field_validator("level")
        @classmethod
        def validate_level(cls, v: str) -> str:
            """Validate log level is one of the valid levels."""
            valid_levels = ["debug", "info", "warning", "error", "critical"]
            if v.lower() not in valid_levels:
                msg = f"Log level must be one of: {valid_levels}"
                raise ValueError(msg)
            return v.lower()

        @field_serializer("context", when_used="json")
        def serialize_context_with_log_metadata(
            self,
            value: dict[str, t.GeneralValueType],
            _info: object,
        ) -> dict[str, dict[str, t.GeneralValueType] | dict[str, str | bool]]:
            """Serialize context with log metadata."""
            return {
                "context": value,
                "log_metadata": {
                    "level": self.level,
                    "source": self.source,
                    "logger": self.logger_name,
                    "is_error": self.is_error_level,
                },
            }

    class LogConfig(BaseModel):
        """Log configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
            str_strip_whitespace=True,
            str_to_lower=False,
        )

        retention_days: int = Field(
            default=7,  # 7 days
            description="Log retention in days",
        )
        max_log_size_mb: int = Field(
            default=100,  # 100 MB
            description="Maximum log size in MB",
        )
        enable_structured_logging: bool = Field(
            default=True,
            description="Enable structured logging",
        )
        log_format: str = Field(default="json", description="Log format")

        @computed_field
        def max_log_size_bytes(self) -> int:
            """Computed field for max log size in bytes."""
            return self.max_log_size_mb * 1024 * 1024

        @model_validator(mode="after")
        def validate_log_config(self) -> Self:
            """Validate log configuration parameters."""
            if self.retention_days <= 0:
                msg = "Retention days must be positive"
                raise ValueError(msg)
            if self.max_log_size_mb <= 0:
                msg = "Max log size must be positive"
                raise ValueError(msg)
            return self

    class FlextLogEntry(FlextModels.Entity):
        """Structured Logging Entity for FLEXT Ecosystem.

        structured logging entity implementing complete logging
        semantics with severity classification, rich contextual information, and
        correlation ID support.
        """

        message: str = Field(..., min_length=1, description="Log message")
        level: Literal["debug", "info", "warning", "error", "critical"] = Field(
            default="info",
            description="Log level",
        )
        context: dict[str, t.GeneralValueType] = Field(
            default_factory=dict,
            description="Log context",
        )
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

        def validate_business_rules(self) -> FlextResult[bool]:
            """Validate structured logging business rules."""
            try:
                if not (self.message and str(self.message).strip()):
                    return FlextResult[bool].fail("Invalid log message")
                if self.level not in {"debug", "info", "warning", "error", "critical"}:
                    return FlextResult[bool].fail(f"Invalid log level: {self.level}")
                return FlextResult[bool].ok(value=True)
            except Exception as e:
                return FlextResult[bool].fail(f"Business rule validation failed: {e}")


# Export the focused logging namespace class
__all__ = [
    "FlextObservabilityLogging",
]
