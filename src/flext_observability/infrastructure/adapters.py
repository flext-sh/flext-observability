"""Infrastructure adapters for external systems."""

from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING
from typing import Any

from flext_core.config.base import injectable
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.value_objects import ComponentName
from flext_observability.domain.value_objects import HealthStatus
from flext_observability.infrastructure.ports import AlertNotifier
from flext_observability.infrastructure.ports import EventBus
from flext_observability.infrastructure.ports import HealthChecker
from flext_observability.infrastructure.ports import LogExporter
from flext_observability.infrastructure.ports import MetricsExporter
from flext_observability.infrastructure.ports import TraceExporter

if TYPE_CHECKING:
    from flext_observability.domain.entities import Alert
    from flext_observability.domain.entities import LogEntry
    from flext_observability.domain.entities import Metric
    from flext_observability.domain.entities import Trace
    from flext_observability.domain.events import DomainEvent


@injectable(EventBus)
class InMemoryEventBus(EventBus):
    """In-memory event bus implementation."""

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[callable]] = {}

    async def publish(self, event: DomainEvent) -> None:
        """Publish a domain event."""
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception:
                # Log error but don't stop processing
                pass

    async def subscribe(self, event_type: type[DomainEvent], handler: callable) -> None:
        """Subscribe to domain events."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def unsubscribe(self, event_type: type[DomainEvent], handler: callable) -> None:
        """Unsubscribe from domain events."""
        if event_type in self._handlers:
            with contextlib.suppress(ValueError):
                self._handlers[event_type].remove(handler)


@injectable(MetricsExporter)
class PrometheusMetricsExporter(MetricsExporter):
    """Prometheus metrics exporter."""

    def __init__(self) -> None:
        self._metrics_registry: dict[str, Any] = {}

    async def export_metrics(self, metrics: list[Metric]) -> None:
        """Export metrics to Prometheus."""
        for metric in metrics:
            await self.export_metric(metric)

    async def export_metric(self, metric: Metric) -> None:
        """Export single metric to Prometheus."""
        # In a real implementation, this would create Prometheus metrics
        # For now, we'll just store them in memory
        metric_key = f"{metric.component.full_name}.{metric.name}"
        self._metrics_registry[metric_key] = {
            "value": float(metric.value.value),
            "unit": metric.value.unit,
            "type": metric.metric_type.value,
            "timestamp": metric.timestamp,
            "tags": metric.tags,
        }


@injectable(TraceExporter)
class OpenTelemetryTraceExporter(TraceExporter):
    """OpenTelemetry trace exporter."""

    def __init__(self) -> None:
        self._traces: list[dict[str, Any]] = []

    async def export_trace(self, trace: Trace) -> None:
        """Export trace to OpenTelemetry."""
        trace_data = {
            "trace_id": trace.trace_id.trace_id,
            "span_id": trace.trace_id.span_id,
            "operation_name": trace.operation_name,
            "component": trace.component.full_name,
            "status": trace.status.value,
            "start_time": trace.start_time,
            "end_time": trace.end_time,
            "duration_ms": trace.duration.milliseconds if trace.duration else None,
            "tags": trace.tags,
            "logs": trace.logs,
            "error": trace.error,
        }
        self._traces.append(trace_data)

    async def export_traces(self, traces: list[Trace]) -> None:
        """Export multiple traces to OpenTelemetry."""
        for trace in traces:
            await self.export_trace(trace)


@injectable(LogExporter)
class StructlogLogAdapter(LogExporter):
    """Structlog log adapter."""

    def __init__(self) -> None:
        self._logs: list[dict[str, Any]] = []

    async def export_log(self, log_entry: LogEntry) -> None:
        """Export log entry to structlog."""
        log_data = {
            "level": log_entry.level.value,
            "message": log_entry.message,
            "component": log_entry.component.full_name,
            "timestamp": log_entry.created_at,
            "correlation_id": log_entry.correlation_id,
            "trace_id": log_entry.trace_id,
            "span_id": log_entry.span_id,
            "fields": log_entry.fields,
            "exception": log_entry.exception,
        }
        self._logs.append(log_data)

    async def export_logs(self, log_entries: list[LogEntry]) -> None:
        """Export multiple log entries to structlog."""
        for log_entry in log_entries:
            await self.export_log(log_entry)


@injectable(AlertNotifier)
class SlackAlertNotifier(AlertNotifier):
    """Slack alert notifier."""

    def __init__(self, webhook_url: str | None = None) -> None:
        self.webhook_url = webhook_url
        self._notifications: list[dict[str, Any]] = []

    async def notify(self, alert: Alert) -> None:
        """Send alert notification to Slack."""
        notification = {
            "alert_id": str(alert.id),
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity.value,
            "component": alert.metric.component.full_name,
            "metric_name": alert.metric.name,
            "metric_value": float(alert.metric.value.value),
            "threshold": float(alert.threshold.value),
            "timestamp": alert.created_at,
        }

        # In a real implementation, this would send to Slack
        self._notifications.append(notification)

    async def notify_batch(self, alerts: list[Alert]) -> None:
        """Send batch of alert notifications to Slack."""
        for alert in alerts:
            await self.notify(alert)


@injectable(HealthChecker)
class HttpHealthChecker(HealthChecker):
    """HTTP health checker implementation."""

    def __init__(self) -> None:
        self._registered_components: dict[str, dict[str, Any]] = {}

    async def check_health(
        self,
        component: ComponentName,
        endpoint: str | None = None,
        timeout_ms: int = 5000,
    ) -> HealthCheck:
        """Perform health check for a component."""
        from datetime import UTC
        from datetime import datetime

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
                status = HealthStatus.HEALTHY
                message = "Component is healthy"
                error = None
            else:
                status = HealthStatus.UNHEALTHY
                message = "Component health check failed"
                error = "Connection timeout"

            end_time = datetime.now(UTC)
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            duration = Duration(milliseconds=duration_ms)

            return HealthCheck(
                component=component,
                status=status,
                message=message,
                duration=duration,
                endpoint=endpoint,
                error=error,
            )

        except Exception as e:
            end_time = datetime.now(UTC)
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            duration = Duration(milliseconds=duration_ms)

            return HealthCheck(
                component=component,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {e}",
                duration=duration,
                endpoint=endpoint,
                error=str(e),
            )

    async def check_all_components(self) -> list[HealthCheck]:
        """Check health of all registered components."""
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
        """Register a component for health checking."""
        self._registered_components[component_name] = {
            "endpoint": endpoint,
            "timeout_ms": timeout_ms,
        }

    def unregister_component(self, component_name: str) -> None:
        """Unregister a component."""
        self._registered_components.pop(component_name, None)


@injectable()
class ConsoleAlertNotifier(AlertNotifier):
    """Console alert notifier for development."""

    async def notify(self, alert: Alert) -> None:
        """Print alert to console."""

    async def notify_batch(self, alerts: list[Alert]) -> None:
        """Print batch of alerts to console."""
        for alert in alerts:
            await self.notify(alert)


@injectable()
class FileMetricsExporter(MetricsExporter):
    """File-based metrics exporter for development."""

    def __init__(self, file_path: str = "/tmp/flext_metrics.log") -> None:
        self.file_path = file_path

    async def export_metrics(self, metrics: list[Metric]) -> None:
        """Export metrics to file."""
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.writelines(f"{metric.timestamp},{metric.component.full_name},{metric.name},"
                       f"{metric.value.value},{metric.value.unit},{metric.metric_type.value}\n" for metric in metrics)

    async def export_metric(self, metric: Metric) -> None:
        """Export single metric to file."""
        await self.export_metrics([metric])


@injectable()
class NoOpEventBus(EventBus):
    """No-op event bus for testing."""

    async def publish(self, event: DomainEvent) -> None:
        """Do nothing."""

    async def subscribe(self, event_type: type[DomainEvent], handler: callable) -> None:
        """Do nothing."""

    async def unsubscribe(self, event_type: type[DomainEvent], handler: callable) -> None:
        """Do nothing."""
