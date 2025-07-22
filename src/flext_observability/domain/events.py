"""Domain events for observability - things that have happened.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import DomainEvent, Field

if TYPE_CHECKING:
    from datetime import datetime

    from flext_core import AlertSeverity, LogLevel

    from flext_observability.domain.entities import (
        Alert,
        HealthCheck,
        LogEntry,
        Metric,
        Trace,
    )
    from flext_observability.domain.value_objects import (
        ComponentName,
        HealthStatus,
    )


class MetricCollected(DomainEvent):
    """Event raised when a metric is collected."""

    metric: Metric = Field(description="The collected metric")
    component: ComponentName = Field(description="Component that generated the metric")


class AlertTriggered(DomainEvent):
    """Event raised when an alert is triggered."""

    alert: Alert = Field(description="The triggered alert")
    metric: Metric = Field(description="Metric that triggered the alert")
    severity: AlertSeverity = Field(description="Alert severity")


class AlertAcknowledged(DomainEvent):
    """Event raised when an alert is acknowledged."""

    alert_id: str = Field(description="ID of the acknowledged alert")
    acknowledged_by: str = Field(description="User who acknowledged the alert")
    acknowledged_at: datetime = Field(description="When the alert was acknowledged")


class AlertResolved(DomainEvent):
    """Event raised when an alert is resolved."""

    alert_id: str = Field(description="ID of the resolved alert")
    resolved_at: datetime = Field(description="When the alert was resolved")
    resolution_reason: str | None = Field(
        default=None,
        description="Reason for resolution",
    )


class HealthCheckCompleted(DomainEvent):
    """Event raised when a health check is completed."""

    health_check: HealthCheck = Field(description="The completed health check")
    component: ComponentName = Field(description="Component that was checked")
    status: HealthStatus = Field(description="Health check status")
    duration_ms: int = Field(description="Check duration in milliseconds")


class ComponentHealthChanged(DomainEvent):
    """Event raised when a component's health status changes."""

    component: ComponentName = Field(description="Component whose health changed")
    previous_status: HealthStatus = Field(description="Previous health status")
    new_status: HealthStatus = Field(description="New health status")
    reason: str | None = Field(default=None, description="Reason for the change")


class TraceStarted(DomainEvent):
    """Event raised when a trace is started."""

    trace: Trace = Field(description="The started trace")
    component: ComponentName = Field(description="Component performing the operation")
    operation_name: str = Field(description="Name of the operation being traced")


class TraceCompleted(DomainEvent):
    """Event raised when a trace is completed."""

    trace: Trace = Field(description="The completed trace")
    component: ComponentName = Field(
        description="Component that performed the operation",
    )
    operation_name: str = Field(description="Name of the operation that was traced")
    duration_ms: int = Field(description="Operation duration in milliseconds")
    success: bool = Field(description="Whether the operation succeeded")


class LogEntryCreated(DomainEvent):
    """Event raised when a log entry is created."""

    log_entry: LogEntry = Field(description="The created log entry")
    component: ComponentName = Field(description="Component that generated the log")
    level: LogLevel = Field(description="Log level")
    message: str = Field(description="Log message")


class ErrorLogCreated(DomainEvent):
    """Event raised when an error log is created."""

    log_entry: LogEntry = Field(description="The error log entry")
    component: ComponentName = Field(description="Component that generated the error")
    error_message: str = Field(description="Error message")
    exception: str | None = Field(default=None, description="Exception details")


class MetricThresholdExceeded(DomainEvent):
    """Event raised when a metric exceeds its threshold."""

    metric: Metric = Field(description="Metric that exceeded threshold")
    threshold_value: float = Field(description="Threshold value that was exceeded")
    actual_value: float = Field(description="Actual metric value")
    component: ComponentName = Field(description="Component that generated the metric")


class SystemResourceExhausted(DomainEvent):
    """Event raised when system resources are exhausted."""

    resource_type: str = Field(
        description="Type of exhausted resource (cpu, memory, disk)",
    )
    current_usage: float = Field(description="Current usage percentage")
    threshold: float = Field(description="Threshold percentage")
    component: ComponentName = Field(description="Component monitoring the resource")
    recommendations: list[str] = Field(
        default_factory=list,
        description="Recommendations",
    )


class ComponentUnavailable(DomainEvent):
    """Event raised when a component becomes unavailable."""

    component: ComponentName = Field(description="Component that became unavailable")
    reason: str = Field(description="Reason for unavailability")
    last_seen: datetime = Field(description="When the component was last seen")
    impact: str | None = Field(default=None, description="Impact description")
