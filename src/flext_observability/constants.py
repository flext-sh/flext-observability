"""FLEXT Observability Constants - Simplified constants using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Constants simplificadas usando apenas o essencial do flext-core.
"""

from __future__ import annotations

from typing import Any

# ============================================================================
# CORE OBSERVABILITY CONSTANTS
# ============================================================================


class ObservabilityConstants:
    """Core constants for observability system."""

    NAME = "flext-observability"
    VERSION = "1.0.0"

    # Log levels
    LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]

    # Metric types
    METRIC_TYPES = ["counter", "gauge", "histogram", "summary"]

    # Alert severities
    ALERT_SEVERITIES = ["low", "medium", "high", "critical", "emergency"]

    # Health statuses
    HEALTH_STATUSES = ["healthy", "unhealthy", "degraded", "unknown"]

    # Alert statuses
    ALERT_STATUSES = ["active", "resolved", "escalated", "suppressed"]


# Default configuration
DEFAULT_OBSERVABILITY_CONFIG: dict[str, Any] = {
    "environment": "development",
    "log_level": "info",
    "metrics_enabled": True,
    "logging_enabled": True,
    "tracing_enabled": True,
    "alerts_enabled": True,
    "health_checks_enabled": True,
}


# Error codes for observability
OBSERVABILITY_ERROR_CODES = {
    "METRICS_VALIDATION": "OBSERVABILITY_METRICS_001",
    "LOGGING_ERROR": "OBSERVABILITY_LOGGING_002",
    "TRACING_ERROR": "OBSERVABILITY_TRACING_003",
    "ALERT_ERROR": "OBSERVABILITY_ALERT_004",
    "HEALTH_CHECK_ERROR": "OBSERVABILITY_HEALTH_005",
    "VALIDATION_ERROR": "OBSERVABILITY_VALIDATION_006",
    "CONFIG_ERROR": "OBSERVABILITY_CONFIG_007",
}


# Simplified enums as classes for compatibility
class MetricType:
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertStatus:
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    SUPPRESSED = "suppressed"


class HealthStatus:
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class TraceStatus:
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
