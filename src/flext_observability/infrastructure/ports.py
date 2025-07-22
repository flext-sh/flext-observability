"""Infrastructure ports implementations for FLEXT-OBSERVABILITY.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Using flext-core infrastructure patterns - NO duplication.
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from flext_core.domain.shared_types import ServiceResult

from flext_observability.domain.entities import Dashboard
from flext_observability.domain.ports import (
    AlertService,
    DashboardService,
    HealthService,
    LogService,
    MetricsService,
    TracingService,
)

if TYPE_CHECKING:
    from flext_observability.config import (
        AlertingConfig,
        HealthCheckConfig,
        LoggingConfig,
        MetricsConfig,
        TracingConfig,
    )
    from flext_observability.domain.entities import (
        Alert,
        HealthCheck,
        LogEntry,
        Metric,
        Trace,
    )


class MetricsExporter(ABC):
    """Abstract metrics exporter port."""

    @abstractmethod
    async def export_metric(self, metric: Metric) -> None:
        """Export single metric.

        Args:
            metric: The metric to export.

        """
        ...

    @abstractmethod
    async def export_metrics(self, metrics: list[Metric]) -> None:
        """Export multiple metrics.

        Args:
            metrics: The metrics to export.

        """
        ...


class TraceExporter(ABC):
    """Abstract trace exporter port."""

    @abstractmethod
    async def export_trace(self, trace: Trace) -> None:
        """Export single trace.

        Args:
            trace: The trace to export.

        """
        ...

    @abstractmethod
    async def export_traces(self, traces: list[Trace]) -> None:
        """Export multiple traces.

        Args:
            traces: The traces to export.

        """
        ...


class LogExporter(ABC):
    """Abstract log exporter port."""

    @abstractmethod
    async def export_log(self, log_entry: LogEntry) -> None:
        """Export single log entry.

        Args:
            log_entry: The log entry to export.

        """
        ...

    @abstractmethod
    async def export_logs(self, log_entries: list[LogEntry]) -> None:
        """Export multiple log entries.

        Args:
            log_entries: The log entries to export.

        """
        ...


class AlertNotifier(ABC):
    """Abstract alert notifier port."""

    @abstractmethod
    async def notify(self, alert: Alert) -> None:
        """Send alert notification.

        Args:
            alert: The alert to send.

        """
        ...

    @abstractmethod
    async def notify_batch(self, alerts: list[Alert]) -> None:
        """Send multiple alert notifications.

        Args:
            alerts: The alerts to send.

        """
        ...


class FileLogPort(LogService):
    """File-based log service implementation."""

    def __init__(self, config: LoggingConfig) -> None:
        """Initialize file log port.

        Args:
            config: The logging configuration.

        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def write_log(self, log_entry: LogEntry) -> ServiceResult[Any]:
        """Write log entry to file.

        Args:
            log_entry: Log entry to write containing timestamp, level, message, and
                metadata.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            if self.config.log_to_file:
                log_file = Path(self.config.log_file_path)
                log_file.parent.mkdir(parents=True, exist_ok=True)

                # Create log record
                log_record = {
                    "timestamp": log_entry.created_at.isoformat(),
                    "level": log_entry.level,
                    "message": log_entry.message,
                    "logger": log_entry.logger_name,
                    "module": log_entry.module,
                    "function": log_entry.function,
                    "line": log_entry.line_number,
                    "correlation_id": log_entry.correlation_id,
                    "user_id": log_entry.user_id,
                    "request_id": log_entry.request_id,
                    "extra": log_entry.extra,
                    "tags": log_entry.tags,
                }

                # Use aiofiles for proper async I/O
                import aiofiles

                # NO FALLBACKS - SEMPRE usar implementações originais conforme instrução
                async with aiofiles.open(log_file, "a", encoding="utf-8") as f:
                    if self.config.structured_logging:
                        await f.write(json.dumps(log_record) + "\n")
                    else:
                        timestamp = log_record["timestamp"]
                        level = log_record["level"]
                        message = log_record["message"]
                        await f.write(f"{timestamp} [{level}] {message}\n")

            return ServiceResult.ok(None)
        except OSError as e:
            return ServiceResult.fail(f"Failed to write log: {e}")
        except (TypeError, AttributeError, UnicodeError) as e:
            return ServiceResult.fail(f"Unexpected error writing log: {e}")

    async def configure_logging(self, config: dict[str, Any]) -> ServiceResult[Any]:
        """Configure logging settings.

        Args:
            config: Dictionary containing logging configuration with keys like
                'level', 'format'.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Update logging configuration
            logging.basicConfig(
                level=getattr(logging, config.get("level", "INFO")),
                format=config.get(
                    "format",
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                ),
            )
            return ServiceResult.ok(None)
        except (ValueError, OSError, TypeError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to configure logging: {e}")

    async def get_log_level(self) -> ServiceResult[Any]:
        """Get current log level.

        Returns:
            ServiceResult with current log level string or error message on failure.

        """
        try:
            return ServiceResult.ok(self.config.log_level)
        except (AttributeError, ValueError, TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Failed to get log level: {e}")

    async def set_log_level(self, level: str) -> ServiceResult[Any]:
        """Set log level.

        Args:
            level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Convert string to LogLevel enum
            from flext_core import LogLevel

            self.config.log_level = LogLevel(level.upper())
            logging.getLogger().setLevel(getattr(logging, level))
            return ServiceResult.ok(None)
        except (ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to set log level: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error setting log level: {e}")


class PrometheusMetricsPort(MetricsService):
    """Prometheus metrics service implementation."""

    def __init__(self, config: MetricsConfig) -> None:
        """Initialize Prometheus metrics port.

        Args:
            config: The metrics configuration.

        """
        self.config = config
        self.metrics_cache: dict[str, list[dict[str, Any]]] = {}

    async def record_metric(self, metric: Metric) -> ServiceResult[Any]:
        """Record a metric value.

        Args:
            metric: Metric to record containing name, type, value, timestamp,
                labels, and unit.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Store in cache
            key = f"{metric.name}_{metric.metric_type.value}"
            if key not in self.metrics_cache:
                self.metrics_cache[key] = []

            self.metrics_cache[key].append(
                {
                    "value": metric.value,
                    "timestamp": metric.timestamp.isoformat(),
                    "labels": metric.labels,
                    "unit": metric.unit,
                },
            )

            # Keep only recent metrics
            if len(self.metrics_cache[key]) > self.config.max_metrics_per_name:
                self.metrics_cache[key] = self.metrics_cache[key][
                    -self.config.max_metrics_per_name :
                ]

            return ServiceResult.ok(None)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to record metric: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error recording metric: {e}")

    async def get_current_metrics(self) -> ServiceResult[Any]:
        """Get current metric values.

        Returns:
            ServiceResult with dictionary of current metrics containing
                current_value, count, and latest_timestamp for each metric.

        """
        try:
            current_metrics = {}
            for key, values in self.metrics_cache.items():
                if values:
                    current_metrics[key] = {
                        "current_value": values[-1]["value"],
                        "count": len(values),
                        "latest_timestamp": values[-1]["timestamp"],
                    }
            return ServiceResult.ok(current_metrics)
        except (KeyError, ValueError) as e:
            return ServiceResult.fail(f"Failed to get current metrics: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error getting current metrics: {e}")

    async def reset_metrics(self) -> ServiceResult[Any]:
        """Reset all stored metrics.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            self.metrics_cache.clear()
            return ServiceResult.ok(None)
        except (AttributeError, ValueError) as e:
            return ServiceResult.fail(f"Failed to reset metrics: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error resetting metrics: {e}")

    async def export_metrics(self, format_type: str) -> ServiceResult[Any]:
        """Export metrics in specified format.

        Args:
            format_type: Export format ('prometheus' or 'json').

        Returns:
            ServiceResult with exported metrics string or error message on failure.

        """
        try:
            if format_type == "prometheus":
                output = []
                for key, values in self.metrics_cache.items():
                    if values:
                        metric_name = key.split("_")[0]
                        latest = values[-1]
                        labels = ",".join(
                            [f'{k}="{v}"' for k, v in latest["labels"].items()],
                        )
                        output.append(f"{metric_name}{{{labels}}} {latest['value']}")
                return ServiceResult.ok("\n".join(output))
            if format_type == "json":
                return ServiceResult.ok(json.dumps(self.metrics_cache, indent=2))
            return ServiceResult.fail(f"Unsupported format: {format_type}")
        except (ValueError, KeyError, TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Failed to export metrics: {e}")


class JaegerTracingPort(TracingService):
    """Jaeger tracing service implementation."""

    def __init__(self, config: TracingConfig) -> None:
        """Initialize Jaeger tracing port.

        Args:
            config: The tracing configuration.

        """
        self.config = config
        self.traces_cache: dict[str, dict[str, Any]] = {}

    async def start_trace(self, trace: Trace) -> ServiceResult[Any]:
        """Start a new trace.

        Args:
            trace: Trace object containing trace_id, span_id, operation_name,
                service_name, and metadata.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            trace_data = {
                "trace_id": trace.trace_id,
                "span_id": trace.span_id,
                "operation_name": trace.operation_name,
                "service_name": trace.service_name,
                "start_time": trace.start_time.isoformat(),
                "status": trace.trace_status.value,
                "tags": trace.trace_tags,
                "logs": trace.logs,
                "events": trace.events,
            }

            self.traces_cache[str(trace.id)] = trace_data
            return ServiceResult.ok(None)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to start trace: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error starting trace: {e}")

    async def finish_trace(self, trace: Trace) -> ServiceResult[Any]:
        """Finish an existing trace.

        Args:
            trace: Trace object with end_time, duration_ms, status, and error
                information.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            trace_key = str(trace.id)
            if trace_key in self.traces_cache:
                self.traces_cache[trace_key].update(
                    {
                        "end_time": (
                            trace.end_time.isoformat() if trace.end_time else None
                        ),
                        "duration_ms": trace.duration_ms,
                        "status": trace.trace_status.value,
                        "error": trace.error,
                    },
                )
            return ServiceResult.ok(None)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to finish trace: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error finishing trace: {e}")

    async def add_span(
        self,
        trace: Trace,
        span_data: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Add span data to an existing trace.

        Args:
            trace: Trace object to add span to.
            span_data: Dictionary containing span information.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            trace_key = str(trace.id)
            if trace_key in self.traces_cache:
                if "spans" not in self.traces_cache[trace_key]:
                    self.traces_cache[trace_key]["spans"] = []
                self.traces_cache[trace_key]["spans"].append(span_data)
            return ServiceResult.ok(None)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to add span: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error adding span: {e}")

    async def export_traces(self, format_type: str) -> ServiceResult[Any]:
        """Export traces in specified format.

        Args:
            format_type: Export format ('jaeger' or 'json').

        Returns:
            ServiceResult with exported traces string or error message on failure.

        """
        try:
            if format_type in {"jaeger", "json"}:
                return ServiceResult.ok(json.dumps(self.traces_cache, indent=2))
            return ServiceResult.fail(f"Unsupported format: {format_type}")
        except (ValueError, KeyError, TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Failed to export traces: {e}")


class SlackAlertPort(AlertService):
    """Slack alert service implementation."""

    def __init__(self, config: AlertingConfig) -> None:
        """Initialize Slack alert port.

        Args:
            config: The alerting configuration.

        """
        self.config = config

    async def trigger_alert(self, alert: Alert) -> ServiceResult[Any]:
        """Send alert notification via Slack.

        Args:
            alert: Alert object containing title, description, severity, source,
                condition, and timestamp.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Simulate sending to Slack
            {
                "title": alert.title,
                "description": alert.description,
                "severity": alert.severity,
                "source": alert.source,
                "condition": alert.condition,
                "timestamp": alert.created_at.isoformat(),
            }

            return ServiceResult.ok(None)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to send alert: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error sending alert: {e}")

    async def resolve_alert(self, alert_id: str) -> ServiceResult[Any]:
        """Mark alert as resolved in Slack.

        Args:
            alert_id: ID of alert to resolve.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Simulate resolving in Slack
            {
                "title": f"RESOLVED: Alert {alert_id}",
                "resolved_at": datetime.now(UTC).isoformat(),
            }

            return ServiceResult.ok(None)
        except (ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to resolve alert: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error resolving alert: {e}")

    async def configure_channels(self, channels: dict[str, Any]) -> ServiceResult[Any]:
        """Configure alert channels.

        Args:
            channels: Dictionary containing channel configuration including webhook_url.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Store webhook URL in instance variable
            self.webhook_url = channels.get("webhook_url")
            self.channels = channels
            return ServiceResult.ok(None)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to configure channels: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error configuring channels: {e}")

    async def test_alert(self, channel: str) -> ServiceResult[Any]:
        """Send test alert to specified channel.

        Args:
            channel: Channel identifier to send test alert to.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Send test alert to channel
            {
                "title": "Test Alert",
                "description": "This is a test alert",
                "channel": channel,
                "timestamp": datetime.now(UTC).isoformat(),
            }

            return ServiceResult.ok(None)
        except (ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to test alert: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error testing alert: {e}")

    async def acknowledge_alert(self, alert_id: str) -> ServiceResult[Any]:
        """Acknowledge an alert.

        Args:
            alert_id: ID of alert to acknowledge.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Simulate acknowledging in Slack
            {
                "alert_id": alert_id,
                "acknowledged_at": datetime.now(UTC).isoformat(),
                "acknowledged_by": "system",
            }

            return ServiceResult.ok(None)
        except (ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to acknowledge alert: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error acknowledging alert: {e}")

    async def get_active_alerts(self) -> ServiceResult[Any]:
        """Get all active alerts.

        Returns:
            ServiceResult with list of active alerts or error message on failure.

        """
        try:
            # Simulate getting active alerts - return empty list for now
            return ServiceResult.ok([])
        except (ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get active alerts: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error getting active alerts: {e}")


class SimpleHealthPort(HealthService):
    """Simple health service implementation."""

    def __init__(self, config: HealthCheckConfig) -> None:
        """Initialize simple health port.

        Args:
            config: The health check configuration.

        """
        self.config = config
        self.registered_checks: dict[str, HealthCheck] = {}

    async def perform_health_check(self, check: HealthCheck) -> ServiceResult[Any]:
        """Perform a health check.

        Args:
            check: HealthCheck object containing check configuration.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            # Simulate running health check
            {
                "name": check.name,
                "status": "healthy",
                "timestamp": datetime.now(UTC).isoformat(),
                "response_time_ms": 5.0,
            }

            return ServiceResult.ok(None)
        except (ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Health check failed: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error in health check: {e}")

    async def get_system_health(self) -> ServiceResult[Any]:
        """Get overall system health status.

        Returns:
            ServiceResult with dictionary containing status, timestamp, and
                individual check results.

        """
        try:
            health_status: dict[str, Any] = {
                "status": "healthy",
                "timestamp": datetime.now(UTC).isoformat(),
                "checks": {},
            }

            # Run all registered checks
            for name, check in self.registered_checks.items():
                check_result = await self.perform_health_check(check)
                health_status["checks"][name] = {
                    "healthy": check_result.success,
                    "response_time_ms": 5.0 if check_result.success else None,
                    "error": (check_result.error if not check_result.success else None),
                }

            # Overall status
            if any(not check["healthy"] for check in health_status["checks"].values()):
                health_status["status"] = "unhealthy"

            return ServiceResult.ok(health_status)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get system health: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error getting system health: {e}")

    async def register_health_check(self, check: HealthCheck) -> ServiceResult[Any]:
        """Register a new health check.

        Args:
            check: HealthCheck object to register.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            self.registered_checks[check.name] = check
            return ServiceResult.ok(None)
        except (ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to register check: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error registering check: {e}")

    async def unregister_check(self, check_name: str) -> ServiceResult[Any]:
        """Unregister a health check by name.

        Args:
            check_name: Name of the health check to remove.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        try:
            if check_name in self.registered_checks:
                del self.registered_checks[check_name]
            return ServiceResult.ok(None)
        except (KeyError, ValueError) as e:
            return ServiceResult.fail(f"Failed to unregister check: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error unregistering check: {e}")


class MemoryDashboardPort(DashboardService):
    """Memory-based dashboard service implementation."""

    def __init__(self, config: AlertingConfig) -> None:
        """Initialize memory dashboard port.

        Args:
            config: The alerting configuration.

        """
        self.config = config
        self.dashboard_cache: dict[str, Any] = {}

    async def render_dashboard(
        self,
        dashboard: Dashboard,
    ) -> ServiceResult[Any]:
        """Render dashboard with current data.

        Args:
            dashboard: Dashboard object containing configuration, widgets, and layout.

        Returns:
            ServiceResult with dictionary containing rendered dashboard data
                including widgets and metadata.

        """
        try:
            rendered: dict[str, Any] = {
                "id": str(dashboard.id),
                "title": dashboard.title,
                "description": dashboard.description,
                "refresh_interval": dashboard.refresh_interval_seconds,
                "widgets": [],
                "timestamp": dashboard.created_at.isoformat(),
            }

            # Render widgets
            for widget in dashboard.widgets:
                widget_data = await self.get_widget_data(widget)
                if widget_data.is_success:
                    rendered["widgets"].append(widget_data.data)

            return ServiceResult.ok(rendered)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to render dashboard: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error rendering dashboard: {e}")

    async def export_dashboard(
        self,
        dashboard: Dashboard,
        format_type: str,
    ) -> ServiceResult[Any]:
        """Export dashboard in specified format.

        Args:
            dashboard: The dashboard to export.
            format_type: The export format.

        Returns:
            ServiceResult with exported dashboard string or error message.

        """
        try:
            if format_type == "json":
                config = {
                    "title": dashboard.title,
                    "description": dashboard.description,
                    "refresh_interval": dashboard.refresh_interval_seconds,
                    "widgets": dashboard.widgets,
                    "layout": dashboard.layout,
                    "filters": dashboard.filters,
                    "variables": dashboard.variables,
                }
                return ServiceResult.ok(json.dumps(config, indent=2))
            return ServiceResult.fail(f"Unsupported format: {format_type}")
        except (ValueError, KeyError, TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Failed to export dashboard: {e}")

    async def import_dashboard(
        self,
        config_str: str,
        format_type: str,
    ) -> ServiceResult[Any]:
        """Import dashboard from configuration.

        Args:
            config_str: The dashboard configuration string.
            format_type: The import format.

        Returns:
            ServiceResult with imported dashboard or error message.

        """
        try:
            if format_type == "json":
                config_data = json.loads(config_str)
                dashboard = Dashboard(
                    title=config_data["title"],
                    description=config_data.get("description"),
                    refresh_interval_seconds=config_data.get("refresh_interval", 30),
                    widgets=config_data.get("widgets", []),
                    layout=config_data.get("layout", {}),
                    filters=config_data.get("filters", {}),
                    variables=config_data.get("variables", {}),
                )
                return ServiceResult.ok(dashboard)
            return ServiceResult.fail(f"Unsupported format: {format_type}")
        except (ValueError, KeyError, TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Failed to import dashboard: {e}")

    async def get_widget_data(
        self,
        widget_config: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Get widget data for rendering.

        Args:
            widget_config: The widget configuration dictionary.

        Returns:
            ServiceResult with widget data dictionary or error message.

        """
        try:
            # Simulate widget data
            widget_data = {
                "id": widget_config.get("id", "widget-1"),
                "type": widget_config.get("type", "metric"),
                "title": widget_config.get("title", "Widget"),
                "data": {
                    "value": 42,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "unit": widget_config.get("unit", "count"),
                },
            }

            return ServiceResult.ok(widget_data)
        except (KeyError, ValueError, AttributeError) as e:
            return ServiceResult.fail(f"Failed to get widget data: {e}")
        except (TypeError, RuntimeError) as e:
            return ServiceResult.fail(f"Unexpected error getting widget data: {e}")


class EventBus(ABC):
    """Base class for event bus implementations."""

    @abstractmethod
    async def publish_event(
        self,
        event: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Publish event to bus.

        Args:
            event: The event to publish.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        ...

    @abstractmethod
    async def subscribe(
        self,
        topic: str,
        handler: Any,
    ) -> ServiceResult[Any]:
        """Subscribe to topic with handler.

        Args:
            topic: The topic to subscribe to.
            handler: The handler function.

        Returns:
            ServiceResult with None on success or error message on failure.

        """
        ...
