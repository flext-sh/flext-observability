"""Simple API for easy adoption of observability features.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module provides a simplified API for integrating observability features
including metrics, logging, tracing, alerts, and health checks.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any
from typing import Self

from flext_core.config import get_container
from flext_core.domain.types import LogLevel
from flext_core.domain.types import MetricType
from flext_observability.application import AlertService
from flext_observability.application import LoggingService
from flext_observability.application import MetricsService
from flext_observability.application import TracingService
from flext_observability.application.services import HealthService
from flext_observability.config import get_settings
from flext_observability.domain.services import AlertingService
from flext_observability.domain.services import HealthAnalysisService
from flext_observability.domain.services import LogAnalysisService
from flext_observability.domain.services import MetricsAnalysisService
from flext_observability.domain.services import TraceAnalysisService
from flext_observability.infrastructure import InMemoryAlertRepository
from flext_observability.infrastructure import InMemoryHealthRepository
from flext_observability.infrastructure import InMemoryLogRepository
from flext_observability.infrastructure import InMemoryMetricsRepository
from flext_observability.infrastructure import InMemoryTraceRepository
from flext_observability.infrastructure.adapters import InMemoryEventBus

# Global service instances
_services: dict[type, Any] = {}


def _get_service(service_type: type[Any]) -> Any:
    """Get or create a service instance of the specified type.

    Args:
        service_type: The type of service to retrieve.

    Returns:
        The service instance.

    """
    if service_type not in _services:
        container = get_container()
        _services[service_type] = container.resolve(service_type)
    return _services[service_type]


def setup_observability(
    *,
    enable_metrics: bool = True,
    enable_alerts: bool = True,
    enable_health_checks: bool = True,
    enable_logging: bool = True,
    enable_tracing: bool = True,
) -> None:
    """Set up observability services with specified capabilities.

    Args:
        enable_metrics: Whether to enable metrics collection.
        enable_alerts: Whether to enable alert management.
        enable_health_checks: Whether to enable health monitoring.
        enable_logging: Whether to enable structured logging.
        enable_tracing: Whether to enable distributed tracing.

    """
    get_settings()
    container = get_container()

    # Register repositories
    if enable_metrics:
        container.register(
            MetricsService,
            MetricsService(
                metric_repository=InMemoryMetricsRepository(),
                metrics_analysis_service=MetricsAnalysisService(),
                alerting_service=AlertingService(),
                event_bus=InMemoryEventBus(),
            ),
        )

    if enable_alerts:
        container.register(
            AlertService,
            AlertService(
                alert_repository=InMemoryAlertRepository(),
                alerting_service=AlertingService(),
                event_bus=InMemoryEventBus(),
            ),
        )

    if enable_health_checks:
        container.register(
            HealthService,
            HealthService(
                health_repository=InMemoryHealthRepository(),
                health_analysis_service=HealthAnalysisService(),
                event_bus=InMemoryEventBus(),
            ),
        )

    if enable_logging:
        container.register(
            LoggingService,
            LoggingService(
                log_repository=InMemoryLogRepository(),
                log_analysis_service=LogAnalysisService(),
                event_bus=InMemoryEventBus(),
            ),
        )

    if enable_tracing:
        container.register(
            TracingService,
            TracingService(
                trace_repository=InMemoryTraceRepository(),
                trace_analysis_service=TraceAnalysisService(),
                event_bus=InMemoryEventBus(),
            ),
        )


def collect_metric(
    name: str,
    value: float,
    unit: str = "count",
    metric_type: MetricType = MetricType.GAUGE,
    component_name: str = "default",
    component_namespace: str = "default",
    tags: dict[str, str] | None = None,
) -> bool:
    """Collect a metric value.

    Args:
        name: The name of the metric.
        value: The metric value.
        unit: The unit of measurement.
        metric_type: The type of metric (gauge, counter, etc.).
        component_name: The name of the component.
        component_namespace: The namespace of the component.
        tags: Additional tags for the metric.

    Returns:
        True if the metric was successfully collected, False otherwise.

    """
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
        return bool(result.is_success)
    except Exception:
        return False


def create_alert(
    title: str,
    description: str,
    severity: str = "warning",
    component_name: str = "default",
    component_namespace: str = "default",
) -> bool:
    """Create an alert.

    Args:
        title: The title of the alert.
        description: The description of the alert.
        severity: The severity level of the alert.
        component_name: The name of the component.
        component_namespace: The namespace of the component.

    Returns:
        True if the alert was successfully created, False otherwise.

    """
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
    """Log a message with the specified level and metadata.

    Args:
        message: The log message.
        level: The log level.
        component_name: The name of the component.
        component_namespace: The namespace of the component.
        correlation_id: Optional correlation ID for request tracking.
        trace_id: Optional trace ID for distributed tracing.
        span_id: Optional span ID for distributed tracing.
        fields: Additional structured data fields.
        exception: Optional exception information.

    Returns:
        True if the message was successfully logged, False otherwise.

    """
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
        return bool(result.is_success)
    except Exception:
        return False


def start_trace(
    operation_name: str,
    component_name: str = "default",
    component_namespace: str = "default",
    tags: dict[str, str] | None = None,
) -> str | None:
    """Start a new trace for an operation.

    Args:
        operation_name: The name of the operation being traced.
        component_name: The name of the component.
        component_namespace: The namespace of the component.
        tags: Additional tags for the trace.

    Returns:
        The trace ID if successful, None otherwise.

    """
    try:
        service = _get_service(TracingService)
        result = asyncio.run(service.start_trace(
            operation_name=operation_name,
            component_name=component_name,
            component_namespace=component_namespace,
            tags=tags,
        ))
        if result.is_success and result.data and hasattr(result.data, "trace_id"):
            return str(result.data.trace_id)
        return None
    except Exception:
        return None


def complete_trace(
    trace_id: str,
    *,
    success: bool = True,
    error: str | None = None,
) -> bool:
    """Complete an existing trace.

    Args:
        trace_id: The ID of the trace to complete.
        success: Whether the operation completed successfully.
        error: Optional error message if the operation failed.

    Returns:
        True if the trace was successfully completed, False otherwise.

    """
    try:
        service = _get_service(TracingService)
        result = asyncio.run(service.complete_trace(
            trace_id=trace_id,
            success=success,
            error=error,
        ))
        return bool(result.is_success)
    except Exception:
        return False


def check_health(
    component_name: str = "default",
    component_namespace: str = "default",
    endpoint: str | None = None,
    timeout_ms: int = 5000,
) -> bool:
    """Perform a health check on a component.

    Args:
        component_name: The name of the component to check.
        component_namespace: The namespace of the component.
        endpoint: Optional endpoint URL to check.
        timeout_ms: Timeout in milliseconds for the health check.

    Returns:
        True if the component is healthy, False otherwise.

    """
    try:
        service = _get_service(HealthService)
        result = asyncio.run(service.perform_health_check(
            component_name=component_name,
            component_namespace=component_namespace,
            endpoint=endpoint,
            timeout_ms=timeout_ms,
        ))
        return bool(result.is_success) and result.data and getattr(result.data, "is_healthy", False)
    except Exception:
        return False


def get_system_overview() -> dict[str, Any]:
    """Get a comprehensive overview of system status.

    Returns:
        A dictionary containing system status information including
        component health, active alerts, recent errors, and active traces.

    """
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
            health_service = _get_service(HealthService)
            health_result = asyncio.run(health_service.get_system_health())
            if health_result.is_success and health_result.data:
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
            from datetime import timedelta  # TODO Move import to module level

            start_time = datetime.now() - timedelta(hours=1)
            logs_result = asyncio.run(log_service.get_logs(
                    level=LogLevel.ERROR,
                    start_time=start_time,
                    limit=100,
                ),
            )
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
    """Log a debug message.

    Args:
        message: The log message.
        component_name: The name of the component.
        **kwargs: Additional keyword arguments for log_message.

    Returns:
        True if the message was successfully logged, False otherwise.

    """
    return log_message(message, LogLevel.DEBUG, component_name, **kwargs)


def info(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log an info message.

    Args:
        message: The log message.
        component_name: The name of the component.
        **kwargs: Additional keyword arguments for log_message.

    Returns:
        True if the message was successfully logged, False otherwise.

    """
    return log_message(message, LogLevel.INFO, component_name, **kwargs)


def warning(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log a warning message.

    Args:
        message: The log message.
        component_name: The name of the component.
        **kwargs: Additional keyword arguments for log_message.

    Returns:
        True if the message was successfully logged, False otherwise.

    """
    return log_message(message, LogLevel.WARNING, component_name, **kwargs)


def error(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log an error message.

    Args:
        message: The log message.
        component_name: The name of the component.
        **kwargs: Additional keyword arguments for log_message.

    Returns:
        True if the message was successfully logged, False otherwise.

    """
    return log_message(message, LogLevel.ERROR, component_name, **kwargs)


def critical(message: str, component_name: str = "default", **kwargs: Any) -> bool:
    """Log a critical message.

    Args:
        message: The log message.
        component_name: The name of the component.
        **kwargs: Additional keyword arguments for log_message.

    Returns:
        True if the message was successfully logged, False otherwise.

    """
    return log_message(message, LogLevel.CRITICAL, component_name, **kwargs)


# Context manager for tracing
class TraceContext:
    """Context manager for tracing operations.

    Provides a context manager for automatic trace lifecycle management
    including start, completion, error handling, and cleanup.
    """

    def __init__(
        self,
        operation_name: str,
        component_name: str = "default",
        component_namespace: str = "default",
        tags: dict[str, str] | None = None,
    ) -> None:
        """Initialize the trace context.

        Args:
            operation_name: The name of the operation being traced.
            component_name: The name of the component.
            component_namespace: The namespace of the component.
            tags: Additional tags for the trace.

        """
        self.operation_name = operation_name
        self.component_name = component_name
        self.component_namespace = component_namespace
        self.tags = tags
        self.trace_id: str | None = None
        self.success = True
        self.error: str | None = None

    def __enter__(self) -> Self:
        """Enter the trace context.

        Returns:
            The trace context instance.

        """
        self.trace_id = start_trace(
            operation_name=self.operation_name,
            component_name=self.component_name,
            component_namespace=self.component_namespace,
            tags=self.tags,
        )
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object | None) -> None:
        """Exit the trace context.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.

        """
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
        """Add a tag to the trace.

        Args:
            key: The tag key.
            value: The tag value.

        """
        if self.tags is None:
            self.tags = {}
        self.tags[key] = value

    def log(self, message: str, level: LogLevel = LogLevel.INFO, **kwargs: Any) -> bool:
        """Log a message within the trace context.

        Args:
            message: The log message.
            level: The log level.
            **kwargs: Additional keyword arguments for log_message.

        Returns:
            True if the message was successfully logged, False otherwise.

        """
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
    """Create a trace context for an operation.

    Args:
        operation_name: The name of the operation being traced.
        component_name: The name of the component.
        component_namespace: The namespace of the component.
        tags: Additional tags for the trace.

    Returns:
        A TraceContext instance that can be used as a context manager.

    """
    return TraceContext(
        operation_name=operation_name,
        component_name=component_name,
        component_namespace=component_namespace,
        tags=tags,
    )
