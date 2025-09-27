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

from pydantic import Field, field_validator

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

    # Core Metrics Models
    class MetricEntry(FlextModels.Value):
        """Comprehensive metric entry model."""

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

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate metric name is not empty."""
            if not v or not v.strip():
                msg = "Metric name cannot be empty"
                raise ValueError(msg)
            return v.strip()

    class MetricConfig(FlextModels.Configuration):
        """Metric configuration model."""

        collection_interval: float = Field(
            default=60.0, description="Collection interval in seconds"
        )
        retention_days: int = Field(default=30, description="Metric retention in days")
        aggregation_method: str = Field(default="sum", description="Aggregation method")
        enable_alerting: bool = Field(
            default=True, description="Enable alerting for metrics"
        )

    # Distributed Tracing Models
    class TraceEntry(FlextModels.Value):
        """Comprehensive trace entry model."""

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

        @field_validator("operation_name")
        @classmethod
        def validate_operation_name(cls, v: str) -> str:
            """Validate operation name is not empty."""
            if not v or not v.strip():
                msg = "Operation name cannot be empty"
                raise ValueError(msg)
            return v.strip()

    class TraceConfig(FlextModels.Configuration):
        """Trace configuration model."""

        sampling_rate: float = Field(
            default=0.1, description="Trace sampling rate (0.0-1.0)"
        )
        max_trace_duration: int = Field(
            default=300, description="Maximum trace duration in seconds"
        )
        enable_performance_tracing: bool = Field(
            default=True, description="Enable performance tracing"
        )

    # Alert Management Models
    class AlertEntry(FlextModels.Value):
        """Comprehensive alert entry model."""

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

        @field_validator("severity")
        @classmethod
        def validate_severity(cls, v: str) -> str:
            """Validate severity is one of the valid levels."""
            valid_severities = ["critical", "warning", "info", "low"]
            if v.lower() not in valid_severities:
                msg = f"Severity must be one of: {valid_severities}"
                raise ValueError(msg)
            return v.lower()

    class AlertConfig(FlextModels.Configuration):
        """Alert configuration model."""

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

    # Health Monitoring Models
    class HealthCheckEntry(FlextModels.Value):
        """Comprehensive health check entry model."""

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

        @field_validator("status")
        @classmethod
        def validate_status(cls, v: str) -> str:
            """Validate health check status is one of the valid statuses."""
            valid_statuses = ["healthy", "degraded", "unhealthy", "unknown"]
            if v.lower() not in valid_statuses:
                msg = f"Status must be one of: {valid_statuses}"
                raise ValueError(msg)
            return v.lower()

    class HealthConfig(FlextModels.Configuration):
        """Health monitoring configuration model."""

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

    # Log Management Models
    class LogEntry(FlextModels.Value):
        """Comprehensive log entry model."""

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

        @field_validator("level")
        @classmethod
        def validate_level(cls, v: str) -> str:
            """Validate log level is one of the valid levels."""
            valid_levels = ["debug", "info", "warning", "error", "critical"]
            if v.lower() not in valid_levels:
                msg = f"Log level must be one of: {valid_levels}"
                raise ValueError(msg)
            return v.lower()

    class LogConfig(FlextModels.Configuration):
        """Log configuration model."""

        retention_days: int = Field(default=7, description="Log retention in days")
        max_log_size_mb: int = Field(default=100, description="Maximum log size in MB")
        enable_structured_logging: bool = Field(
            default=True, description="Enable structured logging"
        )
        log_format: str = Field(default="json", description="Log format")

    # Performance Monitoring Models
    class PerformanceEntry(FlextModels.Value):
        """Performance monitoring entry model."""

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

    class PerformanceConfig(FlextModels.Configuration):
        """Performance monitoring configuration model."""

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

    # Observability Dashboard Models
    class DashboardEntry(FlextModels.Value):
        """Dashboard configuration entry model."""

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

    class MonitoringConfig(FlextModels.Configuration):
        """Global monitoring configuration model."""

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


# Export the unified models class
__all__ = [
    "FlextObservabilityModels",
]
