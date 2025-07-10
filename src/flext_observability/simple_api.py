"""Simple API for easy adoption of observability features."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any
from typing import Self

from flext_core.config import get_container
from flext_core.domain.types import LogLevel
from flext_core.domain.types import MetricType
from flext_observability.application import AlertService
from flext_observability.application import HealthMonitoringService
from flext_observability.application import LoggingService
from flext_observability.application import MetricsService
from flext_observability.application import TracingService
from flext_observability.config import get_settings
from flext_observability.domain.services import AlertingService
from flext_observability.domain.services import HealthAnalysisService
from flext_observability.domain.services import LogAnalysisService
from flext_observability.domain.services import MetricsAnalysisService
from flext_observability.domain.services import TraceAnalysisService
from flext_observability.infrastructure import InMemoryAlertRepository
from flext_observability.infrastructure import InMemoryEventBus
from flext_observability.infrastructure import InMemoryHealthRepository
from flext_observability.infrastructure import InMemoryLogRepository
from flext_observability.infrastructure import InMemoryMetricsRepository
from flext_observability.infrastructure import InMemoryTraceRepository

# Global service instances
_services: dict[type, Any] = {}


def _get_service(service_type: type) -> Any:
    """Get or create a service instance."""
    if service_type not in _services:
        container = get_container()
        _services[service_type] = container.resolve(service_type)
    return _services[service_type]


def setup_observability(
    enable_metrics: bool = True,
    enable_alerts: bool = True,
    enable_health_checks: bool = True,
    enable_logging: bool = True,
    enable_tracing: bool = True,
) -> None:
    """Setup observability services with default configuration."""
    get_settings()
    container = get_container()

    # Register repositories
    if enable_metrics:
        container.register(MetricsService, MetricsService(
            metrics_repository=InMemoryMetricsRepository(),
            metrics_analysis_service=MetricsAnalysisService(),
            event_bus=InMemoryEventBus(),
        ))

    if enable_alerts:
        container.register(AlertService, AlertService(
            alert_repository=InMemoryAlertRepository(),
            alerting_service=AlertingService(),
            event_bus=InMemoryEventBus(),
        ))

    if enable_health_checks:
        container.register(HealthMonitoringService, HealthMonitoringService(
            health_repository=InMemoryHealthRepository(),
            health_analysis_service=HealthAnalysisService(),
            event_bus=InMemoryEventBus(),
        ))

    if enable_logging:
        container.register(LoggingService, LoggingService(
            log_repository=InMemoryLogRepository(),
            log_analysis_service=LogAnalysisService(),
            event_bus=InMemoryEventBus(),
        ))

    if enable_tracing:
        container.register(TracingService, TracingService(
            trace_repository=InMemoryTraceRepository(),
            trace_analysis_service=TraceAnalysisService(),
            event_bus=InMemoryEventBus(),
        ))


def collect_metric(
    name: str,
    value: float,
    unit: str = "count",
    metric_type: MetricType = MetricType.GAUGE,
    component_name: str = "default",
    component_namespace: str = "default",
    tags: dict[str, str] | None = None,
) -> bool:
    """Collect a metric value."""
    try:
        service = _get_service(MetricsService)
        result = asyncio.run(service.collect_metric(
            name=name,
            value=value,
            unit=unit,
            metric_type=metric_type,
            component_name=component_name,
            component_namespace=component_namespace,
            tags=tags,
        ))
        return result.success
    except Exception:
        return False


def create_alert(
    title: str,
    description: str,
    severity: str = "warning",
    component_name: str = "default",
    component_namespace: str = "default",
) -> bool:
    """Create an alert."""
    try:
        # This would typically be triggered by metric evaluation
        # For now, we'll create a simple metric and evaluate it
        collect_metric(
            name=f"alert_trigger_{title.lower().replace(' ', '_')}",
            value=1.0,
            component_name=component_name,
            component_namespace=component_namespace,
        )
        return True
    except Exception:
        return False


def log_message(
    message: str,
    level: LogLevel = LogLevel.INFO,
    component_name: str = "default",
    component_namespace: str = "default",
    correlation_id: str | None = None,
    trace_id: str | None = None,
    span_id: str | None = None,
    fields: dict[str, Any] | None = None,
    exception: str | None = None,
) -> bool:
    """Log a structured message."""
    try:
        service = _get_service(LoggingService)
        result = asyncio.run(service.create_log_entry(
            level=level,
            message=message,
            component_name=component_name,
            component_namespace=component_namespace,
            correlation_id=correlation_id,
            trace_id=trace_id,
            span_id=span_id,
            fields=fields,
            exception=exception,
        ))
        return result.success
    except Exception:
        return False


def start_trace(
    operation_name: str,
    component_name: str = "default",
    component_namespace: str = "default",
    tags: dict[str, str] | None = None,
) -> str | None:
    """Start a new trace and return trace ID."""
    try:
        service = _get_service(TracingService)
        result = asyncio.run(service.start_trace(
            operation_name=operation_name,
            component_name=component_name,
            component_namespace=component_namespace,
            tags=tags,
        ))
        if result.success and result.data:
            return result.data.trace_id.trace_id
        return None
    except Exception:
        return None


def complete_trace(
    trace_id: str,
    success: bool = True,
    error: str | None = None,
) -> bool:
    """Complete a trace."""
    try:
        service = _get_service(TracingService)
        result = asyncio.run(service.complete_trace(
            trace_id=trace_id,
            success=success,
            error=error,
        ))
        return result.success
    except Exception:
        return False


def check_health(
    component_name: str = "default",
    component_namespace: str = "default",
    endpoint: str | None = None,
    timeout_ms: int = 5000,
) -> bool:
    """Perform a health check."""
    try:
        service = _get_service(HealthMonitoringService)
        result = asyncio.run(service.perform_health_check(
            component_name=component_name,
            component_namespace=component_namespace,
            endpoint=endpoint,
            timeout_ms=timeout_ms,
        ))
        return result.success and result.data and result.data.is_healthy
    except Exception:
        return False


def get_system_overview() -> dict[str, Any]:
    """Get system overview with key metrics."""
    try:
        overview = {
            "status": "healthy",
            "components": 0,
            "active_alerts": 0,
            "recent_errors": 0,
            "active_traces": 0,
        }

        # Get system health
        try:
            health_service = _get_service(HealthMonitoringService)
            health_result = asyncio.run(health_service.get_system_health())
            if health_result.success and health_result.data:
                overview["status"] = health_result.data["overall_status"].value
                overview["components"] = health_result.data["total_components"]
        except Exception:
            pass

        # Get active alerts
        try:
            alert_service = _get_service(AlertService)
            alerts_result = asyncio.run(alert_service.get_active_alerts())
            if alerts_result.success and alerts_result.data:
                overview["active_alerts"] = len(alerts_result.data)
        except Exception:
            pass

        # Get recent errors (last hour)
        try:
            log_service = _get_service(LoggingService)
            from datetime import timedelta
            start_time = datetime.now() - timedelta(hours=1)
            logs_result = asyncio.run(log_service.get_logs(
                level=LogLevel.ERROR,
                start_time=start_time,
                limit=100,
            ))
            if logs_result.success and logs_result.data:
                overview["recent_errors"] = len(logs_result.data)
        except Exception:
            pass

        return overview

    except Exception:
        return {
            "status": "unknown",
            "components": 0,
            "active_alerts": 0,
            "recent_errors": 0,
            "active_traces": 0,
        }


# Convenience functions for common log levels
def debug(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log a debug message."""
    return log_message(message, LogLevel.DEBUG, component_name, **kwargs)


def info(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log an info message."""
    return log_message(message, LogLevel.INFO, component_name, **kwargs)


def warning(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log a warning message."""
    return log_message(message, LogLevel.WARNING, component_name, **kwargs)


def error(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log an error message."""
    return log_message(message, LogLevel.ERROR, component_name, **kwargs)


def critical(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log a critical message."""
    return log_message(message, LogLevel.CRITICAL, component_name, **kwargs)


# Context manager for tracing
class TraceContext:
    """Context manager for tracing operations."""

    def __init__(
        self,
        operation_name: str,
        component_name: str = "default",
        component_namespace: str = "default",
        tags: dict[str, str] | None = None,
    ) -> None:
        self.operation_name = operation_name
        self.component_name = component_name
        self.component_namespace = component_namespace
        self.tags = tags
        self.trace_id: str | None = None
        self.success = True
        self.error: str | None = None

    def __enter__(self) -> Self:
        """Start the trace."""
        self.trace_id = start_trace(
            operation_name=self.operation_name,
            component_name=self.component_name,
            component_namespace=self.component_namespace,
            tags=self.tags,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Complete the trace."""
        if exc_type is not None:
            self.success = False
            self.error = str(exc_val)

        if self.trace_id:
            complete_trace(
                trace_id=self.trace_id,
                success=self.success,
                error=self.error,
            )

    def add_tag(self, key: str, value: str) -> None:
        """Add a tag to the trace."""
        if self.tags is None:
            self.tags = {}
        self.tags[key] = value

    def log(self, message: str, level: LogLevel = LogLevel.INFO, **kwargs: Any) -> bool:
        """Log a message with trace context."""
        return log_message(
            message=message,
            level=level,
            component_name=self.component_name,
            component_namespace=self.component_namespace,
            trace_id=self.trace_id,
            **kwargs,
        )


def trace(
    operation_name: str,
    component_name: str = "default",
    component_namespace: str = "default",
    tags: dict[str, str] | None = None,
) -> TraceContext:
    """Create a trace context manager."""
    return TraceContext(
        operation_name=operation_name,
        component_name=component_name,
        component_namespace=component_namespace,
        tags=tags,
    )
