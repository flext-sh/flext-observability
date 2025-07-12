"""Domain entities for FLEXT-OBSERVABILITY.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from typing import TYPE_CHECKING
from typing import Any

from flext_core.domain.pydantic_base import DomainEntity
from flext_core.domain.pydantic_base import Field
from flext_core.domain.types import AlertSeverity
from flext_core.domain.types import LogLevel
from flext_core.domain.types import MetricType
from flext_core.domain.types import Status
from flext_core.domain.types import TraceStatus

if TYPE_CHECKING:
    from flext_observability.domain.value_objects import ComponentName


class LogEntry(DomainEntity):
    """Log entry domain entity using enhanced mixins for code reduction."""

    level: LogLevel = Field(default=LogLevel.INFO, description="Log level")
    message: str = Field(..., min_length=1, description="Log message")
    logger_name: str = Field(..., min_length=1, description="Logger name")
    module: str | None = None
    function: str | None = None
    line_number: int | None = None

    # Context
    correlation_id: str | None = None
    user_id: str | None = None
    request_id: str | None = None
    session_id: str | None = None

    # Metadata
    extra: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    # Performance
    duration_ms: float | None = None
    memory_usage: int | None = None

    @property
    def is_error(self) -> bool:
        """Check if log entry is an error level.

        Returns:
            True if log level is ERROR or CRITICAL.

        """
        return self.level in {LogLevel.ERROR, LogLevel.CRITICAL}

    @property
    def is_warning_or_higher(self) -> bool:
        """Check if log entry is warning level or higher.

        Returns:
            True if log level is WARNING, ERROR, or CRITICAL.

        """
        return self.level in {LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL}

    @property
    def is_structured(self) -> bool:
        """Check if log entry has structured data.

        Returns:
            True if log entry has extra data or tags.

        """
        return len(self.extra) > 0 or len(self.tags) > 0

    def add_tag(self, tag: str) -> None:
        """Add a tag to the log entry.

        Args:
            tag: Tag to add to the log entry.

        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the log entry.

        Args:
            tag: Tag to remove from the log entry.

        """
        if tag in self.tags:
            self.tags.remove(tag)

    def add_extra(self, key: str, value: Any) -> None:
        """Add extra metadata to the log entry.

        Args:
            key: Metadata key.
            value: Metadata value.

        """
        self.extra[key] = value

    def remove_extra(self, key: str) -> None:
        """Remove extra metadata from the log entry.

        Args:
            key: Metadata key to remove.

        """
        self.extra.pop(key, None)


class Metric(DomainEntity):
    """Metric domain entity using enhanced mixins for code reduction."""

    name: str = Field(..., min_length=1, max_length=255)
    metric_type: MetricType = Field(
        default=MetricType.GAUGE
    )  # Using metric_type instead of type
    value: float = Field(...)
    unit: str | None = None

    # Component information
    component: ComponentName = Field(...)

    # Labels/Tags
    labels: dict[str, str] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    # Metadata
    help_text: str | None = None
    source: str | None = None
    namespace: str | None = None
    subsystem: str | None = None

    # Timing
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Buckets for histogram
    buckets: list[float] = Field(default_factory=list)

    # Quantiles for summary
    quantiles: dict[float, float] = Field(default_factory=dict)

    @property
    def is_counter(self) -> bool:
        """Check if metric is a counter type.

        Returns:
            True if metric type is COUNTER.

        """
        return bool(self.metric_type == MetricType.COUNTER)

    @property
    def is_gauge(self) -> bool:
        """Check if metric is a gauge type.

        Returns:
            True if metric type is GAUGE.

        """
        return bool(self.metric_type == MetricType.GAUGE)

    @property
    def is_histogram(self) -> bool:
        """Check if metric is a histogram type.

        Returns:
            True if metric type is HISTOGRAM.

        """
        return bool(self.metric_type == MetricType.HISTOGRAM)

    @property
    def is_summary(self) -> bool:
        """Check if metric is a summary type.

        Returns:
            True if metric type is SUMMARY.

        """
        return bool(self.metric_type == MetricType.SUMMARY)

    @property
    def full_name(self) -> str:
        """Get the full metric name with namespace and subsystem.

        Returns:
            Complete metric name with namespace_subsystem_name format.

        """
        parts = []
        if self.namespace:
            parts.append(self.namespace)
        if self.subsystem:
            parts.append(self.subsystem)
        parts.append(self.name)
        return "_".join(parts)

    def add_label(self, key: str, value: str) -> None:
        """Add a label to the metric.

        Args:
            key: Label key.
            value: Label value.

        """
        self.labels[key] = value

    def remove_label(self, key: str) -> None:
        """Remove a label from the metric.

        Args:
            key: Label key to remove.

        """
        self.labels.pop(key, None)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the metric.

        Args:
            tag: Tag to add to the metric.

        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the metric.

        Args:
            tag: Tag to remove from the metric.

        """
        if tag in self.tags:
            self.tags.remove(tag)


class Trace(DomainEntity):
    """Trace domain entity using enhanced mixins for code reduction."""

    trace_id: str = Field(..., min_length=1)
    span_id: str = Field(..., min_length=1)
    parent_span_id: str | None = None
    operation_name: str = Field(..., min_length=1)

    # Timing
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime | None = None
    duration_ms: float | None = None

    # Status
    trace_status: TraceStatus = Field(
        default=TraceStatus.STARTED,
        description="Trace status (renamed to avoid conflict with StatusMixin)",
    )
    error: str | None = None

    # Context
    service_name: str = Field(..., min_length=1)
    service_version: str | None = None
    component: ComponentName = Field(...)

    # Tags
    trace_tags: dict[str, str] = Field(
        default_factory=dict,
        description="Trace tags (renamed to avoid conflict with MetadataMixin)",
    )

    # Baggage
    baggage: dict[str, str] = Field(default_factory=dict)

    # Logs
    logs: list[dict[str, Any]] = Field(default_factory=list)

    # Events
    events: list[dict[str, Any]] = Field(default_factory=list)

    @property
    def is_finished(self) -> bool:
        """Check if trace has finished execution.

        Returns:
            True if trace has an end time.

        """
        return self.end_time is not None

    @property
    def is_error(self) -> bool:
        """Check if trace ended with an error.

        Returns:
            True if trace status is FAILED.

        """
        return self.trace_status == TraceStatus.FAILED

    @property
    def is_ok(self) -> bool:
        """Check if trace completed successfully.

        Returns:
            True if trace status is COMPLETED.

        """
        return self.trace_status == TraceStatus.COMPLETED

    @property
    def is_root_span(self) -> bool:
        """Check if this is a root span.

        Returns:
            True if trace has no parent span ID.

        """
        return self.parent_span_id is None

    def start(self) -> None:
        """Start the trace execution.

        Sets status to IN_PROGRESS and records start time.
        """
        self.trace_status = TraceStatus.IN_PROGRESS
        self.start_time = datetime.utcnow()

    def finish(self, end_time: datetime | None = None) -> None:
        """Finish the trace execution.

        Args:
            end_time: Optional end time, defaults to current time.

        """
        self.end_time = end_time or datetime.utcnow()
        if self.trace_status == TraceStatus.IN_PROGRESS:
            self.trace_status = TraceStatus.COMPLETED

        if self.duration_ms is None:
            self.duration_ms = (self.end_time - self.start_time).total_seconds() * 1000

    def fail(self, error: str) -> None:
        """Mark the trace as failed.

        Args:
            error: Error message explaining the failure.

        """
        self.trace_status = TraceStatus.FAILED
        self.error = error
        self.finish()

    def cancel(self) -> None:
        """Cancel the trace execution.

        Sets status to CANCELLED and finishes the trace.
        """
        self.trace_status = TraceStatus.CANCELLED
        self.finish()

    def add_trace_tag(self, key: str, value: str) -> None:
        """Add a tag to the trace.

        Args:
            key: Tag key.
            value: Tag value.

        """
        self.trace_tags[key] = value

    def remove_trace_tag(self, key: str) -> None:
        """Remove a tag from the trace.

        Args:
            key: Tag key to remove.

        """
        self.trace_tags.pop(key, None)

    def add_baggage(self, key: str, value: str) -> None:
        """Add baggage to the trace.

        Args:
            key: Baggage key.
            value: Baggage value.

        """
        self.baggage[key] = value

    def remove_baggage(self, key: str) -> None:
        """Remove baggage from the trace.

        Args:
            key: Baggage key to remove.

        """
        self.baggage.pop(key, None)

    def add_log(
        self,
        message: str,
        level: LogLevel = LogLevel.INFO,
        **kwargs: Any,
    ) -> None:
        """Add a log entry to the trace.

        Args:
            message: Log message.
            level: Log level, defaults to INFO.
            **kwargs: Additional log attributes.

        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "message": message,
            **kwargs,
        }
        self.logs.append(log_entry)

    def add_event(self, name: str, **attributes: Any) -> None:
        """Add an event to the trace.

        Args:
            name: Event name.
            **attributes: Event attributes.

        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": name,
            "attributes": attributes,
        }
        self.events.append(event)


class Alert(DomainEntity):
    """Alert domain entity using enhanced mixins for code reduction."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    severity: AlertSeverity = Field(default=AlertSeverity.MEDIUM)

    # Source
    source: str = Field(..., min_length=1)
    source_type: str = Field(..., min_length=1)  # metric, log, trace

    # Conditions
    condition: str = Field(..., min_length=1)
    threshold: float | None = None

    # Status
    alert_status: Status = Field(
        default=Status.ACTIVE,
        description="Alert status (renamed to avoid conflict with StatusMixin)",
    )
    resolved_at: datetime | None = None
    resolution_reason: str | None = None

    # Context
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)

    # Notifications
    notified_at: datetime | None = None
    notification_channels: list[str] = Field(default_factory=list)

    # Acknowledgment
    acknowledged_at: datetime | None = None
    acknowledged_by: str | None = None

    # Suppression
    suppressed_until: datetime | None = None
    suppression_reason: str | None = None

    @property
    def is_resolved(self) -> bool:
        """Check if alert has been resolved.

        Returns:
            True if alert has a resolution timestamp.

        """
        return self.resolved_at is not None

    @property
    def is_critical(self) -> bool:
        """Check if alert has critical severity.

        Returns:
            True if alert severity is CRITICAL.

        """
        return self.severity == AlertSeverity.CRITICAL

    @property
    def is_high_priority(self) -> bool:
        """Check if alert has high priority.

        Returns:
            True if alert severity is HIGH or CRITICAL.

        """
        return self.severity in {AlertSeverity.HIGH, AlertSeverity.CRITICAL}

    @property
    def is_acknowledged(self) -> bool:
        """Check if alert has been acknowledged.

        Returns:
            True if alert has an acknowledgment timestamp.

        """
        return self.acknowledged_at is not None

    @property
    def is_suppressed(self) -> bool:
        """Check if alert is currently suppressed.

        Returns:
            True if alert is suppressed until a future time.

        """
        return (
            self.suppressed_until is not None
            and self.suppressed_until > datetime.utcnow()
        )

    def resolve(self) -> None:
        """Resolve the alert.

        Sets resolution timestamp and status to RESOLVED.
        """
        self.resolved_at = datetime.utcnow()
        self.alert_status = Status.RESOLVED

    def acknowledge(self, user: str) -> None:
        """Acknowledge the alert.

        Args:
            user: User who acknowledged the alert.

        """
        self.acknowledged_at = datetime.utcnow()
        self.acknowledged_by = user

    def suppress(self, duration_minutes: int, reason: str) -> None:
        """Suppress the alert for a specified duration.

        Args:
            duration_minutes: Minutes to suppress the alert.
            reason: Reason for suppression.

        """
        self.suppressed_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.suppression_reason = reason

    def add_label(self, key: str, value: str) -> None:
        """Add a label to the alert.

        Args:
            key: Label key.
            value: Label value.

        """
        self.labels[key] = value

    def remove_label(self, key: str) -> None:
        """Remove a label from the alert.

        Args:
            key: Label key to remove.

        """
        self.labels.pop(key, None)

    def add_annotation(self, key: str, value: str) -> None:
        """Add an annotation to the alert.

        Args:
            key: Annotation key.
            value: Annotation value.

        """
        self.annotations[key] = value

    def remove_annotation(self, key: str) -> None:
        """Remove an annotation from the alert.

        Args:
            key: Annotation key to remove.

        """
        self.annotations.pop(key, None)


class HealthCheck(DomainEntity):
    """Health check domain entity using enhanced mixins for code reduction."""

    name: str = Field(..., min_length=1, max_length=255)
    health_status: Status = Field(
        default=Status.ACTIVE,
        description="Health check status (renamed to avoid conflict with StatusMixin)",
    )

    # Check details
    check_type: str = Field(..., min_length=1)  # database, cache, service, etc.
    endpoint: str | None = None
    timeout_seconds: int = Field(default=5)

    # Component information
    component: ComponentName = Field(...)

    # Results
    last_check_at: datetime | None = None
    last_success_at: datetime | None = None
    last_failure_at: datetime | None = None

    # Health status (mutable)
    is_healthy: bool = Field(default=True)
    check_result: dict[str, Any] = Field(default_factory=dict)

    # Status tracking
    consecutive_failures: int = Field(default=0)
    total_checks: int = Field(default=0)
    total_successes: int = Field(default=0)
    total_failures: int = Field(default=0)

    # Response data
    response_time_ms: float | None = None
    response_data: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None

    # Thresholds
    warning_threshold: float | None = None
    critical_threshold: float | None = None

    @property
    def is_healthy_computed(self) -> bool:
        """Check if health check is healthy based on status.

        Returns:
            True if status is ACTIVE and no consecutive failures.

        """
        return self.health_status == Status.ACTIVE and self.consecutive_failures == 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage.

        Returns:
            Success rate as a percentage (0-100).

        """
        if self.total_checks == 0:
            return 0.0
        return (self.total_successes / self.total_checks) * 100

    @property
    def is_failing(self) -> bool:
        """Check if health check is currently failing.

        Returns:
            True if there are consecutive failures.

        """
        return self.consecutive_failures > 0

    @property
    def is_critical(self) -> bool:
        """Check if health check is in critical state.

        Returns:
            True if consecutive failures exceed critical threshold.

        """
        return (
            self.critical_threshold is not None
            and self.consecutive_failures >= self.critical_threshold
        )

    @property
    def is_warning(self) -> bool:
        """Check if health check is in warning state.

        Returns:
            True if consecutive failures exceed warning threshold.

        """
        return (
            self.warning_threshold is not None
            and self.consecutive_failures >= self.warning_threshold
        )

    def record_success(
        self,
        response_time_ms: float,
        response_data: dict[str, Any] | None = None,
    ) -> None:
        """Record a successful health check.

        Args:
            response_time_ms: Response time in milliseconds.
            response_data: Optional response data.

        """
        self.last_check_at = datetime.utcnow()
        self.last_success_at = self.last_check_at
        self.consecutive_failures = 0
        self.total_checks += 1
        self.total_successes += 1
        self.response_time_ms = response_time_ms
        self.response_data = response_data or {}
        self.error_message = None

    def record_failure(self, error_message: str) -> None:
        """Record a failed health check.

        Args:
            error_message: Error message for the failure.

        """
        self.last_check_at = datetime.utcnow()
        self.last_failure_at = self.last_check_at
        self.consecutive_failures += 1
        self.total_checks += 1
        self.total_failures += 1
        self.error_message = error_message
        self.response_data = {}

    def reset_counters(self) -> None:
        """Reset all health check counters.

        Resets all counters to zero for a fresh start.
        """
        self.consecutive_failures = 0
        self.total_checks = 0
        self.total_successes = 0
        self.total_failures = 0


class Dashboard(DomainEntity):
    """Dashboard domain entity using enhanced mixins for code reduction."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None

    # Configuration
    refresh_interval_seconds: int = Field(default=30)
    auto_refresh: bool = Field(default=True)

    # Widgets
    widgets: list[dict[str, Any]] = Field(default_factory=list)
    layout: dict[str, Any] = Field(default_factory=dict)

    # Filters
    time_range: str = Field(default="1h")  # 1h, 6h, 24h, 7d, 30d
    filters: dict[str, Any] = Field(default_factory=dict)

    # Sharing
    is_public: bool = Field(default=False)
    shared_with: list[str] = Field(default_factory=list)

    # Metadata
    tags: list[str] = Field(default_factory=list)
    category: str | None = None

    # Variables
    variables: dict[str, Any] = Field(default_factory=dict)

    @property
    def widget_count(self) -> int:
        """Get the number of widgets in the dashboard.

        Returns:
            Number of widgets.

        """
        return len(self.widgets)

    @property
    def is_shared(self) -> bool:
        """Check if dashboard is shared.

        Returns:
            True if dashboard is public or shared with users.

        """
        return self.is_public or len(self.shared_with) > 0

    @property
    def is_auto_refreshing(self) -> bool:
        """Check if dashboard has auto-refresh enabled.

        Returns:
            True if auto-refresh is enabled with valid interval.

        """
        return self.auto_refresh and self.refresh_interval_seconds > 0

    def add_widget(self, widget: dict[str, Any]) -> None:
        """Add a widget to the dashboard.

        Args:
            widget: Widget configuration to add.

        """
        self.widgets.append(widget)

    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the dashboard.

        Args:
            widget_id: ID of the widget to remove.

        Returns:
            True if widget was removed.

        """
        original_length = len(self.widgets)
        self.widgets = [w for w in self.widgets if w.get("id") != widget_id]
        return len(self.widgets) < original_length

    def update_widget(self, widget_id: str, updates: dict[str, Any]) -> bool:
        """Update a widget in the dashboard.

        Args:
            widget_id: ID of the widget to update.
            updates: Updates to apply to the widget.

        Returns:
            True if widget was found and updated.

        """
        for widget in self.widgets:
            if widget.get("id") == widget_id:
                widget.update(updates)
                return True
        return False

    def add_tag(self, tag: str) -> None:
        """Add a tag to the dashboard.

        Args:
            tag: Tag to add to the dashboard.

        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the dashboard.

        Args:
            tag: Tag to remove from the dashboard.

        """
        if tag in self.tags:
            self.tags.remove(tag)

    def set_variable(self, name: str, value: Any) -> None:
        """Set a dashboard variable.

        Args:
            name: Variable name.
            value: Variable value.

        """
        self.variables[name] = value

    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get a dashboard variable.

        Args:
            name: Variable name.
            default: Default value if variable not found.

        Returns:
            Variable value or default.

        """
        return self.variables.get(name, default)

    def remove_variable(self, name: str) -> None:
        """Remove a dashboard variable.

        Args:
            name: Variable name to remove.

        """
        self.variables.pop(name, None)


__all__ = [
    "Alert",
    "Dashboard",
    "HealthCheck",
    "LogEntry",
    "Metric",
    "Trace",
]
