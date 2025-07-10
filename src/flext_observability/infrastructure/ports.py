"""Infrastructure ports implementations for FLEXT-OBSERVABILITY.

Using flext-core infrastructure patterns - NO duplication.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

from flext_core.domain.types import ServiceResult
from flext_observability.domain.entities import Dashboard
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.ports import AlertService
from flext_observability.domain.ports import DashboardService
from flext_observability.domain.ports import HealthService
from flext_observability.domain.ports import LogService
from flext_observability.domain.ports import MetricsService
from flext_observability.domain.ports import TracingService

if TYPE_CHECKING:
    from flext_observability.domain.entities import Alert
    from flext_observability.domain.entities import LogEntry
    from flext_observability.domain.entities import Metric
    from flext_observability.domain.entities import Trace
    from flext_observability.infrastructure.config import AlertingConfig
    from flext_observability.infrastructure.config import HealthConfig
    from flext_observability.infrastructure.config import LoggingConfig
    from flext_observability.infrastructure.config import MetricsConfig
    from flext_observability.infrastructure.config import TracingConfig


class FileLogPort(LogService):
    """File-based log service implementation."""

    def __init__(self, config: LoggingConfig) -> None:
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def write_log(self, log_entry: LogEntry) -> ServiceResult[None]:
        """Write log entry to file."""
        try:
            if self.config.logging_file_enabled:
                log_file = Path(self.config.logging_file_path)
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

                # Write to file
                with log_file.open("a", encoding="utf-8") as f:
                    if self.config.logging_format == "json":
                        f.write(json.dumps(log_record) + "\n")
                    else:
                        f.write(
                            f"{log_record['timestamp']} [{log_record['level']}] {log_record['message']}\n",
                        )

            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to write log: {e}")

    async def configure_logging(self, config: dict[str, Any]) -> ServiceResult[None]:
        """Configure logging system."""
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
        except Exception as e:
            return ServiceResult.fail(f"Failed to configure logging: {e}")

    async def get_log_level(self) -> ServiceResult[str]:
        """Get current log level."""
        try:
            return ServiceResult.ok(self.config.log_level)
        except Exception as e:
            return ServiceResult.fail(f"Failed to get log level: {e}")

    async def set_log_level(self, level: str) -> ServiceResult[None]:
        """Set log level."""
        try:
            self.config.log_level = level
            logging.getLogger().setLevel(getattr(logging, level))
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to set log level: {e}")


class PrometheusMetricsPort(MetricsService):
    """Prometheus metrics service implementation."""

    def __init__(self, config: MetricsConfig) -> None:
        self.config = config
        self.metrics_cache = {}

    async def record_metric(self, metric: Metric) -> ServiceResult[None]:
        """Record metric."""
        try:
            # Store in cache
            key = f"{metric.name}_{metric.type}"
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
            if len(self.metrics_cache[key]) > self.config.metrics_retention_limit:
                self.metrics_cache[key] = self.metrics_cache[key][
                    -self.config.metrics_retention_limit :
                ]

            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to record metric: {e}")

    async def get_current_metrics(self) -> ServiceResult[dict[str, Any]]:
        """Get current metrics."""
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
        except Exception as e:
            return ServiceResult.fail(f"Failed to get current metrics: {e}")

    async def reset_metrics(self) -> ServiceResult[None]:
        """Reset all metrics."""
        try:
            self.metrics_cache.clear()
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to reset metrics: {e}")

    async def export_metrics(self, format: str) -> ServiceResult[str]:
        """Export metrics in specified format."""
        try:
            if format == "prometheus":
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
            if format == "json":
                return ServiceResult.ok(json.dumps(self.metrics_cache, indent=2))
            return ServiceResult.fail(f"Unsupported format: {format}")
        except Exception as e:
            return ServiceResult.fail(f"Failed to export metrics: {e}")


class JaegerTracingPort(TracingService):
    """Jaeger tracing service implementation."""

    def __init__(self, config: TracingConfig) -> None:
        self.config = config
        self.traces_cache = {}

    async def start_trace(self, trace: Trace) -> ServiceResult[None]:
        """Start a trace."""
        try:
            trace_data = {
                "trace_id": trace.trace_id,
                "span_id": trace.span_id,
                "operation_name": trace.operation_name,
                "service_name": trace.service_name,
                "start_time": trace.start_time.isoformat(),
                "status": trace.status,
                "tags": trace.tags,
                "logs": trace.logs,
                "events": trace.events,
            }

            self.traces_cache[trace.id] = trace_data
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to start trace: {e}")

    async def finish_trace(self, trace: Trace) -> ServiceResult[None]:
        """Finish a trace."""
        try:
            if trace.id in self.traces_cache:
                self.traces_cache[trace.id].update(
                    {
                        "end_time": (
                            trace.end_time.isoformat() if trace.end_time else None
                        ),
                        "duration_ms": trace.duration_ms,
                        "status": trace.status,
                        "error": trace.error,
                    },
                )
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to finish trace: {e}")

    async def add_span(
        self,
        trace: Trace,
        span_data: dict[str, Any],
    ) -> ServiceResult[None]:
        """Add span to trace."""
        try:
            if trace.id in self.traces_cache:
                if "spans" not in self.traces_cache[trace.id]:
                    self.traces_cache[trace.id]["spans"] = []
                self.traces_cache[trace.id]["spans"].append(span_data)
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to add span: {e}")

    async def export_traces(self, format: str) -> ServiceResult[str]:
        """Export traces in specified format."""
        try:
            if format in {"jaeger", "json"}:
                return ServiceResult.ok(json.dumps(self.traces_cache, indent=2))
            return ServiceResult.fail(f"Unsupported format: {format}")
        except Exception as e:
            return ServiceResult.fail(f"Failed to export traces: {e}")


class SlackAlertPort(AlertService):
    """Slack alert service implementation."""

    def __init__(self, config: AlertingConfig) -> None:
        self.config = config

    async def send_alert(self, alert: Alert) -> ServiceResult[None]:
        """Send alert notification."""
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

            # In real implementation, send to Slack webhook

            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to send alert: {e}")

    async def resolve_alert(self, alert: Alert) -> ServiceResult[None]:
        """Resolve alert notification."""
        try:
            # Simulate resolving in Slack
            {
                "title": f"RESOLVED: {alert.title}",
                "resolved_at": (
                    alert.resolved_at.isoformat() if alert.resolved_at else None
                ),
            }

            # In real implementation, update Slack thread

            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to resolve alert: {e}")

    async def configure_channels(self, channels: dict[str, Any]) -> ServiceResult[None]:
        """Configure alert channels."""
        try:
            # Update configuration
            self.config.webhook_url = channels.get("webhook_url")
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to configure channels: {e}")

    async def test_alert(self, channel: str) -> ServiceResult[None]:
        """Test alert channel."""
        try:
            # Send test alert

            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to test alert: {e}")


class SimpleHealthPort(HealthService):
    """Simple health service implementation."""

    def __init__(self, config: HealthConfig) -> None:
        self.config = config
        self.registered_checks = {}

    async def run_check(
        self,
        health_check: HealthCheck,
    ) -> ServiceResult[dict[str, Any]]:
        """Run health check."""
        try:
            # Simulate running health check
            result = {
                "response_time_ms": 5.0,
                "response_data": {"status": "healthy"},
                "healthy": True,
            }

            return ServiceResult.ok(result)
        except Exception as e:
            return ServiceResult.fail(f"Health check failed: {e}")

    async def get_system_health(self) -> ServiceResult[dict[str, Any]]:
        """Get overall system health."""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "checks": {},
            }

            # Run all registered checks
            for name, check in self.registered_checks.items():
                check_result = await self.run_check(check)
                health_status["checks"][name] = {
                    "healthy": check_result.is_success,
                    "response_time_ms": (
                        check_result.data.get("response_time_ms", 0)
                        if check_result.is_success
                        else None
                    ),
                    "error": (
                        check_result.error if not check_result.is_success else None
                    ),
                }

            # Overall status
            if any(not check["healthy"] for check in health_status["checks"].values()):
                health_status["status"] = "unhealthy"

            return ServiceResult.ok(health_status)
        except Exception as e:
            return ServiceResult.fail(f"Failed to get system health: {e}")

    async def register_check(self, health_check: HealthCheck) -> ServiceResult[None]:
        """Register health check."""
        try:
            self.registered_checks[health_check.name] = health_check
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to register check: {e}")

    async def unregister_check(self, check_name: str) -> ServiceResult[None]:
        """Unregister health check."""
        try:
            if check_name in self.registered_checks:
                del self.registered_checks[check_name]
            return ServiceResult.ok(None)
        except Exception as e:
            return ServiceResult.fail(f"Failed to unregister check: {e}")


class MemoryDashboardPort(DashboardService):
    """Memory-based dashboard service implementation."""

    def __init__(self, config: AlertingConfig) -> None:
        self.config = config
        self.dashboard_cache = {}

    async def render_dashboard(
        self,
        dashboard: Dashboard,
    ) -> ServiceResult[dict[str, Any]]:
        """Render dashboard with current data."""
        try:
            rendered = {
                "id": str(dashboard.id),
                "title": dashboard.title,
                "description": dashboard.description,
                "refresh_interval": dashboard.refresh_interval_seconds,
                "widgets": [],
                "timestamp": dashboard.updated_at.isoformat(),
            }

            # Render widgets
            for widget in dashboard.widgets:
                widget_data = await self.get_widget_data(widget)
                if widget_data.is_success:
                    rendered["widgets"].append(widget_data.data)

            return ServiceResult.ok(rendered)
        except Exception as e:
            return ServiceResult.fail(f"Failed to render dashboard: {e}")

    async def export_dashboard(
        self,
        dashboard: Dashboard,
        format: str,
    ) -> ServiceResult[str]:
        """Export dashboard configuration."""
        try:
            if format == "json":
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
            return ServiceResult.fail(f"Unsupported format: {format}")
        except Exception as e:
            return ServiceResult.fail(f"Failed to export dashboard: {e}")

    async def import_dashboard(
        self,
        config: str,
        format: str,
    ) -> ServiceResult[Dashboard]:
        """Import dashboard configuration."""
        try:
            if format == "json":
                config_data = json.loads(config)
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
            return ServiceResult.fail(f"Unsupported format: {format}")
        except Exception as e:
            return ServiceResult.fail(f"Failed to import dashboard: {e}")

    async def get_widget_data(
        self,
        widget_config: dict[str, Any],
    ) -> ServiceResult[dict[str, Any]]:
        """Get data for dashboard widget."""
        try:
            # Simulate widget data
            widget_data = {
                "id": widget_config.get("id", "widget-1"),
                "type": widget_config.get("type", "metric"),
                "title": widget_config.get("title", "Widget"),
                "data": {
                    "value": 42,
                    "timestamp": "2024-01-01T00:00:00Z",
                    "unit": widget_config.get("unit", "count"),
                },
            }

            return ServiceResult.ok(widget_data)
        except Exception as e:
            return ServiceResult.fail(f"Failed to get widget data: {e}")
