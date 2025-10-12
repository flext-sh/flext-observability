"""FLEXT Observability Models.

Consolidated Pydantic v2 models following FLEXT principles and SOLID design.
All observability domain models organized in a single unified class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
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


class FlextObservabilityModels(FlextCore.Models):
    """Consolidated observability domain models extending FlextCore.Models.

    Single unified class containing all Pydantic v2 models for the observability domain,
    organized in nested classes following SOLID principles and FLEXT patterns.
    """

    # ============================================================================
    # METRICS DOMAIN - Metric collection and management
    # ============================================================================

    class Metrics(FlextCore.Models):
        """Metrics domain models for observability operations."""

        class MetricEntry(FlextCore.Models.Value):
            """Comprehensive metric entry model."""

            model_config = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                str_strip_whitespace=True,
                str_to_lower=False,
            )

            metric_id: str = Field(description="Unique metric identifier")
            name: str = Field(description="Metric name")
            value: float = Field(description="Metric value")
            unit: str = Field(default="count", description="Metric unit")
            timestamp: datetime = Field(
                default_factory=datetime.now, description="Metric timestamp"
            )
            labels: FlextCore.Types.StringDict = Field(
                default_factory=dict, description="Metric labels"
            )
            source: str = Field(description="Metric source service")

            @field_validator("name")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate metric name is not empty."""
                if not v or not v.strip():
                    msg = "Metric name cannot be empty"
                    raise ValueError(msg)
                return v.strip()

            @field_serializer("labels", when_used="json")
            def serialize_labels_with_metadata(
                self, value: FlextCore.Types.StringDict, _info: object
            ) -> FlextCore.Types.Dict:
                """Serialize labels with metadata for monitoring."""
                return {
                    "labels": value,
                    "label_count": len(value),
                    "metric_context": self.source,
                }

        class MetricConfig(BaseModel):
            """Metric configuration model."""

            model_config = ConfigDict(
                validate_assignment=True,
                extra="forbid",
                frozen=False,
                str_strip_whitespace=True,
                str_to_lower=False,
            )

            collection_interval: float = Field(
                default=60.0,  # 1 minute default
                description="Collection interval in seconds",
            )
            retention_days: int = Field(
                default=30,
                description="Metric retention in days",
            )
            aggregation_method: str = Field(
                default="sum", description="Aggregation method"
            )
            enable_alerting: bool = Field(
                default=True, description="Enable alerting for metrics"
            )

            @model_validator(mode="after")
            def validate_metric_config(self) -> Self:
                """Validate metric configuration consistency."""
                if self.collection_interval <= 0:
                    msg = "Collection interval must be positive"
                    raise ValueError(msg)
                if self.retention_days <= 0:
                    msg = "Retention days must be positive"
                    raise ValueError(msg)
                return self

    # ============================================================================
    # TRACING DOMAIN - Distributed tracing and span management
    # ============================================================================

    class Tracing(FlextCore.Models):
        """Tracing domain models for observability operations."""

        class TraceEntry(FlextCore.Models.Value):
            """Comprehensive trace entry model."""

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
            end_time: datetime | None = Field(
                default=None, description="Trace end time"
            )
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

    # ============================================================================
    # ALERTING DOMAIN - Alert management and escalation
    # ============================================================================

    class Alerting(FlextCore.Models):
        """Alerting domain models for observability operations."""

        class AlertEntry(FlextCore.Models.Value):
            """Comprehensive alert entry model."""

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
                return delta.total_seconds() / 60.0

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

    # ============================================================================
    # HEALTH DOMAIN - Health monitoring and status tracking
    # ============================================================================

    class Health(FlextCore.Models):
        """Health domain models for observability operations."""

        class HealthCheckEntry(FlextCore.Models.Value):
            """Comprehensive health check entry model."""

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
                default_factory=datetime.now, description="Check timestamp"
            )
            response_time_ms: float | None = Field(
                default=None, description="Response time in milliseconds"
            )
            details: FlextCore.Types.Dict = Field(
                default_factory=dict, description="Health check details"
            )

            @computed_field
            @property
            def health_key(self) -> str:
                """Computed field for unique health check key."""
                return f"{self.component}.{self.name}"

            @computed_field
            @property
            def is_healthy(self) -> bool:
                """Computed field indicating if component is healthy."""
                return self.status.lower() == "healthy"

            @computed_field
            @property
            def formatted_response_time(self) -> str:
                """Computed field for formatted response time."""
                if self.response_time_ms is None:
                    return "unknown"
                return f"{self.response_time_ms:.2f}ms"

            @field_validator("status")
            @classmethod
            def validate_status(cls, v: str) -> str:
                """Validate status is one of the valid health statuses."""
                valid_statuses = ["healthy", "degraded", "unhealthy"]
                if v.lower() not in valid_statuses:
                    msg = f"Status must be one of: {valid_statuses}"
                    raise ValueError(msg)
                return v.lower()

            @field_serializer("details", when_used="json")
            def serialize_details_with_health_context(
                self, value: FlextCore.Types.Dict, _info: object
            ) -> FlextCore.Types.Dict:
                """Serialize details with health context."""
                return {
                    "details": value,
                    "health_context": f"{self.component}.{self.name}",
                    "status": self.status,
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

            check_interval_seconds: int = Field(
                default=30,
                description="Health check interval in seconds",
            )
            failure_threshold: int = Field(
                default=3,
                description="Consecutive failures before marking unhealthy",
            )
            timeout_seconds: float = Field(
                default=10.0,
                description="Health check timeout in seconds",
            )
            enable_detailed_logging: bool = Field(
                default=True, description="Enable detailed health check logging"
            )

            @model_validator(mode="after")
            def validate_health_config(self) -> Self:
                """Validate health configuration consistency."""
                if self.check_interval_seconds <= 0:
                    msg = "Check interval must be positive"
                    raise ValueError(msg)
                if self.failure_threshold <= 0:
                    msg = "Failure threshold must be positive"
                    raise ValueError(msg)
                if self.timeout_seconds <= 0:
                    msg = "Timeout must be positive"
                    raise ValueError(msg)
                return self

    # ============================================================================
    # LOGGING DOMAIN - Structured logging and log management
    # ============================================================================

    class Logging(FlextCore.Models):
        """Logging domain models for observability operations."""

        class LogEntry(FlextCore.Models.Value):
            """Comprehensive log entry model."""

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
            level: str = Field(description="Log level")
            message: str = Field(description="Log message")
            logger_name: str = Field(description="Logger name")
            timestamp: datetime = Field(
                default_factory=datetime.now, description="Log timestamp"
            )
            source: str = Field(description="Log source")
            context: FlextCore.Types.Dict = Field(
                default_factory=dict, description="Log context"
            )

            @computed_field
            @property
            def log_key(self) -> str:
                """Computed field for unique log key."""
                return f"{self.source}.{self.logger_name}.{self.level}"

            @computed_field
            @property
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
            def serialize_context_with_log_info(
                self, value: FlextCore.Types.Dict, _info: object
            ) -> FlextCore.Types.Dict:
                """Serialize context with log information."""
                return {
                    "context": value,
                    "log_info": {
                        "level": self.level,
                        "logger": self.logger_name,
                        "source": self.source,
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

            level: str = Field(default="INFO", description="Log level")
            format: str = Field(
                default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                description="Log format string",
            )
            max_file_size_mb: int = Field(
                default=10,
                description="Maximum log file size in MB",
            )
            retention_days: int = Field(
                default=30,
                description="Log retention in days",
            )
            enable_json_format: bool = Field(
                default=False, description="Enable JSON log formatting"
            )

            @model_validator(mode="after")
            def validate_log_config(self) -> Self:
                """Validate log configuration consistency."""
                valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                if self.level.upper() not in valid_levels:
                    msg = f"Log level must be one of: {valid_levels}"
                    raise ValueError(msg)
                if self.max_file_size_mb <= 0:
                    msg = "Max file size must be positive"
                    raise ValueError(msg)
                if self.retention_days <= 0:
                    msg = "Retention days must be positive"
                    raise ValueError(msg)
                return self


__all__ = [
    "FlextObservabilityModels",
]
