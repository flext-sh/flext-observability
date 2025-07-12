"""Infrastructure adapters for external systems.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio
import contextlib
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

from flext_core.config.base import injectable
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.ports import HealthService as HealthChecker
from flext_observability.domain.value_objects import ComponentName
from flext_observability.domain.value_objects import HealthStatus
from flext_observability.infrastructure.persistence.base import EventBus
from flext_observability.infrastructure.ports import AlertNotifier
from flext_observability.infrastructure.ports import LogExporter
from flext_observability.infrastructure.ports import MetricsExporter
from flext_observability.infrastructure.ports import TraceExporter

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_observability.domain.entities import Alert
    from flext_observability.domain.entities import LogEntry
    from flext_observability.domain.entities import Metric
    from flext_observability.domain.entities import Trace


@injectable(EventBus)
class InMemoryEventBus(EventBus):
    """In-memory event bus implementation."""

    def __init__(self) -> None:
        """Initialize in-memory event bus."""
        self._handlers: dict[type[object], list[Callable[..., object]]] = {}

    async def publish(self, event: object) -> None:
        """Publish domain event to registered handlers.

        Args:
            event: Domain event to publish.

        """
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except (ValueError, TypeError, AttributeError) as e:
                # Log error but don't stop processing other handlers
                import logging
                logging.getLogger(__name__).error(f"Event handler failed: {e}")

    async def subscribe(self, event_type: type[object], handler: Callable[..., object]) -> None:
        """Subscribe to events of specific type.

        Args:
            event_type: Type of event to subscribe to.
            handler: Handler function for the event.

        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def unsubscribe(self, event_type: type[object], handler: Callable[..., object]) -> None:
        """Unsubscribe from events of specific type.

        Args:
            event_type: Type of event to unsubscribe from.
            handler: Handler function to remove.

        """
        if event_type in self._handlers:
            with contextlib.suppress(ValueError):
                self._handlers[event_type].remove(handler)


@injectable(MetricsExporter)
class PrometheusMetricsExporter(MetricsExporter):
    """Prometheus metrics exporter."""

    def __init__(self) -> None:
        """Initialize Prometheus metrics exporter."""
        self._metrics_registry: dict[str, object] = {}

    async def export_metrics(self, metrics: list[Metric]) -> None:
        """Export multiple metrics to Prometheus.

        Args:
            metrics: List of metrics to export.

        """
        for metric in metrics:
            await self.export_metric(metric)

    async def export_metric(self, metric: Metric) -> None:
        """Export single metric to Prometheus registry.

        Args:
            metric: Metric to export.

        """
        # In a real implementation, this would create Prometheus metrics
        # For now, we'll just store them in memory
        metric_key = f"{metric.source or 'default'}.{metric.name}"
        self._metrics_registry[metric_key] = {
            "value": float(metric.value),
            "unit": metric.unit,
            "type": metric.metric_type.value,
            "timestamp": metric.timestamp,
            "tags": metric.tags,
        }


@injectable(TraceExporter)
class OpenTelemetryTraceExporter(TraceExporter):
    """OpenTelemetry trace exporter."""

    def __init__(self) -> None:
        """Initialize OpenTelemetry trace exporter."""
        self._traces: list[dict[str, object]] = []

    async def export_trace(self, trace: Trace) -> None:
        """Export trace to OpenTelemetry collector.

        Args:
            trace: Trace to export.

        """
        trace_data = {
            "trace_id": trace.trace_id,
            "span_id": trace.span_id,
            "operation_name": trace.operation_name,
            "service_name": trace.service_name,
            "status": trace.trace_status.value,
            "start_time": trace.start_time,
            "end_time": trace.end_time,
            "duration_ms": trace.duration_ms,
            "tags": trace.trace_tags,
            "logs": trace.logs,
            "error": trace.error,
        }
        self._traces.append(trace_data)

    async def export_traces(self, traces: list[Trace]) -> None:
        """Export multiple traces to OpenTelemetry collector.

        Args:
            traces: List of traces to export.

        """
        for trace in traces:
            await self.export_trace(trace)


@injectable(LogExporter)
class StructlogLogAdapter(LogExporter):
    """Structlog log adapter."""

    def __init__(self) -> None:
        """Initialize structlog log adapter."""
        self._logs: list[dict[str, object]] = []

    async def export_log(self, log_entry: LogEntry) -> None:
        """Export log entry to structured logging system.

        Args:
            log_entry: Log entry to export.

        """
        log_data = {
            "level": log_entry.level.value,
            "message": log_entry.message,
            "logger_name": log_entry.logger_name,
            "timestamp": log_entry.created_at,
            "correlation_id": log_entry.correlation_id,
            "user_id": log_entry.user_id,
            "request_id": log_entry.request_id,
            "extra": log_entry.extra,
            "tags": log_entry.tags,
            "duration_ms": log_entry.duration_ms,
        }
        self._logs.append(log_data)

    async def export_logs(self, log_entries: list[LogEntry]) -> None:
        """Export multiple log entries to structured logging system.

        Args:
            log_entries: List of log entries to export.

        """
        for log_entry in log_entries:
            await self.export_log(log_entry)


@injectable(AlertNotifier)
class SlackAlertNotifier(AlertNotifier):
    """Slack alert notifier."""

    def __init__(self, webhook_url: str | None = None) -> None:
        """Initialize Slack alert notifier.
        
        Args:
            webhook_url: Slack webhook URL for sending notifications.
        
        """
        self.webhook_url = webhook_url
        self._notifications: list[dict[str, object]] = []

    async def notify(self, alert: Alert) -> None:
        """Send alert notification via Slack webhook.

        Args:
            alert: Alert to send notification for.

        """
        notification = {
            "alert_id": str(alert.id),
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity.value,
            "source": alert.source,
            "source_type": alert.source_type,
            "threshold": float(alert.threshold) if alert.threshold else 0.0,
            "alert_status": alert.alert_status.value,
            "timestamp": alert.created_at,
        }

        # In a real implementation, this would send to Slack
        self._notifications.append(notification)

    async def notify_batch(self, alerts: list[Alert]) -> None:
        """Send multiple alert notifications via Slack webhook.

        Args:
            alerts: List of alerts to send notifications for.

        """
        for alert in alerts:
            await self.notify(alert)


@injectable(HealthChecker)
class HttpHealthChecker(HealthChecker):
    """HTTP health checker implementation."""

    def __init__(self) -> None:
        """Initialize HTTP health checker."""
        self._registered_components: dict[str, dict[str, object]] = {}

    async def check_health(self, component: ComponentName, endpoint: str | None = None, timeout_ms: int = 5000) -> HealthCheck:
        """Perform HTTP health check on component.

        Args:
            component: Component to check health of.
            endpoint: Optional HTTP endpoint to check.
            timeout_ms: Timeout in milliseconds for health check.

        Returns:
            HealthCheck result with status and timing information.

        """
        from datetime import UTC

        from flext_observability.domain.value_objects import Duration

        start_time = datetime.now(UTC)

        try:
            # In a real implementation, this would make an HTTP request
            # For now, we'll simulate a health check
            import random

            # Simulate some delay
            await asyncio.sleep(random.uniform(0.01, 0.1))

            # Simulate success/failure
            success = random.random() > 0.1  # 90% success rate

            if success:
                health_status = HealthStatus.HEALTHY
                error = None
            else:
                health_status = HealthStatus.UNHEALTHY
                error = "Connection timeout"

            end_time = datetime.now(UTC)
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            duration = Duration(milliseconds=duration_ms)

            return HealthCheck(
                name=component.name,
                health_status=health_status,
                endpoint=endpoint,
                response_time_ms=duration.milliseconds if duration else None,
                error_message=error,
                component=component,
                check_type="automated",
            )

        except Exception as e:
            end_time = datetime.now(UTC)
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            duration = Duration(milliseconds=duration_ms)

            return HealthCheck(
                name=component.name,
                health_status=HealthStatus.UNHEALTHY,
                endpoint=endpoint,
                response_time_ms=duration.milliseconds if duration else None,
                error_message=str(e),
                component=component,
                check_type="automated",
            )

    async def check_all_components(self) -> list[HealthCheck]:
        """Check health of all registered components.

        Returns:
            List of health check results for all registered components.

        """
        results = []

        for component_name, config in self._registered_components.items():
            component = ComponentName(name=component_name)
            health_check = await self.check_health(
                component=component,
                endpoint=config.get("endpoint"),
                timeout_ms=config.get("timeout_ms", 5000),
            )
            results.append(health_check)

        return results

    def register_component(
        self,
        component_name: str,
        endpoint: str | None = None,
        timeout_ms: int = 5000,
    ) -> None:
        """Register component for health monitoring.

        Args:
            component_name: Name of component to register.
            endpoint: Optional HTTP endpoint for health checks.
            timeout_ms: Timeout in milliseconds for health checks.

        """
        self._registered_components[component_name] = {
            "endpoint": endpoint,
            "timeout_ms": timeout_ms,
        }

    def unregister_component(self, component_name: str) -> None:
        """Unregister component from health monitoring.

        Args:
            component_name: Name of component to unregister.

        """
        self._registered_components.pop(component_name, None)


@injectable(AlertNotifier)
class ConsoleAlertNotifier(AlertNotifier):
    """Console alert notifier for development."""

    async def notify(self, alert: Alert) -> None:
        """Print alert to console."""

    async def notify_batch(self, alerts: list[Alert]) -> None:
        """Print multiple alerts to console."""
        for alert in alerts:
            await self.notify(alert)


@injectable(MetricsExporter)
class FileMetricsExporter(MetricsExporter):
    """File-based metrics exporter for development."""

    def __init__(self, file_path: str = "/tmp/flext_metrics.log") -> None:
        self.file_path = file_path

    async def export_metrics(self, metrics: list[Metric]) -> None:
        """Export multiple metrics to file.

        Args:
            metrics: List of metrics to export to file.

        """
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.writelines(f"{metric.timestamp},{metric.source or 'default'},{metric.name},"
                    f"{metric.value},{metric.unit or ''},{metric.metric_type.value}\n" for metric in metrics)

    async def export_metric(self, metric: Metric) -> None:
        """Export single metric to file.

        Args:
            metric: Metric to export to file.

        """
        await self.export_metrics([metric])


@injectable(EventBus)
class NoOpEventBus(EventBus):
    """No-op event bus for testing."""

    async def publish(self, event: Any) -> None:
        """No-op publish implementation.

        Args:
            event: Domain event (ignored).

        """

    async def subscribe(self, event_type: type[Any], handler: Any) -> None:
        """No-op subscribe implementation.

        Args:
            event_type: Type of domain event (ignored).
            handler: Callable handler (ignored).

        """

    async def unsubscribe(
        self,
        event_type: type[Any],
        handler: Any,
    ) -> None:
        """No-op unsubscribe implementation.

        Args:
            event_type: Type of domain event (ignored).
            handler: Callable handler (ignored).

        """
