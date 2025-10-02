"""Observability constants extending flext-core patterns.

Includes metric types, alert levels, trace statuses, and configuration defaults.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants


class FlextObservabilityConstants(FlextConstants):
    """Observability-specific constants extending flext-core patterns."""

    # Configuration defaults
    DEFAULT_METRICS_NAMESPACE = "flext"
    DEFAULT_SERVICE_NAME = "flext-service"
    DEFAULT_LOG_LEVEL = "INFO"

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

    # Storage limits for metrics service
    MAX_METRICS_STORE_SIZE = 1000
    METRICS_STORE_CLEANUP_SIZE = 500

    # Service names
    SERVICE_METRICS = "metrics"
    SERVICE_TRACING = "tracing"
    SERVICE_ALERTS = "alerts"
    SERVICE_HEALTH = "health"
    SERVICE_LOGGING = "logging"

    # Monitoring endpoints
    # Config-specific defaults
    DEFAULT_METRICS_EXPORT_INTERVAL_SECONDS = 60
    DEFAULT_TRACING_SAMPLING_RATE = 1.0
    DEFAULT_MAX_SPAN_ATTRIBUTES = 128
    DEFAULT_MONITORING_ENDPOINT = "http://localhost:9090"

    # Function argument length constants
    NO_ARGS = 0  # No arguments
    ONE_ARG = 1  # One argument


# Export alias for backward compatibility
# FlextObservabilityConstants is already defined as the class above

__all__ = ["FlextObservabilityConstants"]
