"""Observability constants following flext-core patterns.

Constants for observability domain including metric types, alert levels,
trace statuses, and configuration defaults.
"""

from __future__ import annotations

from flext_core import FlextConstants


class ObservabilityConstants(FlextConstants):
    """Observability-specific constants extending flext-core patterns."""

    # Metric types
    METRIC_TYPE_COUNTER = "counter"
    METRIC_TYPE_GAUGE = "gauge"
    METRIC_TYPE_HISTOGRAM = "histogram"
    METRIC_TYPE_SUMMARY = "summary"

    # Alert levels
    ALERT_LEVEL_INFO = "info"
    ALERT_LEVEL_WARNING = "warning"
    ALERT_LEVEL_ERROR = "error"
    ALERT_LEVEL_CRITICAL = "critical"

    # Trace statuses
    TRACE_STATUS_STARTED = "started"
    TRACE_STATUS_RUNNING = "running"
    TRACE_STATUS_COMPLETED = "completed"
    TRACE_STATUS_FAILED = "failed"

    # Health check statuses
    HEALTH_STATUS_HEALTHY = "healthy"
    HEALTH_STATUS_DEGRADED = "degraded"
    HEALTH_STATUS_UNHEALTHY = "unhealthy"

    # Default values
    DEFAULT_METRIC_UNIT = "count"
    DEFAULT_TRACE_TIMEOUT = 30.0
    DEFAULT_HEALTH_CHECK_INTERVAL = 60.0

    # Service names
    SERVICE_METRICS = "metrics"
    SERVICE_TRACING = "tracing"
    SERVICE_ALERTS = "alerts"
    SERVICE_HEALTH = "health"
    SERVICE_LOGGING = "logging"


__all__ = ["ObservabilityConstants"]
