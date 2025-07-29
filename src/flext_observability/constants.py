"""FLEXT Observability Constants - Simplified constants using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Constants simplificadas usando apenas o essencial do flext-core.
"""

from __future__ import annotations

from typing import ClassVar

# ============================================================================
# CORE OBSERVABILITY CONSTANTS
# ============================================================================


class ObservabilityConstants:
    """Core constants for observability system."""

    NAME = "flext-observability"
    VERSION = "1.0.0"

    # Log levels
    LOG_LEVELS: ClassVar[list[str]] = [
        "debug", "info", "warning", "error", "critical",
    ]

    # Metric types
    METRIC_TYPES: ClassVar[list[str]] = [
        "counter", "gauge", "histogram", "summary",
    ]

    # Alert severities
    ALERT_SEVERITIES: ClassVar[list[str]] = [
        "low", "medium", "high", "critical", "emergency",
    ]

    # Health statuses
    HEALTH_STATUSES: ClassVar[list[str]] = [
        "healthy", "unhealthy", "degraded", "unknown",
    ]

    # Alert statuses
    ALERT_STATUSES: ClassVar[list[str]] = [
        "active", "resolved", "escalated", "suppressed",
    ]


# Default configuration
DEFAULT_OBSERVABILITY_CONFIG: dict[str, object] = {
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
    """Metric type constants for observability."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertStatus:
    """Alert status constants for observability."""

    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    SUPPRESSED = "suppressed"


class HealthStatus:
    """Health status constants for observability."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class TraceStatus:
    """Trace status constants for observability."""

    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
