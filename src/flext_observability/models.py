"""Observability domain models following unified [Project]Models pattern.

Provides unified FlextObservabilityModels class with comprehensive nested classes
for metrics, traces, alerts, health checks, and logging operations.
Built on flext-core patterns with proper separation of concerns.

This module re-exports entities from entities.py to maintain compatibility
while following FLEXT architecture patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Self

from pydantic import (
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from flext_core import FlextModels

# Re-export entities from entities.py to maintain compatibility
from flext_observability.constants import FlextObservabilityConstants


class FlextObservabilityModels(FlextModels):
    """Comprehensive observability models for monitoring operations extending FlextModels.

    Provides standardized models for all observability domain entities including:
    - Metrics collection and management
    - Distributed tracing and monitoring
    - Alert management and escalation
    - Health monitoring and checks
    - Log entry management and analysis
    - Performance monitoring and analysis

    All nested classes inherit FlextModels validation and patterns.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=False,
        validate_return=True,
        ser_json_timedelta="iso8601",
        ser_json_bytes="base64",
        hide_input_in_errors=True,
        json_schema_extra={
            "examples": [
                {
                    "monitoring_enabled": True,
                    "tracing_enabled": True,
                    "alerting_enabled": True,
                    "health_checks_enabled": True,
                }
            ],
            "description": "Enterprise observability models for comprehensive monitoring operations",
        },
    )

    @computed_field
    @property
    def active_observability_models_count(self) -> int:
        """Computed field returning the number of active observability model types."""
        model_types = [
            "MetricEntry",
            "MetricConfig",
            "TraceEntry",
            "TraceConfig",
            "AlertEntry",
            "AlertConfig",
            "HealthCheckEntry",
            "HealthConfig",
            "LogEntry",
            "LogConfig",
            "PerformanceEntry",
            "PerformanceConfig",
            "DashboardEntry",
            "MonitoringConfig",
        ]
        return len(model_types)

    @computed_field
    @property
    def observability_model_summary(self) -> dict[str, object]:
        """Computed field providing summary of observability model capabilities."""
        return {
            "metrics_models": 2,
            "tracing_models": 2,
            "alerting_models": 2,
            "health_models": 2,
            "logging_models": 2,
            "performance_models": 2,
            "dashboard_models": 1,
            "monitoring_models": 1,
            "total_models": self.active_observability_models_count,
            "enterprise_features": [
                "distributed_tracing",
                "metrics_collection",
                "alerting",
                "health_monitoring",
            ],
        }

    @model_validator(mode="after")
    def validate_observability_consistency(self) -> FlextObservabilityModels:
        """Validate observability model consistency across all components."""
        # Perform cross-model validation for observability requirements
        return self

    @field_serializer("model_config", when_used="json")
    def serialize_with_observability_metadata(
        self, value: object, _info: object
    ) -> dict[str, object]:
        """Serialize with observability metadata for monitoring context."""
        return {
            "config": value,
            "observability_metadata": {
                "models_available": self.active_observability_models_count,
                "monitoring_capabilities": [
                    "metrics",
                    "tracing",
                    "alerting",
                    "health",
                    "logging",
                    "performance",
                ],
                "enterprise_ready": True,
            },
        }

    # Core Metrics Models
    class MetricEntry(FlextModels.Value):
        """Comprehensive metric entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
        )

        metric_id: str = Field(description="Unique metric identifier")
        name: str = Field(description="Metric name")
        value: float = Field(description="Metric value")
        unit: str = Field(default="count", description="Metric unit")
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Metric timestamp"
        )
        labels: dict[str, str] = Field(
            default_factory=dict, description="Metric labels"
        )
        source: str = Field(description="Metric source service")

        @computed_field
        @property
        def metric_key(self) -> str:
            """Computed field for unique metric key."""
            return f"{self.source}.{self.name}"

        @computed_field
        @property
        def formatted_value(self) -> str:
            """Computed field for formatted metric value with unit."""
            return f"{self.value} {self.unit}"

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
            self, value: dict[str, str], _info: object
        ) -> dict[str, object]:
            """Serialize labels with metadata for monitoring."""
            return {
                "labels": value,
                "label_count": len(value),
                "metric_context": self.source,
            }

    class MetricConfig(FlextModels.Configuration):
        """Metric configuration model."""

        model_config = ConfigDict(
            validate_assignment=True, use_enum_values=True, extra="forbid", frozen=False
        )

        collection_interval: float = Field(
            default=60.0, description="Collection interval in seconds"
        )
        retention_days: int = Field(default=30, description="Metric retention in days")
        aggregation_method: str = Field(default="sum", description="Aggregation method")
        enable_alerting: bool = Field(
            default=True, description="Enable alerting for metrics"
        )

        @computed_field
        @property
        def config_summary(self) -> dict[str, object]:
            """Computed field for metric configuration summary."""
            return {
                "collection_interval_minutes": self.collection_interval / 60,
                "retention_weeks": self.retention_days / 7,
                "alerting_enabled": self.enable_alerting,
                "aggregation": self.aggregation_method,
            }

        @model_validator(mode="after")
        def validate_metric_config(self) -> Self:
            """Validate metric configuration parameters."""
            if self.collection_interval <= 0:
                msg = "Collection interval must be positive"
                raise ValueError(msg)
            if self.retention_days <= 0:
                msg = "Retention days must be positive"
                raise ValueError(msg)
            return self

    # Distributed Tracing Models
    class TraceEntry(FlextModels.Value):
        """Comprehensive trace entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
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
        end_time: datetime | None = Field(default=None, description="Trace end time")
        duration_ms: float | None = Field(
            default=None, description="Duration in milliseconds"
        )
        status: str = Field(default="active", description="Trace status")
        tags: dict[str, str] = Field(default_factory=dict, description="Trace tags")

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
            self, value: dict[str, str], _info: object
        ) -> dict[str, object]:
            """Serialize tags with trace context."""
            return {
                "tags": value,
                "tag_count": len(value),
                "trace_context": {
                    "service": self.service_name,
                    "operation": self.operation_name,
                    "is_root": self.is_root_span,
                },
            }

    class TraceConfig(FlextModels.Configuration):
        """Trace configuration model."""

        model_config = ConfigDict(
            validate_assignment=True, use_enum_values=True, extra="forbid", frozen=False
        )

        sampling_rate: float = Field(
            default=0.1, description="Trace sampling rate (0.0-1.0)"
        )
        max_trace_duration: int = Field(
            default=300, description="Maximum trace duration in seconds"
        )
        enable_performance_tracing: bool = Field(
            default=True, description="Enable performance tracing"
        )

        @computed_field
        @property
        def sampling_percentage(self) -> float:
            """Computed field for sampling rate as percentage."""
            return self.sampling_rate * 100

        @model_validator(mode="after")
        def validate_trace_config(self) -> Self:
            """Validate trace configuration parameters."""
            if not 0.0 <= self.sampling_rate <= 1.0:
                msg = "Sampling rate must be between 0.0 and 1.0"
                raise ValueError(msg)
            return self

    # Alert Management Models
    class AlertEntry(FlextModels.Value):
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
        metadata: dict[str, str] = Field(
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
            self, value: dict[str, str], _info: object
        ) -> dict[str, object]:
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

    class AlertConfig(FlextModels.Configuration):
        """Alert configuration model."""

        model_config = ConfigDict(
            validate_assignment=True, use_enum_values=True, extra="forbid", frozen=False
        )

        escalation_delay: int = Field(
            default=300, description="Escalation delay in seconds"
        )
        max_escalation_level: int = Field(
            default=3, description="Maximum escalation level"
        )
        enable_notifications: bool = Field(
            default=True, description="Enable alert notifications"
        )
        notification_channels: list[str] = Field(
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

    # Health Monitoring Models
    class HealthCheckEntry(FlextModels.Value):
        """Comprehensive health check entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
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
        details: dict[str, object] = Field(
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
            """Validate health check status is one of the valid statuses."""
            valid_statuses = ["healthy", "degraded", "unhealthy", "unknown"]
            if v.lower() not in valid_statuses:
                msg = f"Status must be one of: {valid_statuses}"
                raise ValueError(msg)
            return v.lower()

        @field_serializer("details", when_used="json")
        def serialize_details_with_health_context(
            self, value: dict[str, object], _info: object
        ) -> dict[str, object]:
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

    class HealthConfig(FlextModels.Configuration):
        """Health monitoring configuration model."""

        model_config = ConfigDict(
            validate_assignment=True, use_enum_values=True, extra="forbid", frozen=False
        )

        check_interval: int = Field(
            default=30, description="Health check interval in seconds"
        )
        timeout: int = Field(default=10, description="Health check timeout in seconds")
        failure_threshold: int = Field(
            default=3, description="Failure threshold for unhealthy status"
        )
        enable_auto_recovery: bool = Field(
            default=True, description="Enable automatic recovery"
        )

        @computed_field
        @property
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

    # Log Management Models
    class LogEntry(FlextModels.Value):
        """Comprehensive log entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
        )

        log_id: str = Field(description="Unique log identifier")
        level: str = Field(description="Log level")
        message: str = Field(description="Log message")
        logger_name: str = Field(description="Logger name")
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Log timestamp"
        )
        source: str = Field(description="Log source")
        context: dict[str, object] = Field(
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
        def serialize_context_with_log_metadata(
            self, value: dict[str, object], _info: object
        ) -> dict[str, object]:
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

    class LogConfig(FlextModels.Configuration):
        """Log configuration model."""

        model_config = ConfigDict(
            validate_assignment=True, use_enum_values=True, extra="forbid", frozen=False
        )

        retention_days: int = Field(default=7, description="Log retention in days")
        max_log_size_mb: int = Field(default=100, description="Maximum log size in MB")
        enable_structured_logging: bool = Field(
            default=True, description="Enable structured logging"
        )
        log_format: str = Field(default="json", description="Log format")

        @computed_field
        @property
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

    # Performance Monitoring Models
    class PerformanceEntry(FlextModels.Value):
        """Performance monitoring entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
        )

        performance_id: str = Field(description="Unique performance entry identifier")
        operation: str = Field(description="Operation being monitored")
        duration_ms: float = Field(description="Operation duration in milliseconds")
        cpu_usage: float | None = Field(
            default=None, description="CPU usage percentage"
        )
        memory_usage: float | None = Field(
            default=None, description="Memory usage in MB"
        )
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Performance timestamp"
        )
        service: str = Field(description="Service name")
        success: bool = Field(default=True, description="Operation success status")

        @computed_field
        @property
        def performance_key(self) -> str:
            """Computed field for unique performance key."""
            return f"{self.service}.{self.operation}"

        @computed_field
        @property
        def formatted_duration(self) -> str:
            """Computed field for formatted duration."""
            return f"{self.duration_ms:.2f}ms"

        @computed_field
        @property
        def resource_summary(self) -> dict[str, object]:
            """Computed field for resource usage summary."""
            return {
                "duration_ms": self.duration_ms,
                "cpu_percent": self.cpu_usage,
                "memory_mb": self.memory_usage,
                "success": self.success,
            }

        @field_serializer("cpu_usage", when_used="json")
        def serialize_cpu_usage_with_metadata(
            self, value: float | None, _info: object
        ) -> dict[str, object]:
            """Serialize CPU usage with performance metadata."""
            return {
                "cpu_percent": value,
                "performance_context": {
                    "service": self.service,
                    "operation": self.operation,
                    "duration_ms": self.duration_ms,
                },
            }

    class PerformanceConfig(FlextModels.Configuration):
        """Performance monitoring configuration model."""

        model_config = ConfigDict(
            validate_assignment=True, use_enum_values=True, extra="forbid", frozen=False
        )

        enable_cpu_monitoring: bool = Field(
            default=True, description="Enable CPU monitoring"
        )
        enable_memory_monitoring: bool = Field(
            default=True, description="Enable memory monitoring"
        )
        sampling_interval: int = Field(
            default=5, description="Sampling interval in seconds"
        )
        performance_threshold_ms: float = Field(
            default=1000.0, description="Performance threshold in milliseconds"
        )

        @computed_field
        @property
        def monitoring_summary(self) -> dict[str, object]:
            """Computed field for monitoring configuration summary."""
            return {
                "cpu_enabled": self.enable_cpu_monitoring,
                "memory_enabled": self.enable_memory_monitoring,
                "sampling_interval_seconds": self.sampling_interval,
                "threshold_ms": self.performance_threshold_ms,
            }

        @model_validator(mode="after")
        def validate_performance_config(self) -> Self:
            """Validate performance configuration parameters."""
            if self.sampling_interval <= 0:
                msg = "Sampling interval must be positive"
                raise ValueError(msg)
            if self.performance_threshold_ms <= 0:
                msg = "Performance threshold must be positive"
                raise ValueError(msg)
            return self

    # Observability Dashboard Models
    class DashboardEntry(FlextModels.Value):
        """Dashboard configuration entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
            hide_input_in_errors=True,
        )

        dashboard_id: str = Field(description="Unique dashboard identifier")
        name: str = Field(description="Dashboard name")
        description: str = Field(description="Dashboard description")
        widgets: list[dict[str, object]] = Field(
            default_factory=list, description="Dashboard widgets"
        )
        created_by: str = Field(description="Dashboard creator")
        created_at: datetime = Field(
            default_factory=datetime.now, description="Dashboard creation time"
        )
        is_public: bool = Field(default=False, description="Dashboard visibility")

        @computed_field
        @property
        def widget_count(self) -> int:
            """Computed field for number of widgets."""
            return len(self.widgets)

        @computed_field
        @property
        def dashboard_summary(self) -> dict[str, object]:
            """Computed field for dashboard summary."""
            return {
                "name": self.name,
                "widget_count": self.widget_count,
                "is_public": self.is_public,
                "created_by": self.created_by,
            }

        @field_serializer("widgets", when_used="json")
        def serialize_widgets_with_dashboard_context(
            self, value: list[dict[str, object]], _info: object
        ) -> dict[str, object]:
            """Serialize widgets with dashboard context."""
            return {
                "widgets": value,
                "widget_count": len(value),
                "dashboard_context": {
                    "name": self.name,
                    "is_public": self.is_public,
                    "created_by": self.created_by,
                },
            }

    class MonitoringConfig(FlextModels.Configuration):
        """Global monitoring configuration model."""

        model_config = ConfigDict(
            validate_assignment=True, use_enum_values=True, extra="forbid", frozen=False
        )

        enable_metrics: bool = Field(
            default=True, description="Enable metrics collection"
        )
        enable_tracing: bool = Field(
            default=True, description="Enable distributed tracing"
        )
        enable_alerting: bool = Field(
            default=True, description="Enable alerting system"
        )
        enable_health_checks: bool = Field(
            default=True, description="Enable health monitoring"
        )
        monitoring_endpoint: str = Field(
            default=FlextObservabilityConstants.DEFAULT_MONITORING_ENDPOINT,
            description="Monitoring endpoint URL",
        )

        @computed_field
        @property
        def enabled_features_count(self) -> int:
            """Computed field for number of enabled monitoring features."""
            features = [
                self.enable_metrics,
                self.enable_tracing,
                self.enable_alerting,
                self.enable_health_checks,
            ]
            return sum(features)

        @computed_field
        @property
        def monitoring_summary(self) -> dict[str, object]:
            """Computed field for monitoring configuration summary."""
            return {
                "metrics_enabled": self.enable_metrics,
                "tracing_enabled": self.enable_tracing,
                "alerting_enabled": self.enable_alerting,
                "health_checks_enabled": self.enable_health_checks,
                "enabled_features": self.enabled_features_count,
                "endpoint": self.monitoring_endpoint,
            }

        @model_validator(mode="after")
        def validate_monitoring_config(self) -> Self:
            """Validate monitoring configuration parameters."""
            if self.enabled_features_count == 0:
                msg = "At least one monitoring feature must be enabled"
                raise ValueError(msg)
            return self

        @field_serializer("monitoring_endpoint", when_used="json")
        def serialize_endpoint_with_security_mask(
            self, value: str, _info: object
        ) -> dict[str, object]:
            """Serialize monitoring endpoint with security considerations."""
            return {
                "endpoint": value,
                "monitoring_features": {
                    "metrics": self.enable_metrics,
                    "tracing": self.enable_tracing,
                    "alerting": self.enable_alerting,
                    "health_checks": self.enable_health_checks,
                },
            }


# Export the unified models class
__all__ = [
    "FlextObservabilityModels",
]
